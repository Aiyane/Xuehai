# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime  # 导入当前时间

from django.db import models


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    tag = models.CharField(default=u"全国知名", max_length=10, verbose_name=u"机构标签")
    category = models.CharField(max_length=20, choices=(("pxjg", "培训机构"), ("gr", "国内高校"), ("gx", "国外高校")), verbose_name= u"机构类别", default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name=u"头像", max_length=100)
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    work_year = models.IntegerField(default=0, verbose_name=u"工作年限")
    points = models.TextField(verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    age = models.IntegerField(default=18, verbose_name=u"年龄")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
