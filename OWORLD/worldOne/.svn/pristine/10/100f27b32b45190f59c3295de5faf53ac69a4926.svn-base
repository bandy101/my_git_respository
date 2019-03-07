# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,checkSession,byerp'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
import MySQLdb
import httplib
import urllib
"""
短信产品-发送短信接口
Created on 2017-06-12
"""
REGION = "cn-hangzhou"# 暂时不支持多region
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAInMlNPwPEbiSF"
ACCESS_KEY_SECRET = "ueUeouYBm04FurtsbpTO1dAgmIgY0G"
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
# testid=207
testid=207
def send_sms(business_id, phone_number, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数,友情提示:如果JSON中需要带换行符,请参照标准的JSON协议对换行符的要求,比如短信内容中包含\r\n的情况在JSON中需要表示成\\r\\n,否则会导致JSON在服务端解析失败
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name);
    # 短信发送的号码，必填。支持以逗号分隔的形式进行批量调用，批量上限为1000个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
    smsRequest.set_PhoneNumbers(phone_number)
    # 发送请求
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse

def getCode(request):	
    #addr_group_id
    #1 项目经理 tj 
    #2 供应商联系人 gy 
    #7 劳务团队 lw
    usr_id = request.session.get('usr_id','') or testid
    itype = request.POST.get('itype','') or 'lw'  
    phone = request.POST.get('phone','')
    is_partner = request.POST.get('is_partner','') or 0 
    labour_proj_id = request.POST.get('labour_proj_id','')
    user_table = 'users_wx'
    addr_group_id = 7
    if itype=='tj':
        addr_group_id = 1
        user_table = 'users_tj'
        usr_id = request.session.get('usr_id_tj','') or testid
    if itype=='gy':
        addr_group_id = 2
        user_table = 'users_gy'
        usr_id = request.session.get('usr_id_gy','') or testid
    print usr_id
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    # usr_id = 1
    # phone = '18138280106'
    random_no = random.randint(100000,999999)
    now = int(time.time())  #转为时间戳
    st = time.localtime(now)
    stime = time.strftime('%Y-%m-%d', st) #当前日期
    
    # random_no=123456
    # sql="INSERT INTO msgPushCode(usr_id,code,ctime,phone,addr_id) VALUES(%s,'%s','%s','%s',17517)"%(usr_id,random_no,now,phone)
    # db.executesql(sql)
    # s = """
    #     {
    #     "errcode": 0,
    #     "errmsg": "验证码发送成功",
    #     "code":%s
    #     }        """%random_no
    # return HttpResponseJsonCORS(s)
    ###验证码获取频率检测
    rows,iN = db.select("select ctime from msgPushCode where usr_id='%s' and itype='%s' order by id desc limit 1"%(usr_id,itype))
    if iN>0:
    	lastCtime = rows[0][0]
    	
    	if now - int(lastCtime) <=120 :
    		s = """
	        {
	        "errcode": -1,
	        "errmsg": "2分钟内不得再次获取验证码"
	        }        """
	        return HttpResponseJsonCORS(s)
        sql ="select count(*) from msgPushCode where FROM_UNIXTIME(ctime,'%%Y-%%m-%%d')='%s' and usr_id=%s and itype='%s' "%(stime,usr_id,itype)
        rows,iN=db.select(sql)
        if rows[0][0] > 10:
        	s = """
	        {
	        "errcode": -1,
	        "errmsg": "每天只能获取5次验证码"
	        }        """
	        return HttpResponseJsonCORS(s)
    ###检测是否有该手机号码

    #sql = "select name,license from addr_book limit 0,5"
    #rows,iN = db.select(sql)
    #names = 'name ID_number'.split()
    #data = [dict(zip(names, d)) for d in rows]
    #L2 = []   
    #L21 = ['','','']   
    #L21[0] = '123'
    #L21[1] = '12434'
    #L21[2] = data
    #L2.append(L21)
    #L22 = ['','','']   
    #L22[0] = '123'
    #L22[1] = '12434'
    #L22[2] = data
    #L2.append(L22)
    #names = 'leader_name leader_id users'.split()
    #data1 = [dict(zip(names, d)) for d in L2]
    #L = ['1234','']
    #L[1] = data1
    #names = 'proj_id teams'.split()
    #print dict(zip(names, L))  
    
    sql = """select ab.id,u.status from addr_book ab left join %s u on u.addr_id = ab.id 
    where ab.status=1 and ab.mobile='%s' and ab.id in (select addr_book_id from addr_book_group WHERE addr_group_id=%s)"""%(user_table,phone,addr_group_id)
    if itype=='tj':
        sql = """select ab.id,u.status from addr_book ab left join %s u on u.addr_id = ab.id 
                        where ab.status=1 and ab.mobile='%s' and IFNULL(ab.license,'')!='' """%(user_table,phone)
    elif itype=='gy':
        sql = """select ab.id,u.status from addr_book ab left join %s u on u.addr_id = ab.id 
                 where ab.status=1 and ab.mobile='%s' and ab.id in (select addr_book_id from addr_book_group WHERE addr_group_id=%s) and ab.sup_id is not null"""%(user_table,phone,addr_group_id)
    print sql
    rows,iN = db.select(sql)
    # print iN
    if iN>0:       
        for e in rows: 
            if e[1]==1:
                s = """
                {
                "errcode": -1,
                "errmsg": "该手机号码已被使用"
                }        """
                return HttpResponseJsonCORS(s)
        business_id = uuid.uuid1()
        # print business_id
        params = "{\"code\":\"%s\",\"product\":\"宝鹰\"}"%(random_no)
        data = send_sms(business_id, phone, "宝鹰集团", "SMS_90265011", params)
        d = json.loads(data)
        mark = d['Message']  #是否OK标识
        print d
        if mark=='OK':
            sql="INSERT INTO msgPushCode(usr_id,code,ctime,phone,addr_id,itype) VALUES(%s,'%s','%s','%s',%s,'%s')"%(usr_id,random_no,now,phone,rows[0][0],itype)
            db.executesql(sql)
            s = """
            {
            "errcode": 0,
            "errmsg": "验证码发送成功",
            "code":%s
            }        """%random_no
            return HttpResponseJsonCORS(s)
        else:
            s = """
            {
            "errcode": -1,
            "errmsg": "验证码发送失败"
            }        """
            return HttpResponseJsonCORS(s)
    else:
        #if itype=='lw': #此时为劳务工
        #    if str(is_partner)=='1':
        #        sql="""SELECT id FROM labour_partner WHERE phone='%s' """%(phone)
        #        r,iN=db.select(sql)
        #        if iN>0:
        #            partner_id=r[0][0]
        #            sql="""SELECT LP.id FROM labour_proj LP
        #                WHERE LP.partner_id=%s AND LP.parent_id=%s """%(partner_id,labour_proj_id)
        #            rows2,iN2=db.select(sql)
        #            if iN2>0:
        #                s = """
        #                {
        #                "errcode": -1,
        #                "errmsg": "您的伙伴已登记在该项目，不能重复"
        #                }        """
        #                return HttpResponseJsonCORS(s)
        #    else:
        #        sql="""SELECT U.usr_id as id FROM users_wx U WHERE U.phone='%s' and U.status=1 """%(phone)
        #        r,iN=db.select(sql)
        #        if iN>0:
        #            s = """
        #            {
        #            "errcode": -1,
        #            "errmsg": "手机号码已被使用，请联系管理员。"
        #            }        """
        #            return HttpResponseJsonCORS(s)
        #    business_id = uuid.uuid1()
        #    params = "{\"code\":\"%s\",\"product\":\"宝鹰\"}"%(random_no)
        #    data = send_sms(business_id, phone, "宝鹰集团", "SMS_90265011", params)
        #    d = json.loads(data)
        #    mark = d['Message']  #是否OK标识
        #    print d
        #    if mark=='OK':
        #        sql="INSERT INTO msgPushCode(usr_id,code,ctime,phone,itype,is_labor) VALUES(%s,'%s','%s','%s','%s',1)"%(usr_id,random_no,now,phone,itype)
        #        db.executesql(sql)
        #        s = """
        #        {
        #        "errcode": 0,
        #        "errmsg": "验证码发送成功",
        #        "code":%s,
        #        "is_labor":1
        #        }        """%random_no
        #        return HttpResponseJsonCORS(s)
        #    else:
        #        s = """
        #        {
        #        "errcode": -1,
        #        "errmsg": "验证码发送失败"
        #        }        """
        #        return HttpResponseJsonCORS(s)
        #else:    
        s = """
            {
            "errcode": -1,
            "errmsg": "该手机号码不存在，请联系管理员"
            }        """
        return HttpResponseJsonCORS(s)

