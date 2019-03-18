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
import httplib
from django.db import connection
from share import db,HttpResponseCORS,g_data,ToGBK,mValidateUser,fs_url

def home_func(request):
    audit_data = ['','']
    ret,errmsg,d_value = mValidateUser(request,"view",'')
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    dept_id = d_value[2]
    sql = "select cname,start_s,end_s,style from chkdatetime order by end_s"
    lT1,iN1 = db.select(sql)

    sql = """SELECT case source when 1 then ga.title 
                     else case ifnull(d.title,'') when '' then concat(op.gc_no,'/',op.cname)
                      else d.title
                     end
                    end,
                    case source when 1 then ga.type_name
                    else gfd.cname
                    end,
                    ga.cusrname,
                    date_format(ga.ctime,'%%Y-%%m-%%d %%T'),
                    d.menu_id,
                    d.id,
                    '',
                    ifnull(ga.url,''),
                    TIMESTAMPDIFF(SECOND,ga.ctime,now())/60,
                    datediff(now(),ga.ctime)
              FROM gw_audit ga
              left join gw_doc d on ga.gw_id= d.id
              left join gw_type gfd on ga.type_id= gfd.id
              left join out_proj op on op.id= d.proj_id
             where ga.usr_id= '%s' order by ga.ctime desc"""%(usr_id)
    #print sql
    lT,iN = db.select(sql)
    L = []
    iN2 = iN
    if iN2 > 10: iN2 = 10
    for i in range(0,iN2):
        e = list(lT[i])
        i = 0
        for a in lT1:
            if e[9]>30: e[8] = e[9]*1440
            if float(e[8]) < float(a[2]):
                if i < iN1:
                    e[3] = a[0]
                    e[6] = a[3]
                else:
                    e[3] = '1年前'
                break
            i+=1
        L.append(e)

    names = 'title gw_type usr_name ctime menu_id pk style url'.split()
    data = [dict(zip(names, d)) for d in L]
    audit_data[0] = data
    audit_data[1] = iN
    names = 'data count'.split()
    L1 = dict(zip(names, audit_data))
    audit = json.dumps(L1,ensure_ascii=False)
 
    sign_data = ['','']
    sql = """SELECT ifnull(ga.title, op.cname),
                    case source when 1 then ga.type_name
                    else gfd.cname
                    end,
                    ga.cusrname,
                    date_format(ga.ctime,'%%Y-%%m-%%d %%T'),
                    d.menu_id,
                    d.id,
                    '',
                    ifnull(ga.url,''),
                    TIMESTAMPDIFF(SECOND,ga.ctime,now())/60,
                    datediff(now(),ga.ctime)
              FROM gw_sign ga
              left join gw_doc d on ga.gw_id= d.id
              left join gw_type gfd on ga.type_id= gfd.id
              left join out_proj op on op.id= d.proj_id
             where ga.usr_id= %s order by ga.ctime desc """%(usr_id)
    lT,iN = db.select(sql)
    L = []
    iN2 = iN
    if iN2 > 10: iN2 = 10
    for i in range(0,iN2):
        e = list(lT[i])
        i = 0
        for a in lT1:
            if e[9]>30: e[8] = e[9]*1440
            if float(e[8]) < float(a[2]):
                if i < iN1:
                    e[3] = a[0]
                    e[6] = a[3]
                else:
                    e[3] = '1年前'
                break
            i+=1
        L.append(e)

    names = 'title gw_type usr_name ctime menu_id pk style url'.split()
    data = [dict(zip(names, d)) for d in L]
    sign_data[0] = data
    sign_data[1] = iN
    names = 'data count'.split()
    L1 = dict(zip(names, sign_data))
    sign = json.dumps(L1,ensure_ascii=False)

    sql = """SELECT 
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,NT.cname
                    ,ifnull(U.pic,'')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
                    ,TIMESTAMPDIFF(SECOND,WB.ref_date,now())/60
                    ,''
                    ,datediff(now(),ifnull(WB.ref_date,now()))
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN (
                   select DISTINCT bb_id from bumph_bubbl_groups where group_id in (
                       select id from news_group where is_all=1 or find_in_set(%s,depts) or find_in_set(%s,users))
               ) G ON G.bb_id=WB.id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where (G.bb_id is not NULL or find_in_set(%s,recv_users)) and ifnull(audit,3) >= 2 and gw_type = 'A05'
               order by WB.ref_date desc limit 10"""%(dept_id,usr_id,usr_id,usr_id)
    #print sql
    lT,iN = db.select(sql)
    L = []
    for i in range(0,iN):
        e = list(lT[i])
        i = 0
        for a in lT1:
            if e[10]>30: e[8] = e[10]*1440
            if float(e[8]) < float(a[2]):
                if i < iN1:
                    e[8] = a[0]
                    e[9] = a[3]
                else:
                    e[8] = '1年前'
                break
            i+=1
        L.append(e)

    names = 'id r_flag title ref_date cusrname news_type pic l_flag timediff style'.split()
    data = [dict(zip(names, d)) for d in L]
    notice = json.dumps(data,ensure_ascii=False)
               

    sql = """SELECT 
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,NT.cname
                    ,ifnull(U.pic,'')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
                    ,TIMESTAMPDIFF(SECOND,WB.ref_date,now())/60
                    ,''
                    ,datediff(now(),ifnull(WB.ref_date,now()))
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN (
                   select DISTINCT bb_id from bumph_bubbl_groups where group_id in (
                       select id from news_group where is_all=1 or find_in_set(%s,depts) or find_in_set(%s,users))
               ) G ON G.bb_id=WB.id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where (G.bb_id is not NULL or find_in_set(%s,recv_users)) and ifnull(audit,3) >= 2 and gw_type != 'A05'
               order by WB.ref_date desc limit 10"""%(dept_id,usr_id,usr_id,usr_id)
    #print sql
    lT,iN = db.select(sql)
    L = []
    for i in range(0,iN):
        e = list(lT[i])
        i = 0
        for a in lT1:
            if e[10]>30: e[8] = e[10]*1440
            if float(e[8]) < float(a[2]):
                if i < iN1:
                    e[8] = a[0]
                    e[9] = a[3]
                else:
                    e[8] = '1年前'
                break
            i+=1
        pic = e[6]
        if pic=='':
            e[6] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            e[6] = "%s/user_pic/small_%s"%(fs_url,pic)
        L.append(e)

    names = 'id r_flag title ref_date cusrname news_type pic l_flag timediff style'.split()
    data = [dict(zip(names, d)) for d in L]
    recv_info = json.dumps(data,ensure_ascii=False)

    sql ="""SELECT  
                    WB.id
                    ,0
                    ,WB.title
                    ,left(WB.content,300)
                    ,date_format(WB.ctime,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,ifnull(WB.ifaud,0)
                    ,NT.cname
                    ,D.cname
                    ,ifnull(WB.must_reply,0)
                    ,ifnull(U.pic,'')
                    ,ifnull(WB.audit,3)
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               where WB.audusrid=%s and WB.audit in (1) order by WB.ctime desc limit 10
            """%(usr_id)
    names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic audit'.split()
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L2 = list(e)
        pic = L2[10]
        if pic=='':
            L2[10] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L2[10] = "%s/user_pic/small_%s"%(fs_url,pic)

        L.append(L2)

    data = [dict(zip(names, d)) for d in L]
    waitAudit = json.dumps(data,ensure_ascii=False)

    sql = """SELECT 
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,NT.cname
                    ,ifnull(U.pic,'')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
                    ,TIMESTAMPDIFF(SECOND,WB.ref_date,now())/60
                    ,''
                    ,datediff(now(),ifnull(WB.ref_date,now()))
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN (
                   select DISTINCT bb_id from bumph_bubbl_groups where group_id in (
                       select id from news_group where is_all=1 or find_in_set(%s,depts) or find_in_set(%s,users))
               ) G ON G.bb_id=WB.id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where (G.bb_id is not NULL or find_in_set(%s,recv_users)) and ifnull(audit,3) >= 2 and gw_type = 'A09'
               order by WB.ref_date desc limit 10"""%(dept_id,usr_id,usr_id,usr_id)
    #print sql
    lT,iN = db.select(sql)
    L = []
    for i in range(0,iN):
        e = list(lT[i])
        i = 0
        for a in lT1:
            if e[10]>30: e[8] = e[10]*1440
            if float(e[8]) < float(a[2]):
                if i < iN1:
                    e[8] = a[0]
                    e[9] = a[3]
                else:
                    e[8] = '1年前'
                break
            i+=1
        L.append(e)

    names = 'id r_flag title ref_date cusrname news_type pic l_flag timediff style'.split()
    data = [dict(zip(names, d)) for d in L]
    zhidu = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取主页数据成功",
        "audit":%s,
        "sign":%s,
        "notice":%s,
        "zhidu":%s,
        "recv_info":%s,
        "audit_info":%s
        }        """%(audit,sign,notice,zhidu,recv_info,waitAudit)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)
