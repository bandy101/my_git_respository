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
from share import db,is_lock,is_valid,generate_valid,create_db,DB_Op,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,fs_url,oSysInfo,m_aesKey,m_prjname,m_muti_lang
from users import ProcessPassword
import re

# 验证码接口
def valid_generater(request):
    errCode = 0
    imgcode = ''

    login_id =  request.POST.get('login_id','') or request.GET.get('login_id','')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        login_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        login_ip = request.META['REMOTE_ADDR']  
    try:
        imgcode,_real_valid = generate_valid()
        msg = u'获取成功'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "imgcode": "%s",
            "login_id":'%s',
            }
            """%(errCode,msg,imgcode,_real_valid,login_id)
        DB_Op('temp_sheet',['valid_code'],\
                    ["'%s'"%_real_valid],"where temp_id='%s' and temp_ip='%s' "%(login_id,login_ip))
        print("where temp_id='%s' and temp_ip='%s' "%(login_id,login_ip))
    
    except:
        errCode = -1
        msg = u'获取失败'
        imgcode = ''
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "imgcode": "%s",
            }
            """%(errCode,msg,imgcode)

    
    response = HttpResponseCORS(request,s)
    return response


# 修改密码`
def change_pwd(request):
    errCode = 0
    msg = u''
    now = datetime.datetime.now()
    login_id =  request.POST.get('login_id','') or request.GET.get('login_id','')
    oldpwd = request.POST.get('oldpassword','') or request.GET.get('oldpassword','')
    password =  request.POST.get('password_login','') or request.GET.get('password_login','')

    # 判断旧密码是否正确
    sql = "select password from `users` where login_id='%s'"%(login_id)
    rows,iN = db.select(sql)
    print(request.POST)
    print('rows:',rows,login_id)
    if iN:
        print('###:',oldpwd,rows[0][-1])
        if oldpwd != rows[0][0]:
            errCode = 1
            msg = u'旧密码输入错误'
            s = """
                {
                "errcode": %s,
                "errmsg": "%s",
                "login_id": "%s",
                }
                """ %(errCode,msg,login_id)
            response = HttpResponseCORS(request,s)
    # else:
    #     errCode = 1
    #     msg = u'旧密码输入错误'
    # 判断新密码是否符合要求
    sql = "select old_password from `usr_history_info` where login_id='%s'"%(login_id)

    rows,iN = db.select(sql)
    if not password or password in [_[0] for _ in rows]:
        errCode = 2
        msg = u'不能使用历史密码或空密码！'
    
    if not errCode:
        # 更新用户记录表
        DB_Op('users',['password'],["'%s'"%password]," where login_id='%s'"%login_id)
        DB_Op('login_record',['pwd_update_time'],["'%s'"%now]," where login_id='%s'"%(login_id))
        
        sql = "select create_time,pwd_update_time from `login_record` where login_id='%s'"%(login_id)
        rows,iN = db.select(sql)
        print request.POST
        print(rows)
        # 插入历史数据
        old_createTime = rows[0][-1] or rows[0][0] or now # 优先密码更新时间
        DB_Op('usr_history_info',['login_id','old_password','old_createTime'],\
                ["'%s'"%login_id,"'%s'"%oldpwd,"'%s'"%old_createTime],'insert')

    s = """
        {
        "errcode": %s,
        "errmsg": "%s",
        "login_id": "%s",
        }
        """ %(errCode,msg,login_id)
    response = HttpResponseCORS(request,s)
    return response


# 提示过期账户
def update_login(request):
    # 取消账户过期提示（90天）
    login_id =  request.POST.get('login_id','') or request.GET.get('login_id','')
    ignore   = request.POST.get('is_ignore','') or request.GET.get('is_ignore','')
    now = datetime.datetime.now()
    if ignore:
        DB_Op('usr_info',['update_time'],["'%s'"%now]," where login_id='%s'"%login_id)
    errCode = 0
    msg = u'操作成功'
    s = """
        {
        "errcode": %s,
        "errmsg": "%s",
        "login_id": "%s",
        }
        """ %(errCode,msg,login_id)
    response = HttpResponseCORS(request,s)
    return response


