# -*- coding:utf-8 -*-
"""ruan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
import xadmin  # 引入xadmin
from operation.views import IndexView
from django.views.static import serve  # 处理静态文件，针对media文件
from ruan.settings import MEDIA_ROOT  # media的路径

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),

    url(r'^operation/', include('operation.urls', namespace="operation")),
    url(r'^orgs/', include('orgs.urls', namespace="orgs")),
    url(r'^courses/', include('courses.urls', namespace="courses")),
    url(r'^users/', include('users.urls', namespace="users")),

    # 配置上传文件的访问处理函数--media
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT})
]

#  全局404配置
handler404 = 'users.views.page_not_found'
