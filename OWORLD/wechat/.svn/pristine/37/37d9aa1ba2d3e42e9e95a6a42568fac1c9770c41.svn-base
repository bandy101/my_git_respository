# -*- coding: utf-8 -*-
prj_name=__name__.split('.')[0]

import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
from share import db,g_data,dActiveUser,mValidateUser,ToGBK,HttpResponseCORS,encode_table_sql,ComplexEncoder,m_prjname
from share import get_sel_cols,get_gw_type_data2,get_flow_data,get_first_flow_data,get_table_field,get_roles_list
exec ('from %s.common.flow import get_next_flow'%prj_name) 
exec ('from %s.common.common import getAuditData,getFormData,getFilterData'%prj_name) 
import MySQLdb

def getData_func(request):
    audit = request.GET.get('audit', '')
    field_id = request.GET.get('field_id') or 0
    pk = request.GET.get('pk') or 0
    func = request.GET.get('func', '')
    lang_id =  request.POST.get('lang_id') or request.GET.get('lang_id','')
    if lang_id=='':lang_id=1
    else:lang_id = int(lang_id)

    if func=='refresh':
        menu_id = request.GET.get('menu_id', 0)
        ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
        if ret!=0:
            return HttpResponseCORS(request,errmsg) 
        usr_id = g_data.usr_id
        #print usr_id
        #if usr_id == 187:usr_id = 144
        #print usr_id

        if audit =='1':
            field_value = request.POST.get('field_value','')
            next_flow = request.POST.get('next_flow','')
            opt = request.POST.get('flow_opt','')
            formData = getAuditData(pk,field_id,field_value,usr_id,next_flow,opt,menu_id)
            names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
            data = [dict(zip(names, d)) for d in formData]
            formData = json.dumps(data,ensure_ascii=False)  
            s = """
                {
                "errcode":0,
                "errmsg":"",
                "formData":%s,
                }
                """%(formData)
            #print ToGBK(s)
            return HttpResponseCORS(request,s)
        else:
            #print request.POST
            #AccessToken = request.POST.get('AccessToken', '')
            #t = time.time()
            #print (int(round(t * 1000)))    #毫秒级时间戳
            #request.session['AccessToken']
            if m_prjname=='oWorld' and field_id in ['187','3368']:
                formData = getFormData187(pk,field_id,menu_id,usr_id,request)
            elif field_id in ['107','1516','112']:
                formData = getFormData107(pk,field_id,menu_id,usr_id,request)
            elif field_id in ['1518']:
                formData = getFormData1518(pk,field_id,menu_id,usr_id,request)
            elif field_id in ['2076']:
                formData = getFormData2076(pk,field_id,menu_id,usr_id,request)
            else:
                formData = getFormData(pk,field_id,menu_id,usr_id,request,lang_id)

            #添加常用选择项
            field_type = request.GET.get('field_type', '')
            options_type = request.GET.get('options_type', '')
            usr_id = request.GET.get('usr_id', '')
            sel_value = request.POST.get('sel_value','')
            if str(field_type) in ['18','32']: 
                saveSelectedOptions(field_type,options_type,usr_id,sel_value)
            s = """
                {
                "errcode":0,
                "errmsg":"",
                "formData":%s,
                }
                """%(formData)
            #print ToGBK(s)
            return HttpResponseCORS(request,s)
    elif func=='filter':
        formData = getFilterData(field_id,request)
        s = """
            {
            "errcode":0,
            "errmsg":"",
            "filter":%s,
            }
            """%(formData)
        #print ToGBK(s)
        return HttpResponseCORS(request,s)
    elif func=='search':
        field_type = request.GET.get('field_type', '')
        options_type = request.GET.get('options_type', '')
        usr_id = request.GET.get('usr_id', '')
        search = request.POST.get('search','')
        search = MySQLdb.escape_string(search)
        page_limit = request.POST.get('page_limit') or 10
        field_id = request.GET.get('field_id', '')
        formData = get_options(field_type,options_type,search,page_limit,usr_id,field_id,request)
        #t = time.time()
        #print "search %s %s %s"%(field_id,ToGBK(int(round(t * 1000))))    #毫秒级时间戳
        s = """
            {
            "errcode":0,
            "errmsg":"",
            "data":%s,
            }
            """%(formData)
        #print ToGBK(s)
        return HttpResponseCORS(request,s)
    elif func=='validity':
        field_id = request.GET.get('field_id', '')
        ret = getValidityResult(field_id,request)
        s =  """
            {
            "errcode":0,
            "errmsg":"获取有效性结果成功",
            "validity":%s,
            }
            """%(ret)
        return HttpResponseCORS(request,s)

    filed_name = request.GET.get('fname', '')
    para1,para2,para3,para4='','','',''
    if filed_name=='gw_type':
        para1 = request.POST.get('parent_id', '') or request.GET.get('parent_id', '')
    elif filed_name=='flow':
        para1 = request.POST.get('type_id', '') or request.GET.get('type_id', '')
        para2 = request.POST.get('has_flow', '') or request.GET.get('has_flow', '')
    elif filed_name=='first_flow':
        para1 = request.POST.get('type_id', '') or request.GET.get('type_id', '')
    elif filed_name=='cols':
        para1 = request.POST.get('table_name', '') or request.GET.get('table_name', '')
    elif filed_name=='sel_cols': #获取弹出框所有字段
        para1 = request.POST.get('sel_type', '')
        para2 = request.GET.get('single', '')
    elif filed_name=='roles':
        para1 = request.POST.get('dept', '') or request.GET.get('dept', '')
    elif filed_name=='next_flow':
        para1 = request.GET.get('pk', '')
        para2 = request.GET.get('flow_id', '')
        para3 = request.POST.get('opt', '')
        para4 = request.GET.get('usr_id', '')
    L1 = getData(filed_name,'',para1,para2,para3,para4)
    s1 = json.dumps(L1,ensure_ascii=False)      
    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "data":%s,
        }
        """%s1 
    #print ToGBK(s)
    return HttpResponseCORS(request,s)  

def getValidityResult(field_id,request):
    sql = "select ifnull(validity_sql,''),para_cols from menu_form_validity where field_id= '%s'"%(field_id)
    lT,iN=db.select(sql)
    if iN==0:
        return 1
    sql=lT[0][0]
    para_cols = lT[0][1]
    paras = para_cols.split(',')
    print paras
    print request.POST
    for e in paras: 
        if e =='': break
        sql = sql.replace("{%s}"%e,MySQLdb.escape_string(request.POST.get(e, '')))
    
    print ToGBK(sql)    
    lT,iN=db.select(sql)
    if iN==0:
        return 1
    return lT[0][0]

def getData(func,sDF,para1,para2='',para3='',para4=''):
    L = []
    if func=='gw_type':
        L = get_gw_type_data2(sDF,para1)
    elif func=='flow':
        L = get_flow_data(sDF,para1,para2)
    elif func=='first_flow':
        L = get_first_flow_data(sDF,para1)
    elif func=='cols':
        L = get_table_field(sDF,para1)
    elif func=='sel_cols': #获取弹出框所有字段
        L = get_sel_cols(sDF,para1,'',para2)
    elif func=='roles':
        L = get_roles_list(sDF,para1)
    elif func=='next_flow':
        L = get_next_flow(sDF,para1,para2,para3,para4)

    options =['',1]
    names = 'value label checked'.split()
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = 0
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1 


def getFormData107(pk,field_id,menu_id,usr_id,request):
    mode = request.GET.get('mode','view')
       
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
                where mfc.id = '171'"""
    sql+="""     order by mfc.sort """
    #print sql
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    rows1,iN1 = db.select(sql)
            
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        new_field = request.POST.get('new_field[]','')
        new_field = handleMutilValue(new_field,1)
        table_name = request.POST.get('table_name','')
        col_name = request.POST.get('col_name','')
        field_type = request.POST.get('field_type','')
        field_col_name = request.POST.get('field_col_name','')
        id = request.POST.get('id','')
        sql = """select t.table_ab from menu_form_tables t 
                    left join menu_form_cols c on c.step_id = t.step_id
                 where c.id = %s  and t.`table_name` = '%s'"""%(id,table_name)
        rows,iN = db.select(sql)
        if iN == 0:
            table_ab = ''
        else:
            table_ab = '%s.'%rows[0][0]
        if str(new_field) == '1':
            col = '%s%s'%(table_ab,col_name)
        else:
            col = '%s%s'%(table_ab,field_col_name)
        if field_type in ['17','22','24']:
            e[6] = ''
        else:
            e[6] = col
        L1.append(e)
    
    data = [dict(zip(names, d)) for d in L1]
    #print data
    formData = json.dumps(data,ensure_ascii=False)      
    return formData

