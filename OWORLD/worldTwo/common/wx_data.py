# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import os
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
from aesMsgCrypt                import WXBizMsgCrypt
import httplib
import urllib
import random
import base64,time
from django.http import HttpResponseRedirect  
exec ('from %s.share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,fs_url,front_url,m_aesKey'%prj_name) 

error_url = '%s/wx/mui/error.html'%front_url
errmsg = """
    {
    "errcode": -1,
    "errmsg": "你没有权限浏览当前页",
    }
    """ 
def check_usr(request):
    """功能：验证用户是否有访问当前功能的权限"""
    d_value = ['']*10
    #print request.POST
    if request.session.has_key('login_data_wx'):  
        d_value = request.session.get('login_data_wx','')
        #print d_value
        #if d_value[0] == 187:d_value[0] = 144
        #print d_value
        return 0,d_value
    return -1,d_value

    '''usr_id = request.session.get('usr_id', 0)
    AccessToken = request.POST.get('AccessToken') 
    wxcpt=WXBizMsgCrypt('szoworld',m_aesKey)
    ret,login_id,sTimeStamp = wxcpt.DecryptMsg(AccessToken)   
    if (ret !=0):
        return ret,d_value

    sql = """select u.usr_id,u.usr_name,d.id,d.cname,0,time_to_sec(timediff(now(),u.refresh_time)),u.expire_time,u.id
                    from (select u.usr_id,u.usr_name,u.dept_id,ul.refresh_time,ul.expire_time,ul.id  from users_login ul left join users u on u.usr_id=ul.usr_id where u.login_id='%s'  and token='%s' order by ul.login_time desc limit 1) U
                    left join dept d on d.id=u.dept_id
                    """%(login_id,AccessToken)
    rows,iN = db.select(sql)
    if iN==0:
        return -1,d_value
    #if int(usr_id) != rows[0][0]:
    #    return -1,d_value

    d_value = list(rows[0])
    #print d_value
    return 0,d_value'''

