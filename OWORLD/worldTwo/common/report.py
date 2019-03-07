# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import os
import json
import time
import datetime 
import decimal
from HW_DT_TOOL                 import getToday
import httplib
import random
import MySQLdb
from django.http import HttpResponseRedirect  

exec ('from %s.share        import ComplexEncoder,mValidateUser,HttpResponseCORS'%prj_name) 
exec ('from %s.share        import db,ToGBK,dActiveUser,g_data,data_url,front_url,fs_url,m_corp_name,m_muti_lang'%prj_name) 

def getReportData(request):
    menu_id = request.POST.get('menu_id', '20501')
    #ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    #if ret!=0:
    #    return HttpResponseCORS(request,errmsg)
    #usr_id = d_value[0]
    #dept_id = d_value[2]

    sql = """select menu_name from menu_func 
                    where menu_id=%s"""%(menu_id)
    L,iN = db.select(sql)
    title = L[0][0]

    #print request.POST
    pk = request.GET.get('pk', '')
    page = request.POST.get('page', '')
    data = request.POST.get('data', '{}')
    data_list = json.loads(data)
    value_dict = dict()    
    sql = """select DISTINCT mp.page_name,mp.label,mp.sort,'',mp.id from menu_report_pages mp 
                    where mp.menu_id=%s and mp.status=1 order by sort"""%(menu_id)
    rows,iN = db.select(sql)
    TL = []
    for e in rows:
        L1=list(e)
        if page=='':
            page = L1[0]
        if L1[0] == page:
            L1[3] = 1
            page_id = L1[4]
        TL.append(L1)            
    names = 'page_ename page_cname sort selected'.split()
    data = [dict(zip(names, d)) for d in TL]
    page_value = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    #获取当前页数据的参数
    sql = "select final_sql from menu_report_pages where id='%s'"%(page_id)
    rows,iN = db.select(sql)
    page_sql = rows[0][0]
    sql = packPara(page_sql,value_dict,request)
    if sql == '':  
        rows,iN = [],0
    else:
        rows,iN = db.select(sql)

    sql ="""SELECT mc.col_name
                  ,mc.label
                  ,ft.name
                  ,mc.default_value
                  ,mc.hide
                  ,''
                  ,''
                  ,url
                  ,mc.url_target
                  ,mc.sort
                  ,mc.final_sql
                  ,mc.field_type
                  ,ifnull(default_options,'')
                  ,ifnull(mc.change_cols,'')
                  ,mc.id
                FROM menu_report_cols mc
                LEFT join field_type ft on mc.field_type = ft.id
                where mc.page_id=%s and mc.status = 1"""%(page_id)
    sql+="""     order by mc.sort """
    names = 'cid label field_type value hide table_col table_data url field_options sort'.split()
    rows1,iN1 = db.select(sql)
    L = []
    for i in range(0,iN1):
        e = list(rows1[i])
        if iN>0 and i<len(rows[0]):
            e[3] = rows[0][i]
            
        value_dict[rows1[i][0]] = e[3]
        L.append(e)

    L1 = []
    for i in range(0,iN1):
        e = list(L[i])
        if str(e[11]) == '36':  #表格
            e[5],e[6] = getReportGrid(menu_id,e[-1],pk,value_dict,request)
        elif str(e[11]) in ['6','26','18']:  
            e[8] = get_options_data(e[10],e[3],e[12],value_dict,request)
        if e[-2] != '':
            change_cols = e[-2].strip()
            if change_cols[-1] == ',':
                change_cols = change_cols[:-1]
            e[7] = packRefreshUrl(menu_id,pk,page,page_id,e[-1],change_cols)
        L1.append(e)

    data = [dict(zip(names, d)) for d in L1]
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取报表数据成功",
        "title":"%s",
        "pages":%s,
        "data":%s
        }
        """%(title,page_value,s3)
    #print s
    return HttpResponseCORS(request,s)

def getReportGridData(request):
    #print request.POST
    menu_id = request.POST.get('menu_id', '20501')
    pk = request.GET.get('pk', '')
    page = request.POST.get('page', '')
    field_id = request.POST.get('field_id', '')
    value_dict = dict()    

    sql = """select DISTINCT mp.page_name,mp.label,mp.sort,'',mp.id from menu_report_pages mp 
                    where mp.menu_id=%s and mp.status=1 order by sort"""%(menu_id)
    rows,iN = db.select(sql)
    for e in rows:
        L1=list(e)
        if page=='':
            page = L1[0]
        if L1[0] == page:
            L1[3] = 1
            page_id = L1[4]
    
    sql ="""SELECT mc.col_name
                  ,mc.label
                  ,ft.name
                  ,mc.default_value
                  ,mc.hide
                  ,''
                  ,''
                  ,url
                  ,mc.url_target
                  ,mc.sort
                  ,mc.final_sql
                  ,mc.field_type
                  ,ifnull(default_options,'')
                  ,mc.is_number
                  ,mc.id
                FROM menu_report_cols mc
                LEFT join field_type ft on mc.field_type = ft.id
                where mc.page_id=%s and mc.status = 1 and mc.col_name='%s'"""%(page_id,field_id)
    names = 'cid label field_type value hide table_col table_data url field_options sort'.split()
    rows1,iN1 = db.select(sql)
    L = []
    for i in range(0,iN1):
        e = list(rows1[i])
        if str(e[11]) == '36':  #表格
            e[5],e[6] = getReportGrid(menu_id,e[-1],pk,value_dict,request)
        L.append(e)

    data = [dict(zip(names, d)) for d in L]
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    s = """
        {
        "errcode": 0,
        "errmsg": "获取报表数据成功",
        "data":%s
        }
        """%(s3)
    #print s
    return HttpResponseCORS(request,s)

def getReportGrid(menu_id,field_id,pk,value_dict,request):
    #print request.POST
    page = request.POST.get('page', '')
    aoData= request.POST.get('aoData', '')
    select_size = 50
    startNo = 0
    orderby = ''
    orderbydir=''
    qqid=''
    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
                qqid = MySQLdb.escape_string(qqid)
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    #print value_dict
    L = []
    for i in range(1,4):
        sql ="""SELECT col_name,ifnull(label,''),hide,rowspan,colspan,is_sum,bg_color,can_expanded,url,sort,align,value_align,url_target,paras
                  ,id
                FROM menu_report_grid_cols
                where m_id=%s and status=1 and level = %s
                order by sort """%(field_id,i)
        #print sql
        names = 'cid label hide rowspan colspan is_sum bg_color can_expanded url sort align value_align'.split()
        LL=[]
        rows1,iN1 = db.select(sql)
        for e in rows1:
            LL1 = list(e)
            LL1[1] = packGridLabel(e[0],e[1],value_dict,request)
            if e[7] == 1:
                LL1[8] = packExpandedUrl(e[-1],e[-2])
            LL.append(LL1)
        data = [dict(zip(names, d)) for d in LL]
        L1 = [i,'']
        L1[1] = data
        if iN1>0:
            col_row = rows1
            L.append(L1)
    names = 'level cols'.split()
    col_data = [dict(zip(names, d)) for d in L]

    sql = "select final_sql,ifnull(default_order,''),ifnull(search_sql,'') from `menu_report_cols` where id=%s "%(field_id)
    rows,iN = db.select(sql)
    if iN>0:
        L = ['','','','','']
        grid_sql = rows[0][0]
        default_order = rows[0][1]
        search_sql = rows[0][2]
        sql = packPara(grid_sql,value_dict,request)
        if qqid!='' and search_sql!='':
            sql+=" AND %s LIKE '%%%s%%'"%(search_sql,qqid)
        sql2 = sql + " limit 1"
        if aoData!='':
            rows2,iN2,cols2 = db.select_include_name(sql2)
            jsonData = json.loads(aoData)
            for e in jsonData:
                if e['name']=='iSortCol_0':
                    iCol = e['value']
                    orderby = cols2[int(iCol)][0] 
                elif e['name']=='sSortDir_0':
                    orderbydir = e['value']
        #ORDER BY 
        if orderby!='':
            sql+=' ORDER BY %s %s' % (orderby,orderbydir)
        else:
            sql+=" %s"%default_order
        print ToGBK(sql)
        rows,L[1],L[2],L[3],L[4] = db.select_for_grid(sql,pageNo,select_size)
        names=[]
        for n in range(0,len(col_row)):
            names.append(col_row[n][0])
        print names
        data = [dict(zip(names, d)) for d in rows]
        L[0] = data      
        names = 'rows iTotal_length iTotal_Page pageNo select_size'.split()
        list_data = dict(zip(names, L))
    return col_data,list_data

def getReportExpandedData(request):
    #print request.POST
    col_id = request.GET.get('col_id', '')

    data = []
    value_dict = dict()    
    sql ="""SELECT ifnull(expanded_sql,'')
                FROM menu_report_grid_cols
                where id='%s' """%(col_id)
    rows,iN = db.select(sql)
    if iN>0:
        sql = rows[0][0]
        sql = packPara(sql,value_dict,request)
        print sql
        data = db.select_zip_by_name(sql)
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取报表数据成功",
        "data":%s
        }
        """%(s3)
    #print s
    return HttpResponseCORS(request,s)