def checkPass(request):
    usr_id = request.session.get('usr_id','') or testid
    itype = request.POST.get('itype','') or 'lw'  
    user_table = 'users_wx'
    addr_group_id = 7
    license_col = 'license'
    if itype=='tj':
        addr_group_id = 1
        user_table = 'users_tj'
        usr_id = request.session.get('usr_id_tj','') or testid
    if itype=='gy':
        #身份证号码： gysct_cardid
        license_col = 'license'
        addr_group_id = 2
        user_table = 'users_gy'
        usr_id = request.session.get('usr_id_gy','') or testid

    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    #print request.POST
    code = request.POST.get('code','')
    name = request.POST.get('name','')
    license = request.POST.get('license','')
    is_partner = request.POST.get('is_partner','') or 0
    name = MySQLdb.escape_string(name)
    sql = """select mc.code,mc.ctime,mc.addr_id,mc.phone 
             from msgPushCode mc 
             left join addr_book ab on ab.id = mc.addr_id
             where ab.status=1 and mc.code='%s' and mc.usr_id =%s and ab.name='%s' and ab.%s='%s' and mc.itype='%s'
             order by mc.id desc limit 1"""%(code,usr_id,name,license_col,license,itype)
    print ToGBK(sql)
    rows,iN = db.select(sql)
    if iN>0:
        now = int(time.time())  #转为时间戳
        if now-int(rows[0][1])>600:
            s = """
            {
            "errcode": -1,
            "errmsg": "已过期(验证码有效期为10分钟)"
            }        """
            return HttpResponseJsonCORS(s)
        if itype=='tj':
            #errcode = changeBindStatus(rows[0][2]) 
            #if str(errcode)!='0':
            #    s = """
            #    {
            #    "errcode": -1,
            #    "errmsg": "绑定失败(00)"
            #    }        """
            #    return HttpResponseJsonCORS(s)
            sql="""update addr_book set bind_status=1 where id = %s"""%(rows[0][2])
            byerp.executesql(sql)
 
        if itype=='lw':
            sql="update %s set status=1,addr_id=%s,usr_name='%s',phone='%s',bandtime=now(),is_labor=0 where usr_id=%s"%(user_table,rows[0][2],name,rows[0][3],usr_id)  
        else:
            sql="update %s set status=1,addr_id=%s,usr_name='%s',phone='%s',bandtime=now() where usr_id=%s"%(user_table,rows[0][2],name,rows[0][3],usr_id)  
        
        db.executesql(sql)
        s = """
        {
        "errcode": 0,
        "errmsg": "验证通过"
        }        """
        return HttpResponseJsonCORS(s)
    else:
        '''if itype=='lw':
            sql = """select mc.code,mc.ctime,mc.addr_id,mc.phone 
             from msgPushCode mc 
             where mc.code='%s' and mc.usr_id =%s and mc.itype='lw'
             order by mc.id desc limit 1"""%(code,usr_id)
            print sql
            rows,iN = db.select(sql)
            print iN
            if iN>0:
                now = int(time.time())  #转为时间戳
                if now-int(rows[0][1])>600:
                    s = """
                    {
                    "errcode": -1,
                    "errmsg": "已过期(验证码有效期为10分钟)"
                    }        """
                    return HttpResponseJsonCORS(s)
                if str(is_partner)!='0': #是帮小伙伴绑定
                    sql="""SELECT id FROM labour_partner WHERE phone='%s' """%(rows[0][3])
                    row1,iN1=db.select(sql)
                    if iN1<1:
                        sql="""INSERT INTO labour_partner(license,name,phone,cid,ctime) 
                            VALUES('%s','%s','%s',%s,now())"""%(license,name,rows[0][3],usr_id)
                        db.executesql(sql)
                        sql="""SELECT id FROM labour_partner WHERE license='%s' AND name='%s' AND phone='%s' """%(license,name,rows[0][3])
                        row2,iN2=db.select(sql)
                        partner_id=row2[0][0]                    
                    else:
                        partner_id=row1[0][0]
                    s = """
                    {
                    "errcode": 0,
                    "errmsg": "绑定成功",
                    "partner_id":%s
                    }        """%partner_id
                    return HttpResponseJsonCORS(s)
                else:
                    sql="""update users_wx set status=1,usr_name='%s',phone='%s',license='%s',is_labor=1,bandtime=now() where usr_id=%s"""%(name,rows[0][3],license,usr_id)
                    print sql
                    db.executesql(sql)
                    s = """
                    {
                    "errcode": 0,
                    "errmsg": "绑定成功"
                    }        """
                    return HttpResponseJsonCORS(s)
            else:
                s = """
                {
                "errcode": -1,
                "errmsg": "身份信息不符。"
                }        """
                return HttpResponseJsonCORS(s)
        else:'''
        s = """
            {
            "errcode": -1,
            "errmsg": "身份信息不符"
            }        """
        return HttpResponseJsonCORS(s)

