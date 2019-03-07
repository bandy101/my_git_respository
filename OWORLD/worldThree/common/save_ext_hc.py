# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname'%prj_name) 
import json
import MySQLdb

def saveDataExt(pk,mode,value_dict,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    if str(menu_id)=='611':
        saveData611(pk,mode,d_value,request)
    if str(menu_id)=='605':
        saveData605(pk,mode,d_value,request)
    elif str(menu_id)=='61402':
        saveData61402(pk,mode,d_value,request)
    elif str(menu_id)=='61403':
        saveData61403(pk,mode,d_value,request)
    elif str(menu_id)=='615':
        saveData615(pk,mode,d_value,request)
    
    return 
def saveData605(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sql = """update _m605_huangliaocaigou cg,(select gw_id,count(1) as qty from _m605_hlcgmx_list group by gw_id) mx 
           set cg.total_qty = mx.qty 
           where cg.gw_id = mx.gw_id and cg.gw_id=%s"""%pk
    #print ToGBK(sql)
    db.executesql(sql)

    return

def saveData611(pk,mode,d_value,request):
    #print request.POST
    usr_id = d_value[0]
    usr_name = d_value[1]
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    hl_id = data_list.get('hl_id','')
    sql = "update _m6031_stone_stock set status=2,md_gwid=%s,md_usrid=%s,md_usrname='%s',md_time=now() where id = %s"%(pk,usr_id,usr_name,hl_id)
    db.executesql(sql)
    bundle_list =  data_list.get('bundle_code','')
    if len(bundle_list) <=0:
        return

    sql = "delete from _m611_packing_list where gw_id = '%s'"%(pk)
    db.executesql(sql)
    for e in  bundle_list:
        bundle_code = e 
        slices = data_list.get(bundle_code,'')
        for e1 in slices:
            status = e1.get('status','') 
            slice_code = e1.get('slice_code','') 
            length = e1.get('length','') 
            width = e1.get('width','') 
            thick = e1.get('thick','') 
            square = e1.get('square','') 
            realSquare = e1.get('realSquare','') 
            picUpload = e1.get('picUpload','') 
            corner1_length = e1.get('corner1_length') or 'NULL'
            corner1_width = e1.get('corner1_width') or 'NULL'
            corner2_length = e1.get('corner2_length') or 'NULL'
            corner2_width = e1.get('corner2_width') or 'NULL'
            corner3_length = e1.get('corner3_length') or 'NULL'
            corner3_width = e1.get('corner3_width') or 'NULL'
            corner4_length = e1.get('corner4_length') or 'NULL'
            corner4_width = e1.get('corner4_width') or 'NULL'
            cornerSquare = e1.get('cornerSquare') or 'NULL'
            if status == 'deleted':
                continue
            else:
                sql = "select max(slice_code) from _m611_packing_list where bundle_code = '%s'"%(bundle_code)
                lT,iN = db.select(sql)
                if lT[0][0] is not None:
                    maxnum=str(int(lT[0][0][-2:])+1)
                else:
                    maxnum = '1'
                maxnum = maxnum.zfill(2)
                slice_code = bundle_code + maxnum
                sql = """INSERT INTO `_m611_packing_list` (`gw_id`, `status`, `cid`, `cusrname`, `ctime`,`bundle_code`, `slice_code`, `s_long`, `s_wide`, `s_thick`, `square`, `square_real`, `pic`
                             ,corner1_length,corner1_width,corner2_length,corner2_width
                             ,corner3_length,corner3_width,corner4_length,corner4_width,cornerSquare) 
                             VALUES (%s, 1, %s, '%s', now(), '%s', '%s', %s, %s, %s, %s, %s, '%s'
                             ,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                      """%(pk,usr_id,usr_name,bundle_code,slice_code,length,width,thick,square,realSquare,picUpload
                             ,corner1_length,corner1_width,corner2_length,corner2_width
                             ,corner3_length,corner3_width,corner4_length,corner4_width,cornerSquare) 
                #print ToGBK(sql)
                db.executesql(sql)

    return

def saveData61402(pk,mode,d_value,request):
    print request.POST
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    sale_gwid =  data_list.get('Sales_sn', '')
    usr_id = d_value[0]
    usr_name = d_value[1]
    sql = "update _m615_sales_order set gw_status = 2 where gw_id='%s'"%(sale_gwid)
    db.executesql(sql)
    sql = """update _m6144_plank_stock set status=1,ck_usrid=%s,ck_usrname='%s',ck_time=now()
            where sale_gwid = %s"""%(usr_id,usr_name,sale_gwid)
    #print sql
    db.executesql(sql)

def saveData61403(pk,mode,d_value,request):
 
    sql = """INSERT INTO _m6144_plank_stock  ( `status`, `cid`, `cusrname`, `ctime`
                , `md_gwid`, rk_id, `hl_number`, `bundle_code`, `plank_sn`, `sc_long`, `wide`, `thick`, `square`, `square_real`
                , `pricing`, `bc_picture`, `stone_id`, `stone_name`, `hl_id`, `scsx_name`, `sccd`
                , `rk_usrid`, `rk_usrname`, `rk_time`, `stock_id`, `stock_name`, `material`) 
            select 0,rk.cid, rk.cusrname,now() 
                 , rk.md_gwid, rk.id, rk.hlbh , rl.bundle_code , rl.plank_sn , rl.sc_long , rl.wide, rl.thick , pl.square , pl.square_real
                 , NULL , pl.pic , ss.stone_id, ss.stone_name, ss.id, ss.scsx_name, ss.sccd
                 , rk.consignee, u.usr_name, rk.Date_of_receipt, rk.storehouse, m.txt1, sv.material 
            from _m61403_dbrk_list rl 
            left join _m61403_dabanruku rk on rk.id = rl.m_id
            left join _m611_packing_list pl on pl.slice_code = rl.plank_sn
            left join _m6031_stone_stock ss on ss.hl_number = rk.hlbh
            left join users u on u.usr_id = rk.consignee
            left join mtc_t m on m.id = rk.storehouse and m.type = 'CKMC'
            left join _m616_stone_varieties sv on sv.id = ss.stone_id
            where rk.id = %s"""%(pk)
    db.executesql(sql)

    return

def saveData615(pk,mode,d_value,request):
    usr_id = d_value[0]
    usr_name = d_value[1]

    data =  request.POST.get('data','')
    data_list = json.loads(data)
    dd_list = data_list.get('dd_list','')
    for e in dd_list:
        status = e.get('status','')
        selected = e.get('selected','')
        hl_number =  e.get('hl_number','')
        if status =='deleted': 
            sql = "update _m6144_plank_stock set is_sale=0,sale_gwid=NULL where sale_gwid=%s and hl_number='%s'"%(pk,hl_number)
            db.executesql(sql)
        else:
            if len(selected) >0:
                sql = "update _m6144_plank_stock set is_sale=0,sale_gwid=NULL where sale_gwid=%s and hl_number='%s'"%(pk,hl_number)
                db.executesql(sql)
            for e1 in selected:
                panelArray = e1.get('panelArray','')
                for e2 in panelArray:
                    panel_no = e2.get('panel_no','')
                    price = e2.get('price','')
                    sql = "update _m6144_plank_stock set is_sale=1,sale_gwid=%s,sale_price=%s,sales='%s',sale_time=now() where plank_sn='%s'"%(pk,price,usr_name,panel_no)
                    db.executesql(sql)
    return

def saveVerifyExt(pk,mode,d_value,request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    if str(menu_id)=='608':
        saveVerify608(pk,mode,d_value,request)
    elif str(menu_id)=='610':
        saveVerify610(pk,mode,d_value,request)
    elif str(menu_id)=='618':
        saveVerify618(pk,mode,d_value,request)
    elif str(menu_id)=='61401':
        saveVerify61401(pk,mode,d_value,request)
    elif str(menu_id)=='6033':
        saveVerify6033(pk,mode,d_value,request)

    return 

def saveVerify608(pk,mode,d_value,request):
    usr_id = d_value[0]
    usr_name = d_value[1]

    sql = "delete from _m6031_stone_stock where rk_gwid=%s"%(pk)
    db.executesql(sql)

    sql = """INSERT INTO `_m6031_stone_stock` ( `hl_gwid`, `yf_gwid`, `rk_gwid`, `hl_sn`, `yf_sn`, `rk_sn`, `hl_mxid`, `yf_mxid`, `rk_mxid`
                   , `hl_number`, `stone_id`, `stone_name`, `scsx_id`, `scsx_name`, `sccd`, `hl_long`, `wide`, `thick`, `volume`, `weight`
                   , `hl_money`, `hl_picture`, `yf_money`, `remark`, `cid`, `cusrname`, `ctime`,stock_id,stock_name) 
            select rk.cg_gwid,rk.yf_gwid,rk.gw_id,cg.sn,yf.sn,rk.sn,mx.cg_mxid,mx.yf_mxid,mx.id
                  ,mx.hl_number,cgmx.stonename,p.Stone_varieties,m.id,mx.scsx,mx.sccd
                  ,mx.in_length,mx.in_width,mx.in_height,mx.in_volume,mx.in_weight
                  ,cgmx.hl_money,cgmx.hl_picture,yf.yf_money*mx.in_weight,yfmx.remark_list,%s,'%s',now(),rk.warehouse,m1.txt1
            from  _m608_hlrk_list mx 
            left join _m608_hl_storage rk on rk.gw_id = mx.gw_id
            left join _m606_freight_sq yf on yf.gw_id = rk.yf_gwid
            left join _m605_huangliaocaigou cg on cg.gw_id = rk.cg_gwid
            left join mtc_t m on m.txt1 = mx.scsx and m.type='MATYP'
            left join mtc_t m1 on m1.id = rk.warehouse and m1.type='HLCK'
            left join _m606_yfdj_sq_list yfmx on yfmx.id = mx.yf_mxid
            left join _m605_hlcgmx_list cgmx on cgmx.id = mx.cg_mxid
            left join _m616_stone_varieties p on p.id = cgmx.stonename
            where mx.is_sel = 1 and mx.gw_id = %s
          """%(usr_id,usr_name,pk)
    db.executesql(sql)
    #根据入库实际重量更新运费单运费总价
    sql = """update _m606_freight_sq yf,_m608_hl_storage rk set yf.total_weight = rk.total_weight ,yf.total_money = rk.total_weight*yf.yf_money ,yf.gw_status = 2
             where yf.gw_id = rk.yf_gwid and rk.gw_id = %s"""%(pk)
    db.executesql(sql)
    return

def saveVerify610(pk,mode,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('list','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:    
        mx_id = e.get('mx_id','')
        sql = "select hl_number from _m610_produced_list where id=%s"%(mx_id)
        print ToGBK(sql)
        rows,iN = db.select(sql)
        hl_number = rows[0][0]
        sql = "update _m6031_stone_stock set status=1,ck_gwid=%s,ck_usrid=%s,ck_usrname='%s',ck_time=now() where id = %s"%(pk,cid,cusrname,hl_number)
        #print sql
        db.executesql(sql)
    return

def saveVerify618(pk,mode,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('dd_list','')
    cid = d_value[0]
    cusrname = d_value[1]
    for e in lists:    
        hlbh = e.get('hlbh','')
        sql = "update _m6031_stone_stock set status=3,ck_gwid=%s,ck_usrid=%s,ck_usrname='%s',ck_time=now() where hl_number = '%s'"%(pk,cid,cusrname,hlbh)
        #print sql
        db.executesql(sql)
    return

def saveVerify61401(pk,mode,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('dd_list','')
    cid = d_value[0]
    cusrname = d_value[1]
 
    sql = """update _m61401_db_ck_list ckl,_m6144_plank_stock ps,_m61401_db_chuku ck,mtc_t m set ps.stock_id = ck.dr_warehouse,ps.stock_name = m.txt1
             where ckl.gw_id = ck.gw_id and ckl.plank_sn = ps.plank_sn and m.id= ck.dr_warehouse and m.type='CKMC' and ck.gw_id = %s"""%(pk)
    db.executesql(sql)

    return

def saveVerify6033(pk,mode,d_value,request):
    data = request.POST.get('data','')
    data_list = json.loads(data)
    lists = data_list.get('dd_list','')
    cid = d_value[0]
    cusrname = d_value[1]
 
    sql = """update _m6033_hldb_list ckl,_m6031_stone_stock ss,_m6033_hldb ck,mtc_t m set ss.stock_id = ck.dr_warehouse,ss.stock_name = m.txt1
             where ckl.gw_id = ck.gw_id and ckl.hl_sn = ss.hl_number and m.id= ck.dr_warehouse and m.type='HLCK' and ck.gw_id = %s"""%(pk)
    db.executesql(sql)

    return