# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.db.models import F
from django.shortcuts import render, HttpResponse

from blog.models import Account, Article, Blog, Category, ArticleUpDown, Comment, Profile
from blog.tools import filter_content


def index(request):
    # 首页视图函数，提供网站首页的处理逻辑
    article_list = Article.objects.all()
    for article in article_list:
        article.content = filter_content(article.content)

    content = {
        'article_list': article_list,
        'profile': Profile.objects.filter(user__username=request.user.username).first(),
    }
    return render(request, 'index/index.html', content)


def site(request, site_path):
    # 访问个人博客站点首页的视图函数
    blog = Blog.objects.filter(path=site_path).first()
    if not blog:
        return HttpResponse('没有找到此人的博客')

    # 获取博客站点的各类数据
    article_list = blog.article_set.all()
    category_list = blog.category_set.all()
    profile = blog.user.profile

    content = {
        'article_list': article_list,
        'category_list': category_list,
        'profile': profile,
        'blog': blog,
        'site_path': site_path,
        'nick_name': profile.nick_name,
    }
    return render(request, 'site/site.html', content)


def article(request, site_path, category_name, nid):
    """访问文章详情页接口"""

    # 判断文章路径的有效性
    blog = Blog.objects.filter(path=site_path).first()
    category = Category.objects.filter(name=category_name).first()
    article_set = Article.objects.filter(blog__path=site_path, category__name=category_name, nid=nid)
    article = article_set.first()
    if not article:
        return HttpResponse('此文章不存在')

    # 获取博客站点的各类数据
    article_list = blog.article_set.all()
    category_list = blog.category_set.all()
    profile = blog.user.profile
    comment_list = Comment.objects.filter(article=article)
    # 增加文章阅读量
    article_set.update(view_count=F('view_count') + 1)

    # 处理喜欢/不喜欢的记录显示
    user = Account.objects.filter(username=request.user.username).first()
    updown = ArticleUpDown.objects.filter(user=user, article=article).first()
    like_flag = None
    if updown:
        like_flag = updown.is_like

    context = {
        'article_list': article_list,
        'category_list': category_list,
        'profile': profile,
        'blog': blog,
        'site_path': site_path,
        'article': article,
        'cur_category': category,
        'comment_list': comment_list,
        'like_flag': like_flag,
        'nick_name': profile.nick_name,
        'comment_count': len(comment_list),
        'article_img_url': article.img,
    }
    return render(request, 'article/article.html', context)
