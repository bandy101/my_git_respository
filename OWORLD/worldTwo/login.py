# -*- coding: utf-8 -*-
# 尝试
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
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,fs_url,oSysInfo,m_aesKey,m_prjname,m_muti_lang

def login_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   
    usr_id,usr_name,dept_id,dept_name='','','',''
    login_id =  request.POST.get('login_id','') or request.GET.get('login_id','')
    password =  request.POST.get('password','') or request.GET.get('password','')
    source =  request.POST.get('source','web')
    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  
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
        response = HttpResponseCORS(request,s)
        return response
    login_id=login_id.replace("'","")
    if password!='':
        password=password.lower()

    s1 =''
    sql="""SELECT U.usr_id,U.usr_name,ifnull(U.dept_id,0),ifnull(D.cname,''),IFNULL(U.pic,''),U.password
                   FROM users U LEFT JOIN dept D ON U.dept_id=D.id
                   WHERE U.login_id='%s' AND U.status=1 
                """ % (login_id)
    lT,iN = db.select(sql)
    if iN>0:
        pwd1 = lT[0][5]
        m1 = md5.new()   
        m1.update(lT[0][5])   
        pwd = m1.hexdigest()   
        if password != pwd:
            errCode = 2
            msg = u'密码错误'
        else:
            ret = True
            if ret == False:
                errCode = 3
                msg = u'密码过于简单，请修改密码后重新登陆'
                s = """
                    {
                    "errcode": %s,
                    "errmsg": "%s",
                    "login_id": "%s",
                    }
                    """ %(errCode,msg,login_id)  
                response = HttpResponseCORS(request,s)
                return response
            usr_id=lT[0][0]
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
            
            if m_muti_lang==1 and lang_id>1:
                if usr_id in [1,2]:
                    sql="""SELECT distinct WMF.menu,WMF.menu_id,case l.`name` when '' then WMF.menu_name else l.`name` end,
                           WMF.sort,WMF.parent_id,WMF.status,WMF.url,WMF.icon
                           FROM menu_func WMF 
                           Left JOIN menu_func WMF1 on WMF.parent_id = WMF1.menu_id
                           left join muti_lang_menu l on l.menu_id = WMF.menu_id and l.lang_id = %s
                           WHERE WMF.status=1 and WMF.menu_id>0 and WMF1.status=1
                           ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                        """%(lang_id)
                else:
                    sql="""SELECT distinct WMF.menu,WMF.menu_id,case l.`name` when '' then WMF.menu_name else l.`name` end,
                           WMF.sort,WMF.parent_id,WMF.status,WMF.url,WMF.icon
                           FROM usr_role WUR JOIN (role_menu WRM JOIN menu_func WMF ON WRM.menu_id=WMF.menu_id) ON WUR.role_id=WRM.role_id
                           left join muti_lang_menu l on l.menu_id = WMF.menu_id and l.lang_id = %s
                           WHERE WUR.usr_id='%s' AND WMF.status=1 and WMF.menu_id>0 and WRM.can_view=1
                           ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                        """%(lang_id,usr_id)
            else:
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

def logout_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   

    login_id =  request.GET.get('login_id','')

    errCode = 0
    msg = u'Log Out'
    try:
        del request.session['usr_id']
    except KeyError:
        pass
    print request.POST
    s = """
        {
            "errcode": %s,
            "errmsg": "%s",
            "login_id": "%s",
        }
        """ %(errCode,msg,login_id)  
    return HttpResponseCORS(request,s)

def menu_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   

    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    usr_id =  request.POST.get('usr_id','') or request.GET.get('usr_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)
 
    if m_muti_lang==1 and lang_id>1:
        if str(usr_id) in ['1','2']:
            sql="""SELECT distinct WMF.menu,WMF.menu_id,case l.`name` when '' then WMF.menu_name else l.`name` end,
                   WMF.sort,WMF.parent_id,WMF.status,WMF.url,WMF.icon
                   FROM menu_func WMF 
                   Left JOIN menu_func WMF1 on WMF.parent_id = WMF1.menu_id
                   left join muti_lang_menu l on l.menu_id = WMF.menu_id and l.lang_id = %s
                   WHERE WMF.status=1 and WMF.menu_id>0 and WMF1.status=1
                   ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                """%(lang_id)
        else:
            sql="""SELECT distinct WMF.menu,WMF.menu_id,case l.`name` when '' then WMF.menu_name else l.`name` end,
                   WMF.sort,WMF.parent_id,WMF.status,WMF.url,WMF.icon
                   FROM usr_role WUR JOIN (role_menu WRM JOIN menu_func WMF ON WRM.menu_id=WMF.menu_id) ON WUR.role_id=WRM.role_id
                   left join muti_lang_menu l on l.menu_id = WMF.menu_id and l.lang_id = %s
                   WHERE WUR.usr_id='%s' AND WMF.status=1 and WMF.menu_id>0 and WRM.can_view=1
                   ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                """%(lang_id,usr_id)
    else:
        if str(usr_id) in ['1','2']:
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
    names = 'level menu_id menu_name sort parent_id status url icon'.split()
    data = [dict(zip(names, d)) for d in rows]
    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
            "errcode": 0,
            "errmsg": "获取数据成功",
            "menu_data": %s,
        }
        """ %(s3)  
    return HttpResponseCORS(request,s)