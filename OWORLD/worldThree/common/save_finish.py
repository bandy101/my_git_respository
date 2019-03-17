# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK'%prj_name) 
import json

def saveFinishData(menu_id,pk,d_value,request):
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]

    if str(menu_id)=='41102':  #入库申请
        finish_save_41102(pk,d_value,request)
    elif str(menu_id)=='407':  #材料采购
        finish_save_407(pk,d_value,request)

    return 

def finish_save_407(pk,d_value,request):
    cid = d_value[0]
    cusrname = d_value[1]
    
    sql = "select mat_id,price from _m407_clcg_list where gw_id=%s"%(pk)
    rows,iN = db.select(sql)
    for e in rows:
        mat_id = e[0]
        price = e[1]
        #更新最新采购价
        sql = "update _m504_clgl set new_cost=%s where id = %s"%(price,mat_id)
        db.executesql(sql)    
        
        sql1 = "select low_cost from _m504_clgl where id = %s"%(mat_id)
        rows1,iN1 = db.select(sql1)
        low_cost = rows1[0][0]
        if low_cost is None:
            sql2 = "update _m504_clgl set low_cost=%s where id = %s"%(price,mat_id)
            db.executesql(sql2)    
        elif price<low_cost:
            sql2 = "update _m504_clgl set low_cost=%s where id = %s"%(price,mat_id)
            db.executesql(sql2)    

def finish_save_41102(pk,d_value,request):
    cid = d_value[0]
    cusrname = d_value[1]

    sql = "update _m41102_rk_list set status = 1 where gw_id=%s"%pk
    db.executesql(sql)    
    sql = """insert into `mat_stock_log` (`type`,`type_name`,`direction`,`gw_id`,`mx_id`,`proj_id`,`mat_id`,`qty`,`in_qty`,`out_qty`,`price`,`amount`,`cid`,`cusrname`,`ctime`)
             select 1,'材料入库',1,rl.gw_id,rl.id,r.proj_id,mat_id,qty,qty,0,price,amount,rl.cid,rl.cusrname,rl.ctime from _m41102_rk_list rl 
                  left join `_m41102_rk` r on r.gw_id = rl.gw_id
                  where r.gw_id=%s;
          """%pk
    db.executesql(sql)    
    sql = "select r.proj_id,rl.mat_id,rl.qty,rl.price,rl.amount from _m41102_rk_list rl left join `_m41102_rk` r on r.gw_id = rl.gw_id  where r.gw_id=%s"%pk
    rows,iN = db.select(sql)
    for e in rows:
        proj_id = e[0]
        mat_id = e[1]
        qty = e[2]
        price = e[3]
        amount = e[4]
        cur_price = price   #本次价格

        sql1 = "select id,ifnull(qty,0),ifnull(amount,0),min_price,max_price from mat_stock where proj_id=%s and mat_id = %s"%(proj_id,mat_id)
        rows1,iN1 = db.select(sql1)
        if iN1 == 0:
            price = amount/qty
            sql2 = """insert mat_stock (`mat_id`,`proj_id`,`qty`,`price`,`amount`,min_price,max_price,new_price) 
                         values (%s,%s,%s,%s,%s,%s,%s,%s)
                   """%(mat_id,proj_id,qty,price,amount,price,price,price)
            db.executesql(sql2)    
        else:
            id = rows1[0][0]
            qty += rows1[0][1]
            amount += rows1[0][2]
            min_price = rows1[0][3]    #最低价
            max_price = rows1[0][4]    #最高价 
            price = amount/qty         #均价
            
            sql2 = "update mat_stock set qty = %s,price = %s,new_price=%s,amount = %s where id = %s"%(qty,price,cur_price,amount,id)
            db.executesql(sql2)    
            if max_price is None or cur_price> max_price:
                sql2 = "update mat_stock set max_price = %s where id =%s"%(cur_price,id)
                db.executesql(sql2)    
            if min_price is None or cur_price < min_price:
                sql2 = "update mat_stock set min_price = %s where id =%s"%(cur_price,id)
                db.executesql(sql2)    
        
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