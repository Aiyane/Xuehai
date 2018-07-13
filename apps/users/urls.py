# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/5/1 0:19'
from django.conf.urls import url, include  # 引入基本方法
from .views import UserHomeView, UserMessageView, UserListView, ResetEmailView, ActiveEmailView, ChangePasswordView, ResetPwdView

urlpatterns = [
    url(r'^home/$', UserHomeView.as_view(), name="user_home"),
    url(r'^message/$', UserMessageView.as_view(), name="user_message"),
    url(r'^list/$', UserListView.as_view(), name="user_list"),
    url(r'^reset_email/$', ResetEmailView.as_view(), name="reset_email"),
    url(r'^email_active/$', ActiveEmailView.as_view(), name="email_active"),
    url(r'^change_password/$', ChangePasswordView.as_view(), name="change_password"),
    url(r'^reset_pwd/(?P<active_code>.*)/$', ResetPwdView.as_view(), name="reset_pwd"),
]