def getFormData1518(pk,field_id,menu_id,usr_id,request):
    mode = request.GET.get('mode','view')
       
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
                where mfc.id = '1519'"""
    sql+="""     order by mfc.sort """
    #print sql
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    rows1,iN1 = db.select(sql)
            
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        table_name = request.POST.get('table_name','')
        col_name = request.POST.get('col_name','')
        field_type = request.POST.get('field_type','')
        id = request.POST.get('id','')
        menu_id = request.POST.get('menu_id','')
        field_options_type = request.POST.get('field_options_type','')
        new_field = request.POST.get('new_field[]','')
        new_field = handleMutilValue(new_field,1)
        field_col_name = request.POST.get('field_col_name','')
        #field_type = request.POST.get('field_type','')
        sql = """select t.table_ab from menu_list_tables t 
                 where t.menu_id =%s  and t.`table_name` = '%s'"""%(menu_id,table_name)
        rows,iN = db.select(sql)
        if iN == 0:
            table_ab = ''
            col = col_name
        else:
            table_ab = rows[0][0]
            col = '%s.%s'%(table_ab,col_name)
        if str(new_field) == '1':
            field_col_name = col_name

        if field_type in ['17','22','24']:
            e[6] = ''
        elif str(field_type) in ['3','5','6','18','26','32']:
            type = int(field_options_type)
            if type==1:
                pass
            elif type==2:
                pass
            elif type==3:
                pass
            elif type==4:
                pass
            elif type==5:
                pass
            elif type==6:
                pass
            elif type==7:
                pass
            elif type==10:
                pass
            elif type==8:
                pass
            elif type==9:
                pass
            elif type==11:
                pass
            elif type==12:
                pass
            elif type==13:
                pass
            elif type==14:
                pass
            elif type==15:
                pass
            elif type==16:
                pass
            elif type==17:
                pass
            elif type==18:
                pass
            elif type==19:
                pass
            elif type==20:
                pass
            elif type==21:
                tn = 'out_proj'
                tb = 'OP'
                tid = 'id'
                e[6] = "concat('(',ifnull(OP.gc_no,''),')',ifnull(OP.cname,''))"
            elif type==22:
                tn = 'contract_sg_file'
                tb = 'SG'
                tid = 'id'
                e[6] = "ifnull(SG.code,'')"    
            elif type==23:
                tn = 'suppliers'
                tb = 'su'
                tid = 'id'
                e[6] = "ifnull(su.cname,'')"    
            sql = "select id,page_name,ifnull(where_sql,'') from menu_list_pages where menu_id=%s"%(menu_id)
            rows1,iN1 = db.select(sql)
            for e1 in rows1:
                sql = "select id from menu_list_tables where page_id = %s and table_name='%s'"%(e1[0],tn)
                #print sql
                rows2,iN2 = db.select(sql)
                if iN2 == 0:
                    sql = """insert into menu_list_tables 
                                 (menu_id,page_id,join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,sort)
                                 values (%s,%s,'LEFT JOIN','%s','%s','%s','%s','%s','%s',%s)
                              """%(menu_id,e1[0],tn,tb,tid,table_name,table_ab,field_col_name,99)
                    db.executesql(sql)
                    sql = "select join_type,table_name,table_ab,index_name,link_ab,link_index,ifnull(table_sql,'') from menu_list_tables where page_id = %s  order by sort"%(e1[0])
                    #print sql
                    rows,iN = db.select(sql)
                    table_sql = encode_table_sql(rows)
                    table_sql = '%s %s'%(table_sql,e1[2])
                    sql = """update menu_list_pages set table_sql="%s" where id=%s
                          """%(table_sql,e1[0])
                    #print sql
                    db.executesql(sql)

        else:
            e[6] = col
        L1.append(e)
    
    data = [dict(zip(names, d)) for d in L1]
    #print data
    formData = json.dumps(data,ensure_ascii=False)      
    return formData

def getFormData2076(pk,field_id,menu_id,usr_id,request):
    mode = request.GET.get('mode','view')
    sql = "SELECT change_cols,para_cols,is_grid from menu_form_cols where id=%s"%field_id
    rows,iN = db.select(sql)
    if iN>0:
        refresh_field = rows[0][0]
        para_cols = rows[0][1] or ''
        is_grid = rows[0][2]
    sql = "SELECT form_table,has_audit from menu_data_source where menu_id=%s"%pk
    rows,iN = db.select(sql)
    if iN>0:
        form_table = rows[0][0].lower()
        has_audit = rows[0][1] or 0
       
    sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name,mfc.required,mfc.size,mfc.readonly,IFNULL(mfc.default_value,'')
                  ,mfc.hide
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
                where mfc.id in (2073,2079)"""
    sql+="""     order by mfc.sort """
    #print sql
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    rows1,iN1 = db.select(sql)
    #print request.POST
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        is_new = request.POST.get('is_new[]','')
        if e[-1] == 2079 and str(is_new) == '1':
            e[6] = form_table + "_list"
        if e[-1] == 2073 and str(is_new) == '1':
            if has_audit == 1:
                link = 'gw_id'
            else:
                link = 'm_id'
            e[6] = "select id from %s_list where %s = {pk}"%(form_table,link)
        L1.append(e)
    
    data = [dict(zip(names, d)) for d in L1]
    #print data
    formData = json.dumps(data,ensure_ascii=False)      
    return formData

