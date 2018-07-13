# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/22 10:03'
from django import forms  # 引入格式检验


class LoginForm(forms.Form):
    """
    这是一个登录表单(LoginForm)的类，该类继承于Form类，
    接受一个POST网页请求(request.POST)参数，该类有一个is_valid方法，
    用于检验Key对应值得基本格式是否出错，若出错则返回False，
    无误则返回True.以下方法中Key必须与前端传过来的Key相同
    """
    username = forms.CharField(required=True, min_length=2, max_length=10)  # 这里的True指的是如果这个字段为空会报错
    password = forms.CharField(required=True, min_length=5, max_length=16)


class RegisterForm(forms.Form):
    """
    这是一个注册表单(RegisterForm)的类，该类继承于Form类，
    接受一个POST网页请求(request.POST)参数，该类有一个is_valid方法，
    用于检验Key对应值得基本格式是否出错，若出错则返回False，
    无误则返回True。
    """
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=2, max_length=10)
    password = forms.CharField(required=True, min_length=5, max_length=16)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5, max_length=16)
    password2 = forms.CharField(required=True, min_length=5, max_length=16)
