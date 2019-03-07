# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,m_sCorpID,m_sCorpSecret,m_sAgentId_gy,m_sCorpSecret_gy'%prj_name)
exec ('from %s.share        import checkSession,data_url,host_url,my_urlencode,read_access_token_common,write_access_token_common'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
from HW_DT_TOOL                 import getToday
import MySQLdb
testid = 1087
attach_url = 'http://lw.szby.cn/attach/'

def feedbackResult(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    id = request.POST.get('id','')
    sql = """select su.id,su.cname from users_gy u
             left join addr_book ab on u.addr_id = ab.id
             left join suppliers su on ab.sup_id = su.id
             where u.usr_id = '%s'"""%(usr_id_gy)
    print sql
    rows,iN=db.select(sql)
    sup_id = rows[0][0]
    sup_name = rows[0][1]
    sql = """select title,fb_money,Find_in_set(%s,fb_pass),Find_in_set(%s,fb_reject),fb_time,'%s' from complaint_sup_msg_send 
             where id = %s"""%(sup_id,sup_id,sup_name,id)
    rows,iN=db.select(sql)
    names = 'title fb_money pass reject fb_time sup_name'.split()
    data = dict(zip(names, rows[0]))
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    s = """
        {
        "errcode": 0,
        "errmsg": "获取反馈结果成功",
        "data":%s
        }        """%(L)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

#testid = 0
def getContractList(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    search =  request.POST.get('search','')
    search = MySQLdb.escape_string(search)

    sql="""SELECT OP.id,OP.gc_no,OP.cname,MT.txt1 
        FROM out_proj OP 
        LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
        LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
        WHERE FIND_IN_SET(OP.id,(
            select group_concat(prj_id) from (select prj_id,sup_id from prj_mat_buy_ht
            union 
            select prj_id,sup_id from prj_mat_buy) HT
        LEFT JOIN addr_book AB ON AB.sup_id = HT.sup_id
        LEFT JOIN users_gy U ON U.addr_id = AB.id
        WHERE U.usr_id = %s)) 
        """%(usr_id_gy)
    if search !='':
        sql+="AND ( IFNULL(OP.cname,'') LIKE '%%%s%%' OR IFNULL(OP.gc_no,'') LIKE '%%%s%%' ) "%(search,search)
    sql+="ORDER BY OP.ctime DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id req_no cname ctype_name'.split()
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

def getMatBuyList(request):   
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    search =  request.POST.get('search','')
    search = MySQLdb.escape_string(search)

    sql="""SELECT OP.id,OP.gc_no,OP.cname,MT.txt1 
        FROM out_proj OP 
        LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
        LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
        WHERE FIND_IN_SET(OP.id,(
            select group_concat(prj_id) from (select prj_id,sup_id from prj_mat_buy_ht
            union 
            select prj_id,sup_id from prj_mat_buy) HT
        LEFT JOIN addr_book AB ON AB.sup_id = HT.sup_id
        LEFT JOIN users_gy U ON U.addr_id = AB.id
        WHERE U.usr_id = %s)) 
        """%(usr_id_gy)
    if search !='':
        sql+="AND ( IFNULL(OP.cname,'') LIKE '%%%s%%' OR IFNULL(OP.gc_no,'') LIKE '%%%s%%' ) "%(search,search)
    sql+="ORDER BY OP.ctime DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id req_no cname ctype_name'.split()
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

def incorruptDetail(request):  
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    dept = 0
    pk = request.POST.get('pk','')
    # pk = 79731
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT OP.id,IFNULL(OP.gc_no,''),OP.cname,DP.cname,IFNULL(DP.id,0),IFNULL(MT.txt1,''),OP.id
               FROM out_proj OP 
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               WHERE OP.id=%s
            """%(pk)
    # print sql
    rows,iN=db.select(sql)
    if iN>0:
        dept = rows[0][4]
    names = 'id req_no cname dept_name dept_id prj_property prj_id'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""SELECT IFNULL(U.usr_id,0),U.usr_name,U.dept_id,r.role_name,1
           FROM users U 
           LEFT JOIN usr_role ur on U.usr_id = ur.usr_id
           LEFT JOIN roles r on ur.role_id = r.role_id
           where ur.role_id = 514 or ur.role_id = 582
        """
    # print sql
    rows,iN=db.select(sql)
    leader=[]
    for e in rows:
        if e[0] !=0:
            leader.append(list(e))
    # leader = json.dumps(leader,ensure_ascii=False)
    names = 'usr_id usr_name dept_id dept_name level'.split()
    data = [dict(zip(names, d)) for d in leader]
    leader = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    random_no = "%s_%s"%(time.time(),usr_id_gy)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映详情成功",
        "data":%s,
        "leader":%s,
        "random_no":"%s"
        }        """%(L,leader,random_no)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def putIncorruptComplaint(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s) 
    print request.POST
    pk = request.POST.get('pk','')
    complaintObject = request.POST.get('complaintObject','')
    leader = request.POST.get('leader','')  
    memo = request.POST.get('memo','') 
    dept_id = request.POST.get('dept_id','') 
    random_no = request.POST.get('random_no','')
    prj_id = request.POST.get('prj_id','') or 0
    level =  request.POST.get('level','') or 0
    now = int(time.time())
    anonymous =  request.POST.get('anonymous','') or 0

    complaintObject = MySQLdb.escape_string(complaintObject)
    memo = MySQLdb.escape_string(memo)

    if prj_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "未传项目参数"
        }        """
        return HttpResponseJsonCORS(s) 
    sql="""INSERT INTO complaint_sup_detail_incorrupt(cid,ctime,complaintObject,memo,leader,dept_id,random_no,level,prj_id,anonymous) 
               VALUES(%s,'%s','%s','%s',%s,%s,'%s',%s,%s,%s) 
            """%(usr_id_gy,now,complaintObject,memo,leader,dept_id,random_no,level,prj_id,anonymous)
    # print sql
    db.executesql(sql)
    sql="""SELECT id FROM complaint_sup_detail_incorrupt WHERE random_no='%s'"""%random_no
    rows,iN=db.select(sql)
    pk=rows[0][0]
    sql="""INSERT INTO complaint_sup_view_right_incorrupt(m_id,usr_id,utype) VALUES(%s,%s,'fw'),(%s,%s,'qy');
        """%(pk,usr_id_gy,pk,leader)
    # print sql
    db.executesql(sql)

    mWxPushMsg_NewComplaint_incorrupt(request,pk)  #往企业号推送消息

    s = """
        {
        "errcode": 0,
        "errmsg": "上报供应商廉政投诉成功"
        }        """
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def myIncorruptComplaint(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    situation = request.POST.get('situation','')
    search = request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    sql="""SELECT CD.id
           ,IFNULL(OP.gc_no,'')
           ,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d')
           ,IFNULL(OP.cname,'')
           ,CD.memo,CD.status,IFNULL(VR.hasNew,0)
           ,CASE WHEN IFNULL(CD.finish,0)=1 THEN '已结案' ELSE IFNULL(F.cname,'新情况') END,UX.usr_name 
           FROM complaint_sup_detail_incorrupt CD 
           LEFT JOIN out_proj OP ON OP.id = CD.prj_id
           LEFT JOIN flow F ON F.ftype='ts' AND F.flow_id=CD.status
           LEFT JOIN complaint_sup_view_right_incorrupt VR ON VR.m_id=CD.id AND VR.utype='fw' AND VR.usr_id=%s
           LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
           WHERE (CD.cid=%s)  
        """%(usr_id_gy,usr_id_gy)
    if situation !='':
        sql+="AND (CD.status='%s' "%(situation)
        if situation !='9':
            sql+="AND IFNULL(CD.finish,0) !=1 "
        else:
            sql+="OR IFNULL(CD.finish,0) =1 "
        sql+=")"
    if search !='':
        sql+="AND ( IFNULL(OP.cname,'') LIKE '%%%s%%' OR IFNULL(OP.gc_no,'') LIKE '%%%s%%' ) "%(search,search)
    sql+="ORDER BY CD.id DESC"
    print sql
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id req_no ctime cname memo status hasNew situation usr_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取我的投诉列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def myIncorruptComplaintDetail(request):  
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 1
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql = "update complaint_sup_view_right_incorrupt set hasNew = 0 where m_id=%s AND utype='fw' AND usr_id=%s"%(pk,usr_id_gy)
    db.executesql(sql)

    sql="""SELECT CD.id,IFNULL(OP.gc_no,''),IFNULL(OP.cname,''),DP.cname
           ,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d'),CD.complaintObject,'监事会',CD.memo
           ,IFNULL(CD.random_no,''),IFNULL(CD.finish,0),CD.cid
           ,ifnull(CD.pj_memo,'')
           ,case CD.anonymous when 0 then ab.name else '' end
           ,case CD.anonymous when 0 then ab.mobile else '' end
           ,case CD.anonymous when 0 then su.cname else '' end
           ,CD.anonymous
           FROM complaint_sup_detail_incorrupt CD 
           LEFT JOIN out_proj OP ON OP.id = CD.prj_id
           LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
           LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
           LEFT JOIN users U ON U.usr_id = CD.leader
           LEFT JOIN users_gy gy ON CD.cid = gy.usr_id
           LEFT JOIN addr_book ab ON gy.addr_id = ab.id
           LEFT JOIN suppliers su ON su.id = ab.sup_id
           WHERE CD.id=%s
        """%(pk)
    rows,iN=db.select(sql)
    random_no=rows[0][8]
    L = []
    for e in rows:
        L1 = list(e)
        if e[9] == 1 and str(usr_id_gy) == str(e[10]) and e[11] == '':
            L1[10] = 1
        else:
            L1[10] = 0
        L.append(L1)
    names = 'id req_no proj_name dept_name ctime complaintObject usr_name memo random_no finish pj_btn pj_memo cusrname mobile sup_name anonymous'.split()
    data = [dict(zip(names, d)) for d in L]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    sql ="""SELECT FP.id,FP.ctime,ifnull(FP.title,''),FP.fname,FP.file_size,FP.is_pic,'','','',YEAR(ctime),MONTH(ctime)
            FROM file_pic_gy FP
            WHERE FP.random_no='%s'
        """%(random_no)
    # print sql
    rows,iN = db.select(sql)
    file_list=[]
    for e in rows:
        e=list(e)
        e[6] = "%s/%s/%s/%s"%(attach_url,e[9],e[10],e[3])
        e[7] = "%s/%s/%s/thumbnail/%s"%(attach_url,e[9],e[10],e[3])
        e[8] = "%s/fileUpload/del_attach_file?fname=%s&func=Progress"%(data_url,e[3])
        file_list.append(e)
        # print e[6]
    names = 'id ctime title fname file_size is_pic url thumbnail_url delete_url'.split()
    data = [dict(zip(names, d)) for d in file_list]
    LL = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT CF.id,'监事会',CF.ctime,F.cname,case CF.is_open when 1 then CF.memo else '' end
            FROM complaint_sup_flow_incorrupt CF  
            LEFT JOIN users U ON U.usr_id = CF.cid
            LEFT JOIN flow F ON F.flow_id = CF.cur_flow_id AND F.ftype='ts'
            WHERE CF.m_id=%s and CF.cur_flow_id = 9 
            ORDER BY CF.id DESC
        """%(pk) 
    rows,iN = db.select(sql)
    names = 'id usr_name ctime cname memo'.split()
    data = [dict(zip(names, d)) for d in rows]
    flow = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT MS.id,'监事会',MS.ctime,MS.memo,D1.id,D2.id
            FROM complaint_sup_message_incorrupt MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
            Left JOIN dept D1 on D1.header = U.usr_id
            Left JOIN dept D2 on D2.sub_director = U.usr_id
            WHERE MS.m_id=%s AND MS.canview =1
            ORDER BY MS.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    names = 'id usr_name ctime memo'.split()
    data = [dict(zip(names, d)) for d in rows]
    message = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映详情成功",
        "data":%s,
        "files":%s,
        "flow":%s,
        "message":%s
        }        """%(L,LL,flow,message)
    return HttpResponseJsonCORS(s)

def complaintDetail(request):  
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    dept = 0
    pk = request.POST.get('pk','')
    # pk = 79731
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT OP.id,IFNULL(OP.gc_no,''),OP.cname,DP.cname,IFNULL(DP.id,0),IFNULL(MT.txt1,''),OP.id 
               FROM out_proj OP
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               WHERE OP.id=%s
            """%(pk)
    # print sql
    rows,iN=db.select(sql)
    if iN>0:
        dept = rows[0][4]
    names = 'id req_no cname dept_name dept_id prj_property prj_id'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'第一负责人'),1
           FROM dept DP
           LEFT JOIN users U ON DP.header = U.usr_id
           WHERE DP.id = %s
           UNION ALL
           SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'材料采购部第一负责人'),1
           FROM dept DP
           LEFT JOIN users U ON DP.header = U.usr_id
           WHERE DP.id = 40
           UNION ALL
           SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'分管领导'),2
           FROM dept DP
           LEFT JOIN users U ON DP.sub_director = U.usr_id
           WHERE DP.id = %s
           UNION ALL
           SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'领导'),3
           FROM dept DP
           LEFT JOIN users U ON DP.header = U.usr_id
           WHERE DP.id = 37
        """%(dept,dept)
    # print sql
    rows,iN=db.select(sql)
    leader=[]
    for e in rows:
        if e[0] !=0:
            leader.append(list(e))
    # leader = json.dumps(leader,ensure_ascii=False)
    names = 'usr_id usr_name dept_id dept_name level'.split()
    data = [dict(zip(names, d)) for d in leader]
    leader = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    random_no = "%s_%s"%(time.time(),usr_id_gy)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映详情成功",
        "data":%s,
        "leader":%s,
        "random_no":"%s"
        }        """%(L,leader,random_no)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def putComplaint(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s) 
    pk = request.POST.get('pk','')
    complaintObject = request.POST.get('complaintObject','')
    leader = request.POST.get('leader','')  
    memo = request.POST.get('memo','') 
    dept_id = request.POST.get('dept_id','') 
    random_no = request.POST.get('random_no','')
    prj_id = request.POST.get('prj_id','') or 0
    level =  request.POST.get('level','') or 0
    now = int(time.time())

    complaintObject = MySQLdb.escape_string(complaintObject)
    memo = MySQLdb.escape_string(memo)
    #测试数据
    # pk=10866
    # complaintObject='投诉对象'
    # leader=2029 #韩工ID
    # memo='投诉内容'
    # dept_id=182
    # random_no='123456'
    # prj_id=16631
    if prj_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "未传项目参数"
        }        """
        return HttpResponseJsonCORS(s) 
    sql="""INSERT INTO complaint_sup_detail(cid,ctime,complaintObject,memo,leader,dept_id,random_no,level,prj_id) 
               VALUES(%s,'%s','%s','%s',%s,%s,'%s',%s,%s) 
            """%(usr_id_gy,now,complaintObject,memo,leader,dept_id,random_no,level,prj_id)
    # print sql
    db.executesql(sql)
    sql="""SELECT id FROM complaint_sup_detail WHERE random_no='%s'"""%random_no
    rows,iN=db.select(sql)
    pk=rows[0][0]
    sql="""INSERT INTO complaint_sup_view_right(m_id,usr_id,utype) VALUES(%s,%s,'fw'),(%s,%s,'qy');
        """%(pk,usr_id_gy,pk,leader)
    # print sql
    db.executesql(sql)

    mWxPushMsg_NewComplaint(request,pk)  #往企业号推送消息

    s = """
        {
        "errcode": 0,
        "errmsg": "上报供应商反映成功"
        }        """
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def myComplaint(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    situation = request.POST.get('situation','')
    search = request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    sql="""SELECT CD.id
           ,IFNULL(OP.gc_no,'')
           ,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d')
           ,IFNULL(OP.cname,'')
           ,CD.memo,CD.status,IFNULL(VR.hasNew,0)
           ,CASE WHEN IFNULL(CD.finish,0)=1 THEN '已结案' ELSE IFNULL(F.cname,'新情况') END,UX.usr_name 
           FROM complaint_sup_detail CD 
           LEFT JOIN out_proj OP ON OP.id = CD.prj_id
           LEFT JOIN flow F ON F.ftype='ts' AND F.flow_id=CD.status
           LEFT JOIN complaint_sup_view_right VR ON VR.m_id=CD.id AND VR.utype='fw' AND VR.usr_id=%s
           LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
           WHERE (CD.cid=%s)  
        """%(usr_id_gy,usr_id_gy)
    if situation !='':
        sql+="AND (CD.status='%s' "%(situation)
        if situation !='9':
            sql+="AND IFNULL(CD.finish,0) !=1 "
        else:
            sql+="OR IFNULL(CD.finish,0) =1 "
        sql+=")"
    if search !='':
        sql+="AND ( IFNULL(OP.cname,'') LIKE '%%%s%%' OR IFNULL(OP.gc_no,'') LIKE '%%%s%%' ) "%(search,search)
    sql+="ORDER BY CD.id DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id req_no ctime cname memo status hasNew situation usr_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取我的投诉列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def myComplaintDetail(request):  
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 1
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql = "update complaint_sup_view_right set hasNew = 0 where m_id=%s AND utype='fw' AND usr_id=%s"%(pk,usr_id_gy)
    db.executesql(sql)

    sql="""SELECT CD.id,IFNULL(OP.gc_no,''),IFNULL(OP.cname,''),DP.cname
           ,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d'),CD.complaintObject
           ,case D1.id when 40 then '材料采购部第一负责人' when 37 then '工程管理中心领导' else concat(ifnull(D2.cname,D1.cname),'第一负责人') end
           ,CD.memo
           ,IFNULL(CD.random_no,''),IFNULL(CD.finish,0),CD.cid,ifnull(CD.pj_memo,'')
           FROM complaint_sup_detail CD 
           LEFT JOIN out_proj OP ON OP.id = CD.prj_id
           LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
           LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
           LEFT JOIN users U ON U.usr_id = CD.leader
           Left JOIN dept D1 on D1.header = U.usr_id
           Left JOIN dept D2 on D2.sub_director = U.usr_id
           WHERE CD.id=%s
        """%(pk)
    rows,iN=db.select(sql)
    random_no=rows[0][8]
    L = []
    for e in rows:
        L1 = list(e)
        if e[9] == 1 and str(usr_id_gy) == str(e[10]) and e[11] == '':
            L1[10] = 1
        else:
            L1[10] = 0
        L.append(L1)
    names = 'id req_no proj_name dept_name ctime complaintObject usr_name memo random_no finish pj_btn pj_memo'.split()
    data = [dict(zip(names, d)) for d in L]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    sql ="""SELECT FP.id,FP.ctime,ifnull(FP.title,''),FP.fname,FP.file_size,FP.is_pic,'','','',YEAR(ctime),MONTH(ctime)
            FROM file_pic_gy FP
            WHERE FP.random_no='%s'
        """%(random_no)
    # print sql
    rows,iN = db.select(sql)
    file_list=[]
    for e in rows:
        e=list(e)
        e[6] = "%s/%s/%s/%s"%(attach_url,e[9],e[10],e[3])
        e[7] = "%s/%s/%s/thumbnail/%s"%(attach_url,e[9],e[10],e[3])
        e[8] = "%s/fileUpload/del_attach_file?fname=%s&func=Progress"%(data_url,e[3])
        file_list.append(e)
        # print e[6]
    names = 'id ctime title fname file_size is_pic url thumbnail_url delete_url'.split()
    data = [dict(zip(names, d)) for d in file_list]
    LL = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT CF.id
            ,case CF.cur_flow_id when 1 then '处理人' when 2 then '处理人' else case D1.id when 40 then '材料采购部第一负责人' when 37 then '工程管理中心领导' else concat(ifnull(D2.cname,D1.cname),'第一负责人') end end
            ,CF.ctime,F.cname,case CF.is_open when 1 then CF.memo else '' end
            FROM complaint_sup_flow CF  
            LEFT JOIN users U ON U.usr_id = CF.cid
            LEFT JOIN flow F ON F.flow_id = CF.cur_flow_id AND F.ftype='ts'
            Left JOIN dept D1 on D1.header = U.usr_id
            Left JOIN dept D2 on D2.sub_director = U.usr_id
            WHERE CF.m_id=%s
            ORDER BY CF.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    names = 'id usr_name ctime cname memo'.split()
    data = [dict(zip(names, d)) for d in rows]
    flow = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT MS.id,case D1.id when 40 then '材料采购部第一负责人' when 37 then '工程管理中心领导' else concat(ifnull(D2.cname,D1.cname),'第一负责人') end
            ,MS.ctime,MS.memo,D1.id,D2.id
            FROM complaint_sup_message MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
            Left JOIN dept D1 on D1.header = U.usr_id
            Left JOIN dept D2 on D2.sub_director = U.usr_id
            WHERE MS.m_id=%s AND MS.canview =1
            ORDER BY MS.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    names = 'id usr_name ctime memo'.split()
    data = [dict(zip(names, d)) for d in rows]
    message = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映详情成功",
        "data":%s,
        "files":%s,
        "flow":%s,
        "message":%s
        }        """%(L,LL,flow,message)
    return HttpResponseJsonCORS(s)

def closeFile(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 1
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    result = request.POST.get('id','')
    # print request.POST
    sql="""SELECT cid FROM complaint_sup_detail WHERE id=%s
    """%pk
    rows,iN=db.select(sql)
    cid = rows[0][0]
    if cid !=usr_id_gy:
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    else:
        sql="""UPDATE complaint_sup_detail SET finish=1,result=%s WHERE id=%s"""%(result,pk)
        db.executesql(sql)
        #mWxPushMsg_Result(request,pk)
        s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
        return HttpResponseJsonCORS(s)

def putEvaluation(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s) 
    pk = request.POST.get('pk','')
    memo = request.POST.get('pj_memo','') 

    memo = MySQLdb.escape_string(memo)
    sql="""update complaint_sup_detail set pj_memo='%s',pj_date=now()
               where id = %s
            """%(memo,pk)

    db.executesql(sql)

    mWxPushMsg_PJ(request,pk)  #往企业号推送消息

    s = """
        {
        "errcode": 0,
        "errmsg": "评价成功"
        }        """
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

import httplib
def mWxPushMsg_NewComplaint(request,pk):   
    year=getToday()[:4]  
    L =Get_data_NewComplaint(request,pk)
    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    file_id=L[0]
    # title = ToUnicode(L[1])
    
    cusrname = L[1]  #投诉人
    complaintObject = L[2] #投诉对象
    proj_name = L[3]
    toUser = L[4]
    if toUser=='gup':
        toUser+='|mengxp|zhongzhg|hanruiming'
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,file_id)
    stitle = """新反映提醒"""
    description = """【%s】发起了针对“%s”关于“%s”的情况反映，请及时查阅。"""%(cusrname,complaintObject,proj_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    surl = my_urlencode(sUrl)
    sUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
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

    """%(m_sAgentId_gy,stitle,sUrl,description)
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

def Get_data_NewComplaint(request,pk):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,CD.complaintObject,OP.cname,U.login_id
            FROM complaint_sup_detail CD 
            LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
            LEFT JOIN out_proj OP ON OP.id = CD.prj_id
            LEFT JOIN users U ON U.usr_id = CD.leader
            WHERE CD.id = %s
            """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_NewComplaint_incorrupt(request,pk):   
    year=getToday()[:4]  
    L =Get_data_NewComplaint_incorrupt(request,pk)
    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    file_id=L[0]
    # title = ToUnicode(L[1])
    
    cusrname = L[1]  #投诉人
    complaintObject = L[2] #投诉对象
    proj_name = L[3]
    toUser = L[4]
    toUser +='|liusq|lishijie'
    sUrl='%s/complaint/login/login_qy?fid=accuseDetail&path=policy_accuse&func_id=1000004&seq=%s'%(host_url,file_id)
    surl = my_urlencode(sUrl)
    sUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
    stitle = """廉政投诉"""
    description = """有供应商发起了廉政投诉，请您注意查看处理。\r\n投诉时间：%s"""%(L[5])
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
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

    """%(m_sAgentId_gy,stitle,sUrl,description)
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

def Get_data_NewComplaint_incorrupt(request,pk):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,CD.complaintObject,OP.cname,U.login_id,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d %%T')
            FROM complaint_sup_detail_incorrupt CD 
            LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
            LEFT JOIN out_proj OP ON OP.id = CD.prj_id
            LEFT JOIN users U ON U.usr_id = CD.leader
            WHERE CD.id = %s
            """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_Result(request,pk):   
    year=getToday()[:4]  
    L,toUser =Get_data_Result(request,pk)
    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    file_id=L[0]
    # title = ToUnicode(L[1])
    
    cusrname = L[1]  #投诉人
    complaintObject = L[2] #投诉对象
    proj_name = L[3]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,file_id)
    stitle = """新反映结案提醒"""
    surl = my_urlencode(sUrl)
    description = """针对“%s”关于“%s”的供应商反映已结案。"""%(complaintObject,proj_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    sUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
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

    """%(m_sAgentId_gy,stitle,sUrl,description)
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

def Get_data_Result(request,pk):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,CD.complaintObject,IFNULL(OP.cname,OP1.cname),U.login_id
        FROM complaint_sup_detail CD 
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN prj_mat_buy_ht HT ON HT.id = CD.ht_id
        LEFT JOIN out_proj OP ON OP.id = HT.prj_id
        LEFT JOIN users U ON U.usr_id = CD.leader
        LEFT JOIN prj_mat_buy PMB ON PMB.id = CD.mb_id
        LEFT JOIN out_proj OP1 ON OP1.id = PMB.prj_id
        WHERE CD.id = %s
        """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]

    toUser=''
    sql="""SELECT IFNULL(U.login_id,'') FROM complaint_sup_view_right VR 
        LEFT JOIN users U ON U.usr_id=VR.usr_id
        WHERE VR.m_id = %s and VR.utype='qy'
        """%(pk)
    rows,iN = db.select(sql)
    for e in rows:
        toUser+='%s|'%(e[0])
    return L,toUser  

def mWxPushMsg_PJ(request,pk):   
    year=getToday()[:4]  
    L,toUser =Get_data_PJ(request,pk)
    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    file_id=L[0]
    # title = ToUnicode(L[1])
    toUser = '|lishijie'
    cusrname = L[1]  #投诉人
    sup_name = L[2] #投诉对象
    proj_name = L[3]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&func_id=1000004&seq=%s'%(host_url,file_id)
    stitle = """服务评价"""
    surl = my_urlencode(sUrl)
    description = """供应商对“%s”的情况反映处理结果做出了服务评价，请及时查看。\r\n供应商名称:%s"""%(proj_name,sup_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    sUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
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

    """%(m_sAgentId_gy,stitle,sUrl,description)
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

def Get_data_PJ(request,pk):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,su.cname,IFNULL(OP.cname,OP1.cname),U.login_id
        FROM complaint_sup_detail CD 
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN prj_mat_buy_ht HT ON HT.id = CD.ht_id
        LEFT JOIN out_proj OP ON OP.id = HT.prj_id
        LEFT JOIN users U ON U.usr_id = CD.leader
        LEFT JOIN prj_mat_buy PMB ON PMB.id = CD.mb_id
        LEFT JOIN out_proj OP1 ON OP1.id = PMB.prj_id
        LEFT JOIN addr_book ab on ab.id = UX.addr_id
        Left Join suppliers su on su.id = ab.sup_id
        WHERE CD.id = %s
        """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]

    toUser=''
    sql="""select u.login_id from complaint_sup_flow f 
        left join users u on u.usr_id = f.cid
        where f.next_flow_id = 10 and f.m_id = %s
        union 
        select u.login_id from usr_role r 
        left join users u on r.usr_id = u.usr_id
        where r.role_id = 514
        """%(pk)
    rows,iN = db.select(sql)
    for e in rows:
        toUser+='%s|'%(e[0])
    return L,toUser  