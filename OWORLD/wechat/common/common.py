# -*- coding: utf-8 -*-
# 尝试
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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

exec ('from %s.share        import ComplexEncoder,mValidateUser,get_YES_NO_data,get_mtc_t_data,get_roles_list,HttpResponseCORS,get_mtc_sys_data'%prj_name) 
exec ('from %s.share        import addtwodimdict,get_gw_type_data1,get_gw_type_data2,get_flow_data,get_table_field,get_page_field,get_col_field,get_all_tables,get_use_tables'%prj_name) 
exec ('from %s.share        import get_options_data,ToGBK,get_options_data_view,get_options_data_level,get_options_data_search'%prj_name) 
exec ('from %s.share        import op_CB,db,dActiveUser,g_data,data_url,front_url,fs_url,m_corp_name,m_muti_lang'%prj_name) 
from flow import get_next_flow,get_next_sel_type,get_next_dept,get_next_role,get_next_user
from info import getInfoAttribute,getInfoList,getInfoFormView,saveComment,saveInfo,getInfoAuditHis
from save_list import saveListData
from form_ext import getPageDataExt
from schedule import getScheduleData

def getTitle(menu_id,lang_id):
    if m_muti_lang==1 and lang_id>1:
        sql = """select m1.menu_id,
       case l1.`name` when '' then m1.menu_name else l1.`name` end,m2.menu_id,
       case l2.`name` when '' then m2.menu_name else l2.`name` end,ifnull(m3.menu_id,0),
       case ifnull(l3.`name`,'') when '' then '' else l3.`name` end from menu_func m1 
                    left join menu_func m2 on m2.menu_id = m1.parent_id
                    left join menu_func m3 on m3.menu_id = m2.parent_id and m3.menu !=0 
                    left join muti_lang_menu l1 on l1.menu_id = m1.menu_id and l1.lang_id = %s
                    left join muti_lang_menu l2 on l2.menu_id = m2.menu_id and l2.lang_id = %s
                    left join muti_lang_menu l3 on l3.menu_id = m3.menu_id and l3.lang_id = %s
                    where m1.menu_id=%s"""%(lang_id,lang_id,lang_id,menu_id)
    else:
        sql = """select m1.menu_id,m1.menu_name,m2.menu_id,m2.menu_name,ifnull(m3.menu_id,0),ifnull(m3.menu_name,'%s') from menu_func m1 
                    left join menu_func m2 on m2.menu_id = m1.parent_id
                    left join menu_func m3 on m3.menu_id = m2.parent_id and m3.menu !=0 
                    where m1.menu_id=%s"""%(m_corp_name,menu_id)
    #print ToGBK(sql)
    L,iN = db.select(sql)
    if iN ==0:
        errCode = -1
        errmsg = ''
        s = """
            {
            "errcode": %s,
            "errmsg": "你没有权限浏览当前页",
            }
            """ %(errCode,errmsg)  
        return HttpResponseCORS(request,s)


    title = L[0][1]
    names = 'menu_id menu_name parent_id parent_name pp_id pp_name'.split()
    data = [dict(zip(names, d)) for d in L]

    menu = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    return title,menu
def getTabPermission(tab_id,menu_id,gw_type,usr_id):
    show_flag = 1
    if usr_id in [1,2]: 
        return show_flag
    sql = """select 1
                from usr_role ur
                left join role_menu rm on rm.role_id = ur.role_id and rm.menu_id=%s
                where FIND_IN_SET('%s',rm.tabs) and ur.usr_id=%s
                """%(menu_id,tab_id,usr_id)
    #print sql
    rows,iN = db.select(sql)    
    if iN==0:
        show_flag = 0
    return show_flag

