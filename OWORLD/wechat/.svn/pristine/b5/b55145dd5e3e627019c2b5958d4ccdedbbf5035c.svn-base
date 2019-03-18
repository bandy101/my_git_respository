#-*- coding: utf-8 -*-
"""oWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import worklog



urlpatterns = [
    url(r'getLogType/$', worklog.getLogType, name='getLogType'),  # 日志类别
    url(r'getLogPriority/$', worklog.getLogPriority, name='getLogPriority'),  # 日志重要程度
    url(r'getMyLogList/$', worklog.getMyLogList, name='getMyLogList'),  # 我的日志
    url(r'getLogList/$', worklog.getLogList, name='getLogList'),  # 他人日志

    url(r'putLog/$', worklog.putLog, name='putLog'),  # 日志填写
    url(r'putComment/$', worklog.putComment, name='putComment'),  # 点评日志
    url(r'getLog/$', worklog.getLog, name='getLog'),  # 查看日志点评日志

    url(r'attach_save/$', worklog.attach_save, name='attach_save'),  
    url(r'getDepts/$', worklog.getDepts, name='getDepts'),  
    url(r'getUsers/$', worklog.getUsers, name='getUsers'),  

]
