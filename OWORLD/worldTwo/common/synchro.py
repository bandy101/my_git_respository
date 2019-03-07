# -*- coding: utf-8 -*-
prj_name=__name__.split('.')[0]
import sys,os,time
import json
import httplib
import cookielib
import urllib 
exec ('from %s.share        import mValidateUser,HttpResponseCORS,db,dActiveUser,ToGBK'%prj_name) 
exec ('from %s.wx_cb.wxpush        import getInfoFromWx,update_wx_dept,update_wx_user'%prj_name) 

def synchroWxUsers(request):
    s = ''
    func = request.GET.get('func', '')
    if func == 'getUsers':
        s = getUsers(request)
    elif func == 'synchroUsers':
        s = synchroUsers(request)
    return s

def getUsers(request):
    dL,uL = getInfoFromWx()
    
    #更新部门同步信息
    sql = """delete from synchro_dept_log where upd_status = 0 """
    db.executesql(sql)
    sql = """insert into `synchro_dept_log` (`dept_id`,`name`,`parentid`,`sort`,`upd_status`,`wx_status`)
             select id,cname,parent_id,sort,0,1 from dept where del_flag = 0
          """
    db.executesql(sql)
    sql = "select id,cname,parent_id,sort from dept where del_flag = 0"
    rows,iN = db.select(sql)
    L =[]
    sql = ''
    for e1 in rows:  #遍历本地部门
        dept_id1 = e1[0]
        name1 = e1[1]
        parentid1 = e1[2]
        order1 = e1[3]
        
        is_find = 0
        for e in dL:   #遍历企业号部门
            dept_id = e.get("id",'')
            name = e.get("name",'')
            parentid = e.get("parentid",'')
            order = e.get("order",'')
            if dept_id1 == dept_id:
                if name1!=name or str(parentid1)!=str(parentid):  #需要更新
                    sql += "update synchro_dept_log set wx_status=2 where dept_id=%s and upd_status=0;"%(dept_id)
                else:  #无需跟新
                    sql += "delete from synchro_dept_log where dept_id=%s and upd_status=0;"%(dept_id)
                is_find = 1
                break
    for e in dL:   #遍历企业号部门
        dept_id = e.get("id",'')
        name = e.get("name",'')
        parentid = e.get("parentid",'')
        order = e.get("order",'')
        is_find = 0
        for e1 in rows:  #遍历本地部门
            dept_id1 = e1[0]
            name1 = e1[1]
            parentid1 = e1[2]
            order1 = e1[3]
            if dept_id1 == dept_id: 
                is_find = 1
                break
        if is_find == 0:
            sql += """insert into `synchro_dept_log` (`dept_id`,`name`,`parentid`,`sort`,`upd_status`,`wx_status`) 
                       values (%s,'%s',%s,%s,0,3);
                  """%(dept_id,name,parentid,order)    
    #print sql
    db.executesql(sql)

    #更新人员同步信息
    sql = """delete from synchro_user_log where upd_status = 0 """
    db.executesql(sql)
    sql = """insert into `synchro_user_log` (`usr_id`,wx_id,`usr_name`,`dept_id`,`sort`,`mobile`,`gender`,`email`,`enable`,`upd_status`,`wx_status`)
             select u.usr_id,ifnull(wxqy_id,login_id),u.usr_name,u.dept_id,u.sort,ifnull(a.mobile ,u.`mobil`),a.sex,ifnull(a.email,u.e_mail),u.status,0,1 from users u 
                left join empl e on e.usr_id = u.usr_id
                left join `addr_book` a on a.emp_id = e.id                                                                  
                where u.status = 1
                order by u.usr_id
          """
    
    db.executesql(sql)
    sql = """select ifnull(wxqy_id,login_id),u.usr_name,u.dept_id,u.sort,ifnull(a.mobile ,u.`mobil`),ifnull(a.sex,''),ifnull(a.email,u.e_mail),u.status,u.usr_id from users u 
                left join empl e on e.usr_id = u.usr_id
                left join `addr_book` a on a.emp_id = e.id                                                                  
                where u.status = 1
                order by u.usr_id"""
    rows,iN = db.select(sql)
    L =[]
    sql = ''
    for e1 in rows:  #遍历本地人员
        usr_id1 = e1[0]
        name1 = e1[1]
        dept_id1 = e1[2]
        order1 = e1[3]
        mobile1 = e1[4]
        gender1 = e1[5]
        email1 = e1[6]
        enable1 = e1[7]
        
        is_find = 0
        for e in uL:   #遍历企业号人员
            usr_id = e.get("userid",'')
            name = e.get("name",'')
            dept_id = e.get("department",'')
            dept_id = dept_id[0]
            order = e.get("order",'')
            order = order[0]
            mobile = e.get("mobile",'')
            gender = e.get("gender",'')
            email = e.get("email",'')
            enable = e.get("enable",'')
            if usr_id1 == usr_id:
                #手机号只能自己更新  
                if name1==name and dept_id1==dept_id and email1==email and enable1==enable:  #无需跟新
                    sql = "delete from synchro_user_log where wx_id='%s' and upd_status=0;"%(usr_id)
                    #print sql
                    db.executesql(sql)
                else:  #需要更新
                    print "%s %s %s %s %s "%(usr_id,dept_id,mobile,email,enable)
                    print "%s %s %s %s %s "%(usr_id1,dept_id1,mobile1,email1,enable1)
                    sql = "update synchro_user_log set wx_status=2 where wx_id='%s' and upd_status=0;"%(usr_id)
                    #print sql
                    db.executesql(sql)
                is_find = 1
                break
    for e in uL:   #遍历企业号人员
        usr_id = e.get("userid",'')
        name = e.get("name",'')
        dept_id = e.get("department",'')
        order = e.get("order",'')
        mobile = e.get("mobile",'')
        gender = e.get("gender",'')
        email = e.get("email",'')
        enable = e.get("enable",'')
        status = e.get("status",'')
        is_find = 0
        for e1 in rows:  #遍历本地人员
            usr_id1 = e1[0]
            name1 = e1[1]
            if usr_id1 == usr_id: 
                is_find = 1
                id = e1[8]
                sql1 = "update users set wx_status = %s where usr_id=%s"%(status,id)
                db.executesql(sql1)
                break
            elif name == name1 and mobile==e1[4]:
                is_find = 1
                id = e1[8]
                sql1 = "update users set wxqy_id = '%s' where usr_id=%s"%(usr_id,id)
                db.executesql(sql1)
                break

        if is_find == 0:
            sql = """insert into `synchro_user_log` (wx_id,usr_name,`upd_status`,`wx_status`)
                       values ('%s','%s',0,3);
                  """%(usr_id,name)    
            db.executesql(sql)
  
    sql = "select `dept_id`,`name`,`parentid`,wx_status from synchro_dept_log where upd_status=0" 
    rows,iN = db.select(sql)
    names = 'id cname parent_id wx_status'.split()
    L = [dict(zip(names, d)) for d in rows]
    deptData = json.dumps(L,ensure_ascii=False)      

    sql = "select usr_id,usr_name,dept_id,wx_status from synchro_user_log where upd_status = 0"
    rows,iN = db.select(sql)
    names = 'usr_id usr_name dept_id wx_status'.split()
    L = [dict(zip(names, d)) for d in rows]
    userData = json.dumps(L,ensure_ascii=False)      

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户列表成功",
        "deptList":%s,
        "userList":%s
        }
        """%(deptData,userData)
    #print s
    return HttpResponseCORS(request,s)      

def synchroUsers(request):
    #同步部门
    sql = "select `dept_id`,`name`,ifnull(`parentid`,0),ifnull(`sort`,0),wx_status from synchro_dept_log where upd_status=0" 
    rows,iN = db.select(sql)
    for e in rows:
        dept_id = e[0]
        name = e[1]
        parentid = e[2]
        sort = e[3]
        wx_status = e[4]
        errcode,errmsg = update_wx_dept(dept_id,name,parentid,sort,wx_status)
        if int(errcode) == 0 :
            wx_status = 0 
        sql = "update synchro_dept_log set ctime=now(),errcode='%s',errmsg = '%s' where dept_id=%s and upd_status=0;"%(errcode,errmsg,dept_id)
        db.executesql(sql)

    sql = "select dept_id,name,wx_status,errcode,errmsg from synchro_dept_log where upd_status=0 and errcode!=0"
    rows,iN = db.select(sql)
    names = 'dept_id name wx_status errcode errmsg'.split()
    L = [dict(zip(names, d)) for d in rows]
    deptData = json.dumps(L,ensure_ascii=False)      
    
    sql = "update synchro_dept_log set upd_status=1 where upd_status=0;"
    db.executesql(sql)

    #同步人员
    sql = "select wx_id,`usr_name`,`dept_id`,`sort`,`mobile`,`gender`,`email`,`enable`,`wx_status`,usr_id from synchro_user_log where upd_status=0" 
    rows,iN = db.select(sql)
    for e in rows:
        wx_id = e[0]
        usr_name = e[1]
        dept_id = e[2]
        sort = e[3]
        mobile = e[4]
        gender = e[5]
        email = e[6]
        enable = e[7]
        wx_status = e[8]
        usr_id = e[9]
        errcode,errmsg = update_wx_user(wx_id,usr_name,dept_id,sort,mobile,gender,email,enable,wx_status)
        if int(errcode) == 0 :
            wx_status = 0 
        sql = "update synchro_user_log set ctime=now(),errcode='%s',errmsg = '%s' where wx_id='%s' and upd_status=0;"%(errcode,errmsg,wx_id)
        db.executesql(sql)

    sql = "select usr_id,usr_name,dept_id,wx_status,errcode,errmsg  from synchro_user_log where upd_status=0 and errcode!=0"
    rows,iN = db.select(sql)
    names = 'usr_id usr_name dept_id wx_status errcode errmsg'.split()
    L = [dict(zip(names, d)) for d in rows]
    userData = json.dumps(L,ensure_ascii=False)      
    
    sql = "update synchro_user_log set upd_status=1 where upd_status=0;"
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "同步完成！",
        "deptList":%s,
        "userList":%s
        }
        """%(deptData,userData)
    #print s
    return HttpResponseCORS(request,s)                  
