# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/23 23:52'
from django.conf.urls import url, include  # 引入基本方法
from .views import TeacherListView, OrgListView, OrgDetailView, TeacherDetailView

urlpatterns = [
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^list/$', OrgListView.as_view(), name="org_list"),
    url(r'^detail/(?P<org_id>\d+)/$', OrgDetailView.as_view(), name="org_detail"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
