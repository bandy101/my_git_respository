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
from django.contrib import admin
from . import test
from . import login
from . import checkLogin
from . import wxpush
from . import main
from . import main_qy
from . import fileUpload
from . import common
from . import msgread
from . import msgread_qy
from . import main_tj
from . import main_tj_qy
from . import main_gy
from . import main_gy_qy
from . import fileUpload_gy
from . import msgread_gy
from . import msgread_gy_qy
from . import labor
from . import wechatPush

urlpatterns = [
    url(r'^test/', test.application, name='test'), 
    # url(r'^login/', login.index, name='login'), 
    url(r'^login/index$', login.index, name='login'),
    url(r'^login/login_qy$', login.login_qy, name='login'),
    url(r'^login/default$', login.default, name='login'), 
    url(r'^login/default_tj$', login.default_tj, name='login'), 
    url(r'^login/index_tj$', login.index_tj, name='login'),
    url(r'^login/index_gy$', login.index_gy, name='login'),
    url(r'^login/default_gy$', login.default_gy, name='login'),
    # url(r'^wxpush/', wxpush.callback, name='wxpush'), 
    # url(r'^wxpush/', wxpush.lw, name='wxpush'),  
    url(r'^wxpush/callback$', wxpush.callback, name='wxpush'),
    url(r'^wxpush/callback_tj$', wxpush.callback_tj, name='wxpush'),
    url(r'^wxpush/callback_gy$', wxpush.callback_gy, name='wxpush'),
    url(r'^wxpush/lw$', wxpush.lw, name='wxpush'),
    url(r'^wxpush/tj$', wxpush.tj, name='wxpush'),
    url(r'^wxpush/gy$', wxpush.gy, name='wxpush'),
    url(r'^checkLogin/getCode$', checkLogin.getCode, name='checkLogin'), 
    url(r'^checkLogin/checkPass$', checkLogin.checkPass, name='checkLogin'),
    url(r'^checkLogin/myInfo$', checkLogin.myInfo, name='checkLogin'), 

    url(r'^main/getLabourContractList$', main.getLabourContractList, name='main'), 
    url(r'^main/getProgressDetail$', main.getProgressDetail, name='main'), 
    url(r'^main/saveProgressDetail$', main.saveProgressDetail, name='main'), 
    url(r'^main/getProgressList$', main.getProgressList, name='main'), 

    url(r'^main/getAgreementList$', main.getAgreementList, name='main'), 
    url(r'^main/agreementDetail$', main.agreementDetail, name='main'),
    url(r'^main/myComplaint$', main.myComplaint, name='main'),
    url(r'^main/putComplaint$', main.putComplaint, name='main'),
    url(r'^main/myComplaintDetail$', main.myComplaintDetail, name='main'), 
    url(r'^main/closeFile$', main.closeFile, name='main'),  

    url(r'^fileUpload/attach_save$', fileUpload.attach_save, name='fileUpload'),
    url(r'^fileUpload/attach_save_qy$', fileUpload.attach_save_qy, name='fileUpload'),
    url(r'^fileUpload/del_attach_file$', fileUpload.del_attach_file, name='fileUpload'),
    url(r'^fileUpload/file_down$', fileUpload.file_down, name='fileUpload'),
    url(r'^main_qy/myComplaint$', main_qy.myComplaint, name='main_qy'),
    url(r'^main_qy/myComplaintDetail$', main_qy.myComplaintDetail, name='main_qy'), 
    url(r'^main_qy/putFlowDetail$', main_qy.putFlowDetail, name='main_qy'), 
    url(r'^main_qy/putFlow$', main_qy.putFlow, name='main_qy'),
    url(r'^main_qy/putMessage$', main_qy.putMessage, name='main_qy'),
    url(r'^main_qy/putFlowSj$', main_qy.putFlowSj, name='main_qy'),
    url(r'^main_qy/getProgressList$', main_qy.getProgressList, name='main_qy'), 
    url(r'^main_qy/cancelProgress$', main_qy.cancelProgress, name='main_qy'), 

    # url(r'^main_qy/mWxPushMsg_Comment_fw$', main_qy.mWxPushMsg_Comment_fw, name='main_qy'),
    url(r'^common/getDepts$', common.getDepts, name='common'), 
    url(r'^common/getUsers$', common.getUsers, name='common'),  
    url(r'^common/getSituation$', common.getSituation, name='common'), 
    url(r'^common/getTypeList$', common.getTypeList, name='common'),
    url(r'^common/getTypeList_gy$', common.getTypeList_gy, name='common'),
    url(r'^common/getMtcType$', common.getMtcType, name='common'),
    url(r'^common/getLaborTeam$', common.getLaborTeam, name='common'),
    url(r'^common/getProj$', common.getProj, name='common'),
    url(r'^common/makeMenu$', common.makeMenu, name='common'), 
    url(r'^msgread/getMsgList$', msgread.getMsgList, name='msgread'), 
    url(r'^msgread/msgDetail$', msgread.msgDetail, name='msgread'), 
    url(r'^msgread/joinToubiao$', msgread.joinToubiao, name='msgread'),
    url(r'^msgread_qy/getMsgList$', msgread_qy.getMsgList, name='msgread_qy'),
    url(r'^msgread_qy/msgDetail$', msgread_qy.msgDetail, name='msgread_qy'),
    url(r'^msgread_qy/putToubiao$', msgread_qy.putToubiao, name='msgread_qy'),

    url(r'^main_tj/getProjList$', main_tj.getProjList, name='main_tj'),
    url(r'^main_tj/getProjTrack$', main_tj.getProjTrack, name='main_tj'),
    url(r'^main_tj/putProjTrack$', main_tj.putProjTrack, name='main_tj'),
    url(r'^main_tj_qy/getProjList$', main_tj_qy.getProjList, name='main_tj_qy'),
    url(r'^main_tj_qy/getProjTrack$', main_tj_qy.getProjTrack, name='main_tj_qy'),
    url(r'^main_tj_qy/putProjTrack$', main_tj_qy.putProjTrack, name='main_tj_qy'),

    url(r'^main_gy/getContractList$', main_gy.getContractList, name='main_gy'),
    url(r'^main_gy/getMatBuyList$', main_gy.getMatBuyList, name='main_gy'),
    url(r'^main_gy/complaintDetail$', main_gy.complaintDetail, name='main_gy'),
    url(r'^main_gy/putComplaint$', main_gy.putComplaint, name='main_gy'),
    url(r'^main_gy/myComplaint$', main_gy.myComplaint, name='main_gy'),
    url(r'^main_gy/myComplaintDetail$', main_gy.myComplaintDetail, name='main_gy'),
    url(r'^main_gy/putEvaluation$', main_gy.putEvaluation, name='main_gy'),

    url(r'^main_gy/feedbackResult$', main_gy.feedbackResult, name='main_gy'),

    url(r'^main_gy/incorruptDetail$', main_gy.incorruptDetail, name='main_gy'),
    url(r'^main_gy/putIncorruptComplaint$', main_gy.putIncorruptComplaint, name='main_gy'),
    url(r'^main_gy/myIncorruptComplaint$', main_gy.myIncorruptComplaint, name='main_gy'),
    url(r'^main_gy/myIncorruptComplaintDetail$', main_gy.myIncorruptComplaintDetail, name='main_gy'),
    url(r'^main_gy_qy/myIncorruptComplaint$', main_gy_qy.myIncorruptComplaint, name='main_gy_qy'),
    url(r'^main_gy_qy/myIncorruptComplaintDetail$', main_gy_qy.myIncorruptComplaintDetail, name='main_gy_qy'), 
    url(r'^main_gy_qy/putIncorruptFlow$', main_gy_qy.putFlow_incorrupt, name='main_gy_qy'),
    url(r'^main_gy_qy/putIncorruptMessage$', main_gy_qy.putMessage_incorrupt, name='main_gy_qy'),

    url(r'^main_gy/closeFile$', main_gy.closeFile, name='main_gy'),   
    url(r'^fileUpload_gy/attach_save$', fileUpload_gy.attach_save, name='fileUpload_gy'),
    url(r'^fileUpload_gy/attach_save_qy$', fileUpload_gy.attach_save_qy, name='fileUpload_gy'),
    url(r'^fileUpload_gy/del_attach_file$', fileUpload_gy.del_attach_file, name='fileUpload_gy'),
    url(r'^fileUpload_gy/file_down$', fileUpload_gy.file_down, name='fileUpload_gy'),
    url(r'^main_gy_qy/myComplaint$', main_gy_qy.myComplaint, name='main_gy_qy'),
    url(r'^main_gy_qy/myComplaintDetail$', main_gy_qy.myComplaintDetail, name='main_gy_qy'), 
    url(r'^main_gy_qy/putFlowDetail$', main_gy_qy.putFlowDetail, name='main_gy_qy'), 
    url(r'^main_gy_qy/putFlow$', main_gy_qy.putFlow, name='main_gy_qy'),
    url(r'^main_gy_qy/putMessage$', main_gy_qy.putMessage, name='main_gy_qy'),
    url(r'^main_gy_qy/putFlowSj$', main_gy_qy.putFlowSj, name='main_gy_qy'),
    url(r'^msgread_gy/getMsgList$', msgread_gy.getMsgList, name='msgread_gy'), 
    url(r'^msgread_gy/msgDetail$', msgread_gy.msgDetail, name='msgread_gy'), 
    url(r'^msgread_gy/putFeedback$', msgread_gy.putFeedback, name='msgread_gy'),
    url(r'^msgread_gy/payInfo$', msgread_gy.payInfo, name='msgread_gy'), 
    url(r'^msgread_gy/joinToubiao$', msgread_gy.joinToubiao, name='msgread_gy'),
    url(r'^msgread_gy/getInvoiceData$', msgread_gy.getInvoiceData, name='msgread_gy'),
    url(r'^msgread_gy/exportInvoiceExcel$', msgread_gy.exportInvoiceExcel, name='msgread_gy'),

    url(r'^msgread_gy_qy/getMsgList$', msgread_gy_qy.getMsgList, name='msgread_gy_qy'),
    url(r'^msgread_gy_qy/msgDetail$', msgread_gy_qy.msgDetail, name='msgread_gy_qy'),
    url(r'^msgread_gy_qy/putToubiao$', msgread_gy_qy.putToubiao, name='msgread_gy_qy'),
    url(r'^msgread_gy_qy/otherMsgList$', msgread_gy_qy.otherMsgList, name='msgread_gy_qy'),
    url(r'^msgread_gy_qy/otherMsgDetail$', msgread_gy_qy.otherMsgDetail, name='msgread_gy_qy'),
    url(r'^msgread_gy_qy/putFeedback$', msgread_gy_qy.putFeedback, name='msgread_gy_qy'),

    url(r'^labor/putProj$', labor.putProj, name='labor'),
    url(r'^labor/getPartnerDetail$', labor.getPartnerDetail, name='labor'),
    url(r'^labor/getSucessInfo$', labor.getSucessInfo, name='labor'),
    url(r'^labor/getLaborInfo$', labor.getLaborInfo, name='labor'),
    url(r'^labor/getCompanyType$', labor.getCompanyType, name='labor'),
    url(r'^labor/uploadSafetyEducation$', labor.uploadSafetyEducation, name='labor'),
 
    url(r'^wechatPush/supplierPayInfo$', wechatPush.supplierPayInfo, name='wechatPush'),

    url(r'^gy/', include('%s.gy.urls'%prj_name)),  
]
