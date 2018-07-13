# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/21 23:57'
import xadmin  # 引入xadmin后台管理系统
from .models import Course, Lesson, Video, CourseResource  # 引入要注册的model


class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_times', 'students', 'click_nums']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students', 'click_nums', 'add_time']
    ordering = ['-click_nums']  # 排列的顺序
    readonly_fields = ['click_nums']  # 只读
    list_editable = ['degree', 'desc']  # 可以在列表页进行直接修改
    refresh_times = [3, 5]  # 定时刷新


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)