def saveSelectedOptions(field_type,options_type,usr_id,sel_value):
    type = int(options_type)
    iN = 0
    if type ==21:
        L,iN = get_proj_info_selected(sel_value)
    elif type==23:   #供应商
        L,iN = get_sup_info_selected(sel_value)
    #elif type==24:   #人员
    #    L,iN = get_addr_book_selected(sel_value)
    elif type ==26:
        L,iN = get_mat_info_selected(sel_value)
    if iN > 0:
        sql = "select id from user_options where usr_id=%s and option_type=%s and option_id=%s"%(usr_id,options_type,sel_value)  
        lT,iN1 = db.select(sql)
        if iN1>0 :
            sql = "update user_options set ctime=now(), hits = hits +1 where id=%s"%(lT[0][0])
        else:
            sql = """insert into `user_options` (`usr_id`,`option_type`,`option_id`,`option_value`,`option_level`,`option_parent_id`,`option_tips`,`ctime`,`hits`)
                     values (%s,%s,'%s','%s','%s','%s','%s',now(),1)
                  """%(usr_id,options_type,L[0][0],L[0][1],L[0][2],L[0][3],L[0][4])
        print ToGBK(sql)
        db.executesql(sql)
    return

def get_options(field_type,type,search,page_limit,usr_id,field_id,request):
    L = []

    type = int(type)
    if search == '':
        if type==3:
            L = get_sql_info(search,page_limit,field_id,request)
        else:
            L = get_recently_data(type,page_limit,usr_id)
    else:
        if type==21:  #项目
            L = get_proj_info(search,page_limit)
        elif type==19:  #费用
            L = get_cw_data(search,page_limit)
        elif type==23:   #供应商
            L = get_sup_info(search,page_limit)
        #elif type==24:   #人员
        #    L = get_addr_book_info(search,page_limit)
        #elif type==25:   #项目经理
        #    L = get_addr_book_info(search,page_limit)
        elif type==26:   #材料
            L = get_mat_info(search,page_limit,usr_id)
        elif type==3:
            L = get_sql_info(search,page_limit,field_id,request)

    names = 'value label checked tips'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)      
    return data

