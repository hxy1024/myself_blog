# -*- coding: utf-8 -*-
# 'author':'hxy'


from django.urls import re_path
from account import views


# account 账户操作接口
urlpatterns = [
    # 注册
    re_path(r'^register/$', views.register, name='register'),

    # 登录
    re_path(r'^login/$', views.login, name='login'),

    # 注销
    re_path(r'^logout/$', views.logout, name='logout'),
]
