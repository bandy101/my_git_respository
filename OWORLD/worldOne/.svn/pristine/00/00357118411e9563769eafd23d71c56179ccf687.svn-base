# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,host_url,my_urlencode,read_access_token_common,write_access_token_common'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,checkSession,data_url,m_sCorpID,m_sCorpSecret,m_sAgentId_gy,m_sCorpSecret_gy,AppId_gy,AppSecret_gy,template_id_msg_gy,template_id_result_gy'%prj_name) 
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
testid = 2110
attach_url = 'http://lw.szby.cn/attach/'
def myIncorruptComplaint(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    #查出当前用户是否在审计部
    sql="""SELECT dept_id FROM users WHERE usr_id=%s
        """%(usr_id_qy)
    rows,iN=db.select(sql)
    dept_id=rows[0][0]
    if str(dept_id)=='77':
        viewRight = 0
    else:
        viewRight = 1
    sql="""SELECT CD.id,IFNULL(OP.gc_no,''),FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d'),IFNULL(OP.cname,''),CD.memo,CD.status,IFNULL(VR.hasNew,0)
           ,CASE WHEN IFNULL(CD.finish,0)=1 THEN '已结案' ELSE IFNULL(F.cname,'新情况') END,su.cname
           FROM complaint_sup_detail_incorrupt CD 
           LEFT JOIN complaint_sup_view_right_incorrupt VR ON VR.m_id=CD.id AND VR.utype='qy' AND VR.usr_id=%s
           LEFT JOIN out_proj OP ON OP.id = CD.prj_id
           LEFT JOIN flow F ON F.ftype='ts' AND F.flow_id=CD.status
           LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
           LEFT JOIN addr_book ab on UX.addr_id = ab.id
           LEFT JOIN suppliers su on ab.sup_id = su.id
           WHERE (CD.leader=%s OR EXISTS(SELECT 1 FROM complaint_sup_view_right_incorrupt WHERE m_id=CD.id AND utype='qy' AND usr_id=%s) or %s=2029) #AND IFNULL(CD.finish,0) !=1
        """%(usr_id_qy,usr_id_qy,usr_id_qy,usr_id_qy)
    if search !='':
        sql+="AND (IFNULL(OP.cname,'') LIKE '%%%s%%' )"%(search)
    if situation !='':
        sql+="AND (CD.status='%s' "%(situation)
        if situation !='9':
            sql+="AND IFNULL(CD.finish,0) !=1 "
        else:
            sql+="OR IFNULL(CD.finish,0) =1 "
        sql+=")"
    sql+="ORDER BY CD.id DESC"
    # print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[4]='内容隐藏'
        dataList.append(e)
    names = 'id req_no ctime cname memo status hasNew situation usr_name'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def myIncorruptComplaintDetail(request):  
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 9
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    #查出当前用户是否在审计部
    sql="""SELECT dept_id FROM users WHERE usr_id=%s
        """%(usr_id_qy)
    rows,iN=db.select(sql)
    dept_id=rows[0][0]
    if str(dept_id)=='77':
        viewRight = 0
    else:
        viewRight = 1

    sql = "update complaint_sup_view_right_incorrupt set hasNew = 0 where m_id=%s AND utype='qy' AND usr_id=%s"%(pk,usr_id_qy)
    db.executesql(sql)

    sql="""SELECT CD.id,OP.gc_no,OP.cname,DP.cname,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d')
               ,CD.complaintObject,U.usr_name,CD.memo,IFNULL(CD.random_no,''),IFNULL(CD.status,''),CD.level 
               ,IFNULL(CF.next_usr_id,0),IFNULL(CF.next_flow_id,0),IFNULL(CF.cur_flow_id,0),CD.leader,IFNULL(CF.ctime,''),CF.dealDays
               ,IFNULL(CD.status_sj,0),IFNULL(CD.cid_sj,0),IFNULL(UX.usr_name,''),IFNULL(CD.finish,0),su.cname,ab.mobile,CD.anonymous
               FROM complaint_sup_detail_incorrupt CD 
               LEFT JOIN out_proj OP ON OP.id = CD.prj_id
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               LEFT JOIN users U ON U.usr_id = CD.leader
               LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
               LEFT JOIN complaint_sup_flow_incorrupt CF ON CF.m_id = CD.id 
               LEFT JOIN addr_book ab on UX.addr_id = ab.id
               LEFT JOIN suppliers su on ab.sup_id = su.id
               WHERE CD.id=%s ORDER BY CF.id DESC LIMIT 1
            """%(pk)
    print sql
    rows,iN=db.select(sql)
    random_no=rows[0][8]
    status=str(rows[0][9])
    level=rows[0][10]
    next_usr_id=rows[0][11]
    cur_flow_id=rows[0][13]
    leader=rows[0][14]
    ctime=rows[0][15] #流程提交日期
    dealDays=rows[0][16] #处理期限
    status_sj=rows[0][17] #审计流程ID
    cid_sj =rows[0][18] #介入审计ID
    finish =rows[0][20] #是否已结案
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    dataDetail=[]
    for e in rows:
        e=list(e)
        #if viewRight==0:
        #    e[6]='内容隐藏'
        #    e[8]='内容隐藏'
        dataDetail.append(e)
    # print day
    names = 'id req_no proj_name dept_name ctime complaintObject usr_name memo random_no status level next_usr_id next_flow_id cur_flow_id leader fctime dealDays status_sj cid_sj complainant finish supplier mobile anonymous'.split()
    data = [dict(zip(names, d)) for d in dataDetail]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    btn=[]
    if finish !=1:
        if next_usr_id==0: 
            if leader==usr_id_qy:
                btn.append(['0','交办处理人'])
        else:
            if usr_id_qy == next_usr_id:
                if status=='' or status=='-1':
                    btn.append(['0','交办'])
                elif status=='0':
                    btn.append(['1','提交'])
                elif status=='1':
                    btn.append(['2','处理结果上报'])
                elif status=='2':
                    btn.append(['3','处理结果确认'])
    names = 'btnType title'.split()
    data = [dict(zip(names, d)) for d in btn]
    btn = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT FP.id,FP.ctime,ifnull(FP.title,''),FP.fname,FP.file_size,FP.is_pic,'','','',YEAR(ctime),MONTH(ctime)
            FROM file_pic_gy FP
            WHERE FP.random_no='%s'
        """%(random_no)
    # print sql
    rows,iN = db.select(sql)
    file_list=[]
    for e in rows:
        e=list(e)
        url = "%s/fileUpload_gy/file_down?fname=%s"%(data_url,e[3])
        e[6] = url
        e[7] = "%s/%s/%s/thumbnail/%s"%(attach_url,e[9],e[10],e[3])
        file_list.append(e)
        # print e[6]
    names = 'id ctime title fname file_size is_pic url thumbnail_url'.split()
    data = [dict(zip(names, d)) for d in file_list]
    LL = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT CF.id,U.usr_name,CF.ctime,F.cname,CF.memo,IFNULL(FP.fname,''),FP.is_pic
            FROM complaint_sup_flow_incorrupt CF  
            LEFT JOIN users U ON U.usr_id = CF.cid
            LEFT JOIN flow F ON F.flow_id = CF.cur_flow_id AND F.ftype='ts'
            LEFT JOIN file_pic_gy FP ON FP.random_no = CF.random_no
            WHERE CF.m_id=%s
            ORDER BY CF.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    tem=[]
    data_tem=''
    file_tem=[]
    n=0
    mark=0
    for e in rows:
        if n>0 and mark!=e[0]:
            data_tem[5]=file_tem
            tem.append(data_tem)
            data_tem=list(e)
            file_tem=[]
            file_list=[]
            if e[5] !='':
                url = "%s/fileUpload_gy/file_down?fname=%s"%(data_url,e[5])
                file_list.append(e[5])  
                file_list.append(url)
                file_list.append(e[6])
                file_tem.append(file_list)
        else:
            data_tem=list(e)
            if viewRight==0:
                data_tem[4]='内容隐藏'
            file_list=[]
            if e[5] !='':
                url = "%s/fileUpload_gy/file_down?fname=%s"%(data_url,e[5])
                file_list.append(e[5])  
                file_list.append(url)
                file_list.append(e[6])
                file_tem.append(file_list)  
        mark = e[0]
        n+=1
    if len(file_tem)!=0:
        data_tem[5]=file_tem
    if len(data_tem)!=0:
        tem.append(data_tem)
    names = 'id usr_name ctime cname memo file'.split()
    data = [dict(zip(names, d)) for d in tem]
    flow = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    sql ="""SELECT MS.id,U.usr_name,MS.ctime,MS.memo
            FROM complaint_sup_message_incorrupt MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
            WHERE MS.m_id=%s
            ORDER BY MS.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    tem=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[3]='内容隐藏'
        tem.append(e)
    names = 'id usr_name ctime memo'.split()
    data = [dict(zip(names, d)) for d in tem]
    message = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映详情成功",
        "data":%s,
        "files":%s,
        "btn":%s,
        "flow":%s,
        "viewRight":%s,
        "message":%s
        }        """%(L,LL,btn,flow,viewRight,message)
    return HttpResponseJsonCORS(s)

def myComplaint(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    #查出当前用户是否在审计部
    sql="""SELECT dept_id FROM users WHERE usr_id=%s
        """%(usr_id_qy)
    rows,iN=db.select(sql)
    dept_id=rows[0][0]
    if str(dept_id)=='77':
        viewRight = 0
    else:
        viewRight = 1
    sql="""SELECT CD.id,IFNULL(OP.gc_no,''),FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d'),IFNULL(OP.cname,''),CD.memo,CD.status,IFNULL(VR.hasNew,0)
           ,CASE WHEN IFNULL(CD.finish,0)=1 THEN '已结案' ELSE IFNULL(F.cname,'新情况') END,su.cname
           FROM complaint_sup_detail CD 
           LEFT JOIN complaint_sup_view_right VR ON VR.m_id=CD.id AND VR.utype='qy' AND VR.usr_id=%s
           LEFT JOIN out_proj OP ON OP.id = CD.prj_id
           LEFT JOIN flow F ON F.ftype='ts' AND F.flow_id=CD.status
           LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
           LEFT JOIN addr_book ab on UX.addr_id = ab.id
           LEFT JOIN suppliers su on ab.sup_id = su.id
           WHERE (CD.leader=%s OR EXISTS(SELECT 1 FROM complaint_sup_view_right WHERE m_id=CD.id AND utype='qy' AND usr_id=%s) or %s=2110) #AND IFNULL(CD.finish,0) !=1
        """%(usr_id_qy,usr_id_qy,usr_id_qy,usr_id_qy)
    if search !='':
        sql+="AND (IFNULL(OP.cname,'') LIKE '%%%s%%' )"%(search)
    if situation !='':
        sql+="AND (CD.status='%s' "%(situation)
        if situation !='9':
            sql+="AND IFNULL(CD.finish,0) !=1 "
        else:
            sql+="OR IFNULL(CD.finish,0) =1 "
        sql+=")"
    sql+="ORDER BY CD.id DESC"
    # print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[4]='内容隐藏'
        dataList.append(e)
    names = 'id req_no ctime cname memo status hasNew situation usr_name'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def myComplaintDetail(request):  
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 9
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    #查出当前用户是否在审计部
    sql="""SELECT dept_id FROM users WHERE usr_id=%s
        """%(usr_id_qy)
    rows,iN=db.select(sql)
    dept_id=rows[0][0]
    if str(dept_id)=='77':
        viewRight = 0
    else:
        viewRight = 1

    sql = "update complaint_sup_view_right set hasNew = 0 where m_id=%s AND utype='qy' AND usr_id=%s"%(pk,usr_id_qy)
    db.executesql(sql)

    sql="""SELECT CD.id,OP.gc_no,'',OP.cname,DP.cname,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d')
               ,CD.complaintObject,U.usr_name,CD.memo,IFNULL(CD.random_no,''),IFNULL(CD.status,''),CD.level 
               ,IFNULL(CF.next_usr_id,0),IFNULL(CF.next_flow_id,0),IFNULL(CF.cur_flow_id,0),CD.leader,IFNULL(CF.ctime,''),CF.dealDays
               ,IFNULL(CD.status_sj,0),IFNULL(CD.cid_sj,0),IFNULL(UX.usr_name,''),IFNULL(CD.finish,0),su.cname,ab.mobile
               FROM complaint_sup_detail CD 
               LEFT JOIN out_proj OP ON OP.id = CD.prj_id
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               LEFT JOIN users U ON U.usr_id = CD.leader
               LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
               LEFT JOIN complaint_sup_flow CF ON CF.m_id = CD.id 
               LEFT JOIN addr_book ab on UX.addr_id = ab.id
               LEFT JOIN suppliers su on ab.sup_id = su.id
               WHERE CD.id=%s ORDER BY CF.id DESC LIMIT 1
            """%(pk)
    rows,iN=db.select(sql)
    random_no=rows[0][9]
    status=str(rows[0][10])
    level=rows[0][11]
    next_usr_id=rows[0][12]
    cur_flow_id=rows[0][14]
    leader=rows[0][15]
    ctime=rows[0][16] #流程提交日期
    dealDays=rows[0][17] #处理期限
    status_sj=rows[0][18] #审计流程ID
    cid_sj =rows[0][19] #介入审计ID
    finish =rows[0][21] #是否已结案
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    dataDetail=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[6]='内容隐藏'
            e[8]='内容隐藏'
        dataDetail.append(e)
    # print day
    names = 'id req_no apply_day proj_name dept_name ctime complaintObject usr_name memo random_no status level next_usr_id next_flow_id cur_flow_id leader fctime dealDays status_sj cid_sj complainant finish supplier mobile'.split()
    data = [dict(zip(names, d)) for d in dataDetail]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    btn=[]
    if finish !=1:
        if next_usr_id==0: 
            if leader==usr_id_qy:
                btn.append(['0','交办处理人'])
                if level<3:
                    btn.append(['-1','上报至上级领导'])
        else:
            if usr_id_qy == next_usr_id:
                if status=='' or status=='-1':
                    btn.append(['0','交办处理人'])
                    if level<3:
                        btn.append(['-1','上报至上级领导'])
                elif status=='0':
                    btn.append(['1','提交受理结果'])
                elif status=='1':
                    btn.append(['2','处理结果上报'])
                elif status=='2':
                    btn.append(['3','处理结果确认'])
        if status=='1' and ctime !='':
            d1 = datetime.datetime(int(ctime[:4]),int(ctime[5:7]),int(ctime[8:10]))
            d2 = datetime.datetime(int(now[:4]),int(now[5:7]),int(now[8:10]))
            day =(d2-d1).days

            if str(dept_id)=='77':
                if day>dealDays and str(status_sj)=='0':
                    btn.append(['4','收单介入'])
                if str(status_sj)=='4' and usr_id_qy==cid_sj:
                    btn.append(['5','上报监事长'])
    names = 'btnType title'.split()
    data = [dict(zip(names, d)) for d in btn]
    btn = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT FP.id,FP.ctime,ifnull(FP.title,''),FP.fname,FP.file_size,FP.is_pic,'','','',YEAR(ctime),MONTH(ctime)
            FROM file_pic_gy FP
            WHERE FP.random_no='%s'
        """%(random_no)
    # print sql
    rows,iN = db.select(sql)
    file_list=[]
    for e in rows:
        e=list(e)
        url = "%s/fileUpload_gy/file_down?fname=%s"%(data_url,e[3])
        e[6] = url
        e[7] = "%s/%s/%s/thumbnail/%s"%(attach_url,e[9],e[10],e[3])
        file_list.append(e)
        # print e[6]
    names = 'id ctime title fname file_size is_pic url thumbnail_url'.split()
    data = [dict(zip(names, d)) for d in file_list]
    LL = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT CF.id,U.usr_name,CF.ctime,F.cname,CF.memo,IFNULL(FP.fname,''),FP.is_pic
            FROM complaint_sup_flow CF  
            LEFT JOIN users U ON U.usr_id = CF.cid
            LEFT JOIN flow F ON F.flow_id = CF.cur_flow_id AND F.ftype='ts'
            LEFT JOIN file_pic_gy FP ON FP.random_no = CF.random_no
            WHERE CF.m_id=%s
            ORDER BY CF.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    tem=[]
    data_tem=''
    file_tem=[]
    n=0
    mark=0
    for e in rows:
        if n>0 and mark!=e[0]:
            data_tem[5]=file_tem
            tem.append(data_tem)
            data_tem=list(e)
            file_tem=[]
            file_list=[]
            if e[5] !='':
                url = "%s/fileUpload_gy/file_down?fname=%s"%(data_url,e[5])
                file_list.append(e[5])  
                file_list.append(url)
                file_list.append(e[6])
                file_tem.append(file_list)
        else:
            data_tem=list(e)
            if viewRight==0:
                data_tem[4]='内容隐藏'
            file_list=[]
            if e[5] !='':
                url = "%s/fileUpload_gy/file_down?fname=%s"%(data_url,e[5])
                file_list.append(e[5])  
                file_list.append(url)
                file_list.append(e[6])
                file_tem.append(file_list)  
        mark = e[0]
        n+=1
    if len(file_tem)!=0:
        data_tem[5]=file_tem
    if len(data_tem)!=0:
        tem.append(data_tem)
    names = 'id usr_name ctime cname memo file'.split()
    data = [dict(zip(names, d)) for d in tem]
    flow = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    sql ="""SELECT MS.id,U.usr_name,MS.ctime,MS.memo
            FROM complaint_sup_message MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
            WHERE MS.m_id=%s
            ORDER BY MS.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    tem=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[3]='内容隐藏'
        tem.append(e)
    names = 'id usr_name ctime memo'.split()
    data = [dict(zip(names, d)) for d in tem]
    message = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商反映详情成功",
        "data":%s,
        "files":%s,
        "btn":%s,
        "flow":%s,
        "viewRight":%s,
        "message":%s
        }        """%(L,LL,btn,flow,viewRight,message)
    return HttpResponseJsonCORS(s)

