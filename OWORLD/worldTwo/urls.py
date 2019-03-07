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
prj_name=__name__.split('.')[0]
from django.conf.urls import include, url  
from . import views 
from . import users
from . import xcx
from . import proj

urlpatterns = [
    url(r'sysinfo/$', views.sysinfo, name='sysinfo'),  
    url(r'translate/$', views.translate, name='translate'),  
    url(r'login/$', views.login, name='login'),  
    url(r'home/$', views.home, name='home'),  
    url(r'logout/$', views.logout, name='logout'),  
    url(r'getMenu/$', views.getMenu, name='getMenu'),  
    url(r'select/$', views.select, name='select'),  
    url(r'getData/$', views.getData, name='getData'),  
    url(r'upload_file/$', views.upload_file, name='upload_file'),  
    url(r'del_file/$', views.del_file, name='del_file'),  
    url(r'get_file/$', views.get_file, name='get_file'),  
    url(r'get_file_list/$', views.get_file_list, name='get_file_list'),  
    url(r'editor_upload/$', views.editor_upload, name='editor_upload'),  
    url(r'^menu/', include('%s.menu.urls'%prj_name)),  
    url(r'^depts/', include('%s.depts.urls'%prj_name)),  
    url(r'^roles/', include('%s.roles.urls'%prj_name)),  
    url(r'^common/', include('%s.common.urls'%prj_name)),  
    url(r'rd/$', views.rd, name='rd'),  
    url(r'index_wx/$', views.index_wx, name='index_wx'),  
    url(r'login_wx/$', views.login_wx, name='login_wx'),  
    url(r'get_data_wx/$', views.get_data_wx, name='get_data_wx'),  
    url(r'modify_pwd/$', users.modify_pwd, name='modify_pwd'),
    url(r'LinkToShajd/$', xcx.LinkToShajd, name='LinkToShajd'),  

    url(r'proj/getProjInfo/$', proj.getProjInfo, name='getProjInfo'),  
    url(r'proj/getRecentlyProj/$', proj.getRecentlyProj, name='getRecentlyProj'),  
    url(r'proj/setRecentlyProj/$', proj.setRecentlyProj, name='setRecentlyProj'),  
]
