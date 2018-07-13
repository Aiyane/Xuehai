# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View  # 基础的View类，让其他View继承于他，可以不用对POST或GET访问方式做判断
from django.contrib.auth import authenticate, login, logout  # 对用户名密码校验，后一个发出一个session登录，登出
from django.http import HttpResponse, HttpResponseRedirect  # content_type='application/json'
from django.core.urlresolvers import reverse  # 保留当前View跳转,返回url,但是一般的render是直接返回的html页面
from django.contrib.auth.hashers import make_password  # 此方法可对明文加密

from users.models import Banner, UserProfile, EmailVerifyRecord
from .models import UserMessage
from courses.models import Course
from orgs.models import CourseOrg, Teacher
from .forms import LoginForm, RegisterForm, ModifyPwdForm
from utils.send_email import send_register_email  # 引入发送邮件的方法


class IndexView(View):
    # 首页
    def get(self, request):
        app = request.GET.get('app', "")
        all_orgs = CourseOrg.objects.all()
        all_courses = Course.objects.filter(is_banner=False)[:9]
        vip_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = all_orgs[:6]
        return render(request, 'index.html', {
            "courses": all_courses,
            "orgs": orgs,
            "app": app,
            "vip_courses": vip_courses,
        })


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    """
    这是一个注册逻辑(RegisterView)的类，继承于View
    """
    def get(self, request):
        return render(request, "register.html", {})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")  # 将用户的email与password传入
            username = request.POST.get("username", "")
            gender = request.POST.get("gender", "")
            birthday = request.POST.get("birth", "")
            tel = request.POST.get("tel", "")
            image = request.POST.get("image", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "error": "用户已经存在！"})
            if UserProfile.objects.filter(username=username):
                return render(request, "register.html", {"register_form": register_form, "error": "该用户名已被注册，请换一个用户名重新注册"})
            pass_word = request.POST.get("password", "")

            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = user_name
            user_profile.gender = gender
            user_profile.birthday = birthday
            user_profile.mobile = int(tel)
            user_profile.image = image
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)

            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile
            user_message.message = "欢迎注册学海网"
            user_message.save()

            send_register_email(user_name, "register")  # 发送验证邮箱
            login_type = "register"
            return render(request, "login.html", {"register_form": register_form, "login_type": login_type})
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        email = request.POST.get("email", "")
        if email:
            try:
                user = UserProfile.objects.get(email=email)
            except:
                return render(request, "login.html", {
                    "login_type": '失败'
                })
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

        elif login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:  # 验证是否激活
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"error": "用户未激活！"})
            else:
                return render(request, "login.html", {"error": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"error": "请输入正确格式！"})


class ActiveUserView(View):
    """
    这是一个用户激活逻辑(ActiveUserView)的类,继承于View，该类有一个方法，
    接受一个网页验证请求(request)参数，若用户点击验证网址，
    则返回登录页面(login.html)
    """

    def get(self, request, active_code):
        """
        传入网页的验证码(active_code)是否与邮箱验证表单中的验证码(code)相同，
        相同则返回相关邮箱验证实例。filter与get的区别在于filter遇到表单中属性相同匹配到时不会报错，但是get会报错，
        所以用get时条件最好是该属性值在表单中是唯一的，随机验证码还是不能保证不会出项相同情况。
        """
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 这里的all_records是多个邮箱验证实例，因为验证码可能相同
        if all_records:
            for record in all_records:
                email = record.send_email
                user = UserProfile.objects.get(email=email)  # 得到一个用户信息邮箱与传来的邮箱验证邮箱相同的用户信息实例
                user.is_active = True  # 令这个实例中is_active值为True
                user.save()  # 保存用户
            return render(request, "login.html", {
                "user": user,
            })
        else:
            return render(request, "active_fail.html")


class ResetView(View):
    """
    这是一个用户重置密码逻辑(ActiveUserView)的类,继承于View，该类有一个方法，
    接受一个网页验证请求(request)参数，若用户点击重置密码，信息无误则返回密码重置网页，
    否则返回激活失败页面。
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 这里的all_records是多个邮箱验证实例，因为验证码可能相同
        if all_records:
            for record in all_records:
                email = record.send_email
                user = UserProfile.objects.get(email=email)  # 得到一个用户信息邮箱与传来的邮箱验证邮箱相同的用户信息实例
                return render(request, "password_reset.html", {"user": user})
        else:
            return render(request, "active_fail.html")


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        user = request.POST.get("username", "")
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"user": user, "msg": "密码不一致!"})
            user = UserProfile.objects.get(username=user)
            user.password = make_password(pwd1)
            user.save()
            login_type = "success"
            return render(request, "login.html", {
                "user": user,
                "login_type": login_type
            })
        else:
            return render(request, "password_reset.html", {"user": user, "msg": "密码格式不正确"})
