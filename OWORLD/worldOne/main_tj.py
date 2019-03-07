# -*- coding: utf-8 -*-
# 项目推荐人
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,m_sCorpID,m_sCorpSecret,m_sAgentId_tj,m_sCorpSecret_tj'%prj_name)
exec ('from %s.share        import read_access_token_common,write_access_token_common,checkSession,data_url,host_url,my_urlencode,imgUrl'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
import MySQLdb
from django.http import HttpResponseRedirect,HttpResponse
from HW_DT_TOOL                 import getToday
sys.path.append("/home/webroot/oWorld/complaint/data")
from HW_DB   import DataBaseParent_byerp
byerp=DataBaseParent_byerp() 

testid = 0
def getProjList(request):	
    usr_id_tj = request.session.get('usr_id_tj','') or testid
    if usr_id_tj ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    search =  request.POST.get('search','')
    typeId =  request.POST.get('typeId','') or 0
    search = MySQLdb.escape_string(search)
    sql ="""SELECT 
            OP.id
            ,OP.cname
            ,P.cname
            ,C.cname
            ,DATE_FORMAT(OP.bbtime,'%%Y-%%m-%%d')
            ,datediff(now(),ifnull(pt.ctime,op.bbtime)) as days
            ,F.flow_id
            ,F.cname
            FROM out_proj OP
            LEFT JOIN province P on P.code=OP.province
            LEFT JOIN city C on C.code=OP.city
            LEFT JOIN addr_book AB ON AB.id = OP.p_id 
            LEFT JOIN users_tj UT ON UT.addr_id=AB.id
            LEFT JOIN (select pid,max(ctime) as ctime from out_proj_tracking group by pid) pt on pt.pid = OP.id
            LEFT JOIN flow F ON 
            F.flow_id = IFNULL((select IFNULL(status,0) from out_proj_tracking where pid=OP.id ORDER BY ctime desc limit 1),0)  AND F.ftype='track'
            WHERE UT.usr_id = %s
        """%(usr_id_tj)
    if str(typeId) in('0','1'):
        sql+="AND F.flow_id=%s "%typeId
    if str(typeId) =='2':
        sql+="AND F.flow_id in (2,3) "
    if search !='':
        sql+="AND ( IFNULL(OP.cname,'') LIKE '%%%s%%' ) "%(search)
    sql+="ORDER BY OP.ctime DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id cname province city bbtime days typeId typeName'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取项目列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def getProjTrack(request):
    usr_id_tj = request.session.get('usr_id_tj','') or testid
    if usr_id_tj ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 16631
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)

    sql ="""SELECT 
            OP.id
            ,OP.cname
            ,P.cname
            ,C.cname
            ,DATE_FORMAT(OP.bbtime,'%%Y-%%m-%%d')
            ,datediff(now(),ifnull(pt.ctime,op.bbtime)) as days
            FROM out_proj OP
            LEFT JOIN province P on P.code=OP.province
            LEFT JOIN city C on C.code=OP.city
            LEFT JOIN addr_book AB ON AB.id = OP.p_id 
            LEFT JOIN users_tj UT ON UT.addr_id=AB.id
            LEFT JOIN (select pid,max(ctime) as ctime from out_proj_tracking group by pid) pt on pt.pid = OP.id
            WHERE OP.id = %s
        """%(pk)
    rows,iN=db.select(sql)
    names = 'id cname province city bbtime days'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""SELECT   
            CASE IFNULL(FR.istj,0) WHEN 1 THEN UT.headimgurl ELSE CONCAT('%s',U.pic) END
            ,CASE IFNULL(FR.istj,0) WHEN 1 THEN UT.usr_name ELSE U.usr_name END
            ,DATE_FORMAT(FR.ctime,'%%Y-%%m-%%d %%H:%%i:%%s')
            ,DATE_FORMAT(FR.stime,'%%Y-%%m-%%d %%H:%%i:%%s')
            ,FR.memo
            ,FR.next
            ,IFNULL(F.cname,'')
            FROM out_proj_tracking FR
            LEFT JOIN users_tj UT ON UT.usr_id = FR.cid
            LEFT JOIN users U ON U.usr_id = FR.cid 
            LEFT JOIN flow F ON F.flow_id = FR.status AND F.ftype='track'
            WHERE FR.pid=%s
            ORDER BY FR.ctime DESC
        """%(imgUrl,pk)
    rows,iN=db.select(sql)
    names = 'headimgurl usr_name ctime stime memo next status'.split()
    data = [dict(zip(names, d)) for d in rows]
    L1 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""SELECT flow_id,cname FROM flow WHERE ftype='track'"""
    rows,iN=db.select(sql)

    names = 'flow_id cname'.split()
    data = [dict(zip(names, d)) for d in rows]
    L2 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取项目追踪详情成功",
        "data":%s,
        "list":%s,
        "selectData":%s
        }        """%(L,L1,L2)
    return HttpResponseJsonCORS(s)

import httplib
import urllib
def putProjTrack(request):
    # 测试读取主系统数据库
    # sql="select count(*) from users"
    # rows,iN=byerp.select(sql)
    # return HttpResponseJsonCORS(rows[0][0])

    usr_id_tj = request.session.get('usr_id_tj','') or testid
    if usr_id_tj ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    usr_tj = 3323  #人员ID

    pk = request.POST.get('pk','')
    memo = request.POST.get('memo','')
    next_memo = request.POST.get('next_memo','')
    status = request.POST.get('status','') or 0
    statusName = request.POST.get('statusName','')   

    memo = MySQLdb.escape_string(memo)
    next_memo = MySQLdb.escape_string(next_memo)
    ###测试数据###
    # pk=16631
    # memo='当前'
    # next_memo='下一步'
    # statusName ='正在跟进'
    # status = 0

    # if statusName!='':
    #     memo+='%s</br>%s'%(memo,statusName)
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    # memo='测试测试'
    # memo+='</br>状态'
    # return HttpResponseCORS(request,memo)
    
    
    #写入主系统
    # sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime) 
    #     output inserted.seq
    #     VALUES (%s,getdate(),'%s','%s',%s,getdate()) """%(pk,memo,next_memo,usr_tj)
    # # print sql
    # # sql = ToGBK(sql)
    # r,iN = byerp.select(sql)
    # seq = r[0][0]   #获取刚刚写入的seq
    # errcode='0'
    # sToken='Ljdiu74F_A5Sf75ws5d1fE_DFs8d'
    # memo_gbk=ToGBK(memo)
    # next_memo_gbk=ToGBK(next_memo)
    # params = urllib.urlencode({'usr_tj': usr_tj,'memo':memo_gbk,'sToken':sToken,'next_memo':next_memo_gbk,'status':status,'pid':pk,'itype':'tracking'})  
    # headers = {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"}  
    # conn = httplib.HTTPConnection('pr.szby.cn')  
    # url = "/byerp/communication"
    # conn.request('POST', '%s'%url,params,headers)  
    # res = conn.getresponse()       
    # body = res.read()  
    # conn.close()  
    # ddata=json.loads(body)
    # errcode = ddata['errcode']  
    # seq = ddata['last_id']   
    # # print errcode
    # if str(errcode)=='0':
    #     sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime,seq,datasource,status,istj,is_wx) 
    #         VALUES (%s,now(),'%s','%s',%s,now(),%s,1,%s,1,1) """%(pk,memo,next_memo,usr_id_tj,seq,status)
    #     db.executesql(sql)
    #     mWxPushMsg_NewTracking(request,seq,pk)
    #     s = """
    #         {
    #         "errcode": 0,
    #         "errmsg": "提交成功"
    #         }        """
    #     return HttpResponseJsonCORS(s)
    # else:
    #     s = """
    #         {
    #         "errcode": -1,
    #         "errmsg": "提交失败"
    #         }        """
    #     return HttpResponseJsonCORS(s)
   
    sql="SELECT IFNULL(MAX(seq),0) FROM out_proj_tracking WHERE datasource=2"
    rows,iN=db.select(sql)
    seq = rows[0][0]
    if seq==0:seq=200000000
    seq+=1
    sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime,seq,datasource,status,istj,is_wx) 
        VALUES (%s,now(),'%s','%s',%s,now(),%s,2,%s,1,1) """%(pk,memo,next_memo,usr_id_tj,seq,status)
    db.executesql(sql)
    mWxPushMsg_NewTracking(request,seq,pk)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
    return HttpResponseJsonCORS(s)


def mWxPushMsg_NewTracking(request,seq,pk):   
    year=getToday()[:4]  
    L =Get_data_NewTracking(request,pk)
    sToken =  read_access_token_common('access_token_tj_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_tj)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_tj_qy')
    
    cusrname = L[1]  #投诉人
    proj_name = L[0]
    toUser = L[1]+'|'+L[2]
    sUrl='%s/complaint/login/login_qy?fid=projDetail&seq=%s&must_reply=true&func_id=1000003'%(host_url,pk)
    stitle = """新项目跟进提醒"""
    surl = my_urlencode(sUrl)
    description = """您在深圳宝鹰建设集团报备的:%s 已进行跟进，请点击查阅"""%(proj_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_tj,stitle,url,description)
    # print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return HttpResponseCORS(request,errcode)

def Get_data_NewTracking(resquest,pk):
    L=[]
    sql="""SELECT 
        OP.cname
        ,IFNULL(U.login_id,'')
        ,IFNULL(UB.login_id,'')
        ,IFNULL(UL.login_id,'') 
        FROM out_proj OP 
        LEFT JOIN users U ON U.usr_id = OP.mana_id
        LEFT JOIN users UB ON UB.usr_id = OP.busi_usr_id
        LEFT JOIN users UL ON UL.usr_id = OP.led_id
        WHERE OP.id=%s
    """%pk
    rows,iN = db.select(sql)
    L=rows[0]
    return L