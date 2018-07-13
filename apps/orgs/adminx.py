# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/21 23:57'
import xadmin  # 引入xadmin后台管理系统
from .models import CourseOrg, Teacher  # 引入要注册的model


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'tag', 'add_time', 'category', 'course_nums']
    search_fields = ['name', 'desc', 'click_nums', 'tag', 'category', 'course_nums']
    list_filter = ['name', 'desc', 'click_nums', 'tag', 'add_time', 'category', 'course_nums']
    ordering = ['-click_nums']  # 排列的顺序
    readonly_fields = ['click_nums']  # 只读
    list_editable = ['degree', 'desc']  # 可以在列表页进行直接修改


class TeacherAdmin(object):
    list_display = ['org', 'name','work_year', 'points', 'click_nums', 'add_time']
    search_fields = ['org', 'name','work_year', 'points', 'click_nums']
    list_filter = ['org__name', 'name', 'work_year', 'points', 'click_nums', 'add_time']

xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
