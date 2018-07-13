# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/5/1 13:59'
from django.shortcuts import render


def is_login(func):  # 我在这里写了一个装饰器，可以在方法中对权限判断
    def is_method(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        else:
            return func(self, request, *args, **kwargs)
    return is_method
