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
from . import common 
from . import menu_data 
from . import flow 
from . import verify 
from . import info 
from . import pdf 
from . import synchro
from . import schedule
from . import category
from . import codeUpload
from . import exportExcel
from . import report
from . import msg_send
from . import upload

urlpatterns = [
    url(r'getReportData/*', report.getReportData, name='getReportData'),  
    url(r'getReportGridData/*', report.getReportGridData, name='getReportGridData'),  
    url(r'getReportExpandedData/*', report.getReportExpandedData, name='getReportExpandedData'),  
    url(r'getReportRefreshData/*', report.getReportRefreshData, name='getReportRefreshData'),  

    url(r'getListAttribute/*', common.getListAttribute, name='getListAttribute'),  
    url(r'getListData/*', common.getListData, name='getListData'),  
    url(r'getPageForm/*', common.getPageForm, name='getPageForm'),  
    url(r'savePageForm/*', common.savePageForm, name='savePageForm'),  
    url(r'saveAudit/*', flow.saveAudit, name='saveAudit'),  
    url(r'updateDB/*', flow.updateDB, name='updateDB'),  
    url(r'rePushMsg/*', flow.rePushMsg, name='rePushMsg'),  
    url(r'deletePageForm/*', common.deletePageForm, name='deletePageForm'),  
    url(r'actionPageForm/*', common.actionPageForm, name='actionPageForm'),  
    url(r'setListSql/*', menu_data.setListSql, name='setListSql'),  
    url(r'setFormSql/*', menu_data.setFormSql, name='setFormSql'),  
    url(r'saveFormData/*', menu_data.saveFormData, name='saveFormData'),  
    url(r'saveUserPara/*', menu_data.saveUserPara, name='saveUserPara'),  
    url(r'savePageVerify/*', verify.savePageVerify, name='savePageVerify'),  
    url(r'upload_pic/*', pdf.upload_pic, name='upload_pic'),  
    url(r'pdfData/*', pdf.pdfData, name='pdfData'),  
    url(r'savePdfSetting/*', pdf.savePdfSetting, name='savePdfSetting'),  
    url(r'printPDF/*', pdf.printPDF, name='printPDF'),  
    url(r'synchroWxUsers/*', synchro.synchroWxUsers, name='synchroWxUsers'),  
    url(r'saveWxInfo/*', info.saveWxInfo, name='saveWxInfo'),  
    url(r'delWxInfo/*', info.delWxInfo, name='delWxInfo'),  
    url(r'auditWxInfo/*', info.auditWxInfo, name='auditWxInfo'),  
    url(r'saveWxComment/*', info.saveWxComment, name='saveWxComment'),  
    url(r'saveSchedule/*', schedule.saveSchedule, name='saveSchedule'), 
    url(r'getScheduleList/*', schedule.getScheduleList, name='getScheduleList'), 
    url(r'getProjList/*', schedule.getProjList, name='getProjList'), 
    url(r'getPlanList/*', schedule.getPlanList, name='getPlanList'), 
    url(r'getFloorList/*', schedule.getFloorList, name='getFloorList'), 
    url(r'getFloorDetail/*', schedule.getFloorDetail, name='getFloorDetail'), 
    url(r'editTable/*', schedule.editTable, name='editTable'), 
    url(r'getScheduleDetail/*', schedule.getScheduleDetail, name='getScheduleDetail'), 
    url(r'saveSechedule/*', schedule.saveSechedule, name='saveSechedule'), 
    url(r'getCategoryList/$', category.getCategoryList, name='getCategoryList'),  
    url(r'getCategory/$', category.getCategory, name='getCategory'),  
    url(r'addCategory/$', category.addCategory, name='addCategory'),  
    url(r'modifyCategory/$', category.modifyCategory, name='modifyCategory'),  
    url(r'deleteCategory/$', category.deleteCategory, name='deleteCategory'),  
    url(r'getCodeLists/$', codeUpload.getCodeLists, name='getCodeLists'),  
    url(r'getSaleLists/$', codeUpload.getSaleLists, name='getSaleLists'),  
    url(r'exportExcel/$', exportExcel.exportExcel, name='exportExcel'),  

    url(r'saveMsgSup/*', msg_send.saveMsgSup, name='saveMsgSup'), 
    url(r'saveMsg/*', msg_send.saveMsg, name='saveMsg'),
    url(r'feedback_gy/*', msg_send.feedback_gy, name='feedback_gy'), 

    url(r'uploadSE/*', upload.uploadSE, name='uploadSE'), 
    url(r'uploadHT/*', upload.uploadHT, name='uploadHT'),
]
