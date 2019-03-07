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
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS,HttpResponseJsonCORS,ToGBK,m_corp_name'%prj_name) 
exec ('from %s.wx_cb.wxpush        import mWxPushMsg_Audit'%prj_name) 
from save_finish import saveFinishData

def packData(L):
    options =['',1]
    names = 'value label checked'.split()
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = 0
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def get_next_flow(sDF,pk,flow_id,opt,usr_id):
    lT=[]
    L=[]
    L1=[]
    sDF = str(sDF)
    if str(opt) == '3':  #作废
        L.append([-1,"<font color='red'>作废</font>",1])
        return packData(L),-1
    elif str(opt)=='': #未选择审核方向
        return packData(L),''
    #elif sDF!='':  #当前已选择，只显示已选择选项
    #    sql = "select id,cname from gw_flow_def where id=%s"%(sDF)
    #    lT,iN = db.select(sql)   
    #    for e in lT:
    #        L.append([e[0],e[1],1)
        
    elif str(opt) == '0': #退回
        sql = "select distinct flow_id,flow_name from gw_flow_his where m_id=%s and opt=1 and (flow_id!=%s or cid=%s)"%(pk,flow_id,usr_id)
        lT,iN = db.select(sql)   
        for e in lT:
            L.append([e[0],e[1],''])

    else:
        sql = "select ifnull(e_flag,0),ifnull(can_repeat,0),ifnull(no_pass,0),cname from gw_flow_def where id =%s"%(flow_id)
        #print sql
        lT,iN = db.select(sql)
        if iN==0:
            return L,-1
        e_flag = lT[0][0]
        can_repeat = lT[0][1]
        cname = lT[0][3]
        #1 当前流程可为结束流程,增加办理完毕选项
        if e_flag == 1:
            L.append(['-2',"<font color='green'>办理完毕</font>",''])
        #2 当前流程为必须重复流转流程,判断审核人是否全部流转完毕,未流转完毕添加本流程并返回，流转完毕继续下一步
        #2 当前流程为可重复流转流程,判断审核人是否全部流转完毕，未流转完毕添加本流程并继续下一步，流转完毕继续下一步    
        has_user = check_flow_users(pk,flow_id)
        if(has_user!=0 and can_repeat!=0):
            L.append([flow_id,cname,''])
        if(has_user!=0 and can_repeat==2):
            return packData(L),-1
        sql = "select  rule_flow_id,gd.cname,is_condition,gl_table,gl_field,gl_operator,gl_value  from gw_flow_rule gr left join gw_flow_def gd on gd.id=gr.rule_flow_id WHERE flow_id = %s"%(flow_id)
        #print sql
        lT,iN = db.select(sql)
        for e in lT:
            if check_flow_condition(pk,e) == False:
                continue
            L1 = get_flow(pk,e[0],e[1])
            for e1 in L1:
                is_add = 0
                for e2 in L:
                    if e1[0] == e2[0]:
                        is_add = 1
                        break
                if is_add == 0:
                    L.append([e1[0],e1[1],''])
    i = 0
    for k in L:
        if str(k[0])==str(sDF):b='1'                
        else:b=''
        L[i][2] = b
        i += 1

    #import numpy
    #print np.array(list(set([tuple(t) for t in L])))
    if len(L)==1:
        sDF=L[0][0]
        L[0][2]='1'
    return packData(L),sDF

def check_flow_condition(pk,e):
    if e[2] == 0:
        return True
    sql = "select %s from %s where gw_id=%s"%(e[4],e[3],pk)
    try:
        lT,iN = db.select(sql)
        if iN==0:
            return False
        value = lT[0][0]
        if e[5] == 'in':
            return (str(value) in e[6].split(','))
        if e[5] == 'not in':
            return (str(value) not in e[6].split(','))
        try:
            oper = "%s %s %s"%(value,e[5],e[6])
            print oper
            return eval(oper)
        except:
            oper = "'%s' %s '%s'"%(value,e[5],e[6])
            print oper
            return eval(oper)
    except:
        return False
    return True
def get_flow(pk,flow_id,flow_name):
    L = []
    L1 = [1,'']
    L1[0] = flow_id
    L1[1] = flow_name
    sql=" SELECT IFNULL(e_flag,0),IFNULL(no_pass,0),cname FROM gw_flow_def WHERE id = %s "%flow_id
    lT,iN=db.select(sql)
    if lT[0][0] == 1: #流程有办结
        L.append(L1)
        return L
    if lT[0][1] == 1: #不能被PASS
        L.append(L1)
        return L
    has_user = check_flow_users(pk,flow_id)
    #print "%s flow_id =%s has_user=%s"%(ToGBK(lT[0][2]),flow_id,has_user)
    if has_user!=0:
        L.append(L1)
        return L
    sql = "select  rule_flow_id,gd.cname  from gw_flow_rule gr left join gw_flow_def gd on gd.id=gr.rule_flow_id WHERE flow_id = %s"%(flow_id)
    #print sql
    lT,iN = db.select(sql)
    for e in lT:
        L2 = get_flow(pk,e[0],e[1])
        for e2 in L2:
            L.append(e2)
    return L

