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
from aesMsgCrypt                import WXBizMsgCrypt
import httplib
import urllib
from django.db import connection
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,fs_url,ComplexEncoder,mValidateUser
import MySQLdb

def getProjInfo(request):
    pageNo = request.POST.get('pageNo','') or 1
    pageNo = int(pageNo)
    search = request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    sql="""select id,gc_no,cname from out_proj where 1=1 
        """
    if search !='':
        sql+=" AND (IFNULL(cname,'') LIKE '%%%s%%' OR IFNULL(gc_no,'') LIKE '%%%s%%' )"%(search,search)
    sql+="ORDER BY id DESC"
    print sql
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'proj_id proj_no proj_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(request,s)

def getRecentlyProj(request):
    #ret,errmsg,d_value = mValidateUser(request,"view",104)
    #if ret!=0:
    #    return HttpResponseCORS(request,errmsg)
    usr_id = 2#d_value[0] 
    sql="""select op.id,op.cname,op.gc_no from user_options u
           left join out_proj op on u.option_id = op.id
           where u.option_type = 21 and u.usr_id = %s
           order by u.ctime desc
           limit 10
        """%(usr_id)
    rows,iN = db.select(sql)
    names = 'proj_id proj_name proj_no'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "data":%s
        }        """%(L)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(request,s)

def setRecentlyProj(request):
    #ret,errmsg,d_value = mValidateUser(request,"view",104)
    #if ret!=0:
    #    return HttpResponseCORS(request,errmsg)
    usr_id = 2#d_value[0] 
    proj_id = request.POST.get('proj_id','')
    if (usr_id==0 or proj_id==''):
        s = """
        {
        "errcode": -1,
        "errmsg": "参数错误"
        }        """
        return HttpResponseJsonCORS(request,s)

    sql="""select id,gc_no,cname from out_proj where id=%s
        """%(proj_id)
    rows,iN = db.select(sql)
    proj_name = '(%s)%s'%(rows[0][1],rows[0][2])
    sql = "select id from user_options where usr_id=%s and option_type=21 and option_id=%s"%(usr_id,proj_id)
    rows,iN = db.select(sql)
    if iN>0:
        sql = "update user_options set option_value='%s',option_tips='%s',ctime=now(),hits=hits+1 where id=%s"%(proj_name,proj_name,rows[0][0])
    else:
        sql = """insert into user_options (usr_id,option_type,option_id,option_value,option_tips,ctime,hits)
              values (%s,21,%s,'%s','%s',now(),1)"""%(usr_id,proj_id,proj_name,proj_name)
    #print sql
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "保存成功"
        }        """
    return HttpResponseJsonCORS(request,s)








