# -*- coding: utf-8 -*-
# 登录验证
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,byerp,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,host_url,my_urlencode,read_access_token_common,write_access_token_common'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,checkSession,data_url,m_sCorpID,m_sCorpSecret,m_sAgentId_gy,m_sCorpSecret_gy,AppId_gy,AppSecret_gy,template_id_msg_gy,template_id_result_gy'%prj_name) 
import httplib
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
import datetime
from HW_DT_TOOL                 import getToday
import MySQLdb
#testid = 2110
testid = 2029
import emoji

remote_db = byerp
def getPurchasingList(request):
    usr_id_qy = request.session.get('usr_id_qy') or testid
    print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    users = getViewUserIds()
    if str(usr_id_qy) not in users :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    sql="""select cg.id,cg.sn,op.cname,su.cname,u.usr_name,u.pic,cg.ctime,cg.status from _m1501_cgdd cg
           left join out_proj op on op.id = cg.proj_id
           left join suppliers su on su.id = cg.sup_id
           left join users u on u.usr_id = cg.cid
           where cg.cid = %s 
        """%(usr_id_qy)
    if search !='':
        sql+="AND ((IFNULL(cg.sn,'') LIKE '%%%s%%' ) or (IFNULL(op.cname,'') LIKE '%%%s%%' ) or (IFNULL(su.cname,'') LIKE '%%%s%%' ))"%(search,search,search)
    if situation !='':
        sql+="AND (cg.status='%s') "%(situation)
    sql+="ORDER BY cg.id DESC"
    #print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    names = 'id sn proj_name sup_name usr_name head_pic ctime status'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取采购订单列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def savePurchasing(request):
    usr_id_qy = request.session.get('usr_id_qy') or testid
    if usr_id_qy == 0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    print data_list
    pk = data_list.get('pk','')
    cg_type = data_list.get('cg_type') or '1'
    is_gycg = data_list.get('is_gycg','')
    gy_company = data_list.get('gy_company') or 'NULL'
    is_jzgy = data_list.get('is_jzgy') or 'NULL'
    jzgy_name = data_list.get('jzgy_name') or 'NULL'
    cg_zt = data_list.get('cg_zt','')
    pay_way = data_list.get('pay_way','')
    sh_way = data_list.get('sh_way','')
    cg_price = data_list.get('cg_price','')
    busi_usr_id = data_list.get('busi_usr_name','')
    memo = data_list.get('memo','')
    has_cght = data_list.get('has_cght') or 'NULL'
    cght_no = data_list.get('cght_no','')

    if pk == '':
        sql = """insert into _m1501_cgdd (sn,proj_id,ctr_id,sup_id,cght,deliver_date,memo,is_gyl,gyl,cgzt,random_no,cid,cusrname,status,ctime) 
                 VALUES ('%s', %s, %s, %s, %s, '%s', '%s', %s, %s, %s, '%s', %s, '%s', 0, now());
              """%(pk,cg_type,ghf,js_way,is_gycg,gy_company,is_jzgy,jzgy_name,cg_zt,pay_way,sh_way
                   ,cg_price,busi_usr_id,memo)
    else:
        sql = """UPDATE _m1501_cgdd set `ghf`='%s', `js_way`='%s', `is_gycg`='%s', `gy_company`=%s, `is_jzgy`=%s, `jzgy_name`=%s, `cg_zt`='%s', `pay_way`='%s', `sh_way`='%s'
                            ,cg_price = '%s', `busi_usr_id`='%s', memo='%s', `utime`=now(),status = 0
                 where id=%s;
              """%(ghf,js_way,is_gycg,gy_company,is_jzgy,jzgy_name,cg_zt,pay_way,sh_way
                   ,cg_price,busi_usr_id,memo,pk)
    print ToGBK(sql)
    #db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "保存成功",
        "pk":%s
        }        """%(pk)
    return HttpResponseJsonCORS(s)

def invalidPurchasing(request):
    usr_id_qy = request.session.get('usr_id_qy') or testid
    if usr_id_qy == 0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    sql = """UPDATE _m1501_cgdd set status = -1,status1=-1 where id=%s;
              """%(pk)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "作废成功"
        }        """
    return HttpResponseJsonCORS(s)

def deletePurchasing(request):
    usr_id_qy = request.session.get('usr_id_qy') or testid
    if usr_id_qy == 0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    sql = """delete from _m1501_cgdd where id=%s;
              """%(pk)
    print ToGBK(sql)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "删除成功"
        }        """
    return HttpResponseJsonCORS(s)

def getAuditList(request):
    usr_id_qy = request.session.get('usr_id_qy') or testid
    #print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    users = getViewUserIds()
    if str(usr_id_qy) not in users:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    sql="""select cg.id,cg.sn,op.cname,su.cname,u.usr_name,cg.cgd_no,cg.ctime,cg.status1 from _m1501_cgdd cg
           left join out_proj op on op.id = cg.proj_id
           left join suppliers su on su.id = cg.sup_id
           left join users u on u.usr_id = cg.cid
           where cg.cid = %s  and cg.status1 != 0
        """%(usr_id_qy)
    if search !='':
        sql+="AND ((IFNULL(cg.sn,'') LIKE '%%%s%%' ) or (IFNULL(op.cname,'') LIKE '%%%s%%' ) or (IFNULL(su.cname,'') LIKE '%%%s%%' ))"%(search,search,search)
    if situation !='':
        sql+="AND (cg.status1='%s') "%(situation)
    sql+="ORDER BY cg.id DESC"
    print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    names = 'id sn proj_name sup_name usr_name cgd_no ctime status'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def audit(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    users = getViewUserIds()
    if str(usr_id_qy) not in users:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)

    id = request.POST.get('id','')
    pass1 = request.POST.get('pass','') 
    cont = request.POST.get('cont','')
    cont = MySQLdb.escape_string(cont)
    if str(pass1) == '1':
        sql = """select mx.id,ifnull(cl_id,''),cl_code,cl_type,cl_name,cl_unit,cl_spec,cl_model,cl_brand,mt.type_code,cg.cid,cg.cusrname,mx.price
                 from _m1501_cgdd_list mx
                 left join _m1501_cgdd cg on mx.m_id = cg.id
                 left join mat_type mt on mx.cl_type = mt.id
                 where mx.m_id=%s"""%(id)
        rows,iN = db.select(sql)
        for e in rows:
            cl_id = e[1]
            if cl_id == '':    #未与主系统同步的材料明细
                code = e[2]
                if code != '':    #主系统已存在的材料
                    sql = "select id from mat where code='%s' order by id desc"%(code)
                    rows,iN = remote_db.select(sql)
                    if iN>0:
                        cl_id = rows[0][0]
                if cl_id == '':             #主系统中没有的材料
                    sql = "select isnull(matcodenum,0) from mat_type where type_code = '%s'"%(e[9])
                    #print sql
                    rows,iN = remote_db.select(sql)
                    if iN>0:
                        code = rows[0][0]
                        if code == '':
                            maxnum = 1
                            code = "%s-00001"%(e[9])
                        else:
                            maxnum = int(code)+1
                            maxnum = str(maxnum).zfill(5)
                            code = "%s-%s"%(e[9],maxnum)
                    else:
                        maxnum = 1
                        code = "%s-00001"%(e[9])
                    sql = "update mat_type set matcodenum = %s where type_code = '%s'"%(maxnum,e[9])
                    remote_db.executesql(sql)
                    #print code
                    sql="""INSERT INTO mat
                           ([cname],[code],[type],[sepc],brand
                           ,[unit],[avg_price],[max_price],[min_price],[MATYP]
                           ,[size],[meno],[status]
                           ,[cid],[cusrname],[ctime])
                        VALUES
                           ('%s','%s','%s','%s','%s'
                           ,%s,%s,%s,%s,NULL
                           ,'%s','供应商平台添加',2
                           ,%s,'%s',getdate())
                        """%(e[4],code,e[9],e[7],e[8]
                          ,e[5],e[12],e[12],e[12]
                          ,e[6],e[10],e[11])
                    remote_db.executesql(sql)
                    sql = "select id from mat where code='%s'"%code
                    rows,iN = remote_db.select(sql)
                    if iN>0:
                        cl_id = rows[0][0]
                     
                if cl_id != '':           
                    sql = "update _m1501_cgdd_list set cl_id = %s,cl_code='%s' where id=%s"%(cl_id,code,e[0])
                    print sql
                    db.executesql(sql)
        sql = "update _m1501_cgdd set status1=2,status=5,audit_time=now() where id = %s"%(id)
        db.executesql(sql)
    else:
        sql = "update _m1501_cgdd set status1=5,status=4,audit_time=now(),audit_cont='%s' where id = %s"%(cont,id)
        db.executesql(sql)
        sql = """select op.cname,cg.sup_id,cg.sn from _m1501_cgdd cg
                 left join out_proj op on cg.proj_id = op.id
                 where cg.id=%s"""%(id)
        rows,iN = db.select(sql)
        if iN > 0:
            proj_name = rows[0][0]
            sup_id = rows[0][1]
            sn = rows[0][2]
            sql = """select GROUP_CONCAT(u.openid) from users_gy u 
                     left join addr_book ab on u.addr_id = ab.id
                     where ab.sup_id = %s and u.status = 1"""%(sup_id)
            rows1,iN1 = db.select(sql)
            users = rows1[0][0]
            mWxPushMsg_nopass(id,users,sn,proj_name,cont)
    s = """
        {
        "errcode": 0,
        "errmsg": "审核成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def getCgdInfo(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.GET.get('pk','')
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    
    
    sql="""SELECT MS.id, MS.cg_type, MS.ghf, MS.js_way, MS.is_gycg, MS.gy_company, MS.is_jzgy, MS.jzgy_name, MS.cg_zt, MS.pay_way, MS.sh_way
                  ,MS.cg_price ,  MS.busi_usr_id, MS.memo, MS.status, MS.ctime , MS.has_cght, MS.cght_no
                  ,ifnull(flow_opt,''),flow_memo,ifnull(flow_next_flow,''),ifnull(flow_next_dept,''),ifnull(flow_next_role,''),ifnull(flow_next_usr,'')
        FROM _m1501_cgsq MS 
        left join _m1501_cgdd cg on cg.id = ms.id
        WHERE MS.id=%s
        """%pk
    # print sql
    rows,iN=db.select(sql)
    if iN == 0:
        sql="""SELECT cg.id, '', '', '', cg.is_gyl, cg.gyl, '', '', cg.cgzt, '', ''
                  ,case ifnull(cg.is_gyl,0) when 0 then cg.cg_amount else cg.cg_amount*1.005 end, cg.cid , '', 0, '', case ifnull(cg.cght,0) when 0 then 0 else 1 end,ht.req_no
                  ,'','','','','',''
        FROM _m1501_cgdd cg
        left join prj_mat_buy_ht ht on ht.id = cg.cght
        WHERE cg.id=%s
        """%pk
        rows,iN=db.select(sql)
    L =[]
    for e in rows:
        L1 = list(e)
        cid = e[12]
        status = e[14]
        flow_opt = e[18]
        flow_next_flow = e[20]
        flow_next_dept = e[21]
        flow_next_role = e[22]
        flow_next_usr = e[23]
        if flow_next_flow != '':
            if flow_next_dept != '':
                L1[20],L1[21],L1[23] = getFlowAll(pk,usr_id_qy,'cgd',flow_next_flow,flow_next_dept,flow_next_usr)
            else:
                L1[20],L1[22],L1[23] = getFlowAll(pk,usr_id_qy,'cgd',flow_next_flow,flow_next_role,flow_next_usr)
        L.append(L1)
    names = 'id cg_type ghf js_way is_gycg gy_company is_jzgy jzgy_name cg_zt pay_way sh_way cg_price busi_usr_name memo status ctime has_cght cght_no flow_opt flow_memo flow_next_flow flow_next_dept flow_next_role flow_next_usr'.split()
    data = [dict(zip(names, d)) for d in L]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    if cid==usr_id_qy and status == 0:
        canEdit = 1
    else:
        canEdit = 0
        
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s,
        "canEdit":%s
        }        """%(L,canEdit)
    return HttpResponseJsonCORS(s)
   
def saveCgd(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    data = request.POST.get('data','')
    data_list = json.loads(data)
    print data_list
    pk = data_list.get('pk','')
    cg_type = data_list.get('cg_type') or '1'
    ghf = 1
    js_way = 1
    is_gycg = data_list.get('is_gycg','')
    gy_company = data_list.get('gy_company') or 'NULL'
    is_jzgy = data_list.get('is_jzgy') or 'NULL'
    jzgy_name = data_list.get('jzgy_name') or 'NULL'
    cg_zt = data_list.get('cg_zt','')
    pay_way = data_list.get('pay_way','')
    sh_way = data_list.get('sh_way','')
    sh_way = MySQLdb.escape_string(sh_way)
    cg_price = data_list.get('cg_price','')
    busi_usr_id = data_list.get('busi_usr_name','')
    memo = data_list.get('memo','')
    memo = MySQLdb.escape_string(memo)
    has_cght = data_list.get('has_cght') or 'NULL'
    cght_no = data_list.get('cght_no','')

    sql = "select id from _m1501_cgsq where id = %s"%(pk)
    rows,iN = db.select(sql)
    if iN == 0:
        sql = """INSERT INTO _m1501_cgsq (`id`, `cg_type`, `ghf`, `js_way`, `is_gycg`, `gy_company`, `is_jzgy`, `jzgy_name`, `cg_zt`, `pay_way`, `sh_way`
                            ,cg_price , `busi_usr_id`, memo, `status`, `ctime`) 
                 VALUES (%s, '%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', 0, now());
              """%(pk,cg_type,ghf,js_way,is_gycg,gy_company,is_jzgy,jzgy_name,cg_zt,pay_way,sh_way
                   ,cg_price,busi_usr_id,memo)
    else:
        sql = """UPDATE _m1501_cgsq set `ghf`='%s', `js_way`='%s', `is_gycg`='%s', `gy_company`=%s, `is_jzgy`=%s, `jzgy_name`=%s, `cg_zt`='%s', `pay_way`='%s', `sh_way`='%s'
                            ,cg_price = '%s', `busi_usr_id`='%s', memo='%s', `utime`=now(),status = 0
                 where id=%s;
              """%(ghf,js_way,is_gycg,gy_company,is_jzgy,jzgy_name,cg_zt,pay_way,sh_way
                   ,cg_price,busi_usr_id,memo,pk)
    print ToGBK(sql)
    db.executesql(sql)

    sql = "update _m1501_cgdd set status1=2 where id = %s"%(pk)
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "暂存成功"
        }        """
    return HttpResponseJsonCORS(s)

