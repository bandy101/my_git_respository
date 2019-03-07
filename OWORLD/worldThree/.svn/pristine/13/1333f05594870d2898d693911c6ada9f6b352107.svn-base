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
from django.db import connection
exec ('from %s.share import db,HttpResponseCORS,g_data,ToGBK,mValidateUser,fs_url,ComplexEncoder'%prj_name) 
from qr_code import genShdCode

def printShd(request):
    pk =  request.POST.get('pk') or  request.GET.get('pk','') 
    sql = """select op.cname,sh.sn,sh.ctime,su.cname,su.tel,sh.cusrname,ifnull(sh.qr_code,''),''
                   ,ht.req_no,cg.cusrname,m1.txt1,m2.txt1 
             from _m3000004_shd sh 
             left join _m1501_cgdd cg on sh.cgd_id = cg.id
             left join out_proj op on op.id = cg.proj_id
             left join suppliers su on su.id = cg.sup_id
             left join prj_mat_buy_ht ht on ht.id = cg.cght 
             left join mtc_t m1 on m1.type = 'cgzt' and m1.id = cg.cgzt
             left join mtc_t m2 on m2.type = 'cylgs' and m2.id = cg.gyl
             where sh.id=%s
             """%(pk)
    print sql
    rows,iN = db.select(sql)
    if iN == 0:
        s = """
        {
        "errcode": -1,
        "errmsg": "获取送货单数据失败"
        }        """
        return HttpResponseCORS(request,s)

    L = list(rows[0])
    if L[6] == '':
        L[6] = genShdCode(pk)
        sql = "update _m3000004_shd set qr_code='%s' where id=%s"%(L[6],pk)
        db.executesql(sql)
    sql = "select cl_code,cl_name,cl_spec,cl_model,cl_type,cl_brand,cl_unit,replace(cast(ROUND(total_qty,2) as char),'.00',''),replace(cast(ROUND(qty,2) as char),'.00',''),ROUND(price,2),ROUND(amount,2),memo  from _m3000004_shd_list where m_id=%s"%(pk)
    rows1,iN1 = db.select(sql)
    names = 'cl_code cl_name cl_spec cl_model cl_type cl_brand cl_unit total_qty qty price amount memo'.split()
    L[7] = [dict(zip(names, d)) for d in rows1]

    names = 'proj_name shd_no sh_date sup_name sup_tel usr_name qr_code lists cght cg_usr_name cgzt gyl'.split()
    L2 = dict(zip(names, L))
    data = json.dumps(L2,ensure_ascii=False,cls=ComplexEncoder)    
    s = """
        {
        "errcode": 0,
        "errmsg": "获取送货单数据成功",
        "data":%s
        }        """%(data)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)
