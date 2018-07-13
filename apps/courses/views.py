# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course, Video
from operation.models import CourseComments, UserCourse, UserMessage
from django.http import HttpResponse
from utils.is_login import is_login  # 这里引入了我写的判断登录的装饰器

from pure_pagination import Paginator, PageNotAnInteger  # 翻页的模块
from django.db.models import Q  # 这是一个或方法
from datetime import datetime  # 导入当前时间


class CourseView(View):
    def get(self, request):
        app = request.GET.get('app', "")
        all_courses = Course.objects.all()
        order = request.GET.get("order", "")
        tag = request.GET.get("tag", "")

        # 对课程进行排序
        all_courses = all_courses.order_by("-add_time")

        if order == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # tag分类
        if tag:
            all_courses = all_courses.filter(tag=tag)
# ====================================这里是课程搜索========================================
        classifica = request.GET.get('classifica', "")
        search_keyword = request.GET.get('keyword', "")
        if classifica == "课程":
            app = classifica
            all_courses = all_courses.filter(
                Q(name__icontains=search_keyword) | Q(tag__icontains=search_keyword) | Q(
                    degree__icontains=search_keyword) | Q(desc__icontains=search_keyword)
                | Q(category__icontains=search_keyword) | Q(you_get__icontains=search_keyword))  # 前面加上i不区分大小写

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        need_page = courses.number
        return render(request, 'courses_list.html', {
            "app": app,
            "need_page": need_page,
            "courses": courses,
            "order": order,
            "tag": tag,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        teacher = course.teacher
        org = course.course_org

        # 增加课程点击数
        course.click_nums += 1
        course.save()
        course_resources = course.courseresource_set.all()

        return render(request, "course_detail.html", {
            "course": course,
            "org": org,
            "teacher": teacher,
            "course_resources": course_resources,
        })


class VideoView(View):
    @is_login
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        user = request.user
        try:
            user_course = UserCourse.objects.get(course=course, user=user)
            user_course.add_time = datetime.now()
        except:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
        user_course.save()
        all_users_courses = CourseComments.objects.filter(course=course, is_add_info=False).order_by("-add_time")[:10]
        all_users_reply = CourseComments.objects.filter(course=course, is_add_info=True).order_by("add_time")
        return render(request, "video.html", {
            "course": course,
            "video": video,
            "all_users_courses": all_users_courses,
            "all_users_reply": all_users_reply,
        })


class AddCommentsView(View):
    def get(self, request):
        video_id = request.GET.get("video_id", 0)
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_users_courses = CourseComments.objects.filter(course=course, is_add_info=False).order_by("-add_time")[:10]
        all_users_reply = CourseComments.objects.filter(course=course, is_add_info=True).order_by("add_time")
        more = request.GET.get('more', '')
        if more == '1':
            all_users_courses = CourseComments.objects.filter(course=course, is_add_info=False).order_by("-add_time")
        if video_id > 0:
            return render(request, "new_comments.html", {
                "all_users_courses": all_users_courses,
                "course": course,
                "all_users_reply": all_users_reply,
                "video": video,
                "more": more,
            })
        else:
            return render(request, "404.html", {})

    @is_login
    def post(self, request):
        """
        用户添加课程评论
        """
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        course = Course.objects.get(id=int(course_id))
        comment = CourseComments()
        comment.comments = comments
        comment.course = course
        comment.user = request.user
        comment.is_add_info = False
        if CourseComments.objects.filter(course=course):
            comment.floor = CourseComments.objects.filter(course=course, is_add_info=False).order_by("-add_time")[0].floor + 1
        else:
            comment.floor = 1
        comment.save()
        return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')


class AddHateView(View):
    @is_login
    def post(self, request):
        """
        投诉评论
        """
        video_id = request.GET.get("video_id", 0)
        video = Video.objects.get(id=int(video_id))
        hate_reason = request.POST.get("reason", 0)
        comment_id = request.POST.get("comment", 0)
        comment = CourseComments.objects.get(id=int(comment_id))
        comment.hate_reason = int(hate_reason)
        comment.hate_nums += 1
        comment.save()
        course = video.lesson.course
        all_users_courses = CourseComments.objects.filter(course=course, is_add_info=False).order_by("-add_time")[:10]
        all_users_reply = CourseComments.objects.filter(course=course, is_add_info=True).order_by("add_time")
        more = request.GET.get('more', '')
        hate_success = 1
        if more == '1':
            all_users_courses = CourseComments.objects.filter(course=course).order_by("-add_time")
        if video_id > 0:
            return render(request, "new_comments.html", {
                "all_users_courses": all_users_courses,
                "course": course,
                "all_users_reply": all_users_reply,
                "video": video,
                "more": more,
                "hate_success": hate_success,
            })


class AddReplyView(View):
    @is_login
    def post(self, request):
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        floor = int(request.POST.get("floor", 0))
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            if CourseComments.objects.filter(course=course):
                course_comments.course = course
                course_comments.comments = comments
                course_comments.user = request.user
                course_comments.is_add_info = True
                course_comments.floor = floor
                course_comments.save()
                message = UserMessage()
                message.message = comments
                message.post_user = request.user.username
                message.course = course
                message.user = CourseComments.objects.get(course=course, floor=floor, is_add_info=False).user
                message.save()
            else:
                return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')