def replaceStr(str):
    str = str.replace(u'\xd8','Ø')
    return str

def pushCgd(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    data = request.POST.get('data','')
    data_list = json.loads(data)
    pk = data_list.get('pk','')
    flow_opt = data_list.get('flow_opt') or 0
    flow_memo = data_list.get('flow_memo','')
    flow_memo = MySQLdb.escape_string(flow_memo)
    flow_next_flow = data_list.get('flow_next_flow') or 'NULL'
    flow_next_dept = data_list.get('flow_next_dept') or 'NULL'
    flow_next_role = data_list.get('flow_next_role') or 'NULL'
    flow_next_usr = data_list.get('flow_next_usr') or 'NULL'

    is_send = request.GET.get('is_send','')
    is_send = is_send.replace('/','')

    cg_type = data_list.get('cg_type') or '1'
    ghf = 1
    js_way = 1
    is_gycg = data_list.get('is_gycg','')
    gy_company = data_list.get('gy_company') or 'NULL'
    is_jzgy = data_list.get('is_jzgy') or 'NULL'
    jzgy_name = data_list.get('jzgy_name') or 'NULL'
    cg_zt = data_list.get('cg_zt','')
    pay_way = data_list.get('pay_way','')
    sh_way = data_list.get('sh_way','')
    sh_way = MySQLdb.escape_string(sh_way)
    cg_price = data_list.get('cg_price','')
    busi_usr_id = data_list.get('busi_usr_name','')
    memo = data_list.get('memo','')
    memo = MySQLdb.escape_string(memo)
    has_cght = data_list.get('has_cght') or 'NULL'
    cght_no = data_list.get('cght_no','')

    sql = "select id from _m1501_cgsq where id = %s"%(pk)
    rows,iN = db.select(sql)
    if iN == 0:
        sql = """INSERT INTO _m1501_cgsq (`id`, `cg_type`, `ghf`, `js_way`, `is_gycg`, `gy_company`, `is_jzgy`, `jzgy_name`, `cg_zt`, `pay_way`, `sh_way`
                            ,cg_price , `busi_usr_id`, memo, `status`, `ctime`) 
                 VALUES (%s, '%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', 0, now());
              """%(pk,cg_type,ghf,js_way,is_gycg,gy_company,is_jzgy,jzgy_name,cg_zt,pay_way,sh_way
                   ,cg_price,busi_usr_id,memo)
    else:
        sql = """UPDATE _m1501_cgsq set `ghf`='%s', `js_way`='%s', `is_gycg`='%s', `gy_company`=%s, `is_jzgy`=%s, `jzgy_name`=%s, `cg_zt`='%s', `pay_way`='%s', `sh_way`='%s'
                            ,cg_price = '%s', `busi_usr_id`='%s', memo='%s', `utime`=now(),status = 0
                 where id=%s;
              """%(ghf,js_way,is_gycg,gy_company,is_jzgy,jzgy_name,cg_zt,pay_way,sh_way
                   ,cg_price,busi_usr_id,memo,pk)
    print ToGBK(sql)
    db.executesql(sql)

    sql = "update _m1501_cgdd set status1=2 where id = %s"%(pk)
    db.executesql(sql)

    #sql = """update _m1501_cgsq set flow_opt=%s,flow_memo='%s',flow_next_flow=%s,flow_next_dept=%s,flow_next_role=%s,flow_next_usr=%s,flow_send_time=now() where id=%s
    #      """%(flow_opt,flow_memo,flow_next_flow,flow_next_dept,flow_next_role,flow_next_usr,pk)
    #db.executesql(sql)

    if is_send == '1':
        sql = "select usr_name,dept_id from users where usr_id = %s"%(usr_id_qy)
        rows,iN=db.select(sql)
        usr_name = rows[0][0]
        dept_id = rows[0][1]
        sql="""SELECT MS.id, MS.cg_type, MS.ghf, MS.js_way, MS.is_gycg, MS.gy_company, MS.is_jzgy, MS.jzgy_name, MS.cg_zt
                  , MS.pay_way, MS.sh_way, cg.cg_amount ,  MS.busi_usr_id, u1.usr_name, MS.memo 
                  ,ifnull(MS.flow_opt,''),MS.flow_memo,ifnull(MS.flow_next_flow,''),ifnull(MS.flow_next_dept,''),ifnull(MS.flow_next_role,''),ifnull(MS.flow_next_usr,'')
                  ,cg.proj_id,op.cname,su.id,su.cname,case ifnull(ht.id,'') when '' then 0 else 1 end,ht.id,ht.req_no
                  ,cg.audit_time,cg.deliver_date,MS.cg_price
                  ,sg.id,sg.cname,op.gc_no,sg.code
                  ,case MS.cg_zt when 1 then '深圳市宝鹰建设集团股份有限公司' when 2 then '普宁市宝鹰供应链管理有限公司' else '深圳市中建南方建设集团有限公司' end
                  ,cg.cgd_no,ifnull(cg.cgd_gwid,''),ifnull(cg.cgd_id,'')
        FROM _m1501_cgsq MS 
        left join _m1501_cgdd cg on ms.id = cg.id
        left join out_proj op on cg.proj_id = op.id
        left join contract_sg_file sg on sg.id = cg.ctr_id
        left join suppliers su on su.id = cg.sup_id
        left join prj_mat_buy_ht ht on ht.id = cg.cght
        left join users u1 on u1.usr_id = MS.busi_usr_id
        WHERE MS.id=%s
        """%pk
        print ToGBK(sql)
        rows,iN=db.select(sql)
        L = list(rows[0])
        #保存公文表
        title = '采购单申请：%s'%(L[22])
        m_id = L[-1]
        gw_id = L[-2]
        code = L[-3]
        is_gyl = L[4]
        if is_gyl == 1:
            scope = 1.005
        else: 
            scope = 1
        proj_id = L[21]
        if gw_id == '':
            gw_id = add_save_master('cgd',title,usr_id_qy,usr_name,dept_id,flow_next_usr)
            t=time.time()
            date_ary=time.localtime(t)
            x=time.strftime("WCG%Y%m%d",date_ary)
        
            sql = "select ifnull(max(last_code),'') from code_lib where last_code like '%s%%' and src = 'D017'"%(x)
            rows,iN = db.select(sql)
            if iN>0:
                code = rows[0][0]
                if code == '':
                    code = "%s001"%(x)
                    maxnum = 1
                else:
                    code = code.replace("%s"%x,'')
                    maxnum = int(code.strip())+1
                    maxnum1 = str(maxnum).zfill(3)
                    code = "%s%s"%(x,maxnum1)
            else:
                code = "%s001"%(x)
                maxnum = 1
            sql = "update code_lib set last_code='%s',maxnum=%s where src = 'D017'"%(code,maxnum)
            db.executesql(sql)

            #保存主表单
            sql = """INSERT INTO [prj_mat_buy](
                            [Gw_id],[buy_type],[Prj_id],[gc_name],[Sup_id],[sp_name],
                            [ifht],[htcode],[ht_no],[Req_no],[Order_date],
                            [Ship_date],[Ship_type],[Totay_price],[Buyer],[buyer_name],[Memo],
                            [ctr_id],[ctr_name],[gc_no],[ctr_code],[GHF],[JSFS],
                            [pay_type],[is_from_hxsh],[Supply],[act_total],[cgzt],[cgzt_txt],
                            [cid],[cusrname],[ctime])
                    VALUES(%s,%s,%s,'%s',%s,'%s'
                        ,%s,%s,'%s','%s','%s','%s'
                        ,'%s',%s,%s,'%s','%s'
                        ,%s,'%s','%s','%s',%s,%s
                        ,%s,%s,%s,%s,%s,'%s'
                        ,%s,'%s',getdate())
                """ %(gw_id,L[1],L[21],L[22],L[23],L[24]
                       ,L[25],L[26] or 'NULL',L[27] or '',code,L[28]
                       ,L[29],L[10],L[30],L[12],L[13],L[14]
                       ,L[31] or 'NULL',L[32] or '',L[33],L[34] or '',L[2],L[3]
                       ,L[9],L[4],L[5] or 'NULL',L[11],L[8],L[35] or 'NULL'
                       , usr_id_qy,usr_name)
            print ToGBK(sql)
            remote_db.executesql(sql)
        
            sql = "select id from prj_mat_buy where gw_id=%s"%(gw_id)
            rows,iN = remote_db.select(sql)
            if iN>0: 
                m_id = rows[0][0]
            else:
                m_id = 0
            #更新公文表
            sql = "UPDATE gw_doc set proj_id=%s,sn='%s' where id=%s"%(proj_id,code,gw_id)
            remote_db.executesql(sql)
            #材料明细表
            sql = "select cl_id,cl_code,cl_name,cl_spec,cl_model,cl_brand,cl_unit,qty,price,ifnull(amount,0),id from _m1501_cgdd_list where m_id = %s order by sort"%(pk)
            rows,iN=db.select(sql)
            i = 0           
            for e in rows:
                random_no = "%s_%s"%(gw_id,i)
                cl_name = e[2]
                cl_spec = e[3]
                cl_model = e[4]
                cl_brand = e[5]
                #cl_model = replaceStr(cl_model)
                #print cl_model

                sql = """INSERT INTO [prj_mat_buy_list]
               ([gw_id]
               ,[M_id]
               ,[proj_id]
               ,[Mat_id]
               ,[mat_code]
               ,[Mat_name]
               ,[Spec]
               ,[Model]
               ,[Brand]
               ,[unit_id]
               ,[Count]
               ,[act_unit_price]
               ,[act_total_price]
               ,[Unit_price]
               ,[Total_price]
               ,[cid]
               ,[ctime],random_no)
            VALUES
               (%s,%s,%s,%s,'%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,getdate(),'%s')
              """%(gw_id,m_id,proj_id,e[0],e[1],cl_name,cl_spec,cl_model,cl_brand,e[6],e[7],e[8],e[9],float(e[8])*scope,float(e[9])*scope,usr_id_qy,random_no)
                print ToGBK(sql)
                remote_db.executesql(sql)
                sql = "select id from prj_mat_buy_list where random_no='%s'"%(random_no)
                rows,iN = remote_db.select(sql)
                if iN>0:mxid=rows[0][0]
                else:mxid=0
                sql = "update _m1501_cgdd_list set cgd_mxid = %s where id=%s"%(mxid,e[-1])
                db.executesql(sql)
                i += 1
            #流程处理
            #mForm_2_save(gw_id,flow_next_flow,flow_next_dept,flow_next_role,flow_next_usr,flow_memo,usr_id_qy,usr_name,dept_id)

        sql = "update _m1501_cgsq set status=1,gw_id=%s where id = %s"%(gw_id,pk)
        db.executesql(sql)
        sql = "update _m1501_cgdd set status1=4,cgd_no='%s',cgd_gwid=%s,cgd_id=%s where id = %s"%(code,gw_id,m_id,pk)
        print sql
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "发送成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def searchUsers(request):
    L=[]
    search = request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    usr_id = request.POST.get('usr_id','')
    if usr_id != '':
        sql="""select usr_name from users 
           where usr_id = %s
            """%usr_id
        lT,iN=db.select(sql)
        if iN>0:
            usr_name = lT[0][0]
        else:
            usr_name = ''
        s = """
            {
            "errcode":0,
            "errmsg":"",
            "data":"%s"
            }
            """%(usr_name)
        #print ToGBK(s)
        return HttpResponseCORS(request,s)
    if search != '':         
        sql="""select usr_id,usr_name,0,D.cname from users U
           left join dept D on D.id = U.dept_id
           where usr_name like '%%%s%%' and U.status=1 
           order by usr_id asc limit 10
            """%search
        lT,iN=db.select(sql)
    else:
        lT = []
    for e in lT:
        txt=e[1]
        if txt == search:b=1
        else:b=0
        L.append([e[0],e[1],b,e[3]])
    names = 'value label checked tips'.split()
    data = [dict(zip(names, d)) for d in L]

    #options =['',False]
    #options[0] = data
    #options[1] = False
    #names = 'options include_other_option'.split()
    #L1 = dict(zip(names, options))
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
            {
            "errcode":0,
            "errmsg":"",
            "data":%s
            }
            """%(data)
        #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getFlowAll(pk,usr_id,type,sel_flow,sel_dept,sel_usr):
    if type == 'cgd':
        gw_type = '154'  # 获取的为 gw_type 表中的 ID 在子类中定义
        flow_id = '592'  # 获取的为 gw_flow_def 表中的ID 在子类中定义
    elif type == 'rkd':
        gw_type='307'  # 获取的为 gw_type 表中的 ID 在子类中定义
        flow_id='1730'  # 获取的为 gw_flow_def 表中的ID 在子类中定义
    else:
        gw_type='0' 
        flow_id='0' 
    print sel_flow,sel_dept,sel_usr
    L,sel_flow = getNextFlow(gw_type,flow_id,sel_flow)
    names = 'value label checked sel_type'.split()
    flow_data = [dict(zip(names, d)) for d in L]
    L,sel_dept = getDeptByFlow(gw_type,sel_flow,sel_dept)
    names = 'value label checked'.split()
    dept_data = [dict(zip(names, d)) for d in L]
    L = get_usr(usr_id,pk,sel_flow,sel_dept,sel_usr)
    names = 'value label checked'.split()
    usr_data = [dict(zip(names, d)) for d in L]
    print flow_data
    return flow_data,dept_data,usr_data

def getFlow(request):
    type = request.POST.get('type') or request.GET.get('type','')
    if type == 'cgd':
        gw_type = '154'  # 获取的为 gw_type 表中的 ID 在子类中定义
        flow_id = '592'  # 获取的为 gw_flow_def 表中的ID 在子类中定义
    elif type == 'rkd':
        gw_type='307'  # 获取的为 gw_type 表中的 ID 在子类中定义
        flow_id='1730'  # 获取的为 gw_flow_def 表中的ID 在子类中定义
    else:
        gw_type='0' 
        flow_id='0'  

    L,sel_flow_id = getNextFlow(gw_type,flow_id,'')
    names = 'value label checked sel_type'.split()
    data = [dict(zip(names, d)) for d in L]
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
            {
            "errcode":0,
            "errmsg":"",
            "data":%s
            }
            """%(data)
        #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getNextFlow(type_id,cur_flow_id,sel_flow_id):
    sql=""" SELECT DISTINCT FD.id, FD.cname,FD.sort,ISNULL(FD.repeat,0),isnull(FD.usr_sel_type,0)
                    FROM gw_flow_def FD
                    LEFT JOIN gw_type T ON T.id=FD.type_id AND run_mode = 2 AND ISNULL(re_id,0) IN (0,%s)
                    LEFT JOIN gw_flow_def PD ON PD.id = ISNULL(FD.re_id,0)
                    WHERE
                    (
                        FD.id IN (
                          SELECT rD.id FROM gw_flow_def rD 
                          LEFT JOIN gw_flow_def pD ON pD.id = rD.re_id 
                          LEFT JOIN gw_flow_def sD ON sD.re_id = rD.id 
                          WHERE (pD.id = %s OR sD.id = %s) 
                        ) OR
                        FD.id IN(
                          SELECT rD.id FROM gw_flow_def rD 
                          LEFT JOIN gw_flow_rule R ON R.rule_flow_id = rD.id AND R.dir = 'P'
                          LEFT JOIN gw_flow_def sD ON sD.re_id = R.flow_id 
                          LEFT JOIN gw_flow_def pD ON pD.id = R.flow_id  
                          WHERE sD.id = %s OR pD.id = %s 
                        ) OR
                        T.id=%s
                    )
                    AND FD.type_id = %s AND FD.id != %s AND (ISNULL(FD.re_id,0) = 0 OR PD.repeat = 1) 
                    ORDER BY FD.sort
                """%(cur_flow_id,cur_flow_id,cur_flow_id,cur_flow_id,cur_flow_id,type_id,type_id,cur_flow_id)
    print sql
    rows,iN = remote_db.select(sql)
    L=[]
    for e in rows:
        if str(e[0]) == str(sel_flow_id):b=1
        else:b=0
        L.append([e[0],e[1],b,e[4]])

    if len(L)==1:
        sel_flow_id=L[0][0]
        L[0][2]='1'

    return L,sel_flow_id
    
def getFlowDept(request):
    type = request.POST.get('type') or request.GET.get('type','')
    flow_id = request.POST.get('flow_id') or request.GET.get('flow_id','')
    if type == 'cgd':
        gw_type = '154'  # 获取的为 gw_type 表中的 ID 在子类中定义
    elif type == 'rkd':
        gw_type='307'  # 获取的为 gw_type 表中的 ID 在子类中定义
    else:
        gw_type='0' 

    L,sel_dept = getDeptByFlow(gw_type,flow_id,'')
    names = 'value label checked'.split()
    data = [dict(zip(names, d)) for d in L]
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
            {
            "errcode":0,
            "errmsg":"",
            "data":%s
            }
            """%(data)
        #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getDeptByFlow(type_id,flow_id,sel_dept):
    sql="SELECT usr_sel_type,isnull(def_dept,0),isnull(def_usr_id,0) FROM gw_flow_def WHERE id=%s ORDER BY sort"%(flow_id)
    lT,iN = remote_db.select(sql)
    sel_type=lT[0][0]
    def_dept=lT[0][1]
    def_user=lT[0][2]
    if str(sel_type) in ['8','9']: #角色 
        sql=" select distinct r.role_id,r.role_name from gw_fr_role_sel f left join roles r on r.role_id = f.role_id where f.m_id = %s "%flow_id
    elif str(sel_type) in ['2','3']:  #2：限定部门及人  3：限定部门
        sql="""SELECT DISTINCT FUS.dept_id,D.cname,isnull(D.parent_id,0)
               FROM gw_fr_usr_sel FUS
               LEFT JOIN dept D ON D.id=FUS.dept_id
               WHERE FUS.m_id=%s  AND D.id!=1
            """%(flow_id)
    elif str(sel_type) in ['4','5']:  #4:限定于作者部门的人  5:限定于作者
        sql="""
            SELECT DISTINCT D.id,D.cname,isnull(D.parent_id,0)
            FROM gw_doc GD
            LEFT JOIN users U ON U.usr_id=GD.cid
            LEFT JOIN dept D ON D.id=U.dept_id
            WHERE GD.id=%s AND D.id!=1
            """%pk
    elif str(sel_type) in ['10']: #限定作者部门的人  限定作者部门领导
        sql="""
            SELECT ISNULL(G.form_dept_id,0),ISNULL(U.dept_id,0)
            FROM gw_doc G
            LEFT JOIN users U ON U.usr_id = G.cid
            WHERE G.id = %s
            """%pk
        lT,iN = remote_db.select(sql)
        if lT[0][0] != 0:
            deptid=lT[0][0]
        else:
            deptid=lT[0][1]
        sql="""
            select isnull(u1.usr_id,0),isnull(u2.usr_id,0),isnull(u3.usr_id,0),isnull(u4.usr_id,0),isnull(u5.usr_id,0),isnull(u6.usr_id,0)
            ,isnull(u7.usr_id,0),isnull(u8.usr_id,0),isnull(u9.usr_id,0),isnull(u10.usr_id,0),isnull(u11.usr_id,0),isnull(u12.usr_id,0),isnull(u13.usr_id,0)            
            FROM dept D1
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND ISNULL(D1.true_dept_id,0) = 0)
            left join users u1 on u1.usr_id = d2.header
            left join users u2 on u2.usr_id = d2.second_header
            left join users u3 on u3.usr_id = d2.proxy_header
            left join users u4 on u4.usr_id = d2.sub_director
            left join users u5 on u5.usr_id = d2.fzcn
            left join users u6 on u6.usr_id = d2.fzkj
            left join users u7 on u7.usr_id = d2.cl_acc
            left join users u8 on u8.usr_id = d2.[lw_acc]
            left join users u9 on u9.usr_id = d2.[xmfy_acc]
            left join users u10 on u10.usr_id = d2.[byj_acc]
            left join users u11 on u11.usr_id = d2.[zg_acc]
            left join users u12 on u12.usr_id = d2.[cl_zgkj]
            left join users u13 on u13.usr_id = d2.[fy_zgkj]
            WHERE D1.id = %s
        """%deptid
        lT,iN = remote_db.select(sql)
        D={1:lT[0][0],2:lT[0][1],3:lT[0][2],4:lT[0][3],5:lT[0][4],6:lT[0][5],7:lT[0][6],8:lT[0][7],9:lT[0][8],10:lT[0][9],11:lT[0][10],12:lT[0][11],13:lT[0][12]}
        sql=" SELECT S.l_id FROM gw_fr_leader_sel S WHERE S.m_id = %s "%(flow_id)
        lT,iN = remote_db.select(sql)
        s="0"
        for e in lT:
            if D.has_key(e[0]):
                if D[e[0]] != 0:
                    s+=",%s"%D[e[0]]
        sql="""
            select distinct d.id,d.cname,d.sort
            from users u
            left join dept d on d.id = u.dept_id
            where u.usr_id in (%s) order by d.sort DESC
            """%s
    elif str(sel_type) in ['7']:  #7: 排除部门
        sql="SELECT id,cname,isnull(parent_id,0) FROM dept WHERE id not in(SELECT dept_id FROM gw_fr_usr_sel WHERE m_id=%s) AND id!=1 ORDER BY sort"%flow_id
    elif str(sel_type) == '11': #限定项目所在部门领导和负责人
        sql="""
            select isnull(u1.usr_id,0),isnull(u2.usr_id,0),isnull(u3.usr_id,0),isnull(u4.usr_id,0),isnull(u5.usr_id,0),isnull(u6.usr_id,0)
            ,isnull(u7.usr_id,0),isnull(u8.usr_id,0),isnull(u9.usr_id,0),isnull(u10.usr_id,0),isnull(u11.usr_id,0),isnull(u12.usr_id,0),isnull(u13.usr_id,0)            
            FROM gw_doc GD
            left join proj_tran_info t on t.proj_id = GD.proj_id
            LEFT JOIN dept D1 ON D1.id = t.tran_to_dpid
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND ISNULL(D1.true_dept_id,0) = 0)
            left join users u1 on u1.usr_id = d2.header
            left join users u2 on u2.usr_id = d2.second_header
            left join users u3 on u3.usr_id = d2.proxy_header
            left join users u4 on u4.usr_id = d2.sub_director
            left join users u5 on u5.usr_id = d2.fzcn
            left join users u6 on u6.usr_id = d2.fzkj
            left join users u7 on u7.usr_id = d2.cl_acc
            left join users u8 on u8.usr_id = d2.[lw_acc]
            left join users u9 on u9.usr_id = d2.[xmfy_acc]
            left join users u10 on u10.usr_id = d2.[byj_acc]
            left join users u11 on u11.usr_id = d2.[zg_acc]
            left join users u12 on u12.usr_id = d2.[cl_zgkj]
            left join users u13 on u13.usr_id = d2.[fy_zgkj]
            WHERE GD.id=%s
        """%pk
        lT,iN = remote_db.select(sql)
        D={1:lT[0][0],2:lT[0][1],3:lT[0][2],4:lT[0][3],5:lT[0][4],6:lT[0][5],7:lT[0][6],8:lT[0][7],9:lT[0][8],10:lT[0][9],11:lT[0][10],12:lT[0][11],13:lT[0][12]}
        sql=" SELECT S.l_id FROM gw_fr_proj_leader_sel S WHERE S.m_id = %s "%(flow_id)
        lT,iN = remote_db.select(sql)
        s="0"
        for e in lT:
            if D.has_key(e[0]):
                if D[e[0]] != 0:
                    s+=",%s"%D[e[0]]
        sql="""
            select distinct d.id,d.cname,d.sort
            from users u
            left join dept d on d.id = u.dept_id
            where u.usr_id in (%s) order by d.sort DESC
            """%s
    else:
        sql="SELECT id,cname,isnull(parent_id,0) FROM dept WHERE id!=1 ORDER BY sort"

    rows,iN = remote_db.select(sql)
    L=[]
    for e in rows:
        if str(e[0]) == str(sel_dept):b=1
        else:b=0
        L.append([e[0],e[1],b])
    if len(L)==1:
        sel_dept=L[0][0]
        L[0][2]='1'

    return L,sel_dept

def getFlowUser(request):
    pk = request.POST.get('pk') or request.GET.get('pk','')
    dept_id = request.POST.get('dept_id') or request.GET.get('dept_id','')
    flow_id = request.POST.get('flow_id') or request.GET.get('flow_id','')

    usr_id_qy = request.session.get('usr_id_qy','') or testid
    users = getViewUserIds()
    if str(usr_id_qy) not in users:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)

    L = get_usr(usr_id_qy,pk,flow_id,dept_id,'')
    names = 'value label checked'.split()
    data = [dict(zip(names, d)) for d in L]
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
            {
            "errcode":0,
            "errmsg":"",
            "data":%s
            }
            """%(data)
        #print ToGBK(s)
    return HttpResponseCORS(request,s)