#返回是否有未审核人员
def check_flow_users(pk,flow_id):      
    sql=" SELECT usr_sel_type,ifnull(sel_usr_id,''),ifnull(sel_dept_id,''),ifnull(sel_role_id,''),ifnull(sel_leader,'') FROM gw_flow_def WHERE id = %s "%flow_id
    lT,iN=db.select(sql)
    sel_type=lT[0][0]
    sel_usr_id=lT[0][1]
    sel_dept_id=lT[0][2]
    sel_role_id=lT[0][3]
    sel_leader=lT[0][4]
    if str(sel_type) == '5': #作者
        sql=" SELECT D.cid FROM gw_doc D WHERE D.id = %s "%pk
        lT,iN=db.select(sql)
    if str(sel_type) == '8': #角色
        sql="""
                select r.usr_id
                from usr_role r
                left join users u on u.usr_id = r.usr_id
                where U.status = 1 and FIND_IN_SET(r.role_id,'%s')
                """%sel_role_id
        #print sql
        lT,iN=db.select(sql)
    if str(sel_type) == '9': #项目角色
        sql="""
                select u.usr_id
                from users u
                left join proj_user p on p.usr_id = u.usr_id and p.ifuse = 1
                left join gw_doc d on d.proj_id = p.proj_id or d.proj_id_2 = p.proj_id
                where d.id = %s AND U.status = 1 and FIND_IN_SET(p.role_id,'%s')
                """%(pk,sel_role_id)
        print sql
        lT,iN=db.select(sql)
    if str(sel_type) == '10': #限定作者部门领导
        sql="""
                SELECT IFNULL(G.form_dept_id,0),IFNULL(G.form_dept_id_2,0),IFNULL(U.dept_id,0)
                FROM gw_doc G
                LEFT JOIN users U ON U.usr_id = G.cid
                WHERE G.id = %s
                """%pk
        #print sql
        lT,iN=db.select(sql)
        if lT[0][0] != 0:
            deptid1=lT[0][0]
            deptid2=lT[0][1]
        else:
            deptid1=lT[0][2]
            deptid2=0
        sql="""select u.usr_id from dept_role_users du
               left join users u on du.usr_id = u.usr_id
               where du.dept_id in (%s,%s) and FIND_IN_SET(du.dr_id,'%s') and u.status =1
            """%(deptid1,deptid2,sel_leader)
        print sql
        lT,iN=db.select(sql)
    if str(sel_type) == '11': #限定项目所在经营管理部门领导和负责人
        sql="""
            select du.usr_id
            from gw_doc g
            left join out_proj o on o.id = g.proj_id or o.id = g.proj_id_2
            LEFT JOIN dept D1 ON D1.id = o.b_dept 
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND IFNULL(D1.true_dept_id,0) = 0)
            left join dept_role_users du on D2.id = du.dept_id
            left join users u on du.usr_id = u.usr_id
            where g.id = %s and FIND_IN_SET(du.dr_id,'%s') and u.status =1
            """%(pk,sel_leader)
        lT,iN=db.select(sql)
    if str(sel_type) == '12': #限定项目所在工程管理部门领导和负责人
        sql="""
            select du.usr_id
            from gw_doc g
            left join _m303_xmlx t on t.proj_id = g.proj_id or t.proj_id = g.proj_id_2
            LEFT JOIN dept D1 ON D1.id = t.proj_management 
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND IFNULL(D1.true_dept_id,0) = 0)
            left join dept_role_users du on D2.id = du.dept_id
            left join users u on du.usr_id = u.usr_id
            where g.id = %s and FIND_IN_SET(du.dr_id,'%s') and u.status =1
            """%(pk,sel_leader)
        lT,iN=db.select(sql)
        
    has_user = 0
    if str(sel_type) == '2': #具体人
        lT = sel_usr_id.split(',')
        for e in lT:
            if check_users(e,pk) != 0:
                has_user = 1
                break
    else:
        for e in lT:
            if check_users(e[0],pk) != 0:
                has_user = 1
                break
           
    return has_user

def check_users(usr_id,pk):
    if usr_id=='':
        return 0
    has_user = 1
     
    sql=" SELECT ifnull(cur_flow_id,0) FROM gw_doc WHERE id = %s "%pk 
    lT,iN=db.select(sql)
    cflow = lT[0][0]
        
    sql=" SELECT H.id FROM gw_flow_his H WHERE H.m_id = %s AND H.flow_id = %s AND H.status = 0 "%(pk,cflow) #查出来自己流程
    print sql
    lT,iN=db.select(sql)
    
    hid=lT[0][0]
    sql=" SELECT COUNT(1) FROM gw_flow_his WHERE m_id = %s AND ifnull(opt,1) = 1 AND cid = %s AND id <= %s "%(pk,usr_id,hid) #通过的
    #print sql
    aL,aN=db.select(sql)
    if aL[0][0] > 0: #同一个人 通过次数 比 退回次数要多， 则跳过
        has_user = 0
    return has_user

def get_next_sel_type(flow_id):
    if str(flow_id) in ('','0','-1','-2'):
        return ''
    sql = "select usr_sel_type from gw_flow_def where id=%s"%(flow_id)
    lT,iN = db.select(sql)   
    if iN==0:
        return ''
    return lT[0][0]