def get_recently_data(type,page_limit,usr_id):   
    L=[]
    
    if type==21:  #项目
        sql="""select option_id,concat('(',ifnull(op.gc_no,''),')',ifnull(op.cname,'')),concat('(',ifnull(op.gc_no,''),')',ifnull(op.cname,'')) from user_options o
               left join out_proj op on op.id = o.option_id
               where o.usr_id='%s' and o.option_type='%s' and ifnull(op.status,-1) != -1 order by o.ctime desc limit %s
            """%(usr_id,type,page_limit)
    elif type==19:  #费用
        sql="""select option_id,option_value,option_tips from user_options where usr_id='%s' and option_type='%s' order by o.ctime desc limit %s
            """%(usr_id,type,page_limit)
    elif type==23:   #供应商
        sql="""select option_id,ifnull(s.cname,''),s.cname from user_options o
               left join suppliers s on s.id = o.option_id
               where o.usr_id='%s' and o.option_type='%s' and ifnull(s.status,-1) != -1 order by o.ctime desc limit %s
            """%(usr_id,type,page_limit)
    elif type==24:   #员工
        sql="""select option_id,option_value,option_tips from user_options where usr_id='%s' and option_type='%s' order by o.ctime desc limit %s
            """%(usr_id,type,page_limit)
    elif type==25:   #项目经理
        sql="""select option_id,option_value,option_tips from user_options where usr_id='%s' and option_type='%s' order by o.ctime desc limit %s
            """%(usr_id,type,page_limit)
    elif type==26:   #材料
        sql="""select option_id,concat(number,'/',name),concat('规格:',ifnull(size,''),')') from user_options o
               left join _m504_clgl m on m.id = o.option_id
               where o.usr_id='%s' and o.option_type='%s' and m.id is not null and ifnull(m.status,-1) != -1 and (state = 1 or (state in (2,3)) and cid=%s)  order by o.ctime desc limit %s
            """%(usr_id,type,usr_id,page_limit) 
    else:
        return L
    #print sql
    lT,iN=db.select(sql)
    for e in lT:
        txt=e[1] 
        L.append([e[0],txt,'',e[2]])
    return L