def putFlow_incorrupt(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
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
    btntype = request.POST.get('btnType','')
    dealMan = request.POST.get('dealMan','')
    random_no = request.POST.get('random_no','')
    memo = request.POST.get('memo','')
    level = request.POST.get('level','') or 0
    dealDays = request.POST.get('dealDays','') or 0
    isok = request.POST.get('isok','')
    is_open = request.POST.get('is_open') or 0

    memo = MySQLdb.escape_string(memo)
    # print request.POST
    sql="""SELECT IFNULL(CF.next_flow_id,''),CD.leader,IFNULL(CF.next_usr_id,0),IFNULL(CD.dealMan,0) FROM complaint_sup_detail_incorrupt CD 
           LEFT JOIN complaint_sup_flow_incorrupt CF ON CF.m_id = CD.id
           WHERE CD.id = %s
           ORDER BY CF.id desc limit 1
        """%(pk)
    print sql
    rows,iN=db.select(sql)
    next_flow_id = rows[0][0]
    leader = rows[0][1]
    next_usr_id = rows[0][2]
    accMan = rows[0][3]  #受理人
    sql=''
    if next_usr_id==0:
        # print '=============='
        if leader==usr_id_qy and btntype=='-1':
            flownext=1
            cur_flow_id=0
            if btntype=='-1':
                flownext=0
                cur_flow_id=-1
                sql1="""UPDATE complaint_sup_detail_incorrupt SET level=%s WHERE id = %s
                    """%(level,pk)
                db.executesql(sql1)
            sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                """%(pk,usr_id_qy,dealMan,flownext,memo,cur_flow_id,random_no,is_open)
        if leader==usr_id_qy and btntype=='0':
            flownext=1
            cur_flow_id=0
            sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                """%(pk,usr_id_qy,dealMan,flownext,memo,cur_flow_id,random_no,is_open)
    else:
        # print '---------------------'
        if next_usr_id==usr_id_qy:
            if btntype=='0':
                flownext=1
                cur_flow_id=0
                sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                    VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                    """%(pk,usr_id_qy,dealMan,flownext,memo,cur_flow_id,random_no,is_open)
            elif btntype=='1':
                sql2="""UPDATE complaint_sup_detail_incorrupt SET dealMan=%s WHERE id = %s
                    """%(usr_id_qy,pk)
                db.executesql(sql2)
                flownext=2
                cur_flow_id=1
                sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,dealDays,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s,%s);
                """%(pk,usr_id_qy,usr_id_qy,flownext,memo,cur_flow_id,random_no,dealDays,is_open)
            elif btntype=='2':
                flownext=3
                cur_flow_id=2
                sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                """%(pk,usr_id_qy,leader,flownext,memo,cur_flow_id,random_no,is_open)
            elif btntype=='3':
                flownext=10
                cur_flow_id=9
                # print '**************'
                if str(isok)=='1':
                    sql3="""UPDATE complaint_sup_detail_incorrupt SET finish=1 WHERE id = %s
                        """%(pk)
                    db.executesql(sql3)
                    sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,isok,is_open)
                        VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',1,%s);
                        """%(pk,usr_id_qy,leader,flownext,memo,cur_flow_id,random_no,is_open)
                if str(isok)=='0':
                    flownext=2
                    cur_flow_id=1
                    sql="""INSERT INTO complaint_sup_flow_incorrupt(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,isok,is_open)
                        VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',0,%s);
                        """%(pk,usr_id_qy,accMan,flownext,memo,cur_flow_id,random_no,is_open)
    # print sql 
    if sql!='':
        sql+="""UPDATE complaint_sup_detail_incorrupt SET status = %s WHERE id = %s;
            """%(cur_flow_id,pk)
        if dealMan !='':
            sql+="""INSERT INTO complaint_sup_view_right_incorrupt(m_id,usr_id,utype) VALUES(%s,%s,'qy');
                """%(pk,dealMan)
        sql+="""UPDATE complaint_sup_view_right_incorrupt SET hasNew=1 WHERE m_id=%s AND usr_id !=%s
            """%(pk,usr_id_qy)
        # print sql
        db.executesql(sql)

        if btntype=='-1' or btntype=='0' or btntype=='2':
            sql="""SELECT id FROM complaint_sup_flow_incorrupt WHERE random_no='%s'"""%(random_no)
            rows,iN = db.select(sql)
            id = rows[0][0]
            mWxPushMsg_Flow_incorrupt(request,id)
        elif btntype=='3':
            sql="""SELECT id FROM complaint_sup_flow_incorrupt WHERE random_no='%s'"""%(random_no)
            rows,iN = db.select(sql)
            id = rows[0][0]
            if str(isok)=='1':
                #mWxPushMsg_Comfirm_incorrupt(request,id,1)
                mWxPushMsg_Comfirm_fw_incorrupt(request,id)
            else:
                mWxPushMsg_Comfirm_incorrupt(request,id,0)
        s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
        return HttpResponseJsonCORS(s)
    else:
        s = """
        {
        "errcode": -1,
        "errmsg": "提交失败"
        }        """
        return HttpResponseJsonCORS(s)

def putFlow(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
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
    btntype = request.POST.get('btnType','')
    dealMan = request.POST.get('dealMan','')
    random_no = request.POST.get('random_no','')
    memo = request.POST.get('memo','')
    level = request.POST.get('level','') or 0
    dealDays = request.POST.get('dealDays','') or 0
    isok = request.POST.get('isok','')
    is_open = request.POST.get('is_open') or 0

    memo = MySQLdb.escape_string(memo)
    # print request.POST
    sql="""SELECT IFNULL(CF.next_flow_id,''),CD.leader,IFNULL(CF.next_usr_id,0),IFNULL(CD.dealMan,0) FROM complaint_sup_detail CD 
           LEFT JOIN complaint_sup_flow CF ON CF.m_id = CD.id
           WHERE CD.id = %s
           ORDER BY CF.id desc limit 1
        """%(pk)
    # print request.POST
    rows,iN=db.select(sql)
    next_flow_id = rows[0][0]
    leader = rows[0][1]
    next_usr_id = rows[0][2]
    accMan = rows[0][3]  #受理人
    sql=''
    if next_usr_id==0:
        # print '=============='
        if leader==usr_id_qy and btntype=='-1':
            flownext=1
            cur_flow_id=0
            if btntype=='-1':
                flownext=0
                cur_flow_id=-1
                sql1="""UPDATE complaint_sup_detail SET level=%s WHERE id = %s
                    """%(level,pk)
                db.executesql(sql1)
            sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                """%(pk,usr_id_qy,dealMan,flownext,memo,cur_flow_id,random_no,is_open)
        if leader==usr_id_qy and btntype=='0':
            flownext=1
            cur_flow_id=0
            sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                """%(pk,usr_id_qy,dealMan,flownext,memo,cur_flow_id,random_no,is_open)
    else:
        # print '---------------------'
        if next_usr_id==usr_id_qy:
            if btntype=='0':
                flownext=1
                cur_flow_id=0
                sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                    VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                    """%(pk,usr_id_qy,dealMan,flownext,memo,cur_flow_id,random_no,is_open)
            elif btntype=='1':
                sql2="""UPDATE complaint_sup_detail SET dealMan=%s WHERE id = %s
                    """%(usr_id_qy,pk)
                db.executesql(sql2)
                flownext=2
                cur_flow_id=1
                sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,dealDays,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s,%s);
                """%(pk,usr_id_qy,usr_id_qy,flownext,memo,cur_flow_id,random_no,dealDays,is_open)
            elif btntype=='2':
                flownext=3
                cur_flow_id=2
                sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,is_open)
                VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',%s);
                """%(pk,usr_id_qy,leader,flownext,memo,cur_flow_id,random_no,is_open)
            elif btntype=='3':
                flownext=10
                cur_flow_id=9
                # print '**************'
                if str(isok)=='1':
                    sql3="""UPDATE complaint_sup_detail SET finish=1 WHERE id = %s
                        """%(pk)
                    db.executesql(sql3)
                    sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,isok,is_open)
                        VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',1,%s);
                        """%(pk,usr_id_qy,leader,flownext,memo,cur_flow_id,random_no,is_open)
                if str(isok)=='0':
                    flownext=2
                    cur_flow_id=1
                    sql="""INSERT INTO complaint_sup_flow(m_id,ctime,cid,next_usr_id,next_flow_id,memo,cur_flow_id,random_no,isok,is_open)
                        VALUES(%s,now(),%s,%s,%s,'%s',%s,'%s',0,%s);
                        """%(pk,usr_id_qy,accMan,flownext,memo,cur_flow_id,random_no,is_open)
    # print sql 
    if sql!='':
        sql+="""UPDATE complaint_sup_detail SET status = %s WHERE id = %s;
            """%(cur_flow_id,pk)
        if dealMan !='':
            sql+="""INSERT INTO complaint_sup_view_right(m_id,usr_id,utype) VALUES(%s,%s,'qy');
                """%(pk,dealMan)
        sql+="""UPDATE complaint_sup_view_right SET hasNew=1 WHERE m_id=%s AND usr_id !=%s
            """%(pk,usr_id_qy)
        # print sql
        db.executesql(sql)

        if btntype=='-1' or btntype=='0' or btntype=='2':
            sql="""SELECT id FROM complaint_sup_flow WHERE random_no='%s'"""%(random_no)
            rows,iN = db.select(sql)
            id = rows[0][0]
            mWxPushMsg_Flow(request,id)
        elif btntype=='3':
            sql="""SELECT id FROM complaint_sup_flow WHERE random_no='%s'"""%(random_no)
            rows,iN = db.select(sql)
            id = rows[0][0]
            if str(isok)=='1':
                mWxPushMsg_Comfirm(request,id,1)
                mWxPushMsg_Comfirm_fw(request,id)
            else:
                mWxPushMsg_Comfirm(request,id,0)
        s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
        return HttpResponseJsonCORS(s)
    else:
        s = """
        {
        "errcode": -1,
        "errmsg": "提交失败"
        }        """
        return HttpResponseJsonCORS(s)

def putFlowSj(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
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
    btntype = request.POST.get('btnType','')
    leader = 'NULL'
    random_no = "%s_%s_gysj"%(time.time(),usr_id_qy)
    if btntype=='5':
        sql="""SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'监事长')
               FROM dept DP
               LEFT JOIN users U ON DP.header = U.usr_id
               WHERE DP.id = 76
            """
        rows,iN=db.select(sql)
        leader=rows[0][0]
    sql="""INSERT INTO complaint_sup_flow_sj(m_id,cid,ctime,status,leader,random_no)
        VALUES(%s,%s,now(),%s,%s,'%s');
        """%(pk,usr_id_qy,btntype,leader,random_no)
    sql+="""UPDATE complaint_sup_detail SET status_sj=%s,cid_sj=%s WHERE id=%s
        """%(btntype,usr_id_qy,pk)
    # print sql 
    db.executesql(sql)
    if btntype=='5':
        sql="""SELECT id FROM complaint_sup_flow_sj WHERE random_no='%s'"""%random_no
        rows,iN = db.select(sql)
        id = rows[0][0]
        mWxPushMsg_FlowSj(request,id)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
    return HttpResponseJsonCORS(s)

def putFlowDetail(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    btntype = request.POST.get('btnType','')
    pk = request.POST.get('pk','')
    # print request.POST
    # pk='9'
    # btntype='-1'
    random_no = "%s_%s_qy_gy"%(time.time(),usr_id_qy)
    leader=''
    leader = json.dumps(leader,ensure_ascii=False)
    if btntype=='-1':
        sql="""SELECT CD.id,DP.id,IFNULL(CD.level,1)
               FROM complaint_sup_detail CD 
               LEFT JOIN out_proj OP ON OP.id = CD.prj_id
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               WHERE CD.id=%s
            """%(pk)
        dept = 0
        rows,iN=db.select(sql)
        if iN>0:
            dept = rows[0][1]
            level = rows[0][2]
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

        rows,iN=db.select(sql)
        leader=[]
        n=0
        for e in rows:
            n+=1
            if e[0] !=0 and n>level:
                leader.append(list(e))
        names = 'usr_id usr_name dept_id dept_name level'.split()
        data = [dict(zip(names, d)) for d in leader]
        leader = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)


    # if btntype=='5':
    #     sql="""SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'监事长')
    #            FROM dept DP
    #            LEFT JOIN users U ON DP.header = U.usr_id
    #            WHERE DP.id = 76
    #         """
    #     rows,iN=db.select(sql)
    #     names = 'usr_id usr_name dept_id dept_name'.split()
    #     data = [dict(zip(names, d)) for d in rows]
    #     leader = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder) 
    s = """
        {
        "errcode": 0,
        "errmsg": "获取流程详情信息成功",
        "random_no":"%s",
        "leader":%s
        }"""%(random_no,leader)
    return HttpResponseJsonCORS(s)

def putMessage_incorrupt(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    memo = request.POST.get('memo','')
    pk = request.POST.get('pk','')
    canview = request.POST.get('canview','') or 0
    memo = MySQLdb.escape_string(memo)
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    cRandom = str(usr_id_qy) + '_' + str(time.time())
    sql="""INSERT INTO complaint_sup_message_incorrupt(cid,ctime,memo,m_id,canview,cRandom)
        VALUES(%s,now(),'%s',%s,%s,'%s');
        """%(usr_id_qy,memo,pk,canview,cRandom)
    sql+="""UPDATE complaint_sup_view_right_incorrupt SET hasNew=1 WHERE m_id=%s AND usr_id !=%s
            """%(pk,usr_id_qy)
    db.executesql(sql)

    sql ="select id from complaint_sup_message_incorrupt where cRandom='%s'"%cRandom
    rows,iN = db.select(sql)
    id = rows[0][0]
    mWxPushMsg_Comment_qy_incorrupt(request,id)
    if str(canview)=='1':
        mWxPushMsg_Comment_fw_incorrupt(request,id)
    sql="""insert into complaint_sup_message_push_incorrupt (m_id,ctime) values (%s,now())"""%(id)
    db.executesql(sql)

    #查出当前用户是否在审计部
    sql="""SELECT dept_id FROM users WHERE usr_id=%s
        """%(usr_id_qy)
    rows,iN=db.select(sql)
    dept_id=rows[0][0]
    if str(dept_id)=='77':
        viewRight = 0
    else:
        viewRight = 1
    sql ="""SELECT MS.id,U.usr_name,MS.ctime,MS.memo
            FROM complaint_sup_message_incorrupt MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
            WHERE MS.m_id=%s
            ORDER BY MS.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    tem=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[3]='内容隐藏'
        tem.append(e)
    names = 'id usr_name ctime memo'.split()
    data = [dict(zip(names, d)) for d in tem]
    message = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "提交留言成功",
        "message":%s
        }        """%(message)
    return HttpResponseJsonCORS(s)

def putMessage(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    memo = request.POST.get('memo','')
    pk = request.POST.get('pk','')
    canview = request.POST.get('canview','') or 0
    memo = MySQLdb.escape_string(memo)
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    cRandom = str(usr_id_qy) + '_' + str(time.time())
    sql="""INSERT INTO complaint_sup_message(cid,ctime,memo,m_id,canview,cRandom)
        VALUES(%s,now(),'%s',%s,%s,'%s');
        """%(usr_id_qy,memo,pk,canview,cRandom)
    sql+="""UPDATE complaint_sup_view_right SET hasNew=1 WHERE m_id=%s AND usr_id !=%s
            """%(pk,usr_id_qy)
    db.executesql(sql)

    sql ="select id from complaint_sup_message where cRandom='%s'"%cRandom
    rows,iN = db.select(sql)
    id = rows[0][0]
    mWxPushMsg_Comment_qy(request,id)
    if str(canview)=='1':
        mWxPushMsg_Comment_fw(request,id)
    sql="""insert into complaint_sup_message_push (m_id,ctime) values (%s,now())"""%(id)
    db.executesql(sql)

    #查出当前用户是否在审计部
    sql="""SELECT dept_id FROM users WHERE usr_id=%s
        """%(usr_id_qy)
    rows,iN=db.select(sql)
    dept_id=rows[0][0]
    if str(dept_id)=='77':
        viewRight = 0
    else:
        viewRight = 1
    sql ="""SELECT MS.id,U.usr_name,MS.ctime,MS.memo
            FROM complaint_sup_message MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
            WHERE MS.m_id=%s
            ORDER BY MS.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    tem=[]
    for e in rows:
        e=list(e)
        if viewRight==0:
            e[3]='内容隐藏'
        tem.append(e)
    names = 'id usr_name ctime memo'.split()
    data = [dict(zip(names, d)) for d in tem]
    message = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "提交留言成功",
        "message":%s
        }        """%(message)
    return HttpResponseJsonCORS(s)

import httplib
def mWxPushMsg_Comment_qy(request,id):   
    year=getToday()[:4]  
    L,toUser =Get_data_Comment(request,id,'qy')
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
    proj_name = L[2]
    cusrname = L[1]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,file_id)
    stitle ="""新评论提醒"""
    description = """【%s】发表了关于“%s”情况反映的评论，请及时查阅。"""%(cusrname,proj_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    surl = my_urlencode(sUrl)
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

    """%(m_sAgentId_gy,stitle,url,description)
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

def mWxPushMsg_Comment_fw(request,id):   
    year=getToday()[:4]  
    L,toUser =Get_data_Comment(request,id,'fw')
    sToken =  read_access_token()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    file_id=L[0]
    proj_name = L[2]
    cusrname = L[1]
    toUser = L[3]
    sUrl='%s/complaint/login/default_gy?fid=complainDetail&seq=%s&must_reply=true'%(host_url,file_id)
    stitle ="""新评论提醒"""
    description = """【%s】对您提交的关于“%s”情况反映发表了评论，请及时查阅。"""%(cusrname,proj_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    surl = my_urlencode(sUrl)
    sUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

    sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "url":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#173177"
            }
            
            }
            }
    """%(toUser,template_id_msg_gy,sUrl,description)
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
    return HttpResponseCORS(request,errcode)

def Get_data_Comment(request,id,utype):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    L=[]
    sql="""SELECT CD.id,U.usr_name,IFNULL(OP.cname,''),UX.openid 
        FROM complaint_sup_message MSG
        LEFT JOIN complaint_sup_detail CD ON CD.id = MSG.m_id 
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users U ON U.usr_id = MSG.cid
        WHERE MSG.id = %s
        """%(id)
    # print sql
    rows,iN = db.select(sql)
    pk =rows[0][0]
    L=rows[0]
    toUser=''
    if utype=='qy':
        sql="""SELECT IFNULL(U.login_id,'') FROM complaint_sup_view_right VR 
            LEFT JOIN users U ON U.usr_id=VR.usr_id
            WHERE VR.m_id = %s AND VR.usr_id !=%s AND VR.utype='%s'
            """%(pk,usr_id_qy,utype)
        rows,iN = db.select(sql)
        for e in rows:
            toUser+='%s|'%(e[0])
    return L,toUser

def mWxPushMsg_Flow(request,id):
    year=getToday()[:4]  
    L =Get_data_Flow(request,id)
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
    cusrname = L[1]
    proj_name = L[2]
    nowUsrname = L[3]
    complaintObject = L[4]
    toUser = L[5]
    if toUser=='gup':
        toUser+='|mengxp|zhongzhg|hanruiming'
    flow_id = L[6]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&seq=%s&func_id=1000004&must_reply=true'%(host_url,file_id)
    surl = my_urlencode(sUrl)

    if str(flow_id)=='-1':
        stitle ="""新上报提醒"""
        description = """【%s】将“%s”反映“%s”关于“%s”的情况提报给您，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    elif str(flow_id)=='0':
        stitle ="""新指派提醒"""
        description = """【%s】指派您处理“%s”反映“%s”关于“%s”的情况，请及时查阅并受理该情况反映。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    elif str(flow_id)=='2':
        stitle ="""新处理结果上报提醒"""
        description = """【%s】就“%s”反映“%s”关于“%s”的情况提交了处理结果，请及时查阅并受理该情况反映。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    else:
        stitle=''
        description=''
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

    """%(m_sAgentId_gy,stitle,url,description)
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

def Get_data_Flow(request,id):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,IFNULL(OP.cname,''),UC.usr_name,CD.complaintObject,UN.login_id,CF.cur_flow_id
        FROM complaint_sup_flow CF 
        LEFT JOIN complaint_sup_detail CD ON CD.id = CF.m_id
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users UN ON UN.usr_id = CF.next_usr_id
        LEFT JOIN users UC ON UC.usr_id = CF.cid
        WHERE CF.id = %s
        """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_FlowSj(request,id):   
    year=getToday()[:4]  
    L =Get_data_FlowSj(request,id)
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
    cusrname = L[1]
    proj_name = L[2]
    nowUsrname = L[3]
    complaintObject = L[4]
    toUser = L[5]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,file_id)
    stitle ="""审计上报提醒"""
    description = """【%s】将“%s”反映“%s”关于“%s”的情况上报给您，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    surl = my_urlencode(sUrl)
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

    """%(m_sAgentId_gy,stitle,url,description)
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

def Get_data_FlowSj(request,id):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,IFNULL(OP.cname,''),UC.usr_name,CD.complaintObject,UN.login_id
        FROM complaint_sup_flow_sj CS 
        LEFT JOIN complaint_sup_detail CD ON CD.id = CS.m_id
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users UC ON UC.usr_id = CS.cid
        LEFT JOIN users UN ON UN.usr_id = CS.leader
        WHERE CS.id = %s
        """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_Comfirm(request,id,isok):
    year=getToday()[:4]  
    L =Get_data_Comfirm(request,id)
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
    cusrname = L[1]
    proj_name = L[2]
    nowUsrname = L[3]
    complaintObject = L[4]
    flow_id = L[6]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,file_id)
    surl = my_urlencode(sUrl)
    if str(isok) =='1':
        toUser = L[7]
        stitle ="""新处理结果通过提醒"""
        description = """【%s】通过了“%s”反映“%s”关于“%s”的情况反映，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    else:
        toUser = L[5]
        stitle ="""新退回提醒"""
        description = """【%s】将“%s”反映“%s”关于“%s”的情况退回给您，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    # print toUser
    if toUser=='gup':
        toUser+='|mengxp|zhongzhg|hanruiming'
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

    """%(m_sAgentId_gy,stitle,url,description)
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

def Get_data_Comfirm(request,id):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,IFNULL(OP.cname,''),UC.usr_name,CD.complaintObject,UN.login_id
        ,CF.cur_flow_id,UL.login_id,UX.openid,CF.ctime
        FROM complaint_sup_flow CF 
        LEFT JOIN complaint_sup_detail CD ON CD.id = CF.m_id
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users UN ON UN.usr_id = CF.next_usr_id
        LEFT JOIN users UC ON UC.usr_id = CF.cid
        LEFT JOIN users UL ON UL.usr_id = CD.leader
        WHERE CF.id = %s
        """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_Comfirm_fw(request,id):
    year=getToday()[:4]  
    L =Get_data_Comfirm(request,id)
    sToken =  read_access_token()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    file_id=L[0]
    proj_name = L[2]
    cusrname = L[3]
    toUser = L[8]
    ctime = L[9]
    sUrl='%s/complaint/login/default_gy?fid=complainDetail&seq=%s&must_reply=true'%(host_url,file_id)
    # stitle ="""新评论提醒"""
    description = """【%s】通过了“%s”情况反映，请及时查阅。"""%(cusrname,proj_name)
    surl = my_urlencode(sUrl)
    # print toUser
    # stitle=json.dumps(stitle)
    description = json.dumps(description)
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
            "value":"通过",
            "color":"#173177"
            },
            "keyword2": {
            "value":"%s",
            "color":"#173177"
            }
            
            }
            }
    """%(toUser,template_id_result_gy,url,description,ctime)
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
    return HttpResponseCORS(request,errcode)

def mWxPushMsg_Flow_incorrupt(request,id):
    year=getToday()[:4]  
    L =Get_data_Flow_incorrupt(request,id)
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
    cusrname = L[1]
    proj_name = L[2]
    nowUsrname = L[3]
    complaintObject = L[4]
    toUser = L[5]
    #toUser = 'lishijie'
    flow_id = L[6]
    sUrl='%s/complaint/login/login_qy?fid=accuseDetail&path=policy_accuse&seq=%s&func_id=1000004&must_reply=true'%(host_url,file_id)

    if str(flow_id)=='-1':
        stitle ="""【廉政投诉】新上报提醒"""
        description = """【%s】将廉政投诉“%s”关于“%s”的情况提报给您，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    elif str(flow_id)=='0':
        stitle ="""【廉政投诉】新指派提醒"""
        description = """【%s】指派您处理“%s”廉政投诉“%s”关于“%s”的情况，请及时查阅并受理该情况反映。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    elif str(flow_id)=='2':
        stitle ="""【廉政投诉】新处理结果上报提醒"""
        description = """【%s】就“%s”廉政投诉“%s”关于“%s”的情况提交了处理结果，请及时查阅并受理该情况反映。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    else:
        stitle=''
        description=''
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

