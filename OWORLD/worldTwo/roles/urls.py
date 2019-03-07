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
from . import roles 

urlpatterns = [
    url(r'getRoleList/$', roles.getRoleList, name='getRoleList'),  
    url(r'addRole/$', roles.addRole, name='addRole'),  
    url(r'modifyRole/$', roles.modifyRole, name='modifyRole'),  
    url(r'deleteRole/$', roles.deleteRole, name='deleteRole'),  
    url(r'getRoleUser/$', roles.getRoleUser, name='getRoleUser'),  
    url(r'getRolMenu/$', roles.getRolMenu, name='getRolMenu'),  
    url(r'modifyRoleMenu/$', roles.modifyRoleMenu, name='modifyRoleMenu'),  
    url(r'getUserRole/$', roles.getUserRole, name='getUserRole'),  
    url(r'getRoleUserList/$', roles.getRoleUserList, name='getRoleUserList'),  
    url(r'addRoleUsers/$', roles.addRoleUsers, name='addRoleUsers'),  
    url(r'deleteRoleUser/$', roles.deleteRoleUser, name='deleteRoleUser'),  
]
