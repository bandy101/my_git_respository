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
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,fs_url,oSysInfo,m_aesKey
import re

def ProcessPassword(inputPassword): 
    #处理正则表达式 
    #isMatch = bool(re.match(r"[a-zA-Z0-9]{6,}",inputPassword,flags=0)); 
    isMatch = True

    if len(inputPassword)<6 or len(inputPassword)>20:
        isMatch = False
        
    #用type的三位表示数字type[0]，小写字母type[1]，大写字母type[2]是否都具备 
    
    if isMatch: 
        type = [False,False,False] 
        for i in range(0,len(inputPassword)): 
            temp = inputPassword[i] 
            if ord(temp) >= ord('0') and ord(temp) <= ord('9'): 
                type[0] = True; 
            elif ord(temp) >= ord('a') and ord(temp) <= ord('z'): 
                type[1] = True; 
            elif ord(temp) >= ord('A') and ord(temp) <= ord('Z'): 
                type[2] = True; 
        for i in type: 
            if i is False: 
                isMatch = False; 
                break; 
    #处理是否有重复的字符出现 
    #if isMatch: 
    #    for i in range(0,7):  
    #        temp = inputPassword[i]; 
    #        for j in range(i + 1,8): 
    #            if inputPassword[j] == temp: 
    #                isMatch = False; 
    #                break; 
      
    return isMatch; 

def modify_pwd(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   
    #print request.POST
    login_id =  request.POST.get('login_id','')
    oldPwd =  request.POST.get('oldPwd','')
    newPwd =  request.POST.get('newPwd','')

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
    if oldPwd!='':
        oldPwd=oldPwd.lower()

    s1 =''
    sql="""SELECT U.usr_id,U.usr_name,ifnull(U.dept_id,0),ifnull(D.cname,''),IFNULL(U.pic,''),U.password
                   FROM users U LEFT JOIN dept D ON U.dept_id=D.id
                   WHERE U.login_id='%s' AND U.status=1 
                """ % (login_id)
    lT,iN = db.select(sql)
    if iN>0:
        usr_id = lT[0][0]
        pwd1 = lT[0][5]
        m1 = md5.new()   
        m1.update(lT[0][5])   
        pwd = m1.hexdigest()   
        if oldPwd != pwd:
            errCode = 2
            msg = u'密码错误'
        else:
            sql = "update users set password = '%s' where usr_id =%s"%(newPwd,usr_id)
            db.executesql(sql)
            errCode = 0
            msg = u'修改成功'
    else:
        errCode = 1
        msg = u'用户名不存在'
    s = """
        {
            "errcode": %s,
            "errmsg": "%s",
            "login_id": "%s",
        }
        """ %(errCode,msg,login_id)  
    return HttpResponseCORS(request,s)
