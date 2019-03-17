# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,get_YES_NO_data,HttpResponseCORS'%prj_name) 

def getDeptList(request):
    ret,msg,d_value = mValidateUser(request,"view",902)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    parent_id =  request.POST.get('parent_id','') 

    if parent_id=='':
        sql=" SELECT id,cname,ilevel,parent_id,IFNULL(del_flag,0) FROM dept ORDER BY sort "
    else:
        sql=" SELECT id,cname,ilevel,parent_id,IFNULL(del_flag,0) FROM dept where parent_id =%s ORDER BY sort "%parent_id
    #print sql
    rows,iN = db.select(sql)
    names = 'id cname ilevel parent_id del_flag'.split()
    data = [dict(zip(names, d)) for d in rows]

    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取部门列表成功",
        "deptList": %s,
        }
        """ %(s3)  
    return HttpResponseCORS(request,s)

def getDept(request):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    dept_id =  request.POST.get('dept_id','') 

    if dept_id=='':
        errCode = -1
        msg = '部门ID不能为空'
        s = """
            %s({
            "errcode": %s,
            "errmsg": "%s",
            })
            """ %(callback,errCode,msg)  
        return HttpResponseCORS(request,s)

    sql="""SELECT id,cname,parent_id,cant_del,type,IFNULL(sort,''),true_dept_id,IFNULL(del_flag,0),IFNULL(isRA,0)
                   ,IFNULL(jygl,0)
                   FROM dept WHERE id=%s 
                """% dept_id
    #print sql
    rows,iN = db.select(sql)
    L=[]
    for e in rows:
        L1=list(e)
        dept_id=e[0]
        L1[4]=get_mtc_t_data(e[4],'D_TYPE','') 
        L1[7]=get_YES_NO_data(e[7])
        L.append(L1)            
    
    names = 'id cname parent_id cant_del type sort true_dept_id del_flag isRA jygl'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    sql = "select id,txt1,'' from mtc_t m where m.type = 'D_LEAD' order by m.sort"
    rows,iN = db.select(sql)
    L=[]
    for e in rows:
        L1=list(e)
        dr_id = e[0]
        sql1 = """select dr.usr_id,u.usr_name from dept_role_users dr
                  left join users u on dr.usr_id = u.usr_id
                  where dr.dept_id = %s and dr.dr_id = %s
               """%(dept_id,dr_id)
        rows1,iN1 = db.select(sql1)
        if iN1>0:
            L1[2]=rows1[0][0]
        L.append(L1)            
    
    names = 'role_id role_name usr_id'.split()
    data = [dict(zip(names, d)) for d in L]
    s4 = json.dumps(data,ensure_ascii=False)

    s5 = json.dumps(get_users_data('','ALL'),ensure_ascii=False)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取部门信息成功",
        "deptInfo": %s,
        "roles":%s,
        "users":%s
        }
        """ %(s3,s4,s5)  
    return HttpResponseCORS(request,s)

def getNewDept(request):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    parent_id =  request.POST.get('parent_id','') 

    if parent_id=='':
        errCode = -1
        msg = '上级部门ID不能为空'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        return HttpResponseCORS(request,s)

    dept_id = ''
    sql="""SELECT '','',id,
                   '',type,sort,'',IFNULL(del_flag,0),''
                   ,''
                   FROM dept WHERE id=%s 
                """% parent_id    #print sql
    rows,iN = db.select(sql)
    L=[]
    for e in rows:
        L1=list(e)
        L1[4]=get_mtc_t_data(e[4],'D_TYPE','') 
        L1[7]=get_YES_NO_data(e[7])
        L.append(L1)            
    
    names = 'id cname parent_id cant_del type sort true_dept_id del_flag isRA jygl'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    sql = "select id,txt1,'' from mtc_t m where m.type = 'D_LEAD' order by m.sort"
    rows,iN = db.select(sql)
    L=[]
    for e in rows:
        L1=list(e)
        dr_id = e[0]
        sql1 = """select dr.usr_id,u.usr_name from dept_role_users dr
                  left join users u on dr.usr_id = u.usr_id
                  where dr.dept_id = '%s' and dr.dr_id = %s
               """%(dept_id,dr_id)
        rows1,iN1 = db.select(sql1)
        if iN1>0:
            L1[2]=rows1[0][0]
        L.append(L1)            
    
    names = 'role_id role_name usr_id'.split()
    data = [dict(zip(names, d)) for d in L]
    s4 = json.dumps(data,ensure_ascii=False)

    s5 = json.dumps(get_users_data('','ALL'),ensure_ascii=False)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取部门信息成功",
        "deptInfo": %s,
        "roles":%s,
        "users":%s
        }
        """ %(s3,s4,s5)  
    return HttpResponseCORS(request,s)

def addDept(request):
    ret,msg,d_value = mValidateUser(request,"add",902)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    callback =  request.POST.get('callback','')

    dept_id =  request.POST.get('dept_id','') 

    cname = request.POST.get('cname','')                        #部门名
    parent_id = request.POST.get('parent_id') or 'NULL'            #上级部门
    type = request.POST.get('type') or 'NULL'                      #类型
    sort = request.POST.get('sort') or 'NULL'                      #序号
    true_dept_id = request.POST.get('true_dept_id') or 'NULL'      #事实部门ID
    del_flag = request.POST.get('del_flag') or 'NULL'              #禁用
    isRA = request.POST.get('isRA') or 'NULL'                      #是否注册机构
    jygl = request.POST.get('jygl') or 'NULL'                      #经营管理
    ilevel = 1
    sql = "select ifnull(iLevel,1) from dept where id=%s"%parent_id  
    lT,iN = db.select(sql)
    if iN>0:
        ilevel = lT[0][0] + 1
    sql="""INSERT INTO dept(cname,parent_id,type,sort,true_dept_id,ilevel,del_flag,isRA,jygl) 
                  VALUES('%s','%s',%s,%s,%s,%s,%s,%s,%s)
        """ %(cname,parent_id,type,sort,true_dept_id,ilevel,del_flag,isRA,jygl)
    #print sql
    db.executesql(sql)
    sql = "select last_insert_id();"
    rows,iN = db.select(sql)
    dept_id = rows[0][0]

    roles =  request.POST.get('roles','') 
    roles = json.loads(roles)
    for e in roles:
        role_id = e.get('role_id','')
        usr_id = e.get('usr_id','')
        if usr_id != '':
            sql = "insert into dept_role_users (dept_id,dr_id,usr_id) values (%s,%s,%s)"%(dept_id,role_id,usr_id)
            db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "部门添加成功",
        }
        """
    return HttpResponseCORS(request,s)

