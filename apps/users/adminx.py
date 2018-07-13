# _*_ coding: utf-8 _*_
__author__ = 'aiyane'
__date__ = '2017/4/21 21:28'
import xadmin  # 引入xadmin后台管理系统
from xadmin import views  # 引入全局的后台管理主题注册
from .models import UserProfile, EmailVerifyRecord, Banner  # 引入要注册的model


class BaseSetting(object):
    enable_themes = True  # 将主题功能改为可以使用
    use_bootswatch = True  # 加载主题改为True


class GlobalSetting(object):
    """
    后台管理系统的全局设置
    """
    site_title = u"学海网后台管理"
    site_footer = u"学海网"
    menu_style = "accordion"  # 设置侧边栏收起菜单


class UserProfileAdmin(object):
    list_display = ['username', 'birthday', 'gender', 'mobile', 'username', 'email', 'is_staff']  # 后台排列项
    search_fields = ['username', 'gender', 'mobile', 'username', 'email', 'is_staff']  # 后台搜索项
    list_filter = ['username', 'birthday', 'gender', 'mobile', 'username', 'email', 'is_staff']  # 后台筛选项


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'send_email', 'send_type', 'send_time']
    search_fields = ['code', 'send_email', 'send_type']
    list_filter = ['code', 'send_email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'url', 'index', 'add_time']
    search_fields = ['title', 'url', 'index']
    list_filter = ['title', 'url', 'index', 'add_time']

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 主题的注册
xadmin.site.register(views.CommAdminView, GlobalSetting)  # 标题与页脚的注册
