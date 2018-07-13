# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View  # 基础的View类，让其他View继承于他，可以不用对POST或GET访问方式做判断
from utils.is_login import is_login  # 这里引入了我写的判断登录的装饰器

from operation.models import UserCourse, UserMessage
from courses.models import Course
from .models import UserProfile, EmailVerifyRecord
from utils.send_email import send_register_email  # 引入发送邮件的方法
from .forms import UserInfoForm


class UserHomeView(View):
    @is_login
    def get(self, request):
        user = request.user
        more = int(request.GET.get("more", 0))
        seen_courses = UserCourse.objects.filter(user=user).order_by("-add_time")
        if more == 0:
            seen_courses = seen_courses[:9]
        courses = Course.objects.all().order_by("-click_nums")[:4]

        return render(request, "user_home.html", {
            "seen_courses": seen_courses,
            "courses": courses,
            "more": more,
        })


class UserMessageView(View):
    @is_login
    def get(self, request):
        user = request.user
        all_messages = user.usermessage_set.filter(has_read=False).order_by("-add_time")
        all_message = user.usermessage_set.all().order_by("-add_time")
        messages = []
        for message in all_messages:
            message.has_read = True
            message.save()
            messages.append(message)
        return render(request, "user_message.html", {
            "messages": messages,
            "all_message": all_message,
        })


class UserListView(View):
    @is_login
    def get(self, request):
        user = request.user
        return render(request, "user_list.html", {
            "user": user,
        })

    @is_login
    def post(self, request):
        user = request.user
        username = request.POST.get("username", "")
        gender = request.POST.get("gender", "")
        birthday = request.POST.get("birthday", "")
        mobile = request.POST.get("mobile", "")
        user_info_form = UserInfoForm(request.POST)
        if user_info_form.is_valid():
            user.username = username
            user.gender = gender
            if request.POST.get("birthday", ""):
                user.birthday = birthday
            user.mobile = mobile
            if request.FILES.get("image"):
                user.image = request.FILES.get("image", "")
            user.save()
            return render(request, "user_list.html", {
                "user": user,
            })
        else:
            return render(request, "user_list.html", {
                "user": user,
                "error": "修改出错",
            })


class ResetEmailView(View):
    @is_login
    def post(self, request):
        email = request.POST.get("email", "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"msg":"邮箱已经存在"}', content_type='application/json')
        user_id = request.POST.get("user_id", 0)
        if user_id > 0:
            user = UserProfile.objects.get(id=int(user_id))
            # 写入重置邮箱消息
            user_message = UserMessage()
            user_message.user = user
            user_message.message = user.username + "修改邮箱为:" + email
            user_message.save()
            # 发送验证邮箱
            send_register_email(email, "update_email")
            return HttpResponse('{"msg":"请前往邮箱验证"}', content_type='application/json')
        else:
            return HttpResponse('{"msg":"修改失败"}', content_type='application/json')


class ActiveEmailView(View):
    @is_login
    def post(self, request):
        email = request.POST.get('email', '')
        active_code = request.POST.get('active_code', '')
        all_records = EmailVerifyRecord.objects.filter(send_email=email, code=active_code, send_type='update_email')
        if all_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"msg":"验证码出错"}', content_type='application/json')


class ChangePasswordView(View):
    @is_login
    def get(self, request):
        email = request.GET.get("email", "")
        if email:
            user = UserProfile.objects.get(email=email)
            user_message = UserMessage()
            user_message.user = user
            user_message.message = "学海网修改密码"
            user_message.save()

            send_register_email(email, "forget")  # 发送验证邮箱
            login_type = "forget"
            return render(request, "login.html", {
                "user": user,
                "login_type": login_type
            })
        else:
            return render(request, "login.html", {})


class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 这里的all_records是多个邮箱验证实例，因为验证码可能相同
        if all_records:
            for record in all_records:
                email = record.send_email
                user = UserProfile.objects.get(email=email)  # 得到一个用户信息邮箱与传来的邮箱验证邮箱相同的用户信息实例
                return render(request, "password_reset.html", {"user": user})
        else:
            return render(request, "active_fail.html")

def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response
