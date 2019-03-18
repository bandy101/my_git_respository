# -*- coding: utf-8 -*-
# 尝试
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
from share import db,HttpResponseCORS,g_data,ToGBK,mValidateUser,fs_url,ComplexEncoder

def proj_mat_func(request):
    audit_data = ['','']
    ret,errmsg,d_value = mValidateUser(request,"view",'')
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    dept_id = d_value[2]
    proj_id = request.POST.get('proj_id','')    

    sql = """select s.proj_id,op.cname,op.gc_no,s.jh_money,s.cght_money
             ,s.cg_money,s.rk_money,s.cg_money - ifnull(s.rk_money,0),s.paid_money
             from report_proj_statistics_all s
             left join out_proj op on s.proj_id = op.id
             where s.proj_id = %s"""%(proj_id)

    names = 'proj_id proj_name proj_no jh_money cght_money cg_money rk_money wrk_money paid_money'.split()
    rows,iN = db.select(sql)
    data = [dict(zip(names, d)) for d in rows]
    proj_data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql = """select s.sup_id,su.cname,s.cght_money
             ,s.cg_money,s.rk_money
             from report_proj_sup_stat s
             left join suppliers su on s.sup_id = su.id
             where s.proj_id = %s"""%(proj_id)
    names = 'sup_id sup_name cght_money cg_money rk_money'.split()
    rows,iN = db.select(sql)
    data = [dict(zip(names, d)) for d in rows]
    sup_data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql = """select p.year,p.month,p.cght_money,p.cg_money,p.rk_money,p.paid_money,m.stock_money
             from report_proj_statistics_month p
             left join report_proj_mat_month m on p.proj_id = m.proj_id and p.year = m.year and p.month = m.month
             where p.proj_id = %s
             order by p.year desc,p.month desc
             limit 12
          """%(proj_id)
    names = 'year month cght_money cg_money rk_money paid_money stock_money'.split()
    rows,iN = db.select(sql)
    data = [dict(zip(names, d)) for d in rows]
    month_data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""select proj_id,proj_name,proj_no,proj_id=%s from report_proj_statistics_all
        """%(proj_id)
    rows,iN=db.select(sql)
    names = 'id cname proj_no selected'.split()
    data = [dict(zip(names, d)) for d in rows]
    option_data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取主页数据成功",
        "proj_data":%s,
        "sup_data":%s,
        "month_data":%s,
        "option_data":%s
        }        """%(proj_data,sup_data,month_data,option_data)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)
