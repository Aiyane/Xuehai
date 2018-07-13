# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime  # 导入当前时间

from django.db import models

from users.models import UserProfile
from courses.models import Course


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    floor = models.IntegerField(verbose_name=u"楼数", default=0)
    hate_reason = models.IntegerField(verbose_name=u"举报类型", default=0)
    hate_nums = models.IntegerField(verbose_name=u"举报次数", default=0)
    is_add_info = models.BooleanField(verbose_name=u"是否回复", default=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.comments


class UserMessage(models.Model):
    post_user = models.CharField(max_length=20, default=u"学海网", verbose_name=u"发送用户")
    user = models.ForeignKey(UserProfile, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    course = models.ForeignKey(Course, verbose_name=u"课程", blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.message


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name
