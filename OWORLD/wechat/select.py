# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
from django.db import connection
from share import db,dActiveUser,mValidateUser,HttpResponseCORS,ToGBK,ComplexEncoder
exec ('from %s.common.common import get_filter_data'%prj_name) 

def select_func(request):
    #menu_id = request.POST.get('menu_id', 0)
    #print menu_id
    #ret,msg,d_value = mValidateUser(request,"view",menu_id)
    #if ret!=0:
    #    return HttpResponseCORS(request,msg)
    func = request.GET.get('func', '')
    #print func
    if func =='getSigns':
       msg = get_sign_data(request)
    else:
        msg = get_select_data(request)

    return HttpResponseCORS(request,msg)

def get_select_data(request):
    field_id = request.GET.get('field_id', '') or request.POST.get('field_id', '')
    btn_id =  request.GET.get('btn_id', '') or request.POST.get('btn_id', '')
    if btn_id != '':
        sql ="""SELECT sel_type,sel_cols,24 from menu_form_grid_button where id=%s
         """%(btn_id)
    else:
        sql ="""SELECT sel_type,sel_cols,field_type from menu_form_cols where id=%s
         """%(field_id)
    print sql
    rows,iN = db.select(sql)
    if iN==0:
        return HttpResponseCORS(request,'')
    sel_type = rows[0][0]
    sel_cols = rows[0][1]
    field_type = rows[0][2]
    if field_type == 24 and btn_id == '':
        sql = "select id from menu_form_grid_button where field_id=%s order by id asc"%(field_id)
        rows,iN = db.select(sql)
        btn_id = rows[0][0]
    sql ="""SELECT sel_table,ifnull(sel_sort,'') from menu_select_source where  sel_type=%s"""%sel_type
    #print sql
    rows,iN = db.select(sql)
    if iN==0:
        return HttpResponseCORS(request,'')
    from_table = rows[0][0]
    from_table = from_table.replace('\n','')
    from_table = from_table.replace('\r','')
    from_sort = rows[0][1]
    #获取筛选的参数
    sql = """SELECT label,show_label,filter_name,filter_type
                   ,sort,defalut_value,span
                   ,field_type,field_txt,field_title,ifnull(para1,''),ifnull(para2,''),filter_sql
             FROM menu_select_filters
             where sel_type=%s order by sort"""%(sel_type)
    #print sql
    rows,iN = db.select(sql)
    SL=[]
    for e in rows:
        L1=list(e)
        value = request.POST.get(e[2],'')
        if value!='':
            value = e[5]
        para1,para2='',''
        if e[10]!='':
            para1 = request.POST.get(e[10],'')
        if e[11]!='':
            para2 = request.POST.get(e[11],'')
        L1[5] = get_filter_data(e[7],e[8],e[9],value,para1,para2)
        SL.append(L1)
    #print SL
    names = 'cname txt_show ename type sort data span'.split()
    data = [dict(zip(names, d)) for d in SL]
    filter = json.dumps(data,ensure_ascii=False)
    
    if btn_id != '':
        sql ="""select mp.para_name,ap.muti_sql from menu_form_url_para mp 
                   left join menu_select_all_para ap on ap.para_name=mp.para_name and ap.sel_type=%s
            where mp.btn_id=%s and ap.muti_sql is not null
          """%(sel_type,btn_id)
    elif field_type==15:
        sql ="""select mp.para_name,ap.filter_sql from menu_form_url_para mp 
                   left join menu_select_all_para ap on ap.para_name=mp.para_name and ap.sel_type=%s
            where mp.field_id=%s and ap.filter_sql is not null
          """%(sel_type,field_id)
    else:
        sql ="""select mp.para_name,ap.muti_sql from menu_form_url_para mp 
                   left join menu_select_all_para ap on ap.para_name=mp.para_name and ap.sel_type=%s
            where mp.field_id=%s and ap.muti_sql is not null
          """%(sel_type,field_id)
    print sql
    FL,iN = db.select(sql)

    #获取排序字段参数
    if btn_id != '':
        sql ="""SELECT ms.label,ms.col_name,ms.field_order,ifnull(fc.col_name,''),ifnull(is_hide,0),ifnull(is_unique,0), ms.field_show,ifnull(can_search,0) from menu_select_all_cols ms
                   left join menu_form_select_cols mc on mc.sel_col_id = ms.id
                   left join menu_form_cols fc on mc.field_id1 = fc.id 
                   where mc.btn_id=%s
                   order by ifnull(mc.sort,999)
         """%(btn_id)
    else:
        sql ="""SELECT ms.label,ms.col_name,ms.field_order,ifnull(fc.col_name,''),ifnull(is_hide,0),ifnull(is_unique,0), ms.field_show,ifnull(can_search,0) from menu_select_all_cols ms
                   left join menu_form_select_cols mc on mc.sel_col_id = ms.id
                   left join menu_form_cols fc on mc.field_id1 = fc.id 
                   where mc.field_id=%s
                   order by ifnull(mc.sort,999)
         """%(field_id)
    print ToGBK(sql)  
    NL,iN = db.select(sql)
    names = 'cname ename order field_name hide unique'.split()
    data = [dict(zip(names, d)) for d in NL]
    cols = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    aoData= request.POST.get('aoData', '')

    select_size = 10
    startNo = 0
    orderby = ''
    orderbydir=''
    qqid=''
    #print aoData
    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='iSortCol_0':
                iCol = e['value']
                orderby = NL[int(iCol)][2]
            elif e['name']=='sSortDir_0':
                orderbydir = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    sql = "select "
    for e in NL:    
       sql += "%s,"%(e[6])
    sql = sql[:-1]
    sql += " %s "%from_table
    if qqid!='':
        sTemp = "CONCAT('',"
        for e in NL:
            if e[7]==1:
                sTemp += "%s,"%e[6]
        sTemp = sTemp[:-1] + ")"
        sql+=" AND %s LIKE '%%%s%%'"%(sTemp,qqid)
    for e in SL:
        value = request.POST.get(e[2],'')
        if value != '': 
            sTemp = e[12].replace("$s",str(value))
            sql += " and (%s)"%(sTemp) 
    for e in FL:
        value = request.POST.get(e[0],'')
        if value != '': 
            sTemp = e[1].replace("$s",str(value))
            sql += " and (%s)"%(sTemp) 
    #ORDER BY 
    if orderby!='':
        sql+=' ORDER BY %s %s' % (orderby,orderbydir)
    elif from_sort!='':
        sql+= from_sort
    print ToGBK(sql)  
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,select_size)
    names=[]
    for n in range(0,len(NL)):
        names.append(NL[n][1])
    data = [dict(zip(names, d)) for d in rows]

    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "filter":%s,
        "cols":%s,
        "dataList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(filter,cols,s3,iTotal_length,iTotal_Page,pageNo,select_size)
    print ToGBK(s)
    return HttpResponseCORS(request,s)