def Get_data_Flow_incorrupt(request,id):
    L=[]
    sql="""SELECT CD.id,case CD.anonymous when 1 then '***' else UX.usr_name end,IFNULL(OP.cname,''), UC.usr_name,CD.complaintObject,UN.login_id,CF.cur_flow_id
        FROM complaint_sup_flow_incorrupt CF 
        LEFT JOIN complaint_sup_detail_incorrupt CD ON CD.id = CF.m_id
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users UN ON UN.usr_id = CF.next_usr_id
        LEFT JOIN users UC ON UC.usr_id = CF.cid
        WHERE CF.id = %s
        """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_Comfirm_incorrupt(request,id,isok):
    year=getToday()[:4]  
    L =Get_data_Comfirm_incorrupt(request,id)
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
    cusrname = L[1]
    proj_name = L[2]
    nowUsrname = L[3]
    complaintObject = L[4]
    flow_id = L[6]
    sUrl='%s/complaint/login/login_qy?fid=accuseDetail&path=policy_accuse&seq=%s&func_id=1000004&must_reply=true'%(host_url,file_id)
    if str(isok) =='1':
        toUser = L[7]
        stitle ="""【廉政投诉】新处理结果通过提醒"""
        description = """【%s】通过了“%s”反映“%s”关于“%s”的情况反映，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
    else:
        toUser = L[5]
        stitle ="""【廉政投诉】新退回提醒"""
        description = """【%s】将“%s”反映“%s”关于“%s”的情况退回给您，请及时查阅。"""%(nowUsrname,cusrname,complaintObject,proj_name)
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

def Get_data_Comfirm_incorrupt(request,id):
    L=[]
    sql="""SELECT CD.id,case CD.anonymous when 1 then '***' else UX.usr_name end,IFNULL(OP.cname,''),UC.usr_name,CD.complaintObject,UN.login_id
        ,CF.cur_flow_id,UL.login_id,UX.openid,CF.ctime
        FROM complaint_sup_flow_incorrupt CF 
        LEFT JOIN complaint_sup_detail_incorrupt CD ON CD.id = CF.m_id
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users UN ON UN.usr_id = CF.next_usr_id
        LEFT JOIN users UC ON UC.usr_id = CF.cid
        LEFT JOIN users UL ON UL.usr_id = CD.leader
        WHERE CF.id = %s
        """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_Comfirm_fw_incorrupt(request,id):
    year=getToday()[:4]  
    L =Get_data_Comfirm_incorrupt(request,id)
    sToken =  read_access_token()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    file_id=L[0]
    proj_name = L[2]
    cusrname = L[3]
    toUser = L[8]
    ctime = L[9]
    sUrl='%s/complaint/login/default_gy?fid=accuseDetail&path=policy_accuse&seq=%s&func_id=1000004&must_reply=true'%(host_url,file_id)
    # stitle ="""新评论提醒"""
    description = """您好，您的投诉已经受理完毕。"""
    # print toUser
    # stitle=json.dumps(stitle)
    description = json.dumps(description)
    surl = my_urlencode(sUrl)
    surl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

    template_id = 'vOWezoP_kVsTyCQyD9btAs3lMt5blS6TpqIvwVwK4ko'
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
            },
            "keyword3": {
            "value":"%s",
            "color":"#173177"
            }
            }
            }
    """%(toUser,template_id,sUrl,description,json.dumps(proj_name),json.dumps('监事会'),ctime)
    print ToGBK(sMsg)
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  
    res = conn.getresponse()       
    body = res.read() 
    print body
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return HttpResponseCORS(request,errcode)