def get_proj_info_selected(sDF):   
    L=[]
       
    sql="""select id,concat('(',ifnull(gc_no,''),')',ifnull(cname,'')),0,'',concat('(',ifnull(gc_no,''),')',ifnull(cname,'')) from out_proj where id='%s' order by id desc
            """%sDF
    #print sql
    lT,iN=db.select(sql)

    return lT,iN

def get_proj_info(search,page_limit):   
    L=[]
    
    sql="""select id,concat('(',ifnull(gc_no,''),')',ifnull(cname,'')) from out_proj where gw_status = 1 and ifnull(status,1)!=-1 and concat('(',ifnull(gc_no,''),')',ifnull(cname,'')) like '%%%s%%' order by id desc limit %s
            """%(search,page_limit)
    print sql
    lT,iN=db.select(sql)
    for e in lT:
        txt=e[1]
        L.append([e[0],txt,'',txt])
    return L

def get_sup_info_selected(sDF):   
    L=[]
       
    sql="""select id,ifnull(cname,''),0,'',ifnull(cname,'') from suppliers where id='%s' order by id desc
            """%sDF
    print sql
    lT,iN=db.select(sql)

    return lT,iN

def get_sup_info(search,page_limit):   
    L=[]
       
    sql="""select id,ifnull(cname,'') from suppliers where ifnull(status,0)!=-1 and cname like '%%%s%%' order by id desc limit %s
            """%(search,page_limit)
    print sql
    lT,iN=db.select(sql)
    for e in lT:
        txt=e[1]
        L.append([e[0],txt,'',e[1]])
    return L

