# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/5/3 16:40'
from django import forms  # 引入格式检验


class UserInfoForm(forms.Form):
    username = forms.CharField(required=True, min_length=2, max_length=10)
    mobile = forms.CharField(required=True)