def mWxPushMsg_Comment_qy_incorrupt(request,id):   
    year=getToday()[:4]  
    L,toUser =Get_data_Comment_incorrupt(request,id,'qy')
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
    proj_name = L[2]
    cusrname = L[1]
    sUrl='%s/complaint/login/login_qy?fid=accuseDetail&path=policy_accuse&seq=%s&func_id=1000004&must_reply=true'%(host_url,file_id)
    stitle ="""【廉政投诉】新评论提醒"""
    description = """【%s】发表了关于“%s”情况反映的评论，请及时查阅。"""%(cusrname,proj_name)
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

def mWxPushMsg_Comment_fw_incorrupt(request,id):   
    year=getToday()[:4]  
    L,toUser =Get_data_Comment_incorrupt(request,id,'fw')
    sToken =  read_access_token()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    file_id=L[0]
    proj_name = L[2]
    cusrname = L[1]
    toUser = L[3]
    sUrl='%s/complaint/login/default_gy?fid=accuseDetail&path=policy_accuse&seq=%s&func_id=1000004&must_reply=true'%(host_url,file_id)
    stitle ="""【廉政投诉】新评论提醒"""
    description = """【%s】对您提交的关于“%s”廉政投诉发表了评论，请及时查阅。"""%(cusrname,proj_name)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    surl = my_urlencode(sUrl)
    surl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

    sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "url":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#173177"
            }
            
            }
            }
    """%(toUser,template_id_msg_gy,sUrl,description)
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
    return HttpResponseCORS(request,errcode)

def Get_data_Comment_incorrupt(request,id,utype):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    L=[]
    sql="""SELECT CD.id,U.usr_name,IFNULL(OP.cname,''),UX.openid 
        FROM complaint_sup_message_incorrupt MSG
        LEFT JOIN complaint_sup_detail_incorrupt CD ON CD.id = MSG.m_id 
        LEFT JOIN users_gy UX ON UX.usr_id = CD.cid
        LEFT JOIN out_proj OP ON OP.id = CD.prj_id
        LEFT JOIN users U ON U.usr_id = MSG.cid
        WHERE MSG.id = %s
        """%(id)
    # print sql
    rows,iN = db.select(sql)
    pk =rows[0][0]
    L=rows[0]
    toUser=''
    if utype=='qy':
        sql="""SELECT IFNULL(U.login_id,'') FROM complaint_sup_view_right_incorrupt VR 
            LEFT JOIN users U ON U.usr_id=VR.usr_id
            WHERE VR.m_id = %s AND VR.usr_id !=%s AND VR.utype='%s'
            """%(pk,usr_id_qy,utype)
        rows,iN = db.select(sql)
        for e in rows:
            toUser+='%s|'%(e[0])
    return L,toUser