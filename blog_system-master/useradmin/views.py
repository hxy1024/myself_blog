# -*- coding: utf-8 -*-
# 'author':'zlw'


from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.transaction import atomic
from django.http import JsonResponse

from useradmin.useradmin_forms import ProfileForm
from blog.models import Article, Blog, Category, Profile
from useradmin.tools import filter_executable_content, switch_category, update_avatar, update_article_img


@login_required
def useradmin(request):
    """
    用户个人博客后台文章管理首页
    管理首页提供了进一步操作和处理的各类接口和链接
    """

    context = {'profile': Profile.objects.filter(user__username=request.user.username).first()}
    return render(request, 'useradmin/home.html', context)


@login_required
def show_articles(request):
    """
    查看用户文章信息
    """

    site_path = request.user.username
    article_list = Article.objects.filter(blog__path=site_path)
    context = {
        'article_list': article_list,
        'profile': Profile.objects.filter(user__username=request.user.username).first()
    }
    return render(request, 'useradmin/show_articles.html', context)


@login_required
def add_article(request):
    """
    用户增加文章视图函数
    此函数的主要功能有如下几项：
    1、负责提供空白表单用于用户增加文章数据
    2、负责接收用户提交的文章数据，并校验数据合法性
    3、对合法的文章数据加入数据库
    """

    blog = Blog.objects.filter(path=request.user.username).first()
    if request.method == 'GET':
        # 提前准备新建文章表单中的分类选择数据
        category_list = Category.objects.filter(blog=blog)
        context = {
            'category_list': category_list,
            'profile': Profile.objects.filter(user__username=request.user.username).first()
        }
        return render(request, 'useradmin/edit_article.html', context)

    else:  # 用户创建了一篇新文章
        dic = request.POST
        file = request.FILES.get('article_img')
        title = dic.get('title')
        content = dic.get('content')
        category_id = int(dic.get('category'))
        category_set = Category.objects.filter(nid=category_id)
        # 对用户提交的文章content和title数据进行过滤，处理可执行标签
        title = filter_executable_content(title)
        content = filter_executable_content(content)

        with atomic():
            # 增加新的文章记录
            new_article = Article.objects.create(  # 对用户提交的文章对应的分类数据进行处理，数据库中对应数据更新
                title=title,
                content=content,
                category=category_set.first(),
                blog=blog,
            )
            category_set.update(article_count=F('article_count') + 1)

        # 更新文章题图文件
        if file:
            update_article_img(file, new_article.nid)
        return redirect(reverse('show_articles'))


@login_required
def edit_article(request, nid):
    # 文章编辑视图函数
    site_path = request.user.username
    article_set = Article.objects.filter(blog__path=site_path, nid=nid)
    article = article_set.first()
    if not article:
        return HttpResponse('此文章不存在')

    if request.method == 'GET':
        category_list = Category.objects.filter(blog__path=site_path)
        article_img_url = article.img
        context = {
            'article': article,
            'category_list': category_list,
            'article_img_url': article_img_url,
            'profile': Profile.objects.filter(user__username=request.user.username).first()
        }
        return render(request, 'useradmin/edit_article.html', context)

    else:  # 用户提交修改后的文章数据
        dic = request.POST
        file = request.FILES.get('article_img')
        new_title = dic.get('title')
        new_content = dic.get('content')
        new_category_id = int(dic.get('category'))
        old_category_id = article.category.nid

        # 处理新的文章内容,过滤可执行标签
        new_title = filter_executable_content(new_title)
        new_content = filter_executable_content(new_content)

        # 处理文章数据更新
        with atomic():
            article_set.update(title=new_title)
            article_set.update(content=new_content)
            if file:
                update_article_img(file, nid)
            # 切换分类
            switch_category(nid, old_category_id, new_category_id)
        return redirect(reverse('show_articles'))