def get_usr(usr_id,pk,flow_id,dept_id,sel_usr):
    sql="SELECT usr_sel_type,isnull(def_dept,0),isnull(def_usr_id,0) FROM gw_flow_def WHERE id=%s ORDER BY sort"%(flow_id)
    lT,iN = remote_db.select(sql)
    sel_type=lT[0][0]

    if str(sel_type) in ['8']: #角色 
        L2 = get_user_by_role_flow(dept_id)
    elif str(sel_type) in ['9']: #角色 
        L2 = get_user_by_role_and_proj_flow(usr_id,pk,flow_id,dept_id)
    else:
        L2 = get_user_by_dept_flow(usr_id,pk,flow_id,dept_id)
    L=[]
    for e in L2:
        if str(e[0]) == str(sel_usr):b=1
        else:b=0
        L.append([e[0],e[1],b])

    return L

def get_user_by_role_flow(role_id):
    sql="""
        select u.usr_id,u.usr_name,''
        from usr_role r
        left join users u on u.usr_id = r.usr_id
        where r.role_id = %s AND U.status = 1 AND isnull(U.del_flag,0) != 1
        """%role_id
    #print sql
    lT,iN = remote_db.select(sql)
    L=[]
    for e in lT:
        L.append([e[0],e[1],''])
    if len(L)==1:
        L[0][2]='1'
    return L

