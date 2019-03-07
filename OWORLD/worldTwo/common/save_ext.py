# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname'%prj_name) 
import json
import MySQLdb

def saveDataExt(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    sql = """select saveFunc from menu_data_source
             where menu_id='%s'
          """%(menu_id)    
    rows,iN = db.select(sql)
    if iN == 0:
        return
    saveFunc = rows[0][0]
    #print saveFunc
    if saveFunc == 'saveDataFix':  #固定资产登记入库
        saveDataFix(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveDataFixBorrow':  #固定资产借用
        saveDataFixBorrow(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveDataFixAlter':  #责任人变更
        saveDataFixAlter(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveDataFixReturn':  #归还入库
        saveDataFixReturn(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveDataScrap':  #报废申请
        saveDataScrap(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveDataLWTeams':  #劳务团队
        saveDataLWTeams(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveBzqzFunc':  #班组签证
        saveBzqzFunc(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveJfqzFunc':  #甲方签证
        saveJfqzFunc(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'saveClbjFunc': #材料报价审批
        saveClbjFunc(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'addNewMat':
        addNewMat(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'addNewMat407':
        addNewMat407(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'addNewMat405':
        addNewMat405(pk,mode,value_dict,d_value,request)
    elif saveFunc == 'addNewMat426':
        addNewMat426(pk,mode,value_dict,d_value,request)

    return 

def saveDataFix(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    if mode == 'add':  #添加时如果数量大于1，自动添加多条记录
        smll_type = data_list.get("smll_type",'')
        buy_time = data_list.get("buy_time",'')
        zc_count = data_list.get("zc_count") or 0
        sql = "select code from fixedast_sort where id = '%s'"%smll_type
        lT,iN = db.select(sql)
        code =  lT[0][0]
        code += buy_time[2:4]
    
        sql = "select max(sn) from _m1102_gdzc_warehousing where sn like '%s%%'"%(code)
        lT,iN = db.select(sql)
        if lT[0][0] is not None:
            maxnum=int(lT[0][0][len(code):])+1
        else:
            maxnum = 1
        sn = code + str(maxnum).zfill(4)
        sql = "update _m1102_gdzc_warehousing set zc_count=1,sn='%s',status=1 where id=%s"%(sn,pk)
        db.executesql(sql)
        zc_count = int(zc_count)
        print zc_count
        if zc_count >1:
            for num in range(1,zc_count):
                maxnum += 1
                sn = code + str(maxnum).zfill(4)
                sql = """INSERT INTO _m1102_gdzc_warehousing (`status`, `cid`, `cusrname`, `ctime`, `correlate_sgdh`, `sn`
                            , `big_type`, `smll_type`, `name`, `brand`, `type`, `size`, `unit`, `zc_count`, `zc_price`, `buy_time`
                            , `buy_man`, `provider`, `linkman`, `number`, `bxq`, `bxqz`, `cf_place`, `comment`, `sg_gwid`)
                        select `status`, `cid`, `cusrname`, `ctime`, `correlate_sgdh`, '%s'
                            , `big_type`, `smll_type`, `name`, `brand`, `type`, `size`, `unit`, `zc_count`, `zc_price`, `buy_time`
                            , `buy_man`, `provider`, `linkman`, `number`, `bxq`, `bxqz`, `cf_place`, `comment`, `sg_gwid`
                        from _m1102_gdzc_warehousing where id =%s"""%(sn,pk)
                db.executesql(sql)
    else:
        pass
    return

def saveDataFixBorrow(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('borrow_mxb','')
    cid = d_value[0]
    cusrname = d_value[1]
    
    sql = "update _m1102_gdzc_warehousing set status =1,jy_gwid=NULL,jy_usrname=NULL,jy_time=NULL where jy_gwid=%s"%(pk)
    db.executesql(sql)
    for e in lists:
        status = e.get('status','')
        gdzc_id = e.get('gdzc_id','')
        if status !='deleted':  
            sql = """update _m1102_gdzc_warehousing set status = 3,jy_gwid=%s,jy_usrname='%s',jy_time=now() where id=%s
                      """%(pk,cusrname,gdzc_id)
            #print sql
            db.executesql(sql)
    sql = "update _m1103_borrow set dept_id = NULL where gw_id=%s and type = 2;"%(pk)
    sql += "update _m1103_borrow set proj_id = NULL where gw_id=%s and type = 1;"%(pk)
    db.executesql(sql)
    sql = "update _m1103_borrow_list mx,_m1103_borrow bo set mx.dept_id=bo.dept_id,mx.proj_id=bo.proj_id where mx.gw_id=bo.gw_id and mx.gw_id=%s"%(pk)
    db.executesql(sql)
    return

def saveDataFixReturn(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    location = data_list.get('location','')
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]
    
    for e in lists:
        status = e.get('status','')
        gdzc_id = e.get('gdcz_id','')
        br_id = e.get('br_id','')
        if status !='deleted':  
            sql = """update _m1102_gdzc_warehousing set status = 1,jy_gwid=NULL,jy_usrname=NULL,jy_time=NULL,cf_place='%s' where id=%s
                      """%(location,gdzc_id)
            #print sql
            db.executesql(sql)
            sql = """update _m1103_borrow_list set status = 2,return_date=now() where id=%s
                      """%(br_id)
            #print sql
            db.executesql(sql)
        else:
            sql = "select gw_id,cusrname,dj_date from _m1103_borrow_list where id=%s"%(br_id)
            rows,iN = db.select(sql)
            if iN > 0:
                jy_gwid = rows[0][0]
                jy_usrname = rows[0][1]
                jy_time = rows[0][2]
            sql = """update _m1102_gdzc_warehousing set status = 2,jy_gwid=%s,jy_usrname='%s',jy_time='%s' where id=%s
                      """%(jy_gwid,jy_usrname,jy_time,gdzc_id)
            db.executesql(sql)
            sql = """update _m1103_borrow_list set status = 1,return_date=NULL where id=%s
                      """%(br_id)
            db.executesql(sql)
    return

def saveDataFixAlter(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]

    #把原借出人记录改为1
    sql = "update _m1103_borrow_list cur,_m1103_borrow_list pre set pre.status = 1 where cur.pre_mxid = pre.id and cur.gw_id=%s"%(pk)
    db.executesql(sql)
    
    for e in lists:
        gdzc_id = e.get('gdzc_id','')
        is_sel = e.get('is_sel','')
        is_sel = handleMutilValue(is_sel,1)
        if str(is_sel) != '1':
            sql = "delete from _m1103_borrow_list where gw_id=%s and gdzc_id=%s"%(pk,gdzc_id)
            #print sql
            db.executesql(sql)
    sql = "update _m1103_borrow_list mx,_m1104_alteration bo set mx.dept_id=bo.dept_id,mx.proj_id=bo.proj_id where mx.gw_id=bo.gw_id and mx.gw_id=%s"%(pk)
    db.executesql(sql)

    sql = "update _m1104_alteration set dept_id = NULL where gw_id=%s and agency = 2;"%(pk)
    sql += "update _m1104_alteration set proj_id = NULL where gw_id=%s and agency = 1;"%(pk)
    db.executesql(sql)
    #把原借出人记录改为已借出，防止其他人再次调用数据
    sql = "update _m1103_borrow_list cur,_m1103_borrow_list pre set pre.status = 2 where cur.pre_mxid = pre.id and cur.gw_id=%s"%(pk)
    db.executesql(sql)
    return

def saveDataScrap(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]
    
    sql = "update _m1102_gdzc_warehousing set status =2,bf_gwid=NULL,bf_usrname=NULL,bf_time=NULL where bf_gwid=%s"%(pk)
    db.executesql(sql)
    #把原借出人记录改为1
    sql = "update _m1103_borrow_list br,_m1107_scrap_list sc set br.status = 1 where br.id = sc.br_id and sc.gw_id=%s"%(pk)
    db.executesql(sql)


    for e in lists:
        status = e.get('status','')
        gdzc_id = e.get('gdzc_id','')
        br_id = e.get('br_id','')
        is_sel = e.get('is_sel','')
        is_sel = handleMutilValue(is_sel,1)
        if str(is_sel) == '1':
            sql = """update _m1102_gdzc_warehousing set status = 4,bf_gwid=%s,bf_usrname='%s',bf_time=now() where id=%s
                      """%(pk,cusrname,gdzc_id)
            #print sql
            db.executesql(sql)
            sql = "update _m1103_borrow_list set status = 4 where id = %s"%(br_id)
            db.executesql(sql)
        else:
            sql = "delete from _m1107_scrap_list where gw_id=%s and gdzc_id=%s"%(pk,gdzc_id)
            db.executesql(sql)
    sql = "update _m1107_scrap set dept_id = NULL where gw_id=%s and type = 2;"%(pk)
    sql += "update _m1107_scrap set proj_id = NULL where gw_id=%s and type = 1;"%(pk)
    db.executesql(sql)
    return

def saveDataLWTeams(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]
    mode = request.POST.get('mode','')
    step = request.POST.get('step','')
    print "step=%s"%step
    if mode =='add':
        if str(step) == '':
            sql = "insert into addr_book_group (addr_book_id,addr_group_id,cid,cusrname,ctime) values (%s,6,%s,'%s',now())"%(pk,cid,cusrname)
            db.executesql(sql)
            sql = "insert into _m423_laborserviceteam (ab_id,cid,cusrname,ctime) values (%s,%s,'%s',now())"%(pk,cid,cusrname)
            print sql
            db.executesql(sql)
    return

def saveBzqzFunc(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]
    jf_gwid = data_list.get('jfqz_gwid','')
    if jf_gwid == '':
        return
    sql = "select sn from _m421_bzqz where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    if iN == 0:
        return
    sn = rows[0][0]
    sql = "update _m430_changelist set bzqz_gwid = %s,bzqz_sn='%s' where gw_id=%s"%(pk,sn,jf_gwid)
    db.executesql(sql)
    return

def addNewMat(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('lists','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:
        status = e.get('status','')
        cl_id = e.get('cl_id','')
        cl_mat_code =  e.get('cl_mat_code','')
        cl_mat_name =  e.get('cl_mat_name','')
        cl_size =  e.get('cl_size','')
        cl_unit =  e.get('cl_unit','')
        cl_mat_type =  e.get('cl_mat_type','')
        cl_type =  e.get('cl_type','')
        cl_brand =  e.get('cl_brand','')
        if status =='deleted': 
            pass
        else:
            sql = """select cl.id,cl.number,cl.cllb from _m504_clgl cl 
                     left join _m503_clfl fl on cl.cllb = fl.id
                     where cl.name = '%s' and cl.unit = '%s' and cl.size = '%s' and cl.brand = '%s' and cl.type='%s' 
                """%(cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            rows,iN = db.select(sql)
            if iN == 0:
                cl_mat_code = getAutoCode(cl_mat_type)
                sql = """insert into _m504_clgl (cllb,number,name,size,unit,state,cid,cusrname,ctime,brand,type,commer) 
                           values (%s,'%s','%s','%s','%s',1,'%s','%s',now(),'%s','%s','材料采购总计划--系统自动增加')
                    """%(cl_mat_type,cl_mat_code,cl_mat_name,cl_size,cl_unit,cid,cusrname,cl_brand,cl_type)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                cl_mat_id = rows[0][0]
            else:
                cl_mat_id = rows[0][0]
                cl_mat_code = rows[0][1]
                cl_mat_type = rows[0][2]
            sql = """update _m444_clcg_zjh_list set cl_mat_id=%s,cl_mat_code='%s',cl_mat_type='%s'
                  where gw_id=%s and cl_mat_name='%s' and cl_unit='%s' and cl_size='%s' and cl_brand='%s' and cl_type='%s'
            """%(cl_mat_id,cl_mat_code,cl_mat_type,pk,cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            db.executesql(sql)
    return

def addNewMat407(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('cg_list','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:
        status = e.get('status','')
        cl_id = e.get('cl_id','')
        cl_mat_code =  e.get('cl_mat_code','')
        cl_mat_name =  e.get('cl_mat_name','')
        cl_size =  e.get('cl_size','')
        cl_unit =  e.get('cl_unit','')
        cl_mat_type =  e.get('cl_mat_type','')
        cl_type =  e.get('cl_type','')
        cl_brand =  e.get('cl_brand','')
        if status =='deleted': 
            pass
        else:
            sql = """select cl.id,cl.number,cl.cllb from _m504_clgl cl 
                     left join _m503_clfl fl on cl.cllb = fl.id
                     where cl.name = '%s' and cl.unit = '%s' and cl.size = '%s' and cl.brand = '%s' and cl.type='%s' 
                """%(cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            rows,iN = db.select(sql)
            if iN == 0:
                cl_mat_code = getAutoCode(cl_mat_type)
                sql = """insert into _m504_clgl (cllb,number,name,size,unit,state,cid,cusrname,ctime,brand,type,commer) 
                           values (%s,'%s','%s','%s','%s',1,'%s','%s',now(),'%s','%s','材料采购--系统自动增加')
                    """%(cl_mat_type,cl_mat_code,cl_mat_name,cl_size,cl_unit,cid,cusrname,cl_brand,cl_type)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                cl_mat_id = rows[0][0]
            else:
                cl_mat_id = rows[0][0]
                cl_mat_code = rows[0][1]
                cl_mat_type = rows[0][2]
            sql = """update _m407_clcg_list set mat_id=%s,cl_mat_code='%s',cl_mat_type='%s'
                  where gw_id=%s and cl_mat_name='%s' and mat_unit='%s' and mat_size='%s' and brand='%s' and mat_type='%s'
            """%(cl_mat_id,cl_mat_code,cl_mat_type,pk,cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            db.executesql(sql)
    return

def addNewMat405(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('borrow_list','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:
        status = e.get('status','')
        cl_id = e.get('cl_id','')
        cl_mat_code =  e.get('cl_mat_code','')
        cl_mat_name =  e.get('cl_mat_name','')
        cl_size =  e.get('cl_size','')
        cl_unit =  e.get('cl_unit','')
        cl_mat_type =  e.get('cl_mat_type','')
        cl_type =  e.get('cl_type','')
        cl_brand =  e.get('cl_brand','')
        if status =='deleted': 
            pass
        else:
            sql = """select cl.id,cl.number,cl.cllb from _m504_clgl cl 
                     left join _m503_clfl fl on cl.cllb = fl.id
                     where cl.name = '%s' and cl.unit = '%s' and cl.size = '%s' and cl.brand = '%s' and cl.type='%s' 
                """%(cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            rows,iN = db.select(sql)
            if iN == 0:
                cl_mat_code = getAutoCode(cl_mat_type)
                sql = """insert into _m504_clgl (cllb,number,name,size,unit,state,cid,cusrname,ctime,brand,type,commer) 
                           values (%s,'%s','%s','%s','%s',1,'%s','%s',now(),'%s','%s','材料计划上报--系统自动增加')
                    """%(cl_mat_type,cl_mat_code,cl_mat_name,cl_size,cl_unit,cid,cusrname,cl_brand,cl_type)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                cl_mat_id = rows[0][0]
            else:
                cl_mat_id = rows[0][0]
                cl_mat_code = rows[0][1]
                cl_mat_type = rows[0][2]
            sql = """update _m405_cljh_list set cl_mat_id=%s,cl_mat_code='%s',cl_mat_type='%s'
                  where gw_id=%s and cl_mat_name='%s' and cl_unit='%s' and cl_size='%s' and cl_brand='%s' and cl_type='%s'
            """%(cl_mat_id,cl_mat_code,cl_mat_type,pk,cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            db.executesql(sql)
    return

def addNewMat426(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('cght_list','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:
        status = e.get('status','')
        cl_id = e.get('cl_id','')
        cl_mat_code =  e.get('cl_mat_code','')
        cl_mat_name =  e.get('cl_mat_name','')
        cl_size =  e.get('cl_size','')
        cl_unit =  e.get('cl_unit','')
        cl_mat_type =  e.get('cl_mat_type','')
        cl_type =  e.get('cl_type','')
        cl_brand =  e.get('cl_brand','')
        if status =='deleted': 
            pass
        else:
            sql = """select cl.id,cl.number,cl.cllb from _m504_clgl cl 
                     left join _m503_clfl fl on cl.cllb = fl.id
                     where cl.name = '%s' and cl.unit = '%s' and cl.size = '%s' and cl.brand = '%s' and cl.type='%s' 
                """%(cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            rows,iN = db.select(sql)
            if iN == 0:
                cl_mat_code = getAutoCode(cl_mat_type)
                sql = """insert into _m504_clgl (cllb,number,name,size,unit,state,cid,cusrname,ctime,brand,type,commer) 
                           values (%s,'%s','%s','%s','%s',1,'%s','%s',now(),'%s','%s','材料采购合同--系统自动增加')
                    """%(cl_mat_type,cl_mat_code,cl_mat_name,cl_size,cl_unit,cid,cusrname,cl_brand,cl_type)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                cl_mat_id = rows[0][0]
            else:
                cl_mat_id = rows[0][0]
                cl_mat_code = rows[0][1]
                cl_mat_type = rows[0][2]
            sql = """update _m426_cght_list set mat_id=%s,cl_mat_code='%s',cl_mat_type='%s'
                  where gw_id=%s and cl_mat_name='%s' and mat_unit='%s' and mat_size='%s' and brand='%s' and mat_type='%s'
            """%(cl_mat_id,cl_mat_code,cl_mat_type,pk,cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            db.executesql(sql)
    return

def saveData41103(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sql = "update _m41103_collar_list mx,_m41103_material_collar ll set mx.proj_id=ll.proj_id where ll.id=mx.m_id and ll.id = %s"""%pk
    db.executesql(sql)

    sql = """select mx.id,mx.mat_id,mx.lc_number,mx.vwap,mx.money,ll.proj_id from _m41103_collar_list mx
            left join _m41103_material_collar ll on ll.id = mx.m_id
            where ll.id = %s"""%pk
    lT,iN = db.select(sql)
    for e in lT:
        mx_id = e[0]
        mat_id = e[1]
        qty = e[2]
        price = e[3]
        amount = e[4]
        proj_id = e[5]
    
        sql = "select qty from mat_stock_log where type=2 and mx_id = %s order by id desc"%(mx_id)
        lT1,iN1 = db.select(sql)
        if iN1 == 0: #新增
            sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (2,'领料出库',-1,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,'%s',now())
                """%(pk,mx_id,proj_id,mat_id,qty,qty,price,amount,usr_id,usr_name)
            print ToGBK(sql)
            db.executesql(sql)
            sql = "update mat_stock set qty = qty-%s,amount = amount-%s where mat_id = %s and proj_id= %s"%(qty,amount,mat_id,proj_id)
            print ToGBK(sql)
            db.executesql(sql)
    
        else: #修改
            old_qty = lT1[0][0]
            if old_qty < qty: 
                sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (2,'领料出库-修改变更',-1,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,'%s',now())
                    """%(pk,mx_id,proj_id,mat_id,(qty-old_qty),(qty-old_qty),price,float(qty-old_qty)*float(price),usr_id,usr_name)
                print ToGBK(sql)
                db.executesql(sql)    
            elif old_qty > qty:
                sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (2,'领料出库-修改变更',1,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,'%s',now())
                    """%(pk,mx_id,proj_id,mat_id,(old_qty-qty),(old_qty-qty),price,float(old_qty-qty)*float(price),usr_id,usr_name)

                print ToGBK(sql)
                db.executesql(sql)    
            sql = "update mat_stock set qty = qty-%s,amount = amount-%s where mat_id = %s and proj_id= %s"%((qty-old_qty),float(qty-old_qty)*float(price),mat_id,proj_id)
            db.executesql(sql)

    return

def getAutoCode(cllb):
    code =''
    if cllb == '' or str(cllb) == '-1':
        return code
    else:
        sql = "select ifnull(code,''),ifnull(level,1) from _m503_CLFL where id=%s"%cllb
        lT,iN = db.select(sql)
        if iN>0:
            code = lT[0][0]
            code += "-" 
            sql = "select max(number) from _m504_CLGL  where number like '%s%%'"%(code)
            lT,iN = db.select(sql)
            if lT[0][0] is not None:
                maxnum=str(int(lT[0][0][len(code):])+1)
            else:
                maxnum = '1'
            maxnum = maxnum.zfill(3)
            code += maxnum

    return code

def saveJfqzFunc(pk,mode,value_dict,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]
    bz_gwid = data_list.get('bzqz_gwid','')
    if bz_gwid =='':
	    return
    sql = "select sn from _m430_changelist where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    if iN == 0:
        return
    sn = rows[0][0]
    sql = "update _m421_bzqz set jfqz_gwid = %s,jfqz_sn='%s' where gw_id=%s"%(pk,sn,bz_gwid)
    db.executesql(sql)
    return

def saveVerifyExt(pk,mode,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    sql = """select verifyFunc from menu_data_source
             where menu_id='%s'
          """%(menu_id)    
    rows,iN = db.select(sql)
    if iN == 0:
        return
    saveFunc = rows[0][0]
    if saveFunc == 'saveVerifyFixBorrow':  #固定资产借用
        saveVerifyFixBorrow(pk,mode,d_value,request)
    elif saveFunc == 'saveVerifyScrap':  #报废申请
        saveVerifyScrap(pk,mode,d_value,request)
    elif saveFunc == 'saveVerifyTH':  #退货管理
        saveVerifyTH(pk,mode,d_value,request)
    elif saveFunc == 'saveVerifyTL':  #退料管理
        saveVerifyTL(pk,mode,d_value,request)
    elif saveFunc=='saveData41103':       #材料领出
        saveData41103(pk,mode,d_value,request)
    elif saveFunc == 'saveVerifyPD':  #材料盘点
        saveVerifyPD(pk,mode,d_value,request)

    return 

def saveVerifyFixBorrow(pk,mode,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    dj_status = data_list.get('dj_status','')
    if str(dj_status) == '1':
        sql = "update _m1102_gdzc_warehousing set status =2 where jy_gwid=%s"%(pk)
        db.executesql(sql)
        sql = "update _m1103_borrow_list set status = 1,dj_date=now() where gw_id=%s"%(pk)
        db.executesql(sql)
    else:
        sql = "update _m1102_gdzc_warehousing set status =1,jy_gwid=NULL,jy_usrname=NULL,jy_time=NULL where jy_gwid=%s"%(pk)
        db.executesql(sql)
        sql = "update _m1103_borrow_list set status = 0 where gw_id=%s"%(pk)
        db.executesql(sql)

    return

def saveVerifyScrap(pk,mode,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    sql = "update _m1102_gdzc_warehousing set status =5,jy_usrname=NULL,jy_time=NULL,bf_time=now() where bf_gwid=%s"%(pk)
    db.executesql(sql)
    sql = "update _m1103_borrow_list br,_m1107_scrap_list sc set br.status = 2 where br.id = sc.br_id and sc.gw_id=%s"%(pk)
    db.executesql(sql)
    return

def saveVerifyTH(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sql = "update _m41105_r_goods_list mx,_m41105_return_goods th set mx.proj_id=th.proj_id where th.id=mx.m_id and th.id = %s"""%pk
    db.executesql(sql)

    sql = """select mx.id,mx.mat_id,mx.th_number,mx.th_price,mx.money,th.proj_id from _m41105_r_goods_list mx
            left join _m41105_return_goods th on th.id = mx.m_id
            where th.id = %s"""%pk
    lT,iN = db.select(sql)
    for e in lT:
        mx_id = e[0]
        mat_id = e[1]
        qty = e[2]
        price = e[3]
        amount = e[4]
        proj_id = e[5]
    
        sql = "select qty from mat_stock_log where type=4 and mx_id = %s order by id desc"%(mx_id)
        lT1,iN1 = db.select(sql)
        if iN1 == 0: #新增
            sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (4,'退货',-1,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,'%s',now())
                """%(pk,mx_id,proj_id,mat_id,qty,qty,price,amount,usr_id,usr_name)
            db.executesql(sql)
            sql = "update mat_stock set qty = qty-%s,amount = amount-%s where mat_id = %s and proj_id= %s"%(qty,amount,mat_id,proj_id)
            print sql
            db.executesql(sql)
    
    return

def saveVerifyTL(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sql = "update _m41104_mat_rej_list mx,_m41104_mat_rejected tl set mx.proj_id=tl.proj_id where tl.id=mx.m_id and tl.id = %s"""%pk
    db.executesql(sql)

    sql = """select mx.id,mx.mat_id,mx.tl_number,mx.vwap,mx.money,tl.proj_id from _m41104_mat_rej_list mx
            left join _m41104_mat_rejected tl on tl.id = mx.m_id
            where tl.id = %s"""%pk
    lT,iN = db.select(sql)
    for e in lT:
        mx_id = e[0]
        mat_id = e[1]
        qty = e[2]
        price = e[3]
        amount = e[4]
        proj_id = e[5]
    
        sql = "select qty from mat_stock_log where type=3 and mx_id = %s order by id desc"%(mx_id)
        lT1,iN1 = db.select(sql)
        if iN1 == 0: #新增
            sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (3,'退料入库',1,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,'%s',now())
                """%(pk,mx_id,proj_id,mat_id,qty,qty,price,amount,usr_id,usr_name)
            db.executesql(sql)
            sql = "update mat_stock set qty = qty+%s,amount = amount+%s where mat_id = %s and proj_id= %s"%(qty,amount,mat_id,proj_id)
            db.executesql(sql)

    return

def saveData41103(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sql = "update _m41103_collar_list mx,_m41103_material_collar ll set mx.proj_id=ll.proj_id where ll.id=mx.m_id and ll.id = %s"""%pk
    db.executesql(sql)

    sql = """select mx.id,mx.mat_id,mx.lc_number,mx.vwap,mx.money,ll.proj_id from _m41103_collar_list mx
            left join _m41103_material_collar ll on ll.id = mx.m_id
            where ll.id = %s"""%pk
    lT,iN = db.select(sql)
    for e in lT:
        mx_id = e[0]
        mat_id = e[1]
        qty = e[2]
        price = e[3]
        amount = e[4]
        proj_id = e[5]
    
        sql = "select qty from mat_stock_log where type=2 and mx_id = %s order by id desc"%(mx_id)
        lT1,iN1 = db.select(sql)
        if iN1 == 0: #新增
            sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (2,'领料出库',-1,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,'%s',now())
                """%(pk,mx_id,proj_id,mat_id,qty,qty,price,amount,usr_id,usr_name)
            db.executesql(sql)
            sql = "update mat_stock set qty = qty-%s,amount = amount-%s where mat_id = %s and proj_id= %s"%(qty,amount,mat_id,proj_id)
            db.executesql(sql)
    
        else: #修改
            old_qty = lT1[0][0]
            if old_qty < qty: 
                sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (2,'领料出库-修改变更',-1,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,'%s',now())
                    """%(pk,mx_id,proj_id,mat_id,(qty-old_qty),(qty-old_qty),price,float(qty-old_qty)*float(price),usr_id,usr_name)
                db.executesql(sql)    
            elif old_qty > qty:
                sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                     values (2,'领料出库-修改变更',1,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,'%s',now())
                    """%(pk,mx_id,proj_id,mat_id,(old_qty-qty),(old_qty-qty),price,float(old_qty-qty)*float(price),usr_id,usr_name)
                db.executesql(sql)    
            sql = "update mat_stock set qty = qty-%s,amount = amount-%s where mat_id = %s and proj_id= %s"%((qty-old_qty),float(qty-old_qty)*float(price),mat_id,proj_id)
            db.executesql(sql)

    return

def saveVerifyPD(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sql = "update _m41106_take_list mx,_m41106_take_stock pd set mx.proj_id=pd.proj_id where pd.id=mx.m_id and pd.id = %s"""%pk
    db.executesql(sql)

    sql = """select mx.id,mx.mat_id,mx.pd_gross,mx.price,mx.total_price,pd.proj_id,mx.mat_gross from _m41106_take_list mx
            left join _m41106_take_stock pd on pd.id = mx.m_id
            where pd.id = %s"""%pk
    lT,iN = db.select(sql)
    for e in lT:
        mx_id = e[0]
        mat_id = e[1]
        qty = e[2]
        price = e[3]
        amount = e[4]
        proj_id = e[5]
        old_qty = e[6]         
        sql = "select qty from mat_stock_log where type=5 and mx_id = %s order by id desc"%(mx_id)
        lT1,iN1 = db.select(sql)
        if iN1 == 0: #新增
            if qty>old_qty:    #盘盈
                sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                         values (5,'盘盈',1,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,'%s',now())
                    """%(pk,mx_id,proj_id,mat_id,qty-old_qty,qty-old_qty,price,(qty-old_qty)*price,usr_id,usr_name)
            elif qty<old_qty:    #盘亏
                sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
                         values (5,'盘亏',-1,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,'%s',now())
                    """%(pk,mx_id,proj_id,mat_id,old_qty-qty,old_qty-qty,price,(old_qty-qty)*price,usr_id,usr_name)
            db.executesql(sql)
            sql = "update mat_stock set qty = %s,amount = %s where mat_id = %s and proj_id= %s"%(qty,amount,mat_id,proj_id)
            db.executesql(sql)
    
    return

def actionExt(pk,d_value,request,func):
    if func == 'actionFixPass':  #责任人变更
        actionFixPass(pk,d_value,request)
    elif func == 'actionFixNoPass':  #责任人变更
        actionFixNoPass(pk,d_value,request)
    elif func == 'gw_return':  #强制退回
        gw_return(pk,d_value,request)
    return

def gw_return(pk,d_value,request):
    sql = """select gd.type_id,gd.cid,gd.cusrname,gd.menu_id,m.first_flow,m.form_table
             from gw_doc gd
             left join menu_data_source m on m.menu_id = gd.menu_id
             where gd.id = %s"""%(pk)
    print sql
    rows,iN = db.select(sql)

    type_id = rows[0][0]
    cid = rows[0][1]
    cusrname = rows[0][2]
    menu_id = rows[0][3]
    first_flow = rows[0][4]
    form_table = rows[0][5]

    sql="""UPDATE gw_doc SET
            status = 5, cur_flow_status = 0, finish = 0 , is_disable = 0 , status_txt = '强制退回',
            cur_flow_time = now(), cur_user_name='%s',
            cur_flow_id = %s, cur_flow_usr_id = %s,cur_flow_name = '发起人（强制退回）',
            next_flow_id = null,next_flow_usr_id = null 
            WHERE id = %s
            """%(cusrname,first_flow,cid,pk)
    db.executesql(sql)

    sql="""INSERT INTO gw_flow_his(m_id,send_usr_id,flow_id,send_flow_id,send_pre_flow_id,status,cid,ctime,cusrname,flow_name) 
                VALUES(%s,%s,%s,%s,%s,0,%s,now(),'%s','发起人（强制退回）')
                """%(pk,cid,first_flow,first_flow,-1,cid,cusrname)
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

    sql = "update %s set gw_status=0 where gw_id=%s"%(form_table,pk)
    db.executesql(sql)           
    return

def actionFixNoPass(pk,d_value,request):
    cid = d_value[0]
    cusrname = d_value[1]
    dj_status = 0
    sql = "select cid,cur_usrid,ifnull(jr_sign,0),ifnull(jc_sign,0) from _m1104_alteration where gw_id=%s"%pk
    rows,iN = db.select(sql)
    if iN > 0:
        jrr = rows[0][0]
        jcr = rows[0][1]
        jr_sign = rows[0][2]
        jc_sign = rows[0][3]
        if jrr == cid:   #借入人
            if jc_sign == 1: #借出人同意，办结
                sql = "update _m1104_alteration set jr_sign=2,dj_status =2 where gw_id=%s"%pk
                dj_status = 2
            elif jc_sign == 2: #借出人不同意，办结
                sql = "update _m1104_alteration set jr_sign=2,dj_status =2 where gw_id=%s"%pk
                dj_status = 2
            else: #借出人未发表意见，未办结
                sql = "update _m1104_alteration set jr_sign=2,dj_status =0 where gw_id=%s"%pk
            db.executesql(sql)
        elif jcr == cid:   #借出人
            if jc_sign == 1: #借入人同意，办结
                sql = "update _m1104_alteration set jc_sign=2,dj_status =2 where gw_id=%s"%pk
                dj_status = 2
            elif jc_sign == 2: #借入人不同意，办结
                sql = "update _m1104_alteration set jc_sign=2,dj_status =2 where gw_id=%s"%pk
                dj_status = 2
            else: #借入人未发表意见，未办结
                sql = "update _m1104_alteration set jc_sign=2,dj_status =0 where gw_id=%s"%pk
            db.executesql(sql)
    if dj_status == 2:
        sql = "update _m1103_borrow_list cur,_m1103_borrow_list pre set pre.status =1 where cur.pre_mxid = pre.id and cur.gw_id=%s"%(pk)
        db.executesql(sql)
        sql = "update _m1103_borrow_list set status =0 where gw_id=%s"%(pk)
        db.executesql(sql)
    return

def actionFixPass(pk,d_value,request):
    cid = d_value[0]
    cusrname = d_value[1]
    dj_status = 0
    sql = "select cid,cur_usrid,ifnull(jr_sign,0),ifnull(jc_sign,0) from _m1104_alteration where gw_id=%s"%pk
    rows,iN = db.select(sql)
    if iN > 0:
        jrr = rows[0][0]
        jcr = rows[0][1]
        jr_sign = rows[0][2]
        jc_sign = rows[0][3]
        if jrr == cid:   #借入人
            if jc_sign == 1: #借出人同意，办结
                sql = "update _m1104_alteration set jr_sign=1,dj_status =1,dj_date=now() where gw_id=%s;"%pk
                dj_status = 1
            elif jc_sign == 2: #借出人不同意，办结
                sql = "update _m1104_alteration set jr_sign=1,dj_status =2 where gw_id=%s"%pk
                dj_status = 2
            else: #借出人未发表意见，未办结
                sql = "update _m1104_alteration set jr_sign=1,dj_status =0 where gw_id=%s"%pk
            db.executesql(sql)
        elif jcr == cid:   #借出人
            if jc_sign == 1: #借入人同意，办结
                sql = "update _m1104_alteration set jc_sign=1,dj_status =1,dj_date=now() where gw_id=%s"%pk
                dj_status = 1
            elif jc_sign == 2: #借入人不同意，办结
                sql = "update _m1104_alteration set jc_sign=1,dj_status =2 where gw_id=%s"%pk
                dj_status = 2
            else: #借入人未发表意见，未办结
                sql = "update _m1104_alteration set jc_sign=1,dj_status =0 where gw_id=%s"%pk
            db.executesql(sql)
    if dj_status == 1:
        sql = """update _m1102_gdzc_warehousing zc,_m1103_borrow_list mx 
                     set zc.jy_gwid = mx.gw_id,zc.jy_usrname=mx.cusrname,zc.jy_time=now()
                  where mx.gdzc_id = zc.id and mx.gw_id =%s """%(pk)
        #print sql
        db.executesql(sql)
        sql = "update _m1103_borrow_list cur,_m1103_borrow_list pre set pre.status =2 where cur.pre_mxid = pre.id and cur.gw_id=%s"%(pk)
        db.executesql(sql)
        sql = "update _m1103_borrow_list set status =1,dj_date=now() where gw_id=%s"%(pk)
        print sql
        db.executesql(sql)
    elif dj_status == 2:
        sql = "update _m1103_borrow_list cur,_m1103_borrow_list pre set pre.status =1 where cur.pre_mxid = pre.id and cur.gw_id=%s"%(pk)
        db.executesql(sql)
        sql = "update _m1103_borrow_list set status =0 where gw_id=%s"%(pk)
        db.executesql(sql)
    return

#材料报价审批
def saveClbjFunc(pk,mode,value_dict,d_value,request):
    step = request.POST.get('step','')
    if str(step) != '2':
        return

    sql = """select s.cname,l.gys_id from _m406_clbj_gys l
               left join suppliers s on l.gys_id = s.id
               where l.gw_id = '%s' order by l.sort"""%(pk)
    rows,iN = db.select(sql)

    data = request.POST.get('data','')
    data_list = json.loads(data)

    lists = data_list.get('bj_list','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:
        status = e.get('status','')
        clbj_id = e.get('clbj_id','')
        clbj_count = e.get('clbj_count','')
        clbj_craft = e.get('clbj_craft','')       
        clbj_memo = e.get('clbj_memo','')
        clbj_memo = MySQLdb.escape_string(clbj_memo)
        cl_mat_code =  e.get('cl_mat_code','')
        cl_mat_name =  e.get('cl_mat_name','')
        cl_size =  e.get('cl_size','')
        cl_unit =  e.get('cl_unit','')
        cl_mat_type =  e.get('cl_mat_type','')
        cl_type =  e.get('cl_type','')
        cl_brand =  e.get('cl_brand','')
        if status =='deleted': 
            pass
        else:
            sql = """select cl.id,cl.number,cl.cllb from _m504_clgl cl 
                     left join _m503_clfl fl on cl.cllb = fl.id
                     where cl.name = '%s' and cl.unit = '%s' and cl.size = '%s' and cl.brand = '%s' and cl.type='%s' 
                """%(cl_mat_name,cl_unit,cl_size,cl_brand,cl_type)
            rows2,iN2 = db.select(sql)
            if iN2 == 0:
                cl_mat_code = getAutoCode(cl_mat_type)
                sql = """insert into _m504_clgl (cllb,number,name,size,unit,state,cid,cusrname,ctime,brand,type,commer) 
                           values (%s,'%s','%s','%s','%s',1,'%s','%s',now(),'%s','%s','材料报价审批--系统自动增加')
                    """%(cl_mat_type,cl_mat_code,cl_mat_name,cl_size,cl_unit,cid,cusrname,cl_brand,cl_type)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows2,iN2 = db.select(sql)
                cl_mat_id = rows2[0][0]
            else:
                cl_mat_id = rows2[0][0]
                cl_mat_code = rows2[0][1]
                cl_mat_type = rows2[0][2]

        if status =='deleted':
            sql = "delete from _m406_clbj_list where id='%s'"%(clbj_id)
            db.executesql(sql)
        elif clbj_id != '':
            sql = """update _m406_clbj_list set cl_mat_code='%s',cl_mat_type=%s,cl_mat_name='%s',memo='%s',mat_id=%s,cl_size='%s',cl_type='%s',cl_unit='%s',brand='%s',cl_count=%s,craft='%s',uid=%s,utime=now() 
                     where id = %s"""%(cl_mat_code,cl_mat_type,cl_mat_name,clbj_memo,cl_mat_id,cl_size,cl_type,cl_unit,cl_brand,clbj_count,clbj_craft,cid,clbj_id)
            db.executesql(sql)
            sql = "delete from _m406_clbj_gysbj where m_id = %s"%(clbj_id)
            db.executesql(sql)
            n = 0
            for e1 in rows:
                gys_id = e1[1]
                price = e.get('clbj_price_%s'%n) or 'NULL'
                cost = e.get('clbj_cost_%s'%n) or 'NULL'
                sql = "insert into _m406_clbj_gysbj (gw_id,m_id,gys_id,price,cost) values (%s,%s,%s,%s,%s)"%(pk,clbj_id,gys_id,price,cost)
                db.executesql(sql)
                n += 1              
        else:
            sql = """insert into _m406_clbj_list 
                      (gw_id,cl_mat_code,cl_mat_type,cl_mat_name,memo,mat_id,cl_size,cl_type,cl_unit,brand,cl_count,craft,cid,ctime)
                      values (%s,'%s','%s','%s','%s',%s,'%s','%s','%s','%s',%s,'%s',%s,now())
                      """%(pk,cl_mat_code,cl_mat_type,cl_mat_name,clbj_memo,cl_mat_id,cl_size,cl_type,cl_unit,cl_brand,clbj_count,clbj_craft,cid)
            #print sql
            db.executesql(sql)
            sql = "select last_insert_id();"
            rows1,iN1 = db.select(sql)
            clbj_id = rows1[0][0]
            n = 0
            for e1 in rows:
                gys_id = e1[1]
                price = e.get('clbj_price_%s'%n) or 'NULL'
                cost = e.get('clbj_cost_%s'%n) or 'NULL'
                sql = "insert into _m406_clbj_gysbj (gw_id,m_id,gys_id,price,cost) values (%s,%s,%s,%s,%s)"%(pk,clbj_id,gys_id,price,cost)
                db.executesql(sql)
                n += 1              
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