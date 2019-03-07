# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,get_YES_NO_data,HttpResponseCORS,ToGBK'%prj_name) 
def getCategoryInfoByID(id):
    sql = "select cname,date_table from  category where id = '%s' "%(id)
    rows,iN = db.select(sql)
    if iN == 0:
        return '',''
    cname = rows[0][0]
    table_name = rows[0][1]
    return cname,table_name

def getCategoryList(request):
    ret,msg,d_value = mValidateUser(request,"view",803)
    #if ret!=0:
    #    return HttpResponseCORS(request,msg)

    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    category_id =  request.POST.get('category_id')  or request.GET.get('category_id','')
    cname,table_name = getCategoryInfoByID(category_id)
    sql = " SELECT id,cname,level,p_id,IFNULL(is_disable,0) FROM %s order by sort"%(table_name)
    print sql
    rows,iN = db.select(sql)
    L = []
    L1 = [-1,cname,0,'',0]
    L.append(L1)
    for e in rows:
        L1 = list(e)
        if e[2] == 1:
            L1[3] = -1
        L.append(L1)

    names = 'id cname ilevel parent_id del_flag'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取分类列表成功",
        "categoryList": %s,
        }
        """ %(s3)  
    return HttpResponseCORS(request,s)

def getCategory(request):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')

    category_id =  request.POST.get('category_id')  or request.GET.get('category_id','')
    cname,table_name = getCategoryInfoByID(category_id)

    id =  request.POST.get('id','') 

    if id=='':
        errCode = -1
        msg = 'ID不能为空'
        s = """
            %s({
            "errcode": %s,
            "errmsg": "%s",
            })
            """ %(callback,errCode,msg)  
        return HttpResponseCORS(request,s)
    L = []
    if str(id) == '-1':
        L1 = [-1,cname,'','',0,0,'']
        L1[3] = get_options_data_level(table_name,'')
        L.append(L1)
    else:
        sql="""SELECT c.id,c.cname,c.code,c.p_id,c1.cname,c.is_disable,c.sort,c.memo,c.level
                       FROM %s c 
                   left join %s c1 on c1.id = c.p_id
                   WHERE c.id=%s 
                    """%(table_name,table_name,id)
        print sql
        rows,iN = db.select(sql)
        for e in rows:
            L1 = list(e)
            L1[3] = get_options_data_level(table_name,e[3])
            if e[8] == 1:
                L1[4] = cname
            L.append(L1)
   
    names = 'id cname code parent_id parent_name del_flag sort memo'.split()
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False)
   
    s = """
        {
        "errcode": 0,
        "errmsg": "获取分类信息成功",
        "categoryInfo": %s,
        }
        """ %(s3)  
    print 1
    return HttpResponseCORS(request,s)

def get_options_data_level(table_name,p_id):
    L = get_data_level(table_name,p_id)
    options =['',False]
    names = 'value label checked parent_id disabled'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def get_data_level(table_name,p_id,title='--请选择--'):
    ldf=[]
    sDF=str(p_id)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b,'',0]]
    else:
        L=[]

    sql = """SELECT c.id                          
              ,c.cname             
              ,c.p_id                        
              ,0                   
          FROM %s c 
          where 1=1"""%(table_name)
    #print sql
    lT,iN = db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b,e[2],e[3]])
    return L

def addCategory(request):
    ret,msg,d_value = mValidateUser(request,"add",803)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    cid = d_value[0]

    category_id =  request.POST.get('category_id','')
    cname,table_name = getCategoryInfoByID(category_id)

    cname = request.POST.get('cname','')                        #部门名
    parent_id = request.POST.get('parent_id') or 'NULL'            #上级部门
    sort = request.POST.get('sort') or 'NULL'                      #序号
    del_flag = request.POST.get('del_flag') or 'NULL'              #禁用
    code = request.POST.get('code','')                        
    memo = request.POST.get('memo','')                        
    ilevel = 1
    sql = "select ifnull(level,1) from %s where id=%s"%(table_name,parent_id)
    lT,iN = db.select(sql)
    if iN>0:
        ilevel = lT[0][0] + 1
    if ilevel == 1 :
        sql = "select ifnull(max(type),0) from %s where level=1"%(table_name)
        lT,iN = db.select(sql)
        iType = lT[0][0] + 1
    else:
        sql = "select type from %s where id=%s"%(table_name,parent_id)
        lT,iN = db.select(sql)
        iType = lT[0][0]
    sql = "select ifnull(p_ids,'') from %s where id=%s"%(table_name,parent_id)
    lT,iN = db.select(sql)
    if iN >0:
        p_ids = lT[0][0] + ',%s'%(parent_id)
    else:
        p_ids = ''
    sql="""INSERT INTO %s (cname,code,p_id,sort,memo,level,is_disable,type,cid,ctime,p_ids) 
                  VALUES('%s','%s',%s,%s,'%s',%s
                         ,%s,%s,%s,now(),'%s')
        """ %(table_name,cname,code,parent_id,sort,memo,ilevel,del_flag,iType,cid,p_ids)
    #print ToGBK(sql)
    db.executesql(sql)

    sql = "select last_insert_id();"
    rows,iN1 = db.select(sql)
    id = rows[0][0]
    
    sql = "select id,ifnull(child_ids,'') from %s where find_in_set(%s,child_ids) or id = %s"%(table_name,parent_id,parent_id)
    lT,iN = db.select(sql)
    for e in lT:
        child_ids = e[1] + ',%s'%(id)
        p_id = e[0]
        sql = "update %s set has_child = 1,child_ids='%s' where id=%s"%(table_name,child_ids,p_id)
        db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "分类添加成功",
        "id":%s,
        }
        """%id
    return HttpResponseCORS(request,s)