def get_next_dept(sDF,pk,flow_id,opt):
    L=[]
    sel_type = 0
    if str(flow_id) in ('','0','-1','-2'):
        return packData(L),'0',0
    if str(opt) == '0': #退回 
        return packData(L),sDF,0

    sql="""SELECT FD.usr_sel_type,FD.sel_dept_id,FD.sel_leader
           FROM gw_flow_def FD
           WHERE FD.ID=%s
        """%flow_id
    
    lT,iN=db.select(sql)
    sel_type = lT[0][0]
    sel_dept_id = lT[0][1]
    sel_leader = lT[0][2]
    if str(sel_type) in ['8','9']:
        return packData(L),'0',sel_type
    
    #if sDF!='':  #当前已选择，只显示已选择选项
    #    sql="SELECT id,cname,ifnull(parent_id,0) FROM dept WHERE id=%s ORDER BY sort"%sDF
    #    lT,iN = db.select(sql)   
    #    for e in lT:
    #        L.append([e[0],e[1],1)
    #    return packData(L),sDF

    if str(sel_type) in ['2']:  #2：限定部门及人  
        sql="""SELECT DISTINCT D.id,D.cname
                   FROM dept D
                   WHERE FIND_IN_SET(D.id,'%s')
                """%(sel_dept_id)
    elif str(sel_type) in ['4','5']:   #5:限定于作者
        sql="SELECT DISTINCT D.id,D.cname FROM gw_doc GD LEFT JOIN users U ON U.usr_id=GD.cid LEFT JOIN dept D ON D.id=U.dept_id WHERE GD.id=%s AND D.id!=1 "%pk
    elif str(sel_type) in ['10']: #限定作者部门的人  限定作者部门领导
        sql="""
                SELECT IFNULL(G.form_dept_id,0),IFNULL(G.form_dept_id_2,0),IFNULL(U.dept_id,0)
                FROM gw_doc G
                LEFT JOIN users U ON U.usr_id = G.cid
                WHERE G.id = %s
                """%pk
        #print sql
        lT,iN=db.select(sql)
        if lT[0][0] != 0:
            deptid1=lT[0][0]
            deptid2=lT[0][1]
        else:
            deptid1=lT[0][2]
            deptid2=0
        sql="""select distinct d.id,d.cname from dept_role_users du
               left join users u on du.usr_id = u.usr_id
               left join dept d on d.id = du.dept_id
               where du.dept_id in (%s,%s) and FIND_IN_SET(du.dr_id,'%s') and u.status =1
               order by d.sort DESC
            """%(deptid1,deptid2,sel_leader)
    elif str(sel_type) == '11': #限定项目所在部门领导和负责人
        sql="""
            select distinct d2.id,d2.cname
            from gw_doc g
            left join out_proj o on o.id = g.proj_id or o.id = g.proj_id_2
            LEFT JOIN dept D1 ON D1.id = o.b_dept 
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND IFNULL(D1.true_dept_id,0) = 0)
            left join dept_role_users du on D2.id = du.dept_id
            left join users u on du.usr_id = u.usr_id
            where g.id = %s and FIND_IN_SET(du.dr_id,'%s') and u.status =1
            """%(pk,sel_leader)
             
    elif str(sel_type) == '12': #限定项目所在部门领导和负责人
        sql="""
            select distinct d2.id,d2.cname
            from gw_doc g
            left join _m303_xmlx t on t.proj_id = g.proj_id or t.proj_id = g.proj_id_2
            LEFT JOIN dept D1 ON D1.id = t.proj_management 
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND IFNULL(D1.true_dept_id,0) = 0)
            left join dept_role_users du on D2.id = du.dept_id
            left join users u on du.usr_id = u.usr_id
            where g.id = %s and FIND_IN_SET(du.dr_id,'%s') and u.status =1
            """%(pk,sel_leader)
    else:
        sql="SELECT id,cname FROM dept WHERE id!=1 ORDER BY sort"
    print sql
    lT,iN=db.select(sql)
        
    for k in lT:
        if str(k[0])==str(sDF):b='1'                
        else:b=''
        L.append([k[0],k[1],b])
            
    if len(L)==1:
        sDF=L[0][0]
        L[0][2]='1'
            
    return packData(L),sDF,sel_type

def get_next_role(sDF,pk,flow_id,opt):
    L=[]
    if str(flow_id) in ('','0','-1','-2'):
        return packData(L),'0',0
    if str(opt) == '0': #退回 
        return packData(L),'0',0

    sql="""SELECT FD.usr_sel_type,FD.sel_role_id
           FROM gw_flow_def FD
           WHERE FD.ID=%s
        """%flow_id
    
    lT,iN=db.select(sql)
    sel_type = lT[0][0]
    sel_role_id = lT[0][1]
    if str(sel_type) not in ['8','9']:
        return packData(L),'0',sel_type
    
    #if sDF!='':  #当前已选择，只显示已选择选项
    #    sql="SELECT id,cname,ifnull(parent_id,0) FROM dept WHERE id=%s ORDER BY sort"%sDF
    #    lT,iN = db.select(sql)   
    #    for e in lT:
    #        L.append([e[0],e[1],1)
    #    return packData(L),sDF

    sql="""
                select role_id,role_name
                from roles 
                where FIND_IN_SET(role_id,'%s')
                """%sel_role_id
    #print sql
    lT,iN=db.select(sql)
        
    for k in lT:
        if str(k[0])==str(sDF):b='1'                
        else:b=''
        L.append([k[0],k[1],b])
            
    if len(L)==1:
        sDF=L[0][0]
        L[0][2]='1'
    return packData(L),sDF,sel_type

