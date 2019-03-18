# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.urls import path
from blog import views


# blog 博客站点操作接口
urlpatterns = [
    # # 访问个人站点
    path('<str:site_path>/', views.site, name='site'),

    # # 获取文章详情页面
    path('<str:site_path>/article/<str:category_name>/<int:nid>/', views.article, name='article'),
]
