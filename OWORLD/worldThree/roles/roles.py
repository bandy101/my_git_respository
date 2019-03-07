# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS'%prj_name) 

def getRoleList(request):
    ret,msg,d_value = mValidateUser(request,"view",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    dept_id =  request.POST.get('dept_id',1) 
    role_type =  request.POST.get('role_type','') 
    aoData =  request.POST.get('aoData','') 

    select_size = 10
    startNo = 0
    orderby = ' r.dept_id,r.sort'
    orderbydir=''
    qqid=''
    NL = ['r.role_name','r.sort','d.cname']
    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='iSortCol_0':
                iCol = e['value']
                orderby = NL[int(iCol)]
            elif e['name']=='sSortDir_0':
                orderbydir = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    if dept_id == '':
        sql ="""SELECT r.role_id,r.role_name,r.sort,d.cname,is_proj,d.id FROM roles r
                    left join dept d on d.id=r.dept_id
                    where 1=1 """
    else:
        sql ="""SELECT r.role_id,r.role_name,r.sort,d.cname,is_proj,d.id FROM roles r
                    left join dept d on d.id=r.dept_id
                    WHERE r.dept_id=%s """%dept_id
    if role_type!='':
        sql+=" AND r.is_proj = '%s'"%(role_type)
    if qqid!='':
        sql+=" AND r.role_name LIKE '%%%s%%'"%(qqid)
    #ORDER BY 
    if orderby!='':
        sql+=' ORDER BY %s %s' % (orderby,orderbydir)
    else:
        sql+=" ORDER BY r.dept_id,r.sort"

    #print sql 
    L,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,select_size)
    names = 'role_id role_name sort dept_name role_type dept_id'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    s2 = json.dumps(get_dept_data(dept_id,''),ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取角色列表成功",
        "sEcho": %s,
        "deptList":%s,
        "roleList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(sEcho,s2,s3,iTotal_length,iTotal_Page,pageNo,select_size)

    return HttpResponseCORS(request,s)

def addRole(request):
    ret,msg,d_value = mValidateUser(request,"add",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    role_name = request.POST.get('role_name','')                   #角色名
    dept_id = request.POST.get('dept_id') or 'NULL'                #部门ID
    sort = request.POST.get('sort') or 'NULL'                      #序号
    role_type = request.POST.get('role_type') or 'NULL'                      

    sql="INSERT INTO roles(role_name,sort,dept_id,is_proj,ctime) VALUES('%s',%s,%s,%s,now())" %(role_name,sort,dept_id,role_type)
    #print sql
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "角色添加成功",
        }
        """ 
    return HttpResponseCORS(request,s)

def modifyRole(request):
    ret,msg,d_value = mValidateUser(request,"upd",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    role_id = request.POST.get('role_id') or 'NULL'                #角色ID
    role_name = request.POST.get('role_name','')                   #角色名
    dept_id = request.POST.get('dept_id') or 'NULL'                #部门ID
    sort = request.POST.get('sort') or 'NULL'                      #序号
    role_type = request.POST.get('role_type') or 'NULL'                      
  
    sql="""UPDATE roles SET role_name='%s',sort=%s,dept_id=%s,is_proj=%s,utime=now() WHERE role_id=%s
        """ %(role_name,sort,dept_id,role_type,role_id)
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "角色信息修改成功",
        }
        """
    return HttpResponseCORS(request,s)

def deleteRole(request):
    ret,msg,d_value = mValidateUser(request,"delete",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    role_id = request.POST.get('role_id') or 'NULL'                #角色ID
    sql = "DELETE FROM roles WHERE role_id=%s"%role_id
    #print sql
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "菜单删除成功",
        }
        """
    return HttpResponseCORS(request,s)

def getRoleUser(request):
    ret,msg,d_value = mValidateUser(request,"view",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    role_id = request.POST.get('role_id') or 'NULL'                #角色ID
    sql = """SELECT U.usr_id,U.usr_name,D.cname FROM usr_role WUR 
               LEFT JOIN users U ON U.usr_id=WUR.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               WHERE WUR.role_id='%s'"""%role_id
    #print sql
    L,iN = db.select(sql)
    names = 'usr_id usr_name cname'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取授权人员列表成功",
        "userList":%s,
        }
        """%(s3)

    return HttpResponseCORS(request,s)

def getRolMenu(request):
    ret,msg,d_value = mValidateUser(request,"view",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    role_id = request.POST.get('role_id') or 'NULL'                #角色ID

    sql="""SELECT W1.menu,W1.menu_id,W1.menu_name,W1.sort,
                 W1.parent_id,W2.parent_id AS pp_id,ifnull(RM.tabs,''),ifnull(RM.can_view,0)
               FROM menu_func W1 LEFT JOIN menu_func W2 ON W1.parent_id=W2.menu_id
               LEFT JOIN (select distinct menu_id,tabs,can_view from role_menu where role_id=%s) RM on RM.menu_id=W1.menu_id
               WHERE W1.status=1 and W1.menu_id!=0 and W2.status=1 and W1.menu_id != 1402
               ORDER BY W1.parent_id,W1.menu,W1.sort 
            """ % role_id
    #print sql
    
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L1 = list(e)
        tabs = e[6]
        has_child = e[7]
        options =['',False]
        L2 = []
        #if has_child == 0:
        sql = "select id,label from menu_list_pages where menu_id=%s"%e[1]
        rows1,iN1 = db.select(sql)
        for e1 in rows1:
            if str(e1[0]) in tabs:
                b = '1'
            else:b=''    
            L2.append([e1[0],e1[1],b])
            #if len(L2) == 0:
            #    L2.append([0,'默认选项卡',''])

        names = 'value label checked'.split()
        data = [dict(zip(names, d)) for d in L2]
        options[0] = data
        options[1] = False
        names = 'options include_other_option'.split()
        L1[6] = dict(zip(names, options))
        L.append(L1)
    names = 'level menu_id menu_name sort parent_id pp_id tabs selected'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    #print s3
    s = """
        {
        "errcode": 0,
        "errmsg": "获取授权功能列表成功",
        "menuList":%s,
        }
        """%(s3)

    return HttpResponseCORS(request,s)

def modifyRoleMenu(request):
    ret,msg,d_value = mValidateUser(request,"upd",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    usr_id = d_value[0]
    role_id = request.POST.get('role_id') or 'NULL'                #角色ID
    menu_data = request.POST.get('menu_data','')
    menu_list = json.loads(menu_data)
    #print request.POST
    #print menu_data
    #删除旧记录
    sql="DELETE FROM role_menu WHERE role_id=%s" % role_id
    db.executesql(sql)
    for e in menu_list:
        print e
        menu_id = e.get('menu_id','')
        tabs = e.get('tabs','')
        selected = e.get('selected','')
         
        sql="""INSERT INTO role_menu(role_id,menu_id,tabs,can_view,cid,ctime) 
                      VALUES(%s,%s,'%s','%s','%s','%s')
                      """%(role_id,menu_id,tabs,selected,usr_id,getToday())  
        #print sql  
        db.executesql(sql)
         
    s = """
        {
        "errcode": 0,
        "errmsg": "更新授权功能列表成功",
        }
        """
    return HttpResponseCORS(request,s)

def getUserRole(request):
    ret,msg,d_value = mValidateUser(request,"view",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    usr_id1 = request.POST.get('usr_id',0) 
    sql = """select rl.role_name 
                    from usr_role ul
                    inner join roles rl on IFNULL(rl.dept_id,'') != '' and rl.role_id = ul.role_id
                    where ul.usr_id = %s
                    order by ul.role_id"""%usr_id1
    lT,iN = db.select(sql)
    roles = ""
    for e in lT:
        roles += e[0] + ","
    if len(roles)>0:
        roles = roles[:-1]
    s = """
        {
        "errcode": 0,
        "errmsg": "获取角色列表成功",
        "roles":"%s",
        }      
        """%(roles)

    return HttpResponseCORS(request,s)

def getRoles(user_id):
    sql = """select rl.role_name 
                    from usr_role ul
                    inner join roles rl on IFNULL(rl.dept_id,'') != '' and rl.role_id = ul.role_id
                    where ul.usr_id = %s
                    order by ul.role_id"""%user_id
    lT,iN = db.select(sql)
    roles = ""
    for e in lT:
        roles += e[0] + ","
    if len(roles)>0:
        roles = roles[:-1]
    return roles

def getRoleUserList(request):
    ret,msg,d_value = mValidateUser(request,"view",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    role_id = request.POST.get('role_id',0)
    dept_id = request.POST.get('dept_id',0)
    if dept_id==0:
        sql = """SELECT dept_id from roles WHERE role_id=%s"""%role_id
        rows,iN = db.select(sql)
        if iN>0:
            dept_id = rows[0][0]
        else:
            dept_id = 1

    sql = """SELECT U.usr_id,U.usr_name,D.cname FROM usr_role WUR 
               LEFT JOIN users U ON U.usr_id=WUR.usr_id
               LEFT JOIN dept D ON D.id=U.dept_id
               WHERE WUR.role_id='%s'"""%role_id
    L,iN = db.select(sql)
    names = 'usr_id usr_name dept'.split()
    data = [dict(zip(names, d)) for d in L]

    s1 = json.dumps(data,ensure_ascii=False)

    select_size = 10
    startNo = 0
    orderby = ''
    orderbydir=''
    qqid=''
    NL = ['','U.usr_id','U.usr_name','d.cname']
    aoData = request.POST.get('aoData','')
    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='iSortCol_0':
                iCol = e['value']
                orderby = NL[int(iCol)]
            elif e['name']=='sSortDir_0':
                orderbydir = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    sql="""
                  SELECT
                        U.usr_id
                        ,LEFT(U.usr_name,8)
                        ,D.cname
                        ,WUR.usr_id
                   FROM users U
                   LEFT JOIN dept D on D.id=U.dept_id
                   LEFT JOIN dept D1 on D.parent_id=D1.id
                   LEFT JOIN dept D2 on D1.parent_id=D2.id
                   LEFT JOIN (select usr_id from usr_role where role_id=%s)  WUR ON U.usr_id=WUR.usr_id
                  WHERE  U.status=1 and (D.id=%s or D.parent_id=%s or D1.parent_id=%s or D2.parent_id=%s)
                """%(role_id,dept_id,dept_id,dept_id,dept_id)
    if qqid!='':
        sql+=" AND U.usr_name LIKE '%%%s%%'"%(qqid)
    #ORDER BY 
    if orderby!='':
        sql+=' ORDER BY %s %s' % (orderby,orderbydir)
    else:
        sql+=" ORDER BY U.usr_name"

    #print sql 
    L,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,select_size)
    names = 'usr_id usr_name dept status'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    s2 = json.dumps(get_dept_data(dept_id,''),ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户列表成功",
        "selectedUserList":%s,
        "deptList":%s,
        "userList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(s1,s2,s3,iTotal_length,iTotal_Page,pageNo,select_size)

    return HttpResponseCORS(request,s)

def addRoleUsers(request):
    ret,msg,d_value = mValidateUser(request,"add",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    print request.POST
    usr_id = request.session.get('usr_id', 0)
    role_id = request.POST.get('role_id',0)
    user_list = request.POST.get('user_list')
    users = user_list.split(',')
    for e in users:
        sql = "select usr_id from usr_role where usr_id=%s and role_id=%s"%(e,role_id)
        #print sql
        rows,iN = db.select(sql)
        if iN==0:
            sql="INSERT INTO usr_role(usr_id,role_id,cid,ctime) VALUES('%s',%s,%s,'%s')" % (e,role_id,usr_id,getToday())
            #print sql
            db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "添加授权用户成功",
        }
        """

    return HttpResponseCORS(request,s)

def deleteRoleUser(request):
    ret,msg,d_value = mValidateUser(request,"delete",904)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    role_id = request.POST.get('role_id',0)
    user_id = request.POST.get('user_id',0)
    #删除记录
    sql="DELETE FROM usr_role WHERE role_id='%s' and usr_id=%s" %(role_id,user_id)
    #print sql
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "删除授权用户成功",
        }
        """

    return HttpResponseCORS(request,s)

def get_dept_data(sDF,title='--选择部门--',single=True):
    sql="SELECT id,cname,ilevel,parent_id FROM dept ORDER BY parent_id" 
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,'',b,'']]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        iLevel = int(e[2]) - 1
        txt= "---"*iLevel +e[1]
        L.append([e[0],txt,e[2],b,e[3]])
    return L
