# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
from aesMsgCrypt                import WXBizMsgCrypt
import httplib
import urllib
from django.db import connection
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,front_url,fs_url,m_aesKey,m_corp_wxid,my_urlencode
from django.http import HttpResponseRedirect  
exec ('from %s.wx_cb.wxpush        import getuserinfo,getLoginID'%prj_name) 
exec ('from %s.common.wx_data        import *'%prj_name) 

def index_wx_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))
    source = 'wx'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  
    print ip
    code = request.GET.get('code','')
    func = request.GET.get('func','')
    if func == '':
        func = request.GET.get('state','')
    func = func.lower()
    if func in ['gwlist','gw_view','gw_audit','gw_sign']:
        agentname = '公文审批'
    elif func in ['info_send','info_list','info_upd','info_detail','info_audit']:
        agentname = '信息交换'
    elif func in ['myloglist','otherloglist','writelog','logdetail']:
        agentname = '工作日志'
    elif func in ['fa_code']:
        agentname = '固定资产管理'
    else:
        agentname = '通讯录'

    error_url = '%s/wx/mui/error.html'%front_url
    if func == 'FA_Code':
        FAcode = request.GET.get('facode','')
        url = '%s/wx/mui/fixedAssetsInfo.html?code=%s'%(front_url,FAcode)      
        return HttpResponseRedirect(url)

    url = ''
    if func == 'gwlist':
        type = request.GET.get('type','')
        if str(type) in ['1','2','3']:
            url = '%s/wx/mui/examine.html?func=%s&type=%s'%(front_url,func,type)
        else:
            url = '%s/wx/mui/myExamine.html?func=%s&type=%s'%(front_url,func,type)
    elif func == 'gw_view':
        menu_id = request.GET.get('menu_id','')
        pk = request.GET.get('pk','')
        url = '%s/wx/examineDetail.html?menu_id=%s&pk=%s&mode=view&infotype=msg'%(front_url,menu_id,pk)       
    elif func == 'gw_audit':
        menu_id = request.GET.get('menu_id','')
        pk = request.GET.get('pk','')
        url = '%s/wx/examineDetail.html?menu_id=%s&pk=%s&mode=audit&infotype=msg'%(front_url,menu_id,pk)       
    elif func == 'gw_sign':
        menu_id = request.GET.get('menu_id','')
        pk = request.GET.get('pk','')
        url = '%s/wx/examineDetail.html?menu_id=%s&pk=%s&mode=sign&infotype=msg'%(front_url,menu_id,pk)    
    elif func == 'info_send':
        url = '%s/wx/mui/infoExchange_index.html?id=2'%(front_url)       
    elif func == 'info_list':
        id = request.GET.get('id','')
        type = request.GET.get('type','')
        url = '%s/wx/mui/infoExchange_index.html?id=%s&type=%s'%(front_url,id,type)       
    elif func == 'info_audit':
        pk = request.GET.get('pk','')
        must_reply = request.GET.get('must_reply','')
        url = '%s/wx/mui/infoExamine.html?seq=%s&must_reply=%s&infotype=msg'%(front_url,pk,must_reply)       
    elif func == 'info_detail':
        pk = request.GET.get('pk','')
        must_reply = request.GET.get('must_reply','')
        url = '%s/wx/mui/infoDetail.html?seq=%s&must_reply=%s&index=0&infotype=msg'%(front_url,pk,must_reply)       
    elif func == 'info_upd':
        pk = request.GET.get('pk','')
        url = '%s/wx/mui/changeInfo.html?seq=%s&infotype=msg'%(front_url,pk)       
    elif func == 'fa_code':
        FAcode = request.GET.get('facode','')
        url = '%s/wx/mui/fixedAssetsInfo.html?code=%s'%(front_url,FAcode)        
    elif func == 'myloglist':
        url = '%s/wx/mui/myLogList.html?source=%s'%(front_url,source)       
    elif func == 'otherloglist':
        url = '%s/wx/mui/otherLogList.html?source=%s'%(front_url,source)       
    elif func == 'writelog':
        url = '%s/wx/mui/writeLog.html?source=%s'%(front_url,source)       
    elif func == 'logdetail':
        id = request.GET.get('id','')
        url = '%s/wx/mui/logDetail.html?id=%s'%(front_url,id)       
    else:
        return HttpResponseRedirect(error_url)

    if request.session.has_key('login_data_wx'):  
        d = request.session.get('login_data_wx','')
        #userid = request.COOKIES.get('usr_wx_id','')
        userid = d[0]
        print "userid=%s"%(userid)
        sql = """select token,id from users_login where source='%s' and usr_id ='%s'  and time_to_sec(now()) - time_to_sec(refresh_time) < expire_time order by refresh_time desc limit 1 
                    """%(source,userid)
        print sql
        lT,iN = db.select(sql)
        if iN>0:
            token=lT[0][0]
            id=lT[0][1]
            sql = "update users_login set refresh_time=now() where id=%s"%(id)
            db.executesql(sql)
            url += "&AccessToken=%s"%token
            print url
            dt = datetime.datetime.now() + datetime.timedelta(hours = 2)
            response = HttpResponseRedirect(url)
            response.set_cookie("usr_wx_id",userid,expires=dt)
            #sql = "select usr_id,usr_name,dept_id,login_id,d.cname from users  u left join dept d on d.id=u.dept_id where usr_id='%s' and status=1"%userid
            #lT,iN = db.select(sql)
            #if iN>0:
            #    value=[userid,lT[0][1],lT[0][2],lT[0][4],lT[0][3]]
            #    print value
            #    request.session['login_data_wx'] = value
            return response

    if code!='':
        ddata = getuserinfo(code,agentname)
        try:
            print ddata
            uName = ddata['UserId'] 
            DeviceId = ddata['DeviceId'] 
        except Exception, e:
            uName = ''
            DeviceId = ''
            return HttpResponseRedirect(error_url)

        sql = "select usr_id,usr_name,dept_id,login_id,d.cname from users  u left join dept d on d.id=u.dept_id where ifnull(wxqy_id,login_id)='%s' and status=1"%uName
        print sql
        lT,iN = db.select(sql)
        if iN >0 :
            userid=lT[0][0]
            usr_name = lT[0][1]
            dept_id = lT[0][2]
            dept_name = lT[0][4]
            login_id = lT[0][3]
            sTimeStamp = str(time.time())
            wxcpt=WXBizMsgCrypt('szoworld',m_aesKey)
            ret,token = wxcpt.EncryptMsg(login_id,random_no,sTimeStamp)     

            sql = """insert into users_login (usr_id,source,token,login_ip,login_time,refresh_time,expire_time)
                     values (%s,'%s','%s','%s',now(),now(),%s) 
                    """%(userid,source,token,ip,int(TIME_OUT)*60)
            print ToGBK(sql)
            db.executesql(sql)
            token = urllib.quote(token)
            url += "&AccessToken=%s"%token
            dt = datetime.datetime.now() + datetime.timedelta(hours = 2)
            response = HttpResponseRedirect(url)
            response.set_cookie("usr_wx_id",userid,expires=dt)

            value=[userid,usr_name,dept_id,dept_name,login_id]
            print value
            request.session['login_data_wx'] = value

            return response
        else:
            return HttpResponseRedirect(error_url)

    else:    #重定向以获取用户信息
        redirect_uri = request.get_full_path()
        redirect_uri = front_url + redirect_uri
        redirect_uri = my_urlencode(redirect_uri)
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo#wechat_redirect"%(m_corp_wxid,redirect_uri)
        print url
        return HttpResponseRedirect(url)

    return HttpResponseRedirect(error_url)