def get_next_user(sDF,pk,flow_id,dept_id,role_id,opt):
    L=[]
    if str(flow_id) in ('','0','-1','-2'):
        return packData(L),'0'
    if str(opt) == '0': #退回 
        sql = """select FD.usr_sel_type,U.usr_id,U.usr_name
                FROM gw_flow_his FH
                LEFT JOIN gw_flow_def FD ON FD.id = FH.flow_id
                LEFT JOIN users U ON U.usr_id = FH.cid
                LEFT JOIN dept D ON D.id = U.dept_id
                WHERE FH.m_ID=%s and flow_id=%s and FH.opt=1 ORDER BY FH.id limit 1"""%(pk,flow_id)
        #print sql
        lT,iN=db.select(sql)
        if iN >0:
            L1 = list(lT[0])
            L.append([L1[1],L1[2],'1'])
            sDF = L1[1]
        return packData(L),sDF

    if str(dept_id) =='': dept_id = 0
    if str(role_id) =='': role_id = 0
    sql="""SELECT FD.usr_sel_type,IFNULL(FD.e_flag,0),IFNULL(FD.no_pass,0),IFNULL(FD.can_repeat,0),FD.sel_usr_id,FD.sel_leader
           FROM gw_flow_def FD
           WHERE FD.ID = %s
           ORDER BY FD.sort
        """%flow_id
    #print sql
    lT,iN=db.select(sql)
    
    sel_type = 0
    e_flag=0
    no_pass=0
    re2=0
    sel_usr_id = ''
    sel_leader = ''
    if iN!=0:
        sel_type = lT[0][0]
        e_flag = lT[0][1]
        no_pass = lT[0][2]
        re2=lT[0][3]
        sel_usr_id = lT[0][4]
        sel_leader = lT[0][5]
    if str(sel_type) in ['2']:  #2：限定部门及人
        sql="""SELECT  U.usr_id,U.usr_name
                   FROM users U 
                   WHERE FIND_IN_SET(U.usr_id,'%s') AND U.dept_id=%s AND U.status = 1 
                   ORDER BY U.sort DESC
                """%(sel_usr_id,dept_id)
    elif str(sel_type) in ['5']:  #5:限定于作者的部门和限定作者  (不可行或只限于拟稿流程)
        sql=""" SELECT U.usr_id,U.usr_name
                    FROM gw_doc D
                    LEFT JOIN users U ON U.usr_id = D.cid
                    WHERE D.id=%s AND U.status = 1 """%(pk)
    elif str(sel_type) == '8': #角色
        sql="""
                select u.usr_id,u.usr_name
                from usr_role r
                left join users u on u.usr_id = r.usr_id
                where U.status = 1 and r.role_id=%s
                """%role_id
        #print sql
        lT,iN=db.select(sql)
    elif str(sel_type) == '9': #项目角色
        sql="""
                select u.usr_id,u.usr_name
                from users u
                left join proj_user p on p.usr_id = u.usr_id and p.ifuse = 1
                left join gw_doc d on d.proj_id = p.proj_id or d.proj_id_2 = p.proj_id
                where d.id = %s AND U.status = 1 and FIND_IN_SET(p.role_id,'%s')
                """%(pk,role_id)
        lT,iN=db.select(sql)
    elif str(sel_type) in ['10']: #10：限定作者部门的领导或负责人
        sql="""select distinct u.usr_id,u.usr_name from dept_role_users du
               left join users u on du.usr_id = u.usr_id
               left join dept d on d.id = du.dept_id
               where du.dept_id = %s and FIND_IN_SET(du.dr_id,'%s') and u.status =1
               order by u.sort DESC
            """%(dept_id,sel_leader)
    elif str(sel_type) == '11': #限定项目所在部门领导和负责人
        sql="""
            select distinct u.usr_id,u.usr_name 
            from gw_doc g
            left join out_proj o on o.id = g.proj_id or o.id = g.proj_id_2
            LEFT JOIN dept D1 ON D1.id = o.b_dept 
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND IFNULL(D1.true_dept_id,0) = 0)
            left join dept_role_users du on D2.id = du.dept_id
            left join users u on du.usr_id = u.usr_id
            where g.id = %s and FIND_IN_SET(du.dr_id,'%s') and D2.id = %s  and u.status =1
            order by u.sort DESC
            """%(pk,sel_leader,dept_id)
    elif str(sel_type) == '12': #限定项目所在部门领导和负责人
        sql="""
            select distinct u.usr_id,u.usr_name 
            from gw_doc g
            left join _m303_xmlx t on t.proj_id = g.proj_id or t.proj_id = g.proj_id_2
            LEFT JOIN dept D1 ON D1.id = t.proj_management 
            LEFT JOIN dept D2 ON D2.id = D1.true_dept_id OR (D2.id = D1.id AND IFNULL(D1.true_dept_id,0) = 0)
            left join dept_role_users du on D2.id = du.dept_id
            left join users u on du.usr_id = u.usr_id
            where g.id = %s and FIND_IN_SET(du.dr_id,'%s') and D2.id = %s  and u.status =1
            order by u.sort DESC
            """%(pk,sel_leader,dept_id)
    else:
        sql=""" SELECT U.usr_id,U.usr_name
                    FROM users U
                    WHERE U.dept_id=%s AND U.status = 1 
                    ORDER BY U.sort DESC
                """%(dept_id)
    print sql
    lT,iN=db.select(sql)
    
    if e_flag == 1: #是办结流程 
        l=list(lT)
    elif no_pass == 1: #不能跳过的流程 
        l=list(lT)
    elif re2 == 2: #如果是必须重复流转 
        l=[]
        for e in lT:
            if check_users(e[0],pk) != 0:
                l.append(e)
    else:
        if len(lT) == 1:
            l=[]
            for e in lT:
                if check_users(e[0],pk) != 0:
                    l.append(e)
        else:
            l=list(lT)
              
    L=[]
    for e in l:
        if e[0] == sDF or len(l) == 1: k='1'
        else:k=''
        L.append([e[0],e[1],k]) 
    if len(L)==1:
        sDF=L[0][0]
        L[0][2]='1'
 
    L1 = packData(L)
    return L1,sDF