@login_required
def delete_article(request, nid):
    """
    文章删除视图函数,此函数是真实的删除文章数据，不可恢复
    """

    # 获取对应blog的对应文章
    target_article = Article.objects.filter(blog__path=request.user.username, nid=nid).first()
    if not target_article:
        return HttpResponse('不存在此文章')
    else:
        with atomic():
            target_article.delete()
            # 文章的删除需要关联到对应分类中的article_count的更新
            target_category = target_article.category
            Category.objects.filter(nid=target_category.nid).update(article_count=F('article_count') - 1)
        return redirect(reverse('show_articles'))


@login_required
def show_categorys(request):
    # 查看当前用户博客的分类信息
    category_list = Category.objects.filter(blog__path=request.user.username)
    context = {
        'category_list': category_list,
        'profile': Profile.objects.filter(user__username=request.user.username).first()
    }
    return render(request, 'useradmin/show_categorys.html', context)


@login_required
def add_category(request):
    if request.method == 'GET':
        context = {
            'profile': Profile.objects.filter(user__username=request.user.username).first()
        }
        return render(request, 'useradmin/edit_category.html', context)

    else:
        category_name = request.POST.get('name')
        category_name = category_name.strip() if category_name else category_name
        category = Category.objects.filter(blog__path=request.user.username, name=category_name).first()
        response = {
            'url': '',
            'msg': '',
        }

        if not category_name:
            response['msg'] = '分类名称不可为空'
        elif category:
            response['msg'] = '此分类已存在'
        else:
            blog = Blog.objects.filter(path=request.user.username).first()
            Category.objects.create(blog=blog, name=category_name)
            response['url'] = reverse('show_categorys')
    return JsonResponse(response)


@login_required
def edit_category(request, nid):
    category_set = Category.objects.filter(nid=nid)
    category = category_set.first()

    if request.method == 'GET':
        context = {
            'category': category,
            'profile': Profile.objects.filter(user__username=request.user.username).first()
        }
        return render(request, 'useradmin/edit_category.html', context)

    else:
        category_name = request.POST.get('name')
        category_name = category_name.strip() if category_name else category_name
        exist_category = Category.objects.filter(name=category_name, blog__path=request.user.username).first()
        response = {
            'url': '',
            'msg': '',
        }

        if not category_name:
            response['msg'] = '分类名称不可为空'
        elif exist_category:
            response['msg'] = '此分类已存在'
        else:
            category_set.update(name=category_name)
            response['url'] = reverse('show_categorys')
    return JsonResponse(response)


@login_required
def delete_category(request, nid):
    category = Category.objects.filter(nid=nid).first()
    category.delete()
    return redirect(reverse(show_categorys))


@login_required
def edit_profile(request):
    """
    用户个人详情数据修改
    """

    site_path = request.user.username
    profile_set = Profile.objects.filter(user__username=site_path)
    profile = profile_set.first()
    if request.method == 'GET':  # 请求用户详情数据
        data = {
            'city': profile.city,
            'introduction': profile.introduction,
            'college': profile.college,
            'company': profile.company,
            'title': profile.title,
            'nick_name': profile.nick_name,
        }
        profile_form = ProfileForm(data)

        # 个人头像avatar是图片，单独处理
        avatar_url = profile.avatar
        context = {
            'profile_form': profile_form,
            'avatar_url': avatar_url,
            'profile': Profile.objects.filter(user__username=request.user.username).first()
        }
        return render(request, 'useradmin/edit_profile.html', context)

    else:
        # 处理个人详情页的逻辑代码
        file = request.FILES.get('avatar')
        dic = request.POST

        profile_form = ProfileForm(dic)
        if not profile_form.is_valid():
            return HttpResponse(profile_form.errors)

        # 数据校验成功,更新基本数据
        clean_dic = profile_form.cleaned_data
        profile_set.update(city=clean_dic.get('city'), introduction=clean_dic.get('introduction'),
                           college=clean_dic.get('college'), company=clean_dic.get('company'),
                           title=clean_dic.get('title'), nick_name=clean_dic.get('nick_name'))
        # 更新个人头像
        if file:
            update_avatar(file, site_path)
        return redirect(reverse('useradmin'))
