# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View  # 基础的View类，让其他View继承于他，可以不用对POST或GET访问方式做判断
from .models import Teacher, CourseOrg

from pure_pagination import Paginator, PageNotAnInteger  # 翻页的模块
from django.db.models import Q  # 这是一个或方法


class TeacherListView(View):
    def get(self, request):
        app = request.GET.get('app', "")
        teachers = Teacher.objects.all()
        order = request.GET.get("order", "")

        # 对教师进行排序
        all_teachers = teachers.order_by("-add_time")
        if order == "hot":
            all_teachers = teachers.order_by("-click_nums")
        # ====================================这里是教师搜索========================================
        classifica = request.GET.get('classifica', "")
        search_keyword = request.GET.get('keyword', "")
        if classifica == "教师":
            app = classifica
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keyword) | Q(points__icontains=search_keyword))  # 前面加上i不区分大小写

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 6, request=request)
        teachers = p.page(page)

        need_page = teachers.number
        return render(request, 'teacher_list.html', {
            "app": app,
            "need_page": need_page,
            "teachers": teachers,
            "order": order,
        })


class OrgListView(View):
    def get(self, request):
        app = request.GET.get('app', "")
        all_orgs = CourseOrg.objects.all()
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        # ====================================这里是机构搜索========================================
        classifica = request.GET.get('classifica', "")
        search_keyword = request.GET.get('keyword', "")
        if classifica == "机构":
            app = classifica
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))  # 前面加上i不区分大小写

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 6, request=request)
        orgs = p.page(page)

        need_page = orgs.number
        return render(request, 'orgs_list.html', {
            "app": app,
            "need_page": need_page,
            "orgs": orgs,
            "ct": category
        })


class OrgDetailView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))

        # 增加机构点击数
        org.click_nums += 1
        org.save()
        all_courses = org.course_set.all()  # 这里的course_org中的这个course_set是自动生成的，它是models下Course类
        # 自动小写再加上一个set生成的，可以直接返回找到Course
        all_teachers = org.teacher_set.all()  # 这里同上
        return render(request, 'org_detail.html', {
            "org": org,
            "all_teachers": all_teachers,
            "all_courses": all_courses,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))

        # 增加老师点击数
        teacher.click_nums += 1
        teacher.save()
        all_courses = teacher.course_set.all()
        return render(request, 'teacher_detail.html', {
            "teacher": teacher,
            "all_courses": all_courses,
        })
