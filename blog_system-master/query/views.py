# -*- coding: utf-8 -*-
# 'author':'zlw'


from io import BytesIO

from django.shortcuts import HttpResponse, reverse
from django.http import JsonResponse
from django.db.models import F
from django.db.transaction import atomic

from blog.models import Account, Article, Comment, Profile
from query.tools import build_code_img, switch_like


def validate_img(request):
    # 获取验证码图片函数
    memory = BytesIO()
    random_code, image = build_code_img()
    image.save(memory, 'JPEG')
    request.session['validate_code'] = random_code

    return HttpResponse(memory.getvalue())


def article_list_ajax(request):
    """
    处理客户端通过ajax形式发起的请求。
    注意：此请求必须通过get请求携带请求参数--用户名以明确用户。
    若未提供用户名，将会返回一个空数据
    """

    # 请求必须是ajax形式
    if not request.is_ajax():
        return HttpResponse('无效的请求')

    site_path = request.GET.get('curBlogPath')
    category_name = request.GET.get('categoryName')
    article_list = Article.objects.filter(blog__path=site_path, category__name=category_name)
    response_list = []
    for article in article_list:
        response = dict()
        response[article.title] = article.nid
        response['nid'] = article.nid
        response['title'] = article.title
        response['create_time'] = article.create_time.strftime('%Y-%m-%d %H:%M')
        response['comment_count'] = article.comment_count
        response['like_count'] = article.like_count
        response['dislike_count'] = article.dislike_count
        response['view_count'] = article.view_count
        response_list.append(response)
    return JsonResponse(response_list, safe=False)


def article_like_ajax(request, nid):
    """
    对文章发起ajax表示喜欢或者不喜欢
    此函数用于处理用户提交的ajax请求对文章的喜欢/不喜欢操作。
    操作喜欢/不喜欢的用户应该是已登录用户
    """

    if not request.is_ajax():  # 请求必须是ajax形式
        return HttpResponse('无效请求')

    # 如果用户未登录，发送登录地址
    if not request.user.is_authenticated:
        return JsonResponse({'next': reverse('login')})

    # 数据准备
    article_set = Article.objects.filter(nid=nid)
    dic = request.GET
    user_choice = True if dic.get('like') == 'true' else False
    user = Account.objects.filter(username=request.user.username).first()

    # 切换选择
    switch_like(user, article_set, user_choice)

    # 返回客户端数据
    response = {
        'like_count': article_set.first().like_count,
        'dislike_count': article_set.first().dislike_count,
    }
    return JsonResponse(response)


def add_comment(request):
    """评论增加接口 """

    if not request.is_ajax():
        return HttpResponse('无效请求')

    if not request.user.is_authenticated:
        return JsonResponse({'next': reverse('login')})

    # 解析用户提交的数据, 获取用户提交的评论数据，并插入数据库记录
    dic = request.POST
    user = request.user
    root_id = dic.get('root_id')
    root_id = int(root_id) if root_id else None
    article_id = int(dic.get('article_id'))
    article = Article.objects.filter(nid=article_id).first()
    content = dic.get('content')
    parent_id = dic.get('parent_id')
    parent_id = int(parent_id) if parent_id else None  # 客户传递是'2' 或者 null
    parent = Comment.objects.filter(nid=parent_id).first() if parent_id else None
    # reply_to是回复目标用户的username
    reply_to = dic.get('reply_to')
    reply_to_nick_name = None
    reply_to_user = Account.objects.filter(username=reply_to).first()
    # 是否显示页面的回复按钮
    if not reply_to_user:
        reply_to = None
    else:
        reply_to_nick_name = reply_to_user.profile.nick_name

    with atomic():
        # 新增一个评论记录
        new_comment = Comment.objects.create(user=user, article=article,
                                             content=content, parent=parent,
                                             reply_to=reply_to, root_id=root_id)
        # 更新此记录所属文章 的评论数
        Article.objects.filter(nid=article_id).update(comment_count=F('comment_count') + 1)

    # 返回响应数据
    media_root = '/media/'
    response_data = {
        'nid': new_comment.pk,
        'created_at': new_comment.created_at.strftime('%Y-%m-%d %X'),
        'username': user.username,
        'nick_name': new_comment.user.profile.nick_name,
        'reply_to_nick_name': reply_to_nick_name,
        'avatar': media_root + str(new_comment.user.profile.avatar),
        'root_id': new_comment.root_id or new_comment.nid,  # 如果是根评论，就返回nid作为root_id
    }
    return JsonResponse(response_data)


def comment_list(request):
    """评论列表查看接口
    此函数用于，用户以ajax提交请求，对某一篇文章的评论数据
    """

    if not request.is_ajax():
        return HttpResponse('无效请求')

    dic = request.POST
    article_id = dic.get('article_id')
    article_id = int(article_id) if article_id else None
    article = Article.objects.filter(nid=article_id).first()

    if not article_id or not article:
        return HttpResponse('未找到此文章')

    # 文章id正确, 返回给用户此文章的所有评论记录
    comments = list(Comment.objects. filter(article=article). values(
                            'nid', 'user__profile__nick_name', 'user__profile__avatar', 'content',
                            'created_at', 'parent__nid', 'user__username', 'reply_to', 'root_id'))
    # 处理时间格式和个人头像地址
    media_root = '/media/'
    for comment in comments:
        t = comment.get('created_at')
        link = comment.get('user__profile__avatar')

        comment['user__profile__avatar'] = media_root + link
        comment['created_at'] = t.strftime('%Y-%m-%d %X')
        reply_to_user = Profile.objects.filter(user__username=comment.get('reply_to')).first()
        reply_to_nick_name = None
        if reply_to_user:
            reply_to_nick_name = reply_to_user.nick_name
        comment['reply_to_nick_name'] = reply_to_nick_name
        # 判断是否需要html显示回复按钮
        reply_show = False if comment.get('user__username') == request.user.username else True
        comment['reply_show'] = reply_show
        comment['root_id'] = comment.get('root_id') or comment.get('nid')

    return JsonResponse(comments, safe=False)


def article_attrs(request, nid):
    """
    根据指定的nid请求对应文章的属性数据
    """

    article = Article.objects.filter(nid=nid).first()
    if not article:
        return HttpResponse('此文章不存在')

    response = {
        'comment_count': article.comment_count,
        'like_count': article.like_count,
        'dislike_count': article.dislike_count,
        'view_count': article.view_count,
    }
    return JsonResponse(response)