# 解锁 将login_record login_time（60天） 改成当前时间进行解锁
def update_login_lock(request):
    login_id =  request.POST.get('login_id','') or request.GET.get('login_id','')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        login_ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        login_ip = request.META['REMOTE_ADDR']  
    DB_Op('login_record',['login_ip','login_time'],\
                    ["'%s'"%login_ip,"'%s'"%(currentTime)]," where login_id='%s'"%(login_id))



# 登录验证
def login_test(request):
    currentTime = datetime.datetime.now()   # 当前时间
    errCode = -1
    msg, s='', ''   # 返回的基础信息
    error_count = 0
    login_id =  request.POST.get('login_id','') or request.GET.get('login_id','')
    password =  request.POST.get('password','') or request.GET.get('password','')
    valid_code = request.POST.get('valid','') or request.GET.get('valid','')

    print('VALID`VALID`:',valid_code)

    image_code, valid_code_real = '','' # 图片数据 验证码 -1 or ''

    # print(valid_code_real)
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        login_ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        login_ip = request.META['REMOTE_ADDR']
    # 获取验证码
    _sql = """
        select valid_code from `temp_sheet` where temp_id='%s' and temp_ip='%s'
        """%(login_id,login_ip)
    rows,iN = db.select(_sql)
    if iN:
        valid_code_real = rows[0][-1] # 验证码
        print('valid:',valid_code_real)


    # login_id = 'abc'
    sql = """
            select password,usr_name from `users` where login_id='%s'
            """%(login_id)
    rows,iN= db.select(sql)
    if iN:
        real_pwd = [_[0] for _ in rows][0]
    else:
        real_pwd = ''
    print(sql)
    if not iN:
        errCode = -1
        msg = u'用户名不存在!'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "login_id": "%s",
            }
            """ %(errCode,msg,login_id)
        response = HttpResponseCORS(request,s)
        return response
    else:   
        usr_name = rows[0][1]
        # 密码正确 记录登录信息到相应表
        # m1 = md5.new() 
        # m1.update(real_pwd.lower())
        # pwd_l = m1.hexdigest()
        # pwd_h = md5.new(real_pwd.upper()).hexdigest()
        pwd_real = md5.new(real_pwd).hexdigest()

        print('#-#valid:',valid_code_real,valid_code)
        if (password==real_pwd or password in [pwd_real]) and any([valid_code_real in ['','-1'],valid_code_real.lower() == valid_code.lower()]):
            # 检验是否过期
            if is_valid(login_id)>=90:
                errCode = 2 # 用户过期
                msg = u'用户已过期！'
                s ="""
                    {
                        "errcode":%s,
                        "errmsg:":%s",
                        "login_id":"%s",
                        "usr_name":"%s",

                    }
                    """%(errCode,msg,login_id,usr_name) 
                return HttpResponseCORS(request,s)
            if is_lock(login_id)>=60:
                errCode = 3 # 用户锁定
                msg = u'用户已锁定！'
                s ="""
                    {
                        "errcode":%s,
                        "errmsg:":%s",
                        "login_id":"%s",
                        "usr_name":"%s",

                    }
                    """%(errCode,msg,login_id,usr_name) 
                return HttpResponseCORS(request,s)
            # else:
            #     pass # 更新登录时间
            #     DB_Op('usr_info',['login_time'],[''])
            # print('match:',bool(re.compile('[a-z0-9A-Z]{8,16}').match(password)))

            if len(password)<8 or not bool(re.compile(r'^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).*$').match(password)):
                errCode = 4 # 弱密码
                msg = u'密码不符合要求请修改密码！'

                _sql = """
                    select login_id from `login_record` where login_id='%s' 
                    """%(login_id)
                print(_sql)
                print db.executesql(_sql)
            # 记录登录信息
                if not db.executesql(_sql):
                    DB_Op('login_record',['login_id','login_ip','login_time'],\
                        ["'%s'"%login_id,"'%s'"%login_ip,"'%s'"%(currentTime)],'insert')
                s ="""
                    {
                        "errcode":%s,
                        "errmsg:":'%s',
                        "login_id":"%s",
                        "usr_name":"%s",

                    }
                    """%(errCode,msg,login_id,usr_name)
                return HttpResponseCORS(request,s)

            errCode = 0
            msg = u'操作正确'
            _sql = """
                    select login_id from `login_record` where login_id='%s' 
                    """%(login_id)
            print db.executesql(_sql)
            # 记录登录信息
            if not db.executesql(_sql):
                DB_Op('login_record',['login_id','login_ip','login_time'],\
                    ["'%s'"%login_id,"'%s'"%login_ip,"'%s'"%(currentTime)],'insert')
            else:
                DB_Op('login_record',['login_ip','login_time'],\
                    ["'%s'"%login_ip,"'%s'"%(currentTime)]," where login_id='%s'"%(login_id))
        
            # 删除临时表中的记录
            _sql = "delete from `temp_sheet` where temp_id='%s' and temp_ip='%s'"%(login_id,login_ip)
            db.executesql(_sql)
            return None
        
        # 密码错误记录到临时表
        else:
            _sql = """
                    select temp_id,temp_ip,login_num from `temp_sheet` where temp_id='%s' and temp_ip='%s'
                    """%(login_id,login_ip)
            rows,iN = db.select(_sql)
            s +=''
            # 不存在记录 插入数据
            if not iN:
                DB_Op('temp_sheet',['temp_id','temp_ip','login_num','valid_code'],\
                    ["'%s'"%login_id,"'%s'"%login_ip,1,"''"],'insert')
                error_count = 1
            else:
                # 更新数据
                if int(rows[0][2])>=2:
                    image_code, valid_code_real = generate_valid()

                DB_Op('temp_sheet',['login_num','valid_code'],\
                    [int(rows[0][2])+1,"'%s'"%valid_code_real],"where temp_id='%s'"%(login_id))
                error_count =int(rows[0][2])+1
            errCode = -1    
            msg = u'账户或密码错误！'
            print(password,real_pwd,password == real_pwd)
            if password == real_pwd:
                msg = u'验证码错误！'
            s = """
                {
                "errcode": %s,
                "errmsg": "%s",
                "login_id": "%s",
                "image_code":"%s",
                "error_count":%s,
                "usr_name":"%s",
                }
                """ %(errCode,msg,login_id,image_code,error_count,usr_name)

            response = HttpResponseCORS(request,s)
            return response







def login_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))
    print(request.POST)
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
    
    response = login_test(request)
    if  response:
        return response
    
    print('验证借宿·············')


# ----#
    # if login_id=='':
    #     errCode = 1
    #     msg = u'用户名不存在'
    #     s = """
    #         {
    #         "errcode": %s,
    #         "errmsg": "%s",
    #         "login_id": "%s",
    #         }
    #         """ %(errCode,msg,login_id)  
    #     response = HttpResponseCORS(request,s)
    #     return response
    # login_id=login_id.replace("'","")
    # if password!='':
    #     password=password.lower()
