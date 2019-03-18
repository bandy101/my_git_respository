# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname,HttpResponseCORS,HttpResponseJsonCORS,ComplexEncoder'%prj_name) 
import json
import MySQLdb

def getPanelInfo(request):
    bundle_code = request.POST.get('bundle_code') or request.GET.get('bundle_code', 0) 

    sql = """select db.bundle_code,m.txt1,hl.stone_name,hl.scsx_name,hl.sccd,sum(db.square_real),'',p.zhashu,p.square,hl.stone_id,db.stock_id from _m6144_plank_stock db
             left join _m6031_stone_stock hl on hl.hl_number = db.hl_number
             left join _m616_stone_varieties sv on sv.id = hl.stone_id
             left join mtc_t m on m.id = sv.material and m.type='SZCZ'
             left join _m611_packing p on p.hl_number = db.hl_number
             where db.bundle_code = '%s' #and db.is_sale = 0
          """%bundle_code
    rows,iN = db.select(sql)
    #print sql
    if iN == 0:
        s = """
        {
        "errcode": -1,
        "errmsg": "板材信息不存在",
        }        """
        #print ToGBK(s)
        return HttpResponseJsonCORS(request,s)
 
    L=list(rows[0])
    sql = """select sum(db.square_real)  from _m6144_plank_stock db 
             where db.bundle_code = '%s' #and db.is_sale = 0
             group by db.bundle_code
          """%bundle_code
    #print sql
    rows1,iN1 = db.select(sql)
    if iN1 == 0:
        L[5] = 0
    else:
        L[5] = rows1[0][0]

    sql = """select db.plank_sn,db.sc_long,db.wide,db.thick,db.square_real,db.bc_picture,is_sale  from _m6144_plank_stock db 
             where db.bundle_code = '%s' #and db.is_sale = 0
          """%bundle_code
    #print sql
    rows1,iN1 = db.select(sql)
    names = 'panel_no length width thick square pic is_sale'.split()
    data1 =  [dict(zip(names, d)) for d in rows1]
    L[6] = data1

    names = 'bundle_code material name property origin square lists zhashu total_square'.split()
    data = dict(zip(names, L))
    panel_info = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取板材信息成功",
        "panel_info":%s,
        }        """%(panel_info)
    #print ToGBK(s)
    return HttpResponseJsonCORS(request,s)