def saveAudit(request):
    global d_value
    
    menu_id = request.POST.get('menu_id', 0)
    ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id= d_value[0]
    usr_name= d_value[1]
    is_sign = request.GET.get('is_sign','')
    is_sign = is_sign.replace('/','')
    if str(is_sign) == '1':
        return saveSign(request)

    is_send = request.GET.get('is_send',0)
    is_send = is_send.replace('/','')
    sign = request.GET.get('sign',0)
    sign = sign.replace('/','')
    mode = request.POST.get('mode','')
    data = request.POST.get('data','')
    data_list = json.loads(data)
    pk = data_list.get('pk','')
    flow_opt = data_list.get('flow_opt','')
    flow_memo = data_list.get('flow_memo','')
    flow_usr_id = data_list.get('flow_usr_id') or 'NULL'
    flow_usr_name = data_list.get('flow_usr_name','')
    flow_ctime = data_list.get('flow_ctime','')
    next_flow = data_list.get('flow_next_flow')
    sel_type = data_list.get('flow_sel_type') or 'NULL'
    next_dept = data_list.get('flow_next_dept') or 'NULL'
    next_role = data_list.get('flow_next_role') or 'NULL'
    next_usr = data_list.get('flow_next_usr') or 'NULL'
    sign_usr = data_list.get('flow_sign_usr','')
    flow_save_memo = data_list.get('flow_save_memo','')
    flow_save_memo = handleMutilValue(flow_save_memo,1)

    if next_flow == None:
        s = """
            {
            "errcode":-1,
            "errmsg":"下一流程不能为空！",
            "pk":%s,
            }
            """%pk       
        return HttpResponseCORS(request,s)
    
    if next_usr == 'NULL' and  str(next_flow) not in ['-2','-3','3','-1']:
        s = """
            {
            "errcode":-1,
            "errmsg":"下一流程处理人不能为空！",
            "pk":%s,
            }
            """%pk       
        return HttpResponseCORS(request,s)

    ## 从数据库获取相关信息 防止数据出错和刷新 ##
    sql="""SELECT ifnull(cur_flow_usr_id,0),ifnull(cur_flow_id,0),ifnull(cur_flow_status,0),ifnull(status,0) FROM gw_doc WHERE id = %s
        """%pk
    #print sql
   
    lT,iN=db.select(sql) #得到基本信息
    cur_usr_id,cur_flow_id,cur_flow_status,doc_status = lT[0]
       
    if cur_usr_id != usr_id:
        s = """
            {
            "errcode":-1,
            "errmsg":"你不是当前流程处理人，不可办理",
            "pk":%s,
            }
            """%pk       
        return HttpResponseCORS(request,s)

    #处理常用意见
    sql = "select id from appr_opinion where fl_id='%s' and cid='%s' and opinion='%s'"%(cur_flow_id,usr_id,flow_memo)
    lT,iN=db.select(sql)
    if iN == 0:
        if str(flow_save_memo) == '1':
            sql = """insert into appr_opinion (type,pub_type,fl_id,opinion,cid,ctime,uid,utime,counts) values 
                (1,2,%s,'%s',%s,now(),%s,now(),1)"""%(cur_flow_id,flow_memo,usr_id,usr_id)
            db.executesql(sql)
    else:
        sql = "update appr_opinion set utime=now(),counts = counts +1 where id = %s"%(lT[0][0])
        db.executesql(sql)

    sql=" SELECT H.id FROM gw_flow_his H WHERE H.m_id = %s AND H.flow_id = %s and status = 0"%(pk,cur_flow_id)
        
    lT,iN = db.select(sql)
    HID = lT[0][0] #自己的his ID
    
    flow_status = 0
    if str(is_send) =='1':
        flow_status = 1
    
    finish = 0
    disable = 0
    if str(is_send) =='1':
        if str(next_flow) =='-2': #办结
            finish = 1
        if str(flow_opt) == '3': #作废
            disable = 1
        ## 增加下一流程
        if finish==0 and disable==0:
            sql="""
                INSERT INTO gw_flow_his(m_id,send_usr_id,flow_id,send_flow_id,send_pre_flow_id,status,cid,ctime) 
                VALUES(%s,%s,%s,%s,%s,0,%s,now())
                """%(pk,usr_id,next_flow,next_flow,cur_flow_id,next_usr)
            #print ToGBK(sql)
            db.executesql(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
            NHD = rows[0][0]

        #修改当前流程
        sql="""UPDATE gw_flow_his SET send_flow_time=now() WHERE id = %s
            """%(HID)
        db.executesql(sql)

        ## 更改主表信息 ##
        if finish==1:
            sql="""UPDATE gw_doc SET cur_flow_time = now(), cur_user_name='%s',
                cur_flow_id = NULL, cur_flow_usr_id = %s,cur_flow_name = '已办结',
                next_flow_id = null,next_flow_usr_id = null 
                WHERE id = %s
                """%(usr_name,usr_id,pk)
            print ToGBK(sql)
            db.executesql(sql)
        elif disable==1:
            sql="""UPDATE gw_doc SET cur_flow_time = now(), cur_user_name='%s', 
                cur_flow_id = null, cur_flow_usr_id = %s,cur_flow_name = '已作废', 
                next_flow_id = null,next_flow_usr_id = null 
                WHERE id = %s
                """%(usr_name,usr_id,pk)
            #print ToGBK(sql)
            db.executesql(sql)
        else:
            sql="""UPDATE gw_doc SET cur_flow_time = now(), 
                cur_flow_id = %s, cur_flow_usr_id = %s,
                next_flow_id = null,next_flow_usr_id = null 
                WHERE id = %s
                """%(next_flow,next_usr,pk)
            #print ToGBK(sql)
            db.executesql(sql)

        if finish==0 and disable==0:
            update_next_flow_text(pk,NHD)

        #顺便把待办的会签也给办了
        if str(flow_opt) =='0': sign_status = 2
        else: sign_status = 1
        sql="""
            UPDATE gw_flow_sign SET sign_time=now(),memo='%s',status=%s,usr_name='%s'
            WHERE m_id=%s AND usr_id=%s AND IFNULL(status,0) = 0
            """%(flow_memo,sign_status,usr_name,pk,usr_id)
        db.executesql(sql)

        #办结之后把所有未办理的会签改为弃权
        if finish==1 or disable==1:
            sql="""
                SELECT S.id, S.usr_name
                FROM gw_flow_sign S
                WHERE S.m_id = %s AND S.status = 0
                """%pk
            lT,iN=db.select(sql)
            msg="该文已办结，未办理的会签，系统自动处理为放弃。"
            for e in lT:
                id,name = e
                sql="""
                    UPDATE gw_flow_sign SET usr_name = '%s',
                    sign_time = now(),memo = '%s',status = 3
                    WHERE id = %s
                """%(name,msg,id)
                db.executesql(sql)
        #添加下一处理人的浏览权限
        if finish==0 and disable==0:
            sql = "select cybl from gw_doc where id=%s"%pk
            lT,iN=db.select(sql)
            if iN > 0:
                users = lT[0][0]
                cybl = users.split(',')
                if next_usr not in cybl:
                    users += "%s,"%next_usr
                    sql = "update gw_doc set cybl = '%s' where id=%s"%(users,pk)
                    db.executesql(sql)
            
    #添加会签人员,必须在修改当前流程前面,以删除旧的会签人权限
    if finish == 0 and disable==0 and sign_usr!='':
        add_gw_flow_sign(pk,HID,cur_flow_id,sign_usr,usr_id,usr_name) #增加会签

    #修改当前流程
    sql="""
        UPDATE gw_flow_his SET
        opt = %s, memo = '%s', next_flow_id = %s, next_dept =%s, next_usr_id = %s, uid = %s,
        uusrname = '%s', utime = now(), status = %s, next_role_id = %s,sign_users='%s' WHERE id = %s
        """%(flow_opt,flow_memo,next_flow,next_dept,next_usr,usr_id,usr_name,flow_status,next_role,sign_usr,HID)
    #print ToGBK(sql)
    db.executesql(sql)

    if str(is_send) =='1':
        if finish == 1: #办结
            doc_status = 6
            status_txt = '已办结'
        elif str(flow_opt) == '1':#同意办理
            doc_status = 3
            status_txt = '待处理'
        elif str(flow_opt) == '0':#退回
            sql="SELECT id FROM gw_flow_def WHERE id=%s AND s_flag=1"%next_flow
            lT,iN=db.select(sql)
            if iN==0:#退回给非起始流程
                doc_status = 4
                status_txt = '待处理(退回)'
            else:  #退回给起始流程
                doc_status = 5
                status_txt = '重新起草'
        elif str(flow_opt) == '3':#作废
            doc_status = 7
            status_txt = '作废'
        sql="""
            UPDATE gw_doc SET
            status = %s, cur_flow_status = 1, finish = %s , is_disable = %s , status_txt = '%s'
            WHERE id = %s
            """%(doc_status,finish,disable,status_txt,pk)
        db.executesql(sql)
    else:
        sql="""
            UPDATE gw_doc SET
            cur_flow_status = 0,status_txt = '保存未发送'
            WHERE id = %s
            """%(pk)
        #print sql
        db.executesql(sql)

    update_flow_text(pk,HID)
    #更新待办表
    if finish == 1 or disable == 1:
        update_gw_db(pk, 2,disable)
    else:
        update_gw_db(pk, 1,0)

    if finish == 1: #办结并提交的文件需要做的处理
        gw_finish_save(menu_id,pk,d_value,request)

    if str(is_send)=='1':  #微信消息推送
        push_audit_msg(pk,usr_id,usr_name)           

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功",
        "pk":%s,
        }
        """%pk       
    return HttpResponseCORS(request,s)

def gw_finish_save(menu_id,pk,d_value,request):
    sql = "select `form_table`  from `menu_data_source` where `menu_id` = %s"%menu_id
    rows,iN = db.select(sql)
    form_table = rows[0][0]
    sql = "update %s set gw_status = 1 where gw_id=%s"%(form_table,pk)
    try:
        db.executesql(sql)
    except :
        print "Database syntax error!"
    
    #各个功能额外的处理
    saveFinishData(menu_id,pk,d_value,request)
    return

def saveSign(request):
    global d_value
    menu_id = request.POST.get('menu_id', 0)
    ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id= d_value[0]
    usr_name= d_value[1]
    mode = request.POST.get('mode','')
    data = request.POST.get('data','')
    data_list = json.loads(data)
    pk = data_list.get('pk','')
    sign_users = data_list.get('sign_users','')
    sign_status = data_list.get('sign_status','')
    sign_memo = data_list.get('sign_memo','')
    fs_id = data_list.get('fs_id','')
    flow_id = data_list.get('flow_id','')
    fh_id = data_list.get('fh_id','')
      
    sql = "update gw_flow_sign set status='%s',memo='%s',sign_time=now(),sign_users='%s' where id=%s"%(sign_status,sign_memo,sign_users,fs_id)
    db.executesql(sql)

    if sign_users!='':
        usrids = sign_users.split(',')
        sql=""
        for e in usrids:
            sql+=" insert into gw_flow_sign(m_id,usr_id,status,cid,ctime,flow_id,flow_his_id) values(%s,%s,0,%s,now(),%s,%s); "%(pk,e,usr_id,flow_id,fh_id)
        db.executesql(sql)
        
        #添加会签人员的浏览权限
        sql = "update gw_doc set cybl = concat(cybl,'%s,') where id=%s"%(sign_users,pk)
        db.executesql(sql)
        push_sign_msg(pk,usr_id,usr_name)           

    #更新待办表
    update_gw_db(pk, 3,0)

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功",
        "pk":%s,
        }
        """%pk       
    return HttpResponseCORS(request,s)