def getGwList(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)

    usr_id = d_value[0] 
    dept_id = d_value[2] 
    pageNo= request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    search_input= request.POST.get('search_input','')
    type = request.POST.get('type','1')

    if (usr_id==0 or usr_id==''):
        return HttpResponseCORS(request,errmsg)
    
    if type=='1':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(H.ctime,'%%Y-%%m-%%d')
                    ,ifnull(H.cusrname,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,ifnull(D1.cname,'')
                    ,ifnull(Ux.usr_name,'')
                    ,GD.menu_id
                    ,''
                from gw_doc GD
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_his H ON H.m_id = GD.id AND H.status = 0 
                LEFT JOIN gw_flow_def D1 ON D1.id = H.flow_id
                LEFT JOIN users Ux ON ux.usr_id = H.cid
                where (GD.finish=0 and GD.is_disable=0 and H.cid = %s) 
                """%(usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY H.ctime DESC "
    elif type=='2':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(H.ctime,'%%Y-%%m-%%d')
                    ,ifnull(H.cusrname,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,ifnull(D1.cname,'')
                    ,ifnull(Ux.usr_name,'')
                    ,GD.menu_id
                    ,''
                from gw_sign ga
                left join gw_doc gd on ga.gw_id= gd.id
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_his H ON H.m_id = GD.id AND H.status = 0 
                LEFT JOIN gw_flow_def D1 ON D1.id = H.flow_id
                LEFT JOIN users Ux ON ux.usr_id = H.cid
                where ga.usr_id = %s 
                """%(usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY ga.ctime DESC  "
    elif type=='3':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(ifnull(H.ctime,GD.cur_flow_time),'%%Y-%%m-%%d')
                    ,ifnull(H.cusrname,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,ifnull(D1.cname,'已办结')
                    ,ifnull(Ux.usr_name,'')
                    ,GD.menu_id
                    ,''
                from (
                    SELECT DISTINCT D.* FROM gw_doc D
                    LEFT JOIN gw_type gt on gt.id = D.type_id
                    WHERE D.cid=%s or FIND_IN_SET(%s,D.cybl)
                ) GD
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_def FD ON FD.id=GD.cur_flow_id
                LEFT JOIN GW_ROLE GR ON GR.GW_TYPE=GD.TYPE_ID
                LEFT JOIN gw_flow_his H ON H.m_id = GD.id AND H.status = 0 
                LEFT JOIN gw_flow_def D1 ON D1.id = H.flow_id
                LEFT JOIN users Ux ON ux.usr_id = H.cid
                WHERE GD.status not in (-1,0,7) and H.cid != %s 
                """%(usr_id,usr_id,usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY GD.cur_flow_time DESC "
    elif type=='4':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(ifnull(H.ctime,GD.cur_flow_time),'%%Y-%%m-%%d')
                    ,ifnull(H.cusrname,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,ifnull(D1.cname,'')
                    ,ifnull(Ux.usr_name,'')
                    ,GD.menu_id
                    ,D1.s_flag
                from (
                    SELECT D.* FROM gw_doc D
                    WHERE ifnull(D.finish,0)=0 and D.is_disable=0 and D.cid = %s
                ) GD
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_his H ON H.m_id = GD.id AND H.status = 0 
                LEFT JOIN gw_flow_def D1 ON D1.id = H.flow_id
                LEFT JOIN users Ux ON ux.usr_id = H.cid
                WHERE GD.status in (0,4,5) 
                """%(usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY GD.cur_flow_time DESC "
    elif type=='5':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(H.ctime,'%%Y-%%m-%%d')
                    ,ifnull(H.cusrname,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,ifnull(D1.cname,'')
                    ,ifnull(Ux.usr_name,'')
                    ,GD.menu_id
                    ,D1.s_flag
                from (
                    SELECT D.* FROM gw_doc D
                    WHERE ifnull(D.finish,0)=0 and ifnull(D.is_disable,0)=0 and D.cid = %s
                ) GD
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_his H ON H.m_id = GD.id AND H.status = 0
                LEFT JOIN gw_flow_def D1 ON D1.id = H.flow_id
                LEFT JOIN users Ux ON ux.usr_id = H.cid
                WHERE GD.status not in (0,4,5,7,8,-1)
                """%(usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY GD.cur_flow_time DESC "
    elif type=='6':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(GD.cur_flow_time,'%%Y-%%m-%%d')
                    ,ifnull(GD.cur_user_name,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,'已办结'
                    ,''
                    ,GD.menu_id
                    ,0
                from (
                    SELECT D.* FROM gw_doc D
                    WHERE D.finish=1 and D.is_disable=0 and D.status!=-1 and D.cid = %s
                ) GD
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_def FD ON FD.id=GD.cur_flow_id
                WHERE 1=1 
                """%(usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY GD.cur_flow_time DESC "
    elif type=='7':
        sql="""
                select
                    GD.id
                    ,ifnull(OP.cname,GD.title)
                    ,date_format(GD.cur_flow_time,'%%Y-%%m-%%d')
                    ,ifnull(GD.cur_user_name,'')
                    ,''
                    ,0
                    ,0
                    ,GT.cname 
                    ,GD.status_txt
                    ,GD.cur_flow_id
                    ,UC.usr_name
                    ,UC.pic
                    ,'已作废'
                    ,''
                    ,GD.menu_id
                    ,D1.s_flag
                from (
                    SELECT D.* FROM gw_doc D
                    WHERE ifnull(D.is_disable,0)=1 and D.status!=-1 and D.cid = %s
                ) GD
                LEFT JOIN gw_type GT ON GT.ID=GD.type_id
                LEFT JOIN out_proj OP ON OP.id=GD.proj_id
                LEFT JOIN users UC ON UC.usr_id=GD.cid
                LEFT JOIN gw_flow_his H ON H.m_id = GD.id AND H.status = 0 
                LEFT JOIN gw_flow_def D1 ON D1.id = H.flow_id
                LEFT JOIN users Ux ON ux.usr_id = H.cid
                WHERE 1=1
                """%(usr_id)
        if search_input!='':
            sql+=" AND concat(ifnull(GD.title,''),ifnull(OP.cname,''),ifnull(UC.usr_name,''),ifnull(OP.gc_no,'')) LIKE '%%%s%%'"%(search_input)
        sql+=" ORDER BY GD.cur_flow_time DESC "
    #print sql
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    L = []
    for e in rows:
        L2 = list(e)
        pic = L2[11]
        if pic=='':
            L2[11] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L2[11] = "%s/user_pic/small_%s"%(fs_url,pic)

        L.append(L2)

    names = 'id title cur_flow_time usr_name1 sUrl can_update atta_update gw_type status cur_flow_id send_usr_name pic gw_flow_def audit_usr_name menu_id s_flag'.split()
    data = [dict(zip(names, d)) for d in L]
    s = json.dumps(data,ensure_ascii=False)

    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "gwArray":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s,
        }
        """%(s,iTotal_length,iTotal_Page,pageNo,select_size)
    #print s1
    return HttpResponseCORS(request,s1)

def getInfoList(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)

    usr_id = d_value[0] 
    dept_id = d_value[2] 
    pageNo= request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    typeCode= request.POST.get('typeCode','')
    orderby= request.POST.get('orderby','')

    type = request.POST.get('type','infoRead')

    if (usr_id==0 or usr_id==''):
        return HttpResponseCORS(request,errmsg)


    if type=='infoRead':
        sql ="""SELECT  
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,left(WB.content,300)
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,ifnull(WB.ifaud,0)
                    ,NT.cname
                    ,D.cname
                    ,ifnull(WB.must_reply,0)
                    ,ifnull(U.pic,'')
                    ,date_format(MD.lytime,'%%Y-%%m-%%d %%T')
                    ,date_format(RLOG.read_time,'%%Y-%%m-%%d %%T')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               LEFT JOIN (
                   select DISTINCT bb_id from bumph_bubbl_groups where group_id in (
                       select id from news_group where is_all=1 or find_in_set(%s,depts) or find_in_set(%s,users))
               ) G ON G.bb_id=WB.id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where (G.bb_id is not NULL or find_in_set(%s,recv_users)) and ifnull(audit,3) >= 2
            """%(dept_id,usr_id,usr_id,usr_id)
        if typeCode !='':
            sql += " and gw_type='%s'"%typeCode
        if str(orderby)=='1':
            sql+=" ORDER BY l_flag desc,case when WB.ref_date >= MD.lytime then WB.ref_date else MD.lytime end desc"      #未读留言+留言时间最新排前
        else:
            sql+=" ORDER BY WB.ref_date desc"                #未读信息+信息发布时间最新排前
        names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic lytime read_time l_flag'.split()
    elif type=='beSent':
        sql ="""SELECT  
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,left(WB.content,300)
                    ,date_format(WB.ctime,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,ifnull(WB.ifaud,0)
                    ,NT.cname
                    ,D.cname
                    ,ifnull(WB.must_reply,0)
                    ,ifnull(U.pic,'')
                    ,date_format(MD.lytime,'%%Y-%%m-%%d %%T')
                    ,date_format(RLOG.read_time,'%%Y-%%m-%%d %%T')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
                    ,ifnull(WB.audit,3)
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where Wb.cid=%s and WB.audit in (1,2,3)
            """%(usr_id,usr_id)
        if typeCode !='':
            sql += " and gw_type='%s'"%typeCode
        sql+=" ORDER BY WB.ctime desc"               
        names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic lytime read_time l_flag audit'.split()
    elif type=='waitSend':
        sql ="""SELECT  
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,left(WB.content,300)
                    ,date_format(WB.ctime,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,ifnull(WB.ifaud,0)
                    ,NT.cname
                    ,D.cname
                    ,ifnull(WB.must_reply,0)
                    ,ifnull(U.pic,'')
                    ,date_format(MD.lytime,'%%Y-%%m-%%d %%T')
                    ,date_format(RLOG.read_time,'%%Y-%%m-%%d %%T')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
                    ,ifnull(WB.audit,3)
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where Wb.cid=%s and WB.audit in (-1,0)
            """%(usr_id,usr_id)
        if typeCode !='':
            sql += " and gw_type='%s'"%typeCode
        sql+=" ORDER BY WB.ctime desc"               
        names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic lytime read_time l_flag audit'.split()
    elif type=='beTrash':
        sql ="""SELECT  
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,left(WB.content,300)
                    ,date_format(WB.ctime,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,ifnull(WB.ifaud,0)
                    ,NT.cname
                    ,D.cname
                    ,ifnull(WB.must_reply,0)
                    ,ifnull(U.pic,'')
                    ,date_format(MD.lytime,'%%Y-%%m-%%d %%T')
                    ,date_format(RLOG.read_time,'%%Y-%%m-%%d %%T')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
                    ,ifnull(WB.audit,3)
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where Wb.cid=%s and WB.audit in (-2)
            """%(usr_id,usr_id)
        if typeCode !='':
            sql += " and gw_type='%s'"%typeCode
        sql+=" ORDER BY WB.ctime desc"               
        names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic lytime read_time l_flag audit'.split()
    elif type=='beAudited':
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
               where WB.audusrid=%s and WB.audit in (-2,-1,2)
            """%(usr_id)
        names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic audit'.split()
    elif type=='waitAudit':
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
               where WB.audusrid=%s and WB.audit in (1)
            """%(usr_id)
        names = 'seq r_flag title content ref_date usr_name needsh news_type dept must_reply pic audit'.split()
    print ToGBK(sql)
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
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
    s = json.dumps(data,ensure_ascii=False)

    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "infoArray":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s,
        }
        """%(s,iTotal_length,iTotal_Page,pageNo,select_size)
    #print s1
    return HttpResponseCORS(request,s1)

def getInfoDetail(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)

    usr_id = d_value[0] 
    dept_id = d_value[2] 

    seq= request.POST.get('seq','')
    index=  request.POST.get('index','1')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  

    if (usr_id==0 or usr_id==''):
        return HttpResponseCORS(request,errmsg)
    if (seq==0 or seq==''):
        return HttpResponseCORS(request,errmsg)

    sql="""INSERT INTO bumph_bubbl_read_log(bb_id,read_time,usr_id,remote_ip)
               VALUES(%s,now(),'%s','%s')
            """%(seq,usr_id,ip)
    #print sql
    db.executesql(sql)

    sql="""SELECT WB.id                                    
                    ,WB.title                                  
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')   
                    ,U.usr_name                             
                    ,D.cname
                    ,ifnull(U.pic,'')
                    ,ifnull(must_reply,0)                  
                    ,WB.content                        
                    ,WB.gw_type
                    ,WB.audit
                    ,WB.audusrid
                    ,U1.usr_name
                    ,NT.cname
                    ,ifnull(A.explain,'')
                    ,date_format(A.audit_time,'%%Y-%%m-%%d %%T')
                    ,A.status
                FROM bumph_bubbl WB
                Left join bumph_bubbl_audit A on A.bb_id=WB.id
                LEFT JOIN users U ON WB.cid=U.usr_id
                LEFT JOIN users U1 ON WB.audusrid=U1.usr_id
                LEFT JOIN dept D ON D.id=U.dept_id
                LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
                WHERE WB.id=%s order by A.audit_time desc limit 1
            """%(seq)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    if iN == 0:
        errmsg = """
            {
            "errcode": -1,
            "errmsg": "该条记录已被删除",
            }
            """ 
        return HttpResponseCORS(request,errmsg)

    if str(index)=='1':
        names = 'seq title ref_date usr_name dept pic must_reply content gw_type audit audusrid audusr_name gw_type_name explain audit_time auditstatus'.split()
    else:
        names = 'seq title ref_date usr_name dept pic must_reply content gw_type audit audusrid audusr_name gw_type_name'.split()

    L = []
    for e in rows:
        L2 = list(e)
        pic = L2[5]
        if pic=='':
            L2[5] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L2[5] = "%s/user_pic/small_%s"%(fs_url,pic)

        L.append(L2)

    data = [dict(zip(names, d)) for d in L]
    s = json.dumps(data,ensure_ascii=False)

    sql="""SELECT U.usr_name,U.usr_id
                    FROM bumph_bubbl BB
                    LEFT JOIN users U on FIND_IN_SET(U.usr_id,BB.`recv_users` )
                    WHERE BB.id=%s  order by U.sort desc"""%seq        
    rows,iN = db.select(sql)
    names = 'usr_name usr_id'.split()
    data = [dict(zip(names, d)) for d in rows]
    s1 = json.dumps(data,ensure_ascii=False)

    sql="""SELECT G.cname,G.id,G.`must_audit` 
                    FROM bumph_bubbl_groups BB
                    LEFT JOIN news_group G on G.id =BB.group_id
                    WHERE BB.bb_id=%s order by sort desc"""%seq        
    rows,iN = db.select(sql)
    names = 'group_name id must_audit'.split()
    data = [dict(zip(names, d)) for d in rows]
    s2 = json.dumps(data,ensure_ascii=False)

    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "content":%s,
        "readPerson":%s,
        "readGroup":%s,
        }
        """%(s,s1,s2)
    #print s1
    return HttpResponseCORS(request,s1)

def getInfoComment(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)

    usr_id = d_value[0] 
    dept_id = d_value[2] 

    seq= request.POST.get('seq','')
    pageNo= request.POST.get('pageNo') or 1
    pageNo=int(pageNo)

    if (usr_id==0 or usr_id==''):
        return HttpResponseCORS(request,errmsg)
 
    sql="""select C.id,U.usr_name,date_format(C.ctime,'%%Y-%%m-%%d %%T'),U.pic,C.cont 
                    from bumph_bubbl_comment C
                    left join users U on U.usr_id=C.cid
                    where bb_id=%s 
                    order by C.id desc
                 """%seq
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id usr_name ctime pic cont'.split()

    L = []
    for e in rows:
        L2 = list(e)
        pic = L2[3]
        if pic=='':
            L2[3] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L2[3] = "%s/user_pic/small_%s"%(fs_url,pic)

        L.append(L2)

    data = [dict(zip(names, d)) for d in L]
    s = json.dumps(data,ensure_ascii=False)

    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "commentArray":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s,
        }
        """%(s,iTotal_length,iTotal_Page,pageNo,select_size)
    return HttpResponseCORS(request,s1)

def infoType(request):
    #ret,d_value = check_usr(request)
    #if ret != 0:
    #    return HttpResponseCORS(request,errmsg)

    #usr_id = d_value[0] 

    sql="""SELECT type_code,cname
                FROM news_type
                WHERE news_group = 'info' and status=1
                ORDER BY type_code
            """
    rows,iN = db.select(sql)
    names = 'code name'.split()
    data = [dict(zip(names, d)) for d in rows]

    s = json.dumps(data,ensure_ascii=False)
    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "infoTypeArray":%s,
        }
        """%(s)
    #print s1
    return HttpResponseCORS(request,s1)

def getDepts(request):
    parent_id= request.POST.get('parent_id') or 0

    sql="""SELECT id,cname,parent_id
                FROM dept D
                WHERE  ifnull(del_flag,0)=0 
            """
    if parent_id!=0:
        sql += """ and parent_id=%s"""%parent_id
    sql += " ORDER BY parent_id "
    #print sql
    rows,iN = db.select(sql)
    names = 'id name parent_id'.split()
    data = [dict(zip(names, d)) for d in rows]

    s = json.dumps(data,ensure_ascii=False)
    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "deptArray":%s,
        }
        """%(s)
    #print s1
    return HttpResponseCORS(request,s1)

def getUsers(request):
    dept_id= request.POST.get('dept_id','')
    search= request.POST.get('search','')
    usr_id = request.session.get('usr_id', 0)
    sql="""SELECT U.usr_id,U.login_id,U.usr_name,ifnull(U.pic,''),D.cname,D.id
                FROM users U
                left join dept D on D.id=U.dept_id
                WHERE U.status = 1 and u.usr_id not in (1,2,%s)
            """%(usr_id)
    if dept_id!='':
        sql += """ and U.dept_id=%s"""%dept_id
    if search!='':
        sql += """ and U.usr_name like '%%%s%%'"""%search
    sql += " ORDER BY U.usr_name "
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L2 = list(e)
        pic = L2[3]
        if pic=='':
            L2[3] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L2[3] = "%s/user_pic/small_%s"%(fs_url,pic)

        L.append(L2)

    names = 'usr_id login_id usr_name pic dept_name dept_id'.split()
    data = [dict(zip(names, d)) for d in L]

    s = json.dumps(data,ensure_ascii=False)
    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "userArray":%s,
        }
        """%(s)
    #print s1
    return HttpResponseCORS(request,s1)

def getInfoGroup(request):
    sql="""SELECT id,cname,ifnull(must_audit,0)  FROM news_group order by sort desc"""
 
    rows,iN = db.select(sql)
    names = 'gid name must_audit'.split()
    data = [dict(zip(names, d)) for d in rows]

    s = json.dumps(data,ensure_ascii=False)
    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "groupArray":%s,
        }
        """%(s)
    #print s1
    return HttpResponseCORS(request,s1)

def getAuditUser(request):
    #usr_id = request.session.get('usr_id', 0)
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)

    usr_id = d_value[0] 

    sql = """select
                    iv.audtype
                    ,iv.auduser
                    ,ur.usr_name
                from infoaudsort_view iv
                left join users ur on ur.usr_id = iv.auduser
                where iv.usr_id = %s
            """ % usr_id 
    #print sql
    rows,iN = db.select(sql)
    names = 'audtype auduser usr_name'.split()

    data = [dict(zip(names, d)) for d in rows]

    s = json.dumps(data,ensure_ascii=False)
    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取列表成功",
        "auditArray":%s,
        }
        """%(s)
    #print s1
    return HttpResponseCORS(request,s1)