def myInfo(request):
    usr_id = request.session.get('usr_id','') or testid
    itype = request.POST.get('itype','') or 'lw'  
    user_table = 'users_wx'
    if itype=='tj':
        user_table = 'users_tj'
        usr_id = request.session.get('usr_id_tj','') or testid
    if itype=='gy':
        user_table = 'users_gy'
        usr_id = request.session.get('usr_id_gy','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT U.usr_id,AB.license,AB.name,AB.mobile,0
        FROM %s U
        LEFT JOIN addr_book AB ON AB.id = U.addr_id
        WHERE U.usr_id = %s AND U.status=1
        """%(user_table,usr_id)
    if itype=='lw':
        sql="""SELECT 
        U.usr_id
        ,CASE IFNULL(U.is_labor,0) WHEN 0 THEN AB.license ELSE U.license END 
        ,CASE IFNULL(U.is_labor,0) WHEN 0 THEN AB.name ELSE U.usr_name END
        ,CASE IFNULL(U.is_labor,0) WHEN 0 THEN AB.mobile ELSE U.phone END
        ,IFNULL(U.is_labor,0)
        FROM users_wx U 
        LEFT JOIN addr_book AB ON AB.id = U.addr_id
        WHERE  U.status=1 AND U.usr_id=%s"""%usr_id
    elif itype=='gy':
        sql="""SELECT U.usr_id,ifnull(AB.license,''),AB.name,ifnull(AB.mobile,''),su.cname
        FROM users_gy U
        LEFT JOIN addr_book AB ON AB.id = U.addr_id
        LEFT JOIN suppliers su on su.id = AB.sup_id
        WHERE U.usr_id = %s AND U.status=1
        """%(usr_id)

    rows,iN = db.select(sql)
    
    if iN<1:
        s = """
        {
        "errcode": -1,
        "errmsg": "用户不存在或未绑定成功"
        }        """
        return HttpResponseJsonCORS(s)
    tem=[]
    for e in rows:
        e = list(e) 
        lisense = e[1].replace(e[1][6:10],'******',1)
        mobile = e[3].replace(e[3][3:7],'****',1)
        e[1] = lisense
        e[3] = mobile
        tem.append(e)
    if itype=='gy':
        names = 'usr_id license name mobile sup_name'.split()
    else:
        names = 'usr_id license name mobile'.split()
    data = [dict(zip(names, d)) for d in tem]
    info = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    L=[]
    if itype=='lw' and rows[0][4]==1:#劳务工已登记项目列表
        sql="""SELECT LP.id,OP.gc_no,OP.cname,MT.txt1 FROM labour_proj LP 
            LEFT JOIN out_proj OP ON OP.id=LP.proj_id
            LEFT JOIN mtc_t MT ON MT.id=LP.work_type AND MT.type='WTRADE'
            WHERE LP.cid=%s """%(usr_id)
        rows,iN = db.select(sql)
        for e in rows:
            e = list(e)
            L.append(e)
    names = 'labour_proj_id gc_no cname work_type_txt'.split()
    data = [dict(zip(names, d)) for d in L]
    labour_proj_list = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户信息成功",
        "info":%s,
        "labour_proj_list":%s
        }        """%(info,labour_proj_list)
    return HttpResponseJsonCORS(s)


def changeBindStatus(addr_id):
    sToken='Ljdiu74F_A5Sf75ws5d1fE_DFs8d'
    params = urllib.urlencode({'sToken':sToken,'bind_status':1,'addr_id':addr_id,'itype':'bind'})  
    headers = {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"}  
    conn = httplib.HTTPSConnection('ww.szby.cn:8088')  
    url = "/byerp/communication"
    conn.request('POST', '%s'%url,params,headers)  
    res = conn.getresponse()       
    body = res.read()  
    print body
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode']
    return errcode