def update_flow_text(pk,fs_id):
    sql="""update gw_doc d,gw_flow_def cf,users cu set 
        cur_flow_name = cf.cname, cur_user_name = cu.usr_name
        where cf.id = d.cur_flow_id and  cu.usr_id = d.cur_flow_usr_id and d.id=%s
    """%pk
    db.executesql(sql)
    sql="""update gw_doc d,gw_flow_def nf,users nu set 
        next_flow_name = nf.cname, next_user_name = nu.usr_name
        where nf.id = d.next_flow_id and nu.usr_id = d.next_flow_usr_id and d.id=%s
    """%pk
    db.executesql(sql)
    sql="""update gw_flow_his gf,gw_flow_def cf
        set gf.`flow_name` = cf.cname
        where gf.flow_id=cf.id and gf.id=%s;
    """%fs_id
    sql+="""update gw_flow_his gf,gw_flow_def cf1
        set gf.`next_flow_name` =cf1.cname
        where gf.next_flow_id=cf1.id and gf.id=%s;
    """%fs_id
    sql+="""update gw_flow_his gf,dept cd
        set gf.`next_dept_name` =cd.cname
        where gf.next_dept=cd.id and gf.id=%s;
    """%fs_id
    sql+="""update gw_flow_his gf,users cu
        set gf.`next_usr_name` =cu.usr_name
        where gf.next_usr_id=cu.usr_id and gf.id=%s;
    """%fs_id
    sql+="""update gw_flow_his gf,roles r
        set gf.`next_role_name` =r.role_name
        where gf.next_role_id=r.role_id and gf.id=%s;
    """%fs_id
    #print sql
    db.executesql(sql)
    return 

def update_next_flow_text(pk,fs_id):
    sql="""update gw_flow_his gf,gw_flow_def cf
        set gf.`flow_name` = cf.cname
        where gf.flow_id=cf.id and gf.id=%s;
    """%fs_id
    sql+="""update gw_flow_his gf,users cu
        set gf.`cusrname` =cu.usr_name
        where gf.cid=cu.usr_id and gf.id=%s;
    """%fs_id
    #print sql
    db.executesql(sql)
    return 
# 增加公文会签的保存方法
def add_gw_flow_sign(pk,FS_ID,cur_flow_id,sign_usr,usr_id,usr_name):
    sql=" delete from gw_flow_sign where m_id = %s and flow_his_id = %s and status = 0 "%(pk,FS_ID)
    db.executesql(sql)
    
    usrids = sign_usr.split(',')
    sql=""
    n=0
    for e in usrids:
        sql+=" insert into gw_flow_sign(m_id,usr_id,status,cid,ctime,flow_id,flow_his_id) values(%s,%s,0,%s,now(),%s,%s); "%(pk,e,usr_id,cur_flow_id,FS_ID)
        n+=1
        if n>50:
            db.executesql(sql)
            sql=""
            n=0
    if n>0:
        db.executesql(sql)
    
    #添加会签人员的浏览权限
    oldUsers = ''
    sql = "select ifnull(sign_users,'') from gw_flow_his where id='%s'"%FS_ID
    lT,iN=db.select(sql)
    if iN>0:
        oldUsers = lT[0][0]
    if oldUsers != '':
        oldUsers += ","
        sql = "update gw_doc set cybl=replace(cybl,'%s','') where id=%s"%(oldUsers,pk)
        db.executesql(sql)
    sql = "update gw_doc set cybl = concat(cybl,'%s,') where id=%s"%(sign_usr,pk)
    db.executesql(sql)

    push_sign_msg(pk,usr_id,usr_name)           

    return