def getTabCounts(tab_name,menu_id,gw_type,usr_id,request,value_dict):
    counts = ''
    if tab_name=='my':
        sql = "select count(id) from gw_audit D where D.type_id=%s and D.usr_Id=%s and D.s_flag = 1 "%(gw_type,usr_id)
        rows,iN = db.select(sql)    
        if iN>0:
            counts = rows[0][0]
    elif tab_name=='audit':
        sql = "select count(id) from gw_audit D where D.type_id=%s and D.usr_Id=%s and D.s_flag = 0 "%(gw_type,usr_id)
        rows,iN = db.select(sql)    
        if iN>0:
            counts = rows[0][0]
    elif tab_name=='sign':
        sql = "select count(id) from gw_sign D where D.type_id=%s and D.usr_Id=%s"%(gw_type,usr_id)
        rows,iN = db.select(sql)    
        if iN>0:
            counts = rows[0][0]
    elif tab_name in ['verify']:
        if menu_id == '10202':
            sql = "select count(id) from bumph_bubbl where audit=1 and audusrid='%s' "%(usr_id)
        elif menu_id in ['203','207']:
            #获取当前页数据的参数
            sql = "select id,table_sql from menu_list_pages where menu_id=%s and page_name='verify'"%(menu_id)
            TL,iN = db.select(sql)
            page_id = TL[0][0]
            final_sql = TL[0][1]
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_list_pages_para` where page_id=%s order by sort"%(page_id)
            para_row,iN = db.select(sql)
            sql = "select count(1) " + packPara(final_sql,para_row,value_dict,request)
        else:
            sql = "select count(id) from gw_verify D where D.type_id=%s"%(gw_type)
        rows,iN = db.select(sql)    
        if iN>0:
            counts = rows[0][0]
    return counts

def getListAttribute(request):
    menu_id = request.POST.get('menu_id', 0)
    ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    value_dict = dict()    
    sUrl = ''
    sql = " select gw_type2 from menu_data_source where menu_id=%s"%menu_id
    rows,iN = db.select(sql)
    if iN>0:
        gw_type = rows[0][0]
    else:
        gw_type = 0
    value_dict['type_id'] = gw_type

    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)

    usr_id = d_value[0]
    usr_name = d_value[1]

    tab = request.POST.get('tab', '')
    data = request.POST.get('data', '{}')
    data_list = json.loads(data)
    
    title,menu = getTitle(menu_id,lang_id)

    if str(menu_id) == '10201':
        return getInfoAttribute(request,title,menu)

    sql = " select ifnull(gw_type2,0) from menu_data_source where menu_id=%s"%menu_id
    rows,iN = db.select(sql)
    if iN>0:
        gw_type = rows[0][0]
    else:
        gw_type= 0
    
    page_id = 0
    if usr_id in [1,2]:
       sql = "select mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp where  mp.menu_id=%s and mp.status=1 order by mp.sort"%menu_id
    else:
        sql = """select DISTINCT mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp 
                    left join role_menu rm on  rm.menu_id= mp.menu_id
                    left join usr_role ur on rm.role_id = ur.role_id
                    where mp.menu_id=%s and mp.status=1 and ur.usr_id = %s and FIND_IN_SET(mp.id,rm.tabs) order by mp.sort"""%(menu_id,usr_id)
    #print sql
    rows,iN = db.select(sql)
    TL=[]
    for n in range(0,len(rows)):
        L1=list(rows[n])
        if n==0 and tab=='':
            tab = rows[0][0]
            page_id = rows[0][6]
        if L1[0] == tab:
            L1[3] = 1
            page_id = L1[6]
        L1[5] = getTabCounts(rows[n][0],menu_id,gw_type,usr_id,request,value_dict)
        TL.append(L1)            
    names = 'tab_ename tab_cname sort selected has_add count'.split()
    data = [dict(zip(names, d)) for d in TL]
    tab_value = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql = """SELECT label,show_label,filter_name,filter_type
                   ,sort,ifnull(defalut_value,''),span,''
                   ,field_type,field_txt,field_title,ifnull(para1,''),ifnull(para2,''),ifnull(para_cols,''),id
             FROM menu_list_filters 
             where FIND_IN_SET(%s,pages) and filter_type!=0 order by sort"""%(page_id)
    #print sql
    rows,iN = db.select(sql)
    SL=[]
    #print data_list
    for e in rows:
        L1=list(e)
        if data_list.get(e[2]):
            value = data_list[e[2]]
        else:
            value = e[5]
            value = value.replace('{cur_usr_id}',str(usr_id))
        #print "%s %s %s %s "%(e[2],data_list.get(e[2]),e[5],value)
        para1,para2='',''
        if e[11]!='':
            para1 = data_list.get(e[11],0) 
        if e[12]!='':
            para2 = data_list.get(e[12],0)
        if e[3] == 1:
            L1[5] = get_filter_data(e[8],e[9],e[10],value,para1,para2)
        L1[7] = packFilterUrl(e[-1],"%s/getData/?func=filter&menu_id=%s&field_id=%s"%(data_url,menu_id,e[-1]),"_refresh",e[-2])
        SL.append(L1)
    #print SL
    names = 'cname txt_show ename type sort data span url'.split()
    data = [dict(zip(names, d)) for d in SL]
    filter = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    try:
        sql = """SELECT button_name,url,para_cols,id
             FROM menu_list_buttons 
             where FIND_IN_SET(%s,pages) order by sort"""%(page_id)
        #print sql
        rows,iN = db.select(sql)
        BL=[]
        #print data_list
        for e in rows:
            L1=list(e)
            L1[1] = packFilterUrl(e[-1],"%s/common/batchOperation/?menu_id=%s&btn_id=%s"%(data_url,menu_id,e[-1]),"",e[-2])
            BL.append(L1)
    except:
        BL=[]
    names = 'name url'.split()
    data = [dict(zip(names, d)) for d in BL]
    buttons = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    #获取列表字段参数

    if m_muti_lang==1 and lang_id>1:
        sql ="""SELECT DISTINCT case ifnull(l.`label`,'') when '' then c.`label`  else l.`label` end,
                 col_name,IFNULL(field_order,''),col_type1,size,ifnull(url,''),is_index,ifnull(btn_name,''),ifnull(url_target,''),c.id
             FROM menu_list_cols c
             LEFT JOIN muti_lang_list l on l.field_id = c.id and l.lang_id = %s
             where FIND_IN_SET(%s,c.pages)   order by c.sort"""%(lang_id,page_id) 
    else:
        sql ="""SELECT label,col_name,IFNULL(field_order,''),col_type1,size,ifnull(url,''),is_index,ifnull(btn_name,''),ifnull(url_target,''),id
             FROM menu_list_cols 
             where FIND_IN_SET(%s,pages)   order by sort"""%(page_id)
    #print sql
    NL,iN = db.select(sql)
    names = 'cname ename order type length url is_index btn_name'.split()
    L = []
    for i in range(0,iN):
        e = list(NL[i])
        if e[5] != '':
            e[5] = packListUrl(e[-1],e[5],e[-2])
        L.append(e)
    data = [dict(zip(names, d)) for d in L]
    cols = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户管理页面成功",
        "title":"%s",
        "menu":%s,
        "tab":%s,
        "filter":%s,
        "buttons":%s,
        "cols":%s,
        }        """%(title,menu,tab_value,filter,buttons,cols)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getFilterData(field_id,request):
    menu_id = request.GET.get('menu_id', 0)
    value_dict = dict()    
    refresh_field = ''
    para_cols = ''
    sql = "SELECT change_cols,para_cols from menu_list_filters where id=%s"%field_id
    rows,iN = db.select(sql)
    if iN>0:
        refresh_field = rows[0][0] or ''
        para_cols = rows[0][1] or ''
    #print para_cols
    para_list = para_cols.split(',')
    for e in para_list:
        value_dict[e] = request.POST.get(e,'')

    sql = """SELECT label,show_label,filter_name,filter_type
                   ,sort,ifnull(defalut_value,''),span,''
                   ,field_type,field_txt,field_title,ifnull(para1,''),ifnull(para2,''),ifnull(para_cols,''),id
             FROM menu_list_filters
             where FIND_IN_SET(id,'%s')  order by sort"""%(refresh_field)
    rows,iN = db.select(sql)
    SL=[]
    #print data_list
    for e in rows:
        L1=list(e)
        value = ''
        para1,para2='',''
        if e[11]!='':
            para1 = request.POST.get(e[11],'')
        if e[12]!='':
            para2 = request.POST.get(e[12],'')
        L1[5] = get_filter_data(e[8],e[9],e[10],value,para1,para2)
        L1[7] = packFilterUrl(e[-1],"%s/getData/?func=filter&menu_id=%s&field_id=%s"%(data_url,menu_id,e[-1]),"_refresh",e[-2])
        SL.append(L1)
    #print SL
    names = 'cname txt_show ename type sort data span url'.split()
    data = [dict(zip(names, d)) for d in SL]
    filter = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    return filter
    
def getListData(request):
    menu_id = request.POST.get('menu_id', '')
    ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    dept_id = d_value[2]
    if menu_id == '10201':
        return getInfoList(request,usr_id,dept_id)

    #print request.POST
    tab = request.POST.get('tab', '')
    data = request.POST.get('data', '')
    data_list = json.loads(data)
    multiColSearch = data_list.get('multiColSearch') or '{}'
    multiColSearch = json.loads(multiColSearch)
    #print multiColSearch
    aoData= request.POST.get('aoData', '')
    value_dict = dict()    
    sUrl = ''
    sql = " select gw_type2 from menu_data_source where menu_id=%s"%menu_id
    rows,iN = db.select(sql)
    gw_type = rows[0][0]
    value_dict['type_id'] = gw_type

    if usr_id in [1,2]:
       sql = "select mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp where  mp.menu_id=%s and mp.status=1 order by mp.sort"%menu_id
    else:
        sql = """select DISTINCT mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp 
                    left join role_menu rm on  rm.menu_id= mp.menu_id
                    left join usr_role ur on rm.role_id = ur.role_id
                    where mp.menu_id=%s and mp.status=1 and ur.usr_id = %s and FIND_IN_SET(mp.id,rm.tabs) order by sort"""%(menu_id,usr_id)
    TL,iN = db.select(sql)
    for n in range(0,len(TL)):
        if n==0 and tab=='':
            tab = TL[0][0]

    #获取当前页数据的参数
    sql = "select id,final_sql,ifnull(list_order,''),search_sql from menu_list_pages where menu_id=%s and page_name='%s'"%(menu_id,tab)
    TL,iN = db.select(sql)
    page_id = TL[0][0]
    final_sql = TL[0][1]
    list_order = TL[0][2] or ''
    search_sql = TL[0][3] or ''
 
    #获取筛选的参数
    sql = """SELECT filter_name,filter_sql,ifnull(defalut_value,'')
             FROM menu_list_filters
             where FIND_IN_SET(%s,pages) order by sort"""%(page_id)
    SL,iN = db.select(sql)
   
    #获取排序字段参数
    sql ="""SELECT col_name,field_show,IFNULL(field_order,''),is_number,is_ch
             ,IFNULL(value_sql,''),id,col_type1
             FROM menu_list_cols 
             where FIND_IN_SET(%s,pages) order by sort"""%(page_id)
    NL,iN = db.select(sql)

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
                qqid = MySQLdb.escape_string(qqid)
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_list_pages_para` where page_id=%s order by sort"%(page_id)
    para_row,iN = db.select(sql)
    sql = packPara(final_sql,para_row,value_dict,request)

    if qqid!='' and search_sql!='':
        sql+=" AND %s LIKE '%%%s%%'"%(search_sql,qqid)
    for e in multiColSearch:
        for e1 in NL:
            if e1[0] == e.get('searchItem'):
                sql+=" AND %s LIKE '%%%s%%'"%(e1[1],e.get('searchValue'))
                break
    for e in SL:
        if e[0] in data_list or e[0] in request.POST:
            if data_list.get(e[0],'') != '': 
                str1 = e[1].replace("$s",data_list.get(e[0],''))
                sql += " and (%s)"%(str1)
            elif request.POST.get(e[0], '') != '': 
                str1 = e[1].replace("$s",request.POST.get(e[0], ''))
                sql += " and (%s)"%(str1)
        elif e[2]!='':
            value = str(e[2])
            value = value.replace('{cur_usr_id}',str(usr_id))
            str1 = e[1].replace("$s",value)
            sql += " and (%s)"%(str1)

    #ORDER BY 
    if orderby!='':
        sql+=' ORDER BY %s %s' % (orderby,orderbydir)
    else:
        sql+=" %s"%list_order

    print ToGBK(sql) 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,select_size)
    value_dict = dict()
    for n in range(0,len(rows)):
        for i in range(0,len(NL)):
            addtwodimdict(value_dict,n,NL[i][0],rows[n][i])
    #print value_dict
    
    para_dict = dict()
    for e in NL:
        if e[5] !='':
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_list_cols_para` where col_id=%s order by sort"%(e[6])
            para_row,iN = db.select(sql)
            para_dict[e[0]] = para_row
        
    #print para_dict            
    L = []
    for n in range(0,len(rows)):
        L1=list(rows[n])
        for i in range(0,len(NL)):
            if NL[i][5]!='':
                sql = packPara(NL[i][5],para_row,value_dict[n],request)
                #print value_dict[n]
                #print sql
                value_row,iN = db.select(sql)
                L1[i] = value_row[0][0]
            if NL[i][7] >1: 
                if L1[i]!=0:
                    L1[i] = 1
        L.append(L1)

    #print sql
    names=[]
    for n in range(0,len(NL)):
        names.append(NL[n][0])
    data = [dict(zip(names, d)) for d in L]

    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户列表成功",
        "userList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(s3,iTotal_length,iTotal_Page,pageNo,select_size)
    #print s
    return HttpResponseCORS(request,s)

def getRoles(user_id):
    sql = "select dbo.ROLENAMELST(%s) "%user_id
    lT,iN = db.select(sql)
    roles = ""
    if len(lT)>0:
        roles = lT[0][0]
    return roles

def getAllAudit(request,pk):
    sql = """SELECT d.menu_id,ifnull(ga.url,''),ga.s_flag
              FROM gw_audit ga
              left join gw_doc d on ga.gw_id= d.id 
             where d.id =%s"""%(pk)
    rows,iN = db.select(sql)
    if iN == 0:
        s = """{
            "errcode":-1,
            "errmsg":"该条记录不存在!"
            }"""
        return HttpResponseCORS(request,s)
    menu_id = rows[0][0]
    url = rows[0][1]
    s_flag =  rows[0][2]
    if url != '':
        url = url
    else:
        if s_flag == 1:
            url = "commonDataTable.html?menu_id=%s&tab=all&mode=upd&pk=%s"%(menu_id,pk)
        else:
            url = "commonDataTable.html?menu_id=%s&tab=all&mode=audit&pk=%s"%(menu_id,pk)
    s = """{
            "errcode":1000001,
            "url":"%s"
        }"""%(url)
    return HttpResponseCORS(request,s)

def getAllSign(request,pk):
    sql = """SELECT d.menu_id,ifnull(ga.url,'')
              FROM gw_sign ga
              left join gw_doc d on ga.gw_id= d.id 
             where d.id =%s"""%(pk)
    rows,iN = db.select(sql)
    if iN == 0:
        s = """{
            "errcode":-1,
            "errmsg":"该条记录不存在!"
            }"""
        return HttpResponseCORS(request,s)
    menu_id = rows[0][0]
    url = rows[0][1]
    if url != '':
        url = url
    else:
        url = "commonDataTable.html?menu_id=%s&tab=all&mode=sign&pk=%s"%(menu_id,pk)
    s = """{
            "errcode":1000001,
            "url":"%s"
        }"""%(url)
    return HttpResponseCORS(request,s)

def getPageForm(request):
    #print request.POST
    #print getToday(7)
    



    menu_id = request.POST.get('menu_id') or request.GET.get('menu_id',0)
    mode =  request.POST.get('mode') or request.GET.get('mode','view')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = g_data.usr_id

    tab = request.POST.get('tab', '')
    step = request.POST.get('step') or request.GET.get('step','')
    print "setp=%s"%step
    if step=='':
        sql = "select ifnull(view_step,1) from menu_data_source where menu_id=%s"%(menu_id)
        rows,iN = db.select(sql)
        if iN>0 and mode not in ['add','upd']:
            step = rows[0][0]
        else:
            step = 1
    pk =  request.POST.get('pk','')
    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)
    title,menu = getTitle(menu_id,lang_id)

    if menu_id == '10201':
        return getInfoFormView(request,pk,usr_id,title,menu)
    elif menu_id == '10202':
        if mode == 'audit':
            mode = 'verify'
    elif menu_id == '109':
        return getAllAudit(request,pk)
    elif menu_id == '110':
        return getAllSign(request,pk)

    sUrl = ''
    if step in ['audit','sign','verify']:
        sql = """select md.gw_type2,md.first_flow,md.has_audit,md.has_verify,md.has_list,0,1,1,form_table,m.`menu_name`  from menu_data_source md
                left join `menu_func` m on m.menu_id = md.menu_id
                where md.menu_id=%s """%(menu_id)
    else:
        sql = """select md.gw_type2,md.first_flow,md.has_audit,md.has_verify,md.has_list,ms.has_atta,ms.has_flow,ms.has_btn,form_table,m.`menu_name` from menu_data_source md
                left join menu_form_steps ms on ms.menu_id=md.menu_id
                left join `menu_func` m on m.menu_id = md.menu_id
                where md.menu_id=%s and ms.step='%s' """%(menu_id,step)
    print sql
    rows,iN = db.select(sql)
    gw_type = rows[0][0]
    first_flow = rows[0][1]
    has_audit = rows[0][2]
    has_verify = rows[0][3]
    has_list = rows[0][4]
    has_atta = rows[0][5]
    has_flow = rows[0][6]
    has_btn = rows[0][7]
    form_table = rows[0][8].lower()
    menu_name = rows[0][9]

    if str(has_audit) == '1':
        id =  request.POST.get('id','')
        if id != '' and pk == '':
            sql = "select gw_id from %s where id=%s"%(form_table,id)
            try:
                rows,iN = db.select(sql)
                pk = rows[0][0]
            except:
                pass

        try:
            sql = "select status from gw_doc where id=%s"%(pk)
            rows,iN = db.select(sql)
            if iN == 0:
                s = """{
                    "errcode":-1,
                    "errmsg":"该条记录不存在!"
                    }"""
                return HttpResponseCORS(request,s)
            elif rows[0][0] == -1:
                s = """{
                    "errcode":-1,
                    "errmsg":"该条记录不存在!"
                    }"""
                return HttpResponseCORS(request,s)
        except:
            pass

    stepData = []
    L = []
    if mode in ['add','upd'] or str(has_audit) == '0':   
        sql = "select step,step_name from menu_form_steps where menu_id =%s and type=1 order by sort"%menu_id
        rows,iN = db.select(sql)
        for e in rows:
            L.append(list(e))
        if str(has_audit) == '1':
            L.append(['audit','申请单办理'])
    else:
        sql = "select step,step_name from menu_form_steps where menu_id =%s and type=1 order by sort"%menu_id
        rows,iN = db.select(sql)
        for e in rows:
            L1 = list(e)
            if mode =='audit':
                L1[1] += "(审核)"
            elif mode =='verify':
                L1[1] += "(登记)"
            elif mode =='sign':
                L1[1] += "(会签)"
            L.append(L1)
    names = 'step step_name'.split()
    #rows,iN = db.select(sql)
    steps = L
    data = [dict(zip(names, d)) for d in L]
    stepData = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)      
 
    formData = []
    showData = []
    gridData = []
    calData = []
    scheduleData=[]
    #获取流程记录
    L2 = []
    if mode != 'add' and str(has_audit) == '1' and has_flow == 1:
        L2 = ['']*16
        flowData = getFlowHis(pk)
        if len(flowData) >0:
            L2[0] = 'flow_his'
            L2[2] = 'flowRecord'
            L2[6] = json.dumps(flowData,ensure_ascii=False,cls=ComplexEncoder) 
    if mode != 'add' and menu_id == '10202':  #信息管理
        L2 = ['']*16
        flowData = getInfoAuditHis(pk)
        if len(flowData) >0:
            L2[0] = 'flow_his'
            L2[2] = 'flowRecord'
            L2[6] = json.dumps(flowData,ensure_ascii=False,cls=ComplexEncoder) 

    if mode in ['add','upd'] or has_list==0:
        if step == 'audit':
            formData,showData,gridData,errCode = getFlowAudit(pk,g_data.usr_id,menu_id,gw_type,stepData)
            if errCode != 0:
                s = """{
                    "errcode":-1,
                    "errmsg":"该条记录不存在或你没有权限审核此条记录!"
                    }"""
                return HttpResponseCORS(request,s)
            if mode != 'add' and str(has_audit) == '1':
                formData.insert(0,L2)
        else:
            formData,showData,gridData,calData,scheduleData = getPageDataEdit(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta)
            if mode != 'add':
                formData.append(L2)
    elif mode in ['verify']:
        formData,showData,gridData,calData = getPageDataVerifyView(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta)
        formData.append(L2)
        formData1,showData1,gridData1,calData1 = getPageDataVerify(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta)
        #print formData1
        formData.extend(formData1)
        if len(showData1)>0:
            showData.extend(showData1)
        if len(gridData1)>0:
            if len(gridData)>0:
                gridData.extend(gridData1)
            else:
                gridData = gridData1
        if len(calData1)>0:
            calData.extend(calData1)
    else:
        formData,showData,gridData,calData = getPageDataView(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta)
        #增加流程记录
        formData.append(L2)
        if mode in ['audit']: 
            sql = "select status,cur_flow_usr_id from gw_doc where id=%s"%(pk)
            rows,iN = db.select(sql)
            if iN >0 and rows[0][0] not in [6,7] and rows[0][1] == usr_id:
                formData1,showData1,gridData1,errCode  = getFlowAudit(pk,g_data.usr_id,menu_id,gw_type,stepData)
                formData.extend(formData1)
                if len(showData1)>0:
                    showData.extend(showData1)
                if len(gridData1)>0:
                    gridData.extend(gridData1)
        elif mode in ['sign']: 
            sql = "select status,cur_flow_usr_id from gw_doc where id=%s"%(pk)
            rows,iN = db.select(sql)
            if iN >0:
                formData1,showData1,gridData1,errCode  = getFlowAudit(pk,g_data.usr_id,menu_id,gw_type,stepData)
                formData.extend(formData1)
                if len(showData1)>0:
                    showData.extend(showData1)
                if len(gridData1)>0:
                    gridData.extend(gridData1)

    formData,showData,gridData,calData = getPageDataExt(pk,menu_id,usr_id,mode,request,formData,showData,gridData,calData)

    #增加默认按钮
    if has_btn ==1:
        target = request.POST.get('target','')
        sel_type = request.POST.get('sel_type','')
        if target == 'popup':
            L2 = ['']*16
            L2[0] = 'section'
            L2[2] = 'section'
            L2[1] = menu_name
            formData.insert(0,L2)
            btnData = getPopupBtn(sel_type)
        else:
            btnData = getPageBtn(menu_id,mode,step,has_btn,steps)
        formData.extend(btnData)

    lang_id =  request.POST.get('lang_id','') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)
    if m_muti_lang==1 and lang_id>1:   
        col_ids = ''     
        for e in formData:
            if len(e) == 0: continue
            col_ids += "%s,"%e[-1]
        value_dict = dict()    
        sql = "select field_id,label from muti_lang_form where lang_id=%s and FIND_IN_SET(field_id,'%s')"%(lang_id,col_ids)
        rows,iN = db.select(sql)
        for e in rows:
            value_dict[e[0]] = e[1]
        L = []
        for e in formData:
            if len(e) == 0: continue
            L1 = list(e)
            label = value_dict.get(e[-1])
            if label != '' and label != None:
                L1[1] = label
            L.append(L1)
        formData = L
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    L = [dict(zip(names, d)) for d in formData]
    #print L
    formData = json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)      

    names = 'col_name operator check_field conditional value'.split()
    L = [dict(zip(names, d)) for d in showData]
    showData = json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)      
    
    names = 'col_name has_add has_del has_order has_import import_name import_url has_import_from_file file_btn_name has_single_import single_name buttons can_edit'.split()
    L = [dict(zip(names, d)) for d in gridData]
    gridData = json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)      

    names = 'col_name on_change expression'.split()
    L = [dict(zip(names, d)) for d in calData]
    calData = json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)   

    validityData = []
    if mode  in ['add','upd']  or str(has_list) == '0':  
        sql = """SELECT mfc.col_name,v.conditional,v.check_field,v.tips,ifnull(v.para_cols,''),v.field_id
                FROM menu_form_validity v
                LEFT join menu_form_cols mfc on v.field_id = mfc.id
                LEFT JOIN menu_form_steps s on mfc.step_id=s.id 
                where s.menu_id=%s and s.step='%s'  and mfc.status = 1 and FIND_IN_SET(1,mfc.enables )
                group by mfc.id
                order by mfc.sort """%(menu_id,step)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            L1 = list(e)
            if e[4] != '':
                L1[4] = packValidityUrl(e[5],e[4])
            L.append(L1)
        names = 'col_name conditional check_field tips url'.split()
        L2 = [dict(zip(names, d)) for d in L]
        validityData = json.dumps(L2,ensure_ascii=False,cls=ComplexEncoder)      
    elif mode  in ['verify']:  
        sql = """SELECT mfc.col_name,v.conditional,v.check_field,v.tips,ifnull(v.para_cols,''),v.field_id
                FROM menu_form_validity v
                LEFT join menu_form_cols mfc on v.field_id = mfc.id
                LEFT JOIN menu_form_steps s on mfc.step_id=s.id 
                where s.menu_id=%s and s.step='%s'  and mfc.status = 1 and FIND_IN_SET(4,mfc.enables )
                group by mfc.id
                order by mfc.sort """%(menu_id,step)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            L1 = list(e)
            if e[4] != '':
                L1[4] = packValidityUrl(e[5],e[4])
            L.append(L1)
        names = 'col_name conditional check_field tips url'.split()
        L2 = [dict(zip(names, d)) for d in L]
        validityData = json.dumps(L2,ensure_ascii=False,cls=ComplexEncoder)      

    # 判断权限  # --
    # showCB
    showCB = 0
    # _formData = dict(formData,ensure_ascii=False,cls=ComplexEncoder)
    
    if pk:
        # sql = "select cid from gw_doc where id=%s and finish=%s"%(pk,0)
        # rows1 ,iN = db.select(sql)
        # if iN>0:
        sql = "select cid from gw_flow_his where m_id=%s"%(pk)
        rows2,iN_  = db.select(sql)
        # if iN_>1:
        #     rows2 = rows2[:-1]
        print(rows2)
        _d = [ _[0] for _ in rows2[:-1]]
        if d_value[0] in _d:
                showCB = 1
    
    # _frontUrl ='http://pr.sz-hongjing.com'
    url_= str('%s/common/pressCB'%(data_url)).encode('gbk').decode('gbk')
    url_ = json.dumps(str('%s/common/pressCB'%(data_url)).encode('gbk').decode('gbk'))
    # url_ = url_.replace('"','')+'/'
    url_ = url_ + '/'
    
    btn_name = "催办"
    # try:
    #     btn_name = btn_name.encode('gbk').decode('gbk')
    # except:
    #     try:
    #         btn_name = btn_name.encode('utf-8').decode('utf-8')
    #     except:
    #         pass
    extraBtnData = """[{'btn_name':'%s','url':{'href':'%s',
            'para':[{'link_field_name':'pk','para_name':'pk'},
                    {'link_field_name':'mode','para_name':'mode'},
                    {'link_field_name':'menu_id','para_name':'menu_id'}
            ]},'show_flag':%s
        }]"""%(btn_name,url_,showCB)
    if not showCB:
        extraBtnData = """''"""
 
    s = """
        {
        "errcode":0,
        "errmsg":"",
        "title":"%s",
        "menu":%s,
        "formData":%s,
        "showData":%s,
        "gridData":%s,
        "calData":%s,
        "validityData":%s,
        "stepData":%s,
        "activeStep":"%s",
        "scheduleData":%s,
        "extraBtnData":%s,

        }
        """%(title,menu,formData,showData,gridData,calData,validityData,stepData,step,scheduleData,extraBtnData)
    #print getToday(7)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getPopupBtn(sel_type):
    L = []
    L.append(['save','保存','button','','','','','','','','','','','closeModalSubmit','blue','common/savePageForm?sel_type=%s'%sel_type])
    return L

def getPageBtn(menu_id,mode,step,has_btn,steps):
    L = []
    if menu_id == '10202':  #信息管理
        if mode in ['add','upd']:
            L.append(['temp_save','暂存','button','','','','','','','','','','','temporarySave','blue','common/savePageForm?is_send=0'])
            L.append(['send','发送','button','','','','','','','','','','','submit','blue','common/savePageForm?is_send=1'])
        elif mode in ['verify']:
            L.append(['verify','审核','button','','','','','','','','','','','submit','blue','common/savePageForm?is_audit=1'])
        return L
    n = len(steps) - 1
    if mode in ['add','upd'] and str(menu_id)=='99999':
        if str(step) != str(steps[n][0]) :
            L.append(['save','暂存','button','','','','','','','','','','','temporarySave','blue','common/saveSchedule'])
            L.append(['next_step','下一步','button','','','','','','','','','','','next_step','blue','common/saveSchedule'])
        else:
            L.append(['save','暂存','button','','','','','','','','','','','temporarySave','blue','common/saveSchedule'])
            L.append(['save','保存','button','','','','','','','','','','','submit','blue','common/saveSchedule'])
        return L
    if mode in ['add','upd'] and step!='audit':
        if str(step) != str(steps[n][0]) :
            L.append(['save','暂存','button','','','','','','','','','','','temporarySave','blue','common/savePageForm'])
            L.append(['next_step','下一步','button','','','','','','','','','','','next_step','blue','common/savePageForm'])
        else:
            L.append(['save','保存','button','','','','','','','','','','','submit','blue','common/savePageForm'])
    elif mode in ['verify']:
        L.append(['verify','登记','button','','','','','','','','','','','submit','blue','common/savePageVerify'])

    return L

# 返回记录的列表
def getFlowHis(pk):
    if pk=='':
        return []
    sql = """SELECT GFH.cusrname
                    ,ifnull(date_format(send_flow_time,'%%Y-%%m-%%d %%T'),'')
                    ,
                    case GFH.status when 0 then '未办理' 
                     else 
                        case opt 
                        when 1 then '通过'
                        when 0 then '退回'
                        when 2 then '退回'
                        when 3 then '作废'
                        else '未办理'  end
                    end,
                    case GFH.status when 0 then  ''
                    else ifnull(GFH.memo,'') end, ifnull(u.pic,''),GFH.flow_name,
                    GFH.flow_id,
                    case GFH.status when 0 then '#fcb322' 
                     else 
                        case opt 
                        when 1 then 'green'
                        when 0 then 'red'
                        when 2 then 'red'
                        when 3 then 'gray'
                        else '#fcb322'  end
                    end,
                   GFH.id,D.finish
                   FROM gw_flow_his GFH
                   left join gw_doc D on GFH.m_id = D.id
                   Left join users u on GFH.cid = u.usr_id
                   WHERE GFH.m_id=%s 
                   ORDER BY GFH.id ASC
          """%pk
    #print ToGBK(sql)
    names = 'name time suggest content pic flow_name sign color'.split()
    rows,iN = db.select(sql)
    L = []
    n = 0
    for e in rows:
        L1 = list(e)
        if n == iN-1 and e[9]==1:
            L1[2] = '办理完毕'
        sql = """SELECT u.usr_name,ifnull(date_format(sign_time,'%%Y-%%m-%%d %%T'),''),                       
                     case FS.status 
                        when 1 then '同意'
                        when 2 then '不同意'
                        when 3 then '弃权'
                        else '未办理'  end,
                   ifnull(FS.memo,''),ifnull(u.pic,''),
                   case FS.status 
                        when 1 then 'green'
                        when 2 then 'red'
                        when 3 then 'gray'
                        else '#fcb322'  end,
                   fs.id
                   FROM gw_flow_sign FS
                   left join users u on u.usr_id=fs.usr_id
                   WHERE FS.m_id=%s and FS.flow_his_id = %s
                   ORDER BY FS.id DESC"""%(pk,e[-2])
        #print ToGBK(sql)
        names1 = 'name time suggest content pic color'.split()
        rows1,iN1 = db.select(sql)
        L2 = []
        for e1 in rows1:
            L21 = list(e1)
            pic = L21[4]
            if pic=='':
                L21[4] = "%s/user_pic/default.jpg"%(fs_url)
            else:
                L21[4] = "%s/user_pic/small_%s"%(fs_url,pic)
            L2.append(L21)
        L1[6] = [dict(zip(names1, d)) for d in L2]
        pic = L1[4]
        if pic=='':
            L1[4] = "%s/user_pic/default.jpg"%(fs_url)
        else:
            L1[4] = "%s/user_pic/small_%s"%(fs_url,pic)
        L.append(L1)
        n = n + 1
    data = [dict(zip(names, d)) for d in L]
    return data

def getPageGrid(menu_id,field_id,pk,value_dict,request):
    #print value_dict
    mode =  request.POST.get('mode','add')
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    cur_dept_id = request.session.get('cur_dept_id', '')
    cur_dept_name = request.session.get('cur_dept_name', '')

    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)
    if m_muti_lang==1 and lang_id>1:   
        sql ="""SELECT mfc.col_name
                  ,case ifnull(l.label,'') when '' then mfc.label else l.label end
                  ,ft.name
                  ,mfc.requireds
                  ,mfc.size
                  ,mfc.readonlys
                  ,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,ifnull(is_sum,0)
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                LEFT JOIN muti_lang_form l on l.field_id = mfc.id and l.lang_id = %s
                where mfc.parent_id=%s and mfc.status = 1
                order by mfc.sort """%(lang_id,field_id)
    else:
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name
                  ,mfc.requireds
                  ,mfc.size
                  ,mfc.readonlys
                  ,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,ifnull(is_sum,0)
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where mfc.parent_id=%s and mfc.status = 1
                order by mfc.sort """%(field_id)
    #print sql 
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url is_sum'.split()
    L=[]
    rows1,iN1 = db.select(sql)

    sql = "select final_sql,ifnull(default_sql,''),ifnull(add_sql,'') from `menu_form_grid_sql` where field_id=%s "%(field_id)
    print sql
    rows,iN = db.select(sql)  
    if iN>0:
        grid_sql = rows[0][0]
        default_sql = rows[0][1]
        add_sql = rows[0][2]
    else:
        grid_sql = ''
        default_sql = ''
        add_sql = ''
    if default_sql!='':
        sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_grid_sql_default_para` where field_id=%s order by sort"%(field_id)
        para_row,iN = db.select(sql)
        sql = packPara(default_sql,para_row,value_dict,request)
        #print ToGBK(sql)
        rows,iN = db.select(sql)
    else:
        rows=[]
    i = 0
    #print "iN=%s, len=%s"%(len(rows[0]),len(rows1))
    for e in rows1:
        L1 = list(e)
        #print "%s %s %s %s"%(e[3],e[5],e[7] ,mode)
        L1[3] = getFuncValue(e[3],mode)
        L1[5] = getFuncValue(e[5],mode)
        L1[7] = getFuncValue(e[7],mode)

        if e[18] == 1:
            L1[6] = usr_id
        elif e[18] == 2:
            L1[6] = usr_name
        elif e[18] == 3:
            L1[6] = cur_dept_id
        elif e[18] == 4:
            L1[6] = cur_dept_name
        elif e[18] == 5:
            L1[6] = getToday(6)
        elif e[18] == 6:
            L1[6] = getToday(6)
        if len(rows)>0:
            L1[6] = rows[0][i]
        para1,para2='',''
        if e[22] != '':
            para1 = value_dict.get(e[22],'')
            if e[23] == '':
                para2 = 0
            else:
                para2 = value_dict.get(e[23],'')
        single = True
        if e[17]==5:
            single = False
        if str(e[17]) == '15':  #单选弹出框
            L1[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
        elif str(e[17]) =='16':  #多选弹出框 
            L1[10] = get_mutisel_options(e[-1],e[6])
            L1[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
        elif str(e[17]) in ['3','5','6','26']:  #监听数字改变
            L1[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            if e[-3]!='':
                L1[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        elif str(e[17]) in ['32','34','35']:  #带搜素的下拉框
            L1[10] = get_options_data_search(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single,value_dict,e[-2])
            L1[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        elif str(e[17]) in ['18']:  #带分级的下拉框
            L1[10] = get_options_data_level(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            L1[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        #elif str(e[17]) == '33':  #文件上传
        #    L1[10] = packFilesUrl(e[6])
        else:
            if L1[15] != '':
                L1[15] = packFormUrl(pk,L1[-1],L1[15],L1[-4])
        
        value_dict[e[0]] = L1[6]
        L.append(L1)
        i += 1
    head_data = L
    data = [dict(zip(names, d)) for d in L]

    if str(menu_id)=='901':
        list_data = getFormGridData901(pk)
    else:
        print "pk = %s"%pk 
        if pk=='' or str(pk) == '0':
            if add_sql != '':
                default_sql = add_sql
            if default_sql!='':
                sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_grid_sql_default_para` where field_id=%s order by sort"%(field_id)
                para_row,iN = db.select(sql)
                sql = packPara(default_sql,para_row,value_dict,request)
                print ToGBK(sql)
                rows,iN = db.select(sql)
            else:
                rows=[]
        else:
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_grid_sql_para` where field_id=%s order by sort"%(field_id)
            para_row,iN = db.select(sql)
            sql = packPara(grid_sql,para_row,value_dict,request)
            print ToGBK(sql)
            if sql != '':
                rows,iN = db.select(sql)
            else: rows,iN=[],0
        L = []
        for e in rows:
            row = list(e)      
            iCount = len(row) if len(row)<iN1 else iN1
            for i in range(0,iCount):
                para1,para2='',''
                if rows1[i][22] != '':
                    para1 = value_dict.get(rows1[i][22],'')
                    if rows1[i][23] == '':
                        para2 = 0
                    else:
                        para2 = value_dict.get(rows1[i][23],'')
                value_dict[rows1[i][0]] = row[i]
                single = True
                if rows1[i][17]==5:
                    single = False
                if str(rows1[i][17]) =='16':  #多选弹出框
                    row[i] = get_mutisel_options(rows1[i][-1],row[i])
                elif str(rows1[i][17]) in ['3','5','6','26']:  #监听数字改变
                    row[i] = get_options_data(menu_id,usr_id,pk,rows1[i][19],rows1[i][20],rows1[i][21],row[i],para1,para2,single)
                elif str(rows1[i][17]) in ['32','34','35']:  #监听数字改变
                    #row[i] = get_selected_options(head_data[i][10],row[i]) 
                    #print para1,para2,rows1[i][-2]
                    row[i] = get_options_data_search(menu_id,usr_id,pk,rows1[i][19],rows1[i][20],rows1[i][21],row[i],para1,para2,single,value_dict,rows1[i][-2])
                elif str(rows1[i][17]) in ['18']:  #带分级的下拉框
                    row[i] = get_options_data_level(menu_id,usr_id,pk,rows1[i][19],rows1[i][20],rows1[i][21],row[i],para1,para2,single)
                elif str(rows1[i][17]) == '33':  #文件上传
                    row[i] = packFilesUrl(row[i])
                #else:
                #    row[i] = get_options_data(menu_id,usr_id,pk,rows1[i][19],rows1[i][20],rows1[i][21],row[i],para1,para2,single)
                if row[i] == None:
                    row[i] = ''
            L.append(row)
            
        names=[]
        for n in range(0,len(rows1)):
            names.append(rows1[n][0])
        list_data = [dict(zip(names, d)) for d in L]
    #print data
    return data,list_data

def getPageGridView(menu_id,field_id,pk,value_dict,request):
    #print value_dict
    mode =  request.POST.get('mode','view')
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    cur_dept_id = request.session.get('cur_dept_id', '')
    cur_dept_name = request.session.get('cur_dept_name', '')
    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)
    if m_muti_lang==1 and lang_id>1:   
        sql ="""SELECT mfc.col_name
                  ,case ifnull(l.label,'') when '' then mfc.label else l.label end
                  ,ft.name
                  ,0
                  ,mfc.size
                  ,1
                  ,IFNULL(mfc.default_value,'')
                  ,mfc.hide
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,ifnull(is_sum,0)
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                LEFT JOIN muti_lang_form l on l.field_id = mfc.id and l.lang_id = %s
                where mfc.parent_id=%s and FIND_IN_SET(5,mfc.enables) 
                order by mfc.sort """%(lang_id,field_id)
    else:
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name
                  ,0
                  ,mfc.size
                  ,1
                  ,IFNULL(mfc.default_value,'')
                  ,mfc.hide
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,ifnull(is_sum,0)
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where mfc.parent_id=%s and FIND_IN_SET(5,mfc.enables) 
                order by mfc.sort """%(field_id)
    #print sql
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url is_sum'.split()
    L=[]
    rows1,iN1 = db.select(sql)
    i = 0
    is_show = 1    
    for e in rows1:
        L1 = list(e)
        if e[18] == 1:
            L1[6] = usr_id
        elif e[18] == 2:
            L1[6] = usr_name
        elif e[18] == 3:
            L1[6] = cur_dept_id
        elif e[18] == 4:
            L1[6] = cur_dept_name
        elif e[18] == 5:
            L1[6] = getToday(6)
        elif e[18] == 6:
            L1[6] = getToday(6)
        para1,para2='',''
        if e[22] != '':
            para1 = value_dict.get(e[22],'')
            if e[23] == '':
                para2 = 0
            else:
                para2 = value_dict.get(e[23],'')
        single = True
        if e[17]==5:
            single = False
        if str(e[17]) =='16':  #多选弹出框
            L1[10] = get_mutisel_options(e[-1],e[6])
        elif str(e[17]) in ['5']:  
            L1[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
        elif str(e[17]) in ['3','6','18','26','32']:  
            L1[6] = get_options_data_view(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
        else:
            if L1[15] != '':
                L1[15] = packFormUrl(pk,L1[-1],L1[15],L1[-4])
        if str(e[17]) not in ['1','13','14','17','22','33']:  
            L1[2] = 'displayText'
        
        value_dict[e[0]] = L1[6]
        L.append(L1)
    data = [dict(zip(names, d)) for d in L]

    is_view = 1
    if str(menu_id)=='901':
        list_data = getFormGridData901(pk)
        #print list_data
    else:
        sql = "select ifnull(view_sql,''),final_sql from `menu_form_grid_sql` where field_id=%s "%(field_id)
        rows,iN = db.select(sql)
        if iN>0:
            grid_sql = rows[0][0]
            if grid_sql == '':
                is_view = 0
                grid_sql = rows[0][1]
            if grid_sql =='':
                is_show = 0
            else:
                sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_grid_sql_para` where field_id=%s order by sort"%(field_id)
                para_row,iN = db.select(sql)
                sql = packPara(grid_sql,para_row,value_dict,request)
                #print ToGBK(sql)
                rows,iN = db.select(sql)
                if iN == 0:
                    is_show = 0
        else:
            is_show = 0
        L = []
        for e in rows:
            row = list(e)      
            iCount = len(row) if len(row)<iN1 else iN1
            for i in range(0,iCount):
                para1,para2='',''
                if rows1[i][22] != '':
                    para1 = value_dict.get(rows1[i][22],'')
                    if rows1[i][23] == '':
                        para2 = 0
                    else:
                        para2 = value_dict.get(rows1[i][23],'')
                value_dict[rows1[i][0]] = row[i]
                single = True
                if rows1[i][17]==5:
                    single = False
                #print "i=%s row=%s"%(i,ToGBK(str(row[i])))
                if str(rows1[i][17]) in ['5','3','6','18','26','32'] and is_view==0:  
                    row[i] = get_options_data_view(menu_id,usr_id,pk,rows1[i][19],rows1[i][20],rows1[i][21],row[i],para1,para2,single)
                elif str(rows1[i][17]) =='16':  #多选弹出框
                    #print row[i]
                    row[i] = get_mutisel_options_view(rows1[i][-1],row[i])
                elif str(rows1[i][17]) == '33':  #文件上传
                    row[i] = packFilesUrl(row[i])
                #print "i=%s row=%s"%(i,ToGBK(str(row[i])))
                if row[i] == None:
                    row[i] = ''
            L.append(row)
            
        names=[]
        for n in range(0,len(rows1)):
            names.append(rows1[n][0])
        list_data = [dict(zip(names, d)) for d in L]
    return data,list_data,is_show

def getPageDataEdit(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta):
    target = request.POST.get('target', '')
    value_dict = dict()    
    value_dict['pk'] = pk
    value_dict['type_id'] = gw_type
    if pk != '':
        mode = 'upd'
    formData = []
    showData = []
    gridData = []
    calData = []
    scheduleData=[]
    if mode=='add':
        sql = """SELECT id,add_sql,ifnull(default_sql,''),ifnull(default_cols,'') FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    elif mode=='upd':
        sql = """SELECT id,update_sql,ifnull(default_sql,''),ifnull(default_cols,'') FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    else:
        sql = """SELECT id,view_sql,ifnull(default_sql,''),ifnull(default_cols,'') FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    #print sql
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
        form_sql = rows_table[0][1]
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name,mfc.requireds,mfc.size,mfc.readonlys,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,IFNULL(field_col_name,'')
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where mfc.step_id=%s and mfc.status = 1 and mfc.is_grid=0"""%(step_id)
        if mode=='add':
            sql+="""  and FIND_IN_SET(1,mfc.enables)"""
        elif mode=='upd':
            sql+="""  and FIND_IN_SET(2,mfc.enables)"""
        sql+="""     order by mfc.sort """
        names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
        rows1,iN1 = db.select(sql)
        L = []
        if pk !='' or has_list==0:
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_para` where step_id=%s order by sort"%(step_id)
            para_row,iN = db.select(sql)
            sql = packPara(form_sql,para_row,value_dict,request)           
            print ToGBK(sql)
            rows,iN = db.select(sql)
            for i in range(0,iN1):
                e = list(rows1[i])
                e[3] = getFuncValue(rows1[i][3],mode)
                e[5] = getFuncValue(rows1[i][5],mode)
                e[7] = getFuncValue(rows1[i][7],mode)
                para1 = ''
                if e[22] != '':
                    para1 = value_dict.get(e[22],'')
                para2 = ''
                if e[23] != '':
                    para2 = value_dict.get(e[23],'')
                if iN>0 and i<len(rows[0]):
                    e[6] = rows[0][i]
                    #print ToGBK(str(e[6]))
                    if e[6]=='' or e[6] == None:
                        e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
                else:
                    e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
                
                value_dict[rows1[i][0]] = e[6]
                L.append(e)
        else: 
            for i in range(0,iN1):
                e = list(rows1[i])
                e[3] = getFuncValue(rows1[i][3],mode)
                e[5] = getFuncValue(rows1[i][5],mode)
                e[7] = getFuncValue(rows1[i][7],mode)
                para1 = ''
                if e[22] != '':
                    para1 = value_dict.get(e[22],'')
                para2 = ''
                if e[23] != '':
                    para2 = value_dict.get(e[23],'')
                e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
  
                #2017-11-8 材料管理 弹出框添加时 默认为待审状态
                if target =='popup' and menu_id == '504' and e[0] == 'state':
                    e[6] = 2
                value_dict[rows1[i][0]] = e[6]
                L.append(e)

        sql = "select id,ifnull(default_sql,''),ifnull(default_cols,'') from menu_form_steps_default where step_id=%s order by sort"%(step_id)
        rows_d,iN_d = db.select(sql)
        for e_d in rows_d:
            d_id = e_d[0]
            default_sql = e_d[1]
            default_cols = e_d[2]
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_default_para` where default_id=%s order by sort"%(d_id)
            para_row,iN = db.select(sql)
            sql = packPara(default_sql,para_row,value_dict,request)
            #print ToGBK(sql)
            rows,iN = db.select(sql)
            if iN>0: 
                L2 = []
                for i in range(0,iN1):
                    e = list(L[i])
                    if default_cols != '':
                        cols = default_cols.split(',')
                        j = 0
                        for e1 in cols:
                            if e1==e[0]:
                                if e[6]=='' or e[6]==None:
                                    e[6] = rows[0][j]
                                break;
                            j += 1
                    value_dict[rows1[i][0]] = e[6]
                    L2.append(e)
                L = L2
             
        L1 = []
        for i in range(0,iN1):
            e = list(L[i])
            para1 = ''
            para2 = ''
            if e[22] != '':
                para1 = value_dict.get(e[22],'')
                if e[23] == '':
                    para2 = 0
                else:
                    para2 = value_dict.get(e[23],'')

            single = True
            if e[17]==5:
                single = False
            if str(L[i][17]) == '15':  #单选弹出框
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) =='16':  #多选弹出框
                e[10] = get_mutisel_options(e[-1],e[6])
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) in ['3','5']:  #单选、多选框
                e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                options = e[10].get('options','')
                if len(options) == 0: #选项为空是隐藏该列
                    e[2] = 'hidden'
                    e[3] = 0
                if e[-3]!='':
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) in ['6','26']:  #下拉框
                e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                if e[-3]!='':
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) in ['32','34','35']:  #带搜索下拉框
                e[10] = get_options_data_search(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single,value_dict,e[-2])
                e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) in ['18']:  #带分级的下拉框
                e[10] = get_options_data_level(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) == '24':  #表格
                if e[5] == 1:
                    e[11],e[12],is_show = getPageGridView(menu_id,e[-1],pk,value_dict,request)
                else:
                    e[11],e[12] = getPageGrid(menu_id,e[-1],pk,value_dict,request)
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) == '33':  #文件上传
                e[10] = packFilesUrl(e[6])
            elif str(L[i][17]) != '22':
                if e[15] != '':
                    e[15] = packFormUrl(pk,e[-1],e[15],e[-4])

            L1.append(e)
       
        #增加随机数参数，防止重复添加
        L2 = ['']*16
        L2[0] = 'random_no'
        L2[2] = 'hidden'
        
        random_no = "%s_%s_%s"%(usr_id,time.time(),random.randint(0,99))
        L2[6] = random_no
        L1.append(L2)
        #是否有附件
        L2 = ['']*16
        if str(has_atta)=='1':
            L2[0] = 'file_upload'
            L2[2] = 'file_upload'
            L1.append(L2)
        formData = L1
       
        sql ="""SELECT mfc.col_name,'','','','',mfr.field_id
                FROM menu_form_show mfr
                LEFT join menu_form_cols mfc on mfr.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1
                group by mfc.id
                order by mfc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            p1 = []
            p2 = []
            p3 = []
            p4 = []
            sql ="""SELECT operator,check_field,conditional,value
                FROM menu_form_show mfr
                where field_id=%s
                """%(e[5])
            L1,iN1 = db.select(sql)
            for e1 in L1:
                p1.append(e1[0])
                p2.append(e1[1])
                p3.append(e1[2])
                p4.append(e1[3])
            row[1] = p1
            row[2] = p2
            row[3] = p3
            row[4] = p4
            L.append(row)
        showData = L

        sql ="""SELECT mfc.col_name,mg.has_add,mg.has_del,mg.has_order,mg.has_import,mg.import_name,mg.import_url
                ,has_import_from_file,file_btn_name,has_single_import,single_name,'',ifnull(mg.can_edit,0),mg.field_id
                FROM menu_form_grid_setting mg
                LEFT join menu_form_cols mfc on mg.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1
                order by mfc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            row[6] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            sql1 = """SELECT gb.id,gb.btn_name,gb.btn_type,''
                FROM menu_form_grid_button gb
                LEFT join menu_form_cols mfc on gb.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1 and gb.field_id=%s
                order by mfc.sort"""%(step_id,e[-1])
            rows1,iN1 = db.select(sql1)
            L1 = []
            for e1 in rows1:
                row1 = list(e1)
                row1[3] = packButtonUrl(pk,e1[0],"%s/select/?btn_id=%s"%(data_url,e1[0]),"_window")
                L1.append(row1)     
            names = 'btn_id btn_name btn_type url'.split()
            row[11] = [dict(zip(names, d)) for d in L1] 
            L.append(row)        
        gridData = L

        sql ="""SELECT mfc.col_name,'','',mfc.id,ifnull(mc.on_change,''),ifnull(mc.expression,'')
                FROM menu_form_calculate mc
                LEFT join menu_form_cols mfc on mc.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1
                order by mc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            p1 = []
            p2 = []
            p1 = e[4].split(',')
            row[1] = p1
            row[2] = e[5]
            L.append(row)
        calData = L

        if menu_id=='99999':
            scheduleData=getScheduleData(request,step,pk)

    return formData,showData,gridData,calData,scheduleData

def getPageDataView(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta):
    value_dict = dict()    
    value_dict['pk'] = pk
    value_dict['type_id'] = gw_type

    formData = []
    showData = []
    gridData = []
    calData = []
    if mode=='audit':
        sql = """SELECT id,audit_sql,ifnull(default_sql,''),ifnull(default_cols,'') FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    elif mode=='verify':
        sql = """SELECT id,verify_sql,ifnull(default_sql,''),ifnull(default_cols,'') FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    else:
        sql = """SELECT id,view_sql,ifnull(default_sql,''),ifnull(default_cols,'') FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    #print sql
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
        form_sql = rows_table[0][1]
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name,0,mfc.size,1,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,IFNULL(mfc.hint,'')
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,IFNULL(field_col_name,'')
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where mfc.step_id=%s and mfc.status = 1 and mfc.is_grid=0"""%(step_id)
        if mode=='audit':
            sql+="""  and FIND_IN_SET(3,mfc.enables)"""
        elif mode=='verify':
            sql+="""  and FIND_IN_SET(4,mfc.enables)"""
        else:
            sql+="""  and FIND_IN_SET(5,mfc.enables)"""
        sql+="""     order by mfc.sort """
        #print sql
        rows1,iN1 = db.select(sql)
        L = []
        if pk !='' or has_list==0:
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_para` where step_id=%s order by sort"%(step_id)
            para_row,iN = db.select(sql)
            sql = packPara(form_sql,para_row,value_dict,request)
            #print sql

            rows,iN = db.select(sql)
            for i in range(0,iN1):
                e = list(rows1[i])
                e[7] = getFuncValue(rows1[i][7],mode)
                if iN>0 and i<len(rows[0]):
                    e[6] = rows[0][i]
                value_dict[rows1[i][0]] = e[6]
                if e[9] != '':
                    e[9] = packHint(e[9],value_dict)
                L.append(e)
        sql = "select id,ifnull(default_sql,''),ifnull(default_cols,'') from menu_form_steps_default where step_id=%s order by sort"%(step_id)
        rows_d,iN_d = db.select(sql)
        for e_d in rows_d:
            d_id = e_d[0]
            default_sql = e_d[1]
            default_cols = e_d[2]
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_default_para` where default_id=%s order by sort"%(d_id)
            para_row,iN = db.select(sql)
            sql = packPara(default_sql,para_row,value_dict,request)
            #print sql
            rows,iN = db.select(sql)
            if iN>0: 
                L2 = []
                for i in range(0,iN1):
                    e = list(L[i])
                    if default_cols != '':
                        cols = default_cols.split(',')
                        j = 0
                        for e1 in cols:
                            if e1==e[0]:
                                if e[6]=='' or e[6]==None:
                                    e[6] = rows[0][j]
                                break;
                            j += 1
                    value_dict[rows1[i][0]] = e[6]
                    L2.append(e)
                L = L2
      
        L1 = []
        for i in range(0,iN1):
            is_show = 1
            e = list(L[i])
            para1 = ''
            para2 = ''
            if e[22] != '':
                para1 = value_dict.get(e[22],'')
                if e[23] == '':
                    para2 = 0
                else:
                    para2 = value_dict.get(e[23],'')
            single = True
            if e[17]==5:
                single = False
            if str(L[i][17]) =='16':  #多选弹出框
                e[10] = get_mutisel_options(e[-1],e[6])
                e[6] = get_mutisel_options_view(e[-1],e[6])
            elif str(L[i][17]) in ['3','5','6','18','26','32']:  
                if e[-1] == 17:
                    e[1] = u'角色'
                elif e[-1] == 15:
                    e[1] = u'类别'
                else:
                    e[6] = get_options_data_view(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)

            elif str(L[i][17]) == '24':  #表格
                e1=L[i][0]
                e[11],e[12],is_show = getPageGridView(menu_id,e[-1],pk,value_dict,request)
            elif str(L[i][17]) == '33':  #文件上传
                e[10] = packFilesUrl(e[6])
            elif str(L[i][17]) != '22':
                if e[15] != '':
                    e[15] = packFormUrl(pk,e[-1],e[15],e[-4])
            if str(L[i][17]) not in ['1','13','14','17','24','22','33']:  
                e[2] = 'displayText'
                        
            show_sql ="""SELECT operator,check_field,conditional,value
                FROM menu_form_show mfr
                where field_id=%s"""%(e[-1])
            show_rows,iN = db.select(show_sql)
            if iN>0:
                is_show = 1
                for show_e in show_rows:
                    val1 = value_dict.get(show_e[1],'')
                    if show_e[2] == '=':
                        if str(val1) != str(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '!=':
                        if str(val1) == str(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '!=':
                        if str(val1) == str(show_e[3]):
                            is_show = 0
                    elif show_e[2] == 'in':
                        if str(show_e[3]).find(str(val1))<0:
                            is_show = 0
                    elif show_e[2] == 'not in':
                        if str(show_e[3]).find(str(val1))>0:
                            is_show = 0
                    elif show_e[2] == '>':
                        if float(val1) <= float(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '>=':
                        if float(val1) < float(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '<':
                        if float(val1) >= float(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '<=':
                        if float(val1) > float(show_e[3]):
                            is_show = 0
                    #print "%s %s %s %s"%(val1,show_e[2],show_e[3],is_show)
            if is_show ==1 : 
                L1.append(e)
        #是否有附件
        if str(has_atta)=='1':
            L2 = ['']*16
            L2[0] = 'file_upload'
            L2[2] = 'file_upload'
            L2[5] = 1
            L1.append(L2)
        formData = L1
 
        sql ="""SELECT mfc.col_name,0,0,0,0,'','',0,'',0,''
                FROM  menu_form_cols mfc
                where mfc.step_id='%s' and mfc.status = 1 and mfc.field_type =24
                order by mfc.sort """%(step_id)
        #print sql
        names = 'col_name has_add has_del has_order has_import import_name import_url'.split()
        rows,iN = db.select(sql)
        gridData = rows
    return formData,showData,gridData,calData

def getPageDataVerifyView(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta):
    value_dict = dict()    
    value_dict['pk'] = pk
    value_dict['type_id'] = gw_type

    formData = []
    showData = []
    gridData = []
    calData = []
    sql = """SELECT id,view_sql FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    #print sql
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
        form_sql = rows_table[0][1]
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name,0,mfc.size,1,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,IFNULL(field_col_name,'')
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id,FIND_IN_SET(4,mfc.enables)
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where mfc.step_id=%s and mfc.status = 1 and mfc.is_grid=0"""%(step_id)

        sql+="""  and FIND_IN_SET(5,mfc.enables)"""
        sql+="""     order by mfc.sort """
        #print sql
        rows1,iN1 = db.select(sql)
        L = []
        if pk !='' or has_list==0:
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_para` where step_id=%s order by sort"%(step_id)
            para_row,iN = db.select(sql)
            sql = packPara(form_sql,para_row,value_dict,request)
            #print sql

            rows,iN = db.select(sql)
            for i in range(0,iN1):
                e = list(rows1[i])
                e[7] = getFuncValue(rows1[i][7],mode)
                if iN>0 and i<len(rows[0]):
                    e[6] = rows[0][i]
                value_dict[rows1[i][0]] = e[6]
                L.append(e)
        sql = "select id,ifnull(default_sql,''),ifnull(default_cols,'') from menu_form_steps_default where step_id=%s order by sort"%(step_id)
        rows_d,iN_d = db.select(sql)
        for e_d in rows_d:
            d_id = e_d[0]
            default_sql = e_d[1]
            default_cols = e_d[2]
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_default_para` where default_id=%s order by sort"%(d_id)
            para_row,iN = db.select(sql)
            sql = packPara(default_sql,para_row,value_dict,request)
            #print sql
            rows,iN = db.select(sql)
            if iN>0: 
                L2 = []
                for i in range(0,iN1):
                    e = list(L[i])
                    if default_cols != '':
                        cols = default_cols.split(',')
                        j = 0
                        for e1 in cols:
                            if e1==e[0]:
                                if e[6]=='' or e[6]==None:
                                    e[6] = rows[0][j]
                                break;
                            j += 1
                    value_dict[rows1[i][0]] = e[6]
                    L2.append(e)
                L = L2             
        L1 = []
        for i in range(0,iN1):
            e = list(L[i])
            para1 = ''
            para2 = ''
            if e[22] != '':
                para1 = value_dict.get(e[22],'')
                if e[23] == '':
                    para2 = 0
                else:
                    para2 = value_dict.get(e[23],'')
            single = True
            if e[17]==5:
                single = False
            if str(L[i][17]) =='16':  #多选弹出框
                e[10] = get_mutisel_options(e[-2],e[6])
            elif str(L[i][17]) in ['3','5','6','18','26','32']:  
                e[6] = get_options_data_view(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            elif str(L[i][17]) == '24':  #表格
                e1=L[i][0]
                e[11],e[12],is_show = getPageGridView(menu_id,e[-2],pk,value_dict,request)
            elif str(L[i][17]) == '33':  #文件上传
                e[10] = packFilesUrl(e[6])
            elif str(L[i][17]) != '22':
                if e[15] != '':
                    e[15] = packFormUrl(pk,e[-2],e[15],e[-5])
            if str(L[i][17]) not in ['1','13','14','17','24','22']:  
                e[2] = 'displayText'
                        
            show_sql ="""SELECT operator,check_field,conditional,value
                FROM menu_form_show mfr
                where field_id=%s"""%(e[-2])
            show_rows,iN = db.select(show_sql)
            if iN==0:
                is_show = 1
            else:
                is_show = 1
                for show_e in show_rows:
                    val1 = value_dict.get(show_e[1],'')
                    if show_e[2] == '=':
                        if str(val1) != str(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '!=':
                        if str(val1) == str(show_e[3]):
                            is_show = 0
                    elif show_e[2] == '!=':
                        if str(val1) == str(show_e[3]):
                            is_show = 0
                    elif show_e[2] == 'in':
                        if str(show_e[3]).find(str(val1))<0:
                            is_show = 0
                    elif show_e[2] == 'not in':
                        if str(show_e[3]).find(str(val1))>0:
                            is_show = 0
                    #print "%s %s %s %s"%(val1,show_e[2],show_e[3],is_show)
            if e[-1] != 0:
                is_show = 0
            if is_show ==1 : 
                L1.append(e)
        #是否有附件
        #if str(has_atta)=='1':
        #    L2 = ['']*16
        #    L2[0] = 'file_upload'
        #    L2[2] = 'file_upload'
        #    L2[5] = 1
        #    L1.append(L2)
        formData = L1
 
        sql ="""SELECT mfc.col_name,0,0,0,0,'','',0,'',0,'',mg.field_id
                FROM menu_form_grid_setting mg
                LEFT join menu_form_cols mfc on mg.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1 and not FIND_IN_SET(4,mfc.enables)
                order by mfc.sort """%(step_id)
        #print sql
        names = 'col_name has_add has_del has_order has_import import_name import_url'.split()
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            row[6] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            L.append(row)        
        gridData = L
    return formData,showData,gridData,calData

def getPageDataVerify(pk,usr_id,menu_id,gw_type,step,mode,has_list,request,has_atta):
    value_dict = dict()    
    value_dict['pk'] = pk
    value_dict['type_id'] = gw_type

    formData = []
    showData = []
    gridData = []
    calData = []
    sql = """SELECT id,verify_sql FROM menu_form_steps where menu_id=%s and step='%s' """%(menu_id,step)
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
        form_sql = rows_table[0][1]
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name,mfc.requireds,mfc.size,mfc.readonlys,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,IFNULL(field_col_name,'')
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where mfc.step_id=%s and mfc.status = 1 and mfc.is_grid=0
                and FIND_IN_SET(4,mfc.enables)
                order by mfc.sort """%(step_id)
        #print sql
        names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
        rows1,iN1 = db.select(sql)
        L = []
        sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_para` where step_id=%s order by sort"%(step_id)
        para_row,iN = db.select(sql)
        sql = packPara(form_sql,para_row,value_dict,request)
        #print sql

        rows,iN = db.select(sql)

        for i in range(0,iN1):
            e = list(rows1[i])
            e[3] = getFuncValue(rows1[i][3],mode)
            e[5] = getFuncValue(rows1[i][5],mode)
            e[7] = getFuncValue(rows1[i][7],mode)
            para1 = ''
            if e[22] != '':
                para1 = value_dict.get(e[22],'')
            para2 = ''
            if e[23] != '':
                para2 = value_dict.get(e[23],'')
            if rows[0][i] != '' and rows[0][i] != None:
                e[6] = rows[0][i]
            else:
                e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
            value_dict[rows1[i][0]] = e[6]
            L.append(e)

        sql = "select id,ifnull(default_sql,''),ifnull(default_cols,'') from menu_form_steps_default where step_id=%s order by sort"%(step_id)
        rows_d,iN_d = db.select(sql)
        #print sql 
        for e_d in rows_d:
            d_id = e_d[0]
            default_sql = e_d[1]
            default_cols = e_d[2]
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_form_steps_default_para` where default_id=%s order by sort"%(d_id)
            para_row,iN = db.select(sql)
            sql = packPara(default_sql,para_row,value_dict,request)
            #print sql 
            rows,iN = db.select(sql)
            if iN>0: 
                L2 = []
                for i in range(0,iN1):
                    e = list(L[i])
                    if default_cols != '':
                        cols = default_cols.split(',')
                        j = 0
                        for e1 in cols:
                            if e1==e[0]:
                                if e[6]=='' or e[6]==None:
                                     e[6] = rows[0][j]
                                break;
                            j += 1
                    value_dict[rows1[i][0]] = e[6]
                    L2.append(e)
                L = L2

        L1 = []
        for i in range(0,iN1):
            e = list(L[i])
            para1 = ''
            para2 = ''
            if e[22] != '':
                para1 = value_dict.get(e[22],'')
                if e[23] == '':
                    para2 = 0
                else:
                    para2 = value_dict.get(e[23],'')
            single = True
            if e[17]==5:
                single = False
            if str(L[i][17]) == '15':  #单选弹出框
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) =='16':  #多选弹出框
                e[10] = get_mutisel_options(e[-1],e[6])
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) in ['3','5']:  #单选、多选框
                e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                options = e[10].get('options','')
                if len(options) == 0: #选项为空是隐藏该列
                    e[2] = 'hidden'
                    e[3] = 0
                if e[-3]!='':
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) in ['6','26']:  #下拉框
                e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                if e[-3]!='':
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) in ['32','34','35']:  #下拉框
                e[10] = get_options_data_search(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single,value_dict,e[-2])
                e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) in ['18']:  #带分级的下拉框
                e[10] = get_options_data_level(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(L[i][17]) == '24':  #表格
                e[11],e[12] = getPageGrid(menu_id,e[-1],pk,value_dict,request)
            elif str(L[i][17]) == '33':  #文件上传
                e[10] = packFilesUrl(e[6])
            elif str(L[i][17]) != '22':
                if e[15] != '':
                    e[15] = packFormUrl(pk,e[-1],e[15],e[-4])

            L1.append(e)
        #是否有附件
        if str(has_atta)=='1':
            L2 = ['']*16
            L2[0] = 'file_upload1'
            L2[2] = 'file_upload'
            L1.append(L2)
        formData = L1
 
        sql ="""SELECT mfc.col_name,'','','','',mfr.field_id
                FROM menu_form_show mfr
                LEFT join menu_form_cols mfc on mfr.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1 and FIND_IN_SET(4,mfc.enables)
                group by mfc.id
                order by mfc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            p1 = []
            p2 = []
            p3 = []
            p4 = []
            sql ="""SELECT operator,check_field,conditional,value
                FROM menu_form_show mfr
                where field_id=%s
                """%(e[5])
            L1,iN1 = db.select(sql)
            for e1 in L1:
                p1.append(e1[0])
                p2.append(e1[1])
                p3.append(e1[2])
                p4.append(e1[3])
            row[1] = p1
            row[2] = p2
            row[3] = p3
            row[4] = p4
            L.append(row)
        showData = L

        sql ="""SELECT mfc.col_name,mg.has_add,mg.has_del,mg.has_order,mg.has_import,mg.import_name,mg.import_url
                ,has_import_from_file,file_btn_name,has_single_import,single_name,'',ifnull(mg.can_edit,0),mg.field_id
                FROM menu_form_grid_setting mg
                LEFT join menu_form_cols mfc on mg.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1  and FIND_IN_SET(4,mfc.enables)
                order by mfc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            row[6] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            L.append(row)        
        gridData = L

        sql ="""SELECT mfc.col_name,'','',mfc.id,ifnull(mc.on_change,''),ifnull(mc.expression,'')
                FROM menu_form_calculate mc
                LEFT join menu_form_cols mfc on mc.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1 and FIND_IN_SET(4,mfc.enables)
                order by mc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        L = []
        for e in rows:
            row = list(e)
            p1 = []
            p1 = e[4].split(',')
            row[1] = p1
            row[2] = e[5]
            L.append(row)
        calData = L

    return formData,showData,gridData,calData


def getFormData(pk,field_id,menu_id,usr_id,request,lang_id):
    mode = request.GET.get('mode','view')
    value_dict = dict()    
    value_dict['pk'] = pk
    refresh_field = ''
    para_cols = ''
    is_grid = 0
    sql = "SELECT change_cols,para_cols,is_grid from menu_form_cols where id=%s"%field_id
    #print sql
    rows,iN = db.select(sql)
    if iN>0:
        refresh_field = rows[0][0]
        para_cols = rows[0][1] or ''
        is_grid = rows[0][2]

    default_sql = ''
    sql = """SELECT s.id,ifnull(s.default_sql,''),ifnull(s.default_cols,'') FROM menu_form_steps s
             left join menu_form_cols c on c.step_id=s.id
             where c.id=%s """%(field_id)
    #print sql
    rows,iN = db.select(sql)
    if iN>0:
        default_sql = rows[0][1]
        default_cols = rows[0][2]

    #print para_cols
    para_list = para_cols.split(',')
    for e in para_list:
        value_dict[e] = request.POST.get(e,'')
    if m_muti_lang==1 and lang_id>1:   
        sql ="""SELECT mfc.col_name
                  ,case ifnull(l.label,'') when '' then mfc.label else l.label end
                  ,ft.name,mfc.requireds,mfc.size,mfc.readonlys,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,IFNULL(field_col_name,'')
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                LEFT JOIN muti_lang_form l on l.field_id = mfc.id and l.lang_id = %s
                where FIND_IN_SET(mfc.id,'%s')"""%(lang_id,refresh_field)
    else:
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name,mfc.requireds,mfc.size,mfc.readonlys,IFNULL(mfc.default_value,'')
                  ,mfc.hides
                  ,IFNULL(mfc.max_length,'')
                  ,mfc.hint
                  ,''
                  ,''
                  ,'' 
                  ,btn_type
                  ,btn_color
                  ,url
                  ,IFNULL(field_col_name,'')
                  ,mfc.field_type
                  ,mfc.default_type
                  ,mfc.field_options_type
                  ,IFNULL(mfc.field_options_txt,'')
                  ,IFNULL(mfc.field_options_default,'')
                  ,IFNULL(mfc.linkfield1,'')
                  ,IFNULL(mfc.linkfield2,'')
                  ,mfc.url_target
                  ,ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,mfc.id
                FROM menu_form_cols mfc
                LEFT join field_type ft on mfc.field_type = ft.id
                where FIND_IN_SET(mfc.id,'%s')"""%(refresh_field)
    sql+="""     order by mfc.sort """
    #print sql
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    rows1,iN1 = db.select(sql)
            
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        e[3] = getFuncValue(rows1[i][3],mode)
        e[5] = getFuncValue(rows1[i][5],mode)
        e[5] = getReadonlyByRefresh(value_dict,rows1[i][-1],field_id,e[5])
        e[7] = getFuncValue(rows1[i][7],mode)
        para1 = ''
        para2 = ''
        if e[22] != '':
            para1 = request.POST.get(e[22],'')
        if e[23] != '':
            para2 = request.POST.get(e[23],'')
        single = True
        if e[17]==5:
            single = False
        if str(e[17]) == '15':  #单选弹出框
            e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
        elif str(e[17]) =='16':  #多选弹出框
            e[10] = get_mutisel_options(e[-1],e[6])
            e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
        elif str(e[17]) in ['3','5']:  
            e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
            e[6] = getDefaultByRefresh(value_dict,rows1[i][-1],field_id,e[6])
            e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            options = e[10].get('options','')
            if len(options) == 0: #选项为空是隐藏该列
                e[2] = 'hidden'
                e[3] = 0
            if e[-3]!='':
                e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        elif str(e[17]) in ['6','26']:  #监听数字改变
            e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
            e[6] = getDefaultByRefresh(value_dict,rows1[i][-1],field_id,e[6])
            e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            if e[-3]!='':
                e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        elif str(e[17]) in ['32','34','35']:  #监听数字改变
            e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
            e[6] = getDefaultByRefresh(value_dict,rows1[i][-1],field_id,e[6])
            e[10] = get_options_data_search(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single,value_dict,e[-2])
            e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        elif str(e[17]) in ['18']:  #监听数字改变
            e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
            e[6] = getDefaultByRefresh(value_dict,rows1[i][-1],field_id,e[6])
            e[10] = get_options_data_level(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
        elif str(e[17]) == '24':  #表格
            e[11],e[12] = getPageGrid(menu_id,e[-1],pk,value_dict,request)
        elif str(e[17]) == '33':  #文件上传
            e[10] = packFilesUrl(e[6])
        elif str(e[17]) in ['2']:  
            #print "%s %s "%(para1,para2)
            e[6] = getDefaultvalue(menu_id,request,rows1[i][18],rows1[i][6],para1,para2)
            e[6] = getDefaultByRefresh(value_dict,rows1[i][-1],field_id,e[6])
        L1.append(e)
        
    default_sql = ''
    sql = """SELECT s.id,ifnull(s.default_sql,''),ifnull(s.default_cols,'') FROM menu_form_steps_default s
             left join menu_form_cols c on c.step_id=s.step_id
             where c.id=%s """%(field_id)
    #print sql
    rows,iN = db.select(sql)
    for e in rows:
        d_id = e[0]
        default_sql = e[1]
        default_cols = e[2]
        sql = """select s.para_type,IFNULL(s.link_field,'') from `menu_form_steps_default_para` s 
             where s.default_id=%s order by s.sort"""%(d_id)
        #print sql
        para_row,iN = db.select(sql)
        sql = packPara(default_sql,para_row,value_dict,request)
        #print ToGBK(sql)        
        rows,iN = db.select(sql)
        if iN>0: 
            L2 = []
            for i in range(0,iN1):
                e = list(L1[i])
                if default_cols != '':
                    cols = default_cols.split(',')
                    j = 0
                    for e1 in cols:
                        if e1==e[0]:
                            #if e[6]=='' or e[6]==None:
                            e[6] = str(rows[0][j] or '')
                            break;
                        j += 1
                para1 = ''
                para2 = ''
                if e[22] != '':
                    para1 = value_dict.get(e[22],'')
                if e[23] != '':
                    para2 = value_dict.get(e[23],'')
                if str(e[17]) in ['3','5']:  
                    e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                    options = e[10].get('options','')
                    if len(options) == 0: #选项为空是隐藏该列
                        e[2] = 'hidden'
                        e[3] = 0
                    if e[-3]!='':
                        e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
                elif str(e[17]) in ['6','26']:  #监听数字改变
                    e[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                    if e[-3]!='':
                        e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
                elif str(e[17]) in ['32','34','35']:  #监听数字改变
                    e[10] = get_options_data_search(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single,value_dict,e[-2])
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
                elif str(e[17]) in ['18']:  #监听数字改变
                    e[10] = get_options_data_level(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
                elif str(e[17]) == '24':  #表格
                    e[11],e[12] = getPageGrid(menu_id,e[-1],pk,value_dict,request)
                value_dict[e[0]] = e[6]
                L2.append(e)
            L1 = L2
    data = [dict(zip(names, d)) for d in L1]
    formData = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)      
    return formData

def getDefaultByRefresh(value_dict,field_id,p_field,default_value):
    sql = "select ifnull(default_sql,'') from menu_form_cols_refesh where field_id='%s' "%(field_id)
    rows,iN = db.select(sql)
    if iN==0:
        return default_value
    sql = rows[0][0]
    if sql=='':
        return default_value
    sql1 = "select ifnull(para_cols,'') from menu_form_cols where id = '%s'"%(p_field)
    rows,iN = db.select(sql1)
    if iN>0:
        para_cols = rows[0][0]
        paras = para_cols.split(',')
        for e in paras: 
            if e =='': break
            sql = sql.replace("{%s}"%e,MySQLdb.escape_string(value_dict.get(e, '')))
    print ToGBK(sql)
    rows,iN = db.select(sql)
    if iN>0:
        return rows[0][0]
    return default_value

def getReadonlyByRefresh(value_dict,field_id,p_field,default_value):
    sql = "select ifnull(rw_sql,'') from menu_form_cols_refesh where field_id='%s' "%(field_id)
    rows,iN = db.select(sql)
    if iN==0:
        return default_value
    sql = rows[0][0]
    if sql=='':
        return default_value
    sql1 = "select ifnull(para_cols,'') from menu_form_cols where id = '%s'"%(p_field)
    rows,iN = db.select(sql1)
    if iN>0:
        para_cols = rows[0][0]
        paras = para_cols.split(',')
        for e in paras: 
            if e =='': break
            sql = sql.replace("{%s}"%e,MySQLdb.escape_string(value_dict.get(e, '')))
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    if iN>0:
        if rows[0][0] == 0:
            return 0
        else:
            return 1
    return default_value

def getFlowAudit(pk,usr_id,menu_id,gw_type,stepData):
    formData = []
    showData = []
    gridData = []    
    value_dict = dict()    
    #print usr_id
    #if usr_id == 187:usr_id = 144
    #print usr_id
    
    sql = "select cur_flow_id from gw_doc where id=%s and cur_flow_usr_id=%s"%(pk,usr_id)
    #print sql
    rows,iN = db.select(sql)
    if iN ==0:  
        sql = "select id from gw_flow_sign where m_id=%s and usr_id=%s and status = 0 "%(pk,usr_id)  #跳转会签页面
        rows,iN = db.select(sql)
        if iN>0:
            return getFlowSign(pk,usr_id,menu_id,gw_type,stepData)
        return formData,showData,gridData,-1
    cur_flow_id = rows[0][0]

    formData = getAuditData(pk,-1,'',usr_id,'','',menu_id) 

         
    return formData,showData,gridData,0

def getAuditData(pk,field_id,field_value,usr_id,next_flow,opt,menu_id):
    formData = []
    value_dict = dict()    
    if(str(pk)=='0' or str(field_id)=='0'):
        return formData
    sql = "select cur_flow_id from gw_doc where id=%s and cur_flow_usr_id=%s"%(pk,usr_id)
    #print sql
    rows,iN = db.select(sql)
    if iN ==0:  
        return formData
    cur_flow_id = rows[0][0]

    if str(field_id)=='-1':  #获取所有字段
        sql ="""SELECT mfc.col_name
                      ,mfc.label
                      ,ft.name
                      ,mfc.required
                      ,mfc.size,mfc.readonly,''
                      ,mfc.hide
                      ,IFNULL(mfc.max_length,'')
                      ,mfc.hint
                      ,''
                      ,''
                      ,'' 
                      ,btn_type
                      ,btn_color
                      ,'',mfc.id
                    FROM menu_audit_cols mfc
                    LEFT join field_type ft on mfc.field_type = ft.id
                    where type=1 
                    order by mfc.sort """
    else:
        refresh_field = ''
        sql = "SELECT refresh_field,col_name from menu_audit_cols where id=%s"%field_id
        rows,iN = db.select(sql)
        if iN>0:
            refresh_field = rows[0][0]
            value_dict[rows[0][1]] = field_value
            if next_flow!='':
                value_dict['flow_next_flow'] = next_flow
            if opt!='':
                value_dict['flow_opt'] = opt
 
        sql ="""SELECT mfc.col_name
                      ,mfc.label
                      ,ft.name
                      ,mfc.required
                      ,mfc.size,mfc.readonly,''
                      ,mfc.hide
                      ,IFNULL(mfc.max_length,'')
                      ,mfc.hint
                      ,''
                      ,''
                      ,'' 
                      ,btn_type
                      ,btn_color
                      ,'',mfc.id
                    FROM menu_audit_cols mfc
                    LEFT join field_type ft on mfc.field_type = ft.id
                    where type=1 and FIND_IN_SET(mfc.id,'%s')
                    order by mfc.sort """%refresh_field
    #print sql
    rows1,iN1 = db.select(sql)

    sql="""SELECT D.type_id
                    ,ifNULL(FH.opt,'')
                    ,'',  
                    IFNULL(FH.memo,''),'',FH.cid,FH.cusrname,DATE_FORMAT(FH.ctime,'%%Y-%%m-%%d'),''
                    ,FH.next_flow_id,FDN.usr_sel_type
                    ,FH.next_dept
                    ,FH.next_role_id,FH.next_usr_id,'',FH.sign_users,
                    IFNULL(T.CanNotZuoFei,0),IFNULL(FD.s_flag,1),FD.e_flag,FD.cname,FH.flow_id
               FROM gw_doc D
               LEFT JOIN gw_type T ON T.id = D.type_id
               LEFT JOIN gw_flow_his FH ON D.id=FH.m_id and FH.status=0
               LEFT JOIN gw_flow_def FD ON FD.id = FH.flow_id
               LEFT JOIN gw_flow_def FDN ON FDN.id = FH.next_flow_id
               LEFT JOIN roles RN ON RN.role_id = FH.next_role_id 
               WHERE  D.id=%s 
               ORDER BY FH.id  Limit 1
        """%(pk)
    #print sql
    rows,iN = db.select(sql)
    row = list(rows[0])
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        if str(field_id)=='-1':  #获取所有字段
            e[6] = row[i]
        else:
            e[6] = ''
        if e[0] == 'flow_opt': #审核方向
            options = "1,通过"
            if int(row[17])!= 1:
                options += "|0,退回"
            if int(row[16])!= 1:
                options += "|3,作废"         
            e[10] = get_options_data(menu_id,usr_id,pk,6,options,'',e[6],'','')
            e[15] = packAuditUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=1"%(data_url,menu_id,pk,e[-1]),"_refresh",e[0],'')
        elif e[0] == 'flow_apprOpinion': #常用意见
            sql = "SELECT opinion,opinion FROM appr_Opinion WHERE fl_id=%s AND (cid=%s OR pub_type=1) AND type=1 ORDER BY counts desc,utime DESC"%(cur_flow_id,usr_id)
            e[10] = get_options_data(menu_id,usr_id,pk,3,sql,'--请选择 常用办理意见--','','','')
            e[15] = packAuditUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=1"%(data_url,menu_id,pk,e[-1]),"_refresh",e[0],'')
        elif e[0] == 'flow_save_memo': #保存常用意见
            e[10] = get_options_data(menu_id,usr_id,pk,6,'1,保存至常用意见','','','','')
        elif e[0] == 'flow_memo': #办理意见
            flow_apprOpinion = value_dict.get('flow_apprOpinion','')   
            if flow_apprOpinion !='':
                 e[6] = flow_apprOpinion

        elif e[0] == 'flow_next_flow': #下一流程
            opt = value_dict.get('flow_opt','')
            e[10],e[6] = get_next_flow(e[6],pk,cur_flow_id,opt,usr_id)
            e[15] = packAuditUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=1"%(data_url,menu_id,pk,e[-1]),"_refresh",e[0],'')
        elif e[0] == 'flow_sel_type': #流程类型
            next_flow_id = value_dict.get('flow_next_flow','')
            e[6] = get_next_sel_type(next_flow_id)
        elif e[0] == 'flow_next_dept': #下一部门
            opt = value_dict.get('flow_opt','')
            next_flow_id = value_dict.get('flow_next_flow','')
            e[10],e[6],sel_type = get_next_dept(e[6],pk,next_flow_id,opt)
            e[15] = packAuditUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=1"%(data_url,menu_id,pk,e[-1]),"_refresh",e[0],'flow_next_flow')
            if str(sel_type) in ['8','9']:
                e[7] = 1 
            if str(next_flow_id) in ['-1','-2'] or str(opt)=='0':
                e[7] = 1 
        elif e[0] == 'flow_next_role': #下一角色
            opt = value_dict.get('flow_opt','')
            next_flow_id = value_dict.get('flow_next_flow','')
            e[10],e[6],sel_type = get_next_role(e[6],pk,next_flow_id,opt)
            e[15] = packAuditUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=1"%(data_url,menu_id,pk,e[-1]),"_refresh",e[0],'flow_next_flow')
            if str(sel_type) not in ['8','9']:
                e[7] = 1 
            if str(next_flow_id) in ['-1','-2']:
                e[7] = 1 
        elif e[0] == 'flow_next_usr': #下一人员
            opt = value_dict.get('flow_opt','')
            next_flow_id = value_dict.get('flow_next_flow','')
            next_dept_id = value_dict.get('flow_next_dept','')
            next_role_id = value_dict.get('flow_next_role','')
            e[10],e[6] = get_next_user(e[6],pk,next_flow_id,next_dept_id,next_role_id,opt)
            #print e[10]
            if str(next_flow_id) in ['-1','-2']:
                e[7] = 1 
        elif e[0] == 'flow_sign_usr': #会签人
            e[10] = get_mutisel_sign(e[6])
            e[15] = packFormUrl(pk,e[-1],"%s/select/?func=getSigns"%(data_url),"_window")
        elif e[0] == 'flow_btn_save': #暂存
            e[15] = "common/saveAudit?is_send=0&sign=0"
        elif e[0] == 'flow_btn_sign': #发送给会签人
            e[15] = "common/saveAudit?is_send=0&sign=1"
        elif e[0] == 'flow_next_send': #发送办理
            e[15] = "common/saveAudit?is_send=1&sign=1"
        value_dict[e[0]] = e[6]
        L1.append(e)
   
    return L1

def getFlowSign(pk,usr_id,menu_id,gw_type,stepData):
    formData = []
    showData = []
    gridData = []    
    value_dict = dict()    
    sql ="""SELECT mfc.col_name
                      ,mfc.label
                      ,ft.name
                      ,mfc.required
                      ,mfc.size,mfc.readonly,''
                      ,mfc.hide
                      ,IFNULL(mfc.max_length,'')
                      ,mfc.hint
                      ,''
                      ,''
                      ,'' 
                      ,btn_type
                      ,btn_color
                      ,'',mfc.id
                    FROM menu_audit_cols mfc
                    LEFT join field_type ft on mfc.field_type = ft.id
                    where type=2
                    order by mfc.sort """         
    rows1,iN1 = db.select(sql)

    sql="""SELECT id,ifNULL(status,''),IFNULL(memo,''),sign_users,id,flow_id,flow_his_id,''
               FROM gw_flow_sign 
               WHERE usr_id=%s and m_id=%s
               ORDER BY id DESC Limit 1
        """%(usr_id,pk)
    #print sql
    rows,iN = db.select(sql)
    row = list(rows[0])
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        e[6] = row[i]
        if e[0] == 'sign_status': 
            options = "1,<font color='green'>同意</font>|2,<font color='red'>不同意</font>|3,弃权"
            e[10] = get_options_data(menu_id,usr_id,pk,6,options,'',e[6],'','')
        elif e[0] == 'sign_users': #会签人
            e[10] = get_mutisel_sign(e[6])
            e[15] = packFormUrl(pk,e[-1],"%s/select/?func=getSigns"%data_url,"_window")
        elif e[0] == 'sign_save': #发送办理
            e[15] = "common/saveAudit?is_sign=1"
        L1.append(e)
   
    return L1,showData,gridData,0

def savePageForm(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    sel_type = request.GET.get('sel_type', '')
    sel_type = sel_type.replace('/','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)

    if menu_id == '10201':
        return saveComment(request,d_value)
    elif menu_id == '10202':
        return saveInfo(request,d_value)
    elif menu_id == '901':
        return savePageForm901(request,d_value)

    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
 
    tab = request.POST.get('tab', '')
    step = request.POST.get('step', 1)
    if step=='':
        step = 1
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    #print data_list
    pk =  data_list.get('pk','')
    random_no = data_list.get('random_no','')

    value_dict = dict()    
    list_value_dict = dict()    
    sql = """SELECT ms.id,ms.final_sql,ms.has_audit,ifnull(md.`form_table`,'')  FROM menu_form_steps ms
             left join `menu_data_source` md on md.menu_id=ms.menu_id 
             where ms.menu_id=%s and ms.step=%s """%(menu_id,step)
    #print sql
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
    else:
        step_id = 0
    has_audit = rows_table[0][2]
    main_table = rows_table[0][3].lower()

    if mode=='add' and str(has_audit)=='1':
        gw_id = ''
    elif str(has_audit)=='1':
        gw_id = pk
    else:
        gw_id = ''

    if pk != '':
        mode = 'upd'

    sql = """SELECT id,save_table,is_list,del_before_update,delete_sql,field_name
                    FROM menu_form_save_tables 
                    where is_procedure=0 and step_id=%s and status=1 and is_list = 0 order by sort"""%(step_id)
    rows_table,iN = db.select(sql)
    for e_table in rows_table:
        table_id = e_table[0]
        table_name = e_table[1].lower() or ''
        is_list = e_table[2] or 0
        del_before_update = e_table[3] or 0
        delete_sql = e_table[4] or ''
        field_name = e_table[5] or ''

        if mode =='add':
            sql = """SELECT ms.save_field_name,ms.is_identity,ms.is_number,ms.is_ch,ms.is_index,ms.is_unique,ms.default_type,IFNULL(ms.request_name,''),ms.default_value,mc.label,ms.link_table,ms.link_field,ms.is_auto_sn,ms.field_id
                    FROM menu_form_save_cols ms
                    left join `menu_form_cols`  mc on mc.id=ms.`field_id` 
                    where ms.table_id=%s and ms.is_add=1"""%(table_id)
            rows,iN = db.select(sql)
            #print sql
            if iN>0:
                #unique唯一性检查
                #print value_dict
                for e in rows:
                    col_name = e[0].lower()
                    if e[5] == 1:                       
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                        addtwodimdict(value_dict,table_name,col_name,value)
                        sql = "select 1 from %s where %s='%s' and status!=-1"%(table_name,col_name,value)
                        try:
                            rows1,iN1 = db.select(sql)
                            if iN1>0:
                                s = """
                                {
                                "errcode": -1,
                                "errmsg": "%s不能重复",
                                }
                                """%(e[9])  
                                return HttpResponseCORS(request,s)
                        except:
                            pass
                #添加数据
                sql = """insert into %s ("""%(table_name)  #添加数据
                for e in rows:
                    if e[1] == 0:                       
                        sql += "%s,"%(e[0].lower())
                sql += "random_no) values ("
                for e in rows:
                    if e[1] == 0: 
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7]) 
                        if e[12] == 1 and value=='': #自动编号
                            value = getAutoSN(menu_id,e[13],data_list,table_name,e[0].lower())
                            #print 'sn=%s'%value
                        addtwodimdict(value_dict,table_name,e[0].lower(),value)
                        if e[2] == 1:
                            sql += "%s,"%(value)
                        else:
                            sql += "'%s',"%(value)
                addtwodimdict(value_dict,table_name,'random_no',random_no)
                sql += "'%s')"%random_no
                print ToGBK(sql)
                try:
                    db.executesql(sql)
                except:
                    s = """
                        {
                        "errcode": -1,
                        "errmsg": "数据添加失败！",
                        }
                        """  
                    return HttpResponseCORS(request,s)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                id = rows[0][0]
                if gw_id =='' and str(has_audit)=='1':
                    gw_id = add_save_master(menu_id,usr_id,usr_name,dept_id,random_no)
                    sql = "update %s set gw_id = %s where id = %s"%(table_name,gw_id,id)
                    try:
                        db.executesql(sql)
                    except:
                        pass
                if pk =='':
                    if str(has_audit)=='1':
                        pk = gw_id
                    else:
                        pk = id
                cid = d_value[0]
                cusrname = d_value[1]
                ctime = getSaveDefaultValue(6)
                sql = "update %s set cid=%s,cusrname='%s',ctime='%s' where id = %s"%(table_name,cid,cusrname,ctime,id)
                db.executesql(sql)
   
                sql = """SELECT save_field_name FROM menu_form_save_cols  where is_index =1 and table_id=%s 
                      """%(table_id)
                rows,iN = db.select(sql)
                if iN>0:
                    sql = "select "
                    for e in rows:
                        sql +=" %s,"%e[0].lower()
                    sql += " 1 from %s where random_no='%s'"%(table_name,random_no)
                    rows1,iN = db.select(sql)
                    i = 0
                    for e in rows:
                        value = rows1[0][i]
                        addtwodimdict(value_dict,table_name,e[0].lower(),value)
                        i += 1   
            elif is_list == 1 and iN>0:
                if str(menu_id)=='901':
                    savePageFormList901(pk,mode,table_name,data_list,value_dict,rows,field_name,request)
                else:
                    savePageFormList(pk,mode,table_name,data_list,value_dict,rows,field_name,request,has_audit)

        elif mode =='upd':
            sql = """SELECT ms.save_field_name,ms.is_identity,ms.is_number,ms.is_ch,ms.is_index,ms.is_unique,ms.default_type,IFNULL(ms.request_name,''),ms.default_value,mc.label,ms.link_table,ms.link_field,ms.is_auto_sn,ms.field_id
                    FROM menu_form_save_cols ms
                    left join `menu_form_cols`  mc on mc.id=ms.`field_id` 
                    where ms.table_id=%s and ms.is_upd=1"""%(table_id)
            #print sql
            rows,iN = db.select(sql)
            #unique唯一性检查
            for e in rows:
                col_name = e[0].lower()
                if e[5] == 1:                       
                    value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                    addtwodimdict(value_dict,table_name,col_name,value)
                    sql = "select 1 from %s where %s='%s' and status!=-1"%(table_name,col_name,value)
                    sql_where = " and not (1=1"
                    for e1 in rows:
                        if e1[4]==1:
                            value = getSaveValue(request,e1[6],e1[2],e1[3],e1[8],e1[9],e1[10],e1[11],value_dict,data_list,e1[7])
                            addtwodimdict(value_dict,table_name,e1[0].lower(),value)
                            sql_where += " and %s=%s"%(e1[0].lower(),value)
                    sql += sql_where + ')'
                    try:
                        rows1,iN1 = db.select(sql)
                        if iN1>0:
                            s = """
                            {
                            "errcode": -1,
                            "errmsg": "%s不能重复",
                            }
                            """%(e[9])  
                            return HttpResponseCORS(request,s)
                    except:
                        pass
            if iN>0:
                sql = """update %s set """%(table_name)
                for e in rows:
                    col_name = e[0].lower()
                    if e[4]==0:
                        sql += "%s="%(e[0].lower())
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                        if e[12] == 1 and value=='': #自动编号
                            value = getAutoSN(menu_id,e[13],data_list,table_name,col_name)
                        addtwodimdict(value_dict,table_name,col_name,value)
                        if e[2] == 1:
                            sql += "%s,"%(value)
                        else:
                            sql += "'%s',"%(value)
                sql = sql[:-1]
                sql_where = " where "
                n = 0
                for e in rows:
                    col_name = e[0].lower()
                    if e[4]==1:
                        if n>0:
                            sql_where += " and"  
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                        addtwodimdict(value_dict,table_name,col_name,value)
                        sql_where += " %s=%s"%(col_name,value)
                        n = n + 1
                sql += sql_where
                print ToGBK(sql)
                try:
                    db.executesql(sql)
                except:
                    s = """
                        {
                        "errcode": -1,
                        "errmsg": "数据保存失败！",
                        }
                        """  
                    return HttpResponseCORS(request,s)
                uid = d_value[0]
                uusrname = d_value[1]
                utime = getSaveDefaultValue(6)
                sql = "update %s set uid=%s,uusrname='%s',utime='%s' %s"%(table_name,uid,uusrname,utime,sql_where)
                db.executesql(sql)


                sql = """SELECT save_field_name FROM menu_form_save_cols  where is_index =1 and table_id=%s 
                      """%(table_id)
                rows,iN = db.select(sql)
                sql = "select "
                for e in rows:
                    sql +=" %s,"%e[0].lower()
                sql += " 1 from %s %s"%(table_name,sql_where)
                #print sql
                rows1,iN = db.select(sql)
                i = 0
                if len(rows1)>0:
                    for e in rows:
                        value = rows1[0][i]
                        addtwodimdict(value_dict,table_name,e[0].lower(),value)
                        i += 1               
            
    if has_audit == 1:  #保存额外的信息到公文表
        main_data = value_dict.get(main_table)
        if main_data:
            sn = main_data.get('sn','')
            proj_id = main_data.get('proj_id') or 'NULL'
            dept_id = main_data.get('dept_id') or 'NULL'
            title = main_data.get('title','')
            gw_sql = "update gw_doc set sn='%s',proj_id=%s,form_dept_id=%s,title='%s' where id=%s"%(sn,proj_id,dept_id,title,pk)
            #print ToGBK(gw_sql)
            db.executesql(gw_sql)

    #处理明细表的保存
    sql = """SELECT id,save_table,is_list,del_before_update,delete_sql,field_name
                    FROM menu_form_save_tables 
                    where is_procedure=0 and step_id=%s and status=1 and is_list = 1 order by sort"""%(step_id)
    rows_table,iN = db.select(sql)
    for e_table in rows_table:
        table_id = e_table[0]
        table_name = e_table[1].lower() or ''
        is_list = e_table[2] or 0
        del_before_update = e_table[3] or 0
        delete_sql = e_table[4] or ''
        field_name = e_table[5] or ''
        if del_before_update == 1:  #首先删除已有数据
            sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field
                    FROM menu_form_save_cols 
                    where table_id=%s and is_del=1"""%(table_id)
            para_row,iN = db.select(sql)
            for e in para_row:
                value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                sql = delete_sql.replace('$s',str(value),1)
            #print sql
            db.executesql(sql)

        sql = """SELECT ms.save_field_name,ms.is_identity,ms.is_number,ms.is_ch,ms.is_index,ms.is_unique,ms.default_type,IFNULL(ms.request_name,''),ms.default_value,mc.label,ms.link_table,ms.link_field,ms.is_auto_sn,ms.field_id
                FROM menu_form_save_cols ms
                left join `menu_form_cols`  mc on mc.id=ms.`field_id` 
                where ms.table_id=%s """%(table_id)
        if mode =='add':
            sql += " and ms.is_add=1"
        else:
            sql += " and ms.is_upd=1"
        rows,iN = db.select(sql)
        if iN>0:
            if str(menu_id)=='901':
                savePageFormList901(pk,mode,table_name,data_list,value_dict,rows,field_name,request)
            else:
                savePageFormList(pk,mode,table_name,data_list,value_dict,rows,field_name,request,has_audit)

    #特殊功能的额外处理
    saveListData(pk,mode,value_dict,d_value,request)

    #执行额外的存储过程
    sql = """SELECT save_table,id
                    FROM menu_form_save_tables 
                    where is_procedure=1 and step_id=%s and status=1 order by sort"""%(step_id)
    rows_table,iN = db.select(sql)
    for e_table in rows_table:
        table_name = e_table[0].lower()
        table_id = e_table[1]
        sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field
                    FROM menu_form_save_cols
                    where table_id=%s """%(table_id)
        rows,iN = db.select(sql)
        #print sql
        sql = """call %s("""%(table_name)
        for e in rows:
            value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
            addtwodimdict(value_dict,table_name,e[0],value)
            if e[2] == 1:
                sql += "%s,"%(value)
            else:
                sql += "'%s',"%(value)
        sql = sql[:-1]
        sql += ")"
        #print sql
        db.executesql(sql)

    sql = "UPDATE file_pic SET gw_id='%s',random_no=-1 WHERE random_no='%s';"%(pk,random_no)
    #print sql
    db.executesql(sql)

    if str(sel_type) == '23':
        sql="""select id,ifnull(cname,''),0,'',ifnull(cname,'') from suppliers where id='%s' order by id desc
            """%pk
        L,iN=db.select(sql)

        sql = """insert into `user_options` (`usr_id`,`option_type`,`option_id`,`option_value`,`option_level`,`option_parent_id`,`option_tips`,`ctime`,`hits`)
                     values (%s,%s,'%s','%s','%s','%s','%s',now(),1)
                  """%(usr_id,sel_type,L[0][0],L[0][1],L[0][2],L[0][3],L[0][4])
        db.executesql(sql)
    elif str(sel_type) == '26':
        sql="""select id,concat(number,'/',name),0,'',concat('(型号：',ifnull(type,''),' 规格:',ifnull(size,''),')') from _m504_clgl where id='%s' order by id desc
            """%pk
        L,iN=db.select(sql)

        sql = """insert into `user_options` (`usr_id`,`option_type`,`option_id`,`option_value`,`option_level`,`option_parent_id`,`option_tips`,`ctime`,`hits`)
                     values (%s,%s,'%s','%s','%s','%s','%s',now(),1)
                  """%(usr_id,sel_type,L[0][0],L[0][1],L[0][2],L[0][3],L[0][4])
        db.executesql(sql)
    if pk=='':pk=-1
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def savePageForm901(request,d_value):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
 
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
 
    tab = request.POST.get('tab', '')
    step = request.POST.get('step', 1)
    if step=='':
        step = 1
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    #print data_list
    pk =  data_list.get('pk','')
    random_no = data_list.get('random_no','')

    value_dict = dict()    
    list_value_dict = dict()    
    sql = """SELECT id,final_sql,has_audit FROM menu_form_steps where menu_id=%s and step=%s """%(menu_id,step)
    #print sql
    rows_table,iN = db.select(sql)
    if len(rows_table)>0:
        step_id = rows_table[0][0]
    else:
        step_id = 0
    has_audit = rows_table[0][2]
    if mode=='add' and str(has_audit)=='1':
        #print 'add_save_master'
        gw_id = add_save_master(menu_id,usr_id,usr_name,dept_id,random_no)
    elif str(has_audit)=='1':
        gw_id = pk
    else:
        gw_id = 0

    sql = """SELECT id,save_table,is_list,del_before_update,delete_sql,field_name
                    FROM menu_form_save_tables 
                    where is_procedure=0 and step_id=%s and status=1 order by sort"""%(step_id)
    rows_table,iN = db.select(sql)
    for e_table in rows_table:
        table_id = e_table[0]
        table_name = e_table[1] or ''
        is_list = e_table[2] or 0
        del_before_update = e_table[3] or 0
        delete_sql = e_table[4] or ''
        field_name = e_table[5] or ''
        if del_before_update == 1:  #首先删除已有数据
            sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field
                    FROM menu_form_save_cols 
                    where table_id=%s and is_del=1"""%(table_id)
            para_row,iN = db.select(sql)
            for e in para_row:
                value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                sql = delete_sql.replace('$s',str(value),1)
            #print sql
            db.executesql(sql)

        if mode =='add':
            sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field,is_auto_sn,field_id
                    FROM menu_form_save_cols 
                    where table_id=%s and is_add=1"""%(table_id)
            rows,iN = db.select(sql)
            #print sql
            if is_list == 0  and iN>0:
                #unique唯一性检查
                #print value_dict
                for e in rows:
                    if e[5] == 1:                       
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                        addtwodimdict(value_dict,table_name,e[0],value)
                        sql = "select 1 from %s where %s='%s'"%(table_name,e[0],value)
                        rows1,iN1 = db.select(sql)
                        if len(rows1)>0:
                            s = """
                                {
                                "errcode": -1,
                                "errmsg": "%s不能重复",
                                }
                                """%(e[9])    
                            return HttpResponseCORS(request,s)

                #添加数据
                sql = """insert into %s ("""%(table_name)  #添加数据
                for e in rows:
                    if e[1] == 0:                       
                        sql += "%s,"%(e[0])
                if mode=='add' and str(has_audit)=='1':
                    sql += "gw_id,"
                sql += "random_no) values ("
                for e in rows:
                    if e[1] == 0: 
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7]) 
                        if e[12] == 1 and value=='': #自动编号
                            value = getAutoSN(menu_id,e[13],data_list,table_name,e[0])
                            #print 'sn=%s'%value
                        addtwodimdict(value_dict,table_name,e[0],value)
                        if e[2] == 1:
                            sql += "%s,"%(value)
                        else:
                            sql += "'%s',"%(value)
                addtwodimdict(value_dict,table_name,'random_no',random_no)
                if mode=='add' and str(has_audit)=='1':
                    sql += "%s,"%gw_id
                sql += "'%s')"%random_no
                #print ToGBK(sql)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                id = rows[0][0]
                if str(has_audit)=='1':
                    pk = gw_id
                else:
                    pk = id
                cid = getSaveDefaultValue(1)
                cusrname = getSaveDefaultValue(2)
                ctime = getSaveDefaultValue(6)
                sql = "update %s set cid=%s,cusrname='%s',ctime='%s' where usr_id = %s"%(table_name,cid,cusrname,ctime,id)
                db.executesql(sql)
   
                sql = """SELECT save_field_name FROM menu_form_save_cols  where is_index =1 and table_id=%s 
                      """%(table_id)
                rows,iN = db.select(sql)
                if iN>0:
                    sql = "select "
                    for e in rows:
                        sql +=" %s,"%e[0]
                    sql += " 1 from %s where random_no='%s'"%(table_name,random_no)
                    rows1,iN = db.select(sql)
                    i = 0
                    for e in rows:
                        value = rows1[0][i]
                        addtwodimdict(value_dict,table_name,e[0],value)
                        i += 1   
            elif is_list == 1 and iN>0:
                if str(menu_id)=='901':
                    savePageFormList901(pk,mode,table_name,data_list,value_dict,rows,field_name,request)

        elif mode =='upd':
            sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field,is_auto_sn,field_id
                    FROM menu_form_save_cols
                    where table_id=%s and is_upd=1"""%(table_id)
            #print sql
            rows,iN = db.select(sql)
            #unique唯一性检查
            for e in rows:
                if e[5] == 1:                       
                    value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                    addtwodimdict(value_dict,table_name,e[0],value)
                    sql = "select 1 from %s where %s='%s' "%(table_name,e[0],value)
                    sql_where = " and not (1=1"
                    for e1 in rows:
                        if e1[4]==1:
                            value = getSaveValue(request,e1[6],e1[2],e1[3],e1[8],e1[9],e1[10],e1[11],value_dict,data_list,e1[7])
                            addtwodimdict(value_dict,table_name,e1[0],value)
                            sql_where += " and %s=%s"%(e1[0],value)
                    sql += sql_where + ')'
                    rows1,iN1 = db.select(sql)
                    if iN1>0:
                        s = """
                        %s({
                        "errcode": -1,
                        "errmsg": "%s不能重复",
                        })
                        """%(callback,e[9])  
                        return HttpResponseCORS(request,s)
            
            if is_list == 0 and iN>0:
                sql = """update %s set """%(table_name)
                for e in rows:
                    if e[4]==0:
                        sql += "%s="%(e[0])
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                        if e[12] == 1 and value=='': #自动编号
                            value = getAutoSN(menu_id,e[13],data_list,table_name,e[0])
                        addtwodimdict(value_dict,table_name,e[0],value)
                        if e[2] == 1:
                            sql += "%s,"%(value)
                        else:
                            sql += "'%s',"%(value)
                sql = sql[:-1]
                sql_where = " where "
                n = 0
                for e in rows:
                    if e[4]==1:
                        if n>0:
                            sql_where += " and"  
                        #print data_list
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                        addtwodimdict(value_dict,table_name,e[0],value)
                        sql_where += " %s=%s"%(e[0],value)
                        n = n + 1
                sql += sql_where
                print ToGBK(sql)
                if n>0:
                    db.executesql(sql)
                uid = getSaveDefaultValue(1)
                uusrname = getSaveDefaultValue(2)
                utime = getSaveDefaultValue(6)
                sql = "update %s set uid=%s,uusrname='%s',utime='%s' %s"%(table_name,uid,uusrname,utime,sql_where)
                db.executesql(sql)


                sql = """SELECT save_field_name FROM menu_form_save_cols  where is_index =1 and table_id=%s 
                      """%(table_id)
                rows,iN = db.select(sql)
                sql = "select "
                for e in rows:
                    sql +=" %s,"%e[0]
                sql += " 1 from %s %s"%(table_name,sql_where)
                #print sql
                rows1,iN = db.select(sql)
                i = 0
                if len(rows1)>0:
                    for e in rows:
                        value = rows1[0][i]
                        addtwodimdict(value_dict,table_name,e[0],value)
                        i += 1               
            elif is_list == 1 and iN>0:
                if str(menu_id)=='901':
                    savePageFormList901(pk,mode,table_name,data_list,value_dict,rows,field_name,request)
            
    if has_audit == 1:  #保存额外的信息到公文表
        sn = data_list.get('sn','')
        proj_id = data_list.get('proj_id') or 'NULL'
        dept_id = data_list.get('dept_id') or 'NULL'
        title = data_list.get('title','')
        gw_sql = "update gw_doc set sn='%s',proj_id=%s,form_dept_id=%s,title='%s' where id=%s"%(sn,proj_id,dept_id,title,pk)
        db.executesql(gw_sql)

    #执行额外的存储过程
    sql = """SELECT save_table,id
                    FROM menu_form_save_tables 
                    where is_procedure=1 and step_id=%s and status=1 order by sort"""%(step_id)
    rows_table,iN = db.select(sql)
    for e_table in rows_table:
        table_name = e_table[0]
        table_id = e_table[1]
        sql = """SELECT save_field_name,is_identity,is_number,is_ch,is_index,is_unique,default_type,IFNULL(request_name,''),default_value,label,link_table,link_field
                    FROM menu_form_save_cols
                    where table_id=%s """%(table_id)
        rows,iN = db.select(sql)
        #print sql
        sql = """call %s("""%(table_name)
        for e in rows:
            value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
            addtwodimdict(value_dict,table_name,e[0],value)
            if e[2] == 1:
                sql += "%s,"%(value)
            else:
                sql += "'%s',"%(value)
        sql = sql[:-1]
        sql += ")"
        #print sql
        db.executesql(sql)
    sql = "UPDATE file_pic SET gw_id=%s,random_no=-1 WHERE random_no='%s';"%(pk,random_no)
    #print sql
    db.executesql(sql)

    
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def add_save_master(menu_id,usr_id,usr_name,dept_id,random_no):
    sql = "call insert_gw_doc(%s,%s,'%s',%s,'%s')"%(menu_id,usr_id,usr_name,dept_id,random_no)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    if iN>0:
        gw_id = rows[0][0]
    else:
        gw_id = 0
    return gw_id

def savePageFormList(pk,mode,table_name,data_list,value_dict,rows,field_name,request,has_audit):
    if field_name =='':
        return
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    list1 = data_list[field_name]

    n = 1
 
    cid = getSaveDefaultValue(1)
    cusrname = getSaveDefaultValue(2)
    ctime = getSaveDefaultValue(6)
    for e1 in list1: 
        status = e1['status']
        bNew = 0
        for e in rows:
            if e[4]==1:
                value = getSaveListValue(e[2],e[7],e1,data_list)
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
                if e[7] !='':
                    value = getSaveListValue(e[2],e[7],e1,data_list)
                else:
                    value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                if e[4] == 0: 
                    if e[2] == 1:
                        sql += "%s,"%(value)
                    else:
                        sql += '"%s",'%(value)
            sql = sql[:-1]
            sql += ')'
            print ToGBK(sql)
            try:
                db.executesql(sql)
            except:
                s = """
                        {
                        "errcode": -1,
                        "errmsg": "数据添加失败！",
                        }
                        """  
                return HttpResponseCORS(request,s)
            sql = "select last_insert_id();"
            rows2,iN2 = db.select(sql)
            id = rows2[0][0]
            try:
                if str(has_audit) == '1':
                    sql = "update %s set gw_id=%s,cid=%s,cusrname='%s',ctime='%s' where id = %s"%(table_name,pk,cid,cusrname,ctime,id)
                else:
                    sql = "update %s set m_id=%s,cid=%s,cusrname='%s',ctime='%s' where id = %s"%(table_name,pk,cid,cusrname,ctime,id)
                #print ToGBK(sql)
                db.executesql(sql)
            except:
                pass
            try:
                sql1 = "update %s set sort=%s where id = %s"%(table_name,n,id) 
                #print sql1
                db.executesql(sql1)
            except:
                sql1 = "ALTER TABLE %s ADD COLUMN `sort` INT COMMENT '排序';"%(table_name)
                db.executesql(sql1)
                sql1 = "update %s set sort=%s  where id = %s"%(table_name,n,id) 
                db.executesql(sql1)

        elif status =='deleted':  #删除行
            sql_where = " where 1=1"
            j = 0
            for e in rows:
                if e[4]==1:
                    j += 1
                    if e[7] !='':
                        value = getSaveListValue(e[2],e[7],e1,data_list)
                    else:
                        value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                    sql_where += " and %s=%s"%(e[0],value)
            if j>0:
                sql = "delete from %s %s"%(table_name,sql_where)
                db.executesql(sql)
        elif status =='exist':
            sql_where = " where 1=1"
            j = 0
            for e in rows:
                if e[4]==1:
                    j += 1
                    value = getSaveListValue(e[2],e[7],e1,data_list)
                    sql_where += " and %s=%s"%(e[0],value)
            try:
                sql1 = "update %s set sort=%s %s"%(table_name,n,sql_where) 
                db.executesql(sql1)
            except:
                sql1 = "ALTER TABLE %s ADD COLUMN `sort` INT COMMENT '排序';"%(table_name)
                db.executesql(sql1)
                sql1 = "update %s set sort=%s %s"%(table_name,n,sql_where) 
                db.executesql(sql1) 

        else:  #
            sql = """update %s set """%(table_name)
            
            for e in rows:
                if e[7] !='':
                    value = getSaveListValue(e[2],e[7],e1,data_list)
                else:
                    value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
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
                    value = getSaveListValue(e[2],e[7],e1,data_list)
                    sql_where += " and %s=%s"%(e[0],value)
            sql += sql_where
            if j>0:
                print ToGBK(sql)
                db.executesql(sql)
            try:
                sql1 = "update %s set uid=%s,uusrname='%s',utime='%s' %s"%(table_name,cid,cusrname,ctime,sql_where)
                db.executesql(sql1)
            except:
                pass
            try:
                sql1 = "update %s set sort=%s %s"%(table_name,n,sql_where) 
                db.executesql(sql1)
            except:
                sql1 = "ALTER TABLE %s ADD COLUMN `sort` INT COMMENT '排序';"%(table_name)
                db.executesql(sql1)
                sql1 = "update %s set sort=%s %s"%(table_name,n,sql_where) 
                db.executesql(sql1) 
        n = n + 1
    return

def savePageFormList901(pk,mode,table_name,data_list,value_dict,rows,field_name,request):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    if table_name=='news_right':
        n = 0
        for e in rows:
            if e[7] !='':
                list1 = data_list[field_name]
                if isinstance(list1,list):
                    n = len(list1) 
                else:
                    n = 1
    elif table_name=='usr_role':
        list1 = []
        list2 = data_list['roles']
        n = 0
        for e in list2:
            list1.append(e)
        list3 = data_list[field_name] 
        for e3 in list3: 
            #print e3
            list2 = e3['roles']
            for e in list2:
                list1.append(e)
        for e in list1:
            if isinstance(list1,list):
                n = len(list1) 
            else:
                n = 1
    for i in range(0,n):
        sql = """insert into %s ("""%(table_name)  #添加数据
        for e in rows:
            if e[1] == 0:                       
                sql += "%s,"%(e[0])
        sql += "random_no) values ("
        for e in rows:
            if e[1] == 0: 
                if e[7] !='':
                    value = list1[i]
                else:
                    #print "%s %s %s %s %s %s %s %s %s %s %s"%(e[0],e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                    value = getSaveValue(request,e[6],e[2],e[3],e[8],e[9],e[10],e[11],value_dict,data_list,e[7])
                if e[2] == 1:
                    sql += "%s,"%(value)
                else:
                    sql += "'%s',"%(value)
        random_no = "%s_%s"%(time.time(),usr_id)
        sql += "'%s')"%random_no
        #print sql
        db.executesql(sql)
    return

    '''
    menu_id = request.POST.get('menu_id', 0)
    data = request.POST.get('data','')
    data_list = json.loads(data)
    cid = getSaveDefaultValue(1)
    cusrname = getSaveDefaultValue(2)
    
    lxr = data_list.get('lxr','')
    lxr_tel = data_list.get('lxr_tel','')
    lxr_fax = data_list.get('lxr_fax','')
    sql = "select id from addr_book where sup_id='%s' and name='%s'"%(pk,lxr)
    rows,iN = db.select(sql)
    if iN==0:
        sql = "insert into addr_book (name,cotel,cofax,sup_id) values ('%s','%s','%s','%s')"%(lxr,lxr_tel,lxr_fax,pk)  
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows1,iN1 = db.select(sql)
        aid = rows1[0][0]
        sql = """insert into `addr_book_group` (`addr_group_id`,`addr_book_id`,`ctime`,`cid`,`cusrname`) 
                 values(2,%s,now(),%s,'%s');"""%(aid,cid,cusrname)
        db.executesql(sql)
    else:
        aid = rows[0][0]
        sql = "update addr_book set cotel='%s',cofax='%s' where id=%s"%(lxr_tel,lxr_fax,aid)  
        db.executesql(sql)
    sql = "update suppliers set lxid=%s where id=%s"%(aid,pk)  
    db.executesql(sql)'''

    return

def getDefaultvalue(menu_id,request,type,default,para1,para2):
    try:
        usr_id = g_data.usr_id
        usr_name = g_data.usr_name
        cur_dept_id = g_data.cur_dept_id
        cur_dept_name = g_data.cur_dept_name
        type_id = g_data.type_id
    except:
        usr_id = request.session.get('usr_id',0)
        usr_name = request.session.get('usr_name','')
        cur_dept_id = request.session.get('dept_id',0)
        cur_dept_name = request.session.get('dept_name','')
        type_id = 0
       
    value = ''  
    if type == 1:
        value = usr_id
    elif type == 2:
        value = usr_name
    elif type == 3:
        value = cur_dept_id
    elif type == 4:
        value = cur_dept_name
    elif type == 5:
        value = getToday(6)
    elif type == 6:
        value = getToday(9)
    elif type == 8:
        value = request_list[request_name]
        #多选框提交的数据是list,需要做下处理
        if is_number == 1 and isinstance(value,list):
            if len(value)>0:
                value = value[0]
    elif type == 7:
        value = default
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    elif type == 11:
        value = type_id
    #elif type == 13:  #自动编号
    #    value = getAutoSN(menu_id,default,para1,para2)
    elif type == 14:  #当前部门领导
        value,name = getLeader(usr_id)
    elif type == 15:  #当前部门领导
        id,value = getLeader(usr_id)
    return value

def getLeader(usr_id):
    sql =""" select
                    iv.auduser
                    ,ur.usr_name
                from infoaudsort_view iv
                left join users ur on ur.usr_id = iv.auduser
                where iv.usr_id = %s 
         """%(usr_id)
    rows,iN = db.select(sql)
    if iN==0:
        return '',''
    else:
        return rows[0][0],rows[0][1]

def getAutoSN(menu_id,field_id,data_list,table_name,col_name):
    if str(menu_id) == '503':
        return getAutoSN503(field_id,data_list,table_name,col_name)
    elif str(menu_id) == '504':
        return getAutoSN504(field_id,data_list,table_name,col_name)
    elif str(menu_id) == '504':
        return getAutoSN504(field_id,data_list,table_name,col_name)
    elif str(menu_id) == '18':
        return getAutoSN18(field_id,data_list,table_name,col_name)
    elif str(menu_id) == '601':
        return getAutoSN601(field_id,data_list,table_name,col_name)

    sql = "select IFNULL(mfc.default_value,''),IFNULL(mfc.linkfield1,''),IFNULL(mfc.linkfield2,'') FROM menu_form_cols mfc where id=%s"%(field_id)
    rows,iN = db.select(sql)
    if iN==0:
        return ''
    default = rows[0][0]
    type = data_list.get(rows[0][1],'')
    s_date = data_list.get(rows[0][2],'')
    if default =='':
        return ''

    d_list = default.split('|')
    if len(d_list) > 1:
        if type =='':
            return ''
        default = ''
        for e in d_list:
            e1 = e.split(',')
            if str(e1[0]) == str(type):
                default = e1[1]
                break;
    if default =='':
        return ''
    #print s_date
    if s_date =='':
        today = datetime.date.today()
    else:
        today = datetime.datetime.strptime(s_date, "%Y-%m-%d").date()
    year = today.year
    month = today.month
    day = today.day
    pos4 = 0
    pos5 = 0
    pos1 = default.find('$Y')
    if pos1 > 0:
        pos4 = pos1
        pos5 = pos1
        get_year = 1
    else:
        get_year = 0
        pos4 = 0
        pos5 = 0        
    pos2 = default.find('$m')
    if pos2 >0:
        if pos4 == 0:
           pos4 = pos2
        pos5 = pos2
        get_month = 1
    else:
        get_month = 0
    pos3 = default.find('$d')
    if pos3 >0:
        if pos4 == 0:
           pos4 = pos3
        pos5 = pos3
        get_day = 1
    else:
        get_day = 0
    if pos4==0:
        pos4 = default.find('0')
        pos5 = pos4-2
    code_type = default[:pos4]
    maxnum = default[pos5+2:]
    codeleng = len(maxnum)
    sn = code_type
    if get_year == 1:
        sn += str(year)
    if get_month == 1:
        sn += str(month).zfill(2)
    if get_day == 1:
        sn += str(day).zfill(2)
    sql = "SELECT max(%s) FROM %s WHERE %s like '%s%%'"%(col_name,table_name,col_name,sn)
    lT,iN = db.select(sql)
    if lT[0][0] is not None:
        maxnum=str(int(lT[0][0][len(sn):])+1)
    else:
        maxnum = '1'
    maxnum = maxnum.zfill(codeleng)
    sn += maxnum
    return sn

def getAutoSN601(field_id,data_list,table_name,col_name):
    xl_license = data_list.get("xl_license",'')
    sql = "select code from cert_sort where id = '%s'"%xl_license
    lT,iN = db.select(sql)
    code =  "ZZ"+lT[0][0]

    sql = "select max(sn) from _m601_zzk where sn like '%s%%'"%(code)
    lT,iN = db.select(sql)
    if lT[0][0] is not None:
        maxnum=str(int(lT[0][0][len(code):])+1)
    else:
        maxnum = '1'
    maxnum = maxnum.zfill(4)
    code += maxnum

    return code

def getAutoSN18(field_id,data_list,table_name,col_name):
    smll_type = data_list.get("smll_type",'')
    buy_time = data_list.get("buy_time",'')
    sql = "select code from fixedast_sort where id = '%s'"%smll_type
    lT,iN = db.select(sql)
    code =  lT[0][0]
    code += buy_time[2:4]

    sql = "select max(sn) from _m18_gdzc where sn like '%s%%'"%(code)
    lT,iN = db.select(sql)
    if lT[0][0] is not None:
        maxnum=str(int(lT[0][0][len(code):])+1)
    else:
        maxnum = '1'
    maxnum = maxnum.zfill(5)
    code += maxnum

    return code

def getAutoSN503(field_id,data_list,table_name,col_name):
    parent_id = data_list.get("parent_id",'')
    code =''
    if parent_id == '' or str(parent_id) == '-1':
        sql = "select ifnull(max(code),'A') from _m503_CLFL where level = 1"
        lT,iN = db.select(sql)
        if iN>0:
            letter = lT[0][0]
            if letter =='':letter='A'
            code = chr(ord(letter)+1)
        else:
            code = 'A'
    else:
        sql = "select ifnull(code,''),ifnull(level,1) from _m503_CLFL where id=%s"%parent_id
        lT,iN = db.select(sql)
        if iN>0:
            code = lT[0][0]
            level =  int(lT[0][1]) +1
            sql = "select max(code) from _m503_CLFL where code like '%s%%' and level=%s"%(code,level)
            lT,iN = db.select(sql)
            if lT[0][0] is not None:
                maxnum=str(int(lT[0][0][len(code):])+1)
            else:
                maxnum = '1'
            maxnum = maxnum.zfill(2)
            code += maxnum

    return code

def getAutoSN504(field_id,data_list,table_name,col_name):
    cllb = data_list.get("cllb",'')
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

def getSaveValue(request,type,is_number,is_ch,default_value,label,link_table,link_field,dict,request_list,request_name):
    usr_id = g_data.usr_id
    usr_name = g_data.usr_name
    cur_dept_id = g_data.cur_dept_id
    cur_dept_name = g_data.cur_dept_name
    type_id = g_data.type_id
    value = None
    if type == 1:
        value = usr_id
    elif type == 2:
        value = usr_name
    elif type == 3:
        value = cur_dept_id
    elif type == 4:
        value = cur_dept_name
    elif type == 5:
        value = getToday(6)
    elif type == 6:
        value = getToday(7)
    elif type == 7:
        value = default_value
    elif type == 8:
        value = request_list.get(request_name,'')
        #多选框提交的数据是list,需要做下处理
        value = handleMutilValue(value,is_number)
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    elif type == 10:
        value = dict[link_table.lower()][link_field.lower()]
    elif type == 11:
        value = type_id
    if is_number == 1:
        try:
            value = str(value).replace(",",'')    #去掉金额的逗号
        except:
            pass
        value = value or 'NULL' 
    else:
        value = value or '' 
        try:
            value = MySQLdb.escape_string(value)
        except:
            pass
        
    return value

def getSaveListValue(is_number,request_name,data,data_list):
    try:
        value = data[request_name]
    except:
        value = data_list.get(request_name,'')
    value = handleMutilValue(value,is_number)
    if is_number == 1:
        try:
            value = str(value).replace(",",'')    #去掉金额的逗号
        except:
            pass
        value = value or 'NULL' 
    else:
        value = value or '' 
        try:
            value = MySQLdb.escape_string(value)
        except:
            pass
        
    return value
	
def getSaveDefaultValue(type):
    try:
        usr_id = g_data.usr_id
        usr_name = g_data.usr_name
        cur_dept_id = g_data.cur_dept_id
        cur_dept_name = g_data.cur_dept_name
        type_id = g_data.type_id
    except:
        usr_id = request.session.get('usr_id',0)
        usr_name = request.session.get('usr_name','')
        cur_dept_id = request.session.get('dept_id',0)
        cur_dept_name = request.session.get('dept_name','')
        type_id = 0
    value = None
    if type == 1:
        value = usr_id
    elif type == 2:
        value = usr_name
    elif type == 3:
        value = cur_dept_id
    elif type == 4:
        value = cur_dept_name
    elif type == 5:
        value = getToday(6)
    elif type == 6:
        value = getToday(7)
        
    return value

def getListValue(request,type,link_field,dict):
    try:
        usr_id = g_data.usr_id
        usr_name = g_data.usr_name
        cur_dept_id = g_data.cur_dept_id
        cur_dept_name = g_data.cur_dept_name
        type_id = g_data.type_id
    except:
        usr_id = request.session.get('usr_id',0)
        usr_name = request.session.get('usr_name','')
        cur_dept_id = request.session.get('dept_id',0)
        cur_dept_name = request.session.get('dept_name','')

    value = None
    if type == 1:
        value = usr_id
    elif type == 2:
        value = usr_name
    elif type == 3:
        value = cur_dept_id
    elif type == 4:
        value = cur_dept_name
    elif type == 5:
        value = getToday(6)
    elif type == 6:
        value = getToday(7)
    elif type == 7:
        value = link_field
    elif type == 8:
        value = request.POST.get(link_field, '') or request.GET.get(link_field, '') or dict.get(link_field,'')
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    elif type == 10:
        value = dict.get(link_field,'')
    elif type == 11:
        value = dict.get('type_id','')
        
    return value

def actionPageForm(request):
    menu_id = request.POST.get('menu_id', 0)
    ret,errmsg,d_value = mValidateUser(request,"delete",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    dept_name = d_value[3]
    ctime = getToday(7)

    mode = request.POST.get('mode', '')
    pk = request.POST.get('pk', '')
    sql = """select ifnull(func_sql,''),ifnull(func,'') from menu_form_func 
                where menu_id=%s and ename='%s'"""%(menu_id,mode)
    #print sql
    rows,iN = db.select(sql)
    if iN>0:
        func_sql = rows[0][0]
        if func_sql != '':        
            func_sql = func_sql.replace('{usr_id}',str(usr_id))
            func_sql = func_sql.replace('{usr_name}',str(usr_name))
            func_sql = func_sql.replace('{dept_id}',str(dept_id))
            func_sql = func_sql.replace('{dept_name}',str(dept_name))
            func_sql = func_sql.replace('{ctime}',str(ctime))
            func_sql = func_sql.replace('$s',str(pk))
            #print ToGBK(func_sql)
            db.executesql(func_sql)
        
        func = rows[0][1]
        if func != '':
            from save_ext import actionExt
            actionExt(pk,d_value,request,func)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        }
        """   
    return HttpResponseCORS(request,s)

def deletePageForm(request):
    menu_id = request.POST.get('menu_id', 0)
    ret,errmsg,d_value = mValidateUser(request,"delete",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]

    tab = request.POST.get('tab', '')
    pk = request.POST.get('pk', '')
        
    sql = """select md.has_audit from menu_data_source md
                where md.menu_id=%s """%(menu_id)
    rows,iN = db.select(sql)
    has_audit = rows[0][0]   
    #删除公文
    if str(has_audit)=='1':
        sql="delete from gw_doc WHERE id=%s;"%(pk)
        record_del_log(menu_id,usr_id,usr_name,sql)
        db.executesql(sql)
        sql="delete from gw_flow_his WHERE m_id=%s;"%(pk)
        record_del_log(menu_id,usr_id,usr_name,sql)
        db.executesql(sql)
        sql="delete from gw_flow_sign WHERE m_id=%s; "%(pk)          
        record_del_log(menu_id,usr_id,usr_name,sql)
        db.executesql(sql)
        sql="delete from gw_audit WHERE gw_id=%s;"%(pk)
        db.executesql(sql)
        sql="delete from gw_sign WHERE gw_id=%s;"%(pk)
        db.executesql(sql)
        sql="delete from gw_verify WHERE gw_id=%s;"%(pk)
        db.executesql(sql)
    #删除附件
    upload_path = "/home/webroot/data/kjerp/attach_files/"
    sql="SELECT fname,YEAR(ctime),MONTH(ctime) FROM file_pic WHERE gw_id=%s and menu_id=%s"%(pk,menu_id)
    lT,iN=db.select(sql)
    for e in lT:
        L=list(lT[0])
        fname=L[0]
        ext=L[0].split('.')[-1]
        year=L[1]
        month=L[2]
        path=os.path.join(upload_path,'%s/%s'%(year,month))
        path=os.path.join(path,fname)
        try:
            os.remove(path)
        except:
            pass                        
    sql="delete FROM file_pic WHERE gw_id=%s and menu_id=%s"%(pk,menu_id)
    db.executesql(sql)

    if tab == '':
        if usr_id in [1,2]:
            sql = "select mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp where  mp.menu_id=%s and mp.status=1 order by mp.sort"%menu_id
        else:
            sql = """select DISTINCT mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp 
                    left join role_menu rm on  rm.menu_id= mp.menu_id
                    left join usr_role ur on rm.role_id = ur.role_id
                    where mp.menu_id=%s and mp.status=1 and ur.usr_id = %s and FIND_IN_SET(mp.id,rm.tabs) order by mp.sort"""%(menu_id,usr_id)
        rows,iN = db.select(sql)
        if iN>0:
            tab = rows[0][0]

    sql = """SELECT delete_sql,id  FROM menu_list_pages
                where menu_id=%s and page_name='%s'"""%(menu_id,tab)
    rows,iN = db.select(sql)
    for e in rows:
        del_sql = e[0]
        page_id = e[1]
        sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_list_pages_del_para` where page_id=%s order by sort"%(page_id)
        para_row,iN = db.select(sql)
        sql = packPara(del_sql,para_row,'',request)
        dsql_list = sql.split(';')
        for e1 in dsql_list:
            dsql = e1.lower()
            if dsql != '':
                record_del_log(menu_id,usr_id,usr_name,dsql)
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        }
        """   
    return HttpResponseCORS(request,s)

def record_del_log(menu_id,usr_id,usr_name,dsql):
    ssql = dsql.replace("delete from ","select * from ") 
    #print ssql
    rows,iN = db.select(ssql)
    str_convert = json.dumps(rows,ensure_ascii=False,cls=ComplexEncoder)
    str_convert = MySQLdb.escape_string(str_convert)
    sql = """insert into `delete_log` (`cid`,`cusrname`,`ctime`,`menu_id`,`delete_sql`,`data`)
                  values (%s,'%s',now(),%s,'%s','%s')
          """%(usr_id,usr_name,menu_id,dsql,str_convert)
    #print ToGBK(sql)
    db.executesql(sql)
    return

def getFormGridData901(pk):
    options =['',False]
    sql="""select dp.cname,'',rd.dept_id,dp.sort
                from (select dept_id from roles group by dept_id) rd
                inner join dept dp on dp.id = rd.dept_id
                where dp.parent_id != 0
                order by dp.sort
            """
    lT,iN = db.select(sql)
    L=list(lT)
    for n in range(len(L)):
        L[n]=list(L[n])
        L[n][0] = L[n][0]
        data = get_roleslist(L[n][2],'',pk)
        names = 'value label checked'.split()
        options[0] = [dict(zip(names, d)) for d in data]
        options[1] = False
        names = 'options include_other_option'.split()
        L[n][1] = dict(zip(names, options))
    names = 'table1_dept roles'.split()
    data = [dict(zip(names, d)) for d in L]
    return data

def get_filter_data(type,txt,title,default,para1,para2):
    options =['',False]
    if type==1:
        L = get_mtc_t_data(default,txt,title)
    elif type==2:
        L = get_dept_data1(default,title)
    elif type==3:
        L = get_roles_list(default,para1,title)
    elif type==4:
        L = get_menu_list(default,title)
    elif type==5:
        L = get_sql_list(default,txt,para1,para2,title)
    elif type==6:
        L = get_input_list(default,txt,title)
    else:
        return []
    #print L
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = 0
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def mUserRight(user_id,pk):
    L=[]
    if user_id =='':user_id='NULL'
    sql="""SELECT nt.id,nt.cname,IFNULL(nr.user_id,0)
                from news_type nt
                left join news_right nr on nr.user_id=%s and nr.news_id=nt.id
                WHERE nt.news_group='info'
            """%(user_id)
    lT,iN = db.select(sql)
    if len(lT)>0:
        L=list(lT)
        for n in range(len(L)):
            L[n]=list(L[n])
            L[n][1] = L[n][1]
            if pk=='':
                if str(L[n][0]) not in ('34','44'):
                    L[n][2]=1
    return L
def get_mtc_t_data1(sDF,type,title='--请选择--'):
    sql="SELECT id,txt1 FROM mtc_t WHERE type='%s'" %type
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        #print "type=%s SDF=%s e[0]=%s b=%s"%(type,sDF,str(e[0]),b)
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_roleslist(dept,sDF,pk):
    L=[]
    ldf=[]
    if not sDF is None and sDF != '':
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = int(ldf[i])
    elif pk!='':
        sql = "select role_id from usr_role where usr_id=%s"%pk
        lT,iN = db.select(sql)
        for e in lT:
            ldf.append(e[0])
    sql="""select rl.role_id,rl.role_name,''
            from roles rl
            left join dept dp on dp.id = rl.dept_id
            where dp.del_flag = 0
        """
    if dept == '':
        sql+=" and dp.parent_id = 0"
    else:
        sql+=" and dp.id=%s"%dept
        
    sql+=" order by rl.dept_id,rl.role_id"

    lT,iN = db.select(sql)
    if len(lT)>0:
        L=list(lT)
        for n in range(len(L)):
            L[n]=list(L[n])
            L[n][1] = L[n][1]
            if L[n][0] in ldf:
                L[n][2]=1
    return L

def get_dept_data1(sDF,title='--请选择--'):
    sql="SELECT id,cname,'',ifnull(ilevel,0) FROM dept where id!=1 and del_flag = 0 order by sort" 
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        iLevel = int(e[3]) - 1
        txt= "---"*iLevel +e[1]
        L.append([e[0],txt,b])
    return L

def get_menu_list(sDF,title='--请选择--'):
    sql="SELECT menu_id,menu_name FROM menu_func where menu=1 order by sort" 
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt= e[1]
        L.append([e[0],txt,b])
    return L

def get_input_list(sDF,txt,title=''):
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    #print ToGBK(txt)
    if txt=='':
        txt = "1,"
    lT = txt.split('|')
    for e in lT: 
        e1 = e.split(',')
        if sDF==str(e1[0]):b='1'
        else:b=''
        txt=e1[1]
        L.append([e1[0],txt,b])
    return L

def get_sql_list(sDF,txt,para1,para2,title='--请选择--'):
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]

    sql=txt
    if para1 != '':
        sql = sql.replace("$s",str(para1))
    if para2 != '':
        sql = sql.replace("$s",str(para2))

    #print sql
    if sql=='':
        return 
    lT,iN = db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def handleMutilValue(value,is_number):
    sTemp = ''
    if isinstance(value,list):
        if is_number == 1:
            if len(value)>0:
                sTemp = value[0] or 0
            else:
                sTemp = 0
        else:
            for e in value:
                sTemp +="%s,"%e
            sTemp = sTemp[:-1]
    else:
        sTemp = value
    return sTemp

def getParaValue(request,value_dict,key):
    try:
        usr_id = g_data.usr_id
        usr_name = g_data.usr_name
        cur_dept_id = g_data.cur_dept_id
        cur_dept_name = g_data.cur_dept_name
        type_id = g_data.type_id
    except:
        usr_id = request.session.get('usr_id',0)
        usr_name = request.session.get('usr_name','')
        cur_dept_id = request.session.get('dept_id',0)
        cur_dept_name = request.session.get('dept_name','')

    value = request.POST.get(key) or request.GET.get(key, '') or value_dict.get(key,'')
    if value =='':
        if key == 'cid':
            value = usr_id
        elif key == 'cusrname':
            value = usr_name
        elif key == 'dept_id':
            value = cur_dept_id
        elif key == 'dept_name':
            value = cur_dept_name
        elif key == 'ctime':
            value = getToday(7)
    return value
def packPara(source,paraList,value_dict,request):
    sql = source
    pos1 = sql.find("{")
    while pos1>0 :
        pos2 = sql.find("}")
        key = sql[pos1+1:pos2]
        value = getParaValue(request,value_dict,key)
        value = MySQLdb.escape_string(str(value))
        sql = sql.replace("{%s}"%key,value)
        pos1 = sql.find("{")
    for e in paraList:
        value = getListValue(request,e[0],e[1],value_dict)
        sql = sql.replace('$s',str(value),1)
    return sql

def packonChangeUrl(pk,field_id,href,target,para_cols):
    #print "field_id = %s para_cols=%s"%(field_id,para_cols)
    usr_id = g_data.usr_id
    sql = """select `field_type` ,`field_options_type`,ifnull(m.url,ifnull(c.url,'')),col_name  from `menu_form_cols` c
                left join mtc_sys m on m.id = c.field_options_type and m.type='DXSJ' 
                where c.id=%s"""%(field_id)
    #print sql
    rows,iN = db.select(sql)
    field_type = rows[0][0]
    options_type =  rows[0][1]
    add_url = rows[0][2]
    col_name = rows[0][3]
    if field_type in [32]:
        L = ['href','target','para','search_url','add_url']
        L[0] = href + "&field_type=%s&options_type=%s&usr_id=%s"%(field_type,options_type,usr_id)
        L[1] = target
        lT =[]
        if para_cols!='':
            pList = para_cols.split(',')
            for e in pList:
                L2= ['','']
                L2[0] = e
                L2[1] = e
                lT.append(L2)
        lT.append(['sel_value',col_name])
        names = 'para_name link_field'.split()
        L[2] = [dict(zip(names, d)) for d in lT]
        L[3] = "%s/getData/?func=search&field_id=%s&field_type=%s&options_type=%s&usr_id=%s"%(data_url,field_id,field_type,options_type,usr_id)
        L[4] = add_url
        names = 'href target para search_url add_url'.split()
        L1 = dict(zip(names, L))
    elif field_type in [35]:
        L = ['href','target','para','search_url','add_url']
        L[0] = href + "&field_type=%s&options_type=%s&usr_id=%s"%(field_type,options_type,usr_id)
        L[1] = target
        lT =[]
        if para_cols!='':
            pList = para_cols.split(',')
            for e in pList:
                L2= ['','']
                L2[0] = e
                L2[1] = e
                lT.append(L2)
        lT.append(['sel_value',col_name])
        names = 'para_name link_field'.split()
        L[2] = [dict(zip(names, d)) for d in lT]
        L[3] = "%s/getData/?func=search&field_id=%s&field_type=%s&options_type=%s&usr_id=%s"%(data_url,field_id,field_type,options_type,usr_id)
        names = 'href target para search_url'.split()
        L1 = dict(zip(names, L))
    else:
        L = ['href','target','para']
        L[0] = href
        L[1] = target
        lT =[]
        if para_cols!='':
            pList = para_cols.split(',')
            for e in pList:
                if e=='':
                    continue
                L2= ['','']
                L2[0] = e
                L2[1] = e
                lT.append(L2)
        names = 'para_name link_field'.split()
        L[2] = [dict(zip(names, d)) for d in lT]
        names = 'href target para'.split()
        L1 = dict(zip(names, L))
    return L1

def packAuditUrl(pk,field_id,href,target,link,link2):
    L = ['href','target','para']
    L[0] = href
    L[1] = target
    lT =[]
    L2 = ['flow_opt','']
    L2[1] = 'flow_opt'
    lT.append(L2)
    L2 = ['field_value','']
    L2[1] = link
    lT.append(L2)
    if link2!='':
        L3 = ['next_flow','']
        L3[1] = link2
        lT.append(L3)
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]
    names = 'href target para'.split()
    L1 = dict(zip(names, L))
    return L1

def packButtonUrl(pk,field_id,href,target):
    L = ['href','target','para']
    L[0] = href
    L[1] = target
    sql = "select para_name,link_field from menu_form_url_para where btn_id=%s"%field_id
    lT,iN = db.select(sql)
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]

    names = 'href target para'.split()
    L3 = dict(zip(names, L))

    return L3


def packFormUrl(pk,field_id,href,target):
    L = ['href','target','para','refresh_href','refresh_para']
    L[0] = href
    L[1] = target
    sql = "select para_name,link_field from menu_form_url_para where field_id=%s"%field_id
    lT,iN = db.select(sql)
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]

    sql = """SELECT ifnull(mfc.change_cols,'')
                  ,ifnull(mfc.para_cols,'')
                  ,s.menu_id
                FROM menu_form_cols mfc
                LEFT join menu_form_steps s on mfc.step_id = s.id
                where mfc.id = %s"""%(field_id)
    lT,iN = db.select(sql)
    if iN==0 or lT[0][0] == '':
        L[3] = ''
        L[4] = []
    else:
        L[3] = "%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=view"%(data_url,lT[0][2],pk,field_id)
        L1 =[]
        para_cols = lT[0][1]
        if para_cols!='':
            pList = para_cols.split(',')
            for e in pList:
                if e=='':
                    continue
                L2= ['','']
                L2[0] = e
                L2[1] = e
                L1.append(L2)
        names = 'para_name link_field'.split()
        L[4] = [dict(zip(names, d)) for d in L1]
    names = 'href target para refresh_href refresh_para'.split()
    L3 = dict(zip(names, L))

    return L3

def packListUrl(field_id,href,target):
    L = ['href','target','para']
    L[0] = href
    L[1] = target
    sql = "select para_name,link_field from menu_list_url_para where field_id=%s"%field_id
    lT,iN = db.select(sql)
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]
    names = 'href target para'.split()
    L1 = dict(zip(names, L))
    return L1

def packFilterUrl(field_id,href,target,para_cols):
    L = ['href','target','para']
    L[0] = href
    L[1] = target
    lT =[]
    if para_cols!='':
        pList = para_cols.split(',')
        for e in pList:
            if e=='':
                continue
            L2= ['','']
            L2[0] = e
            L2[1] = e
            lT.append(L2)
    else:
        return ''
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]
    names = 'href target para'.split()
    L1 = dict(zip(names, L))
    return L1

def packValidityUrl(field_id,para_cols):
    L = ['href','target','para']
    L[0] = "%s/getData/?func=validity&field_id=%s"%(data_url,field_id)
    L[1] = ''
    lT =[]
    if para_cols!='':
        pList = para_cols.split(',')
        for e in pList:
            if e=='':
                continue
            L2= ['','']
            L2[0] = e
            L2[1] = e
            lT.append(L2)
    else:
        return ''
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]
    names = 'href target para'.split()
    L1 = dict(zip(names, L))
    return L1

def packFilesUrl(file_ids):
    L1 = []
    fid_list = file_ids.split(',')
    for e in fid_list:
        L = ['file_id','size','name','thumbnail_url','url','delete_url']
        if e=='': continue
        sql = "select title,fname,file_size,is_pic from file_pic where id =%s"%e
        #print sql
        lT,iN=db.select(sql)
        if iN>0:
            L[0] = e   
            L[1] = lT[0][2]    
            L[2] = lT[0][0]    
            if lT[0][3] == 1: 
                L[3] = "%s/get_file/?fname=%s"%(data_url,lT[0][1])
            else:
                L[3] = ''
            L[4] = "%s/get_file/?fname=%s"%(data_url,lT[0][1])
            L[5] = "%s/del_file/?fname=%s"%(data_url,lT[0][1])
            L1.append(L)

    options =['',False]
    names = 'file_id size name thumbnail_url url delete_url'.split()
    data = [dict(zip(names, d)) for d in L1]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def packHint(hint,value_dict):
    value = hint
    for e in value_dict:
        value = value.replace('{%s}'%e,str(value_dict.get(e,'')))
    return value

def getFuncValue(values,mode):
    value = 0
    func = '5'
    if mode =='add':
        func = '1'
    elif mode =='upd':
        func = '2'
    elif mode =='audit':
        func = '3'
    elif mode =='verify':
        func = '4'
    if values ==None: values=''
    if func in values.split(','):
        value = 1

    return value

def get_mutisel_options(field_id,values):
    options =['',False]
    L = []
    sql ="""SELECT ifnull(sel_type,0),sel_cols from menu_form_cols where id=%s
         """%(field_id)
    rows,iN = db.select(sql)
    sel_type = rows[0][0]
    sel_cols = rows[0][1]
    sql ="""SELECT sel_table from menu_select_source where  sel_type=%s"""%sel_type
    rows,iN = db.select(sql)
    if iN>0:
        from_table = rows[0][0]
        from_table = from_table.replace('\n','')
        from_table = from_table.replace('\r','')
        #获取排序字段参数
        sql ="""SELECT ms.field_show from menu_select_all_cols ms
                       left join menu_form_select_cols mc on mc.sel_col_id = ms.id and mc.field_id=%s
                       where FIND_IN_SET(ms.id,'%s')
                       order by ifnull(mc.sort,999) limit 2
             """%(field_id,sel_cols)
        #print sql
        rows,iN = db.select(sql)
        col1 = rows[0][0]
        col2 = rows[1][0]
        sql = "select %s,%s %s and FIND_IN_SET(%s,'%s')"%(col1,col2,from_table,col1,values)
        #print sql
        lT,iN = db.select(sql)
        for e in lT:
            L.append([e[0],e[1],1])
    
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def get_mutisel_options_view(field_id,values):
    options =['',False]
    L = []
    value1 = ''
    sql ="""SELECT ifnull(sel_type,0),sel_cols from menu_form_cols where id=%s
         """%(field_id)
    rows,iN = db.select(sql)
    sel_type = rows[0][0]
    sel_cols = rows[0][1]
    sql ="""SELECT sel_table from menu_select_source where  sel_type=%s"""%sel_type
    rows,iN = db.select(sql)
    if iN>0:
        from_table = rows[0][0]
        from_table = from_table.replace('\n','')
        from_table = from_table.replace('\r','')
        #获取排序字段参数
        sql ="""SELECT ms.field_show from menu_select_all_cols ms
                       left join menu_form_select_cols mc on mc.sel_col_id = ms.id and mc.field_id=%s
                       where FIND_IN_SET(ms.id,'%s')
                       order by ifnull(mc.sort,999) limit 2
             """%(field_id,sel_cols)
        #print sql
        rows,iN = db.select(sql)
        col1 = rows[0][0]
        col2 = rows[1][0]
        sql = "select %s,%s %s and FIND_IN_SET(%s,'%s')"%(col1,col2,from_table,col1,values)
        #print sql
        lT,iN = db.select(sql)
        for e in lT:
            value1 += "%s,"%e[1]
        if value1 != '':
            value1 = value1[:-1]
    return value1

def get_mutisel_sign(values):
    options =['',False]
    L = []
 
    sql = "select usr_id,usr_name from users where FIND_IN_SET(usr_id,'%s')"%(values)
    lT,iN = db.select(sql)
    for e in lT:
        L.append([e[0],e[1],1])
    
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

import copy
def get_selected_options(options,value):
    newOptions = copy.deepcopy(options)
    data = newOptions['options']
    #print data
    for e in data:
        #print ToGBK(e['value']),ToGBK(value)
        if e['value'] == value:
            e['checked'] = 1
    #print data
    return newOptions
   