def getReportRefreshData(request):
    menu_id = request.GET.get('menu_id', '20501')
    pk = request.GET.get('pk', '')
    page = request.GET.get('page', '')
    page_id = request.GET.get('page_id', '')
    col_id = request.GET.get('col_id', '')
    refresh_field = ''
    value_dict = dict()    
    sql = "SELECT change_cols from menu_report_cols where id=%s"%col_id
    #print sql
    rows,iN = db.select(sql)
    if iN>0:
        refresh_field = rows[0][0]

    sql ="""SELECT mc.col_name
                  ,mc.label
                  ,ft.name
                  ,mc.default_value
                  ,mc.hide
                  ,''
                  ,''
                  ,url
                  ,mc.url_target
                  ,mc.sort
                  ,mc.final_sql
                  ,mc.field_type
                  ,ifnull(default_options,'')
                  ,ifnull(mc.change_cols,'')
                  ,mc.id
                FROM menu_report_cols mc
                LEFT join field_type ft on mc.field_type = ft.id
                where mc.id in (%s) and mc.status = 1 """%(refresh_field)
    sql+="""     order by mc.sort """
    names = 'cid label field_type value hide table_col table_data url field_options sort'.split()
    rows1,iN1 = db.select(sql)
    L = []
    for i in range(0,iN1):
        e = list(rows1[i])
        if str(e[11]) == '36':  #表格
            e[5],e[6] = getReportGrid(menu_id,e[-1],pk,value_dict,request)
        elif str(e[11]) in ['6','26','18']:  
            e[8] = get_options_data(e[10],e[3],e[12],value_dict,request)
        if e[-2] != '':
            change_cols = e[-2].strip()
            if change_cols[-1] == ',':
                change_cols = change_cols[:-1]
            e[7] = packRefreshUrl(menu_id,pk,page,page_id,e[-1],change_cols)
        L.append(e)

    data = [dict(zip(names, d)) for d in L]
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取报表数据成功",
        "formData":%s
        }
        """%(s3)
    #print s
    return HttpResponseCORS(request,s)

def packRefreshUrl(menu_id,pk,page,page_id,col_id,change_cols):
    L = ['href','para','_refresh']
    L[0] = "/common/getReportRefreshData/?menu_id=%s&pk=%s&page_id=%s&col_id=%s"%(menu_id,pk,page_id,col_id)
    lT = []
    sql = "select col_name,col_name from menu_report_cols where id not in (%s) and field_type not in (9) and page_id=%s"%(change_cols,page_id)
    rows,iN = db.select(sql)
    names = 'para_name link_field'.split()
    L[1] = [dict(zip(names, d)) for d in rows]
    names = 'href para target'.split()
    L3 = dict(zip(names, L))
    return L3


def packExpandedUrl(col_id,paras):
    L = ['expanded_href','expanded_para']
    L[0] = "/common/getReportExpandedData/?col_id=%s"%(col_id)
    lT = []
    para_list = paras.split(',')
    for e in para_list:
       e1 = e.strip()
       if e1 != '':
           L1 = ['','']
           L1 = e1.split(':')
           lT.append(L1)
    names = 'para_name link_field'.split()
    L[1] = [dict(zip(names, d)) for d in lT]
    names = 'expanded_href expanded_para'.split()
    L3 = dict(zip(names, L))
    return L3
def packGridLabel(col_name,label,value_dict,request):
    if col_name == 'daily_cost_header':
        year1 = request.POST.get('year1') or value_dict.get('year1','')
        month1 = request.POST.get('month1') or value_dict.get('month1','')
        if month1 == '':
            label = "%s年度全年费用统计表"%(year1)
        else:
            label = "%s年度%s月费用统计表"%(year1,month1)     
    else:
        return packPara(label,value_dict,request)
    return label
def packPara(source,value_dict,request):
    sql = source
    for e in request.POST:
        value = request.POST.get(e,'')
        sql = sql.replace('{%s}'%e,str(value))
    data = request.POST.get('data', '{}')
    data_list = json.loads(data)
    for e in data_list:
        value = data_list.get(e,'')
        sql = sql.replace('{%s}'%e,str(value))

    for e in request.GET:
        value = request.GET.get(e,'')
        sql = sql.replace('{%s}'%e,str(value))
    for e in value_dict:
        value = value_dict.get(e,'')
        sql = sql.replace('{%s}'%e,str(value))
    return sql

def get_options_data(txt,default,title,value_dict,request):
    sql = packPara(txt,value_dict,request)
    default = packPara(default,value_dict,request)
    L = get_sql_data(sql,default,title)
    options =['',False]
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    print L1
    return L1

def get_sql_data(txt,sDF,title='--请选择--'): 
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]

    sql=txt
    if sql=='':
        return 
  
    print ToGBK(sql)
    #print "sDF = %s"%sDF
    try:
        lT,iN = db.select(sql)
    except:
        lT = []
    for e in lT:
        if sDF.upper()==str(e[0]).upper():b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L