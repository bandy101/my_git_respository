# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,m_sCorpID,m_sCorpSecret,m_sAgentId_lw,m_sCorpSecret_lw'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,checkSession,data_url,host_url,my_urlencode,read_access_token_lw,write_access_token_lw'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
from HW_DT_TOOL                 import getToday
import MySQLdb

testid = 0
attach_url = 'http://lw.szby.cn/attach/'

def getLabourContractList(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    #if int(usr_id) == 447:
    #    usr_id = 173
    pageNo = request.POST.get('pageNo','') or 1
    pageNo = int(pageNo)
    search = request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    sql="""select lc.id,op.id,op.cname,lc.Req_no,lc.apply_day from labour_contract lc 
           left join out_proj op on lc.proj_id = op.id
           LEFT JOIN users_wx U ON U.addr_id = lc.teams_id
           left join labour_contract_invalid lci on lc.id = lci.lc_id
           where U.usr_id = %s and lci.id is null
        """%(usr_id)
    print sql
    if search !='':
        sql+="AND ( IFNULL(op.cname,'') LIKE '%%%s%%' OR IFNULL(lc.req_no,'') LIKE '%%%s%%' ) "%(search,search)
    sql+="ORDER BY lc.apply_day DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'lc_id proj_id proj_name req_no apply_day'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取协议列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    #print ToGBK(s)
    return HttpResponseJsonCORS(s)

def getProgressDetail(request):    
    usr_id = request.session.get('usr_id') or 0
    qy_usr_id = request.session.get('usr_id_qy') or 2110
    if usr_id ==0 and qy_usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    if qy_usr_id in [2110,627,431]:
        has_cancel_btn = 1
    else:
        has_cancel_btn = 0

    id = request.POST.get('id','')  
    lc_id = request.POST.get('lc_id','')
    mode = request.POST.get('mode','add') 
    if mode=='add' and lc_id=='': 
        s = """
        {
        "errcode": -1,
        "errmsg": "参数错误"
        }        """
        return HttpResponseJsonCORS(s)
    elif mode!='add' and id == '':
        s = """
        {
        "errcode": -1,
        "errmsg": "参数错误"
        }        """
        return HttpResponseJsonCORS(s)

    names = 'lc_id proj_id proj_name req_no apply_day proj_property dept_name lc_name paid_money pre_progress cur_progress progress_money visa_money memo status random_no declarer upper_limit unpaid_money plan_time pay_list ctime'.split()
    if mode=='add':
        sql = """select lc.id,op.id,op.cname,lc.Req_no,lc.apply_day,m.txt1,dp.cname,ifnull(su.cname,''),ifnull(pp.total_money,''),ifnull(pd.pre_progress,0),'','','','','','','','','','','',''
                 from labour_contract lc 
                 left join out_proj op on lc.proj_id = op.id
                 left join proj_tran_info ti on ti.proj_id = op.id
                 left join dept dp on ti.tran_to_dpid = dp.id
                 left join mtc_t m on m.id = ti.prj_property and m.type = 'XMSX'
                 left join suppliers su on su.id = lc.lab_id
                 left join (select sum(pay_money) as total_money,proj_id,team_id from progress_pay_list group by proj_id,team_id) pp on pp.proj_id = op.id and pp.team_id = lc.teams_id
                 left join (select max(cur_progress) as pre_progress,lc_id from progress_declare group by lc_id) pd on pd.lc_id = lc.id
                 where lc.id = '%s'"""%(lc_id)
        rows,iN=db.select(sql)
        if iN == 0:
            data = []
        else:
            random_no = "%s_%s"%(time.time(),usr_id)
            L1 = list(rows[0])
            L1[15] = random_no
            data = dict(zip(names, L1))
            data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

        files = []
    else:
        sql = """select lc.id,op.id,op.cname,lc.Req_no,lc.apply_day,m.txt1,dp.cname,ifnull(su.cname,''),ifnull(pd.paid_money,0),ifnull(pd.pre_progress,0),pd.cur_progress
                        ,pd.progress_money,pd.visa_money,pd.memo,pd.status,pd.random_no,ab.name,pd.upper_limit,pd.unpaid_money,pd.plan_time,'',pd.ctime
                 from progress_declare pd 
                 left join labour_contract lc on lc.id = pd.lc_id
                 left join out_proj op on lc.proj_id = op.id
                 left join proj_tran_info ti on ti.proj_id = op.id
                 left join dept dp on ti.tran_to_dpid = dp.id
                 left join mtc_t m on m.id = ti.prj_property and m.type = 'XMSX'
                 left join suppliers su on su.id = lc.lab_id
                 LEFT JOIN users_wx UX ON UX.usr_id = pd.cid
                 LEFT JOIN addr_book ab on ab.id = UX.addr_id
                 where pd.id = '%s'"""%(id)
        #print sql
        rows,iN=db.select(sql)
        if iN == 0:
            data = []
        else:
            random_no = "%s_%s"%(time.time(),usr_id)
            L1 = list(rows[0])
            sql1 = "select pay_money,pay_time,plan_money,plan_time from progress_pay_list where m_id = %s order by pay_time desc"%(id)
            rows1,iN1=db.select(sql1)
            names1 = 'pay_money pay_time plan_money plan_time'.split()
            L1[20] = [dict(zip(names1, d)) for d in rows1]
            data = dict(zip(names, L1))
            data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
        sql ="""SELECT FP.id,FP.ctime,ifnull(FP.title,''),FP.fname,FP.file_size,FP.is_pic,'','','',YEAR(ctime),MONTH(ctime)
            FROM file_pic_pp FP
            WHERE FP.m_id='%s'
            """%(id)
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
        files = [dict(zip(names, d)) for d in file_list]
        files = json.dumps(files,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取进度详情成功",
        "data":%s,
        "files":%s,
        "has_cancel_btn":%s
        }        """%(data,files,has_cancel_btn)
    return HttpResponseJsonCORS(s)

def saveProgressDetail(request):    
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    id = request.POST.get('id','') 
     
    data = request.POST.get('data','') 
    data_list = json.loads(data)
    visa_money = data_list.get('visa_money') or 0
    progress_money = data_list.get('progress_money') or 0
    paid_money = data_list.get('paid_money','')
    if paid_money == '':
        paid_money = 'NULL'
    pre_progress = data_list.get('pre_progress','')
    lc_id = data_list.get('lc_id','')
    proj_id = data_list.get('proj_id','')
    dept_name = data_list.get('dept_name','')
    memo = data_list.get('memo','')
    memo = MySQLdb.escape_string(memo)
    lc_name = data_list.get('lc_name','')
    cur_progress = data_list.get('cur_progress','')
    req_no = data_list.get('req_no','')
    random_no = data_list.get('random_no','')

    total_money = float(progress_money) + float(visa_money)

    if id == '':#新增
        sql = """INSERT INTO progress_declare (lc_id, proj_id,paid_money, pre_progress, cur_progress, progress_money, visa_money, total_money, random_no, status, memo,cid,ctime) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s', 0, '%s', %s, now());
          """%(lc_id, proj_id,paid_money, pre_progress, cur_progress, progress_money, visa_money, total_money, random_no, memo, usr_id)
        print ToGBK(sql)
        db.executesql(sql)

        sql = "select id from progress_declare where random_no='%s'"%(random_no)
        rows,iN=db.select(sql)
        id = rows[0][0]
        sql = "update file_pic_pp set m_id = %s where random_no='%s'"%(rows[0][0],random_no)
        db.executesql(sql)

        #推送给项目经理
        #mWxPushMsg_Progress(id)
    else:
        sql = """update progress_declare set cur_progress = %s, progress_money = %s, visa_money = %s, total_money = %s,memo = '%s'
                 where id = %s
          """%(cur_progress, progress_money, visa_money, total_money, memo, id)
        print ToGBK(sql)
        db.executesql(sql)

        sql = "update file_pic_pp set m_id = %s where random_no='%s'"%(id,random_no)
        db.executesql(sql)
        #推送给项目经理
        #mWxPushMsg_Progress(id)

    s = """
        {
        "errcode": 0,
        "errmsg": "进度款申报成功"
        }        """
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def getProgressList(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo = request.POST.get('pageNo','') or 1
    pageNo = int(pageNo)
    situation = request.POST.get('situation','')
    search = request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    sql="""select pd.id,op.cname,lc.Req_no,lc.apply_day,pd.cur_progress,pd.status,pd.ctime
           from progress_declare pd 
           left join labour_contract lc on lc.id = pd.lc_id
           left join out_proj op on lc.proj_id = op.id
           LEFT JOIN users_wx U ON U.addr_id = lc.teams_id
           where U.usr_id = %s
        """%(usr_id)
    if search !='':
        sql+="AND ( IFNULL(op.cname,'') LIKE '%%%s%%' OR IFNULL(lc.req_no,'') LIKE '%%%s%%' ) "%(search,search)
    if situation != '':
        sql += " and pd.status = %s "%(situation)
    sql+=" ORDER BY lc.apply_day DESC"
    #print ToGBK(sql)
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id proj_name req_no apply_day progress status ctime'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取进度款上报列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def getAgreementList(request):	
    # print request.POST
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
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
    sql="""SELECT LC.id,LC.req_no,LC.apply_day,OP.cname,'LC' as ctype,MT.txt1 FROM labour_contract LC 
           LEFT JOIN addr_book AB ON AB.id = LC.teams_id
           LEFT JOIN users_wx U ON U.addr_id = AB.id
           LEFT JOIN out_proj OP ON OP.id = LC.proj_id
           LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
           LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
           left join labour_contract_invalid lci on lc.id = lci.lc_id
           # LEFT JOIN users_wx UU ON UU.usr_id = 5
           WHERE U.usr_id=%s and lci.id is null
           UNION ALL 
           SELECT AA.id,AA.req_no,AA.apply_day,OP.cname,'AA' as ctype,MT.txt1 FROM assess_affirm AA 
           LEFT JOIN addr_book AB ON AB.id = AA.proj_p_id
           LEFT JOIN users_wx U ON U.addr_id = AB.id
           LEFT JOIN out_proj OP ON OP.id = AA.proj_id
           LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
           LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
           WHERE U.usr_id=%s
           
        """%(usr_id,usr_id)
    if search !='':
        sql+="AND ( IFNULL(cname,'') LIKE '%%%s%%' OR IFNULL(req_no,'') LIKE '%%%s%%' ) "%(search,search)
    sql+="ORDER BY apply_day DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id req_no apply_day cname ctype ctype_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取协议列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def agreementDetail(request):  
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    dept = 0
    pk = request.POST.get('pk','')
    # pk = 1000001
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    ctype = request.POST.get('cType','')
    # print request.POST
    if ctype=='AA':
        sql="""SELECT AA.id,IFNULL(AA.req_no,''),AA.apply_day,OP.cname,DP.cname,IFNULL(DP.id,0),IFNULL(MT.txt1,'') FROM assess_affirm AA 
               LEFT JOIN addr_book AB ON AB.id = AA.proj_p_id
               LEFT JOIN users_wx U ON U.addr_id = AB.id
               LEFT JOIN out_proj OP ON OP.id = AA.proj_id
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               WHERE U.usr_id=%s AND AA.id=%s
            """%(usr_id,pk)
    else:
        sql="""SELECT LC.id,IFNULL(LC.req_no,''),LC.apply_day,OP.cname,DP.cname,IFNULL(DP.id,0),IFNULL(MT.txt1,'') FROM labour_contract LC 
               LEFT JOIN addr_book AB ON AB.id = LC.teams_id
               LEFT JOIN users_wx U ON U.addr_id = AB.id
               LEFT JOIN out_proj OP ON OP.id = LC.proj_id
               LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
               LEFT JOIN mtc_t MT ON MT.id = TI.prj_property AND MT.type='XMSX'
               LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
               WHERE U.usr_id=%s AND LC.id=%s
            """%(usr_id,pk)
    # print sql
    rows,iN=db.select(sql)
    if iN>0:
        dept = rows[0][5]
    names = 'id req_no apply_day cname dept_name dept_id prj_property'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""SELECT IFNULL(U.usr_id,0),U.usr_name,DP.id,CONCAT(DP.cname,'第一负责人'),1
           FROM dept DP
           LEFT JOIN users U ON DP.header = U.usr_id
           WHERE DP.id = %s
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
    random_no = "%s_%s"%(time.time(),usr_id)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取协议详情成功",
        "data":%s,
        "leader":%s,
        "random_no":"%s"
        }        """%(L,leader,random_no)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def putComplaint(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
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
    level =  request.POST.get('level','') or 0
    ctype = request.POST.get('ctype','') or 'LC'
    now = int(time.time())

    complaintObject = MySQLdb.escape_string(complaintObject)
    memo = MySQLdb.escape_string(memo)
    if ctype=='AA':
        sql="""INSERT INTO complaint_detail(cid,ctime,aa_id,complaintObject,memo,leader,dept_id,random_no,level,ctype) 
               VALUES(%s,'%s',%s,'%s','%s',%s,%s,'%s',%s,'%s') 
            """%(usr_id,now,pk,complaintObject,memo,leader,dept_id,random_no,level,ctype)
    else:
        sql="""INSERT INTO complaint_detail(cid,ctime,lc_id,complaintObject,memo,leader,dept_id,random_no,level,ctype) 
               VALUES(%s,'%s',%s,'%s','%s',%s,%s,'%s',%s,'%s') 
            """%(usr_id,now,pk,complaintObject,memo,leader,dept_id,random_no,level,ctype)
    # print sql
    db.executesql(sql)
    sql="""SELECT id FROM complaint_detail WHERE random_no='%s'"""%random_no
    rows,iN=db.select(sql)
    pk=rows[0][0]
    sql="""INSERT INTO complaint_view_right(m_id,usr_id,utype) VALUES(%s,%s,'fw'),(%s,%s,'qy');
        """%(pk,usr_id,pk,leader)
    # print sql
    db.executesql(sql)

    mWxPushMsg_NewComplaint(request,pk,ctype)

    s = """
        {
        "errcode": 0,
        "errmsg": "上报投诉成功"
        }        """
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def myComplaint(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
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
           ,IFNULL(LC.req_no,AA.req_no)
           ,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d')
           ,IFNULL(OP.cname,OP1.cname)
           ,CD.memo,CD.status,IFNULL(VR.hasNew,0)
           ,CASE WHEN IFNULL(CD.finish,0)=1 THEN '已结案' ELSE IFNULL(F.cname,'新情况') END,UX.usr_name 
           FROM complaint_detail CD 
           LEFT JOIN labour_contract LC ON LC.id = CD.lc_id
           LEFT JOIN out_proj OP ON OP.id = LC.proj_id
           LEFT JOIN flow F ON F.ftype='ts' AND F.flow_id=CD.status
           LEFT JOIN complaint_view_right VR ON VR.m_id=CD.id AND VR.utype='fw' AND VR.usr_id=%s
           LEFT JOIN users_wx UX ON UX.usr_id = CD.cid
           LEFT JOIN assess_affirm AA ON AA.id = CD.aa_id
           LEFT JOIN out_proj OP1 ON OP1.id = AA.proj_id
           WHERE (CD.cid=%s  or %s = 447)  
        """%(usr_id,usr_id,usr_id)
    if situation !='':
        sql+="AND (CD.status='%s' "%(situation)
        if situation !='9':
            sql+="AND IFNULL(CD.finish,0) !=1 "
        else:
            sql+="OR IFNULL(CD.finish,0) =1 "
        sql+=")"
    if search !='':
        sql+="AND ( IFNULL(OP.cname,'') LIKE '%%%s%%' OR IFNULL(LC.req_no,'') LIKE '%%%s%%' OR IFNULL(AA.req_no,'') LIKE '%%%s%%' OR IFNULL(OP1.cname,'') LIKE '%%%s%%' ) "%(search,search,search,search)
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
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
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
    sql="""SELECT CD.id,IFNULL(LC.req_no,AA.req_no),IFNULL(LC.apply_day,AA.apply_day),IFNULL(OP.cname,OP1.cname),DP.cname,FROM_UNIXTIME(CD.ctime,'%%Y-%%m-%%d'),CD.complaintObject,U.usr_name,CD.memo,IFNULL(CD.random_no,''),IFNULL(CD.finish,0) 
           FROM complaint_detail CD 
           LEFT JOIN labour_contract LC ON LC.id = CD.lc_id
           LEFT JOIN out_proj OP ON OP.id = LC.proj_id
           LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
           LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
           LEFT JOIN users U ON U.usr_id = CD.leader
           LEFT JOIN assess_affirm AA ON AA.id = CD.aa_id
           LEFT JOIN out_proj OP1 ON OP1.id = AA.proj_id
           WHERE CD.id=%s
        """%(pk)
    rows,iN=db.select(sql)
    random_no=rows[0][9]
    names = 'id req_no apply_day proj_name dept_name ctime complaintObject usr_name memo random_no finish'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    sql ="""SELECT FP.id,FP.ctime,ifnull(FP.title,''),FP.fname,FP.file_size,FP.is_pic,'','','',YEAR(ctime),MONTH(ctime)
            FROM file_pic_lw FP
            WHERE FP.random_no='%s'
        """%(random_no)
    # print sql
    rows,iN = db.select(sql)
    file_list=[]
    for e in rows:
        e=list(e)
        url = "%s/fileUpload/file_down?fname=%s"%(data_url,e[3])
        e[6] = url
        e[7] = "%s/%s/%s/thumbnail/%s"%(attach_url,e[9],e[10],e[3])
        e[8] = "%s/fileUpload/del_attach_file?fname=%s&func=Progress"%(data_url,e[3])
        file_list.append(e)
        # print e[6]
    names = 'id ctime title fname file_size is_pic url thumbnail_url delete_url'.split()
    data = [dict(zip(names, d)) for d in file_list]
    LL = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT CF.id,U.usr_name,CF.ctime,F.cname,CF.memo
            FROM complaint_flow CF  
            LEFT JOIN users U ON U.usr_id = CF.cid
            LEFT JOIN flow F ON F.flow_id = CF.cur_flow_id AND F.ftype='ts'
            WHERE CF.m_id=%s
            ORDER BY CF.id DESC
        """%(pk)
    rows,iN = db.select(sql)
    names = 'id usr_name ctime cname memo'.split()
    data = [dict(zip(names, d)) for d in rows]
    flow = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql ="""SELECT MS.id,U.usr_name,MS.ctime,MS.memo
            FROM message MS  
            LEFT JOIN users U ON U.usr_id = MS.cid
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
        "errmsg": "获取协议详情成功",
        "data":%s,
        "files":%s,
        "flow":%s,
        "message":%s
        }        """%(L,LL,flow,message)
    return HttpResponseJsonCORS(s)

def closeFile(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
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
    sql="""SELECT cid FROM complaint_detail WHERE id=%s
    """%pk
    rows,iN=db.select(sql)
    cid = rows[0][0]
    if cid !=usr_id:
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    else:
        sql="""UPDATE complaint_detail SET finish=1,result=%s WHERE id=%s"""%(result,pk)
        db.executesql(sql)
        mWxPushMsg_Result(request,pk)
        s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
        return HttpResponseJsonCORS(s)

import httplib
def mWxPushMsg_Progress(id):   
    year=getToday()[:4]  
    L =Get_data_Progress(id)
    sToken =  read_access_token_lw()
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_lw)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_lw(body)
    
    cusrname = L[0]  
    proj_name = L[1]
    cur_progress = L[2]
    ctime = L[3]
    toUser = L[4]
    toUser += '|lishijie'
    sUrl='%s/complaint/login/login_qy?fid=uploadDetail&path=ProjPay&seq=%s'%(host_url,id)
    stitle = """进度款上报提醒"""
    description = """上报人:%s
上报项目：%s
上报进度：%s%%
上报日期：%s

请及时查阅，并协助申请进度款！"""%(cusrname,proj_name,cur_progress,ctime)
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

    """%(m_sAgentId_lw,stitle,sUrl,description)
    #print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode']    

    sql = "update progress_declare set push_time=now(),push_errcode=%s where id=%s"%(errcode,id)
    db.executesql(sql)
    errmsg = ddata.get('errmsg','')
    sql = """insert into progress_push_log (pd_id, recv_users, push_time, errcode, msg, iType) 
                 VALUES (%s, '%s', now(), %s, '%s', 0);"""%(id,toUser,errcode,errmsg)
    db.executesql(sql)
    return HttpResponseJsonCORS(errcode)

def Get_data_Progress(pk):
    L=[]
    sql="""SELECT UX.usr_name,OP.cname,pd.cur_progress,pd.ctime,U.login_id
            FROM progress_declare pd 
            LEFT JOIN users_wx UX ON UX.usr_id = pd.cid
            LEFT JOIN out_proj OP ON OP.id = pd.proj_id
            LEFT JOIN proj_user pu on pu.proj_id = pd.proj_id and pu.proj_role_id=1
            LEFT JOIN users U ON U.usr_id = pu.usr_id 
            WHERE pd.id = %s
            """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_NewComplaint(request,pk,ctype):   
    year=getToday()[:4]  
    L =Get_data_NewComplaint(request,pk,ctype)
    sToken =  read_access_token_lw()
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_lw)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_lw(body)
    file_id=L[0]
    # title = ToUnicode(L[1])
    
    cusrname = L[1]  #投诉人
    complaintObject = L[2] #投诉对象
    proj_name = L[3]
    toUser = L[4]
    if toUser=='gup':
        toUser+='|mengxp|zhongzhg|hanruiming'
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&seq=%s&must_reply=true'%(host_url,file_id)
    stitle = """新反映提醒"""
    surl = my_urlencode(sUrl)
    description = """【%s】发起了针对“%s”关于“%s”的情况反映，请及时查阅。"""%(cusrname,complaintObject,proj_name)
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

    """%(m_sAgentId_lw,stitle,sUrl,description)
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

def Get_data_NewComplaint(request,pk,ctype):
    L=[]
    if ctype=='AA':
        sql="""SELECT CD.id,UX.usr_name,CD.complaintObject,OP.cname,U.login_id
            FROM complaint_detail CD 
            LEFT JOIN users_wx UX ON UX.usr_id = CD.cid
            LEFT JOIN assess_affirm AA ON AA.id = CD.lc_id
            LEFT JOIN out_proj OP ON OP.id = AA.proj_id
            LEFT JOIN users U ON U.usr_id = CD.leader
            WHERE CD.id = %s
            """%(pk)
    else:
        sql="""SELECT CD.id,UX.usr_name,CD.complaintObject,OP.cname,U.login_id
            FROM complaint_detail CD 
            LEFT JOIN users_wx UX ON UX.usr_id = CD.cid
            LEFT JOIN labour_contract LC ON LC.id = CD.lc_id
            LEFT JOIN out_proj OP ON OP.id = LC.proj_id
            LEFT JOIN users U ON U.usr_id = CD.leader
            WHERE CD.id = %s
            """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_Result(request,pk):   
    year=getToday()[:4]  
    L,toUser =Get_data_Result(request,pk)
    sToken =  read_access_token_lw()
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_lw)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_lw(body)
    file_id=L[0]
    # title = ToUnicode(L[1])
    
    cusrname = L[1]  #投诉人
    complaintObject = L[2] #投诉对象
    proj_name = L[3]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&seq=%s&must_reply=true'%(host_url,file_id)
    stitle = """新反映结案提醒"""
    surl = my_urlencode(sUrl)
    description = """针对“%s”关于“%s”的劳务情况反映已结案。"""%(complaintObject,proj_name)
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

    """%(m_sAgentId_lw,stitle,sUrl,description)
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
        FROM complaint_detail CD 
        LEFT JOIN users_wx UX ON UX.usr_id = CD.cid
        LEFT JOIN labour_contract LC ON LC.id = CD.lc_id
        LEFT JOIN out_proj OP ON OP.id = LC.proj_id
        LEFT JOIN users U ON U.usr_id = CD.leader
        LEFT JOIN assess_affirm AA ON AA.id = CD.aa_id
        LEFT JOIN out_proj OP1 ON OP1.id = AA.proj_id
        WHERE CD.id = %s
        """%(pk)
    rows,iN = db.select(sql)
    L=rows[0]

    toUser=''
    sql="""SELECT IFNULL(U.login_id,'') FROM complaint_view_right VR 
        LEFT JOIN users U ON U.usr_id=VR.usr_id
        WHERE VR.m_id = %s and VR.utype='qy'
        """%(pk)
    rows,iN = db.select(sql)
    for e in rows:
        toUser+='%s|'%(e[0])
    return L,toUser  