def get_mat_info_selected(sDF):   
    L=[]
       
    sql="""select id,concat(number,'/',name,'/',size,'/',type,'/',unit,'/',brand),0,'',concat('(规格:',ifnull(size,''),')') from _m504_clgl where id='%s' order by id desc
            """%sDF
    lT,iN=db.select(sql)

    return lT,iN

def get_mat_info(search,page_limit,usr_id):   
    L=[]
       
    sql="""select id,concat(number,'/',name,'/',size,'/',type,'/',unit,'/',brand),concat('(规格:',ifnull(size,''),')') from  `_m504_clgl`  
            where status != -1 and (state = 1 or (state in (2,3)) and cid=%s) and concat(number,'/',name) like '%%%s%%' order by id desc limit %s
            """%(usr_id,search,page_limit)
    #print sql
    lT,iN=db.select(sql)
    for e in lT:
        txt=e[1] 
        L.append([e[0],txt,'',e[2]])
    return L

def get_sql_info(search,page_limit,field_id,request):   
    L=[]
    sql = "select IFNULL(field_options_txt,''),ifnull(para_cols,'') from menu_form_cols where id=%s"%(field_id)
    lT,iN=db.select(sql)
    if iN==0:
        return L
    sql=lT[0][0]
    if sql == '':
        return L
    para_cols = lT[0][1]
    sql = sql.replace("{_self}",search)
    paras = para_cols.split(',')
    #print paras
    #print request.POST
    for e in paras: 
        if e =='': break
        sql = sql.replace("{%s}"%e,MySQLdb.escape_string(request.POST.get(e, '')))
    sql += " limit %s"%(page_limit)
    
    #print ToGBK(sql)    
    lT,iN=db.select(sql)
    for e in lT:
        txt=e[1]
        L.append([e[0],txt,'',txt])
    return L


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
        sTemp = value
    return sTemp

def getFormData187(pk,field_id,menu_id,usr_id,request):
    mode = request.GET.get('mode','view')
    if field_id == '187':
        db_id = request.POST.get('source_db','')
        link_id = 189
    else:
        db_id = request.POST.get('dest_db','')
        link_id = 3369

    
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
                where mfc.id = '%s'"""%(link_id)
    sql+="""     order by mfc.sort """
    #print sql
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    rows1,iN1 = db.select(sql)
            
    L1 = []
    for i in range(0,iN1):
        e = list(rows1[i])
        e[10] = get_options1(db_id)
      
        L1.append(e)
    
    data = [dict(zip(names, d)) for d in L1]
    formData = json.dumps(data,ensure_ascii=False)      
    return formData

def get_options1(db_id):
    sql = "select db_host,port,db_name,user_name,passwd from db_info where id=%s"%(db_id)
    rows,iN = db.select(sql)
    db1 = MySQLdb.connect(host=rows[0][0],port=rows[0][1],user=rows[0][3],passwd=rows[0][4],db=rows[0][2],charset="utf8")
    L=[['','--请选择--','1']]
    
    sql = '''select md.menu_id,mf.menu_name from menu_data_source md
                left join menu_func mf on md.menu_id=mf.menu_id
                where mf.status=1 and mf.menu_id!=0
                order by mf.sort
          '''
    lT,iN = sql_select(db1,sql)
    for e in lT:
        txt=e[1]
        L.append([e[0],txt,''])
    db1.close()

    options =['',False]
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def sql_select(db,sqlstr):
    cur=db.cursor()
    cur.execute(sqlstr)
    List=cur.fetchall()
    iTotal_length=len(List)
    cur.close()
    return List,iTotal_length

