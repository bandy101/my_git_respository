# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
import random
import MySQLdb
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS,ToGBK,fs_url'%prj_name) 
exec ('from %s.wx_cb.wxpush        import mWxPushMsg_Info'%prj_name)   

def getInfoAttribute(request,title,menu):
    data = request.POST.get('data', '{}')
    data_list = json.loads(data)
    gw_type = data_list.get('gw_type','')
    SL = []
    L1 = ['公文类别',0, 'gw_type', 2, 1, '', 4, '']
    L1[5] = get_type_data(gw_type)
    names = 'cname txt_show ename type sort data span url'.split()
    SL.append(L1)
    data = [dict(zip(names, d)) for d in SL]
    filter = json.dumps(data,ensure_ascii=False)
    

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户管理页面成功",
        "title":"%s",
        "menu":%s,
        "filter":%s,
        }        """%(title,menu,filter)
    #print s
    return HttpResponseCORS(request,s)

def getInfoList(request,usr_id,dept_id):
    tab = request.POST.get('tab', '')
    data = request.POST.get('data', '{}')
    data_list = json.loads(data)
    aoData= request.POST.get('aoData', '')

    select_size = 10
    startNo = 0

    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1
    readSortFlag = data_list.get('readSortFlag','')
    gw_type = data_list.get('gw_type','')

    sql = """SELECT 
                    WB.id
                    ,CASE ifnull(RLOG.bb_id,'0') WHEN '0' THEN '0' ELSE '1' END as r_flag
                    ,WB.title
                    ,left(WB.content,300)
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,NT.cname
                    ,ifnull(U.pic,'')
                    ,case when ifnull(MD.lytime,'')>ifnull(RLOG.read_time,'') then 1 else 0 end as l_flag
               FROM bumph_bubbl WB
               LEFT JOIN users U ON WB.cid=U.usr_id
               LEFT JOIN (
                   select DISTINCT bb_id from bumph_bubbl_groups where group_id in (
                       select id from news_group where is_all=1 or find_in_set(%s,depts) or find_in_set(%s,users))
               ) G ON G.bb_id=WB.id
               LEFT JOIN (select bb_id,usr_id,MAX(read_time) as read_time from bumph_bubbl_read_log where usr_id = %s group by bb_id,usr_id) RLOG ON RLOG.bb_id=WB.id
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN (select bb_id,MAX(ctime) as lytime from bumph_bubbl_comment group by bb_id) MD on MD.bb_id = WB.id
               where (G.bb_id is not NULL or find_in_set(%s,recv_users)) and ifnull(audit,3) >= 2
          """%(dept_id,usr_id,usr_id,usr_id)
    if gw_type !='':
        sql += " and gw_type='%s'"%gw_type
    if qqid !='':
        sql += " and  CONCAT(IFNULL(WB.title,''),IFNULL(WB.cusrname,'')) LIKE '%%%s%%' "%qqid
    if str(readSortFlag) == 'True':
        sql+=" ORDER BY l_flag desc,case when WB.ref_date >= MD.lytime then WB.ref_date else MD.lytime end desc"      #未读留言+留言时间最新排前
    else:
        sql+=" ORDER BY WB.ref_date desc"                #未读信息+信息发布时间最新排前
    print ToGBK(sql)
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,select_size)
    L = []
    for e in rows:
        L1 = list(e)
        pic = e[7]
        if pic=='':
            L1[7] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L1[7] = "%s/user_pic/small_%s"%(fs_url,pic)
        L.append(L1)
    names = 'id r_flag title content ref_date cusrname news_type pic l_flag'.split()
    data = [dict(zip(names, d)) for d in L]
    info = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户列表成功",
        "userList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(info,iTotal_length,iTotal_Page,pageNo,select_size)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getInfoFormView(request,pk,usr_id,title,menu):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  

    sql="""INSERT INTO bumph_bubbl_read_log (bb_id,read_time,usr_id,remote_ip)
               VALUES(%s,now(),'%s','%s')
            """%(pk,usr_id,ip)
    #print sql
    db.executesql(sql)

    sql = """select WB.id
                    ,WB.title
                    ,WB.content
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,WB.cusrname
                    ,NT.cname
                    ,ifnull(U.pic,'')
                    ,bb_groups(WB.id)
                    ,bb_users(WB.id)
                    ,ifnull(WB.must_reply,0)                      
               FROM bumph_bubbl WB
               LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
               LEFT JOIN users U ON WB.cid=U.usr_id
               WHERE WB.id='%s' 
               Limit 1
          """%(pk)
    rows,iN = db.select(sql)
    if iN >0:
        L = list(rows[0])
        pic = L[6]
        if pic=='':
            L[6] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L[6] = "%s/user_pic/small_%s"%(fs_url,pic)
    else:
        L = []
    names = 'id title content ref_date cusrname news_type pic groups users can_reply'.split()
    data = [dict(zip(names, L))]
    infoData = json.dumps(data,ensure_ascii=False)

    sql="""select C.id,U.usr_name,date_format(C.ctime,'%%Y-%%m-%%d %%T'),U.pic,C.cont 
                    from bumph_bubbl_comment C
                    left join users U on U.usr_id=C.cid
                    where bb_id=%s 
                    order by C.id desc
                 """%pk
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L1 = list(e)
        pic = e[3]
        if pic=='':
            L1[3] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L1[3] = "%s/user_pic/small_%s"%(fs_url,pic)
        L.append(L1)
    names = 'id usr_name ctime pic cont'.split()
    data = [dict(zip(names, d)) for d in L]
    commentData = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode":0,
        "errmsg":"",
        "title":"%s",
        "menu":%s,
        "infoData":%s,
        "commentData":%s,
        }
        """%(title,menu,infoData,commentData)
    return HttpResponseCORS(request,s)

