# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.urls import re_path, path
from query import views


# query ajax请求接口
urlpatterns = [
    # ajax获取验证码图片
    re_path(r'validate_img/$', views.validate_img, name='validate_img'),

    # 站点发起ajax获取文章列表
    re_path(r'article_list/$', views.article_list_ajax, name='article_list'),

    # 对文章表示点赞或者不喜欢
    path('like/<int:nid>/', views.article_like_ajax, name='like'),

    # 用户发起ajax添加文章根评论
    re_path(r'add_comment/$', views.add_comment, name='add_comment'),

    # 用户发起ajax请求某一文章所有评论数据
    re_path(r'comment_list/$', views.comment_list, name='comment_list'),

    # 用户发起ajax请求某一个文章的属性数据
    path('article_attrs/<int:nid>/', views.article_attrs, name='article_attrs'),
]