def get_user_by_role_and_proj_flow(usr_id,pk,flow_id,role_id):
    sql = "select type_id from gw_flow_def where id = %s"%(flow_id)
    lT,iN = remote_db.select(sql)
    type_id = lT[0][0]
    proj_id = ''
    if type_id == 154:
        sql="select proj_id from _m1501_cgdd where id = %s "%pk
        lT,iN = db.select(sql)
    elif type_id == 307:
        sql="select proj_id from _m3000004_shd where id = %s"%pk
        lT,iN = db.select(sql)
    else:
         lT =[]
    if len(lT) > 0:
        proj_id = lT[0][0]
    print type_id,proj_id
    if proj_id in ('',0,None):
        lT=[]
    elif role_id == '':
        lT=[]
    else:
        sql="""
            select DISTINCT u.usr_id,u.usr_name
            from users u
            left join usr_role r on r.usr_id = u.usr_id
            left join proj_user t on t.usr_id = u.usr_id and t.proj_id != 0
            where r.role_id = %s and t.proj_id = %s
            AND U.status = 1 AND isnull(U.del_flag,0) != 1
            """%(role_id,proj_id)
        lT,iN = remote_db.select(sql)
    L=[]
    for e in lT:
        L.append([e[0],e[1],''])
    if len(L)==1:
        L[0][2]='1'
    return L

#根据 选择部门获取处理人
def get_user_by_dept_flow(usr_id,pk,flow_id,dept_id):    
    if flow_id!='' and flow_id!='sign' and flow_id!='E':
        sql=" SELECT usr_sel_type,def_usr_id FROM gw_flow_def WHERE id=%s "%flow_id
        lT,iN = remote_db.select(sql)
        if len(lT)!=0:
            sel_type=lT[0][0]
            def_user=lT[0][1]
            if str(sel_type) in ['2']:  #2：限定部门及人
                sql="""
                    SELECT DISTINCT FUS.usr_id,U.usr_name
                    FROM gw_fr_usr_sel FUS
                    LEFT JOIN users U ON U.usr_id=FUS.usr_id
                    WHERE FUS.m_id=%s AND U.dept_id=%s AND U.status = 1 AND isnull(U.del_flag,0) != 1 
                    """%(flow_id,dept_id)
            elif str(sel_type) in ['5']:  #5:限定于作者的部门和限定作者  (不可行或只限于拟稿流程)
                sql="""
                    SELECT D.cid,D.cusrname
                    FROM gw_doc D
                    LEFT JOIN users U ON U.usr_id = D.cid
                    WHERE D.id=%s AND U.status = 1 AND isnull(U.del_flag,0) != 1 """%(pk)
                b='selected'
            elif str(sel_type) in ['10']: #10：限定作者部门的领导或负责人
                sql="""
                    SELECT ISNULL(G.form_dept_id,0),ISNULL(U.dept_id,0)
                    FROM gw_doc G
                    LEFT JOIN users U ON U.usr_id = G.cid
                    WHERE G.id = %s
                    """%pk
                lT,iN = remote_db.select(sql)
                if lT[0][0] != 0:
                    deptid=lT[0][0]
                else:
                    deptid=lT[0][1]
                sql="""
                    select isnull(u1.usr_id,0),isnull(u2.usr_id,0),isnull(u3.usr_id,0),isnull(u4.usr_id,0),isnull(u5.usr_id,0),isnull(u6.usr_id,0)
                    ,isnull(u7.usr_id,0),isnull(u8.usr_id,0),isnull(u9.usr_id,0),isnull(u10.usr_id,0),isnull(u11.usr_id,0),isnull(u12.usr_id,0),isnull(u13.usr_id,0)            
                    FROM dept D1
                    LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND ISNULL(D1.true_dept_id,0) = 0)
                    left join users u1 on u1.usr_id = d2.header
                    left join users u2 on u2.usr_id = d2.second_header
                    left join users u3 on u3.usr_id = d2.proxy_header
                    left join users u4 on u4.usr_id = d2.sub_director
                    left join users u5 on u5.usr_id = d2.fzcn
                    left join users u6 on u6.usr_id = d2.fzkj
                    left join users u7 on u7.usr_id = d2.cl_acc
                    left join users u8 on u8.usr_id = d2.[lw_acc]
                    left join users u9 on u9.usr_id = d2.[xmfy_acc]
                    left join users u10 on u10.usr_id = d2.[byj_acc]
                    left join users u11 on u11.usr_id = d2.[zg_acc]
                    left join users u12 on u12.usr_id = d2.[cl_zgkj]
                    left join users u13 on u13.usr_id = d2.[fy_zgkj]
                    WHERE D1.id = %s
                """%deptid
                lT,iN = remote_db.select(sql)
                D={1:lT[0][0],2:lT[0][1],3:lT[0][2],4:lT[0][3],5:lT[0][4],6:lT[0][5],7:lT[0][6],8:lT[0][7],9:lT[0][8],10:lT[0][9],11:lT[0][10],12:lT[0][11],13:lT[0][12]}
                sql=" SELECT S.l_id FROM gw_fr_leader_sel S WHERE S.m_id = %s "%(flow_id)
                lT = db_erp.executesql(sql)
                s="0"
                for e in lT:
                    if D.has_key(e[0]):
                        if D[e[0]] != 0:
                            s+=",%s"%D[e[0]]
                sql=" select usr_id,usr_name from users where usr_id in (%s) order by sort DESC "%s
            elif str(sel_type) == '11': #限定项目所在部门领导和负责人
                sql="""
                    select isnull(u1.usr_id,0),isnull(u2.usr_id,0),isnull(u3.usr_id,0),isnull(u4.usr_id,0),isnull(u5.usr_id,0),isnull(u6.usr_id,0)
                    ,isnull(u7.usr_id,0),isnull(u8.usr_id,0),isnull(u9.usr_id,0),isnull(u10.usr_id,0),isnull(u11.usr_id,0),isnull(u12.usr_id,0),isnull(u13.usr_id,0)            
                    FROM gw_doc GD
                    left join proj_tran_info t on t.proj_id = GD.proj_id
                    LEFT JOIN dept D1 ON D1.id = t.tran_to_dpid
                    LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND ISNULL(D1.true_dept_id,0) = 0)
                    left join users u1 on u1.usr_id = d2.header
                    left join users u2 on u2.usr_id = d2.second_header
                    left join users u3 on u3.usr_id = d2.proxy_header
                    left join users u4 on u4.usr_id = d2.sub_director
                    left join users u5 on u5.usr_id = d2.fzcn
                    left join users u6 on u6.usr_id = d2.fzkj
                    left join users u7 on u7.usr_id = d2.cl_acc
                    left join users u8 on u8.usr_id = d2.[lw_acc]
                    left join users u9 on u9.usr_id = d2.[xmfy_acc]
                    left join users u10 on u10.usr_id = d2.[byj_acc]
                    left join users u11 on u11.usr_id = d2.[zg_acc]
                    left join users u12 on u12.usr_id = d2.[cl_zgkj]
                    left join users u13 on u13.usr_id = d2.[fy_zgkj]
                    WHERE GD.id=%s
                """%pk
                lT,iN = remote_db.select(sql)
                D={1:lT[0][0],2:lT[0][1],3:lT[0][2],4:lT[0][3],5:lT[0][4],6:lT[0][5],7:lT[0][6],8:lT[0][7],9:lT[0][8],10:lT[0][9],11:lT[0][10],12:lT[0][11],13:lT[0][12]}
                sql=" SELECT S.l_id FROM gw_fr_proj_leader_sel S WHERE S.m_id = %s "%(flow_id)
                lT = db_erp.executesql(sql)
                s="0"
                for e in lT:
                    if D.has_key(e[0]):
                        if D[e[0]] != 0:
                            s+=",%s"%D[e[0]]
                sql=" select usr_id,usr_name from users where usr_id in (%s) AND status = 1 AND isnull(del_flag,0) != 1 order by sort DESC "%s
            else:
                sql="""
                    SELECT U.usr_id,U.usr_name
                    FROM users U
                    WHERE U.dept_id=%s AND U.status = 1 AND isnull(U.del_flag,0) != 1
                    ORDER BY U.sort DESC
                    """%(dept_id)
            #print sql
            
            lT,iN = remote_db.select(sql)
    L=[]
    for e in lT:
        L.append([e[0],e[1],''])
    if len(L)==1:
        L[0][2]='1'
    return L

