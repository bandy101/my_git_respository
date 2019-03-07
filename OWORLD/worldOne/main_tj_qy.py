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

# testid = 2651
testid=0
def getProjList(request):	
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
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
            ,(select datediff(now(),ctime) from out_proj_tracking where pid=OP.id ORDER BY ctime desc limit 1) as days
            ,F.flow_id
            ,F.cname
            FROM out_proj OP
            LEFT JOIN province P on P.code=OP.province
            LEFT JOIN city C on C.code=OP.city
            LEFT JOIN addr_book AB ON AB.id = OP.p_id 
            LEFT JOIN users_tj UT ON UT.addr_id=AB.id
            LEFT JOIN flow F ON 
            F.flow_id = (select IFNULL(status,0) from out_proj_tracking where pid=OP.id ORDER BY ctime desc limit 1)  AND F.ftype='track'
            WHERE OP.busi_usr_id = %s OR OP.mana_id=%s
        """%(usr_id_qy,usr_id_qy)
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
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
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
            ,(select datediff(now(),ctime) from out_proj_tracking where pid=OP.id ORDER BY ctime desc limit 1) as days
            FROM out_proj OP
            LEFT JOIN province P on P.code=OP.province
            LEFT JOIN city C on C.code=OP.city
            LEFT JOIN addr_book AB ON AB.id = OP.p_id 
            LEFT JOIN users_tj UT ON UT.addr_id=AB.id
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
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    # print request.POST
    pk = request.POST.get('pk','')
    memo = request.POST.get('memo','')
    next_memo = request.POST.get('next_memo','')
    status = request.POST.get('status','') or 0
    statusName = request.POST.get('statusName','')  
    memo = MySQLdb.escape_string(memo)
    next_memo = MySQLdb.escape_string(next_memo) 
    # pk=16631
    # memo='当前'
    # next_memo='下一步'
    # statusName ='正在跟进'
    
    # seq=1
    # pk=16631
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
    # 测试读取主系统数据库
    # sql="select count(*) from users"
    # rows,iN=byerp.select(sql)
    # return HttpResponseJsonCORS(rows[0][0])
    
    #写入主系统
    # sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime) 
    #     output inserted.seq
    #     VALUES (%s,getdate(),'%s','%s',%s,getdate()) """%(pk,memo,next_memo,usr_id_qy)
    # # sql=ToGBK(sql)
    # r,iN = byerp.select(sql)
    # seq = r[0][0]   #获取刚刚写入的seq
    # errcode=''
    # sToken='Ljdiu74F_A5Sf75ws5d1fE_DFs8d'
    # memo_gbk=ToGBK(memo)
    # next_memo_gbk=ToGBK(next_memo)
    # params = urllib.urlencode({'usr_tj': usr_id_qy,'memo':memo_gbk,'sToken':sToken,'next_memo':next_memo_gbk,'status':status,'pid':pk,'itype':'tracking'})  
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
    #     sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime,seq,datasource,status,is_wx) 
    #         VALUES (%s,now(),'%s','%s',%s,now(),%s,1,%s,1) """%(pk,memo,next_memo,usr_id_qy,seq,status)
    #     db.executesql(sql)
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
    sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime,seq,datasource,status,is_wx) 
        VALUES (%s,now(),'%s','%s',%s,now(),%s,2,%s,1) """%(pk,memo,next_memo,usr_id_qy,seq,status)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
    return HttpResponseJsonCORS(s)