def update_gw_db(pk,t,disable):
    # t=1 主办  t=2 办结  t=3 其他（协办）
    if t == 2:
        sql=" delete from gw_audit where gw_id = %s"%(pk)
        db.executesql(sql)
        if disable == 0:
            sql="""
                insert into gw_verify(gw_id, title, ctime, type_id)
                select d.id, d.title, now(),d.type_id
                from gw_doc d
                left join menu_data_source md on d.menu_id=md.menu_id
                where d.id = %s and md.has_verify=1
                """%(pk)
            db.executesql(sql)    
    elif t == 1:
        sql=" delete from gw_audit where gw_id = %s "%(pk)
        db.executesql(sql)           
        sql="""
                insert into gw_audit(gw_id, title, flow_id, cur_flow_name, usr_id, cur_user_name,ctime, s_flag,status_txt,type_id,cid,cusrname)
                select d.id, d.title, cf.id, cf.cname, cu.usr_id, cu.usr_name,d.cur_flow_time,cf.s_flag ,d.status_txt,d.type_id,d.cid, cu1.usr_name
                from gw_doc d
                left join gw_flow_def cf on cf.id = d.cur_flow_id
                left join users cu on cu.usr_id = d.cur_flow_usr_id
                left join users cu1 on cu1.usr_id = d.cid
                where d.id = %s
            """%(pk)
        #print sql
        db.executesql(sql)           

    #不管啥情况都重新统计协办
    sql=" delete from gw_sign where gw_id = %s"%(pk)
    db.executesql(sql)

    sql="""
        insert into gw_sign (gw_id, title, flow_id, cur_flow_name, usr_id, cur_user_name, ctime,status_txt,type_id,cid,cusrname)
        select d.id, d.title, cf.id, cf.cname, s.usr_id, cu.usr_name,s.ctime,d.status_txt,d.type_id,d.cid, cu1.usr_name
        from gw_flow_sign s
        left join gw_flow_def f on f.id = s.flow_id
        left join gw_doc d on s.m_id = d.id
        left join gw_flow_def cf on cf.id = d.cur_flow_id
        left join users cu on cu.usr_id = d.cur_flow_usr_id
        left join users cu1 on cu1.usr_id = d.cid
        left join gw_audit g on g.gw_id = s.m_id and g.usr_id = s.usr_id
        where s.m_id = %s and s.status = 0 and g.id is null and not exists(
            select 1 from gw_flow_sign x where x.m_id = s.m_id and x.usr_id = s.usr_id and x.status =0 and x.id > s.id)
        """%(pk)
    #print sql
    db.executesql(sql)
    #update_gw_statistics(pk,t)  
    
    return

def update_gw_statistics(pk,t):
    # t=1 主办  t=2 办结  t=3 其他（协办）
    if t == 2:
        sql="select cid from "%(pk)
        db.executesql(sql)
        sql="""
                insert into gw_verify(gw_id, title, ctime, type_id)
                select d.id, d.title, now(),d.type_id
                from gw_doc d
                left join menu_data_source md on d.menu_id=md.menu_id
                where d.id = %s and md.has_verify=1
            """%(pk)
        db.executesql(sql)    
    elif t == 1:
        sql=" delete from gw_audit where gw_id = %s "%(pk)
        db.executesql(sql)           
        sql="""
                insert into gw_audit(gw_id, title, flow_id, cur_flow_name, usr_id, cur_user_name,ctime, s_flag,status_txt,type_id)
                select d.id, d.title, cf.id, cf.cname, cu.usr_id, cu.usr_name,d.cur_flow_time,cf.s_flag ,d.status_txt,d.type_id
                from gw_doc d
                left join gw_flow_def cf on cf.id = d.cur_flow_id
                left join users cu on cu.usr_id = d.cur_flow_usr_id
                where d.id = %s
            """%(pk)
        db.executesql(sql)           

    #不管啥情况都重新统计协办
    sql=" delete from gw_sign where gw_id = %s"%(pk)
    db.executesql(sql)

    sql="""
        insert into gw_sign (gw_id, title, flow_id, cur_flow_name, usr_id, cur_user_name, ctime,status_txt,type_id)
        select d.id, d.title, cf.id, cf.cname, s.usr_id, cu.usr_name,s.ctime,d.status_txt,d.type_id
        from gw_flow_sign s
        left join gw_flow_def f on f.id = s.flow_id
        left join gw_doc d on s.m_id = d.id
        left join gw_flow_def cf on cf.id = d.cur_flow_id
        left join users cu on cu.usr_id = d.cur_flow_usr_id
        left join gw_audit g on g.gw_id = s.m_id and g.usr_id = s.usr_id
        where s.m_id = %s and s.status = 0 and g.id is null and not exists(
            select 1 from gw_flow_sign x where x.m_id = s.m_id and x.usr_id = s.usr_id and x.status =0 and x.id > s.id)
        """%(pk)
    #print sql
    db.executesql(sql)
    
    return

def rePushMsg(request):
    pk = request.POST.get('pk', 11912)
    #menu_id = request.POST.get('menu_id', 0)
    #ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    #if ret!=0:
    #    return HttpResponseCORS(request,errmsg)
    usr_id = 1
    usr_name = '管理员'
    sql=""" SELECT GD.menu_id
                ,GT.cname 
                ,ifnull(US.wxqy_id,US.login_id)
                ,ifnull(UC.wxqy_id,UC.login_id)
                ,GD.finish
                ,UC.usr_name
                ,H.cusrname
                ,H.opt
                ,H.id
            FROM gw_flow_his H                    
            LEFT JOIN gw_doc GD ON GD.id = H.m_id
            LEFT JOIN gw_type GT ON GT.ID=GD.type_id
            LEFT JOIN users UC ON UC.usr_id=GD.cid
            LEFT JOIN users US ON US.usr_id=H.next_usr_id
            WHERE GD.id = %s and H.opt is not null
            order by H.ctime desc
            limit 1
        """%(pk)
    print sql
    rows,iN = db.select(sql)
    L=list(rows[0])
    menu_id = L[0]
    if L[4] != 1 and str(L[7]) not in ['0','3']:
        title = """催办：【%s】%s"""%(L[5],L[1])
        toUser = L[2]
        state = 'gw_audit'

    return mWxPushMsg_Audit(menu_id,pk,title,toUser,state,usr_id,usr_name)

