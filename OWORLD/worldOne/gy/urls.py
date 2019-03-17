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
from . import sign_up 
from . import sign_up_qy 
from . import mat_souring_qy 
from . import purchasing 

urlpatterns = [
    url(r'sign_up/getSupInfo/$', sign_up.getSupInfo, name='getSupInfo'),  
    url(r'sign_up/saveSupName/$', sign_up.saveSupName, name='saveSupName'),  
    url(r'sign_up/bizlicenseOcr/$', sign_up.bizlicenseOcr, name='bizlicenseOcr'), 
    url(r'sign_up/IDCardOCR/$', sign_up.IDCardOCR, name='IDCardOCR'), 

    url(r'sign_up/upload_licence/$', sign_up.upload_licence, name='upload_licence'), 
    url(r'sign_up/del_attach_file/$', sign_up.del_attach_file, name='del_attach_file'), 

    url(r'sign_up/audit/$', sign_up_qy.audit, name='audit'), 
    url(r'sign_up/getSupList/$', sign_up_qy.getSupList, name='getSupList'), 

    url(r'mat_souring/getMyProjList/$', mat_souring_qy.getMyProjList, name='getMyProjList'), 
    url(r'mat_souring/getAuditor/$', mat_souring_qy.getAuditor, name='getAuditor'), 
    url(r'mat_souring/getMatSouring/$', mat_souring_qy.getMatSouring, name='getMatSouring'), 
    url(r'mat_souring/saveMatSouring/$', mat_souring_qy.saveMatSouring, name='saveMatSouring'), 
    url(r'mat_souring/auditMatSouring/$', mat_souring_qy.auditMatSouring, name='auditMatSouring'), 
    url(r'mat_souring/getMatSouringList/$', mat_souring_qy.getMatSouringList, name='getMatSouringList'),
    url(r'mat_souring/deleteMatSouring/$', mat_souring_qy.deleteMatSouring, name='deleteMatSouring'), 

    url(r'purchasing/getPurchasingList/$', purchasing.getPurchasingList, name='getPurchasingList'), 
    url(r'purchasing/getAuditList/$', purchasing.getAuditList, name='getAuditList'), 
    url(r'purchasing/audit/$', purchasing.audit, name='audit'), 
    url(r'purchasing/saveCgd/$', purchasing.saveCgd, name='saveCgd'), 
    url(r'purchasing/pushCgd/$', purchasing.pushCgd, name='pushCgd'), 
    url(r'purchasing/getCgdInfo/$', purchasing.getCgdInfo, name='getCgdInfo'), 
    url(r'purchasing/searchUsers/$', purchasing.searchUsers, name='searchUsers'), 

    url(r'purchasing/getRkdList/$', purchasing.getRkdList, name='getRkdList'), 
    url(r'purchasing/getRkdInfo/$', purchasing.getRkdInfo, name='getRkdInfo'), 
    url(r'purchasing/saveRkd/$', purchasing.saveRkd, name='saveRkd'), 
    url(r'purchasing/pushRkd/$', purchasing.pushRkd, name='pushRkd'), 
    url(r'purchasing/deleteRkd/$', purchasing.deleteRkd, name='deleteRkd'), 

    url(r'purchasing/getFlow/$', purchasing.getFlow, name='getFlow'), 
    url(r'purchasing/getFlowDept/$', purchasing.getFlowDept, name='getFlowDept'), 
    url(r'purchasing/getFlowUser/$', purchasing.getFlowUser, name='getFlowUser'), 

    url(r'purchasing/savePurchasing/$', purchasing.savePurchasing, name='savePurchasing'), 
    url(r'purchasing/invalidPurchasing/$', purchasing.invalidPurchasing, name='invalidPurchasing'), 
    url(r'purchasing/deletePurchasing/$', purchasing.deletePurchasing, name='deletePurchasing'), 

    url(r'purchasing/getDzdList/$', purchasing.getDzdList, name='getDzdList'), 
    url(r'purchasing/auditDzd/$', purchasing.auditDzd, name='auditDzd'), 
    url(r'purchasing/getDzdInfo/$', purchasing.getDzdInfo, name='getDzdInfo'), 

]