def getInfoAuditHis(pk):
    if pk=='':
        return []
    sql = """SELECT u.usr_name
                    ,ifnull(date_format(audit_time,'%%Y-%%m-%%d %%T'),'')
                    ,case BA.status when 1 then '未办理' 
                        when 2 then '通过'
                        when -1 then '退回'
                        when -2 then '作废'
                    end,
                    ifnull(BA.explain,''), u.pic,'信息审核',
                   '',BA.id
                   FROM bumph_bubbl_audit BA
                   Left join users u on BA.audit_user = u.usr_id
                   WHERE BA.bb_id=%s 
                   ORDER BY BA.id DESC
          """%pk
    #print ToGBK(sql)
    names = 'name time suggest content pic flow_name sign'.split()
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L1 = list(e)
        pic = L1[4]
        if pic=='':
            L1[4] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L1[4] = "%s/user_pic/small_%s"%(fs_url,pic)
        L.append(L1)
    data = [dict(zip(names, d)) for d in L]
    return data

def saveComment(request,d_value):
    #print request.POST
    pk =  request.POST.get('pk','')
    msgValue = request.POST.get('msgValue','')
    usr_id = d_value[0]
    usr_name = d_value[1]
    sql="""insert bumph_bubbl_comment (bb_id,cont,cid,ctime,cusrname) values (%s,'%s',%s,now(),'%s') 
                 """%(pk,msgValue,usr_id,usr_name)
    #print ToGBK(sql)
    db.executesql(sql)
    sql = "select last_insert_id();"
    rows,iN = db.select(sql)
    id =  rows[0][0]
    push_comment_msg(id,usr_id,usr_name)
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def saveInfo(request,d_value):
    #print request.GET
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    pk =  data_list.get('pk','')

    is_send = request.GET.get('is_send','')
    is_audit = request.GET.get('is_audit','')
    is_send = is_send.replace('/','')
    is_audit = is_audit.replace('/','')
    usr_id = d_value[0]
    usr_name = d_value[1]
 
    if str(is_audit) == '1':
        audit = data_list.get('audit','')
        explain = data_list.get('explain','')
        sql="update bumph_bubbl set audit = %s,audusrname='%s',audtime=now(),ref_date = now() where id = %s"%(audit,usr_name,pk)
        db.executesql(sql)

        sql="""insert into bumph_bubbl_audit (bb_id,audit_user,audit_time,status,`explain`)
                    values(%s,%s,now(),%s,'%s')
                """%(pk,usr_id,audit,explain)   
        #print ToGBK(sql)
        db.executesql(sql)
        push_audited_msg(pk,usr_id,usr_name)
        if str(audit)=='2':
            push_sendinfo_msg(pk,usr_id,usr_name)
    else:
        title = data_list.get('title','')
        gw_type = data_list.get('gw_type','')
        ifaud = data_list.get('ifaud','')
        audusrid = data_list.get('audusrid') or 'NULL'
        audusrname = data_list.get('audusrname','')
        content = data_list.get('content','')
        content = MySQLdb.escape_string(content)
        must_reply = data_list.get('must_reply','')
        recv_users = data_list.get('recv_users','')
        recv_groups = data_list.get('recv_groups','')
        ifaud = handleMutilValue(ifaud,1)
        must_reply = handleMutilValue(must_reply,1)
       
        if (str(is_send)=='0'):
            audit1=0
        elif(str(ifaud)=='0'):
            audit1=3
        else:
            audit1=1

        if pk=='':
            sql="""insert bumph_bubbl (title,content,gw_type,must_reply,ifaud,audit,audusrid,audusrname
                                       ,recv_users,recv_groups,cid,cusrname,pub_user,ctime,ref_date) 
                               values ('%s','%s','%s',%s,%s,%s,%s,'%s'
                                       ,'%s','%s',%s,'%s','%s',now(),now()) 
                     """%(title,content,gw_type,must_reply,ifaud,audit1,audusrid,audusrname
                         ,recv_users,recv_groups,usr_id,usr_name,usr_name)
            #print ToGBK(sql)
            db.executesql(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
            pk =  rows[0][0]
        else:
            sql="""update bumph_bubbl set title='%s'
                                        ,content='%s'
                                        ,gw_type='%s'
                                        ,must_reply=%s
                                        ,ifaud=%s
                                        ,audit=%s
                                        ,audusrid='%s'
                                        ,audusrname='%s'
                                        ,recv_users='%s'
                                        ,recv_groups='%s'
                                        ,uid=%s
                                        ,uusrname='%s'
                                        ,utime = now()
                                        ,utime = now()
                    where id=%s
                """%(title,content,gw_type,must_reply,ifaud,audit1,audusrid,audusrname,recv_users,recv_groups,usr_id,usr_name,pk)
            #print ToGBK(sql)
            db.executesql(sql)
            sql = " DELETE FROM bumph_bubbl_groups WHERE bb_id=%s" %(pk)
            db.executesql(sql)
    
        lD = list(recv_groups.split(','))
        sql1 = ''
        if lD != ['']:
            for e in lD:
                sql1 += "INSERT INTO bumph_bubbl_groups(bb_id,group_id) VALUES(%s,%s); \n" %(pk, e)
            #print sql1
            db.executesql(sql1)
        if audit1==3:
            push_sendinfo_msg(pk,usr_id,usr_name)
        elif audit1==1:
            push_needaudit_msg(pk,usr_id,usr_name)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def saveWxComment(request):
    ret,errmsg,d_value = mValidateUser(request,"add",'10202')
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    pk =  request.POST.get('seq','')
    cont =  request.POST.get('cont','')
    cont = MySQLdb.escape_string(cont)
    usr_id = d_value[0]
    usr_name = d_value[1]
    sql="""insert bumph_bubbl_comment (bb_id,cont,cid,ctime,cusrname) values (%s,'%s',%s,now(),'%s') 
                 """%(pk,cont,usr_id,usr_name)
    #print ToGBK(sql)
    db.executesql(sql)
    sql = "select last_insert_id();"
    rows,iN = db.select(sql)
    id =  rows[0][0]
    push_comment_msg(id,usr_id,usr_name)
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def saveWxInfo(request):
    ret,errmsg,d_value = mValidateUser(request,"add",'10202')
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    title =  request.POST.get('title','')
    gw_type =  request.POST.get('gw_type','')
    audit =  request.POST.get('audit','')
    audusrid =  request.POST.get('audusrid') or 'NULL'
    content =  request.POST.get('content','')
    content = MySQLdb.escape_string(content)
    must_reply =  request.POST.get('must_reply','')
    user_list =  request.POST.getlist('user_list[]','')
    group_list =  request.POST.getlist('group_list[]','')
    is_send =  request.POST.get('is_send','')
    pk =  request.POST.get('seq','')

    usr_id = d_value[0]
    usr_name = d_value[1]

    audusrname = ''
    if audusrid!='':
        sql = "select usr_name from users where usr_id=%s"%audusrid
        rows,iN = db.select(sql)
        if iN>0:
            audusrname =  rows[0][0]

    if (str(is_send)=='0'):
        audit1=0
    elif(str(audit)=='0'):
        audit1=3
    else:
        audit1=1
    recv_users = ''
    for e in user_list:
        recv_users += "%s,"%e
    recv_groups = ''
    for e in group_list:
        recv_groups += "%s,"%e
    if pk=='':
        sql="""insert bumph_bubbl (title,content,gw_type,must_reply,ifaud,audit,audusrid,audusrname
                                   ,recv_users,recv_groups,cid,cusrname,pub_user,ctime,ref_date) 
                           values ('%s','%s','%s',%s,%s,%s,%s,'%s'
                                   ,'%s','%s',%s,'%s','%s',now(),now()) 
                 """%(title,content,gw_type,must_reply,audit,audit1,audusrid,audusrname
                     ,recv_users,recv_groups,usr_id,usr_name,usr_name)
        #print ToGBK(sql)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        pk =  rows[0][0]
    else:
        sql="""update bumph_bubbl set title='%s'
                                    ,content='%s'
                                    ,gw_type='%s'
                                    ,must_reply=%s
                                    ,ifaud=%s
                                    ,audit=%s
                                    ,audusrid='%s'
                                    ,audusrname='%s'
                                    ,recv_users='%s'
                                    ,recv_groups='%s'
                                    ,uid=%s
                                    ,uusrname='%s'
                                    ,utime = now()
                                    ,ref_date = now()
                where id=%s
            """%(title,content,gw_type,must_reply,audit,audit1,audusrid,audusrname,recv_users,recv_groups,usr_id,usr_name,pk)
        #print ToGBK(sql)
        db.executesql(sql)
        sql = " DELETE FROM bumph_bubbl_groups WHERE bb_id=%s" %(pk)
        db.executesql(sql)
    
    sql1 = ''
    for e in group_list:
        sql1 = "INSERT INTO bumph_bubbl_groups(bb_id,group_id) VALUES(%s,%s); " %(pk, e)
        db.executesql(sql1)
    if audit1==3:
        push_sendinfo_msg(pk,usr_id,usr_name)
    elif audit1==1:
        push_needaudit_msg(pk,usr_id,usr_name)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def auditWxInfo(request):
    ret,errmsg,d_value = mValidateUser(request,"add",'10202')
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    pk =  request.POST.get('seq','')
    audit =  request.POST.get('audit','')
    explain =  request.POST.get('explain','')
    explain = MySQLdb.escape_string(explain)
    usr_id = d_value[0]
    usr_name = d_value[1]
    sql="update bumph_bubbl set audit = %s,audusrname='%s',audtime=now(),ref_date = now() where id = %s"%(audit,usr_name,pk)
    db.executesql(sql)

    sql="""insert into bumph_bubbl_audit (bb_id,audit_user,audit_time,status,`explain`)
                    values(%s,%s,now(),%s,'%s')
                """%(pk,usr_id,audit,explain)   
    #print ToGBK(sql)
    db.executesql(sql)
    push_audited_msg(pk,usr_id,usr_name)
    if str(audit)=='2':
        push_sendinfo_msg(pk,usr_id,usr_name)
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def delWxInfo(request):
    ret,errmsg,d_value = mValidateUser(request,"delete",'10202')
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    pk =  request.POST.get('seq','')
    sql = " DELETE FROM bumph_bubbl_groups WHERE bb_id=%s;DELETE FROM bumph_bubbl WHERE id=%s;" %(pk,pk)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def push_sendinfo_msg(pk,usr_id,usr_name) :
    sql="""SELECT WB.title
                    ,left(WB.content,300)
                    ,ifnull(WB.`recv_users`,'')
                    ,ifnull(U1.usr_name,'')
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,NT.cname
                    ,WB.must_reply
            FROM bumph_bubbl WB
            LEFT JOIN users U1 ON U1.usr_id = WB.cid
            LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
            WHERE WB.id=%s
        """%(pk)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    L=list(rows[0])
    title = """新信息：【 %s】发布信息"""%(L[3])
    description = L[5] + '--' + L[0] 
    func = 'info_detail'
    must_reply = L[6]

    users = L[2]
    depts = ''
    toUser = ''
    sql = """select n.id from bumph_bubbl_groups bg
                left join news_group n on n.id = bg.group_id
                where bg.bb_id=%s and n.is_all = 1"""%pk
    rows,iN = db.select(sql)
    if iN>0:
        toUser = "@all"
    else:
        sql = """select ifnull(n.users,''),ifnull(n.depts,'')  from bumph_bubbl_groups bg
                left join news_group n on n.id = bg.group_id
                where bg.bb_id=%s and ifnull(n.is_all,0) = 0"""%pk
        rows,iN = db.select(sql)
        for e in rows:
            if e[0] !='':
                users += ",%s"%e[0]
            if e[1] !='':
                depts += ",%s"%e[1]
        sql = """select DISTINCT ifnull(wxqy_id,login_id) from users where FIND_IN_SET(usr_id,'%s') or FIND_IN_SET(dept_id,'%s')"""%(users,depts)
        #print sql
        rows,iN = db.select(sql)
        for e in rows:
            toUser += "%s|"%e[0]

    return mWxPushMsg_Info(pk,title,description,must_reply,toUser,func,usr_id,usr_name)

def push_needaudit_msg(pk,usr_id,usr_name) :
    sql=""" SELECT WB.title
                    ,left(WB.content,300)
                    ,ifnull(U.wxqy_id,U.login_id)
                    ,ifnull(U1.usr_name,'')
                    ,date_format(WB.ref_date,'%%Y-%%m-%%d %%T')
                    ,NT.cname
                    ,WB.must_reply
            FROM bumph_bubbl WB
            LEFT JOIN users U ON U.usr_id = WB.audusrid
            LEFT JOIN users U1 ON U1.usr_id = WB.cid
            LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
            WHERE WB.id=%s
        """%(pk)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    L=list(rows[0])
    title = """新待审信息：【%s】发布信息"""%(L[3])
    description = L[5] + '--' + L[0] 
    func = 'info_audit'
    must_reply = L[6]

    toUser = L[2]
    return mWxPushMsg_Info(pk,title,description,must_reply,toUser,func,usr_id,usr_name)

def push_audited_msg(pk,usr_id,usr_name) :
    sql=""" SELECT WB.title
                    ,left(A.explain,300)
                    ,ifnull(U.wxqy_id,U.login_id)
                    ,ifnull(U1.usr_name,'')
                    ,date_format(A.audit_time,'%%Y-%%m-%%d %%T')
                    ,A.status
                    ,NT.cname
                    ,WB.must_reply
            FROM bumph_bubbl WB
            Left join bumph_bubbl_audit A on A.bb_id=WB.id
            LEFT JOIN users U ON U.usr_id = WB.cid
            LEFT JOIN users U1 ON U1.usr_id = A.audit_user
            LEFT JOIN news_type NT ON NT.type_code=WB.gw_type
            WHERE WB.id=%s
            order by A.id desc
        """%(pk)
    rows,iN = db.select(sql)
    L=list(rows[0])
    status = str(L[5])
    if status == '2':
        info = '通过'
        return
    elif status == '-1':
        info = '退回'
        must_reply = 0
    else:
        info = '作废'
        must_reply = 0
    title = """信息被%s：【%s】"""%(info,L[3])
    description = L[6] + '--' + L[0] 
    func = 'info_detail'

    toUser = L[2]
    return mWxPushMsg_Info(pk,title,description,must_reply,toUser,func,usr_id,usr_name)

def push_comment_msg(id,usr_id,usr_name) :
    sql=""" SELECT WB.id
                    ,WB.title
                    ,ifnull(U.wxqy_id,U.login_id)
                    ,left(C.cont,160)
                    ,ifnull(U.usr_name,'')
                    ,date_format(C.ctime,'%%Y-%%m-%%d %%T')
                    ,WB.must_reply
            FROM bumph_bubbl_comment C
            LEFT JOIN users U ON U.usr_id = C.cid
            LEFT JOIN bumph_bubbl WB ON WB.id = C.bb_id
            LEFT JOIN users U1 ON U1.usr_id = WB.cid
            WHERE C.id=%s
            order by C.ctime desc
        """%(id)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    L=list(rows[0])
    title = """新信息留言：【%s】为<%s>留言"""%(L[4],L[1])
    description = L[3] 
    func = 'info_detail'
    must_reply = L[6]

    toUser = L[2]
    pk = L[0]
    return mWxPushMsg_Info(pk,title,description,must_reply,toUser,func,usr_id,usr_name)

def get_type_data(sDF):
    options =['',False]

    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    L=[['','--请选择--',b]]
    sql = "select type_code,cname from news_type where status=1 and news_group='info'"
    lT,iN = db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = 0
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def handleMutilValue(value,is_number):
    sTemp = ','
    if isinstance(value,list):
        if is_number == 1:
            if len(value)>0:
                sTemp = value[0] or 0
            else:
                sTemp = 0
        else:
            for e in value:
                sTemp +="%s,"%e
    else:
        sTemp = value
    return sTemp