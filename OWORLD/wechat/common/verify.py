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
exec ('from %s.share import db,dActiveUser,mValidateUser,HttpResponseCORS,ToGBK,m_prjname'%prj_name) 
from save_list import savePageFormList303

def savePageVerify(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    global d_value
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    cid = d_value[0] 
    cusrname = d_value[1] 
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    value_dict = dict()    

    tab = request.POST.get('tab', '')
    step = request.POST.get('step', 1)
    if step=='':
        step = 1
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    #print data_list
    pk =  data_list.get('pk','')
    random_no = data_list.get('random_no','')
    sql = """SELECT id,final_sql,has_audit FROM menu_form_steps where menu_id=%s and step=%s """%(menu_id,step)
    #print sql
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
    else:
        step_id = 0
    has_audit = rows_table[0][2]

    sql = """SELECT id,save_table,is_list,del_before_update,delete_sql,field_name
                    FROM menu_form_save_tables 
                    where is_procedure=0 and step_id=%s and status=1 and is_list=0 order by sort"""%(step_id)
    print sql
    rows_table,iN = db.select(sql)
    for e_table in rows_table:
        table_id = e_table[0]
        table_name = e_table[1] or ''
        sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field
                    FROM menu_form_save_cols
                    where table_id=%s and (is_verify=1 or is_index=1)"""%(table_id)
        #print sql
        rows,iN = db.select(sql)

        sql = """update %s set """%(table_name)
        for e in rows:
            if e[4]==0:
                sql += "%s="%(e[0])
                value = getSaveValue(data_list,e[7],e[2])
                if e[2] == 1:
                    sql += "%s,"%(value)
                else:
                    sql += "'%s',"%(value)
        sql += " status = 1,"
        if str(has_audit) == '1':
            sql += " gw_status = 2,"
        sql = sql[:-1]
        sql_where = " where 1=1"
        for e in rows:
            if e[4]==1:
                value = getSaveValue(data_list,e[7],e[2])
                sql_where += " and %s=%s"%(e[0],value)
        sql += sql_where
        print ToGBK(sql)
        db.executesql(sql)

        try:
            sql1 = "update %s set vid=%s,vusrname='%s',vtime=now() %s"%(table_name,cid,cusrname,sql_where)
            db.executesql(sql1)
        except:
            pass

    if str(has_audit) == '1':
        sql = """UPDATE gw_doc SET status = 8, status_txt = '已登记'  WHERE id = %s;
            """%(pk)
        db.executesql(sql)
    if str(menu_id) == '207':  #预借（付）款登记
         saveVerify207(data_list)
    elif str(menu_id) == '203':  #费用报销
         saveVerify203(data_list)
    elif str(menu_id) == '309':  #资金拨付管理
         saveVerify309(data_list)
    elif str(menu_id) == '209':  #投标保证金付款
         saveVerify209(data_list)
    elif str(menu_id) == '210':  #投标保证金退款
         saveVerify210(data_list)
    elif str(menu_id) == '235':  #开增值税发票
         saveVerify235(data_list)
    elif str(menu_id) == '540':  #材料款拨付
         saveVerify540(data_list)
    elif str(menu_id) == '229':  #外经证管理
         saveVerify229(data_list)
    elif str(menu_id)=='303' and m_prjname != 'hcpra':  #立项管理
        savePageFormList303(pk,mode,'',d_value,request)
    elif str(menu_id)=='304' and m_prjname == 'hcpra':  #立项管理
        savePageFormList303(pk,mode,'',d_value,request)
    else:
        #处理明细表的保存
        sql = """SELECT id,save_table,is_list,del_before_update,delete_sql,field_name
                    FROM menu_form_save_tables 
                    where is_procedure=0 and step_id=%s and status=1 and is_list = 1 order by sort"""%(step_id)
        rows_table,iN = db.select(sql)
        for e_table in rows_table:
            table_id = e_table[0]
            table_name = e_table[1].lower() or ''
            is_list = e_table[2] or 0
            field_name = e_table[5] or ''

            sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field
                    FROM menu_form_save_cols
                    where table_id=%s and (is_verify=1 or is_index=1)"""%(table_id)
            rows,iN = db.select(sql)
            if iN>0:
                savePageFormList(pk,mode,table_name,data_list,value_dict,rows,field_name,request,has_audit,d_value)


    if m_prjname == 'hcpra':
        from save_ext_hc import saveVerifyExt
    else:
        from save_ext import saveVerifyExt

    sql=" delete from gw_verify where gw_id = %s"%(pk)
    #print sql
    db.executesql(sql)

    saveVerifyExt(pk,mode,d_value,request)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def savePageFormList(pk,mode,table_name,data_list,value_dict,rows,field_name,request,has_audit,d_value):
    if field_name =='':
        return
    cid = d_value[0] 
    cusrname = d_value[1] 

    list1 = data_list[field_name]
    n = 1
    for e1 in list1: 
        status = e1['status']
        bNew = 0
        for e in rows:
            if e[4]==1:
                value = getSaveValue(e1,e[7],e[2])
                if value=='' or str(value)=='NULL':
                    bNew = 1
        if bNew==1:  #新添加行
            sql = """insert into %s ("""%(table_name)  #添加数据
            for e in rows:
                if e[4]==0:                       
                    sql += "%s,"%(e[0])
            sql = sql[:-1]
            sql += ") values ("
             
            for e in rows:
                value = getSaveValue(e1,e[7],e[2])
                if e[4] == 0: 
                    if e[2] == 1:
                        sql += "%s,"%(value)
                    else:
                        sql += '"%s",'%(value)
            sql = sql[:-1]
            sql += ')'
            print ToGBK(sql)
            '''try:
                db.executesql(sql)
            except:
                s = """
                        {
                        "errcode": -1,
                        "errmsg": "数据添加失败！",
                        }
                        """  
                return HttpResponseCORS(request,s)'''
            sql = "select last_insert_id();"
            rows2,iN2 = db.select(sql)
            id = rows2[0][0]
            try:
                if str(has_audit) == '1':
                    sql = "update %s set gw_id=%s,cid=%s,cusrname='%s',ctime=now() where id = %s"%(table_name,pk,cid,cusrname,id)
                else:
                    sql = "update %s set m_id=%s,cid=%s,cusrname='%s',ctime=now() where id = %s"%(table_name,pk,cid,cusrname,id)
                db.executesql(sql)
            except:
                pass
        elif status =='deleted':  #删除行
            sql_where = " where 1=1"
            j = 0
            for e in rows:
                if e[4]==1:
                    j += 1
                    value = getSaveValue(e1,e[7],e[2])
                    sql_where += " and %s=%s"%(e[0],value)
            if j>0:
                sql = "delete from %s %s"%(table_name,sql_where)
                db.executesql(sql)
        elif status =='exist':
            pass
        else:  #
            sql = """update %s set """%(table_name)
            
            for e in rows:
                value = getSaveValue(e1,e[7],e[2])
                if e[4]==0:
                    sql += "%s="%(e[0])
                    if e[2] == 1:
                        sql += '%s,'%(value)
                    else:
                        sql += '"%s",'%(value)
            sql = sql[:-1]
            sql_where = " where 1=1"
            j = 0
            for e in rows:
                if e[4]==1:
                    j += 1
                    value = getSaveValue(e1,e[7],e[2])
                    sql_where += " and %s=%s"%(e[0],value)
            sql += sql_where
            if j>0:
                print ToGBK(sql)
                db.executesql(sql)
        n = n + 1
    return

def saveVerify207(data_list):
    sn = data_list.get('sn','')
    capital_id = data_list.get('capital_id','')
    br_money = data_list.get('br_money','')
    title = data_list.get('title','')
    memo = data_list.get('pay_memo','')
    
    pk =  data_list.get('pk','')
       
    check_no = data_list.get('check_no','')
    pay_class = data_list.get('pay_class','')
    pay_usr_id = data_list.get('pay_usr_id','')
   
    sql = "select proj_id,dept_id from cost_borrow where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    proj_id = rows[0][0] or 'NULL'
    dept_id = rows[0][1] or 'NULL'
  
    sql = "update capital_manage set balance = balance - %s where id=%s"%(br_money,capital_id)
    db.executesql(sql)

    sql = "select ifnull(balance,0) from capital_manage where id=%s"%capital_id
    rows,iN = db.select(sql)
    balance = rows[0][0] - float(br_money)

    sql = """INSERT INTO capital_flow (pay_date,sn,title,payout,balance,bill_type,check_no,cid,dept_id,proj_id,memo,source,capital_id,menu_id)
                    VALUES (now(),'%s','%s',%s,%s,%s,'%s',%s,%s,%s,'%s','预借（付）款登记',%s,207)
          """%(sn,title,br_money,balance,pay_class,check_no,pay_usr_id,dept_id,proj_id,memo,capital_id)
    #print ToGBK(sql)
    db.executesql(sql)
    return

def saveVerify203(data_list):
    sn = data_list.get('sn','')
    capital_id = data_list.get('capital_id','')
    title = data_list.get('title','')
    memo = data_list.get('pay_memo','')
    
    pk =  data_list.get('pk','')
    ea_total = float(data_list.get('ea_total',''))
    return_money = float(data_list.get('return_money') or 0)
    add_money = float(data_list.get('add_money') or 0)
      
    check_no = data_list.get('check_no','')
    pay_class = data_list.get('pay_class','')
    pay_usr_id = data_list.get('pay_usr_id','')
   
    sql = "select proj_id,dept_id,return_res from cost_ea where gw_id=%s"%(pk)
    #print sql
    rows,iN = db.select(sql)
    proj_id = rows[0][0] or 'NULL'
    dept_id = rows[0][1] or 'NULL'
    return_res = rows[0][2] or 0
    money = 0
    if return_money > 0 and return_res==1:
        money = -return_money  
    elif add_money>0:
        money = add_money
    print "%s %s %s %s "%(return_money,add_money,money,return_res)
    sql = "update capital_manage set balance = balance - %s where id=%s"%(money,capital_id)
    db.executesql(sql)

    sql = "select balance from capital_manage where id=%s"%capital_id
    rows,iN = db.select(sql)
    balance = rows[0][0] - money
    
    global d_value
    cid = d_value[0]
    cname = d_value[1]
    sql = """UPDATE cost_ea SET balance=%s,
                                pay_usr_id=%s,
                                pay_usr_name='%s',
                                status=1,
                                pay_class=%s,
                                capital_id=%s,
                                check_no='%s',
                                pay_memo='%s'
                WHERE gw_id=%s;
          """%(balance,cid,cname,pay_class,capital_id,check_no,memo,pk)
    #print sql
    db.executesql(sql)    
    
    if money==0:
        return 
    if money>0:
        sql = """INSERT INTO capital_flow (pay_date,sn,title,payout,balance,bill_type,check_no,cid,dept_id,proj_id,memo,source,capital_id,menu_id)
                    VALUES (now(),'%s','%s',%s,%s,%s,'%s',%s,%s,%s,'%s','费用报销',%s,203)
              """%(sn,title,money,balance,pay_class,check_no,pay_usr_id,dept_id,proj_id,memo,capital_id)
    else:
        sql = """INSERT INTO capital_flow (pay_date,sn,title,income,balance,bill_type,check_no,cid,dept_id,proj_id,memo,source,capital_id,menu_id)
                    VALUES (now(),'%s','%s',%s,%s,%s,'%s',%s,%s,%s,'%s','费用报销(核销应退余额)',%s,203)
              """%(sn,title,-money,balance,pay_class,check_no,pay_usr_id,dept_id,proj_id,memo,capital_id)
    #print ToGBK(sql)
    db.executesql(sql)
    return

def saveVerify309(data_list):
    sn = data_list.get('sn','')
    pk =  data_list.get('pk','')
    m_id =  data_list.get('id','')
    lists = data_list.get('pay_list','')
    n = 1
    sql = "select proj_id from _m309_ZJBF where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    proj_id = rows[0][0] or 'NULL'
    dept_id = 'NULL'
    global d_value
    usr_id = d_value[0] 
    usr_name = d_value[1] 
    n = 0
    for e in lists:
        #print e
        status = e.get('status','')
        mx_id = e.get('mx_id','')
        pay_date = e.get('pay_date','')
        fk_paytype2 = e.get('fk_paytype2','')
        fk_fkh2 = e.get('fk_fkh2','')
        fk_pz2 = e.get('fk_pz2','')
        fk_checkno2 = e.get('fk_checkno2','')
        pl_money = e.get('money1','')
        pl_memo = e.get('comment1','')
        if pay_date =='':
            pay_date = getToday(7)

        sql = "select balance from capital_manage where id=%s"%fk_fkh2
        rows,iN = db.select(sql)
        balance = rows[0][0] - float(pl_money)

        if str(mx_id) !='':  
            sql = """update fund_call_list set pay_date='%s',pay_class=%s,capital_id=%s,check_no='%s',warrant_id='%s',balance=%s
                          where id=%s
                      """%(pay_date,fk_paytype2,fk_fkh2,fk_checkno2,fk_pz2,balance,mx_id)          
 
            db.executesql(sql) 
 
        sql = "update capital_manage set balance = balance - %s where id=%s"%(pl_money,fk_fkh2)
        db.executesql(sql)
        sql = """INSERT INTO capital_flow (pay_date,sn,title,payout,balance,bill_type,check_no,cid,dept_id,proj_id,memo,source,capital_id,menu_id)
                    VALUES (now(),'%s','%s',%s,%s,%s,'%s',%s,%s,%s,'%s','资金预付',%s,309)
              """%(sn,'',pl_money,balance,fk_paytype2,fk_checkno2,usr_id,dept_id,proj_id,pl_memo,fk_fkh2)
        db.executesql(sql)
        n += 1
    return

def saveVerify209(data_list):
    sn = data_list.get('sn','')
    pk =  data_list.get('pk','')
    m_id =  data_list.get('id','')
    lists = data_list.get('pay_list','')
    n = 1
    sql = "select proj_id from bid_bond_req where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    proj_id = rows[0][0] or 'NULL'
    dept_id = 'NULL'
    global d_value
    usr_id = d_value[0] 
    usr_name = d_value[1] 
    n = 0
    for e in lists:
        #print e
        status = e.get('status','')

        pl_id = e.get('pl_id','')
        pl_date = e.get('pl_date','')
        pl_money = e.get('pl_money','')
        pl_pz = e.get('pl_pz','')
        pl_type = e.get('pl_type','')
        pl_check = e.get('pl_check','')
        pl_name = e.get('pl_name','')
        pl_bank = e.get('pl_bank','')
        pl_bank_no = e.get('pl_bank_no','')
        pl_captal = e.get('pl_captal','')
        sql = "select balance from capital_manage where id=%s"%pl_captal
        rows,iN = db.select(sql)
        balance = rows[0][0] - float(pl_money)

        if str(pl_id) =='0' or str(pl_id) =='':  #新添加行
            sql = """insert into bid_bond_check (gw_id,pay_date,pay_class,capital_id,check_no,pay_money
                          ,balance,warrant_id,rec_name,rec_bank,rec_bank_no,cid,ctime)
                           values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now());
                      """%(pk,pl_date,pl_type,pl_captal,pl_check,pl_money,balance,pl_pz,pl_name,pl_bank,pl_bank_no,usr_id)           
        elif status =='deleted':  #删除行
            sql = "delete from bid_bond_check where id=%s"%(pl_id)
        #else:
        #    sql = "update bid_bond_check set sort=%s where id=%s"%(n,pl_id)
        #print sql
        db.executesql(sql) 
 
        sql = "update capital_manage set balance = balance - %s where id=%s"%(pl_money,pl_captal)
        db.executesql(sql)
        sql = """INSERT INTO capital_flow (pay_date,sn,title,payout,balance,bill_type,check_no,cid,dept_id,proj_id,memo,source,capital_id,menu_id)
                    VALUES (now(),'%s','%s',%s,%s,%s,'%s',%s,%s,%s,'%s','投标保证金付款',%s,209)
              """%(sn,'',pl_money,balance,pl_type,pl_check,usr_id,dept_id,proj_id,'',pl_captal)
        db.executesql(sql)
        n += 1
    return

def saveVerify210(data_list):
    sn = data_list.get('sn','')
    pk =  data_list.get('pk','')
    m_id =  data_list.get('id','')
    lists = data_list.get('pay_list','')
    n = 1
    sql = "select proj_id from bid_bond_refund where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    proj_id = rows[0][0] or 'NULL'
    dept_id = 'NULL'
    global d_value
    usr_id = d_value[0] 
    usr_name = d_value[1] 
    n = 0
    for e in lists:
        #print e
        status = e.get('status','')

        pl_id = e.get('pl_id','')
        pl_date = e.get('pl_date','')
        pl_money = e.get('pl_money','')
        pl_pz = e.get('pl_pz','')
        pl_type = e.get('pl_type','')
        pl_check = e.get('pl_check','')
        pl_name = e.get('pl_name','')
        pl_bank = e.get('pl_bank','')
        pl_bank_no = e.get('pl_bank_no','')
        pl_captal = e.get('pl_captal','')
        sql = "select balance from capital_manage where id=%s"%pl_captal
        rows,iN = db.select(sql)
        balance = rows[0][0] - float(pl_money)

        if str(pl_id) =='0' or str(pl_id) =='':  #新添加行
            sql = """insert into bid_bond_refund_list (gw_id,pay_date,pay_class,capital_id,check_no,pay_money
                          ,balance,warrant_id,rec_name,rec_bank,rec_bank_no,cid,ctime)
                           values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now());
                      """%(pk,pl_date,pl_type,pl_captal,pl_check,pl_money,balance,pl_pz,pl_name,pl_bank,pl_bank_no,usr_id)           
        elif status =='deleted':  #删除行
            sql = "delete from bid_bond_refund_list where id=%s"%(pl_id)
        #else:
        #    sql = "update bid_bond_refund_list set sort=%s where id=%s"%(n,pl_id)
        #print sql
        db.executesql(sql) 
 
        sql = "update capital_manage set balance = balance - %s where id=%s"%(pl_money,pl_captal)
        db.executesql(sql)
        sql = """INSERT INTO capital_flow (pay_date,sn,title,payout,balance,bill_type,check_no,cid,dept_id,proj_id,memo,source,capital_id,menu_id)
                    VALUES (now(),'%s','%s',%s,%s,%s,'%s',%s,%s,%s,'%s','投标保证金退款',%s,209)
              """%(sn,'',pl_money,balance,pl_type,pl_check,usr_id,dept_id,proj_id,'',pl_captal)
        db.executesql(sql)
        n += 1
    return

def saveVerify235(data_list):
    pk =  data_list.get('pk','')
    lists = data_list.get('dj_list','')
    n = 1
    global d_value
    usr_id = d_value[0] 
    usr_name = d_value[1] 
    n = 0
    for e in lists:
        #print e
        status = e.get('status','')

        fp_id = e.get('fp_id','')
        kp_date = e.get('kp_date','')
        fpdm = e.get('fpdm','')
        fphm = e.get('fphm','')
        fp_price = e.get('fp_price','')
        fp_zzs = e.get('fp_zzs','')
        fp_hj = e.get('fp_hj','')
        fp_scope = e.get('fp_scope','')
        fp_taxType = e.get('fp_taxType','')

        if str(fp_id) =='0' or str(fp_id) =='':  #新添加行
            sql = """insert into `_m235_zzs_kp_list` (`gw_id`,`kp_date`,`fpdm`,`fphm`,`js_price`,`zzs`,`js_total`,`taxType`,`scope2`,`cid`,`ctime`)
                         values(%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s',now());
                      """%(pk,kp_date,fpdm,fphm,fp_price,fp_zzs,fp_hj,fp_scope,fp_taxType,usr_id)           
        elif status =='deleted':  #删除行
            sql = "delete from _m235_zzs_kp_list where id=%s"%(fp_id)
        else:
            sql = "update _m235_zzs_kp_list set kp_date='%s',fpdm='%s',fphm='%s',js_price='%s',`zzs`='%s',js_total='%s' where id=%s"%(kp_date,fpdm,fphm,fp_price,fp_zzs,fp_hj,fp_id)
        #print sql
        db.executesql(sql) 
 
        n += 1
    sql = "update _m235_zzs_kp set dj_fs=%s where gw_id=%s"%(n,pk)
    db.executesql(sql) 
    return

def saveVerify540(data_list):
    pk =  data_list.get('pk','')
    lists = data_list.get('ck_list','')
    n = 1
    global d_value
    usr_id = d_value[0] 
    usr_name = d_value[1] 
    n = 0
    for e in lists:
        #print e
        status = e.get('status','')

        ck_id = e.get('ck_id','')
        ck_paydate = e.get('ck_paydate','')
        ck_paytype = e.get('ck_paytype','')
        ck_fkh = e.get('ck_fkh','')
        ck_checkno = e.get('ck_checkno','')

        if str(ck_id) =='0' or str(ck_id) =='':  #新添加行
            pass        
        elif status =='deleted':  #删除行
            pass
        else:
            sql = """update _m540_clfkbf_list set                                 
                                pay_date='%s',
                                pay_class=%s,
                                capital_id=%s,
                                check_no='%s'
                    where id=%s"""%(ck_paydate,ck_paytype,ck_fkh,ck_checkno,ck_id)
            db.executesql(sql) 
 
        n += 1
    return

def saveVerify229(data_list):
    return

def getSaveValue(data_list,fname,is_number):

    value = data_list.get(fname,'')
    #多选框提交的数据是list,需要做下处理
    print value
    value = handleMutilValue(value,is_number)
    if is_number == 1:
        value = value or 'NULL' 
    else:
        value = value or ''   
    return value

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
