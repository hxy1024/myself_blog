# -*- coding: utf-8 -*-
# 'author':'zlw'


from django.urls import re_path, path
from useradmin import views


# useradmin 用户后台管理操作接口
urlpatterns = [
    # 个人博客后台管理路由
    re_path(r'^home/$', views.useradmin, name='useradmin'),

    # 个人后台 -- 文章管理
    re_path(r'^show_articles/$', views.show_articles, name='show_articles'),

    # 个人后台-- 增加文章
    re_path(r'^add_article/$', views.add_article, name='add_article'),

    # 个人后台-- 编辑文章
    path('edit_article/<int:nid>/', views.edit_article, name='edit_article'),

    # 个人后台-- 删除文章
    path('delete_article/<int:nid>/', views.delete_article, name='delete_article'),

    # 个人后台 -- 分类管理
    re_path(r'show_categorys/$', views.show_categorys, name='show_categorys'),

    # 个人后台 -- 添加分类
    re_path(r'add_category/$', views.add_category, name='add_category'),

    # 个人后台 -- 编辑分类
    path('edit_category/<int:nid>/', views.edit_category, name='edit_category'),

    # 个人后台 -- 删除分类
    path('delete_category/<int:nid>/', views.delete_category, name='delete_category'),

    # 个人详情页数据修改
    re_path(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
]
