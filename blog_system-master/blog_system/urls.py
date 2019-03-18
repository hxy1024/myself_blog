"""blogSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from blog import views
from blog_system import settings


urlpatterns = [
    # 管理
    path('admin/', admin.site.urls),

    # 主页
    re_path(r'^$', views.index, name='index'),

    # media配置
    re_path(r'^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 如下是业务路由接口
    # account 账户操作接口
    re_path(r'^account/', include('account.urls')),

    # blog 博客站点操作接口
    re_path(r'^blog/', include('blog.urls')),

    # useradmin 用户后台管理操作接口
    re_path(r'^useradmin/', include('useradmin.urls')),

    # query ajax请求接口
    re_path(r'^query/', include('query.urls')),
]
