# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,host_url,my_urlencode,read_access_token_common,write_access_token_common'%prj_name)
exec ('from %s.share        import data_url,AppId_gy,AppSecret_gy,template_id_msg_gy,template_id_result_gy'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
import datetime
from HW_DT_TOOL                 import getToday
import MySQLdb
# testid = 2029
testid = 0
access_sToken='Js_#81L&DKk12_@$fJ81d4a2fD'

def supplierPayInfo(request):
    gw_id = request.POST.get('gw_id','')  #公文ID
    sToken = request.POST.get('sToken','') #key
    print request.POST
    # gw_id=100029421
    # gw_id='100196450'
    # sToken='Js_#81L&DKk12_@$fJ81d4a2fD'
    if gw_id=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "error!"
        }        """
        return HttpResponseJsonCORS(s)
    if sToken !=access_sToken:
        s = """
        {
        "errcode": -2,
        "errmsg": "error!"
        }        """
        return HttpResponseJsonCORS(s)
    try:
        gw_id=int(gw_id)
    except:
        s = """
        {
        "errcode": -99,
        "errmsg": "非法字符!"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT PMP.id,UG.openid,PMP.pjname,now(),PMP.Sup_id,UG.usr_id
        FROM (SELECT a.* FROM prj_mat_pay a WHERE NOT EXISTS(SELECT 1 FROM complaint_sup_payinfo_push b WHERE a.id=b.m_id) )PMP 
        LEFT JOIN addr_book AB ON AB.sup_id=PMP.Sup_id AND AB.sup_id is not null
        LEFT JOIN users_gy UG ON UG.addr_id=AB.id
        WHERE UG.status=1 AND PMP.is_push=0
        AND IFNULL(UG.openid,'')!=''
        AND PMP.gw_id=%s"""%(gw_id)
    row,iN=db.select(sql)
    if iN>0:
        pk=row[0][0]
        openid=row[0][1]
        pjname=row[0][2]
        pushTime=row[0][3]
        sup_id=row[0][4]
        usr_id=row[0][5]
        errcode = mWxPushMsg_fw_gy(pjname,pk,openid)
        if str(errcode)=='0':
            sql="""INSERT INTO complaint_sup_payinfo_push(ctime,m_id,to_usr_id,sup_id) VALUES(now(),%s,%s,%s)"""%(pk,usr_id,sup_id)
            db.executesql(sql)
            sql="""UPDATE prj_mat_pay SET is_push=1 WHERE id=%s"""%(pk)
            db.executesql(sql)
            s = """
            {
            "errcode": 0,
            "errmsg": "发送成功!"
            }        """
            return HttpResponseJsonCORS(s)
        else:
            s = """
            {
            "errcode": %s,
            "errmsg": "发送失败!"
            }        """%(errcode)
            return HttpResponseJsonCORS(s)
    else:
        s = """
        {
        "errcode": -3,
        "errmsg": "发送对象还未绑定到供应商平台!"
        }        """
        return HttpResponseJsonCORS(s)

import httplib
def mWxPushMsg_fw_gy(pjname,pk,toUser):  
    #获取当前日期
    t=time.time()
    date_ary=time.localtime(t)
    y=time.strftime("%Y-%m-%d %T",date_ary)     
    now=y
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken =  read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    file_id=pk
    sUrl='%s/complaint/login/default_gy?fid=payInfoDetail&seq=%s&must_reply=true'%(host_url,file_id)
    description = """关于“%s”有付款信息，请查阅。"""%(pjname)
    surl = my_urlencode(sUrl)
    # print toUser
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

    sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "url":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#173177"
            },
            "keyword1": {
            "value":%s,
            "color":"#173177"
            },
            "keyword2": {
            "value":%s,
            "color":"#173177"
            }

            }
            }
    """%(toUser,template_id_msg_gy,sUrl,description,city,now)
    # print sMsg
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return errcode