def putAudit():
          
    if opt == '3': #作废
        next_flow_id = -1
        next_dept_id = -1
        next_usr_id = -1
        next_role_id = 'NULL'
    else:
        if sel_type in ('8','9'): #通过角色 换成 部门
            if next_dept_id != '':
                sql=" select dept_id from users where usr_id = %s "%next_dept_id
                lT = db_erp.executesql(sql)
                if len(lT):
                    next_role_id = next_dept_id 
                    next_dept_id = lT[0][0]
        if F3 in ('','NULL',None):
            s1 = """
                    %s({
                      "errCode":-1,
                      "msg":"请选择 下一流程!",
                    })
                 """%(callback)
            return s1         

        if F3 != 'E':
            if next_dept_id in ('','NULL',None):
                s1 = """
                    %s({
                      "errCode":-1,
                      "msg":"请选择 办理部门或角色!",
                    })
                 """%(callback)
                return s1         
            if next_usr_id in ('','NULL',None):
                s1 = """
                    %s({
                      "errCode":-1,
                      "msg":"请选择 办理人!",
                    })
                 """%(callback)
                return s1         

    ## 从数据库获取相关信息 防止数据出错和刷新 ##
    sql="""
        SELECT top 1
            ISNULL(cur_flow_id,0),
            ISNULL(cur_flow_usr_id,0),
            ISNULL(next_flow_id,0),
            ISNULL(next_flow_usr_id,0),
            ISNULL(cur_flow_status,0),
            ISNULL(status,0),
            ISNULL(cur_flow_name,''),
            ISNULL(cur_user_name,''),
            ISNULL(next_flow_name,''),
            ISNULL(next_user_name,''),type_id
        FROM gw_doc (nolock)
        WHERE id = %s
        """%pk
    lT = db_erp.executesql(sql) #得到基本信息
    cur_flow_id,cur_flow_usr_id,next_flow_id,next_flow_usr_id,cur_flow_status,doc_status,cur_flow_name,cur_user_name,next_flow_name,next_user_name,gw_type = lT[0]
    sql=" select count(1) from gw_flow_his where m_id = %s "%pk
    
    lT = db_erp.executesql(sql)
    if lT[0][0] == 1: #第一个流程需要特殊处理
        cur_flow_status = 1
        next_flow_usr_id = usr_id
        next_user_name = usr_name
        next_flow_id = cur_flow_id
        next_flow_name = cur_flow_name

    ## 曾经有保存过 ##
    if cur_flow_status == 0:
        if str(cur_flow_usr_id) != str(usr_id):
            s1 = """
                    %s({
                      "errCode":-1,
                      "msg":"本文已由其他流程办理，不可修改!",
                    })
                 """%(callback)
            return s1         
            
        flow_id = cur_flow_id #flow_id 以后就永远是自己的ID了
        sql=" SELECT H.id FROM gw_flow_his H WHERE H.m_id = %s AND H.flow_id = %s AND H.status = 0 "%(pk,flow_id)
        lT = db_erp.executesql(sql)
        HID = lT[0][0] #自己的his ID
    ## 曾经没有保存过 ##
    if cur_flow_status == 1:
        if str(next_flow_usr_id) != str(usr_id):
            s1 = """
                    %s({
                      "errCode":-1,
                      "msg":"本文已由其他流程办理，不可修改!",
                    })
                 """%(callback)
            return s1         

        flow_id = next_flow_id #flow_id 以后就永远是自己的flow_def ID了
        flow_name = next_flow_name #flow_name 以后就永远是自己的名称了
        sql=" SELECT H.id,send_flow_id,ISNULL(send_flow_name,''),send_opt FROM gw_flow_his H WHERE H.m_id = %s AND H.flow_id = %s AND H.status = 0 "%(pk,flow_id)
        
        lT = db_erp.executesql(sql)
        HID = lT[0][0] #自己的his ID
        send_pre_flow_id=lT[0][1] #增加新流程用到 除此没有别的用处
        send_pre_flow_name=lT[0][2] #增加新流程用到 除此没有别的用处
        send_pre_opt=lT[0][3] or 'NULL' #增加新流程用到 除此没有别的用处
        send_opt=opt #发送人办理意见
        ## 增加下一流程 ## #已经将三个和在一条语句中执行。还需观察是否有问题
        sql="""
            INSERT INTO gw_flow_his(m_id,send_usr_id,send_usr_name,send_flow_id,send_flow_name,send_pre_flow_id,send_pre_flow_name,send_opt,send_pre_opt,status) 
            VALUES(%s,%s,'%s',%s,'%s',%s,'%s',%s,%s,0)
            """%(pk,usr_id,usr_name,flow_id,flow_name,send_pre_flow_id,send_pre_flow_name,send_opt,send_pre_opt)
        sql+="""
            UPDATE gw_flow_his SET cusrname = '%s',ctime = GETDATE()
            WHERE id = %s
            """%(usr_name,HID)
        ## 更改主表信息 ##
        sql+=""" 
            UPDATE gw_doc SET cur_flow_status = 0,pre_flow_time=cur_flow_time,
            pre_flow_id = cur_flow_id,pre_flow_name=cur_flow_name,pre_flow_dept = cur_flow_dept,pre_dept_name=cur_dept_name,pre_flow_usr_id=cur_flow_usr_id,pre_user_name=cur_user_name,
            pre_opt=cur_opt,cur_flow_time = GETDATE(),cur_flow_id = %s,cur_flow_name='%s',cur_flow_dept = %s,cur_dept_name='%s',cur_flow_usr_id = %s,cur_user_name='%s',
            next_flow_id =NULL,next_flow_name=NULL, next_flow_dept = NULL,next_dept_name=NULL, next_flow_usr_id = NULL,next_user_name=NULL
            ,IsTran=0
            WHERE id = %s
            """%(flow_id,flow_name,dept_id,dept_name,usr_id,usr_name,pk)
        db_erp.executesql(sql)
        
    #获取下流程ID
    sql=" SELECT TOP 1 id FROM gw_flow_his WHERE m_id = %s AND send_flow_id = %s AND status = 0 ORDER BY id DESC "%(pk,flow_id)
    
    lT = db_erp.executesql(sql)
    NEXTHID = lT[0][0] #下流程

    ## 将用户选择的流程更新至数据库 ##
    #改主表
    finish = 0
    if str(is_send)=='1': #点了发送
        doc_status = get_doc_status_by_F1(opt,F3)
        doc_flow_status = 1
        his_flow_status = 1
        if F3 == 'E': 
            finish = 1
    else: #点了暂存
        doc_status = doc_status
        doc_flow_status = 0
        his_flow_status = 0
    if F3 == "E": VF3 = "NULL"
    else:VF3 = F3

    status_txt = "已发送"
    if finish == 1:
        status_txt = "办理完毕"
    else:
        if his_flow_status == 0:
            if doc_status == 0: status_txt = "暂未发送"
            elif doc_status in (4,5): status_txt = "退回未发送"
            elif doc_status == 7: status_txt = "作废暂存"
            else: status_txt = "保存未发送"
        else:
            if doc_status in (4,5): status_txt = "已退回"
            elif doc_status == 7: status_txt = "已作废"
            else: status_txt = "已发送"

    sql="""
        UPDATE gw_doc SET
        next_flow_id = %s, next_flow_dept = %s, next_flow_usr_id = %s,
        status = %s, cur_flow_status = %s, finish = %s,IsTran=0, status_txt = '%s',cur_opt=%s  WHERE id = %s
        """%(VF3,next_dept_id,next_usr_id,doc_status,doc_flow_status,finish,ToGBK(status_txt),opt,pk)
    db_erp.executesql(sql)
    
    #改当前流程
    sql="""
        UPDATE gw_flow_his SET
        opt = %s, memo = '%s', next_flow_id = %s, next_dept =%s, next_usr_id = %s, uid = %s,
        uusrname = '%s', utime = GETDATE(), status = %s, next_role_id = %s,dirty_flag=1 WHERE id = %s
        """%(opt,memo,VF3,next_dept_id,next_usr_id,usr_id,usr_name,his_flow_status,next_role_id,HID)
    db_erp.executesql(sql)
    
    #改下一流程
    sql+="""
        UPDATE gw_flow_his SET send_opt=%s,flow_id = %s, cid = %s,dirty_flag=1 WHERE id = %s 
        """%(opt,VF3,next_usr_id,NEXTHID)
    db_erp.executesql(sql)

    update_flow_text(pk,HID,NEXTHID)

    update_gw_db(pk, 1)
  
    s1 = """
%s({
    "errCode":0,
    "msg":"办理成功!",
})
    """%(callback)
    return s1