def push_audit_msg(pk,usr_id,usr_name) :
    sql=""" SELECT GD.menu_id
                ,GT.cname 
                ,ifnull(US.wxqy_id,US.login_id)
                ,ifnull(UC.wxqy_id,UC.login_id)
                ,GD.finish
                ,UC.usr_name
                ,H.cusrname
                ,H.opt
                ,H.id
            FROM gw_flow_his H                    
            LEFT JOIN gw_doc GD ON GD.id = H.m_id
            LEFT JOIN gw_type GT ON GT.ID=GD.type_id
            LEFT JOIN users UC ON UC.usr_id=GD.cid
            LEFT JOIN users US ON US.usr_id=H.next_usr_id
            WHERE GD.id = %s and H.opt is not null
            order by H.ctime desc
            limit 1
        """%(pk)
    #print sql
    rows,iN = db.select(sql)
    L=list(rows[0])
    menu_id = L[0]
    if L[4] == 1:
        title = """%s信息化系统提醒您，<%s>已办结。"""%(m_corp_name,L[1])
        toUser = L[3]
        state = 'gw_view'
    elif str(L[7]) == '0':
        title = """%s信息化系统提醒您，<%s>已退回给您。"""%(m_corp_name,L[1])
        toUser = L[2]    
        state = 'gw_audit'
    elif str(L[7]) == '3':
        title = """%s信息化系统提醒您，<%s>已被作废!"""%(m_corp_name,L[1])
        toUser = L[3]
        state = 'gw_view'
    else:
        title = """新待办：【%s】%s"""%(L[5],L[1])
        toUser = L[2]
        state = 'gw_audit'

    return mWxPushMsg_Audit(menu_id,pk,title,toUser,state,usr_id,usr_name)


def push_sign_msg(pk,usr_id,usr_name) :
    sql=""" SELECT GD.menu_id
                ,GT.cname 
                ,ifnull(US.wxqy_id,US.login_id)
                ,ifnull(UC.wxqy_id,UC.login_id)
                ,GD.finish
                ,UC.usr_name
                ,H.cusrname
                ,H.opt
                ,FS.id
            FROM gw_flow_his H                    
            LEFT JOIN gw_doc GD ON GD.id = H.m_id
            LEFT JOIN gw_type GT ON GT.ID=GD.type_id
            LEFT JOIN users UC ON UC.usr_id=GD.cid
            LEFT JOIN gw_flow_sign FS ON FS.flow_his_id = H.id AND IfNULL(FS.status,0)=0
            LEFT JOIN users US ON US.usr_id=FS.usr_id
            WHERE GD.id = %s and FS.id is not null
            order by H.ctime desc
        """%(pk)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    L=list(rows[0])
    menu_id = L[0]
    title = """新会签：【%s】%s"""%(L[5],L[1])
    toUser = ''
    for e in rows:
        toUser += e[2] + '|'
    state = 'gw_sign'
    return mWxPushMsg_Audit(menu_id,pk,title,toUser,state,usr_id,usr_name)

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
        if is_number == 1:
            sTemp = value or 0
        else:
            sTemp = value
        
    return sTemp

def updateDB(request):
    pk = request.POST.get('pk', '')
    if pk == '':
        s = """
            {
            "errcode":-1,
            "errmsg":""
            }
            """      
        return HttpResponseJsonCORS(request,s)
    auditData = request.POST.get('auditData', '')
    auditData = json.loads(auditData)
    signData = request.POST.get('signData', '')
    signData = json.loads(signData)
    sql = "delete from gw_audit where gw_id =%s and source = 1;delete from gw_sign where gw_id =%s and source = 1;"%(pk,pk)
    db.executesql(sql)
    for e in auditData:
        type_id = e.get('type_id',0)
        pre_time = e.get('pre_time','')
        title = e.get('title','')
        usr_id = e.get('usr_id',0)
        cname = e.get('cname','')
        usr_name = e.get('usr_name','')
        flow_id = e.get('flow_id',0)
        flow_name = e.get('flow_name','')
        cid = e.get('cid',0)
        cusrname = e.get('cusrname','')
        url = e.get('url','')
        sql = """insert into `gw_audit` (`gw_id`,`type_id`,`title`,`flow_id`,`cur_flow_name`,`usr_id`,`cur_user_name`,`ctime`,`s_flag`,`source`,`url`,type_name,cid,cusrname)
                 values(%s,%s,'%s',%s,'%s',%s,'%s','%s',0,1,'%s','%s','%s','%s');
              """%(pk,type_id,title,flow_id,flow_name,usr_id,usr_name,pre_time,url,cname,cid,cusrname)
        db.executesql(sql)
    for e in signData:
        type_id = e.get('type_id',0)
        pre_time = e.get('pre_time','')
        title = e.get('title','')
        usr_id = e.get('usr_id',0)
        cname = e.get('cname','')
        usr_name = e.get('usr_name','')
        flow_id = e.get('flow_id',0)
        flow_name = e.get('flow_name','')
        cid = e.get('cid',0)
        cusrname = e.get('cusrname','')
        url = e.get('url','')
        sql = """insert into `gw_sign` (`gw_id`,`type_id`,`title`,`flow_id`,`cur_flow_name`,`usr_id`,`cur_user_name`,`ctime`,`source`,`url`,type_name,cid,cusrname)
                 values(%s,%s,'%s',%s,'%s',%s,'%s','%s',1,'%s','%s','%s','%s');
              """%(pk,type_id,title,flow_id,flow_name,usr_id,usr_name,pre_time,url,cname,cid,cusrname)
        db.executesql(sql)

    s = """
        {
        "errcode":0,
        "errmsg":""
        }
        """      
    return HttpResponseJsonCORS(request,s)