def get_data_wx_func(request):
    func = request.GET.get('func','')
    #print "func=%s"%func
    s = ''
    if func == 'gwlist':
        s = getGwList(request)
    elif func == 'infoType':
        s = infoType(request)
    elif func == 'getDepts':
        s = getDepts(request)
    elif func == 'getUsers':
        s = getUsers(request)
    elif func == 'getInfoGroup':
        s = getInfoGroup(request)
    elif func == 'getAuditUser':
        s = getAuditUser(request)
    elif func == 'infoList':
        s = getInfoList(request)
    elif func == 'infoDetail':
        s = getInfoDetail(request)
    elif func == 'infoComment':
        s = getInfoComment(request)

    return s

def login_wx_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   
    usr_id,usr_name,dept_id,dept_name='','','',''
    source =  'wx'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  

    code = request.GET.get('code','')
    login_id = getLoginID(code)
    if login_id=='':
        errCode = 1
        msg = u'用户名不存在'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "login_id": "%s",
            }
            """ %(errCode,msg,login_id)  
        return s

    login_id=login_id.replace("'","")

    s1 =''
    sql="""SELECT U.usr_id,U.usr_name,U.dept_id,D.cname,IFNULL(U.pic,''),U.password,U.login_id
                   FROM users U LEFT JOIN dept D ON U.dept_id=D.id
                   WHERE ifnull(U.wxqy_id,U.login_id)='%s' AND U.status=1 
                """ % (login_id)
    lT,iN = db.select(sql)
    if iN>0:
        usr_id=lT[0][0]
        login_id = lT[0][6]
        #求得用户的权限
        dActiveUser[usr_id]={}
        dActiveUser[usr_id]['roles']={}                       #用户角色
        dActiveUser[usr_id]['access_dept_data']=[]            #访问部门内所有人员数据的权限,格式:['部门ID1','部门ID2',...]
        dActiveUser[usr_id]['access_person_data']=[]          #访问人员数据的权限,格式:['人员ID1','人员ID2',...]
        dActiveUser[usr_id]['login_time']=time.time()         #登入时间
        dActiveUser[usr_id]['usr_name']=lT[0][1]              #用户名
        dActiveUser[usr_id]['login_id']=login_id
        dActiveUser[usr_id]['usr_dept']=lT[0][2],lT[0][3]           #用户部门
        dActiveUser[usr_id]['pic']=lT[0][4]
                
        #用户角色/访问部门内所有人员数据的权限
        sql="""SELECT WUR.role_id,WR.role_name,WR.sort,WR.dept_id
                       FROM usr_role WUR LEFT JOIN roles WR ON WUR.role_id=WR.role_id
                       WHERE WUR.usr_id=%s
            """ % usr_id
        lT1,iN1 = db.select(sql)
        if iN1>0:
            for e in lT1:
                #用户角色
                dActiveUser[usr_id]['roles'][e[0]]=e[1:]   

        request.session['usr_id'] = usr_id
        request.session['usr_name'] = dActiveUser[usr_id]['usr_name']
        request.session['dept_id'] = lT[0][2]
        request.session['dept_name'] = lT[0][3]
        request.session['dActiveUser'] = dActiveUser
        d_value = ['','','','','']
        d_value[0] = usr_id
        d_value[1] = dActiveUser[usr_id]['usr_name']
        d_value[2] = lT[0][2]
        d_value[3] = lT[0][3]
        d_value[4] = 0
        g_data.set_value(d_value)
        errCode = 0
        msg = 'OK'
        pic = lT[0][4]
        if pic=='':
            pic_url = "%s/user_pic/default.jpg"%fs_url
        else:
            pic_url = "%s/user_pic/small_"%fs_url+pic
        sTimeStamp = str(time.time())
        wxcpt=WXBizMsgCrypt('szoworld',m_aesKey)
        ret,token = wxcpt.EncryptMsg(login_id,random_no,sTimeStamp)   

        if usr_id in [1,2]:
            sql="""SELECT distinct WMF.menu,WMF.menu_id,WMF.menu_name,
                   WMF.sort,WMF.parent_id,WMF.status,WMF.url,WMF.icon
                   FROM menu_func WMF 
                   Left JOIN menu_func WMF1 on WMF.parent_id = WMF1.menu_id
                   WHERE WMF.status=1 and WMF.menu_id>0 and WMF1.status=1
                   ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                """
        else:
            sql="""SELECT distinct WMF.menu,WMF.menu_id,WMF.menu_name,
                   WMF.sort,WMF.parent_id,WMF.status,WMF.url,WMF.icon
                   FROM usr_role WUR JOIN (role_menu WRM JOIN menu_func WMF ON WRM.menu_id=WMF.menu_id) ON WUR.role_id=WRM.role_id
                   WHERE WUR.usr_id='%s' AND WMF.status=1 and WMF.menu_id>0 and WRM.can_view=1
                   ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                """%usr_id
        #print sql
        rows,iN = db.select(sql)
        L1=[2]
        L2=[]
        #L = formatData(rows,L1,L2)
        names = 'level menu_id menu_name sort parent_id status url icon'.split()
        data = [dict(zip(names, d)) for d in rows]

        s3 = json.dumps(data,ensure_ascii=False)

        s1 = """"userid":%s,
                "username":"%s",
                "dept_id":%s,
                "dept_name":"%s",
                "pic_url":"%s",
                "AccessToken":"%s",
                "menu_data":%s,"""%(lT[0][0],(lT[0][1]),lT[0][2],(lT[0][3]),pic_url,token,s3)
        sql = """insert into users_login (usr_id,source,token,login_ip,login_time,refresh_time,expire_time)
                 values (%s,'%s','%s','%s',now(),now(),%s) 
                """%(lT[0][0],source,token,ip,int(TIME_OUT)*60)
        #print ToGBK(sql)
        
        db.executesql(sql)
    else:
        errCode = 1
        msg = u'用户名不存在'
    s = """
        {
            "errcode": %s,
            "errmsg": "%s",
            "login_id": "%s",
            %s
        }
        """ %(errCode,msg,login_id,s1)  
    #print ToGBK(s)
    response = HttpResponseCORS(request,s)
    return response