def get_sign_data(request):
    ret,msg,d_value = mValidateUser(request,"view",'')
    if ret!=0:
        return HttpResponseCORS(request,msg)

    sql ="""SELECT sel_table from menu_select_source where  sel_type=3"""
    rows,iN = db.select(sql)
    if iN==0:
        return HttpResponseCORS(request,'')
    from_table = rows[0][0]
    from_table = from_table.replace('\n','')
    from_table = from_table.replace('\r','')

    #获取筛选的参数
    sql = """SELECT label,show_label,filter_name,filter_type
                   ,sort,defalut_value,span
                   ,field_type,field_txt,field_title,ifnull(para1,''),ifnull(para2,''),filter_sql
             FROM menu_select_filters
             where sel_type=3 order by sort"""
    #print sql
    rows,iN = db.select(sql)
    SL=[]
    for e in rows:
        L1=list(e)
        value = request.POST.get(e[2],'')
        if value!='':
            value = e[5]
        para1,para2='',''
        if e[10]!='':
            para1 = request.POST.get(e[10],'')
        if e[11]!='':
            para2 = request.POST.get(e[11],'')
        L1[5] = get_filter_data(e[7],e[8],e[9],value,para1,para2)
        SL.append(L1)
    #print SL
    names = 'cname txt_show ename type sort data span'.split()
    data = [dict(zip(names, d)) for d in SL]
    filter = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    #获取排序字段参数
    sql ="""SELECT ms.label,ms.col_name,ms.field_order, ms.field_show,ifnull(can_search,0) from menu_select_all_cols ms
                   where sel_type = 3 and id!=13
                   order by ifnull(ms.sort,999)
         """
    #print sql
    NL,iN = db.select(sql)
    names = 'cname ename order'.split()
    data = [dict(zip(names, d)) for d in NL]
    cols = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    aoData= request.POST.get('aoData', '')

    select_size = 10
    startNo = 0
    orderby = ''
    orderbydir=''
    qqid=''
    #print aoData
    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='iSortCol_0':
                iCol = e['value']
                orderby = NL[int(iCol)][2]
            elif e['name']=='sSortDir_0':
                orderbydir = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    sql = "select "
    for e in NL:    
       sql += "%s,"%(e[3])
    sql = sql[:-1]
    sql += " %s "%from_table
    if qqid!='':
        sTemp = "CONCAT('',"
        for e in NL:
            if e[4]==1:
                sTemp += "%s,"%e[3]
        sTemp = sTemp[:-1] + ")"
        sql+=" AND %s LIKE '%%%s%%'"%(sTemp,qqid)
    for e in SL:
        value = request.POST.get(e[2],'')
        if value != '': 
            sTemp = e[12].replace("$s",str(value))
            sql += " and (%s)"%(sTemp) 
    usr_id = d_value[0]
    #usr_id = request.session.get('usr_id', 1)

    sql += " and ur.usr_id not in (1,2,%s)"%usr_id
    #ORDER BY 
    if orderby!='':
        sql+=' ORDER BY %s %s' % (orderby,orderbydir)
    #print request.POST
    #print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,select_size)
    names=[]
    for n in range(0,len(NL)):
        names.append(NL[n][1])
    data = [dict(zip(names, d)) for d in rows]

    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "filter":%s,
        "cols":%s,
        "dataList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(filter,cols,s3,iTotal_length,iTotal_Page,pageNo,select_size)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)
