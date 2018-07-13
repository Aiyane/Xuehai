# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/21 23:57'
import xadmin  # 引入xadmin后台管理系统
from .models import CourseComments, UserMessage, UserCourse  # 引入要注册的model


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user__username', 'course', 'comments', 'add_time', 'hate_nums']  # 这里取user外键username
    readonly_fields = ['floor', 'hate_nums']  # 只读


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__username', 'course__name', 'add_time']

xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