def modifyCategory(request):
    ret,msg,d_value = mValidateUser(request,"upd",803)
    if ret!=0:
        return HttpResponseCORS(request,msg)
    cid = d_value[0]

    category_id =  request.POST.get('category_id','')
    cname,table_name = getCategoryInfoByID(category_id)

    id =  request.POST.get('id','') 
    if str(id) == '-1' or id =='':
        s = """
            {
            "errcode": 0,
            "errmsg": "分类信息修改成功",
            }
            """ 
        return HttpResponseCORS(request,s)

    cname = request.POST.get('cname','')                        #部门名
    parent_id = request.POST.get('parent_id') or 'NULL'            #上级部门
    sort = request.POST.get('sort') or 'NULL'                      #序号
    del_flag = request.POST.get('del_flag') or 'NULL'              #禁用
    code = request.POST.get('code','')                        
    memo = request.POST.get('memo','')                        
    
    if id == parent_id:
        s = """
            {
            "errcode": -1,
            "errmsg": "上级分类错误！",
            }
            """ 
        return HttpResponseCORS(request,s)

    ilevel = 1
    sql = "select ifnull(level,1) from %s where id=%s"%(table_name,parent_id)
    lT,iN = db.select(sql)
    if iN>0:
        ilevel = lT[0][0] + 1
 
    sql = "select ifnull(p_ids,''),ifnull(child_ids,'') from %s where id=%s"%(table_name,parent_id)
    lT,iN = db.select(sql)
    if iN>0:
        p_ids = lT[0][0] + ',%s'%(parent_id)
    else:
        p_ids = ''
    
    if str(del_flag) == 1:
        sql="""UPDATE %s SET cname='%s',code='%s',p_id=%s,sort=%s,memo='%s'
                       ,is_disable=%s,uid=%s,utime=now(),p_ids='%s',level=%s WHERE id='%s'
            """ %(table_name,cname,code,parent_id,sort,memo,del_flag,cid,p_ids,ilevel,id)
        db.executesql(sql)
    else:
        sql="""UPDATE %s SET cname='%s',code='%s',p_id=%s,sort=%s,memo='%s'
                       ,is_disable=%s,uid=%s,utime=now(),p_ids='%s',level=%s WHERE id='%s'
            """ %(table_name,cname,code,parent_id,sort,memo,del_flag,cid,p_ids,ilevel,id)
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "分类信息修改成功",
        "id":%s,
        }
        """%id
    return HttpResponseCORS(request,s)

def deleteCategory(request):
    ret,msg,d_value = mValidateUser(request,"delete",803)
    if ret!=0:
        return HttpResponseCORS(request,msg)

    category_id =  request.POST.get('category_id','')
    cname,table_name = getCategoryInfoByID(category_id)

    id =  request.POST.get('id','') 
    sql = "select ifnull(p_id,-1) from %s where id=%s"%(table_name,id)
    lT,iN = db.select(sql)
    p_id = lT[0][0]

    sql = "select count(*) from %s where p_id=%s"%(table_name,id)
    #print sql
    lT,iN = db.select(sql)
    if lT[0][0]>0:
        errCode = -1
        msg = '该分类下有子分类，无法删除！'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        return HttpResponseCORS(request,s)
    sql = "select p_id from %s where id=%s"%(table_name,id)
    lT,iN = db.select(sql)
    parent_id = lT[0][0]

    sql = "delete from %s where id=%s"%(table_name,id)
    db.executesql(sql)

    sql = "select count(*) from %s where p_id=%s"%(table_name,parent_id)
    lT,iN = db.select(sql)
    if lT[0][0]==0:
        sql = "update %s set has_child = 0,child_ids='' where id=%s"%(table_name,parent_id)
        db.executesql(sql)
    else:
        sql = "select id,ifnull(child_ids,'') from %s where find_in_set(%s,child_ids) or id = %s"%(table_name,parent_id,parent_id)
        lT,iN = db.select(sql)
        for e in lT:
            child_ids = e[1] + ","
            child_ids = child_ids.replace(',%s,'%id,',')
            p_id = e[0]
            sql = "update %s set child_ids='%s' where id=%s"%(table_name,child_ids,p_id)
            db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "分类删除成功",
        "id":%s,
        }
        """%p_id
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
    L=[['','--请选择--','',b]]
    for e in lT:
        usr_id=e[0]
        usr_name=e[1]
        if str(usr_id)==str(sDF):b='1'
        else:b=''
        L.append([usr_id,usr_name,'',b])
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

