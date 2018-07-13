# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/24 22:35'
from django.conf.urls import url  # 引入基本方法
from .views import CourseView, CourseDetailView, VideoView, AddCommentsView, AddReplyView, AddHateView

urlpatterns = [
    url(r'^list/$', CourseView.as_view(), name="courses_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^video/(?P<video_id>\d+)/$', VideoView.as_view(), name="course_video"),
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),
    url(r'^add_hate/$', AddHateView.as_view(), name="add_hate"),
    url(r'^add_reply/$', AddReplyView.as_view(), name="add_reply"),
]