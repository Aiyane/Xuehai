# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/22 10:49'
from django.conf.urls import url, include  # 引入基本方法
from .views import LoginView, RegisterView, ActiveUserView, LogoutView, ResetView, ModifyPwdView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
]