def getRkdList(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    users = getViewUserIds()
    if str(usr_id_qy) not in users :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    sql="""select rk.id,rk.req_no,op.cname,su.cname,u.usr_name,u.pic,rk.ctime,rk.status,sh.cgd_sn
           from _m3000004_rkd rk
           left join _m3000004_shd sh on rk.id = sh.id
           left join _m1501_cgdd cg on cg.id = sh.cgd_id
           left join out_proj op on op.id = cg.proj_id
           left join suppliers su on su.id = cg.sup_id
           left join users u on u.usr_id = rk.cid
           where (rk.cid = %s or find_in_set(%s,'%s'))
        """%(usr_id_qy,usr_id_qy,','.join(users))
    if search !='':
        sql+="AND ((IFNULL(rk.sn,'') LIKE '%%%s%%' ) or (IFNULL(op.cname,'') LIKE '%%%s%%' ) or (IFNULL(su.cname,'') LIKE '%%%s%%' ))"%(search,search,search)
    if situation !='':
        sql+="AND (rk.status='%s') "%(situation)
    sql+="ORDER BY rk.id DESC"
    print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    names = 'id sn proj_name sup_name usr_name head_pic ctime status cgd_sn'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取入库单列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def getRkdInfo(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk') or request.GET.get('pk','')
    shd_sn = request.POST.get('shd_sn','')
    if pk == '' and shd_sn == '':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    if pk == '':
        sql = "select id from _m3000004_shd where sn='%s'"%(shd_sn)
        print sql
        rows,iN=db.select(sql)
        if iN == 0:
            s = """
            {
            "errcode": -1,
            "errmsg": "送货单号不正确"
            }        """
            return HttpResponseJsonCORS(s)
        pk = rows[0][0]

    sql="""SELECT rk.id, rk.sh_date,rk.ys_result,rk.mt_price,rk.real_mt_price,sh.sn,rk.busi_usr_name,rk.ys_person
                  ,rk.sh_way,rk.zxd,rk.speci,rk.hgz,rk.quality_speci,rk.pack_form,rk.qual_norm,rk.memo
                  ,'','',rk.status,sq.is_gycg
                  ,ifnull(rk.flow_opt,''),rk.flow_memo,ifnull(rk.flow_next_flow,''),ifnull(rk.flow_next_dept,''),ifnull(rk.flow_next_role,''),ifnull(rk.flow_next_usr,'')
                  ,sh.proj_id
        FROM _m3000004_rkd rk 
        left join _m3000004_shd sh on rk.id = sh.id
        left join _m1501_cgsq sq on sq.id = sh.cgd_id
        #left join _m1501_cgdd cg on cg.id = sq.id
        #left join out_proj op on op.id = cg.proj_id
        #left join suppliers su on su.id = cg.sup_id
        WHERE rk.id=%s
        """%pk
    print sql
    rows,iN=db.select(sql)
    is_add = 0
    if iN == 0:
        sql="""SELECT sh.id, '','','','',sh.sn,'',''
                  ,'','','','','','','',''
                  ,'','',0,sq.is_gycg
                  ,'','','','','',''
                  ,sh.proj_id
        FROM _m3000004_shd sh
        left join _m1501_cgsq sq on sq.id = sh.cgd_id
        left join _m1501_cgdd cg on cg.id = sq.id
        left join out_proj op on op.id = cg.proj_id
        left join suppliers su on su.id = cg.sup_id
        WHERE sh.id=%s
        """%pk
        is_add = 1
        rows,iN=db.select(sql)
    L =[]
    for e in rows:
        L1 = list(e)
        status = e[18]
        L1[6] = usr_id_qy
        if is_add == 1:
            sql = """select '',cg.id,sh.id,cg.cl_id,sh.cl_code,sh.cl_name,sh.cl_spec,sh.cl_model,sh.cl_type,sh.cl_brand,sh.cl_unit
                           ,cg.qty, yrk.qty, cg.qty-ifnull(yrk.qty,0),sh.qty,''
                           ,cg.price,sh.price,case sq.is_gycg when 1 then sh.price*1.005 else sh.price end,'','',''
                     from _m3000004_shd_list sh
                     left join _m1501_cgdd_list cg on sh.cgmx_id = cg.id
                     left join (select sum(ys_qty) as qty,cgmx_id from _m3000004_rkd_list group by cgmx_id) yrk on yrk.cgmx_id = cg.id
                     left join _m1501_cgsq sq on cg.m_id = sq.id
                     where sh.m_id = %s"""%(pk)
            rows1,iN1=db.select(sql)
            names = """rkmx_id cgmx_id shmx_id cl_id cl_code cl_name cl_spec cl_model cl_type cl_brand cl_unit cg_qty yrk_qty wrk_qty sh_qty ys_qty cg_price real_price rk_price real_amount amount rkmx_memo""".split()
            L1[16] = [dict(zip(names, d)) for d in rows1]
            L1[17] = []
        else:
            sql = """select rk.id,cg.id,sh.id,cg.cl_id,sh.cl_code,sh.cl_name,sh.cl_spec,sh.cl_model,sh.cl_type,sh.cl_brand,sh.cl_unit
                           ,cg.qty, yrk.qty, rk.wrk_qty,sh.qty,rk.ys_qty
                           ,cg.price,sh.price,case sq.is_gycg when 1 then sh.price*1.005 else sh.price end,rk.real_amount,rk.amount,rk.rkmx_memo
                     from _m3000004_rkd_list rk
                     left join _m3000004_shd_list sh on sh.id = rk.shmx_id
                     left join _m1501_cgdd_list cg on sh.cgmx_id = cg.id
                     left join (select sum(ys_qty) as qty,cgmx_id from _m3000004_rkd_list group by cgmx_id) yrk on yrk.cgmx_id = cg.id
                     left join _m1501_cgsq sq on cg.m_id = sq.id
                     where rk.m_id = %s"""%(pk)
            rows1,iN1=db.select(sql)
            names = """rkmx_id cgmx_id shmx_id cl_id cl_code cl_name cl_spec cl_model cl_type cl_brand cl_unit cg_qty yrk_qty wrk_qty sh_qty ys_qty cg_price real_price rk_price real_amount amount rkmx_memo""".split()
            L1[16] = [dict(zip(names, d)) for d in rows1]
            sql = "select id,fy_type, real_money, _money,qtmx_memo from _m3000004_rkd_fee where m_id = %s"%(pk)
            rows1,iN1=db.select(sql)
            names = """qtmx_id fy_type real_money _money qtmx_memo""".split()
            L1[17] = [dict(zip(names, d)) for d in rows1]

        flow_opt = e[20]
        flow_next_flow = e[22]
        flow_next_dept = e[23]
        flow_next_role = e[24]
        flow_next_usr = e[25]
        if flow_next_flow != '':
            if flow_next_dept != '':
                L1[22],L1[23],L1[25] = getFlowAll(pk,usr_id_qy,'rkd',flow_next_flow,flow_next_dept,flow_next_usr)
            else:
                L1[22],L1[24],L1[25] = getFlowAll(pk,usr_id_qy,'rkd',flow_next_flow,flow_next_role,flow_next_usr)
        proj_id = e[26]
        L.append(L1)
    names = """id sh_date ys_result mt_price real_mt_price sh_no busi_usr_name ys_person sh_way zxd speci hgz quality_speci pack_form qual_norm memo rk_detail other_detail status is_gycg flow_opt flow_memo flow_next_flow flow_next_dept flow_next_role flow_next_usr""".split()
    data = [dict(zip(names, d)) for d in L]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    is_cgy = isProjCgy(proj_id,usr_id_qy)
    if status == 0 and is_cgy == 1:
        canEdit = 1
    else:
        canEdit = 0
    if usr_id_qy == 2110:
        canEdit = 1
             
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s,
        "pk":%s,
        "canEdit":%s
        }        """%(L,pk,canEdit)
    #s=ToGBK(s)
    print ToGBK(s) 
    return HttpResponseJsonCORS(s)
   
def saveRkd(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    users = getViewUserIds()
    if str(usr_id_qy) not in users:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)

    data = request.POST.get('data','')
    data_list = json.loads(data)

    pk = data_list.get('pk','')
    sh_date = data_list.get('sh_date','')
    ys_result = data_list.get('ys_result') or 'NULL'
    mt_price = data_list.get('mt_price') or 'NULL'
    real_mt_price = data_list.get('real_mt_price') or 'NULL'
    sh_no = data_list.get('sh_no','')
    ys_person = data_list.get('ys_person') or 'NULL'
    busi_usr_name = data_list.get('busi_usr_name') or 'NULL'
    sh_way = data_list.get('sh_way','')
    zxd = data_list.get('zxd','')
    speci = data_list.get('speci','')
    hgz = data_list.get('hgz','')
    quality_speci = data_list.get('quality_speci','')
    pack_form = data_list.get('pack_form','')
    qual_norm = data_list.get('qual_norm','')
    memo = data_list.get('memo','')
    memo = MySQLdb.escape_string(memo)

    rk_detail = data_list.get('rk_detail','')
    other_detail = data_list.get('other_detail','')

    sql = "select id from _m3000004_rkd where id = %s"%(pk)
    print sql
    rows,iN = db.select(sql)
    if iN == 0:
        sql = """INSERT INTO _m3000004_rkd (id,status, cid, ctime, sh_date, ys_result, mt_price, real_mt_price, sh_no, busi_usr_name, ys_person
                         , sh_way, zxd, speci, hgz, quality_speci, pack_form, qual_norm, memo) 
                 VALUES (%s,0,%s, now(), '%s', %s, %s, %s, '%s', %s, %s
                        , '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
              """%(pk, usr_id_qy, sh_date, ys_result, mt_price, real_mt_price, sh_no, busi_usr_name, ys_person
                         , sh_way, zxd, speci, hgz, quality_speci, pack_form, qual_norm, memo)
    else:
        sql = """UPDATE _m3000004_rkd set sh_date='%s', ys_result=%s, mt_price=%s, real_mt_price=%s, sh_no='%s', busi_usr_name=%s, ys_person=%s
                         , sh_way='%s', zxd='%s', speci='%s', hgz='%s', quality_speci='%s', pack_form='%s', qual_norm='%s', memo='%s', `utime`=now()
                 where id=%s;
              """%(sh_date, ys_result, mt_price, real_mt_price, sh_no, busi_usr_name, ys_person
                         , sh_way, zxd, speci, hgz, quality_speci, pack_form, qual_norm, memo,pk)
    print ToGBK(sql)
    db.executesql(sql)

    for e in rk_detail:
        rkmx_id = e.get('rkmx_id','')
        cgmx_id = e.get('cgmx_id') or 'NULL'
        shmx_id = e.get('shmx_id') or 'NULL'
        cl_id = e.get('cl_id') or 'NULL'
        cg_qty = e.get('cg_qty') or 'NULL'
        yrk_qty = e.get('yrk_qty') or 'NULL'
        wrk_qty = e.get('wrk_qty') or 'NULL'
        sh_qty = e.get('sh_qty') or 'NULL'
        ys_qty = e.get('ys_qty') or 'NULL'
        cg_price = e.get('cg_price') or 'NULL'
        real_price = e.get('real_price') or 'NULL'
        rk_price = e.get('rk_price') or 'NULL'
        real_amount = e.get('real_amount') or 'NULL'
        amount = e.get('amount') or 'NULL'
        rkmx_memo = e.get('rkmx_memo','')
        if rkmx_id == '':
            sql = """insert into _m3000004_rkd_list (m_id,cgmx_id,shmx_id,cl_id
                     ,cg_qty, yrk_qty, wrk_qty, sh_qty, ys_qty, cg_price, real_price, rk_price, real_amount, amount, rkmx_memo,ctime) values
                     (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',now())
                  """%(pk,cgmx_id,shmx_id,cl_id
                     ,cg_qty, yrk_qty, wrk_qty, sh_qty, ys_qty, cg_price, real_price, rk_price, real_amount, amount, rkmx_memo)
        else:
            sql = """update _m3000004_rkd_list set cgmx_id=%s,shmx_id=%s,cl_id=%s
                     ,cg_qty=%s, yrk_qty=%s, wrk_qty=%s, sh_qty=%s, ys_qty=%s, cg_price=%s, real_price=%s, rk_price=%s, real_amount=%s, amount=%s, rkmx_memo='%s',utime=now() 
                     where id =%s
                  """%(cgmx_id,shmx_id,cl_id
                     ,cg_qty, yrk_qty, wrk_qty, sh_qty, ys_qty, cg_price, real_price, rk_price, real_amount, amount, rkmx_memo, rkmx_id)
        print ToGBK(sql)
        db.executesql(sql)
    for e in other_detail:
        qtmx_id = e.get('qtmx_id','')
        fy_type = e.get('fy_type','')
        real_money = e.get('real_money') or 'NULL'
        _money = e.get('_money') or 'NULL'
        qtmx_memo = e.get('qtmx_memo','')
        status = e.get('status','')
        if qtmx_id == '':
            sql = """insert into _m3000004_rkd_fee (m_id, fy_type, real_money, _money,qtmx_memo) VALUES 
                     (%s,'%s',%s,%s,'%s')
                  """%(pk,fy_type, real_money, _money, qtmx_memo)
        elif status == 'deleted':
            sql = "delete from _m3000004_rkd_fee where id = %s"%(qtmx_id)
        else:
            sql = """update _m3000004_rkd_fee set fy_type='%s', real_money=%s, _money=%s,qtmx_memo='%s' where id = %s
                  """%(fy_type, real_money, _money, qtmx_memo, qtmx_id)
        print ToGBK(sql)
        db.executesql(sql)
 
    s = """
        {
        "errcode": 0,
        "errmsg": "保存成功"
        }        """
    return HttpResponseJsonCORS(s)

def pushRkd(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    data = request.POST.get('data','')
    data_list = json.loads(data)
    pk = data_list.get('pk','')
    flow_opt = data_list.get('flow_opt') or 0
    flow_memo = data_list.get('flow_memo','')
    flow_memo = MySQLdb.escape_string(flow_memo)
    flow_next_flow = data_list.get('flow_next_flow') or 'NULL'
    flow_next_dept = data_list.get('flow_next_dept') or 'NULL'
    flow_next_role = data_list.get('flow_next_role') or 'NULL'
    flow_next_usr = data_list.get('flow_next_usr') or 'NULL'

    is_send = request.GET.get('is_send','')
    is_send = is_send.replace('/','')
 
    sql = """update _m3000004_rkd set flow_opt=%s,flow_memo='%s',flow_next_flow=%s,flow_next_dept=%s,flow_next_role=%s,flow_next_usr=%s,flow_send_time=now() where id=%s
          """%(flow_opt,flow_memo,flow_next_flow,flow_next_dept,flow_next_role,flow_next_usr,pk)
    db.executesql(sql)

    if is_send == '1':
        sql = "select usr_name,dept_id from users where usr_id = %s"%(usr_id_qy)
        rows,iN=db.select(sql)
        usr_name = rows[0][0]
        dept_id = rows[0][1]
        sql="""SELECT rk.id, MS.cg_type, MS.ghf, MS.js_way, MS.is_gycg, MS.gy_company, MS.cg_zt
                  , MS.pay_way,cg.cgd_no,cg.cgd_gwid,cg.cgd_id
                  ,ifnull(rk.flow_opt,''),rk.flow_memo,ifnull(rk.flow_next_flow,''),ifnull(rk.flow_next_dept,''),ifnull(rk.flow_next_role,''),ifnull(rk.flow_next_usr,'')
                  ,cg.proj_id,op.cname,su.id,su.cname
                  ,sg.id,sg.cname,op.gc_no,sg.code
                  ,rk.sh_date,rk.ys_result,rk.mt_price,rk.real_mt_price
                  ,rk.busi_usr_name,u1.usr_name,rk.ys_person,u2.usr_name
                  ,rk.sh_way,rk.zxd,rk.speci,rk.hgz,rk.quality_speci,rk.pack_form,rk.qual_norm,rk.memo,rk.sh_no
                  ,case MS.cg_zt when 1 then '深圳市宝鹰建设集团股份有限公司' when 2 then '普宁市宝鹰供应链管理有限公司' else '深圳市中建南方建设集团有限公司' end
                  ,rk.req_no,ifnull(rk.rk_gwid,''),rk.rk_id
        FROM _m3000004_rkd rk
        left join _m3000004_shd sh on sh.id = rk.id
        left join _m1501_cgdd cg on cg.id = sh.cgd_id
        left join _m1501_cgsq ms on ms.id = sh.cgd_id
        left join out_proj op on cg.proj_id = op.id
        left join contract_sg_file sg on sg.id = cg.ctr_id
        left join suppliers su on su.id = cg.sup_id
        left join users u1 on u1.usr_id = rk.busi_usr_name
        left join users u2 on u2.usr_id = rk.ys_person
        WHERE rk.id=%s
        """%pk
        #print ToGBK(sql)
        rows,iN=db.select(sql)
        L = list(rows[0])
        #保存公文表
        title = '验收入库申请：%s'%(L[18])
        m_id = L[-1]
        gw_id = L[-2]
        code = L[-3]
        cgd_id = L[10] or 'NULL'
        proj_id = L[17]
        ghf = L[2]
        if gw_id == '':
            gw_id = add_save_master('rkd',title,usr_id_qy,usr_name,dept_id,flow_next_usr)
            t=time.time()
            date_ary=time.localtime(t)
            x=time.strftime("WYS%Y%m%d",date_ary)
        
            sql = "select ifnull(max(last_code),'') from code_lib where last_code like '%s%%' and src = 'D402'"%(x)
            rows,iN = db.select(sql)
            if iN>0:
                code = rows[0][0]
                if code == '':
                    code = "%s001"%(x)
                    maxnum = 1
                else:
                    code = code.replace("%s"%x,'')
                    maxnum = int(code.strip())+1
                    maxnum1 = str(maxnum).zfill(3)
                    code = "%s%s"%(x,maxnum1)
            else:
                code = "%s001"%(x)
                maxnum = 1
            sql = "update code_lib set last_code='%s',maxnum=%s where src = 'D402'"%(code,maxnum)
            db.executesql(sql)

            #保存主表单
            sql = """INSERT INTO Prj_Mat_Master (gw_id,Prj_id,Req_No,cDate,Stype,Iscolla,Total_Price,Ysd_Code,mpb_id,sup_id,ship_type
            ,rec_date,rec_usr_id,rec_usr_name,super_usr_id,super_usr_name
            ,Kxzl_Zxd,Zxzl_Sm,Zxzl_Hgz,Zxzl_Zlzm,Pack_Sty,[Standard],Out_No
            , memo,finish,cid,ctime,act_total,check_Concl,IsTran
            ,[GHF],[JSFS],[pay_type],[is_from_hxsh]
            ,[buy_no],[sp_name],[gc_no],[gc_name],[cusrname],[cgzt],[cgzt_txt],supply)
            VALUES(%s,%s,'%s',getdate(),11,1,%s,'%s',%s,%s,'%s'
                  ,'%s',%s,'%s',%s,'%s'
                  ,'%s','%s','%s','%s','%s','%s','%s'
                  ,'%s',0,%s,getdate(),%s,%s,0
                  ,%s,%s,%s,%s
                  ,'%s','%s','%s','%s','%s',%s,'%s',%s)
                """ % (gw_id,proj_id,code,L[27],code,cgd_id,L[19],L[33]
                       ,L[25],L[29],L[30],L[31] or 'NULL',L[32] or ''
                       ,L[34],L[35],L[36],L[37],L[38],L[39],L[41]
                       ,L[40],usr_id_qy,L[28],L[26]
                       ,L[2],L[3],L[7],L[4]
                       ,L[8],L[20],L[23],L[18],usr_name,L[6],L[42],L[5] or 'NULL')
            print ToGBK(sql)
            remote_db.executesql(sql)
        
            sql = "select id from Prj_Mat_Master where gw_id=%s"%(gw_id)
            rows,iN = remote_db.select(sql)
            if iN>0: 
                m_id = rows[0][0]
            else:
                m_id = 0

            sql = "UPDATE gw_doc set proj_id=%s,sn='%s' where id=%s"%(proj_id,code,gw_id)
            remote_db.executesql(sql)

            #材料明细表
            sql = """select cg.cgd_mxid,cg.cl_id,sh.cl_name,sh.cl_spec,sh.cl_model,sh.cl_brand,cg.cl_unit,sh.cl_unit
                           ,cg.qty,rk.ys_qty
                           ,cg.price,case sq.is_gycg when 1 then sh.price*1.005 else sh.price end,rk.real_amount,rk.amount,rk.rkmx_memo
                     from _m3000004_rkd_list rk
                     left join _m3000004_shd_list sh on sh.id = rk.shmx_id
                     left join _m1501_cgdd_list cg on sh.cgmx_id = cg.id
                     left join (select sum(ys_qty) as qty,cgmx_id from _m3000004_rkd_list group by cgmx_id) yrk on yrk.cgmx_id = cg.id
                     left join _m1501_cgsq sq on cg.m_id = sq.id 
                     where rk.m_id = %s order by rk.sort"""%(pk)
            rows,iN=db.select(sql)
            for e in rows:
                sql = """INSERT INTO Prj_Mat_List (
							gw_id,									--gw_id、入库主表单公文id
							M_Id,									--m_id、入库主表单id
							Mpb_id,									--mpb_id、采购单表单id
							stype,									--stype、库存单据类型
							finish,									--finish、是否完成
							yc,										--yc、是否异常
							p_id,									--p_id、材料采购明细id
							Mat_Id,									--mat_id、材料id
							mat_name,								--mat_name、材料名称
							Spec,									--Spec、规格尺寸
							Model,									--Model、型号
							Brand,									--Brand、品牌
							Unit,									--Unit、材料计量单位id
							unit_name,								--unit_name、单位名称
							Check_Amc,								--Check_Amc、入库数量
							sq_countAmc,							--sq_countAmc、采购数量
							F_Amc,									--F_Amc、修改前的数量
							C_Amc,									--C_Amc、修改变动的数量
							L_Amc,									--L_Amc、修改后的数量
							price,									--price、入库单价
							L_Money,								--L_Money、入库金额
							act_price,								--act_price、实际入库单价
							act_money,								--act_money、实际入库金额
							pur_price,								--pur_price、采购单价
							pur_money,								--pur_money、采购金额
							act_pur_price,							--act_pur_price、实际采购单价
							act_pur_money,							--act_pur_money、实际采购金额
							GHF,									--GHF、供货方
							purpose,								--purpose、备注
							Cid,									--cid、入库人
							ctime   								--ctime、入库时间
							)
			VALUES 
               (%s,%s,%s,11,0,0,%s,%s,'%s','%s','%s','%s',%s,'%s'
               ,%s,%s,0,%s,%s,%s,%s
               ,%s,%s,%s,%s,%s,%s,%s,'%s',%s,getdate())
              """%(gw_id,m_id,cgd_id,e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7]
               ,e[9],e[8],e[9],e[9],e[11],e[13],e[10],e[12],e[11],e[13],e[10],e[12],ghf,e[14],usr_id_qy)
                print ToGBK(sql)
                remote_db.executesql(sql)

            #其他费用明细表
            sql = "select fy_type, real_money, _money,qtmx_memo from _m3000004_rkd_fee where m_id = %s"%(pk)
            rows,iN=db.select(sql)
            for e in rows:
                sql = """INSERT INTO [Prj_Mat_Master_other]
                       ([gw_id]
                       ,[m_id]
                       ,[U_type]
                       ,[act_amount]
                       ,[amount]
                       ,[memo]
                       ,[cid]
                       ,[ctime])
                VALUES
                    (%s,%s,'%s',%s,%s,'%s',%s,getdate())
              """%(gw_id,m_id,e[0],e[1],e[2],e[3],usr_id_qy)
                #print ToGBK(sql)
                remote_db.executesql(sql)

            mForm_2_save(gw_id,flow_next_flow,flow_next_dept,flow_next_role,flow_next_usr,flow_memo,usr_id_qy,usr_name,dept_id)

        sql = "update _m3000004_rkd set status=1,req_no='%s',rk_id=%s,rk_gwid=%s where id = %s"%(code,m_id,gw_id,pk)
        db.executesql(sql)
        sql = "update _m3000004_shd set status=1,rkd_no='%s',rkd_id=%s,rkd_gwid=%s where id = %s"%(code,m_id,gw_id,pk)
        #print sql
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "发送成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def deleteRkd(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    users = getViewUserIds()
    if str(usr_id_qy) not in users:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)

    pk = request.POST.get('pk','')

    sql = "delete from _m3000004_rkd_fee where m_id=%s"%(pk)
    db.executesql(sql)
    sql = "delete from _m3000004_rkd_list where m_id=%s"%(pk)
    db.executesql(sql)
    sql = "delete from _m3000004_rkd where id=%s"%(pk)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "保存成功"
        }        """
    return HttpResponseJsonCORS(s)

def add_save_master(type,title,usr_id,usr_name,dept_id,flow_next_usr):
    if type == 'cgd':
        gw_type = '154'  # 获取的为 gw_type 表中的 ID 在子类中定义
        flow_id = '592'  # 获取的为 gw_flow_def 表中的ID 在子类中定义
    elif type == 'rkd':
        gw_type='307'  # 获取的为 gw_type 表中的 ID 在子类中定义
        flow_id='1730'  # 获取的为 gw_flow_def 表中的ID 在子类中定义
    else:
        gw_type='0' 
        flow_id='0'  

    random_no = "%s_%s"%(time.time(),usr_id)
    #sql="exec insert_gw_doc '%s',%s,%s,%s,'%s',%s,'%s'"%(title,flow_id,dept_id,usr_id,usr_name,gw_type,random_no)  
    sql="SELECT isnull(is_pub,0),cname,[type] FROM gw_type WHERE id=%s;"%(gw_type)
    rows,iN = remote_db.select(sql)
    if iN>0: 
        is_pub = int(rows[0][0])
        type_name = rows[0][1]
        itype = rows[0][2]
    else: 
        is_pub = 0
        type_name = ''
        itype = 0

    sql="SELECT cname FROM gw_flow_def WHERE id=%s;"%(flow_id)
    rows,iN = remote_db.select(sql)
    if iN>0: 
        cur_flow_name = rows[0][0]
    else: 
        cur_flow_name = ''
    sql="SELECT cname FROM dept WHERE id=%s;"%(dept_id)
    rows,iN = remote_db.select(sql)
    if iN>0: 
        cur_dept_name = rows[0][0]
    else: 
        cur_dept_name = ''

    sql= """SELECT CAST(
                    (SELECT ','+CONVERT(VARCHAR,A0.dept_id,121)
                    FROM (
                        SELECT CONVERT(VARCHAR,dept_id,121) AS dept_id FROM gw_pub_info WHERE dept_id IS NOT NULL AND type_id=%s
                    ) A0
                    FOR XML PATH ('')) AS VARCHAR(MAX))+','
         """%(gw_type)
    rows,iN = remote_db.select(sql)
    if iN>0: 
        right_depts = rows[0][0]
    else: 
        right_depts = ''

    sql= """SELECT CAST(
                    (SELECT ','+CONVERT(VARCHAR,A0.usr_id,121)
                    FROM (
                        SELECT CONVERT(VARCHAR,usr_id,121) AS usr_id FROM gw_pub_info WHERE usr_id IS NOT NULL AND type_id=%s
                    ) A0
                    FOR XML PATH ('')) AS VARCHAR(MAX))+','
         """%(gw_type)
    rows,iN = remote_db.select(sql)
    if iN>0: 
        right_users = rows[0][0] +'%s,%s,'%(usr_id,flow_next_usr)
    else: 
        right_users = ',%s,%s,'%(usr_id,flow_next_usr)
                    
    sql= """INSERT INTO [gw_doc]
          ( title,cur_flow_id,cur_flow_name,cur_flow_dept,cur_dept_name,cur_flow_usr_id,cur_user_name,cur_flow_time,
           cid, cusrname,ctime,[type],type_id,is_pub,status, P1_flag, next_flow_usr_id, random_no, type_name,right_users,right_depts)  
           VALUES 
          ( '%s', %s,'%s', %s,'%s', %s,'%s',getDate()
             , %s,'%s', getDate(),%s,%s,%s,0, 1, -100, '%s','%s','%s','%s')
        """%(title,flow_id,cur_flow_name,dept_id,cur_dept_name,usr_id,usr_name
             ,usr_id,usr_name, itype, gw_type, is_pub, random_no, type_name, right_users, right_depts)
    print ToGBK(sql)
    remote_db.executesql(sql)

    sql="SELECT id FROM gw_doc WHERE random_no='%s';"%(random_no)
    rows,iN = remote_db.select(sql)
    if iN>0: 
        m_id = rows[0][0]
    else: 
        m_id = ''

    #将起始流程 插入流程表
    sql= """INSERT INTO gw_flow_his(m_id,send_usr_id,send_usr_name,send_flow_id,send_flow_name,send_pre_flow_id,cid,ctime,flow_id,flow_name,cusrname)
            VALUES (%s, %s,'%s',%s,'%s',-100, %s, getDate(), %s,'%s','%s') 
        """%(m_id,usr_id,usr_name,flow_id,cur_flow_name,usr_id,flow_id,cur_flow_name,usr_name)
    remote_db.executesql(sql)

    sql=""" 
            update d
            set 
            pre_flow_name = pf.cname, pre_dept_name = pd.cname, pre_user_name = pu.usr_name,
            cur_flow_name = cf.cname, cur_dept_name = cd.cname, cur_user_name = cu.usr_name,
            next_flow_name = nf.cname, next_dept_name = nd.cname, next_user_name = nu.usr_name
            from gw_doc d
            left join gw_flow_def pf on pf.id = d.pre_flow_id
            left join dept pd on pd.id = d.pre_flow_dept
            left join users pu on pu.usr_id = d.pre_flow_usr_id

            left join gw_flow_def cf on cf.id = d.cur_flow_id
            left join dept cd on cd.id = d.cur_flow_dept
            left join users cu on cu.usr_id = d.cur_flow_usr_id

            left join gw_flow_def nf on nf.id = d.next_flow_id
            left join dept nd on nd.id = d.next_flow_dept
            left join users nu on nu.usr_id = d.next_flow_usr_id
            where d.id = %s
        """%m_id
    remote_db.executesql(sql)
    
    return m_id

def mForm_2_save(pk,next_flow_id,next_dept_id,next_role_id,next_usr_id,memo,usr_id,usr_name,dept_id):
    
    sql = "select usr_sel_type from gw_flow_def where id=%s"%(next_flow_id)
    #print sql
    lT,iN = remote_db.select(sql)
    sel_type = lT[0][0] #8 角色 9 角色和项目
    if sel_type in ('8','9'): #通过角色 换成 部门
        if next_dept_id == '':
            next_dept_id = dept_id
    opt = 1
    VF3 = next_flow_id

    sql="""
        SELECT top 1
            ISNULL(cur_flow_id,0),
            ISNULL(cur_flow_usr_id,0),
            ISNULL(next_flow_id,0),
            ISNULL(next_flow_usr_id,0),
            ISNULL(cur_flow_status,0),
            ISNULL(status,0),
            ISNULL(cur_flow_name,''),
            ISNULL(cur_user_name,''),
            ISNULL(next_flow_name,''),
            ISNULL(next_user_name,''),type_id
        FROM gw_doc 
        WHERE id = %s
        """%pk
    lT,iN = remote_db.select(sql) #得到基本信息
    cur_flow_id,cur_flow_usr_id,next_flow_id,next_flow_usr_id,cur_flow_status,doc_status,cur_flow_name,cur_user_name,next_flow_name,next_user_name,gw_type = lT[0]

    sql="select count(1) from gw_flow_his where m_id = %s "%pk   
    lT,iN = remote_db.select(sql)
    if lT[0][0] == 1: #第一个流程需要特殊处理
        cur_flow_status = 1
        next_flow_usr_id = usr_id
        next_user_name = usr_name
        next_flow_id = cur_flow_id
        next_flow_name = cur_flow_name

    if cur_flow_status == 1:
        flow_id = next_flow_id #flow_id 以后就永远是自己的flow_def ID了
        flow_name = next_flow_name #flow_name 以后就永远是自己的名称了
        sql=" SELECT H.id,send_flow_id,ISNULL(send_flow_name,''),send_opt FROM gw_flow_his H WHERE H.m_id = %s AND H.flow_id = %s AND H.status = 0 "%(pk,flow_id)
        
        lT,iN = remote_db.select(sql)
        HID = lT[0][0] #自己的his ID
        send_pre_flow_id=lT[0][1] #增加新流程用到 除此没有别的用处
        send_pre_flow_name=lT[0][2] #增加新流程用到 除此没有别的用处
        send_pre_opt=lT[0][3] or 'NULL' #增加新流程用到 除此没有别的用处
        send_opt=1 #发送人办理意见
        ## 增加下一流程 ## #已经将三个和在一条语句中执行。还需观察是否有问题
        sql="""
            INSERT INTO gw_flow_his(m_id,send_usr_id,send_usr_name,send_flow_id,send_flow_name,send_pre_flow_id,send_pre_flow_name,send_opt,send_pre_opt,status) 
            VALUES(%s,%s,'%s',%s,'%s',%s,'%s',%s,%s,0)
            """%(pk,usr_id,usr_name,flow_id,flow_name,send_pre_flow_id,send_pre_flow_name,send_opt,send_pre_opt)
        remote_db.executesql(sql)
        sql="""
            UPDATE gw_flow_his SET cusrname = '%s',ctime = GETDATE()
            WHERE id = %s
            """%(usr_name,HID)
        remote_db.executesql(sql)
        ## 更改主表信息 ##
        sql=""" 
            UPDATE gw_doc SET cur_flow_status = 0,pre_flow_time=cur_flow_time,
            pre_flow_id = cur_flow_id,pre_flow_name=cur_flow_name,pre_flow_dept = cur_flow_dept,pre_dept_name=cur_dept_name,pre_flow_usr_id=cur_flow_usr_id,pre_user_name=cur_user_name,
            pre_opt=cur_opt,cur_flow_time = GETDATE(),cur_flow_id = %s,cur_flow_name='%s',cur_flow_dept = %s,cur_flow_usr_id = %s,cur_user_name='%s',
            next_flow_id =NULL,next_flow_name=NULL, next_flow_dept = NULL,next_dept_name=NULL, next_flow_usr_id = NULL,next_user_name=NULL
            ,IsTran=0
            WHERE id = %s
            """%(flow_id,flow_name,dept_id,usr_id,usr_name,pk)
        remote_db.executesql(sql)
        
    #获取下流程ID
    sql=" SELECT TOP 1 id FROM gw_flow_his WHERE m_id = %s AND send_flow_id = %s AND status = 0 ORDER BY id DESC "%(pk,flow_id)
    
    lT,iN = remote_db.select(sql)
    NEXTHID = lT[0][0] #下流程

    ## 将用户选择的流程更新至数据库 ##
    #改主表
    finish = 0
    doc_status = 3
    doc_flow_status = 1
    his_flow_status = 1

    status_txt = "已发送"

    sql="""
        UPDATE gw_doc SET
        next_flow_id = %s, next_flow_dept = %s, next_flow_usr_id = %s,
        status = %s, cur_flow_status = %s, finish = %s,IsTran=0, status_txt = '%s',cur_opt=%s  WHERE id = %s
        """%(VF3,next_dept_id,next_usr_id,doc_status,doc_flow_status,finish,status_txt,opt,pk)
    remote_db.executesql(sql)
   
    #改当前流程
    sql="""
        UPDATE gw_flow_his SET
        opt = %s, memo = '%s', next_flow_id = %s, next_dept =%s, next_usr_id = %s, uid = %s,
        uusrname = '%s', utime = GETDATE(), status = %s, next_role_id = %s,dirty_flag=1 WHERE id = %s
        """%(opt,memo,VF3,next_dept_id,next_usr_id,usr_id,usr_name,his_flow_status,next_role_id,HID)
    remote_db.executesql(sql)
    
    #改下一流程
    sql="""
        UPDATE gw_flow_his SET send_opt=%s,flow_id = %s, cid = %s,dirty_flag=1 WHERE id = %s 
        """%(opt,VF3,next_usr_id,NEXTHID)
    remote_db.executesql(sql)

    update_flow_text(pk,HID,NEXTHID)

    update_gw_db(pk)
    return

def update_flow_text(pk,HID,NEXTHID):
    sql=""" 
            update d set 
            pre_flow_name = pf.cname, pre_dept_name = pd.cname, pre_user_name = pu.usr_name,
            cur_flow_name = cf.cname, cur_dept_name = cd.cname, cur_user_name = cu.usr_name,
            next_flow_name = nf.cname, next_dept_name = nd.cname, next_user_name = nu.usr_name
            from gw_doc d
            left join gw_flow_def pf on pf.id = d.pre_flow_id
            left join dept pd on pd.id = d.pre_flow_dept
            left join users pu on pu.usr_id = d.pre_flow_usr_id

            left join gw_flow_def cf on cf.id = d.cur_flow_id
            left join dept cd on cd.id = d.cur_flow_dept
            left join users cu on cu.usr_id = d.cur_flow_usr_id

            left join gw_flow_def nf on nf.id = d.next_flow_id
            left join dept nd on nd.id = d.next_flow_dept
            left join users nu on nu.usr_id = d.next_flow_usr_id
            where d.id = %s
        """%pk
    remote_db.executesql(sql)
    sql=""" 
            update d set 
            next_flow_name = nf.cname, next_dept_name = nd.cname, next_usr_name = nu.usr_name,
            uusrname = cu.usr_name, next_role_name = r.role_name
            from gw_flow_his d
            left join gw_flow_def nf on nf.id = d.next_flow_id
            left join dept nd on nd.id = d.next_dept
            left join users nu on nu.usr_id = d.next_usr_id
            left join users cu on cu.usr_id = d.uid
            left join roles r on r.role_id = d.next_role_id
            where d.id = %s
        """%HID
    #print sql
    remote_db.executesql(sql)
    sql=""" 
            update d set 
            flow_name = cf.cname,cusrname = cu.usr_name
            from gw_flow_his d
            left join gw_flow_def cf on cf.id = d.flow_id
            left join users cu on cu.usr_id = d.cid
            where d.id = %s
        """%NEXTHID
    #print sql
    remote_db.executesql(sql)
    return 

def update_gw_db(pk):
           
    sql="""
                    insert into gw_db(gw_id, is_sign, flow_id, flow_name, dept_id, dept_name, usr_id, usr_name,
                    pre_flow_name, pre_dept_name, pre_user_name, pre_time)
                    select d.id, 0, cf.id, cf.cname, cd.id, cd.cname, cu.usr_id, cu.usr_name,
                    pf.cname, pd.cname, pu.usr_name, d.cur_flow_time
                    from gw_doc d
                    left join gw_flow_def cf on cf.id = d.next_flow_id
                    left join dept cd on cd.id = d.next_flow_dept
                    left join users cu on cu.usr_id = d.next_flow_usr_id
                    left join gw_flow_def pf on pf.id = d.cur_flow_id
                    left join dept pd on pd.id = d.cur_flow_dept
                    left join users pu on pu.usr_id = d.cur_flow_usr_id
                    where d.id = %s
                """%(pk)
    remote_db.executesql(sql)
    return

def getDzdList(request):
    usr_id_qy = request.session.get('usr_id_qy') or testid
    #print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    #users = getViewUserIds()
    #if str(usr_id_qy) not in users:
    #    s = """
    #    {
    #    "errcode": -1,
    #    "errmsg": "无权访问"
    #    }        """
    #    return HttpResponseJsonCORS(s)

    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    sql="""select dz.id,dz.sn,op.cname,su.cname,dz.ctime,dz.status,m.txt1 from _m3000002_dzd dz
           left join out_proj op on op.id = dz.proj_id
           left join suppliers su on su.id = dz.sup_id
           left join mtc_t m on m.id = dz.dz_type and m.type='DZLX'
           where dz.status != 0 and find_in_set(%s,dz.recv_usr_ids)
        """%(usr_id_qy)
    if search !='':
        sql+="AND ((IFNULL(dz.sn,'') LIKE '%%%s%%' ) or (IFNULL(op.cname,'') LIKE '%%%s%%' ) or (IFNULL(su.cname,'') LIKE '%%%s%%' ))"%(search,search,search)
    if situation !='':
        sql+="AND (dz.status='%s') "%(situation)
    sql+="ORDER BY dz.id DESC"
    print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    names = 'id sn proj_name sup_name ctime status ck_type'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def auditDzd(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    #users = getViewUserIds()
    #if str(usr_id_qy) not in users:
    #    s = """
    #    {
    #    "errcode": -1,
    #    "errmsg": "无权访问"
    #    }        """
    #    return HttpResponseJsonCORS(s)

    id = request.POST.get('id','')
    pass1 = request.POST.get('pass','') 
    cont = request.POST.get('cont','')
    cont = MySQLdb.escape_string(cont)
    if str(pass1) == '1':
        sql = "update _m3000002_dzd set status=2,audit_usr_id=%s,audit_time=now() where id = %s"%(usr_id_qy,id)
        db.executesql(sql)
        sql = """update _m3000004_rkd rk,_m3000002_dzd_list dz 
                 set rk.sq_money = 0,rk.dzsq_status = 0
                 where dz.rk_id = rk.id and dz.m_id = %s"""%(id) 
        db.executesql(sql)
    else:
        sql = "update _m3000002_dzd set status=3,audit_usr_id=%s,audit_time=now(),audit_cont='%s' where id = %s"%(usr_id_qy,cont,id)
        db.executesql(sql)
        sql = """update _m3000004_rkd rk,_m3000002_dzd_list dz 
                 set rk.sq_money = 0,rk.dzsq = rk.dzsq - 1,rk.dzsq_status = 0
                 where dz.rk_id = rk.id and dz.m_id = %s and dz.is_sel=1"""%(id) 
        db.executesql(sql)
      
    sql = """select op.cname,dz.sup_id,dz.sn,su.cname from _m3000002_dzd dz
                 left join out_proj op on dz.proj_id = op.id
                 left join suppliers su on su.id = dz.sup_id
                 where dz.id=%s"""%(id)
    print sql
    rows,iN = db.select(sql)
    if iN > 0:
        proj_name = rows[0][0]
        sup_id = rows[0][1]
        sn = rows[0][2]
        sup_name = rows[0][3]
        sql = """select GROUP_CONCAT(u.openid) from users_gy u 
                 left join addr_book ab on u.addr_id = ab.id
                 where ab.sup_id = %s and u.status = 1"""%(sup_id)
        rows1,iN1 = db.select(sql)
        users = rows1[0][0]
        sql = "select usr_name from users where usr_id=%s"%(usr_id_qy)
        rows1,iN1 = db.select(sql)
        usr_name = rows1[0][0]
        mWxPushMsg_Ddz(id,users,sn,proj_name,cont,pass1,sup_name,usr_name)
    s = """
        {
        "errcode": 0,
        "errmsg": "审核成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def getDzdInfo(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    
    
    sql="""select dz.id,dz.sn,op.cname,su.cname,dz.ctime,dz.status,m.txt1
           ,m1.txt1,case dz.is_gyl when 1 then '普宁市宝鹰供应链管理有限公司' else '不通过供应链公司' end,m3.txt1,dz.memo,'' from _m3000002_dzd dz
           left join out_proj op on op.id = dz.proj_id
           left join suppliers su on su.id = dz.sup_id
           left join mtc_t m on m.id = dz.dz_type and m.type='DZLX'
           left join mtc_t m1 on m1.id = dz.is_gyl and m1.type= 'YN'
           left join mtc_t m3 on m3.id = dz.cgzt and m3.type= 'cgzt'
        WHERE dz.id=%s
        """%pk
    # print sql
    rows,iN=db.select(sql)
    if iN == 0:
        s = """
        {
        "errcode": -1,
        "errmsg": "对账单已被删除"
        }        """
        return HttpResponseJsonCORS(s)

    L =[]
    for e in rows:
        L1 = list(e)
        status = e[5]
        sql = """select cg.sn,sh.sn,rk.req_no,ht.req_no,case cg.is_gyl when 1 then '是' else '否' end
                        ,mx.sh_money,rk.sh_date,rk.real_mt_price,rk.ctime,rk.yfk_money,dz.sq_money
                  from _m3000002_dzd_list dz
                  left join _m3000004_rkd rk on rk.id = dz.rk_id
                  left join _m3000004_shd sh on rk.id = sh.id
                  left join _m1501_cgdd cg on cg.id = sh.cgd_id
                  left join prj_mat_buy_ht ht on ht.id = cg.cght
                  left join (select m_id,sum(sh_qty*real_price) as sh_money from _m3000004_rkd_list group by m_id) mx on mx.m_id = rk.id
                  where dz.m_id = '%s' and dz.is_sel=1"""%pk
        rows,iN=db.select(sql)
        names = 'cg_sn sh_sn rk_sn cght gyl sh_money sh_date rk_money rk_date yfk_money sq_money'.split()
        L1[-1] = [dict(zip(names, d)) for d in rows]
        L.append(L1)
    names = 'id sn proj_name sup_name ctime status ck_type is_gyl gyl_company cgzt memo lists'.split()
    data = [dict(zip(names, d)) for d in L]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    if status == 0:
        canEdit = 1
    else:
        canEdit = 0
        
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s,
        "canEdit":%s
        }        """%(L,canEdit)
    return HttpResponseJsonCORS(s)
   
def isProjCgy(proj_id,cgy):
    sql = "SELECT usr_id FROM proj_user where proj_id = %s and usr_id=%s"%(proj_id,cgy)
    rows,iN = db.select(sql)
    if iN ==0 :
        return 0
    sql = """select u.usr_id from roles r
             left join usr_role ur  on ur.role_id = r.role_id
             left join users u on ur.usr_id = u.usr_id
             where r.role_name ='项目-仓管员'  and u.usr_id = %s"""%(cgy)
    rows,iN = db.select(sql)
    if iN ==0 :
        return 0
    return 1
def getViewUserIds():
    sql = """select u.usr_id from roles r
             left join usr_role ur  on ur.role_id = r.role_id
             left join users u on ur.usr_id = u.usr_id
             where r.role_name in ('项目-材料员','项目-仓管员')"""
    rows,iN = db.select(sql)
    users= []
    for e in rows:
        users.append(str(e[0]))
    users.append('228')
    users.append('651')
    users.append('231')
    users.append('2938')
    users.append('2110')
    users.append('2572')
    return users

import httplib
def mWxPushMsg_nopass(pk,users,sn,proj_name,cont):   
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
    template_id = 'R7redICAoEadYchqkuY8vZoUrbxSCzCeB5iIJ-1OkmQ'
    stitle ="""您提交的材料确认表有误，请更正后重新提交！"""
    stitle=json.dumps(stitle)
    keyword1 = json.dumps("采购订单:%s"%sn)
    keyword2 = json.dumps("【%s】%s"%(proj_name,cont))
    remark = json.dumps("请您登陆【供应商服务平台】进行修改")
    for e in users.split(','):
        sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#ff0000"
            },
            "keyword1": {
            "value":%s,
            "color":"#173177"
            },
            "keyword2": {
            "value":%s,
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }
            }
            }
        """%(e,template_id,stitle,keyword1,keyword2,remark)

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
        errmsg = ddata['errmsg']

    return 

def mWxPushMsg_Ddz(pk,users,sn,proj_name,cont,pass1,sup_name,usr_name):   
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
    if str(pass1) == '1':
        template_id = 'jxzMN9kYTZnhaeDRwjtbiRePfV7AWq9R-Zb52k2U49c'
        stitle = json.dumps("您提交的对账申请已经通过，请留意接收发票清单信息")
        keyword3 = json.dumps(sup_name)
        keyword4 = json.dumps(usr_name)
    else:
        template_id = 'BeQDSogamn4pYs0g2yKmUeLH-d3QwYWY0dO53ulFxio'
        stitle = json.dumps("您提交的对账申请未被通过")
        keyword3 = json.dumps(usr_name)
        keyword4 = json.dumps(cont)

    keyword1 = json.dumps(proj_name)
    keyword2 = json.dumps(sn)
    remark = json.dumps("感谢您对本公司的支持")
    for e in users.split(','):
        sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#ff0000"
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
            "value":%s,
            "color":"#173177"
            },
            "keyword4": {
            "value":%s,
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }
            }
            }
        """%(e,template_id,stitle,keyword1,keyword2,keyword3,keyword4,remark)

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
        errmsg = ddata['errmsg']

    return 