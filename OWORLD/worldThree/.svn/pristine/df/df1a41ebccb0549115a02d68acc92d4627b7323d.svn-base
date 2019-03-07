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
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,ToUnicode,HttpResponseCORS,fs_url,oSysInfo,m_aesKey,m_prjname,mValidateUser
from django.http import HttpResponseRedirect  

def LinkToShajd(request):
    AccessToken = request.GET.get('AccessToken', '')
    wxcpt=WXBizMsgCrypt('szoworld',m_aesKey)
    ret,login_id,sTimeStamp = wxcpt.DecryptMsg(AccessToken)   
    if (ret !=0):
        s = """
            {
            "errcode": -1,
            "errmsg": "验证信息有误，请重新登陆！",
            }        """
        return HttpResponseCORS(request,s)   

    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   
    proj_id =  request.GET.get('id','')
    L = ['','','']
    team_uuid = 'e015c3bd59ba11e88a8d7cd30abeb520'

    sql = "select usr_id,login_id,usr_name,password,ifnull(mobil,'') from users where login_id='%s'"%(login_id)
    rows,iN = db.select(sql)
    names = 'usr_id login_id usr_name password phone'.split()
    data = dict(zip(names, rows[0]))

    sql = "select id,cname,gc_no from out_proj where id='%s'"%(proj_id)
    rows,iN = db.select(sql)
    names = 'proj_id proj_name proj_code'.split()
    data1 = dict(zip(names, rows[0]))
    
    L[0] = team_uuid
    L[1] = data
    L[2] = data1
    names = 'team_uuid user proj'.split()
    L = dict(zip(names, L))
    info = json.dumps(L,ensure_ascii=True)

    #print info
    sTimeStamp = str(time.time())
    wxcpt=WXBizMsgCrypt('szoworld',m_aesKey)
    
    ret,token = wxcpt.EncryptMsg(info,random_no,sTimeStamp)            

    #wxcpt1=WXBizMsgCrypt('szoworld',m_aesKey)
    #ret,info1,sTimeStamp1 = wxcpt1.DecryptMsg(token)   

    url = "https://www.shajd.cn/login_schedule.html?team_id=%s&token=%s"%(team_uuid,urllib.quote(token))
    return HttpResponseRedirect(url)