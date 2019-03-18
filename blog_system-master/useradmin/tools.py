# -*- coding: utf-8 -*-
# 'author':'zlw'

import re

from django.db.models import F
from django.db.transaction import atomic

from blog_system import settings
from blog.models import Article, Category, Profile


def filter_executable_content(content):
    """
    使用re，对content中的字符串进行过滤，尤其针对可执行html标签
    """

    # 针对html页面中的script标签过滤
    content = re.sub(r'<.*script.*>', '', content)
    return content


def switch_category(article_nid, old_category_id, new_category_id):
    """
    将某一篇文章从旧的分类切换到新的分类
    """

    if old_category_id != new_category_id:
        with atomic():
            # 旧的分类-1
            Category.objects.filter(nid=old_category_id).update(article_count=F('article_count') - 1)
            # 新的分类+1
            Category.objects.filter(nid=new_category_id).update(article_count=F('article_count') + 1)
            # 切换分类
            new_category = Category.objects.filter(nid=new_category_id).first()
            article_set = Article.objects.filter(nid=article_nid)

            article_set.update(category=new_category)
            return True


def update_avatar(file, site_path):
    """
    为指定的博客站点更新个人头像
    用户编辑个人详情页面的时候，可能提交个人头像文件，也可以没有提交
    """

    local_path = settings.BLOG_AVATAR_DIR + site_path + '.jpg'
    profile_set = Profile.objects.filter(user__username=site_path)

    with atomic():
        with open(local_path, 'wb') as f:
            for line in file:
                f.write(line)
        profile_set.update(avatar='avatars/' + site_path + '.jpg')


def update_article_img(file, nid):
    """
    为指定的文章更新题图文件, 用户可能提交此文件，也可能没有提交
    """

    article_set = Article.objects.filter(nid=nid)
    nid = str(nid)
    local_path = settings.ARTICLE_IMG_DIR + nid + '.jpg'
    print(settings.ARTICLE_IMG_DIR)
    print(local_path)

    with atomic():
        with open(local_path, 'wb') as f:
            for line in file:
                f.write(line)
        article_set.update(img='article_imgs/' + nid + '.jpg')
