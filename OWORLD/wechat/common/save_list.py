# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname'%prj_name) 
import json
import MySQLdb
exec ('from %s.worklog.worklog        import push_log_msg,getDPUsers'%prj_name)   

def saveListData(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    if str(menu_id)=='80501':
        savePageFormList80501(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='203':  #费用报销
        savePageFormList203(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='216':  #零星材料费用报销
        savePageFormList216(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='208':  #收款管理
        savePageFormList208(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='209':  #投标保证金付款管理
        savePageFormList209(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='210':  #投标保证金退款管理
        savePageFormList210(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='239':  #成本进项票管理
        savePageFormList239(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='308':  #资金预付管理
        savePageFormList308(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='318':  #服务费管理
        savePageFormList208(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='501':  #组织机构管理
        savePageFormList501(pk,mode,value_dict,d_value,request)
    #elif str(menu_id)=='41102':  #入库申请
    #    savePageFormList41102(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='410':  #材料款付款管理
        savePageFormList410(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='540':  #材料款拨付管理
        savePageFormList540(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='303':  #立项管理
        savePageFormList303(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='504':  #材料管理
        savePageFormList504(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='104':  #工作日志
        savePageFormList104(pk,mode,value_dict,d_value,request)
    elif str(menu_id)=='10601':  #写日志
        savePageFormList10601(pk,mode,value_dict,d_value,request)

    if m_prjname == 'hcpra':
        from save_ext_hc import saveDataExt
    else:
        from save_ext import saveDataExt
    saveDataExt(pk,mode,value_dict,d_value,request)
    return 

def savePageFormList504(pk,mode,value_dict,d_value,request):
    print request.POST
    return

def savePageFormList10601(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
    priority = data_list.get('priority','')  
    dp_users = getDPUsers(cid)
    sql = "update work_log set dp_users='%s' where id=%s"%(dp_users,pk)
    db.executesql(sql)
    if int(priority)>1:
        push_log_msg(pk,dp_users)
    return

def savePageFormList104(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
    dp_usr_id = data_list.get('dp_usr_id','')   
    dp_usr_name = data_list.get('dp_usr_name','')   
    usr_ids = data_list.get('usr_ids','')   
    sql = "select id from work_log_right where dp_usr_id='%s'"%(dp_usr_id)
    rows,iN = db.select(sql)
    if iN == 0:
        sql = "insert into work_log_right (dp_usr_id,dp_usr_name,cid,cusrname,ctime) values ('%s','%s',%s,'%s',now())"%(dp_usr_id,dp_usr_name,cid,cusrname)
        db.executesql(sql)
        sql = "update work_log_right set usr_ids='%s' where dp_usr_id='%s'"%(usr_ids,dp_usr_id)
        db.executesql(sql)
    return

def savePageFormList303(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
   
    sql = "select proj_id from _m303_xmlx where gw_id='%s'"%(pk)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    if iN == 0:
        return 
    proj_id = rows[0][0]
    
    sql = "update _m303_xmlx_list set proj_id = %s where gw_id=%s"%(proj_id,pk)
    db.executesql(sql)
    lists = data_list.get('lists','')   
    for e in lists:
        mx_id =  e.get('mx_id','')
        role_id =  e.get('role_id','')
        role_name =  e.get('role_name','')
        users =  e.get('users','')
        sort =  e.get('_tableOrder','')
        if mx_id != '':
            sql = "update _m303_xmlx_list set users = '%s',sort=%s where id=%s"%(users,sort,mx_id)
            db.executesql(sql)
        else:
            sql = "select id from _m303_xmlx_list where proj_id =%s and role_id=%s"%(proj_id,role_id)
            rows,iN = db.select(sql)
            if iN == 0:
                sql = "insert into _m303_xmlx_list (proj_id,users,role_id,role_name,gw_id,cid,cusrname,ctime,sort) values (%s,'%s',%s,'%s',%s,%s,'%s',now(),%s)"%(proj_id,users,role_id,role_name,pk,cid,cusrname,sort)
                db.executesql(sql)
        saveProjRoles(pk,proj_id,role_id,role_name,cid,users)
    if m_prjname == 'bygj':
        saveProjRolesBygj(pk,proj_id,cid)

    return
def saveProjRolesBygj(pk,proj_id,cid):
    sql = "select xmjl,sgy,cly,cgy,zly,ysy,xmcw,aqy,zhily,hty,Safety_supervisor,others from _m303_xmlx where gw_id='%s'"%(pk)
    rows,iN = db.select(sql)
    if iN ==0:
        return
    e = list(rows[0])
    users = e[0] or ''
    role_id = 17
    role_name = u'项目经理'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[1] or ''
    role_id = 54
    role_name = u'施工员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[2] or ''
    role_id = 81
    role_name = u'材料员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[3] or ''
    role_id = 55
    role_name = u'仓管员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[4] or ''
    role_id = 56
    role_name = u'资料员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[5] or ''
    role_id = 59
    role_name = u'预算员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[6] or ''
    role_id = 71
    role_name = u'项目财务'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[7] or ''
    role_id = 82
    role_name = u'安全员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[8] or ''
    role_id = 83
    role_name = u'质量员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[9] or ''
    role_id = 84
    role_name = u'绘图员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[10] or ''
    role_id = 85
    role_name = u'质安监督员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    users = e[11] or ''
    role_id = 'NULL'
    role_name = u'其他人员'
    saveProjRoles(pk,proj_id,role_id,role_name,cid,users)

    return
     
def saveProjRoles(pk,proj_id,role_id,role_name,cid,users):
    for e in users.split(',') :
        if e =='':
            continue
        sql = "select id,ifuse from proj_user where proj_id=%s and role_id=%s and usr_id=%s"%(proj_id,role_id,e)
        print sql
        rows,iN = db.select(sql)
        if iN == 0:
            sql = "insert into proj_user (proj_id,role_id,usr_id,ifuse,intime) values (%s,%s,%s,1,now())"%(proj_id,role_id,e)
            db.executesql(sql)
            sql = "insert into proj_user_his (proj_id,role_id,usr_id,intime,cid) values (%s,%s,%s,now(),%s)"%(proj_id,role_id,e,cid)
            db.executesql(sql)
        else:
            if rows[0][1] == 0:
                sql = "update proj_user set ifuse=1,intime=now() where id = %s"%(rows[0][0])
                db.executesql(sql)
                sql = "insert into proj_user_his (proj_id,role_id,usr_id,intime,cid) values (%s,%s,%s,now(),%s)"%(proj_id,role_id,e,cid)
                #print sql
                db.executesql(sql)
    sql = """insert into proj_user_his (proj_id,role_id,usr_id,outtime,cid) 
             select proj_id,role_id,usr_id,now(),%s from proj_user 
                where proj_id=%s and role_id=%s and ifuse=1 and not find_in_set(usr_id,'%s')
          """%(cid,proj_id,role_id,users)
    db.executesql(sql)

    sql = "update proj_user set ifuse=0,outtime=now() where proj_id=%s and role_id=%s and not find_in_set(usr_id,'%s')"%(proj_id,role_id,users)
    db.executesql(sql)
    
    sql = """insert into usr_role (usr_id,role_id,cid,ctime)
             select usr_id,%s,%s,now() from proj_user where role_id = %s and usr_id not in (select usr_id from usr_role where role_id = %s) group by usr_id ;
          """%(role_id,cid,role_id,role_id)
    db.executesql(sql)
    sql = "delete from usr_role where role_id = %s and usr_id not in (select usr_id from proj_user where role_id = %s and ifuse = 1 group by usr_id )"%(role_id,role_id)
    db.executesql(sql)
    return

def savePageFormList80501(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
   
    gw_type = data_list.get('ID','')
    right_roles = data_list.get('right_roles','')
    #print right_roles
    if gw_type=='':
        return
    sql = "delete from gw_role where gw_type=%s"%gw_type
    db.executesql(sql)
    if right_roles!='':
        roles = right_roles.split(',')
        for e in roles:
            sql = "insert into gw_role (gw_type,role_id) values (%s,%s)"%(gw_type,e)
            db.executesql(sql)
    return

#费用报销
def savePageFormList203(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)

    lists = data_list.get('pay_list','')
    cid = d_value[0]
    cusrname = d_value[1]
    
    for e in lists:
        print e
        status = e.get('status','')
        cel_id = e.get('cel_id','')
        cel_memo = e.get('cel_memo','')
        cel_memo = MySQLdb.escape_string(cel_memo)
        cel_money = e.get('cel_money','')
        cel_u_type = e.get('cel_u_type','')
        memo1 = e.get('memo1','')
        if status =='deleted':
            sql = "delete from cost_ea_list where id='%s'"%(cel_id)
            db.executesql(sql)
        elif cel_id != '':
            sql = """update cost_ea_list set memo='%s',Money=%s,U_type=%s,uid=%s,utime=now(),memo1='%s'  
                     where id = %s"""%(cel_memo,cel_money,cel_u_type,cid,memo1,cel_id)
            db.executesql(sql)
        else:
            sql = """insert into cost_ea_list 
                      (gw_id,memo,Money,U_type,cid,ctime,memo1)
                      values (%s,'%s',%s,%s,%s,now(),'%s')
                      """%(pk,cel_memo,cel_money,cel_u_type,cid,memo1)
            #print ToGBK(sql)
            if m_prjname != 'bygj':
                db.executesql(sql)

    lists1 = data_list.get('pay_list1','')
    for e in lists1:
        status = e.get('status','')
        cel_id = e.get('cel_id1','')
        cel_memo = e.get('cel_memo1','')
        cel_memo = MySQLdb.escape_string(cel_memo)
        cel_money = e.get('cel_money1','')
        cel_u_type = e.get('cel_u_type1','')
        cel_cost_dept = e.get('Cost_division','')
        if status =='deleted':
            sql = "delete from cost_ea_list where id='%s'"%(cel_id)
            db.executesql(sql)
        elif cel_id != '':
            sql = """update cost_ea_list set memo='%s',Money=%s,U_type=%s,Cost_dept_id=%s,uid=%s,utime=now() 
                     where id = %s"""%(cel_memo,cel_money,cel_u_type,cel_cost_dept,cid,cel_id)
            #print sql
            db.executesql(sql)
        else:
            sql = """insert into cost_ea_list 
                      (gw_id,memo,Money,U_type,Cost_dept_id,cid,ctime,sign)
                      values (%s,'%s',%s,%s,%s,%s,now(),0)
                      """%(pk,cel_memo,cel_money,cel_u_type,cel_cost_dept,cid)
            #print sql
            db.executesql(sql)

    sql="DELETE FROM borrow_list WHERE gw_id=%s;"%pk
    db.executesql(sql)
    #print data_list
    ea_total = data_list.get('ea_total','')
    return_res = data_list.get('return_res','')
    return_res = handleMutilValue(return_res,1)

    lists = data_list.get('borrow_list','')
    ea_total = float(ea_total)
    ea_total1 = float(ea_total)
    Borrow = 0    
    for e in lists:
        status = e.get('status','')
        cb_id = e.get('cb_id','')
        br_sel = e.get('br_sel','')
        br_sel = handleMutilValue(br_sel,1)
        br_money = e.get('br_money') or 0
        cb_money1 = e.get('cb_money1') or 0
        #print "%s %s %s %s"%(ea_total,br_money,br_sel,cb_money1)
        br_money = float(br_money) + float(cb_money1) 
        if str(br_sel)=='1':
            Borrow += br_money 
            if ea_total >= br_money:
                money = br_money
            elif str(return_res)=='1':
                money = br_money
            else:
                money = ea_total
            ea_total = ea_total - br_money
            if ea_total < 0: ea_total = 0 
            sql = "INSERT INTO borrow_list (gw_id,br_id,money,menu_id,cid,ctime) VALUES (%s,%s,%s,203,%s,now());"%(pk,cb_id,money,cid)
            #print sql
            db.executesql(sql)
    if Borrow>ea_total1:
        return_money = Borrow - ea_total1
        add_money = 0
    else:
        return_money = 0
        add_money = ea_total1 - Borrow
    lists = data_list.get('return_res','')
    return_res = handleMutilValue(return_res,1)

    print "return_res=%s"%(return_res)
    if str(return_res)!='1':
        return_money = 0
    sql = "update cost_ea set Borrow=%s,return_money=%s,add_money=%s where gw_id=%s"%(Borrow,return_money,add_money,pk)
    print sql
    db.executesql(sql)
    return

def savePageFormList216(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
   
    sql="DELETE FROM borrow_list WHERE gw_id=%s;"%pk
    db.executesql(sql)
    #print data_list
    ea_total = data_list.get('ea_total',0)
    return_res = data_list.get('return_res','')
    return_res = handleMutilValue(return_res,1)

    lists = data_list.get('borrow_list','')
    ea_total = float(ea_total)
    for e in lists:
        status = e.get('status','')
        cb_id = e.get('cb_id','')
        br_sel = e.get('br_sel','')
        br_sel = handleMutilValue(br_sel,1)
        br_money = e.get('br_money','0')
        #print "%s %s %s"%(ea_total,br_money,br_sel)
        br_money = float(br_money)
        if str(br_sel)=='1':
            if ea_total >= br_money:
                money = br_money
            elif str(return_res)=='1':
                money = br_money
            else:
                money = ea_total
            ea_total = ea_total - br_money
            if ea_total < 0: ea_total = 0 
            sql = "INSERT INTO borrow_list (gw_id,br_id,money,menu_id,cid,ctime) VALUES (%s,%s,%s,216,%s,now());"%(pk,cb_id,money,cid)
            #print sql
            db.executesql(sql)
        
    return

#收款管理
def savePageFormList208(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)

    lists = data_list.get('lists','')
    cid = d_value[0]
    cusrname = d_value[1]
   
    rec_money = data_list.get('rec_money','')
    main_sum = data_list.get('main_sum','')
    capital_id = data_list.get('capital_id','')
    cname = data_list.get('cname','')
    sn = data_list.get('sn','')
    rec_type = data_list.get('rec_type','')
    check_no = data_list.get('check_no','')
    memo = data_list.get('memo','')
    memo = MySQLdb.escape_string(memo)
    dept_id = 'NULL'
    proj_id = 'NULL'
    #登记流水账
    if mode == 'add' and capital_id!='':
        sql = """CALL upd_capital_manage(%s,%s,'%s','%s',%s,'%s',%s,%s,%s,%s,'%s','收款登记',@a)
              """%(capital_id,rec_money,sn,cname,rec_type,check_no,cid,dept_id,proj_id,menu_id,memo)
        #print sql
        db.executesql(sql)    
        sql = "select @a;"
        rows,iN = db.select(sql)
        balance = rows[0][0]
        sql = "update rec_money set balance = %s where id=%s"%(balance,pk)
        #print sql
        db.executesql(sql)    

    proj_id=''#记录下明细表的项目集，更新到主表的mul_proj_name，mul_mana_name
    ctr_id='' #记录下明细表的工程合同集，更新到主表的mul_ctr_name
    mul_proj_no=''
    mul_proj_name=''
    mul_mana_name=''
    mul_ctr_code=''
    mul_ctr_name=''
    mul_ctr_price=0
    main_sum1 = 0
    for e in lists:
        #print e
        status = e.get('status','')
        rml_id = e.get('rml_id',0)
        rml_ctype = e.get('rml_ctype','')
        rml_proj = e.get('rml_proj') or 'NULL'
        rml_ctr = e.get('rml_ctr') or 'NULL'
        rml_money = e.get('rml_money') or 0
        main_sum1 += float(rml_money)
        if str(rml_id) =='':  #新添加行
            if main_sum < main_sum1:
                break
            sql="""INSERT INTO rec_money_list (m_id,ctype, proj_id,ctr_id,money,res_money,cid,cusrname,ctime) values 
                         (%s,%s,%s,%s,%s,%s,%s,'%s',now())
                 """%(pk,rml_ctype,rml_proj,rml_ctr,rml_money,rml_money,cid,cusrname)
            db.executesql(sql)
        elif status =='deleted':  #删除行
            sql = "delete from rec_money_list where id=%s"%(rml_id)
            db.executesql(sql)
        elif status =='updated': 
            if main_sum < main_sum1:
                break
            sql = """update rec_money_list set                                 
                                ctype=%s,
                                proj_id=%s,
                                ctr_id=%s,
                                money=%s,
                                res_money=%s,
                                uid=%s,
                                uusrname='%s',
                                utime=now()
                    where id=%s"""%(rml_ctype,rml_proj,rml_ctr,rml_money,rml_money,cid,cusrname,rml_id)
            db.executesql(sql)
        if status !='deleted' and rml_proj!='':
            if proj_id=='':
                proj_id=rml_proj
            else:
                proj_id+=',%s'%rml_proj
        if status !='deleted' and rml_ctr!='':
            if ctr_id=='':
                ctr_id=rml_ctr
            else:
                ctr_id+=',%s'%rml_ctr

    if proj_id!='':
        sql="""SELECT gc_no, cname, mana_name 
                FROM out_proj
                WHERE FIND_IN_SET(id,'%s')
            """%proj_id
        lT,iN=db.select(sql)
        for e in lT:
            if mul_proj_no=='' and (e[0] is not None and e[0]!=''):
                mul_proj_no=e[0].strip()
            elif mul_proj_no!='' and (e[0] is not None and e[0]!=''):
                mul_proj_no+=',%s'%e[0].strip()
            if mul_proj_name=='' and (e[1] is not None and e[1]!=''):
                mul_proj_name=e[1].strip()
            elif mul_proj_name!='' and (e[1] is not None and e[1]!=''):
                mul_proj_name+=',%s'%e[1].strip()
            if mul_mana_name=='' and (e[2] is not None and e[2]!=''):
                mul_mana_name=e[2].strip()
            elif mul_mana_name!='' and (e[2] is not None and e[2]!=''):
                mul_mana_name+=',%s'%e[2].strip()
    if ctr_id!='':
        sql="""
                SELECT
                        code,    
                        cname,  
                        ifnull(price,0)   
                FROM contract_sg_file
                WHERE FIND_IN_SET(id,'%s')
            """%ctr_id
        lT,iN=db.select(sql)
        for e in lT:
            if mul_ctr_code=='' and (e[0] is not None and e[0]!=''):
                mul_ctr_code=e[0].strip()
            elif mul_ctr_code!='' and (e[0] is not None and e[0]!=''):
                mul_ctr_code+=',%s'%e[0].strip()
            if mul_ctr_name=='' and (e[1] is not None and e[1]!=''):
                mul_ctr_name=e[1].strip()
            elif mul_ctr_name and (e[1] is not None and e[1]!=''):
                mul_ctr_name+=',%s'%e[1].strip()
            mul_ctr_price+=e[2]
    sql="""
            UPDATE rec_money SET
                mul_proj_no='%s',   
                mul_proj_name='%s',    
                mul_mana_name='%s',   
                mul_ctr_code='%s',       
                mul_ctr_name='%s',       
                mul_ctr_price=%s
            WHERE id=%s;
        """%(mul_proj_no,mul_proj_name,mul_mana_name,mul_ctr_code,mul_ctr_name,mul_ctr_price,pk)
    #print sql
    db.executesql(sql)

    #print "%s %s"%(float(rec_money),float(main_sum))
    if float(rec_money) == float(main_sum):  
        sql = """UPDATE rec_money SET bltime=now(),is_maintained=1,main_usr_id=%s,main_usr_name='%s',main_date=now() WHERE id=%s"""%(cid,cusrname,pk)
        #print sql
        db.executesql(sql)
    
    return

	
#投标保证金付款
def savePageFormList209(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
    
    sql="SELECT id FROM bid_bond_req WHERE gw_id=%s"%pk
    lT,iN=db.select(sql)
    id = lT[0][0]
    sql="DELETE FROM bid_bond_req_rec WHERE br_id=%s"%id
    db.executesql(sql)
    lists = data_list.get('list','')
    for e in lists:
        status = e.get('status','')
        rml_id = e.get('rml_id',0)
        rml_sel = e.get('rml_sel',0)
        rml_sel = handleMutilValue(rml_sel,1)
        if str(rml_sel) == '1':
            sql="INSERT INTO bid_bond_req_rec (rcl_id,br_id) values (%s,%s)"%(rml_id,id)
            db.executesql(sql)
            sql = "update rec_money_list set fc_id=%s,link_menu_id=%s,link_gw_id=%s where id=%s"%(id,menu_id,pk,rml_id)
            db.executesql(sql)
            sql = "update rec_money rm,rec_money_list rml set rm.is_lock=1,rm.lock_usr_id=%s,rm.lock_time=now() where rm.id=rml.m_id and rml.id=%s"%(cid,rml_id)
            db.executesql(sql)

    return

#投标保证金退款
def savePageFormList210(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
    
    sql="SELECT id FROM bid_bond_refund WHERE gw_id=%s"%pk
    lT,iN=db.select(sql)
    id = lT[0][0]
    sql="DELETE FROM bid_bond_refund_rec WHERE br_id=%s"%id
    db.executesql(sql)
    lists = data_list.get('list','')
    for e in lists:
        status = e.get('status','')
        rml_id = e.get('rml_id',0)
        rml_sel = e.get('rml_sel',0)
        rml_sel = handleMutilValue(rml_sel,1)
        if str(rml_sel) == '1':
            sql="INSERT INTO bid_bond_refund_rec (rcl_id,br_id) values (%s,%s)"%(rml_id,id)
            db.executesql(sql)
            sql = "update rec_money_list set fc_id=%s,link_menu_id=%s,link_gw_id=%s where id=%s"%(id,menu_id,pk,rml_id)
            db.executesql(sql)
            sql = "update rec_money rm,rec_money_list rml set rm.is_lock=1,rm.lock_usr_id=%s,rm.lock_time=now() where rm.id=rml.m_id and rml.id=%s"%(cid,rml_id)
            db.executesql(sql)
    return

def savePageFormList239(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]

    proj_id=''#记录下明细表的项目集，更新到主表的mul_proj_name，mul_mana_name
    ctr_id='' #记录下明细表的工程合同集，更新到主表的mul_ctr_name
    mul_proj_no=''
    mul_proj_name=''
    mul_mana_name=''
    mul_ctr_code=''
    mul_ctr_name=''
    mul_ctr_price=0
    for e in lists:
        #print e
        status = e.get('status','')
        rml_proj = e.get('proj_id') or 'NULL'
        rml_ctr = e.get('ctr_id') or 'NULL'
        if status !='deleted' and rml_proj!='':
            if proj_id=='':
                proj_id=rml_proj
            else:
                proj_id+=',%s'%rml_proj
        if status !='deleted' and rml_ctr!='':
            if ctr_id=='':
                ctr_id=rml_ctr
            else:
                ctr_id+=',%s'%rml_ctr

    if proj_id!='':
        sql="""SELECT gc_no, cname, mana_name 
                FROM out_proj
                WHERE FIND_IN_SET(id,'%s')
            """%proj_id
        lT,iN=db.select(sql)
        for e in lT:
            if mul_proj_no=='' and (e[0] is not None and e[0]!=''):
                mul_proj_no=e[0].strip()
            elif mul_proj_no!='' and (e[0] is not None and e[0]!=''):
                mul_proj_no+=',%s'%e[0].strip()
            if mul_proj_name=='' and (e[1] is not None and e[1]!=''):
                mul_proj_name=e[1].strip()
            elif mul_proj_name!='' and (e[1] is not None and e[1]!=''):
                mul_proj_name+=',%s'%e[1].strip()
            if mul_mana_name=='' and (e[2] is not None and e[2]!=''):
                mul_mana_name=e[2].strip()
            elif mul_mana_name!='' and (e[2] is not None and e[2]!=''):
                mul_mana_name+=',%s'%e[2].strip()
    if ctr_id!='':
        sql="""
                SELECT
                        code,    
                        cname,  
                        ifnull(price,0)   
                FROM contract_sg_file
                WHERE FIND_IN_SET(id,'%s')
            """%ctr_id
        lT,iN=db.select(sql)
        for e in lT:
            if mul_ctr_code=='' and (e[0] is not None and e[0]!=''):
                mul_ctr_code=e[0].strip()
            elif mul_ctr_code!='' and (e[0] is not None and e[0]!=''):
                mul_ctr_code+=',%s'%e[0].strip()
            if mul_ctr_name=='' and (e[1] is not None and e[1]!=''):
                mul_ctr_name=e[1].strip()
            elif mul_ctr_name and (e[1] is not None and e[1]!=''):
                mul_ctr_name+=',%s'%e[1].strip()
            mul_ctr_price+=e[2]
    sql="""
            UPDATE _m239_cbjx SET
                mul_proj_no='%s',   
                mul_proj_name='%s',    
                mul_mana_name='%s',   
                mul_ctr_code='%s',       
                mul_ctr_name='%s',       
                mul_ctr_price=%s
            WHERE id=%s;
        """%(mul_proj_no,mul_proj_name,mul_mana_name,mul_ctr_code,mul_ctr_name,mul_ctr_price,pk)
    #print sql
    db.executesql(sql)
    
    return

#资金预付管理
def savePageFormList308(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
   
    sql="SELECT id FROM fund_call WHERE gw_id=%s"%pk
    lT,iN=db.select(sql)
    id = lT[0][0]
    sql="DELETE FROM fund_rec WHERE fc_id=%s"%id
    db.executesql(sql)
    lists = data_list.get('rec_list','')
    for e in lists:
        status = e.get('status','')
        rml_id = e.get('rml_id',0)
        rml_sel = e.get('rml_sel',0)
        rml_sel = handleMutilValue(rml_sel,1)
        if str(rml_sel) == '1':
            sql="INSERT INTO fund_rec (rcl_id,fc_id) values (%s,%s)"%(rml_id,id)
            db.executesql(sql)
            sql = "update rec_money_list set fc_id=%s,link_menu_id=%s,link_gw_id=%s where id=%s"%(id,menu_id,pk,rml_id)
            db.executesql(sql)
            sql = "update rec_money rm,rec_money_list rml set rm.is_lock=1,rm.lock_usr_id=%s,rm.lock_time=now() where rm.id=rml.m_id and rml.id=%s"%(cid,rml_id)
            db.executesql(sql)
    lists = data_list.get('jk_list','')
    for e in lists:
        jk_mxid = e.get('jk_mxid','')
        jk_gwid = e.get('jk_gwid','')
        jk_total = e.get('jk_total','')
        jk_capital = e.get('jk_capital','')
        jk_fee = e.get('jk_fee','')
        jk_memo = e.get('jk_memo','')
        jk_menu_id = e.get('jk_menu_id','')
        jk_menu_name = e.get('jk_menu_name','')
        jk_memo = MySQLdb.escape_string(jk_memo)
        if jk_capital != '' or jk_fee !='':
            if jk_capital == '': jk_capital = 0
            if jk_fee == '': jk_fee = 0
            if jk_mxid == '':
                sql = "insert into _m220_xmlsjk_zjdk (gw_id,cid,cusrname,ctime,JK_GWID,JK_TOTAL,CAPITAL,FEE,MEMO,menu_id,menu_name) values (%s,%s,'%s',now(),%s,%s,%s,%s,'%s',308,'项目资金预付')"%(pk,cid,cusrname,jk_gwid,jk_total,jk_capital,jk_fee,jk_memo)
                db.executesql(sql)
            else:
                sql = "update _m220_xmlsjk_zjdk set JK_GWID=%s,JK_TOTAL=%s,CAPITAL=%s,FEE=%s,MEMO='%s' where id=%s"%(jk_gwid,jk_total,jk_capital,jk_fee,jk_memo,jk_mxid)
                db.executesql(sql)
        elif jk_mxid != '':
            sql = "delete from _m220_xmlsjk_zjdk where id = %s"%(jk_mxid)
            db.executesql(sql)
        #print sql
    return

#组织机构管理
def savePageFormList501(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]
   
    lxr = data_list.get('lxr','')
    lxr_tel = data_list.get('lxr_tel','')
    lxr_fax = data_list.get('lxr_fax','')
    if lxr=='' :
        return

    sql = "select id from addr_book where sup_id='%s' and name='%s'"%(pk,lxr)
    rows,iN = db.select(sql)
    if iN==0:
        sql = "insert into addr_book (name,cotel,cofax,sup_id) values ('%s','%s','%s','%s')"%(lxr,lxr_tel,lxr_fax,pk)  
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows1,iN1 = db.select(sql)
        aid = rows1[0][0]
        sql = """insert into `addr_book_group` (`addr_group_id`,`addr_book_id`,`ctime`,`cid`,`cusrname`) 
                 values(2,%s,now(),%s,'%s');"""%(aid,cid,cusrname)
        db.executesql(sql)
    else:
        aid = rows[0][0]
        sql = "update addr_book set cotel='%s',cofax='%s' where id=%s"%(lxr_tel,lxr_fax,aid)  
        db.executesql(sql)
    sql = "update suppliers set lxid=%s where id=%s"%(aid,pk)  
    db.executesql(sql)

    return

#入库申请
def savePageFormList41102(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]

    rk_lists = data_list.get('ysrk_list','')
    qt_lists = data_list.get('qtfy_list','')

    #入库
    for e in rk_lists:
        status = e.get('status','')
        rkl_id = e.get('rkl_id','')
        cg_gwid = e.get('cg_gwid','')
        cgmx_id = e.get('cgmx_id','')
        rk_mat_id = e.get('mat_id','')
        brand_id = e.get('brand_id','')
        cg_count = e.get('cg_count','')
        yrk_count = e.get('yrk_count','')
        wrk_count = e.get('wrk_count','')
        rk_count = e.get('rk_count','')
        rk_price = e.get('rk_price','')
        rk_amout = e.get('rk_amout','')
        if str(rkl_id) =='' and status !='deleted':  #新添加行
            sql="""insert into `_m41102_rk_list` (`gw_id`,`cg_gwid`,`cgmx_id`,`mat_id`,`brand_id`,`cg_qty`,`yrk_qty`,`wrk_qty`,`qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',now())
                 """%(pk,cg_gwid,cgmx_id,rk_mat_id,brand_id,cg_count,yrk_count,wrk_count,rk_count,rk_price,rk_amout,cid,cusrname)
            print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted' and str(rkl_id) !='':  #删除行
            sql = "delete from _m41102_rk_list where id=%s"%(rkl_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m41102_rk_list set                                 
                                qty=%s,
                                price=%s,
                                amount=%s,
                                uid=%s,
                                uusrname='%s',
                                utime=now()
                    where id=%s"""%(rk_count,rk_price,rk_amout,cid,cusrname,rkl_id)
            db.executesql(sql)

    return

#材料款付款管理
def savePageFormList410(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]

    cghe_list = data_list.get('cghe_list','')
    rk_list = data_list.get('rk_list','')
    dh_list = data_list.get('dh_list','')
    th_list = data_list.get('th_list','')
    kk_list = data_list.get('kk_list','')

    #合同
    for e in cghe_list:
        print e
        status = e.get('status','')
        ht_id = e.get('ht_id','')
        ht_gwid = e.get('ht_gwid','')
        ht_price = e.get('ht_price','')
        ht_yf = e.get('ht_yf') or 0
        ht_dk = e.get('ht_dk') or 0
        ht_cur_yf = e.get('ht_cur_yf') or 0
        ht_cur_dk = e.get('ht_cur_dk') or 0
        ht_memo = e.get('ht_memo','')
        ht_memo = MySQLdb.escape_string(ht_memo)
        if str(ht_id) =='' and status !='deleted':  #新添加行
            sql="""insert into `_m410_clkfk_ht` (`gw_id`,`ht_gwid`,`ht_total`,`yyf_total`,`wyf_total`,`money`,`dk_money`,`memo`,`cid`,`cusrname`,`ctime`)
                 values(%s,%s,%s,%s,%s,%s,%s,'%s',%s,'%s',now())
                 """%(pk,ht_gwid,ht_price,ht_yf,ht_dk,ht_cur_yf,ht_cur_dk,ht_memo,cid,cusrname)
            #print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted' and str(ht_id) !='':  #删除行
            sql = "delete from _m410_clkfk_ht where id=%s"%(ht_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m410_clkfk_ht set                                 
                                money=%s,
                                dk_money=%s,
                                memo='%s'
                    where id=%s"""%(ht_cur_yf,ht_cur_dk,ht_memo,ht_id)
            db.executesql(sql)

    #入库
    for e in rk_list:
        status = e.get('status','')
        rk_id = e.get('rk_id','')
        rkd_gwid = e.get('rkd_gwid','')
        rkd_total = e.get('rkd_total','')
        rk_wfk = e.get('rk_wfk','')
        rk_price = e.get('rk_price')  or 0 
        if str(rk_id) =='' and status !='deleted':  #新添加行
            sql="""insert into `_m410_clkfk_rkd` (`gw_id`,`rk_gwid`,`rk_total`,`wrk_total`,`fk_total`,`cid`,`cusrname`,`ctime`)
                   values(%s,%s,%s,%s,%s,%s,'%s',now())
                 """%(pk,rkd_gwid,rkd_total,rk_wfk,rk_price,cid,cusrname)
            #print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted' and str(rk_id) !='':  #删除行
            sql = "delete from _m410_clkfk_rkd where id=%s"%(rk_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m410_clkfk_rkd set                                 
                                fk_total=%s
                    where id=%s"""%(rk_price,rk_id)
            db.executesql(sql)

    #订货单
    for e in dh_list:
        status = e.get('status','')
        dh_id = e.get('dh_id','')
        dh_gwid = e.get('dh_gwid','')
        dh_total = e.get('dh_total','')
        dh_wfk = e.get('dh_wfk','')
        dh_money = e.get('dh_money') or 0 
        if str(dh_id) =='' and status !='deleted':  #新添加行
            sql="""insert into `_m410_clkfk_dhd` (`gw_id`,`dh_gwid`,`dh_total`,`wfk_total`,`fk_money`,`cid`,`cusrname`,`ctime`)
                   values(%s,%s,%s,%s,%s,%s,'%s',now())
                 """%(pk,dh_gwid,dh_total,dh_wfk,dh_money,cid,cusrname)
            #print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted' and str(dh_id) !='':  #删除行
            sql = "delete from _m410_clkfk_dhd where id=%s"%(dh_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m410_clkfk_dhd set                                 
                                fk_money=%s
                    where id=%s"""%(dh_money,dh_id)
            db.executesql(sql)

    #退货单
    for e in th_list:
        status = e.get('status','')
        th_id = e.get('th_id','')
        th_gwid = e.get('th_gwid','')
        th_total = e.get('th_total','')
        th_money = e.get('th_money')  or 0 
        if str(th_id) =='' and status !='deleted':  #新添加行
            sql="""insert into `_m410_clkfk_thd` (`gw_id`,`th_gwid`,`dh_total`,`money`,`cid`,`cusrname`,`ctime`)
                   values(%s,%s,%s,%s,%s,'%s',now())
                 """%(pk,th_gwid,th_total,th_money,cid,cusrname)
            #print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted' and str(th_id) !='':  #删除行
            sql = "delete from _m410_clkfk_thd where id=%s"%(th_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m410_clkfk_thd set                                 
                                fk_total=%s
                    where id=%s"""%(th_money,th_id)
            db.executesql(sql)

    #扣款
    for e in kk_list:
        status = e.get('status','')
        kk_id = e.get('kk_id','')
        kk_type = e.get('kk_type','')
        kk_money = e.get('kk_money','')
        kk_memo = e.get('kk_memo','')
        if str(kk_id) =='':  #新添加行
            sql="""insert into `_m410_clkfk_kk` (`gw_id`,`kk_type`,`kk_money`,`kk_memo`,`cid`,`cusrname`,`ctime`)
                 values(%s,%s,%s,'%s',%s,'%s',now())
                 """%(pk,kk_type,kk_money,kk_memo,cid,cusrname)
            #print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted':  #删除行
            sql = "delete from _m410_clkfk_kk where id=%s"%(kk_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m410_clkfk_kk set                                 
                                kk_type=%s,
                                kk_money=%s,
                                kk_memo = '%s'
                    where id=%s"""%(kk_type,kk_money,kk_memo,kk_id)
            db.executesql(sql)

    return

#材料款拨付管理
def savePageFormList540(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = d_value[0]
    cusrname = d_value[1]

    fk_gwid = data_list.get('fk_gwid','')
    ck_list = data_list.get('ck_list','')

    for e in ck_list:
        status = e.get('status','')
        ck_id = e.get('ck_id','')
        ck_memo = e.get('ck_memo','')
        ck_money = e.get('ck_money','')
        ck_khh = e.get('ck_khh','')
        ck_hm = e.get('ck_hm','')
        ck_bankno = e.get('ck_bankno','')
        if str(ck_id) =='':  #新添加行
            sql="""insert into `_m540_clfkbf_list` (`gw_id`,fk_gwid,`memo`,`pay_money`,`rec_name`,rec_bank,rec_bank_no,`cid`,`ctime`)
                 values(%s,%s,'%s',%s,'%s','%s','%s',%s,now())
                 """%(pk,fk_gwid,ck_memo,ck_money,ck_hm,ck_khh,ck_bankno,cid)
            #print ToGBK(sql)
            db.executesql(sql)
        elif status =='deleted':  #删除行
            sql = "delete from _m540_clfkbf_list where id=%s"%(ck_id)
            db.executesql(sql)
        elif status =='updated': 
            sql = """update _m540_clfkbf_list set                                 
                                memo='%s',
                                pay_money=%s
                    where id=%s"""%(ck_memo,ck_money,ck_id)
            db.executesql(sql)

    return

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