# ---#
    s1 =''
    sql="""SELECT U.usr_id,U.usr_name,ifnull(U.dept_id,0),ifnull(D.cname,''),IFNULL(U.pic,''),U.password
                   FROM users U LEFT JOIN dept D ON U.dept_id=D.id
                   WHERE U.login_id='%s' AND U.status=1
                """ % (login_id)
    lT,iN = db.select(sql)
    if iN>0:
        # pwd1 = lT[0][5]
        # m1 = md5.new()   
        # m1.update(lT[0][5])   
        # pwd = m1.hexdigest()   
        # print(password,pwd,'###')
        # if password != pwd:
        #     errCode = 2
        #     msg = u'密码错误'
        # else:
        #     if m_prjname == 'kjerp':
        #         ret = ProcessPassword(pwd1)
        #     else:
        #         ret = True
        #     if ret == False:
        #         errCode = 3
        #         msg = u'密码过于简单，请修改密码后重新登陆'
        #         s = """
        #             {
        #             "errcode": %s,
        #             "errmsg": "%s",
        #             "login_id": "%s",
        #             }
        #             """ %(errCode,msg,login_id)  
        #         response = HttpResponseCORS(request,s)
        #         return response
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
            print(sql)
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
        #print sql   # ---#
            print(sql)
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
            # --#
    # else:
    #     errCode = 1
    #     msg = u'用户名不存在'

    # print('##:',s1)
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
