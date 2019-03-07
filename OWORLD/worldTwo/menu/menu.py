# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS,m_corp_name'%prj_name) 

def getMenuList(request):
    ret,msg,d_value = mValidateUser(request,"view",1401)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    sql=" SELECT menu,menu_id,menu_name,sort,parent_id,status,icon,url FROM menu_func ORDER BY parent_id,menu,sort,menu_id "
    #print sql 
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L1 = list(e)
        if e[1] == 0:
            L1[2] = m_corp_name
        L.append(L1)
    names = 'level menu_id menu_name sort parent_id status icon url'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取菜单列表成功",
        "deptList": %s,
        }
        """ %(s3)  
    return HttpResponseCORS(request,s)

def getMenuRoles(request):
    ret,msg,d_value = mValidateUser(request,"view",1401)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    menu_id = request.POST.get('menu_id','')
    sql="""select r.role_name,rm.tabs,rm.role_id from role_menu rm
           left join roles r on rm.role_id = r.role_id
           where rm.menu_id = %s and rm.tabs != '' and r.role_id is not null
           order by r.role_id"""%(menu_id)
    print sql
    rows,iN = db.select(sql)
    L = []
    for e in rows:
        L1 = list(e)
        L1[1] = getTabs(e[1])
        L1[2] = getUsers(e[2])
        L.append(L1)
    names = 'role_name tabs users'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取授权用户成功",
        "roleList": %s,
        }
        """ %(s3) 
    
    return HttpResponseCORS(request,s)

def getUsers(role_id):
    users = ''
    sql = """select u.usr_name from usr_role ur
             left join users u on u.usr_id = ur.usr_id
             where ur.role_id = '%s' and u.status = 1"""%(role_id)
    rows,iN = db.select(sql)
    for e in rows:
        users += "%s,"%e[0]    
    return users

def getTabs(tabs):
    tab_names = ''
    sql = """select label from menu_list_pages where FIND_IN_SET(id,'%s')"""%(tabs)
    #print sql
    rows,iN = db.select(sql)
    for e in rows:
        tab_names += "%s,"%e[0]    
    return tab_names

def addMenu(request):
    ret,msg,d_value = mValidateUser(request,"add",1401)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    menu_id = request.POST.get('menu_id','')
    cname = request.POST.get('cname','')                    #菜单名
    parent_id = request.POST.get('parent_id') or 'NULL'             #上级菜单
    sort = request.POST.get('sort') or 'NULL'                      #序号
    icon = request.POST.get('icon','')                      #图标
    url = request.POST.get('url','')                      #链接地址
    status = request.POST.get('status',1)                    
    #cname = ToGBK(cname)
    sql = "select count(*) from menu_func where menu_id=%s"%menu_id
    #print sql
    lT,iN = db.select(sql)
    if lT[0][0]>0:
        errCode = -1
        msg = '菜单ID重复！'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        return HttpResponseCORS(request,s)

    sql = "select menu from menu_func where menu_id=%s"%parent_id
    lT,iN = db.select(sql)
    menu = 1
    if iN>0:
        menu = lT[0][0] + 1
        
    sql="""INSERT INTO menu_func (menu,menu_id,menu_name,parent_id,sort,icon,url,status,has_child) 
                  VALUES(%s,%s,'%s',%s,%s,'%s','%s',%s,0)
        """ %(menu,menu_id,cname,parent_id,sort,icon,url,status)
    #print sql
    db.executesql(sql)
    sql = "update menu_func set has_child = 1 where menu_id=%s"%parent_id
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "菜单添加成功",
        }
        """
    return HttpResponseCORS(request,s)

def modifyMenu(request):
    ret,msg,d_value = mValidateUser(request,"update",1401)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    menu_id = request.POST.get('menu_id','')
    cname = request.POST.get('cname','')                    #菜单名
    parent_id = request.POST.get('parent_id') or 'NULL'             #上级菜单
    sort = request.POST.get('sort') or 'NULL'                      #序号
    icon = request.POST.get('icon','')                      #图标
    url = request.POST.get('url','')                      #链接地址
    status = request.POST.get('status',1)                    

    sql="""UPDATE menu_func SET menu_name='%s',parent_id=%s,sort=%s,icon='%s',url='%s',status=%s
                    WHERE menu_id='%s'
        """ %(cname,parent_id,sort,icon,url,status,menu_id)
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "菜单信息修改成功",
        }
        """ 
    return HttpResponseCORS(request,s)

def deleteMenu(request):
    ret,msg,d_value = mValidateUser(request,"delete",1401)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    menu_id = request.POST.get('menu_id','')

    sql = "select count(*) from menu_func where parent_id=%s"%menu_id
    #print sql
    lT,iN = db.select(sql)
    if lT[0][0]>0:
        errCode = -1
        msg = '该菜单下有子菜单，无法删除！'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        return HttpResponseCORS(request,s)
    sql = "select parent_id from menu_func where menu_id=%s"%menu_id
    lT,iN = db.select(sql)
    parent_id = lT[0][0]

    sql = "delete from menu_func where menu_id=%s"%menu_id
    db.executesql(sql)
    sql = "select count(*) from menu_func where parent_id=%s"%parent_id
    lT,iN = db.select(sql)
    if lT[0][0]==0:
        sql = "update menu_func set has_child = 0 where menu_id=%s"%parent_id
        db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "菜单删除成功",
        }
        """ 
    return HttpResponseCORS(request,s)