def modifyDept(request):
    print request.POST
    ret,msg,d_value = mValidateUser(request,"upd",902)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    dept_id =  request.POST.get('dept_id','') 


    cname = request.POST.get('cname','')                        #部门名
    parent_id = request.POST.get('parent_id') or 'NULL'            #上级部门
    type = request.POST.get('type') or 'NULL'                      #类型
    sort = request.POST.get('sort') or 'NULL'                      #序号
    true_dept_id = request.POST.get('true_dept_id') or 'NULL'      #事实部门ID
    del_flag = request.POST.get('del_flag') or 'NULL'              #禁用
    isRA = request.POST.get('isRA') or 'NULL'                      #是否注册机构
    jygl = request.POST.get('jygl') or 'NULL'                      #经营管理

    sql="""UPDATE dept SET cname='%s',parent_id=%s,type=%s,sort=%s,true_dept_id=%s,del_flag=%s,isRA=%s,jygl=%s WHERE id='%s'
        """ %(cname,parent_id,type,sort,true_dept_id,del_flag,isRA,jygl,dept_id)
    db.executesql(sql)
    print sql

    sql = "delete from dept_role_users where dept_id=%s"%(dept_id)
    db.executesql(sql)

    roles =  request.POST.get('roles','') 
    roles = json.loads(roles)
    for e in roles:
        role_id = e.get('role_id','')
        usr_id = e.get('usr_id','')
        if usr_id != '':
            sql = "insert into dept_role_users (dept_id,dr_id,usr_id) values (%s,%s,%s)"%(dept_id,role_id,usr_id)
            db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "部门信息修改成功",
        }
        """ 
    return HttpResponseCORS(request,s)

def deleteDept(request):
    ret,msg,d_value = mValidateUser(request,"delete",902)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    dept_id =  request.POST.get('dept_id','') 

    sql = "select count(*) from users where dept_id=%s"%dept_id
    lT,iN = db.select(sql)
    if lT[0][0]>0:
        errCode = -1
        msg = '该部门下有用户，无法删除！'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        return HttpResponseCORS(request,s)
    sql = "select count(*) from dept where parent_id=%s"%dept_id
    #print sql
    lT,iN = db.select(sql)
    if lT[0][0]>0:
        errCode = -1
        msg = '该部门下有子部门，无法删除！'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        return HttpResponseCORS(request,s)

    sql = "update dept set del_flag=1 where id=%s"%dept_id
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "部门删除成功",
        }
        """
    return HttpResponseCORS(request,s)

def get_users_data(sDF,dept_id):
    if dept_id=='ALL':
        sql = "select usr_id,usr_name  from users where status=1 order by usr_name"
    else:
        sql="""select usr_id,usr_name  from users 
               where dept_id=%s #and usr_id in(select usr_id  from rela_usr_dept where dept_id=%s)
               and status=1 order by usr_name
            """%(dept_id,dept_id)
    #print sql
    lT,iN = db.select(sql)
    if sDF=='':b='1'
    else:b=''
    L=[['','--请选择--']]
    for e in lT:
        usr_id=e[0]
        usr_name=e[1]
        if str(usr_id)==str(sDF):b='1'
        else:b=''
        L.append([usr_id,usr_name])
    return L

def get_mtc_t_data(sDF,type,title='--请选择--'):
    sql="SELECT id,txt1 FROM mtc_t WHERE type='%s'" %type
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,'',b])
    return L

