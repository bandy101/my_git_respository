# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
from HW_FILE_TOOL               import make_sub_path,readImage
import httplib
import random
import base64,os
import MySQLdb
exec ('from %s.share        import db,g_data,data_url,mValidateUser,get_YES_NO_data,get_mtc_t_data,get_roles_list,HttpResponseCORS,get_mtc_sys_data,fs_url,m_prjname'%prj_name) 
exec ('from %s.share        import addtwodimdict,get_gw_type_data1,get_gw_type_data2,get_flow_data,get_table_field,get_page_field,get_col_field,get_all_tables,get_use_tables'%prj_name) 
exec ('from %s.share        import sql_decode,sql_encode,sql_form_encode,get_options_data,encode_table_sql,ToGBK,get_options_data,m_dbname,strDuplicateRemoval'%prj_name) 
 
def setListSql(request):
    menu_id = request.POST.get('menu_id', 1402)
    func = request.GET.get('func', '')
    page_id = request.POST.get('page_id', '')
    pk =  request.POST.get('pk','')
    modal_step = request.POST.get('modal_step_change', '11')
    if str(modal_step) == '11':
        '''sql = """select fc.gw_id,fc.id,fc.proj_id,op.cname,ifnull(fc.pay_money,0),fc.ctime,fc.cid,fc.cusrname,fc.sn,ifnull(fc.`out_moneyA`,0)   from fund_call fc
                 left join gw_doc d on d.id = fc.gw_id
                 left join `out_proj` op on op.id = fc.proj_id
                 where d.finish=1 and fc.gw_status!=1 order by fc.ctime asc"""
        rows,iN = db.select(sql)
        for e in rows:
            gw_id = e[0]
            m_id = e[1]
            proj_id = e[2]
            proj_name = e[3]
            pay_money = e[4]
            ctime = e[5]
            cid = e[6]
            cusrname = e[7]
            sn = e[8]
            sn1 = sn.replace('YF','ZJBF')
            out_moneyA = e[9]
            sql = """INSERT INTO gw_doc ( title,cid,cusrname,ctime,type_id,menu_id,status,status_txt,finish)  
                      VALUES ('系统自动导入',%s,'%s','%s',38,309,8,'已登记',1);"""%(cid,cusrname,ctime)

            print ToGBK(sql)
            db.executesql(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
            bf_gwid = rows[0][0]
            sql = """insert into `_m309_zjbf` (`gw_id`,`gw_status`,`cid`,`cusrname`,`ctime`,`sn`,`sn_zjyf`,`proj_id`,`pay_money`,`pay_bcsq`,`zjyf_gwid`,`proj_name`)
                      VALUES (%s,2,%s,'%s','%s','%s','%s',%s,%s,%s,%s,'%s');
            """%(bf_gwid,cid,cusrname,ctime,sn1,sn,proj_id,pay_money,out_moneyA,gw_id,proj_name)
            print ToGBK(sql)
            db.executesql(sql)
            sql = "update fund_call_list set gw_id =%s where m_id=%s"%(bf_gwid,m_id)            
            db.executesql(sql)'''
        page_name = request.POST.get('page_name', '')
        page_label = request.POST.get('page_label', '')
        if page_name=='':
            s = """
            {
            "errcode":-1,
            "errmsg":"请首先输入name!",
            }
            """      
            return HttpResponseCORS(request,s)
        if page_id=='' or str(page_id)=='0':
            sql = """select id from menu_list_pages where menu_id=%s and page_name='%s'"""%(pk,page_name)
            rows,iN = db.select(sql)
            if iN ==0:
                sql = """insert into menu_list_pages (menu_id,page_name,label,list_table,list_table_ab,list_order,sort,status) \
                     select %s,'%s','%s',form_table,form_table_ab,concat('order by ',form_table_ab,'.',form_index_name,' desc'),999,1
                     from menu_data_source where menu_id=%s;
                     """%(pk,page_name,page_label,pk)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
            page_id = rows[0][0]
        step = 11
    elif str(modal_step) == '12':
        step = 12
    elif str(modal_step) == '13':
        step = 13
    elif str(modal_step) == '16':
        col_name = request.POST.get('lists_col_name', '')
        page_id = request.POST.get('lists_col_id', '')
        pages = request.POST.get('lists_pages', '')
        pages = handleMutilValue(pages,0)
        if col_name=='':
            s = """
            {
            "errcode":-1,
            "errmsg":"请首先输入name!",
            }
            """      
            return HttpResponseCORS(request,s)
        if page_id=='' or str(page_id)=='0':
            random_no = "%s_%s"%(time.time(),usr_id)
            sql = """select id from menu_list_filters where memu_id=%s and filter_name='%s'"""%(pk,col_name)
            rows,iN = db.select(sql)
            if iN ==0:
                sql = """insert into menu_list_filters (menu_id,pages,filter_name) 
                     """%(pk,pages,col_name)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
            page_id = rows[0][0]
        step = 16
    else:
        step = 0
    return getPageData(request,menu_id,pk,page_id,step)


def setFormSql(request):
    #print request.POST
    menu_id = request.POST.get('menu_id', 1402)
    func = request.GET.get('func', '')
    field_id = request.POST.get('field_id', '')
    pk =  request.POST.get('pk','')
    modal_step = request.POST.get('modal_step_change', '21')
    if str(modal_step) == '21':
        step_id = request.POST.get('step_id', '')
        field_name = request.POST.get('field_name', '')
        label = request.POST.get('label', '')
        pk = request.POST.get('pk', '')
        field_type = request.POST.get('field_type', '')
        field_show = request.POST.get('field_show', '')
        if field_name=='':
            s = """
            {
            "errcode":-1,
            "errmsg":"请首先输入name!",
            }
            """      
            return HttpResponseCORS(request,s)
        if field_id=='' or str(field_id)=='0':
            sql = """select id from menu_form_cols where step_id=%s and col_name='%s'"""%(step_id,field_name)
            #print sql
            rows,iN = db.select(sql)
            if iN ==0:
                sql = """insert into menu_form_cols (menu_id,step_id,col_name,label,field_col_name,field_type,sort) 
                        values (%s,%s,'%s','%s','%s',%s,99)
                     """%(pk,step_id,field_name,label,field_show,field_type)
                print ToGBK(sql)
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                field_id = rows[0][0]
            else:
                field_id = rows[0][0]

        step = 21
    elif str(modal_step) == '22':
        step = 22
    elif str(modal_step) == '23':
        step = 23
    elif str(modal_step) == '24':
        step = 24
    elif str(modal_step) == '26':
        step = 26
    elif str(modal_step) == '27':
        step = 27
    elif str(modal_step) == '41':
        step_id = request.POST.get('step_id', '')
        field_name = request.POST.get('field_name', '')
        label = request.POST.get('label', '')
        pk = request.POST.get('pk', '')
        field_type = request.POST.get('field_type', '')
        field_show = request.POST.get('field_show', '')
        parent_id = request.POST.get('parent_id', '')
        if field_name=='':
            s = """
            {
            "errcode":-1,
            "errmsg":"请首先输入name!",
            }
            """      
            return HttpResponseCORS(request,s)
        if field_id=='' or str(field_id)=='0':
            sql = """select id from menu_form_cols where step_id=%s and col_name='%s'"""%(step_id,field_name)
            print sql
            rows,iN = db.select(sql)
            if iN ==0:
                sql = """insert into menu_form_cols (menu_id,step_id,col_name,label,field_col_name,field_type,is_grid,parent_id,sort) 
                        values (%s,%s,'%s','%s','%s',%s,1,%s,99)
                     """%(pk,step_id,field_name,label,field_show,field_type,parent_id)
                #print sql
                db.executesql(sql)
                sql = "select last_insert_id();"
                rows,iN = db.select(sql)
                field_id = rows[0][0]
            else:
                field_id = rows[0][0]

        step = 41
    elif str(modal_step) == '52':
        step_id = request.POST.get('step_id', '')
        default_id = request.POST.get('default_id', '')
        if field_id=='':
            s = """
            {
            "errcode":-1,
            "errmsg":"请首先选择字段!",
            }
            """      
            return HttpResponseCORS(request,s)
        if default_id=='' or str(default_id)=='0':
            sql = """select id from menu_form_calculate where field_id=%s"""%(field_id)
            print sql
            rows,iN = db.select(sql)
            if iN ==0:
                sql = """insert into menu_form_calculate (field_id,sort) 
                        values (%s,99)
                     """%(field_id)
                print sql
                db.executesql(sql)
            else:
                s = """
                {
                "errcode":-1,
                "errmsg":"该字段已设置，请勿重复添加!",
                }
                """      
                return HttpResponseCORS(request,s)

        step = 52
        return getCalData(request,field_id)
    elif func == 'table':
        modal_step = request.POST.get('modal_step_change', '31')
        step_id = request.POST.get('step_id', 0)
        '''if str(step_id)=='0':
            s = """
            {
            "errcode":-1,
            "errmsg":"无法新增!",
            }
            """      
            return HttpResponseCORS(request,s)     '''   
        field_id = step_id
        step = modal_step
    else:
        step = 0
    return getPageData(request,menu_id,pk,field_id,step)

def getCalData(request,field_id):
    sql = """select mf.menu_name,ms.step_name,mc.col_name,mc.label,ifnull(mc.parent_id,''),ifnull(c.expression,''),ifnull(c.exprLabel,''),ifnull(c.on_change,''),ms.id
                from `menu_form_calculate` c
                left join menu_form_cols mc on mc.id=c.field_id
                left join `menu_form_steps` ms on ms.id = mc.step_id
                left join `menu_func` mf on mf.menu_id=mc.menu_id
                where mc.id = %s"""%(field_id)
    rows,iN = db.select(sql)
    names = 'menu_name step_name col_name label cols expression exprLabel checkField'.split()
    L = []
    for e in rows:
        L1 = list(e)
        step_id = e[8]
        parent_id = e[4]
        L2 = []   
        L3 = ['主表','']
        sql = "select col_name,label from menu_form_cols where step_id=%s and is_grid=0 and field_type in (1,3,5,6,8,19) and col_name not in ('id','gw_id','cid','uid')"%(step_id)
        rows1,iN1 = db.select(sql)
        names1 = 'col_name label'.split()
        L3[1] = [dict(zip(names1, d)) for d in rows1]
        L2.append(L3)
        if parent_id == '':
            sql = "select id,col_name,label from  menu_form_cols where step_id=%s and field_type =24"%(step_id)
            rows2,iN2 = db.select(sql)
            for e2 in rows2: 
                L3 = ['','']
                L3[0] = e2[2]
                sql = "select col_name,label from menu_form_cols where step_id=%s and parent_id=%s and field_type in (1,3,5,6,8,19)"%(step_id,e2[0])
                rows1,iN1 = db.select(sql)
                L3[1] = [dict(zip(names1, d)) for d in rows1]
                L2.append(L3)
        else:
            sql = "select id,col_name,label from  menu_form_cols where id=%s and field_type =24"%(parent_id)
            rows2,iN2 = db.select(sql)
            for e2 in rows2: 
                L3 = ['','']
                L3[0] = e2[2]
                sql = "select col_name,label from menu_form_cols where step_id=%s and parent_id=%s and field_type in (1,3,5,6,8,19)"%(step_id,e2[0])
                rows1,iN1 = db.select(sql)
                L3[1] = [dict(zip(names1, d)) for d in rows1]
                L2.append(L3)

        L1[4] = L2
        L.append(L1)
    data = [dict(zip(names, d)) for d in L]

    formData = json.dumps(data,ensure_ascii=False)      
    s = """
        {
        "errcode":0,
        "errmsg":"",
        "formData":%s,
        }
        """%(formData)
    print ToGBK(s)
    return HttpResponseCORS(request,s)

def getPageData(request,menu_id,pk,page_id,step):
    sql = """SELECT id,final_sql FROM menu_form_steps where menu_id=%s and step=%s """%(menu_id,step)
    print sql
    rows_table,iN = db.select(sql)
    data = []
    formData = json.dumps(data,ensure_ascii=False)      
    refreshData = json.dumps(data,ensure_ascii=False)      
    showData = json.dumps(data,ensure_ascii=False)     
    gridData = json.dumps(data,ensure_ascii=False)     
    value_dict = dict()    
    if len(rows_table)>0:
        step_id = rows_table[0][0]
        form_sql = rows_table[0][1]
        sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name
                  ,mfc.required
                  ,mfc.size
                  ,mfc.readonly
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
                order by mfc.sort """%(step_id)
        #print sql
        names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
        rows1,iN1 = db.select(sql)
        L = []
        sql = "select para_type,IFNULL(link_field,'') from menu_form_steps_para where step_id=%s order by sort"%(step_id)
        para_row,iN = db.select(sql)
        if page_id!='' and str(page_id)!='0':
            #print para_row
            print step_id
            if str(step_id) == '26':
                btn_id = request.POST.get('btn_id', '')
                if btn_id == '':
                    sql = form_sql.replace('$s',str(page_id))
                else: 
                    sql = """select '',
    mc.id,
    mc.menu_id,
    mf.menu_name,
    mc.step_id,
    gb.btn_name,
    mc.label,
    ifnull(gb.sel_type,''),
    ifnull(gb.sel_cols,''),
    gb.id
  from menu_form_cols mc
  left join menu_form_grid_button gb on mc.id = gb.field_id
  left join menu_form_steps ms on ms.id=mc.step_id
  left join menu_func mf on mf.menu_id=ms.menu_id
  where gb.id = '%s'"""%(btn_id)
            elif str(step_id) == '31':
                print request.POST
                btn_id = request.POST.get('btn_id', '')
                if btn_id == '':
                    sql = form_sql.replace('$s',str(page_id))
                else: 
                    sql = """select '',
    mc.id,
    mc.menu_id,
    mf.menu_name,
    mc.step_id,
    gb.btn_name,
    mc.label,
    ifnull(gb.sel_type,''),
    ifnull(gb.sel_cols,''),
    '',
    gb.id
  from menu_form_cols mc
  left join menu_form_grid_button gb on mc.id = gb.field_id
  left join menu_form_steps ms on ms.id=mc.step_id
  left join menu_func mf on mf.menu_id=ms.menu_id
  where gb.id = '%s'"""%(btn_id)
            else:
                sql = form_sql.replace('$s',str(page_id))
            print sql

            rows,iN = db.select(sql)
            for i in range(0,iN1):
                e = list(rows1[i])
                #print "i=%s len=%s"%(i,len(rows[0]))
                if i<len(rows[0]):
                    e[6] = rows[0][i]
                else:
                    e[6] = getDefaultvalue(request,rows1[i][18],rows1[i][6])
                value_dict[rows1[i][0]] = e[6]
                L.append(e)
            m_id = rows[0][0]
        else: 
            for i in range(0,iN1):
                e = list(rows1[i])
                e[6] = getDefaultvalue(request,rows1[i][18],rows1[i][6])
                value_dict[rows1[i][0]] = e[6]
                L.append(e)
             
        L1 = []
        for i in range(0,iN1):
            e = list(L[i])
            para1 = ''
            para2 = ''
            if e[22] != '':
                para1 = value_dict[e[22]] or ''
                if e[23] == '':
                    para2 = 0
                else:
                    para2 = value_dict[e[23]] or ''
            single = True
            if e[17]==5:
                single = False
            if str(L[i][17]) == '15':  #单选弹出框
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) =='16':  #多选弹出框
                e[10] = get_mutisel_options(e[-1],e[6])
                e[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
            elif str(L[i][17]) in ['3','5','6','18','26','32']:  #监听数字改变
                e[10] = get_options_data(menu_id,'',pk,e[19],e[20],e[21],e[6],para1,para2,single)
                if e[-3]!='':
                    e[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0"%(data_url,menu_id,pk,e[-1]),"_refresh",e[-2])
            elif str(L[i][17]) == '24':       
                e1=L[i][0]
                e[11],e[12] = getPageGrid(menu_id,e[-1],pk,value_dict,request)
            L1.append(e)

        data = [dict(zip(names, d)) for d in L1]

        formData = json.dumps(data,ensure_ascii=False)      

        sql ="""SELECT mfc.col_name,'','','','',mfr.field_id
                FROM menu_form_show mfr
                LEFT join menu_form_cols mfc on mfr.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1
                group by mfc.id
                order by mfc.sort """%(step_id)
        #print sql
        names = 'col_name operator check_field conditional value'.split()
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

        data = [dict(zip(names, d)) for d in L]
        showData = json.dumps(data,ensure_ascii=False)      

        sql ="""SELECT mfc.col_name,mg.has_add,mg.has_del,mg.has_order,mg.has_import,mg.import_name,mg.import_url
                FROM menu_form_grid_setting mg
                LEFT join menu_form_cols mfc on mg.field_id = mfc.id
                where mfc.step_id=%s and mfc.status = 1
                order by mfc.sort """%(step_id)
        #print sql
        rows,iN = db.select(sql)
        names = 'col_name has_add has_del has_order has_import import_name import_url'.split()
        L = [dict(zip(names, d)) for d in rows]
        gridData = json.dumps(L,ensure_ascii=False)      

    s = """
        {
        "errcode":0,
        "errmsg":"",
        "formData":%s,
        "showData":%s,
        "gridData":%s,
        }
        """%(formData,showData,gridData)
    return HttpResponseCORS(request,s)

def getPageGrid(menu_id,field_id,pk,value_dict,request):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    cur_dept_id = request.session.get('cur_dept_id', '')
    cur_dept_name = request.session.get('cur_dept_name', '')
    sql ="""SELECT mfc.col_name
                  ,mfc.label
                  ,ft.name
                  ,mfc.required
                  ,mfc.size
                  ,mfc.readonly
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
                where mfc.parent_id=%s
                order by mfc.sort """%(field_id)

    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url'.split()
    L=[]
    rows1,iN = db.select(sql)
    i = 0
    
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
            para1 = value_dict[e[22]] or ''
            if e[23] == '':
                para2 = 0
            else:
                para2 = value_dict[e[23]] or ''
        single = True
        if L1[17]==5:
            single = False
        if str(L1[17]) == '15':  #单选弹出框
            L1[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
        elif str(L1[17]) =='16':  #多选弹出框
            L1[10] = get_mutisel_options(e[-1],e[6])
            L1[15] = packFormUrl(pk,e[-1],"%s/select/?field_id=%s"%(data_url,e[-1]),"_window")
        elif str(L1[17]) in ['3','5','6','18','26','32']:  #监听数字改变
            L1[10] = get_options_data(menu_id,'',pk,e[19],e[20],e[21],e[6],para1,para2,single)
            if e[-3]!='':
                L1[15] = packonChangeUrl(pk,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0"%(data_url,menu_id,pk,e[-1]),"_refresh",e[-2])
        else:
            if L1[15] != '':
                L1[15] = packFormUrl(pk,e[-1],e[15],e[-4])

        value_dict[e[0]] = L1[6]
        L.append(L1)
    data = [dict(zip(names, d)) for d in L]
    
    
    sql = "select final_sql from menu_form_grid_sql where field_id=%s "%(field_id)
    rows,iN = db.select(sql)
    if iN>0:
        grid_sql = rows[0][0]
        sql = "select para_type,IFNULL(link_field,'') from menu_form_grid_sql_para where field_id=%s order by sort"%(field_id)
        para_row,iN = db.select(sql)
        sql = packPara(grid_sql,para_row,'',request)
        #print sql
        rows,iN = db.select(sql)

    if str(field_id) == '1641':
        sql = "select f.id,f.cname,'','','','','' from  `menu_form_func` f  where f.`menu_id` = %s"%(pk) 
        rows,iN = db.select(sql)
    elif str(field_id) == '441':
        btn_id = request.POST.get('btn_id', '')
        if btn_id != '':
            sql = "select id,sel_col_id,field_id1 from menu_form_select_cols where btn_id= %s"%(btn_id) 
            rows,iN = db.select(sql)
    elif str(field_id) == '442':
        btn_id = request.POST.get('btn_id', '')
        if btn_id != '':
            sql = "select id,para_name,link_field from menu_form_url_para where btn_id= %s"%(btn_id) 
            rows,iN = db.select(sql)

    L = []
    for e in rows:
        row = list(e)
        for i in range(0,len(row)):
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
            row[i] = get_options_data(menu_id,'',pk,rows1[i][19],rows1[i][20],rows1[i][21],row[i],para1,para2,single)
        L.append(row)
        
    names=[]
    for n in range(0,len(rows1)):
        names.append(rows1[n][0])
    list_data = [dict(zip(names, d)) for d in L]
    return data,list_data

def saveUserPara(request):
    step = request.GET.get('step','')
    step = step.replace('/','')
    if str(step) == '3':
       s = saveUserStep3(request)
    elif str(step) == '4':
       s = saveUserStep4(request)
    elif str(step) == '5':
       s = saveUserStep5(request)
    elif str(step) == '2':
       s = saveUserStep2(request)
    else:
        s = """
        {
        "errcode":-1,
        "errmsg":"保存失败",
        }
        """
    
    return HttpResponseCORS(request,s)

def saveUserStep2(request):
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    id = data_list.get('ID','')
    nick = data_list.get('nick','')
    mobile = data_list.get('mobile','')
    email = data_list.get('email','')
    wx_no = data_list.get('wx_no','')
    birthday = data_list.get('birthday') or 'NULL'
    bank = data_list.get('bank','')
    bank_name = data_list.get('bank_name','')
    bank_no = data_list.get('bank_no','')
    coaddr = data_list.get('coaddr','')
    cocode = data_list.get('cocode','')
    cotel = data_list.get('cotel','')
    cotel_ext = data_list.get('cotel_ext','')
    cofax = data_list.get('cofax','')
    hmaddr = data_list.get('hmaddr','')
    hmcode = data_list.get('hmcode','')
    hmtel = data_list.get('hmtel','')
    remarks = data_list.get('remarks','')
    remarks = remarks.replace("'",'"')
    usr_id = ''
    sql = "select ifnull(usr_id,'') from empl where addr_book_id='%s'"%(id)
    rows,iN = db.select(sql)
    if iN>0:
        usr_id = rows[0][0]
    if iN ==0 or usr_id=='':
        s = """
            {
            "errcode":-1,
            "errmsg":"修改失败",
            }
            """   
        return HttpResponseCORS(request,s)

    sql="""update addr_book set
            nick = '%s',              
            mobile = '%s',            
            email = '%s',           
            birthday = %s,         
            coaddr = '%s',        
            cocode = '%s',         
            cotel = '%s',           
            cotel_ext = '%s',       
            cofax = '%s',     
            hmaddr = '%s',         
            hmcode = '%s',         
            hmtel = '%s',         
            remarks = '%s',        
            uid = %s,               
            utime = now(),   
            bank='%s',           
            bank_name='%s',       
            bank_no='%s',      
            wx_no='%s'         
            where id = '%s'
        """%(nick,mobile,email,birthday,coaddr,cocode,cotel,cotel_ext,cofax
            ,hmaddr,hmcode,hmtel,remarks,usr_id,bank,bank_name,bank_no,wx_no,id)
    db.executesql(sql)
    
    sql = """update empl em
                left join `addr_book`  ab on em.Addr_book_Id = ab.id
                set 
                em.Birth_day = ab.birthday 
                ,em.Mmobil = ab.mobile 
                ,em.tel = ab.cotel 
                ,em.Home_tel = ab.hmtel 
                , em.wx_no = ab.wx_no
            where ab.id = '%s';
          """%(id)
    db.executesql(sql)

    sql = """update users u
                left join empl em on em.usr_id=u.usr_id
                left join `addr_book`  ab on em.Addr_book_Id = ab.id
                set 
                u.mobil = ab.mobile 
                ,u.tel = ab.cotel 
                ,u.e_mail = ab.email 
                , u.wx_no = ab.wx_no
            where ab.id = '%s';
          """%(id)
    db.executesql(sql)

    s = """
        {
        "errcode":0,
        "errmsg":"信息修改成功",
        }
        """   
    return HttpResponseCORS(request,s)

def saveUserStep3(request):
    from PIL import Image
    path= "/home/webroot/data/%s/open/user_pic/"%m_prjname
    pic_url = ''
    make_sub_path(path)#检查目录是否存在，如果不存在，生成目录  make_sub_path
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    usr_id = data_list.get('usr_id','')
    pic =  data_list.get('pic','')
    x =  data_list.get('img_x','') or 0 
    y =  data_list.get('img_y','') or 0 
    w =  data_list.get('img_width','') or 0 
    h =  data_list.get('img_height','') or 0
  
    #print pic.find('http://')
    if pic.find('http://')<0:
        pic_ext = pic.split(';')[0]
        pic_ext = pic_ext.split('/')[-1]
        pic_data = pic.split(';')[1] 
        pic_data = pic_data.split(',')[-1]
        sql_q="SELECT IFNULL(pic,'') FROM users WHERE usr_id='%s'"%usr_id
        lT,iN=db.select(sql_q)
        if iN>0:
            usr_pic=lT[0][0]
            if usr_pic!='':
                file_path=os.path.join(path,usr_pic)
                try:
                    os.remove(file_path)
                except:
                    pass
            save_name='%s.%s'%(usr_id,pic_ext)
            small_name = "small_%s"%save_name
            file_path=os.path.join(path,save_name)
            small_path = os.path.join(path,small_name)
            data= base64.b64decode(pic_data)

            f=open(file_path,'wb')
            f.write(data)
            f.flush()
            f.close()
            sql="update users set pic='%s' where usr_id='%s'"%(save_name,usr_id)
            #print sql
            db.executesql(sql)
            pic_url = "%s/user_pic/"%(fs_url)+save_name
    else:
        usr_pic = pic.split('/')[-1]
        small_name = "small_%s"%usr_pic
        file_path=os.path.join(path,usr_pic)
        small_path = os.path.join(path,small_name)
        pic_url = pic

    if w>0 and h>0:  #裁剪
        img=Image.open(file_path)
        #print img.size
        box=(x,y,w+x,h+y)
        roi=img.crop(box)        
        roi.save(file_path)
    
    #压缩
    #img=Image.open(file_path)
    #x,y = img.size
    #if x>400:
    #    x1 = 400
    #    y1 = 400*y/x
    #    img = img.resize((x1, y1), Image.ANTIALIAS)
    #    img.save(file_path)

    #生成小头像
    img = Image.open(file_path)
    x,y = img.size
    x1 = 40
    y1 = 40*y/x
    img = img.resize((x1, y1), Image.ANTIALIAS)
    img.save(small_path)

    '''sql = "select usr_id,pic from users where ifnull(pic,'')!=''"
    rows,iN = db.select(sql)
    for e in rows:
        pic = e[1]
        small_name = "small_%s"%pic
        file_path=os.path.join(path,pic)
        small_path = os.path.join(path,small_name)
        if not os.path.exists(small_path):  
            img = Image.open(file_path)
            x,y = img.size
            x1 = 40
            y1 = 40*y/x
            img = img.resize((x1, y1), Image.ANTIALIAS)
            if len(img.split()) == 4 and pic.find('png')>=0:
                #prevent IOError: cannot write mode RGBA as BMP
                r, g, b, a = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.save(small_path)
            else:
                img.save(small_path)'''

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功",
        "pic_url":"%s"
        }
        """%pic_url
    return HttpResponseCORS(request,s)

def saveUserStep4(request):
    path= "/home/webroot/data/%s/open/job_img/"%m_prjname
    make_sub_path(path)#检查目录是否存在，如果不存在，生成目录  make_sub_path
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    ab_id = data_list.get('ab_id','')
    pic =  data_list.get('job_img','')
    if pic!='':
        pic_ext = pic.split(';')[0]
        pic_ext = pic_ext.split('/')[-1]
        pic_data = pic.split(';')[1] 
        pic_data = pic_data.split(',')[-1]
        sql_q="SELECT IFNULL(job_img,'') FROM addr_book WHERE id='%s'"%ab_id
        lT,iN=db.select(sql_q)
        if iN>0:
            usr_pic=lT[0][0]
            if usr_pic!='':
                file_path=os.path.join(path,usr_pic)
                try:
                    os.remove(file_path)
                except:
                    pass
            save_name='%s.%s'%(ab_id,pic_ext)
            file_path=os.path.join(path,save_name)
    
            data= base64.b64decode(pic_data)
            f=open(file_path,'wb')
            f.write(data)
            f.flush()
            f.close()
            sql="update addr_book set job_img='%s' where id='%s'"%(save_name,ab_id)
            #print sql
            db.executesql(sql)

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功",
        }
        """   
    return HttpResponseCORS(request,s)

def saveUserStep5(request):
    pwd = ''
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    usr_id = data_list.get('ID','')
    old_passwd = data_list.get('old_passwd','')
    new_passwd = data_list.get('new_passwd','')
    #print data_list
    sql = "select `password` from users where usr_id='%s'"%(usr_id)
    rows,iN = db.select(sql)
    if iN>0:
        pwd = rows[0][0]
    if iN ==0 or pwd != old_passwd:
        s = """
            {
            "errcode":-1,
            "errmsg":"原密码错误，修改失败",
            }
            """   
        return HttpResponseCORS(request,s)
    sql = "update users set password='%s' where usr_id='%s'"%(new_passwd,usr_id)
    db.executesql(sql)

    s = """
        {
        "errcode":0,
        "errmsg":"密码修改成功",
        }
        """   
    return HttpResponseCORS(request,s)

def saveFormData(request):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    #print request.POST
    mode =  request.POST.get('mode','')
    data = request.POST.get('data','')
    data_list = json.loads(data)
    pk = request.GET.get('pk','')
    step = request.GET.get('step','')
    step = step.replace('/','')
    #print "step = %s"%step
    if str(step) == '11':
       s = saveStep11(request,data_list)
    elif str(step) == '12':
       s = saveStep12(request,data_list)
    elif str(step) == '13':
       s = saveStep13(request,data_list)
    elif str(step) == '21':
       s = saveStep21(request,data_list)
    elif str(step) == '22':
       s = saveStep22(request,data_list)
    elif str(step) == '23':
       s = saveStep23(request,data_list)
    elif str(step) == '26':
       s = saveStep26(request,data_list)
    elif str(step) == '31':
       s = saveStep31(request,data_list)
    elif str(step) == '32':
       s = saveStep32(request,data_list)
    elif str(step) == '33':
       s = saveStep33(request,data_list)
    elif str(step) == '1':
       s = saveStep1(request,mode,data_list)
    elif str(step) == '2':
       s = saveStep2(request,data_list)
    elif str(step) == '3':
       s = saveStep3(request,data_list)
    elif str(step) == '4':
       s = saveStep4(request,data_list)
    elif str(step) == '5':
       s = saveStep5(request,data_list)
    elif str(step) == '6':
       s = saveStep6(request,data_list)
    elif str(step) == '41':
       s = saveStep41(request,data_list)
    elif str(step) == '52':
       s = saveStep52(request,data_list)
    else:
        s = """
        {
        "errcode":-1,
        "errmsg":"保存失败",
        "pk":%s,
        }
        """%pk
    
    return HttpResponseCORS(request,s)


def saveStep1(request,mode,data_list):
    pk = data_list.get('pk','')
    menu_name = data_list.get('menu_name','')
    has_list = data_list.get('has_list','')
    has_audit = data_list.get('has_audit','')
    gw_type1 = data_list.get('gw_type1') or 'NULL'
    gw_type2 = data_list.get('gw_type2') or 'NULL'
    first_flow = data_list.get('first_flow') or 'NULL'
    has_verify = data_list.get('has_verify','')
    form_table = data_list.get('form_table','')
    form_table_ab = data_list.get('form_table_ab','')
    form_index_name = data_list.get('form_index_name','')
    is_new = data_list.get('is_new','')
    has_list = handleMutilValue(has_list,1)
    has_audit = handleMutilValue(has_audit,1)
    has_verify = handleMutilValue(has_verify,1)
    new_table_name = data_list.get('new_table_name','')
    is_new = handleMutilValue(is_new,1)
    if form_table_ab=='':
        form_table_ab = form_index_name[:3]

    #新建表
    if str(is_new) == '1':
        new_table_name = "_m%s_%s"%(pk,new_table_name)
        sql = "select `TABLE_NAME` from `INFORMATION_SCHEMA`.`TABLES` where `TABLE_SCHEMA`='%s' and `TABLE_NAME`='%s' and table_type='base table' "%(m_dbname,new_table_name)
        rows,iN = db.select(sql)
        if iN == 0:
            sql = """create table %s(
                        id INT NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY ( id )
                  )comment='自动创建：%s';"""%(new_table_name,menu_name)
            db.executesql(sql)
            form_table = new_table_name
            form_table_ab = "m%s"%pk
            form_index_name = 'id'
    sql = "select 1 from menu_data_source where menu_id=%s"%pk
    rows,iN = db.select(sql)
    if iN==0:
        sql = """insert menu_data_source (has_list,has_audit,gw_type1,gw_type2,first_flow,has_verify,form_table,form_table_ab,form_index_name,menu_id)
                 values (%s,%s,%s,%s,%s,%s,'%s','%s','%s',%s)
              """%(has_list,has_audit,gw_type1,gw_type2,first_flow,has_verify,form_table,form_table_ab,form_index_name,pk)
        init = 1
    else:
        sql = """update menu_data_source set has_list=%s,has_audit=%s,gw_type1=%s,gw_type2=%s,first_flow=%s
              ,has_verify=%s,form_table='%s',form_table_ab='%s',form_index_name='%s' where menu_id=%s
              """%(has_list,has_audit,gw_type1,gw_type2,first_flow,has_verify,form_table,form_table_ab,form_index_name,pk)
        init = 1
    #print sql 
    db.executesql(sql)

    step_id = 0
    sql = "call check_table(%s,'%s')"%(has_audit,form_table)
    db.executesql(sql)
    #写入默认数据
    sql = "select id from menu_form_steps where menu_id = %s and step=1"%(pk)
    #print sql
    rows,iN = db.select(sql)
    if iN>0:
        step_id = rows[0][0]
        sql = "update menu_form_steps set status=1,has_audit=%s where id=%s"%(has_audit,step_id)
        db.executesql(sql)   
    else:
        sql = """insert into menu_form_steps (menu_id,step,sort,status,step_name,type,has_audit) values (%s,1,1,1,'申请单',1,%s);"""%(pk,has_audit)
        db.executesql(sql)   
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        step_id = rows[0][0]

        #配置表单初始数据
        sql = "select id from menu_form_tables where step_id =%s and table_name='%s'"%(step_id,form_table)
        rows,iN = db.select(sql)
        if iN==0:#新添加行
            sql = """insert into menu_form_tables 
                        (menu_id,step_id,join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,sort)
                        values (%s,%s,'','%s','%s','%s','','','',%s)
                      """%(pk,step_id,form_table,form_table_ab,form_index_name,1)
            #print sql
            db.executesql(sql)
            sql = "insert into `menu_form_steps_para` (`step_id`,`para_type`,`link_field`,`sort`) values ('%s',8,'pk',1)"%(step_id)
            db.executesql(sql)
        updateFormStepTable(step_id,'') 

        #添加索引字段
        sql = "select id from menu_form_save_tables where step_id = %s and save_table='%s';"%(step_id,form_table)
        rows,iN = db.select(sql)
        if iN==0:
            sql = "insert into menu_form_save_tables (step_id,save_table,is_list,del_before_update,is_procedure,status) values (%s,'%s',0,0,0,1)"%(step_id,form_table)
            rows,iN = db.select(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
        table_id = rows[0][0]
        
        if str(has_audit) =='1':
            sql = """insert into menu_form_cols (menu_id,step_id,col_name,label,field_col_name,field_type,max_length,sort) 
                        values (%s,%s,'gw_id','公文ID','%s.gw_id',1,0,1)
                     """%(pk,step_id,form_table_ab)
            db.executesql(sql)    
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
            field_id = rows[0][0]
            sql = """update menu_form_cols set
                        enables=',1,2,5,3,',
                        show_table='%s',
                        show_col_name='gw_id',
                        is_number=1,
                        saves=',2,',
                        save_para=',2,3,'
                where id = '%s';"""%(form_table,field_id)
            db.executesql(sql)    

            sql = """insert into menu_form_save_cols (table_id,save_field_name,is_identity,is_number,default_type,request_name
                        ,is_add,is_upd,is_index,is_del,is_audit,is_verify,menu_id,data_table,field_id)
                        values(%s,'gw_id',0,1,8,'gw_id',0,1,1,1,1,1,%s,'%s',%s);"""%(table_id,pk,form_table,field_id)
            db.executesql(sql)   
        else:
            sql = """insert into menu_form_cols (menu_id,step_id,col_name,label,field_col_name,field_type,max_length,sort) 
                        values (%s,%s,'%s','%s','%s.%s',1,0,1)
                     """%(pk,step_id,form_index_name,form_index_name,form_table_ab,form_index_name)
            db.executesql(sql)    
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
            field_id = rows[0][0]

            sql = """update menu_form_cols set
                        enables=',1,2,5,',
                        show_table='%s',
                        show_col_name='%s',
                        is_number=1,
                        saves=',1,2,',
                        save_para=',1,2,3,'
                where id = '%s';"""%(form_table,form_index_name,field_id)
            db.executesql(sql)    

            sql = """insert into menu_form_save_cols (table_id,save_field_name,is_identity,is_number,default_type,request_name
                        ,is_add,is_upd,is_index,is_del,is_audit,is_verify,menu_id,data_table,field_id)
                        values(%s,'%s',1,1,8,'id',1,1,1,1,1,1,%s,'%s',%s);"""%(table_id,form_index_name,pk,form_table,field_id)
            db.executesql(sql)   

    if str(has_list) == '1': 
        v_order = 'order by %s.%s desc'%(form_table_ab,form_index_name)
    
        if str(has_audit) == '1':   
            insert_page(pk,'all','所有',form_table,form_table_ab,v_order,1,1,has_audit)
            insert_page(pk,'my','我的拟稿箱',form_table,form_table_ab,v_order,1,2,has_audit)
            insert_page(pk,'audit','我的待审',form_table,form_table_ab,v_order,0,3,has_audit)
            insert_page(pk,'sign','我的待会签',form_table,form_table_ab,v_order,0,4,has_audit)
            disable_page(pk,'manage',form_table,form_table_ab)
        else:
            insert_page(pk,'my','录入',form_table,form_table_ab,v_order,1,1,has_audit)
            insert_page(pk,'manage','管理',form_table,form_table_ab,v_order,0,2,has_audit)
            insert_page(pk,'all','查询',form_table,form_table_ab,v_order,0,3,has_audit)
            disable_page(pk,'audit',form_table,form_table_ab)
            disable_page(pk,'sign',form_table,form_table_ab)
    
        if str(has_verify) == '1':   
            insert_page(pk,'verify','待登记',form_table,form_table_ab,v_order,0,5,has_audit)
        else:
            disable_page(pk,'verify',form_table,form_table_ab)

    update_func(pk,5,'view','查看',1,5,1)
    if str(has_list) == '1': 
        update_func(pk,1,'add','添加',1,1,1)
        update_func(pk,2,'upd','修改',1,2,1)
        update_func(pk,3,'audit','审核',1,3,int(has_audit))
        update_func(pk,4,'verify','登记',1,4,int(has_verify)) 
        update_func(pk,6,'delete','删除',3,6,1)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%pk
    return HttpResponseCORS(request,s)    
def update_func(pk,id,ename,cname,type,sort,status):
    sql = "select seq from menu_form_func where menu_id=%s and id=%s"%(pk,id)
    rows,iN = db.select(sql)
    if iN>0:
        seq = rows[0][0]
        sql = "update menu_form_func set status=%s where seq=%s"%(status,seq)
        db.executesql(sql)
    else:
        sql = "insert into menu_form_func (menu_id,id,ename,cname,type,sort,status) values (%s,%s,'%s','%s',%s,%s,%s)"%(pk,id,ename,cname,type,sort,status)
        db.executesql(sql)
    print sql
    return 
def insertBtn(pk,step_id,label,btn_type,sort):
    col_name = "btn%s"%sort
    sql = """insert into menu_form_cols (menu_id,step_id,col_name,label,btn_type,btn_color,sort,enables) 
                        values (%s,%s,'%s','%s',%s,'%s',%s,'%s')
                     """%(pk,step_id,col_name,label,22,'blue',sort,'1,2,3,4,5')           
    db.executesql(sql)
    return

def updateDefaultCol(pk,step_id,table_id,form_table,col_name,sort):
    if col_name in ['cid','cusrname','ctime']:
        enables = '1,3,4,5'
        readonlys = '1,3,4,5'
        is_add = 1
        is_upd = 0
    else:
        enables = '2,3,4,5'
        readonlys = '2,3,4,5'
        is_add = 0
        is_upd = 1
    if col_name=='cid':
        label = '创建人ID'
        default_type = 1
    if col_name=='cusrname':
        label = '创建人'
        default_type = 2
    if col_name=='ctime':
        label = '创建时间'
        default_type = 5
    if col_name=='uid':
        label = '修改人ID'
        default_type = 1
    if col_name=='uusrname':
        label = '修改人'
        default_type = 1
    if col_name=='utime':
        label = '修改时间'
        default_type = 1
    sql = "update menu_form_cols set enables='%s',readonlys='%s',label='%s',sort=%s where step_id = %s and col_name='%s'"%(enables,readonlys,label,sort,step_id,col_name)
    db.executesql(sql)    
    sql = """update menu_form_save_cols set default_type=%s,is_add=%s,is_upd=%s where table_id=%s and save_field_name='%s'
          """%(default_type,is_add,is_upd,table_id,col_name)
    db.executesql(sql)    
    return

def updateFormStepTable(step_id,where_sql):
    sql = """select d.has_audit,d.form_table_ab,d.form_index_name from menu_form_steps s
             left join menu_data_source d on d.menu_id=s.menu_id where s.id=%s"""%(step_id)
    rows,iN = db.select(sql)
    has_audit = rows[0][0]
    table_ab = rows[0][1]
    index_name = rows[0][2]
    sql = "select join_type,table_name,table_ab,index_name,link_ab,link_index,ifnull(table_sql,'') from menu_form_tables where step_id = %s  order by sort"%(step_id)
    #print sql
    rows,iN = db.select(sql)
    table_sql = encode_table_sql(rows)
    if where_sql=='':
        if str(has_audit) =='1':
            where_sql = "WHERE %s.gw_id=$s "%(table_ab)
        else:
            where_sql = "WHERE %s.%s=$s "%(table_ab,index_name)
    table_sql = '%s %s'%(table_sql,where_sql)
    sql = """update menu_form_steps set table_sql="%s",where_sql="%s" where id=%s
                  """%(table_sql,where_sql,step_id)
    db.executesql(sql)
    return

def updateFormSql(step_id):
    sql = "select id,ifnull(table_sql,'') from menu_form_steps where id=%s"%(step_id)
    rows,iN = db.select(sql)
    table_sql = rows[0][1]
    sql = "select field_col_name,enables from menu_form_cols where step_id=%s and is_grid=0 and status=1 order by sort"%(step_id)
    rows,iN1 = db.select(sql)
    add_sql,update_sql,audit_sql,view_sql,verify_sql = sql_form_encode(rows,table_sql)
    
    sql = """update menu_form_steps set add_sql="%s",update_sql="%s",audit_sql="%s",view_sql="%s",verify_sql="%s" where id=%s
              """%(add_sql,update_sql,audit_sql,view_sql,verify_sql,step_id)
    #print sql
    db.executesql(sql)
    return

def updateGridSql(field_id):
    sql = "select id,ifnull(final_table,'') from menu_form_grid_sql where field_id=%s"%(field_id)
    rows,iN = db.select(sql)
    if iN == 0:
        return
    table_sql = rows[0][1]
    sql = "select col_name,label,ifnull(field_col_name,''),enables from menu_form_cols where parent_id=%s and status=1 order by sort"%(field_id)
    rows,iN1 = db.select(sql)
    final_sql = sql_grid_encode(rows,table_sql)
    
    sql = """update menu_form_grid_sql set final_sql="%s" where field_id=%s
              """%(final_sql,field_id)
    #print sql
    #db.executesql(sql)
    return
def sql_grid_encode(col_rows,table_sql):
    final_sql = sql_grid_encode_func(col_rows,table_sql,5)
    return final_sql
def sql_grid_encode_func(col_rows,table_sql,func):
    sql = "SELECT "
    col_sql = ''
    for e in col_rows:
        if str(func) in e[3].split(','):
            if e[2] == '':
                col_sql += "'' as %s /*%s*/,"%(e[0],e[1])
            else:
                col_sql += "%s as %s /*%s*/,"%(e[2],e[0],e[1])

    col_sql = col_sql[:-1]
    sql += col_sql +" "
    sql += table_sql 
    sql = sql.replace('%Y-%M-%D','%Y-%m-%d')
    print ToGBK(sql)
    return sql

def insert_page(pk,page_name,cname,form_table,form_table_ab,v_order,has_add,sort,has_audit):
    sql = "select id,where_sql from menu_list_pages where menu_id = %s and page_name='%s'"%(pk,page_name)
    rows,iN = db.select(sql)
    if iN>0:
        page_id = rows[0][0]
        where_sql = rows[0][1]
        sql = "update menu_list_pages set list_table='%s',list_table_ab='%s',list_order='%s',status=1  where id=%s"%(form_table,form_table_ab,v_order,page_id)
        db.executesql(sql)
    else:
        sql = """insert into menu_list_pages (menu_id,page_name,label,has_add,sort,list_table,list_table_ab,list_order)
                 values (%s,'%s','%s',%s,%s,'%s','%s','%s');"""%(pk,page_name,cname,has_add,sort,form_table,form_table_ab,v_order)
        #print ToGBK(sql)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        page_id = rows[0][0]
        where_sql = "WHERE %s.status != -1 "%(form_table_ab)
    sql = "select id from menu_list_tables where menu_id = %s and page_id=%s"%(pk,page_id)
    rows,iN = db.select(sql)
    if iN==0:
        sql = """insert into menu_list_tables (menu_id,page_id,table_name,table_ab,sort)
                 values (%s,%s,'%s','%s',1);"""%(pk,page_id,form_table,form_table_ab)
        db.executesql(sql)
        if str(has_audit) == '1': 
            if page_name == 'all':
                where_sql = " where 1=1 "
                table_sql = """SELECT DISTINCT D.id,D.title,D.cur_flow_id,D.finish,D.cur_flow_name,D.cur_user_name,D.status_txt,D.type_id
                    FROM gw_doc D
                    LEFT JOIN gw_type gt on gt.id = D.type_id
                    WHERE D.type_id=$s  and (gt.is_pub or FIND_IN_SET($s,D.cybl))"""
                sql = """insert into menu_list_tables 
                       (menu_id,page_id,join_type,table_name,table_sql,table_ab,index_name,link_table,link_ab,link_index,sort)
                       values (%s,%s,'LEFT JOIN','GW_DOC_temp013','%s','D','id','%s','%s','gw_id',2);
                      """%(pk,page_id,table_sql,form_table,form_table_ab)
                sql += """insert into menu_list_tables 
                       (menu_id,page_id,join_type,table_name,table_sql,table_ab,index_name,link_table,link_ab,link_index,sort)
                       values (%s,%s,'LEFT JOIN','GW_ROLE','','GR','GW_TYPE','GW_DOC_TEMP013','D','TYPE_ID',3);
                      """%(pk,page_id)
                db.executesql(sql)
                sql = """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,11,'',1);
                      """%(page_id)
                sql += """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,1,'',2);
                      """%(page_id)
                db.executesql(sql)
            elif page_name == 'my':  
                where_sql = " WHERE D.type_id=$s and D.usr_Id=$s and D.s_flag = 1"
                sql = """insert into menu_list_tables 
                       (menu_id,page_id,join_type,table_name,table_sql,table_ab,index_name,link_table,link_ab,link_index,sort)
                       values (%s,%s,'LEFT JOIN','GW_AUDIT','','D','gw_id','%s','%s','gw_id',2);
                      """%(pk,page_id,form_table,form_table_ab)
                db.executesql(sql)
                sql = """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,11,'',1);
                      """%(page_id)
                sql += """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,1,'',2);
                      """%(page_id)
                db.executesql(sql)
            elif page_name == 'audit':  
                where_sql = " WHERE D.type_id=$s and D.usr_Id=$s and D.s_flag = 0"
                sql = """insert into menu_list_tables 
                       (menu_id,page_id,join_type,table_name,table_sql,table_ab,index_name,link_table,link_ab,link_index,sort)
                       values (%s,%s,'LEFT JOIN','GW_AUDIT','','D','gw_id','%s','%s','gw_id',2);
                      """%(pk,page_id,form_table,form_table_ab)
                db.executesql(sql)
                sql = """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,11,'',1);
                      """%(page_id)
                sql += """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,1,'',2);
                      """%(page_id)
                db.executesql(sql)
            elif page_name == 'sign':  
                where_sql = " where D.type_id=$s and D.usr_id=$s"
                sql = """insert into menu_list_tables 
                       (menu_id,page_id,join_type,table_name,table_sql,table_ab,index_name,link_table,link_ab,link_index,sort)
                       values (%s,%s,'LEFT JOIN','GW_SIGN','','D','gw_id','%s','%s','gw_id',2);
                      """%(pk,page_id,form_table,form_table_ab)
                db.executesql(sql)
                sql = """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,11,'',1);
                      """%(page_id)
                sql += """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,1,'',2);
                      """%(page_id)
                db.executesql(sql)
            elif page_name == 'verify':  
                where_sql = " WHERE D.type_id=$s"
                sql = """insert into menu_list_tables 
                       (menu_id,page_id,join_type,table_name,table_sql,table_ab,index_name,link_table,link_ab,link_index,sort)
                       values (%s,%s,'LEFT JOIN','GW_VERIFY','','D','gw_id','%s','%s','gw_id',2);
                      """%(pk,page_id,form_table,form_table_ab)
                db.executesql(sql)
                sql = """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,11,'',1);
                      """%(page_id)
                db.executesql(sql)
        else:
            if page_name == 'my':
                where_sql += " and %s.cid=$s"%form_table_ab
                sql = "select id from menu_list_pages_para where page_id=%s"%(page_id)
                rows,iN = db.select(sql)
                if iN == 0:
                    sql = """insert into menu_list_pages_para 
                          (page_id,para_type,link_field,sort)
                          values (%s,1,'',1)
                          """%(page_id)
                    db.executesql(sql) 
    if str(has_audit) == '1': 
        index_name = 'gw_id'
        label = '公文ID' 
        index_col = '%s.gw_id'%form_table_ab
    else:
        index_name = 'id'
        label = 'ID' 
        index_col = '%s.id'%form_table_ab

    sql = "select join_type,table_name,table_ab,index_name,link_ab,link_index,ifnull(table_sql,'') from menu_list_tables where page_id = %s  order by sort"%(page_id)
    #print sql
    rows,iN = db.select(sql)
    table_sql = encode_table_sql(rows)
  
    del_sql = "delete from %s where %s = $s"%(form_table,index_name)
    table_sql = '%s %s'%(table_sql,where_sql)
    sql = """update menu_list_pages set table_sql="%s",delete_sql="%s",where_sql="%s" where id=%s
                  """%(table_sql,del_sql,where_sql,page_id)
    #print sql
    db.executesql(sql)
    
    #添加删除
    sql = "select id from menu_list_pages_del where FIND_IN_SET(%s,pages)"%(page_id)
    rows,iN = db.select(sql)
    if iN == 0:
        sql = """insert into menu_list_pages_del (pages,delete_sql,sort) values ('%s,',"%s",%s)
                  """%(page_id,del_sql,1)
        db.executesql(sql)
        sql = """insert into menu_list_pages_del_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,8,'pk',1)
                      """%(page_id)
        db.executesql(sql)

    #添加默认索引字段
    sql = "select id,pages from menu_list_cols where menu_id = %s and is_index=1"%(pk)
    rows,iN = db.select(sql)
    if iN==0:
        sql = """insert into menu_list_cols (menu_id,pages,col_name,label,field_show,col_type,is_index,sort,status)
                      values (%s,'%s,',"%s","%s","%s",0,1,1,1)
                      """%(pk,page_id,index_name,label,index_col)           
        db.executesql(sql)
        if str(has_audit) == '1' and page_name == 'all': 
            sql = """insert into menu_list_cols (menu_id,pages,col_name,label,field_show,col_type,is_index,sort,status)
                      values (%s,'',"cur_flow_name","当前流程","D.cur_flow_name",1,0,101,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,field_show,col_type,is_index,sort,status)
                      values (%s,'',"cur_user_name","当前处理人","D.cur_user_name",1,0,102,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,field_show,col_type,is_index,sort,status)
                      values (%s,'',"status_txt","公文审批状态","D.status_txt",1,0,103,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,col_type1,col_type,is_index,sort,status)
                      values (%s,'',"view","查看",2,7,0,104,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,col_type1,col_type,is_index,sort,status)
                      values (%s,'',"update","修改",2,2,0,105,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,col_type1,col_type,is_index,sort,status)
                      values (%s,'',"delete","删除",2,3,0,106,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,col_type1,col_type,is_index,sort,status)
                      values (%s,'',"audit","审核",2,5,0,107,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,col_type1,col_type,is_index,sort,status)
                      values (%s,'',"sign","会签",2,8,0,108,1);
                  """%(pk)           
            sql += """insert into menu_list_cols (menu_id,pages,col_name,label,col_type1,col_type,is_index,sort,status)
                      values (%s,'',"verify","登记",2,6,0,109,1);
                  """%(pk)           

            db.executesql(sql)
    else:
        pages = rows[0][1]
        pl = pages.split(',')
        if str(page_id) not in pl:
            pages = "%s,%s"%(pages,page_id) 
            sql = "update menu_list_cols set pages = '%s' where id = %s"%(pages,rows[0][0])
            db.executesql(sql)

    return

def disable_page(pk,page_name,form_table,form_table_ab):
    sql = """update  menu_list_pages set status=0 where menu_id =%s and page_name='%s';"""%(pk,page_name)
    db.executesql(sql)
    #if page_name == 'audit':  
    #    sql = """delete from menu_form_func where menu_id=%s and id=3;"""%(pk)
    #elif page_name == 'verify':  
    #    sql = """delete from menu_form_func where menu_id=%s and id=4;"""%(pk)
    #db.executesql(sql)
    return

def saveStep2(request,data_list):
    pk = data_list.get('pk','')
    lists = data_list.get('pages','')
    n = 0
    for e in lists:
        status = e.get('status','')
        page_id = e.get('page_id',0)
        has_add = e.get('page_add','')
        page_name = e.get('page_name',0)
        label = e.get('page_label','')
        has_add = handleMutilValue(has_add,1)
        if status =='deleted':  #删除行
            sql = "delete from menu_list_pages where id=%s"%(page_id)
        elif status =='exist':
            sql = "update menu_list_pages set sort=%s where id=%s"%(n,page_id)
        else:
            sql = "update menu_list_pages set sort=%s,has_add=%s,page_name='%s',label='%s' where id=%s"%(n,has_add,page_name,label,page_id)
        db.executesql(sql)
        n = n + 1

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%pk
    return HttpResponseCORS(request,s)    

def saveStep3(request,data_list):
    pk = data_list.get('pk','')
    menu_id = data_list.get('menu_id','')
    page_id = data_list.get('page_id','')
    lists = data_list.get('lists','')
    n = 1
    for e in lists:
        #print e
        status = e.get('status','')
        page_list = e.get('lists_page_id','')
        col_name = e.get('lists_col_name','')
        label = e.get('lists_label','')
        memo = e.get('memo','')
        col_type = e.get('lists_col_type','')
        col_id = e.get('lists_col_id',0)
        index = e.get('lists_index','')
        search = e.get('lists_search','')
        order = e.get('lists_order','')
        show = e.get('lists_show','')
        is_index = handleMutilValue(index,1)
        is_search = handleMutilValue(search,1)
        page_list = handleMutilValue(page_list,0)
        if str(col_id) =='0' or str(col_id) =='':  #新添加行
            sql = """insert into menu_list_cols (menu_id,pages,col_name,label,field_show,field_order,col_type,is_index
                             ,sort,can_search,status)
                      values (%s,'%s',"%s","%s","%s","%s",%s,%s,%s,%s,1)
                      """%(menu_id,page_list,col_name,label,show,order,col_type,is_index,n,is_search)           
        elif status =='deleted':  #删除行
            sql = "delete from menu_list_cols where id=%s"%(col_id)
        #elif status =='exist':
        #    sql = "update menu_list_cols set sort=%s where id=%s"%(n,col_id)
        else:  #
            sql = """update menu_list_cols set pages="%s",col_name="%s",label="%s",field_show="%s",field_order="%s",col_type='%s',is_index='%s'
                             ,sort='%s',can_search='%s'
                     where id=%s
                  """%(page_list,col_name,label,show,order,col_type,is_index,n,is_search,col_id)
        #print ToGBK(sql)
        db.executesql(sql)
        n = n + 1

    sql = "select id,table_sql from menu_list_pages where menu_id = %s and status=1"%(menu_id)
    rows,iN = db.select(sql)
    for e in rows:
        page_id = e[0]
        table_sql = e[1] or ''
        sql = "select field_show,col_type,can_search from menu_list_cols where FIND_IN_SET(%s,pages) order by sort"%(page_id)
        rows,iN1 = db.select(sql)
        final_sql,search_sql = sql_encode(rows,table_sql)
        sql = """update menu_list_pages set final_sql="%s",search_sql="%s" where id=%s
              """%(final_sql,search_sql,page_id)
        #print sql
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%pk
    return HttpResponseCORS(request,s)    

def saveStep4(request,data_list):
    pk = data_list.get('pk','')
    menu_id = data_list.get('menu_id','')
    page_id = data_list.get('page_id','')
    pages = data_list.get('pages','')
    funcs = data_list.get('funcs','')
    n = 1
    for e in pages:
        #print e
        status = e.get('status','')
        step_id = e.get('step_id','')
        step_name = e.get('step_name','')
        has_atta = e.get('has_atta','')
        has_atta = handleMutilValue(has_atta,1)
        if str(step_id) =='0' or str(step_id) =='':  #新添加行
            sql = """insert into menu_form_steps (menu_id,step_name,step,has_atta,sort)
                      values (%s,'%s',%s,%s,%s)
                      """%(menu_id,step_name,n,has_atta,n)           
        elif status =='deleted':  #删除行
            sql = "delete from menu_form_steps where id=%s"%(step_id)
        elif status =='exist':
            sql = "update menu_form_steps set sort=%s where id=%s"%(n,step_id)
        else:  #
            sql = """update menu_form_steps set step_name="%s",step="%s",has_atta='%s',sort='%s'
                     where id=%s
                  """%(step_name,n,has_atta,n,step_id)
        print ToGBK(sql)
        db.executesql(sql)
        n = n + 1

    n = 1
    for e in funcs:
        #print e
        status = e.get('status','')
        func_seq = e.get('func_seq','')
        func_id = e.get('func_id','')
        func_ename = e.get('func_ename','')
        func_cname = e.get('func_cname','')
        func_type = e.get('func_type','')
        func_status = e.get('func_status','')

        if str(func_seq) =='0' or str(func_seq) =='':  #新添加行
            sql = "insert into menu_form_func (menu_id,id,ename,cname,type,sort,status) values (%s,%s,'%s','%s',%s,%s,%s)"%(pk,func_id,func_ename,func_cname,func_type,n,func_status)
        elif status =='deleted':  #删除行
            sql = "delete from menu_form_func where seq=%s"%(func_seq)
        elif status =='exist':
            sql = "update menu_form_func set sort=%s where seq=%s"%(n,func_seq)
        else:  #
            sql = """update menu_form_func set id="%s",ename="%s",cname='%s',type='%s',sort='%s',status='%s'
                     where seq=%s
                  """%(func_id,func_ename,func_cname,func_type,n,func_status,func_seq)
        print ToGBK(sql)
        db.executesql(sql)
        n = n + 1

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%pk
    return HttpResponseCORS(request,s)    

def saveStep5(request,data_list):
    pk = data_list.get('pk','')
    menu_id = data_list.get('menu_id','')
    step_id = data_list.get('step_id','')
    lists = data_list.get('lists','')
    if str(menu_id) == '1402' :
        return
    n = 1
    for e in lists:
        #print e
        status = e.get('status','')
        col_id = e.get('lists_col_id',0)
        if status =='deleted':  #删除行
            sql = """delete from menu_form_cols where id=%s;
                     delete from menu_form_save_cols where field_id=%s"""%(col_id,col_id)
        else:  #
            sql = """update menu_form_cols set sort='%s'
                     where id='%s'
                  """%(n,col_id)
        #print sql
        db.executesql(sql)
        n = n + 1


    sql = "select id from menu_form_steps where menu_id = %s and status=1"%(menu_id)
    #print sql
    rows,iN = db.select(sql)
    for e in rows:
        step_id = e[0]
        updateFormSql(step_id)

    sql = """select g.id,g.col_name,c.id,c.col_name,ifnull(c1.id,''),ifnull(c1.col_name,''),c.`para_cols`,c.`change_cols`   from `menu_form_cols` g 
                    left join `menu_form_cols` c on c.step_id=g.step_id and (c.col_name=g.linkfield1 or c.col_name=g.linkfield2)
                    left join `menu_form_cols` c1 on c.step_id=c1.step_id and (c1.col_name=c.linkfield1 or c1.col_name=c.linkfield2)
                    where c.id is not null and g.step_id=%s 
          """%step_id
    rows,iN = db.select(sql)
    for e in rows:
        p_cols = e[3]
        if e[5]!='':
            p_cols = "%s,%s"%(e[3],e[5])
        sql = "update menu_form_cols set `para_cols` = '%s' where `id` =%s"%(p_cols,e[2])
        db.executesql(sql)
        sql = "select ifnull(change_cols,'') from menu_form_cols where id=%s"%e[2]
        rows1,iN1 = db.select(sql)
        c_cols = rows1[0][0]
        c_list = c_cols.split(',')
        print c_list
        if str(e[0]) not in c_list: 
            c_cols += ",%s"%e[0]
            sql = "update menu_form_cols set change_cols='%s' where id=%s"%(c_cols,e[2])
            db.executesql(sql)
        if e[4] !='':
            sql = "select ifnull(change_cols,'') from menu_form_cols where id=%s"%e[4]
            rows1,iN1 = db.select(sql)
            c_cols = rows1[0][0]
            c_list = c_cols.split(',')
            #print c_list
            if str(e[0]) not in c_list: 
                c_cols += ",%s"%e[0]
                sql = "update menu_form_cols set change_cols='%s' where id=%s"%(c_cols,e[4])
                db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%pk
    return HttpResponseCORS(request,s)    

def saveStep6(request,data_list):

    pk = data_list.get('pk','')
    menu_id = data_list.get('menu_id','')
    step_id = data_list.get('step_id','')
    parent_id = data_list.get('list_id','')
    lists = data_list.get('list_cols','')
    if str(menu_id) == '1402' :
        return
    n = 1
    for e in lists:
        print e
        status = e.get('status','')
        col_id = e.get('list_cols_col_id',0)
        col_name = e.get('list_cols_col_name','')
        label = e.get('list_cols_label','')
        if status =='deleted':  #删除行
            sql = """delete from menu_form_cols where id=%s;
                     delete from menu_form_save_cols where field_id=%s"""%(col_id,col_id)
            db.executesql(sql)
        else:  #
            sql = """update menu_form_cols set sort='%s',col_name='%s',label='%s'
                     where id='%s'
                  """%(n,col_name,label,col_id)
            db.executesql(sql)
        n = n + 1
    if parent_id!='':
        updateGridSql(parent_id)

        sql = """select g.id,g.col_name,c.id,c.col_name,ifnull(c1.id,''),ifnull(c1.col_name,''),c.`para_cols`,c.`change_cols`   from `menu_form_cols` g 
                        left join `menu_form_cols` c on c.step_id=g.step_id and (c.col_name=g.linkfield1 or c.col_name=g.linkfield2)
                        left join `menu_form_cols` c1 on c.step_id=c1.step_id and (c1.col_name=c.linkfield1 or c1.col_name=c.linkfield2)
                        where c.id is not null and g.parent_id=%s 
              """%parent_id
        rows,iN = db.select(sql)
        for e in rows:
            p_cols = e[3]
            if e[5]!='':
                p_cols = "%s,%s"%(e[3],e[5])
            sql = "update menu_form_cols set `para_cols` = '%s' where `id` =%s"%(p_cols,e[2])
            db.executesql(sql)
            sql = "select ifnull(change_cols,'') from menu_form_cols where id=%s"%e[2]
            rows1,iN1 = db.select(sql)
            c_cols = rows1[0][0]
            c_list = c_cols.split(',')
            #print c_list
            if str(e[0]) not in c_list: 
                c_cols += ",%s"%e[0]
                sql = "update menu_form_cols set change_cols='%s' where id=%s"%(c_cols,e[2])
                db.executesql(sql)
            if e[4] !='':
                sql = "select ifnull(change_cols,'') from menu_form_cols where id=%s"%e[4]
                rows1,iN1 = db.select(sql)
                c_cols = rows1[0][0]
                c_list = c_cols.split(',')
                #print c_list
                if str(e[0]) not in c_list: 
                    c_cols += ",%s"%e[0]
                    sql = "update menu_form_cols set change_cols='%s' where id=%s"%(c_cols,e[4])
                    db.executesql(sql)

    lists = data_list.get('list_default','')
    n = 1
    for e in lists:
        #print e
        status = e.get('status','')
        col_id = e.get('default_mxid',0)
        default_sql = e.get('default_sql','')
        default_cols = e.get('default_cols','')
        link_list = e.get('default_link','')
        link_cols = handleMutilValue(link_list,0)
        if status =='deleted':  #删除行
            sql = """delete from menu_form_steps_default where id=%s;"""%(col_id)
            db.executesql(sql)
        elif status =='newAdd':  #
            sql = """insert into menu_form_steps_default (step_id,default_sql,default_cols,link_cols,sort)
                     values (%s,"%s",'%s','%s',%s)
                  """%(step_id,default_sql,default_cols,link_cols,n)
            db.executesql(sql)
        else:
            sql = """update menu_form_steps_default set sort='%s',default_sql="%s",default_cols='%s',link_cols='%s'
                     where id='%s'
                  """%(n,default_sql,default_cols,link_cols,col_id)
            db.executesql(sql)
        add_change_cols(step_id,link_list,default_cols,default_sql)
        n = n + 1

    lists = data_list.get('list_cal','')
    n = 1
    for e in lists:
        #print e
        status = e.get('status','')
        col_id = e.get('list_cal_id',0)
        if status =='deleted':  #删除行
            sql = """delete from menu_form_calculate where id=%s;"""%(col_id)
            db.executesql(sql)
        else:
            sql = """update menu_form_calculate set sort=%s
                     where id='%s'
                  """%(n,col_id)
            db.executesql(sql)
        n = n + 1

    lists = data_list.get('list_show','')
    n = 1
    for e in lists:
        #print e
        status = e.get('status','')
        col_id = e.get('list_show_id',0)
        field_id = e.get('list_show_field_id','')
        operator = e.get('list_show_operator','')
        conditional = e.get('list_show_conditional','')
        check_field = e.get('list_show_check_field','')
        value = e.get('list_show_value','')
        if status =='deleted':  #删除行
            sql = """delete from menu_form_show where id=%s;"""%(col_id)
            db.executesql(sql)
        elif status =='newAdd':  #
            sql = """insert into menu_form_show (field_id,operator,conditional,check_field,value)
                     values (%s,'%s',"%s",'%s','%s')
                  """%(field_id,operator,conditional,check_field,value)
            db.executesql(sql)
        else:
            sql = """update menu_form_show set field_id='%s',operator='%s',conditional="%s",check_field='%s',value='%s'
                     where id='%s'
                  """%(field_id,operator,conditional,check_field,value,col_id)
            db.executesql(sql)
        n = n + 1

    lists = data_list.get('list_validty','')
    n = 1
    for e in lists:
        #print e
        status = e.get('status','')
        col_id = e.get('list_validty_id',0)
        field_id = e.get('list_validty_field_id','')
        conditional = e.get('list_validty_conditional','')
        check_field = e.get('list_validty_check_field','')
        tips = e.get('list_validty_tips','')
        if status =='deleted':  #删除行
            sql = """delete from menu_form_validity where id=%s;"""%(col_id)
            db.executesql(sql)
        elif status =='newAdd':  #
            sql = """insert into menu_form_validity (field_id,conditional,check_field,tips)
                     values (%s,"%s",'%s','%s')
                  """%(field_id,conditional,check_field,tips)
            db.executesql(sql)
        else:
            sql = """update menu_form_validity set field_id='%s',conditional="%s",check_field='%s',tips='%s'
                     where id='%s'
                  """%(field_id,conditional,check_field,tips,col_id)
            db.executesql(sql)
        n = n + 1

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%pk
    return HttpResponseCORS(request,s)   
def add_change_cols(step_id,link_cols,default_cols,sql):
    pos1 = sql.find("{")
    paras = []
    while pos1>0 :
        pos2 = sql.find("}")
        key = sql[pos1+1:pos2]
        paras.append(key)
        sql = sql.replace("{%s}"%key,'')
        pos1 = sql.find("{")

    for e in link_cols:
        sql = "select id,ifnull(change_cols,''),ifnull(para_cols,'') from menu_form_cols where id=%s"%(e)
        rows,iN = db.select(sql)
        if iN>0:
            id = rows[0][0]
            c_cols = rows[0][1]
            c_list = c_cols.split(',')
            d_list = default_cols.split(',')
            for e1 in d_list:
                sql1 = "select id from menu_form_cols where step_id=%s and col_name = '%s'"%(step_id,e1)
                rows1,iN1 = db.select(sql1)
                if iN1>0 and str(rows1[0][0]) not in c_list: 
                    c_cols += ",%s"%rows1[0][0]
            p_cols = rows[0][2]
            p_list = p_cols.split(',')
            for e2 in paras:
                if e2 not in p_list: 
                    p_cols += ",%s"%e2

            sql = "update menu_form_cols set change_cols='%s',para_cols='%s' where id=%s"%(c_cols,p_cols,id)
            db.executesql(sql)          
        
    return

def saveStep11(request,data_list):
    #print data_list
    menu_id = data_list.get('menu_id','')
    page_id = data_list.get('page_id','')
    lists = data_list.get('lists','')
    n = 0
    for e in lists:
        print e 
        status = e.get('status','')
        table_id = e.get('table_id',0)
        table_name = e.get('table_name','')
        table_sql = e.get('table_sql','')
        table_ab = e.get('table_ab','')
        table_name = table_name.strip()
        table_ab = table_ab.strip()
        table_sql = table_sql.strip()
        menu_table_id = e.get('menu_table_id',0)
        if 1==1:#str(menu_table_id)=='0':  
            if table_sql != '':
                sql = """select id,table_name from menu_tables where table_sql="%s" and type=1
                      """%(table_sql)
                print sql
                rows,iN = db.select(sql)
                if iN == 0:
                    col_list,table_name1 = decode_table_sql(table_sql)
                    table_name = "%s_temp"%(table_name1)
                    sql = "SELECT max(table_name) FROM menu_tables WHERE table_name like '%s%%'"%table_name
                    lT,iN=db.select(sql)
                    if lT[0][0] is not None:
                        i=str(int(lT[0][0][-3:])+1)
                        if len(i)==1:#避免在转换成数字时缺少位数，如：字符串01转成数字时就变成了1
                            i='00%s'%i
                        elif len(i)==2:
                            i='0%s'%i
                        table_name='%s%s'%(table_name,i)
                    else:
                        table_name='%s001'%(table_name)

                    sql = """insert into menu_tables (table_name,table_sql,type) values ("%s","%s",1)
                              """%(table_name,table_sql)
                    print sql
                    db.executesql(sql)
                    sql = "select last_insert_id();"
                    rows,iN = db.select(sql)  
                    menu_table_id = rows[0][0]
                    #print menu_table_id
                    for e in col_list:
                        try:
                            col_name = e.upper()
                            col_name = col_name.split('AS')[1]
                            col_name = col_name.strip()
                        except:
                            col_name = e.strip()
                        sql = "insert into menu_table_cols (table_id,col_name) values (%s,'%s')"%(menu_table_id,col_name)
                        #print sql 
                        db.executesql(sql)
                else:
                    menu_table_id = rows[0][0]
                    table_name = rows[0][1]
            elif table_name != '':
                sql = "select id from menu_tables where table_name='%s' and type=0"%(table_name)
                #print sql
                rows,iN = db.select(sql)
                if iN == 0:
                    sql = "insert into menu_tables (table_name,type) values ('%s',0)"%(table_name)
                    db.executesql(sql)
                    sql = "select last_insert_id();"
                    rows,iN = db.select(sql)  
                    menu_table_id = rows[0][0]
                else:
                    menu_table_id = rows[0][0]
        #print "menu_table_id=%s"%menu_table_id
        if table_ab == '':
            table_ab = table_name
        if str(table_id) =='0' or str(table_id) =='':  #新添加行
            if menu_table_id!=0:
                sql = """insert into menu_list_tables 
                      (menu_id,page_id,table_name,table_sql,table_ab,menu_table_id,sort)
                      values (%s,%s,'%s',"%s",'%s',%s,%s)
                      """%(menu_id,page_id,table_name,table_sql,table_ab,menu_table_id,n)           
        elif status =='deleted':  #删除行
            sql = "delete from menu_list_tables where id=%s"%(table_id)
        elif status =='exist':
            sql = "update menu_list_tables set sort=%s where id=%s"%(n,table_id)
        else:  #
            sql = """update menu_list_tables set table_name='%s',table_ab='%s',table_sql="%s",menu_table_id=%s,sort=%s
                     where id=%s
                  """%(table_name,table_ab,table_sql,menu_table_id,n,table_id)
        print sql
        db.executesql(sql)
        n = n + 1

    L = [[1,'','','',1]]
    L[0][0] = page_id
    L[0][1] = ''
    L[0][2] = ''
    L[0][3] = ''
    L[0][4] = get_options_data(menu_id,'','',6,'','',0,'','',False)
    names = 'page_id page_table del_sql page_order finish'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'pages '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      
    
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    return s

def saveStep12(request,data_list):
    menu_id = data_list.get('menu_id','')
    page_id = data_list.get('page_id','')
    lists = data_list.get('lists','')
    deletes = data_list.get('delete_sql','')
    where_sql = data_list.get('where_sql','')
    n = 1
    for e in lists:
        print e
        status = e.get('status','')
        table_id = e.get('table_id','')
        join_type = e.get('join_type','')
        table = e.get('table_name','')
        index_name = e.get('table_index','')
        link = e.get('link_ab','')
        if link!='':
            link_table = link.split(' ')[0]
            link_ab = link.split(' ')[1]
        else:
            link_table = ''
            link_ab = ''
        if table!='':
            table_name = table.split(' ')[0]
            table_ab = table.split(' ')[1]
        else:
            table_name = ''
            table_ab = ''
        link_index = e.get('link_index','')
        if status =='newAdd':  #新添加行
            sql = """insert into menu_list_tables 
                      (menu_id,page_id,join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,sort)
                    values (%s,%s,'%s','%s','%s','%s','%s','%s','%s',%s)
                  """%(menu_id,page_id,join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,n)
            
        elif status =='updated':  #
            sql = """update menu_list_tables set join_type='%s'
                         ,table_name='%s',table_ab='%s',index_name='%s',link_table='%s',link_ab='%s',link_index='%s',sort=%s
                     where id=%s
                  """%(join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,n,table_id)
        elif status =='deleted':  #删除行
            sql = "delete from menu_list_tables where id=%s"%(table_id)
        else:
            sql = "update menu_list_tables set sort=%s where id=%s"%(n,table_id)
        print sql
        db.executesql(sql)
        n = n + 1
    sql = "select join_type,table_name,table_ab,index_name,link_ab,link_index,ifnull(table_sql,'') from menu_list_tables where page_id = %s  order by sort"%(page_id)
    #print sql
    rows,iN = db.select(sql)
    table_sql = encode_table_sql(rows)
    
    n = 0
    for e in deletes:
        status = e.get('status','')
        del_id = e.get('del_id',0)
        del_sql = e.get('del_sql','')
        if str(del_id) =='0' or str(del_id) =='':
            sql = """insert into menu_list_pages_del (pages,delete_sql,sort) values ('%s,',"%s",%s)
                  """%(page_id,del_sql,n)
        elif status =='deleted':  #删除行
            sql = "delete from menu_list_pages_del where id=%s"%(del_id)
        elif status =='exist':
            sql = "update menu_list_pages_del set sort=%s where id=%s"%(n,del_id)
        else:  #
            sql = """update menu_list_pages_del set delete_sql="%s",sort=%s
                     where id=%s
                  """%(del_sql,n,del_id)
        #print sql
        db.executesql(sql)
        n = n + 1
    sql = "select delete_sql from menu_list_pages_del where FIND_IN_SET(%s,pages) order by sort"%(page_id)
    #print sql
    rows,iN = db.select(sql)
    del_sql = ""
    for e in rows:
        del_sql += "%s;"%e[0]

    if where_sql=='':
        where_sql = "WHERE 1=1 "
    table_sql = '%s %s'%(table_sql,where_sql)
    sql = """update menu_list_pages set table_sql="%s",delete_sql="%s",where_sql="%s" where id=%s
                  """%(table_sql,del_sql,where_sql,page_id)
    #print sql
    db.executesql(sql)

    L = [[1,'','','',1]]
    L[0][0] = page_id
    L[0][1] = ''
    L[0][2] = ''
    L[0][3] = ''
    L[0][4] = get_options_data(menu_id,'','',6,'','',0,'','',False)
    names = 'page_id page_table del_sql page_order finish'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'pages '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      
    
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    return s

def saveStep13(request,data_list):
    menu_id = data_list.get('menu_id','')
    page_id = data_list.get('page_id','')
    table_sql = data_list.get('table_sql','')
    delete_sql = data_list.get('delete_sql','')
    order_sql = data_list.get('order_sql','')
    lists = data_list.get('lists','')
    deletes = data_list.get('lists1','')
    n = 0
    for e in lists:
        status = e.get('status','')
        lists_id = e.get('lists_id','')
        lists_page_id = e.get('lists_page_id','')
        lists_para_type = e.get('lists_para_type','')
        lists_link_name = e.get('lists_link_name','')

        if str(lists_id) =='0' or str(lists_id) =='':  #新添加行
            sql = """insert into menu_list_pages_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,%s,'%s',%s)
                      """%(page_id,lists_para_type,lists_link_name,n)
        elif status =='deleted':  #删除行
            sql = "delete from menu_list_pages_para where id=%s"%(lists_id)
        elif status =='exist':
            sql = "update menu_list_pages_para set sort=%s where id=%s"%(n,lists_id)
        else:  #
            sql = """update menu_list_pages_para set para_type='%s',link_field='%s',sort=%s
                     where id=%s
                  """%(lists_para_type,lists_link_name,n,lists_id)
        print sql
        db.executesql(sql)
        n = n + 1

    n = 0
    for e in deletes:
        status = e.get('status','')
        lists_id = e.get('lists1_id','')
        lists_page_id = e.get('lists1_page_id','')
        lists_para_type = e.get('lists1_para_type','')
        lists_link_name = e.get('lists1_link_name','')

        if str(lists_id) =='0' or str(lists_id) =='':  #新添加行
            sql = """insert into menu_list_pages_del_para 
                      (page_id,para_type,link_field,sort)
                      values (%s,%s,'%s',%s)
                      """%(page_id,lists_para_type,lists_link_name,n)
        elif status =='deleted':  #删除行
            sql = "delete from menu_list_pages_del_para where id=%s"%(lists_id)
        elif status =='exist':
            sql = "update menu_list_pages_del_para set sort=%s where id=%s"%(n,lists_id)
        else:  #
            sql = """update menu_list_pages_del_para set para_type='%s',link_field='%s',sort=%s
                     where id=%s
                  """%(lists_para_type,lists_link_name,n,lists_id)
        print sql
        db.executesql(sql)
        n = n + 1
    
    sql = """update menu_list_pages set list_order="%s",finish=1,status=1 where id=%s
                  """%(order_sql,page_id)
    print sql
    db.executesql(sql)

    L = [[1,'','','',1]]
    L[0][0] = page_id
    L[0][1] = table_sql
    L[0][2] = delete_sql
    L[0][3] = order_sql
    L[0][4] = get_options_data(menu_id,'','',6,'','',1,'','',False)
    names = 'page_id page_table del_sql page_order finish'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'pages '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      
    
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def saveStep21(request,data_list):
    #print data_list
    status = data_list.get('status',1)
    linkfield2 = data_list.get('linkfield2','')
    linkfield1 = data_list.get('linkfield1','')
    field_options_default = data_list.get('field_options_default','')
    field_options_type = data_list.get('field_options_type') or 'NULL'
    id = data_list.get('id','')
    ssize = data_list.get('size') or 'NULL'
    default_value = data_list.get('default_value','')
    field_type = data_list.get('field_type') or 'NULL'
    hint = data_list.get('hint','')
    tip = data_list.get('tip','')
    enable_list = data_list.get('enables','') 
    required_list = data_list.get('requireds','') 
    readonly_list = data_list.get('readonlys','') 
    hide_list = data_list.get('hides','') 
    label = data_list.get('label','')
    page_name = data_list.get('page_name','')
    max_length = data_list.get('max_length') or '0'
    memo = data_list.get('memo','')
    menu_id = data_list.get('menu_id') or 'NULL'
    step_id = data_list.get('step_id') or 'NULL'
    page_id = data_list.get('page_id') or 'NULL'
    btn_type = data_list.get('btn_type','')
    btn_color = data_list.get('btn_color','')
    field_show = data_list.get('field_show','')
    field_show = MySQLdb.escape_string(field_show)
    col_name = data_list.get('col_name','')
    default_type = data_list.get('default_type') or 'NULL'
    field_options_txt = data_list.get('field_options_txt','')
    field_options_txt1 = data_list.get('field_options_txt1','')
    url = data_list.get('url','')
    table_name = data_list.get('table_name','')
    field_col_name = data_list.get('field_col_name','')
    
    save_list = data_list.get('saves','') 
    save_para = data_list.get('save_para','') 

    saves = handleMutilValue(save_list,0)
    save_para = handleMutilValue(save_para,0)
    enables = handleMutilValue(enable_list,0)
    requireds = handleMutilValue(required_list,0)
    readonlys = handleMutilValue(readonly_list,0)
    hides = handleMutilValue(hide_list,0)

    new_field = data_list.get('new_field','') 
    new_field = handleMutilValue(new_field,1)
    if '3' in save_para.split(','): 
        is_number = 1
    else:
        is_number = 0
    if str(field_options_type) == '1':
        field_options = field_options_txt
    else:
        field_options = field_options_txt1
    if str(field_type) == '22':
        if btn_type == 'pdf':
            url = 'common/printPDF?field_id=%s'%(id)
        elif url =='':
            url = 'common/savePageForm' 
    #新建字段
    if str(new_field) == '1' and table_name!='' and col_name!='':
        sql="select column_name from information_schema.columns where table_schema='%s' and table_name='%s' and column_name='%s'"%(m_dbname,table_name,col_name)
        rows,iN = db.select(sql)
        if str(field_type) in ['8','19']:
            ftype = 'decimal(18,2)'
        elif is_number==1:
            ftype = 'int'
        elif str(field_type) in ['4','27']:
            ftype = 'text'
        else:
            if str(max_length) == '0':
                ftype = 'varchar(50)'
            else:
                ftype = 'varchar(%s)'%max_length
        if iN == 0:
            sql = "alter table %s add %s %s Null COMMENT '%s';"%(table_name,col_name,ftype,label)
            #print sql
            db.executesql(sql)
        field_col_name = col_name

    add_list = data_list.get('add_list','') 
    list_sql = data_list.get('list_sql','') 
    add_list = handleMutilValue(add_list,1)
    #新建列表字段
    if str(add_list) == '1' and list_sql!='' and col_name!='':
        sql = "select id from menu_list_cols where menu_id=%s and col_name='%s'"%(menu_id,col_name)
        rows,iN = db.select(sql)
        if iN == 0:
            sql = "select id from menu_list_pages where menu_id=%s"%(menu_id)
            rows1,iN1 = db.select(sql)
            pages = ''
            for e1 in rows1:
                pages += '%s,'%e1[0]
            sql = """insert into menu_list_cols (menu_id,pages,col_name,label,field_show,field_order,col_type,is_index
                             ,sort,can_search,status)
                      values (%s,'%s',"%s","%s","%s","%s",1,0,2,1,1)
                      """%(menu_id,pages,col_name,label,list_sql,field_col_name)   
            #print ToGBK(sql)  
            db.executesql(sql)

    sql = """update menu_form_cols SET 
                        step_id=%s,
                        col_name='%s',
                        label='%s',
                        field_col_name="%s",
                        field_type=%s,
                        enables='%s',
                        requireds='%s',
                        readonlys='%s',
                        hides='%s',
                        size=%s,
                        default_type=%s,
                        default_value='%s',
                        max_length=%s,
                        tip='%s',
                        memo="%s",
                        hint='%s',
                        field_options_type=%s,
                        field_options_txt="%s",
                        field_options_default='%s',
                        btn_type='%s',
                        btn_color='%s',
                        url='%s',
                        linkfield1='%s',
                        linkfield2='%s',
                        status='%s',
                        menu_id='%s',
                        show_table='%s',
                        show_col_name='%s',
                        is_number=%s,
                        saves='%s',
                        save_para='%s',
                        add_list='%s',
                        list_sql="%s"
                where id = '%s';
        """%(step_id,col_name,label,field_show,field_type,enables,requireds,readonlys,hides,ssize
           ,default_type,default_value,max_length,tip,memo,hint,field_options_type,field_options,field_options_default
           ,btn_type,btn_color,url,linkfield1,linkfield2,status,menu_id,table_name,field_col_name,is_number
           ,saves,save_para,add_list,list_sql,id)
    #print ToGBK(sql)
    db.executesql(sql)

    if field_col_name !='':
        sql = "select id from menu_form_save_tables where step_id = %s and save_table='%s';"%(step_id,table_name)
        rows,iN = db.select(sql)
        if iN==0:
            sql = "insert into menu_form_save_tables (step_id,save_table,is_list,del_before_update,is_procedure,status) values (%s,'%s',0,0,0,1)"%(step_id,table_name)
            rows,iN = db.select(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
        table_id = rows[0][0]
        if str(default_type) == '13': #自动编号
            is_auto_sn = 1
        else:
            is_auto_sn = 0

        if '1' in save_para.split(','): 
            is_identity = 1
        else:
            is_identity = 0
        if '2' in save_para.split(','): 
            is_index = 1
        else:
            is_index = 0
        if '4' in save_para.split(','): 
            is_unique = 1
        else:
            is_unique = 0
        if '1' in saves.split(','): 
            is_add = 1
        else:
            is_add = 0
        if '2' in saves.split(','): 
            is_upd = 1
        else:
            is_upd = 0
        if '3' in saves.split(','): 
            is_audit = 1
        else:
            is_audit = 0
        if '4' in saves.split(','): 
            is_verify = 1
        else:
            is_verify = 0
    
        sql = "select id from menu_form_save_cols where field_id = %s;"%id
        rows,iN = db.select(sql)
        if iN == 0:
            sql = """insert into menu_form_save_cols (table_id,save_field_name,is_identity,is_number,is_unique,default_type,request_name
                        ,is_add,is_upd,is_index,is_del,is_audit,is_verify,menu_id,data_table,field_id,is_auto_sn)
                        values(%s,'%s',%s,%s,%s,8,'%s',%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s);
                  """%(table_id,field_col_name,is_identity,is_number,is_unique,col_name
                        ,is_add,is_upd,is_index,is_index,is_audit,is_verify,menu_id,table_name,id,is_auto_sn)
        else:
            sql = """update menu_form_save_cols SET 
                            table_id='%s',
                            save_field_name='%s',
                            is_identity='%s',
                            is_number='%s',
                            is_unique='%s',
                            default_type=8,
                            request_name='%s',
                            is_add='%s',
                            is_upd='%s',
                            is_index='%s',
                            is_del='%s',
                            is_audit='%s',
                            is_verify='%s',
                            is_auto_sn='%s',
                            menu_id='%s',
                            data_table='%s'
                        where field_id = %s;
                  """%(table_id,field_col_name,is_identity,is_number,is_unique,col_name
                        ,is_add,is_upd,is_index,is_index,is_audit,is_verify,is_auto_sn,menu_id,table_name,id)
        #print ToGBK(sql)
        db.executesql(sql)

    L = [[1,1,'','','',1,'']]
    L[0][0] = id
    L[0][1] = step_id
    L[0][2] = col_name
    L[0][3] = label
    L[0][4] = field_show
    L[0][5] = get_options_data(menu_id,'','',16,'','',field_type,'','')
    L[0][6] = get_options_data(menu_id,'','',3,'select id,cname from menu_form_func where menu_id=$s and status=1 and type in(1,2)','',enables,menu_id,'',False)

    names = 'lists_col_id lists_step_id lists_col_name lists_label lists_show lists_col_type lists_func'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'lists '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def saveStep22(request,data_list):
    field_id = data_list.get('id','')
    sel_type = data_list.get('sel_type','')
    show_list = data_list.get('show_cols','')
    show_cols = handleMutilValue(show_list,0)
    btn_id = data_list.get('btn_id','')

    if btn_id == '':
        sql = "update menu_form_cols set sel_type=%s,sel_cols='%s' where id=%s"%(sel_type,show_cols,field_id)
        #print sql
        db.executesql(sql)
        for e in  show_list:
            sql = "select id from menu_form_select_cols where sel_col_id=%s and field_id=%s"%(e,field_id)
            #print sql
            rows,iN = db.select(sql)
            if iN == 0:
                sql = "insert into menu_form_select_cols (sel_col_id,field_id) values (%s,%s)"%(e,field_id)      
                db.executesql(sql)      
    else:
        sql = "update menu_form_grid_button set sel_type=%s,sel_cols='%s' where id=%s"%(sel_type,show_cols,btn_id)
        #print sql
        db.executesql(sql)
        for e in  show_list:
            sql = "select id from menu_form_select_cols where sel_col_id=%s and btn_id=%s"%(e,btn_id)
            print sql
            rows,iN = db.select(sql)
            if iN == 0:
                sql = "insert into menu_form_select_cols (sel_col_id,field_id,btn_id) values (%s,%s,%s)"%(e,field_id,btn_id)      
                print sql
                db.executesql(sql)      

    formData = []
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def saveStep23(request,data_list):
    field_id = data_list.get('id','')
    sel_type = data_list.get('sel_type','')
    show_list = data_list.get('show_cols','')
    show_cols = handleMutilValue(show_list,0)
    col_list = data_list.get('col_list','')
    btn_id = data_list.get('btn_id','')
    
    if btn_id == '':
        n = 1
        for e in col_list:
            print e
            status = e.get('status','')
            list_id = e.get('list_id',0)
            sel_col_id = e.get('sel_col_id','')
            list_field_id = e.get('list_field_id') or 'NULL'
            if str(list_id) =='0':  #新添加行
                sql = "insert into menu_form_select_cols (sel_col_id,field_id,field_id1,sel_type,sort) values (%s,%s,%s,%s,%s)"%(sel_col_id,field_id,list_field_id,sel_type,n)      
            elif status =='deleted':  #删除行
                sql = "delete from menu_form_select_cols where id=%s"%(list_id)
            else:  #
                sql = "update menu_form_select_cols set sel_col_id=%s,field_id1=%s,sort=%s where id=%s"%(sel_col_id,list_field_id,n,list_id)
            #print sql
            db.executesql(sql)
            n += 1

        para_list = data_list.get('para_list','')
        n = 1
        for e in para_list:
            #print e
            status = e.get('status','')
            list_id = e.get('para_list_id',0)
            para_name = e.get('para_name','')
            list_field_name = e.get('list_field_name','') 
            if str(list_id) =='0' or str(list_id) =='' :  #新添加行
                sql = "insert into menu_form_url_para (field_id,para_name,link_field,sort) values ('%s','%s','%s',%s)"%(field_id,para_name,list_field_name,n)      
            elif status =='deleted':  #删除行
                sql = "delete from menu_form_url_para where id=%s"%(list_id)
            #elif status =='exist':
            #    sql = "update menu_form_url_para set sort=%s where id=%s"%(n,list_id)
            else:  #
                sql = "update menu_form_url_para set para_name='%s',link_field='%s',sort=%s where id=%s"%(para_name,list_field_name,n,list_id)
            #print sql
            db.executesql(sql)
            n += 1
    else:
        n = 1
        for e in col_list:
            #print e
            status = e.get('status','')
            list_id = e.get('list_id',0)
            sel_col_id = e.get('sel_col_id','')
            list_field_id = e.get('list_field_id') or 'NULL'
            if str(list_id) =='0':  #新添加行
                sql = "insert into menu_form_select_cols (sel_col_id,field_id,field_id1,sel_type,sort,btn_id) values (%s,%s,%s,%s,%s,%s)"%(sel_col_id,field_id,list_field_id,sel_type,n,btn_id)      
            elif status =='deleted':  #删除行
                sql = "delete from menu_form_select_cols where id=%s"%(list_id)
            else:  #
                sql = "update menu_form_select_cols set sel_col_id=%s,field_id1=%s,sort=%s where id=%s"%(sel_col_id,list_field_id,n,list_id)
            #print sql
            db.executesql(sql)
            n += 1

        para_list = data_list.get('para_list','')
        n = 1
        for e in para_list:
            #print e
            status = e.get('status','')
            list_id = e.get('para_list_id',0)
            para_name = e.get('para_name','')
            list_field_name = e.get('list_field_name','') 
            if str(list_id) =='0' or str(list_id) =='' :  #新添加行
                sql = "insert into menu_form_url_para (field_id,para_name,link_field,sort,btn_id) values ('%s','%s','%s',%s,%s)"%(field_id,para_name,list_field_name,n,btn_id)      
            elif status =='deleted':  #删除行
                sql = "delete from menu_form_url_para where id=%s"%(list_id)
            #elif status =='exist':
            #    sql = "update menu_form_url_para set sort=%s where id=%s"%(n,list_id)
            else:  #
                sql = "update menu_form_url_para set para_name='%s',link_field='%s',sort=%s where id=%s"%(para_name,list_field_name,n,list_id)
            #print sql
            db.executesql(sql)
            n += 1
        
    formData = []
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def saveStep26(request,data_list):
    menu_id = data_list.get('menu_id','')
    menu_name = data_list.get('menu_name','')
    col_name = data_list.get('col_name','')
    step_id = data_list.get('step_id','')
    field_id = data_list.get('field_id','')
    new_table_name = data_list.get('new_table_name','')
    form_table = data_list.get('form_table','')
    upd_sql = data_list.get('upd_sql','')
    add_sql = data_list.get('add_sql','')
    default_sql = data_list.get('default_sql','')
    view_sql = data_list.get('view_sql','')
    is_add_col = data_list.get('is_add_col','')
    is_add_col = handleMutilValue(is_add_col,1)

    sql = "SELECT has_audit from menu_data_source where menu_id=%s"%menu_id
    rows,iN = db.select(sql)
    if iN>0:
        has_audit = rows[0][0] or 0

    #新建明细表
    if new_table_name != '':
        if has_audit == 1:
            link = 'gw_id'
        else:
            link = 'm_id'

        sql = "select `TABLE_NAME` from `INFORMATION_SCHEMA`.`TABLES` where `TABLE_SCHEMA`='%s' and `TABLE_NAME`='%s' and table_type='base table' "%(m_dbname,new_table_name)
        rows,iN = db.select(sql)
        if iN == 0:
            sql = """create table %s(
                        id INT NOT NULL AUTO_INCREMENT,
                        %s INT,
                        status TINYINT COMMENT '状态',
                        cid INT COMMENT '建立人ID',
                        cusrname  VARCHAR(50)  COMMENT '建立人',
                        ctime datetime COMMENT '建立时间',
                        uid INT COMMENT '修改人ID',
                        uusrname  VARCHAR(50)  COMMENT '修改人',
                        utime datetime COMMENT '修改时间',
                        PRIMARY KEY ( id )
                  )comment='自动创建：%s明细表';"""%(new_table_name,link,menu_name)
            db.executesql(sql)
        form_table = new_table_name
    sql = "SELECT id from `menu_form_grid_sql` where `field_id` =%s "%(field_id)
    rows,iN = db.select(sql)
    upd_table = getTableSql(upd_sql)
    add_table = getTableSql(add_sql)
    default_table = getTableSql(default_sql)
    view_table = getTableSql(view_sql)
    if iN == 0:
        sql = """insert into `menu_form_grid_sql` (`field_id`,`table_name`,`default_sql`,`default_table`,`add_sql`,`add_table`,`view_sql`,`view_table`,`final_sql`,`final_table`,`status`)
                 values ('%s','%s',"%s","%s","%s","%s","%s","%s","%s","%s",1)
              """%(field_id,form_table,default_sql,default_table,add_sql,add_table,view_sql,view_table,upd_sql,upd_table)
        print ToGBK(sql)
        db.executesql(sql)
    else:
        sql = """update `menu_form_grid_sql` SET 
                        `table_name`='%s',
                        `default_sql`="%s",
                        `default_table`="%s",
                        `add_sql`="%s",
                        `add_table`="%s",
                        `view_sql`="%s",
                        `view_table`="%s",
                        `final_sql`="%s",
                        `final_table`="%s"
                where id=%s"""%(form_table,default_sql,default_table,add_sql,add_table,view_sql,view_table,upd_sql,upd_table,rows[0][0])    
        db.executesql(sql)
    if str(is_add_col) == '1':
        L = decodeGridSql(upd_sql)
        n = 1
        for e in L:
            sql = """insert into menu_form_cols (menu_id,step_id,col_name,label,show_col_name,is_grid,parent_id
                             ,sort,status)
                      values (%s,%s,"%s","%s","%s",1,%s,%s,1)
                      """%(menu_id,step_id,e[0],e[2],e[1],field_id,n)   
            #print sql
            db.executesql(sql)

    has_add = data_list.get('has_add','')
    has_add = handleMutilValue(has_add,1)
    has_del = data_list.get('has_del','')
    has_del = handleMutilValue(has_del,1)
    has_order = data_list.get('has_order','')
    has_order = handleMutilValue(has_order,1)
    has_import = data_list.get('has_import','')
    has_import = handleMutilValue(has_import,1)
    import_name = data_list.get('import_name','')
    has_import_from_file = data_list.get('has_import_from_file','')
    has_import_from_file = handleMutilValue(has_import_from_file,1)
    file_btn_name = data_list.get('file_btn_name','')
    has_single_import = data_list.get('has_single_import','')
    has_single_import = handleMutilValue(has_single_import,1)
    single_name = data_list.get('single_name','')

    sql = "SELECT id from `menu_form_grid_setting` where `field_id` =%s "%(field_id)
    rows,iN = db.select(sql)
    if iN == 0:
        sql = """insert into `menu_form_grid_setting` (`field_id`,has_add,has_del,has_order
                 ,has_import,import_name,has_import_from_file,file_btn_name,has_single_import,single_name)
                 values ('%s',%s,%s,%s,%s,'%s',%s,'%s',%s,'%s')
              """%(field_id,has_add,has_del,has_order,has_import,import_name,has_import_from_file,file_btn_name,has_single_import,single_name)
        print ToGBK(sql)
        db.executesql(sql)
    else:
        sql = """update `menu_form_grid_setting` SET 
                        `has_add`=%s,
                        `has_del`=%s,
                        `has_order`=%s,
                        `has_import`=%s,
                        `import_name`="%s",
                        `has_import_from_file`=%s,
                        `file_btn_name`="%s",
                        `has_single_import`=%s,
                        `single_name`="%s"
                where field_id=%s"""%(has_add,has_del,has_order,has_import,import_name,has_import_from_file,file_btn_name,has_single_import,single_name,field_id)    
        print ToGBK(sql)
        db.executesql(sql)

    formData = []
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def getTableSql(sql):
    if sql == '':
        return ''
    sql = sql.lower()
    #只保留一个空格
    import re
    sql = re.sub(r'\s+', ' ', sql)
    iPos = sql.find(' from ')
    table_sql = sql[iPos+1:]
    return table_sql    

def decodeGridSql(sql):
    if sql == '':
        return ''
    sql = sql.lower()
    #只保留一个空格
    import re
    sql = re.sub(r'\s+', ' ', sql)
    iPos = sql.find(' from ')
    field_sql = sql[:iPos]
    field_sql = field_sql.replace('select ','')
    field_sql = field_sql.replace('%y-%m-%d','%Y-%m-%d')
    field_list = field_sql.split(',')
    n = 0
    sTemp = ''
    bFlag = 1
    col_name = ''
    L1 =[]
    for e1 in field_list:
        e1 = e1.strip()
        if e1.find('ifnull(')>=0 and e1.find('date_format(')>=0:
            n = 2
        elif e1.find('ifnull(')>=0:
            n = 1
        elif e1.find('date_format(')>=0:
            n = 1
        elif e1.find('if(')>=0:
            n = 2
        if n==0:
            sTemp = sTemp + e1
            L1.append(sTemp)
            sTemp = ''
        else:
            n = n - 1
            sTemp = sTemp + e1 +","
    L2 = []
    for e in L1:
        L = ['col_name','show_sql','label']
        iPos = e.find('/*')
        iPos1 = e.find('*/')
        if iPos>0:
            label = e[iPos+2:iPos1]
        else:
            label = ''
        str = e.replace("/*%s*/"%label,'')
        iPos = str.find(' as ')
        if iPos>0:
            show_sql = str[:iPos]
            col_name = str[iPos+4:]
        else:
            show_sql = str
            col_name = str

        L[0] = col_name.strip()
        L[1] = show_sql.strip()
        L[2] = label.strip()
        L2.append(L)
    return L2

def saveStep31(request,data_list):
    #print data_list
    menu_id = data_list.get('menu_id','')
    step_id = data_list.get('step_id','')
    lists = data_list.get('lists','')
    n = 0
    for e in lists:
        #print e 
        status = e.get('status','')
        table_id = e.get('table_id',0)
        table_name = e.get('table_name','')
        table_sql = e.get('table_sql','')
        table_ab = e.get('table_ab','')
        table_name = table_name.strip()
        table_ab = table_ab.strip()
        table_sql = table_sql.strip()
        menu_table_id = e.get('menu_table_id',0)
        if 1==1:#str(menu_table_id)=='0':  
            if table_sql != '':
                sql = """select id,table_name from menu_tables where table_sql="%s" and type=1 
                      """%(table_sql)
                #print sql
                rows,iN = db.select(sql)
                if iN == 0:
                    col_list,table_name1 = decode_table_sql(table_sql)
                    table_name = "%s_temp"%(table_name1)
                    sql = "SELECT max(table_name) FROM menu_tables WHERE table_name like '%s%%'"%table_name
                    lT,iN=db.select(sql)
                    if lT[0][0] is not None:
                        i=str(int(lT[0][0][-3:])+1)
                        if len(i)==1:#避免在转换成数字时缺少位数，如：字符串01转成数字时就变成了1
                            i='00%s'%i
                        elif len(i)==2:
                            i='0%s'%i
                        table_name='%s%s'%(table_name,i)
                    else:
                        table_name='%s001'%(table_name)
                    sql = """insert into menu_tables (table_name,table_sql,type) values ("%s","%s",1)
                              """%(table_name,table_sql)
                    #print sql
                    db.executesql(sql)
                    sql = "select last_insert_id();"
                    rows,iN = db.select(sql)  
                    menu_table_id = rows[0][0]
                    #print menu_table_id
                    for e in col_list:
                        sql = "insert into menu_table_cols (table_id,col_name) values (%s,'%s')"%(menu_table_id,e)
                        #print sql 
                        db.executesql(sql)
                else:
                    menu_table_id = rows[0][0]
                    table_name = rows[0][1]
            elif table_name != '':
                sql = "select id from menu_tables where table_name='%s' and type=0"%(table_name)
                #print sql
                rows,iN = db.select(sql)
                if iN == 0:
                    sql = "insert into menu_tables (table_name,type) values ('%s',0)"%(table_name)
                    db.executesql(sql)
                    sql = "select last_insert_id();"
                    rows,iN = db.select(sql)  
                    menu_table_id = rows[0][0]
                else:
                    menu_table_id = rows[0][0]
        #print "menu_table_id=%s"%menu_table_id
        if table_ab == '':
            table_ab = table_name
        if str(table_id) =='0' or str(table_id) =='':  #新添加行
            if menu_table_id!=0:
                sql = """insert into menu_form_tables 
                      (menu_id,step_id,table_name,table_sql,table_ab,menu_table_id,sort)
                      values (%s,%s,'%s','%s','%s',%s,%s)
                      """%(menu_id,step_id,table_name,table_sql,table_ab,menu_table_id,n)           
        elif status =='deleted':  #删除行
            sql = "delete from menu_form_tables where id=%s"%(table_id)
        elif status =='exist':
            sql = "update menu_form_tables set sort=%s where id=%s"%(n,table_id)
        else:  #
            sql = """update menu_form_tables set table_name='%s',table_ab='%s',table_sql='%s',menu_table_id=%s,sort=%s
                     where id=%s
                  """%(table_name,table_ab,table_sql,menu_table_id,n,table_id)
        #print sql
        db.executesql(sql)
        n = n + 1
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        }
        """
    return s

def saveStep32(request,data_list):
    menu_id = data_list.get('menu_id','')
    step_id = data_list.get('step_id','')
    lists = data_list.get('lists','')
    deletes = data_list.get('delete_sql','')
    where_sql = data_list.get('where_sql','')
    n = 0
    for e in lists:
        status = e.get('status','')
        table_id = e.get('table_id','')
        join_type = e.get('join_type','')
        table = e.get('table_name','')
        index_name = e.get('table_index','')
        link = e.get('link_ab','')
        if link!='':
            link_table = link.split(' ')[0]
            link_ab = link.split(' ')[1]
        else:
            link_table = ''
            link_ab = ''
        if table!='':
            table_name = table.split(' ')[0]
            table_ab = table.split(' ')[1]
        else:
            table_name = ''
            table_ab = ''
        link_index = e.get('link_index','')
        if status =='newAdd':  #新添加行
            sql = """insert into menu_form_tables 
                      (menu_id,step_id,join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,sort)
                    values (%s,%s,'%s','%s','%s','%s','%s','%s','%s',%s)
                  """%(menu_id,step_id,join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,n)
            
        elif status =='updated':  #
            sql = """update menu_form_tables set join_type='%s'
                         ,table_name='%s',table_ab='%s',index_name='%s',link_table='%s',link_ab='%s',link_index='%s',sort=%s
                     where id=%s
                  """%(join_type,table_name,table_ab,index_name,link_table,link_ab,link_index,n,table_id)
        elif status =='deleted':  #删除行
            sql = "delete from menu_form_tables where id=%s"%(table_id)
        else:
            sql = "update menu_form_tables set sort=%s where id=%s"%(n,table_id)
        #print sql
        db.executesql(sql)
        n = n + 1
    updateFormStepTable(step_id,where_sql)

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        }
        """
    return s

def saveStep33(request,data_list):
    menu_id = data_list.get('menu_id','')
    step_id = data_list.get('step_id','')
    table_sql = data_list.get('table_sql','')
    lists = data_list.get('lists','')
    n = 0
    for e in lists:
        status = e.get('status','')
        lists_id = e.get('lists_id','')
        lists_step_id = e.get('lists_step_id','')
        lists_para_type = e.get('lists_para_type','')
        lists_link_name = e.get('lists_link_name','')

        if str(lists_id) =='0' or str(lists_id) =='':  #新添加行
            sql = """insert into menu_form_steps_para 
                      (step_id,para_type,link_field,sort)
                      values (%s,%s,'%s',%s)
                      """%(step_id,lists_para_type,lists_link_name,n)
        elif status =='deleted':  #删除行
            sql = "delete from menu_form_steps_para where id=%s"%(lists_id)
        elif status =='exist':
            sql = "update menu_form_steps_para set sort=%s where id=%s"%(n,lists_id)
        else:  #
            sql = """update menu_form_steps_para set para_type='%s',link_field='%s',sort=%s
                     where id=%s
                  """%(lists_para_type,lists_link_name,n,lists_id)
        print sql
        db.executesql(sql)
        n = n + 1

    L = [[1,'']]
    L[0][0] = step_id
    L[0][1] = table_sql
    names = 'step_id tables'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'pages '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      
    
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def saveStep41(request,data_list):
    #print data_list
    status = data_list.get('status',1)
    linkfield2 = data_list.get('linkfield2','')
    linkfield1 = data_list.get('linkfield1','')
    field_options_default = data_list.get('field_options_default','')
    field_options_type = data_list.get('field_options_type') or 'NULL'
    id = data_list.get('id','')
    ssize = data_list.get('size') or 'NULL'
    default_value = data_list.get('default_value','')
    field_type = data_list.get('field_type') or 'NULL'
    hint = data_list.get('hint','')
    tip = data_list.get('tip','')
    enable_list = data_list.get('enables','') 
    required_list = data_list.get('requireds','') 
    readonly_list = data_list.get('readonlys','') 
    hide_list = data_list.get('hides','') 
    label = data_list.get('label','')
    page_name = data_list.get('page_name','')
    max_length = data_list.get('max_length') or '0'
    memo = data_list.get('memo','')
    menu_id = data_list.get('menu_id') or 'NULL'
    step_id = data_list.get('step_id') or 'NULL'
    page_id = data_list.get('page_id') or 'NULL'
    field_show = data_list.get('field_show','')
    field_show = MySQLdb.escape_string(field_show)
    col_name = data_list.get('col_name','')
    default_type = data_list.get('default_type') or 'NULL'
    field_options_txt = data_list.get('field_options_txt','')
    field_options_txt1 = data_list.get('field_options_txt1','')
    url = data_list.get('url','')
    table_name = data_list.get('table_name','')
    field_col_name = data_list.get('field_col_name','')
    field_col_name1 = data_list.get('field_col_name1','')
    
    save_list = data_list.get('saves','') 
    save_para = data_list.get('save_para','') 
    saves = handleMutilValue(save_list,0)
    save_para = handleMutilValue(save_para,0)
    enables = handleMutilValue(enable_list,0)
    requireds = handleMutilValue(required_list,0)
    readonlys = handleMutilValue(readonly_list,0)
    hides = handleMutilValue(hide_list,0)

    new_field = data_list.get('new_field','') 
    new_field = handleMutilValue(new_field,1)
    is_sum = data_list.get('is_sum','') 
    is_sum = handleMutilValue(is_sum,1)


    if '3' in save_para.split(','): 
        is_number = 1
    else:
        is_number = 0
    if str(field_options_type) == '1':
        field_options = field_options_txt
    else:
        field_options = field_options_txt1

    parent_id = data_list.get('parent_id') or 'NULL'

    #新建字段
    if str(new_field) == '1' and table_name!='' and field_col_name1!='':
        sql="select column_name from information_schema.columns where table_schema='%s' and table_name='%s' and column_name='%s'"%(m_dbname,table_name,field_col_name1)
        rows,iN = db.select(sql)
        if str(field_type) in ['8','19']:
            ftype = 'decimal(18,2)'
        elif is_number==1:
            ftype = 'int'
        elif str(field_type) in ['4','27']:
            ftype = 'text'
        elif str(field_type) in ['10','12']:
            ftype = 'datetime'
        else:
            if str(max_length) == '0':
                ftype = 'varchar(50)'
            else:
                ftype = 'varchar(%s)'%max_length
        if iN == 0:
            sql = "alter table %s add %s %s Null COMMENT '%s';"%(table_name,field_col_name1,ftype,label)
            #print sql
            db.executesql(sql)
        field_col_name = field_col_name1

    sql = """update menu_form_cols SET 
                        step_id=%s,
                        is_grid=1,
                        parent_id=%s,
                        col_name='%s',
                        label='%s',
                        field_col_name="%s",
                        field_type=%s,
                        enables='%s',
                        requireds='%s',
                        readonlys='%s',
                        hides='%s',
                        size=%s,
                        default_type=%s,
                        default_value='%s',
                        max_length=%s,
                        tip='%s',
                        memo="%s",
                        hint='%s',
                        field_options_type=%s,
                        field_options_txt="%s",
                        field_options_default='%s',
                        url='%s',
                        linkfield1='%s',
                        linkfield2='%s',
                        status='%s',
                        menu_id='%s',
                        show_table='%s',
                        show_col_name='%s',
                        is_number=%s,
                        saves='%s',
                        save_para='%s',
                        is_sum = %s
                where id = '%s';
        """%(step_id,parent_id,col_name,label,field_show,field_type,enables,requireds,readonlys,hides,ssize
           ,default_type,default_value,max_length,tip,memo,hint,field_options_type,field_options,field_options_default
           ,url,linkfield1,linkfield2,status,menu_id,table_name,field_col_name,is_number
           ,saves,save_para,is_sum,id)
    #print ToGBK(sql)
    db.executesql(sql)

    if field_col_name !='' and table_name!='':
        sql = "select col_name from menu_form_cols where id=%s"%(parent_id)
        rows,iN = db.select(sql)
        parent_name = rows[0][0]

        sql = "select id from menu_form_save_tables where step_id = %s and save_table='%s' and field_name='%s';"%(step_id,table_name,parent_name)
        rows,iN = db.select(sql)
        if iN==0:
            sql = "insert into menu_form_save_tables (step_id,save_table,is_list,del_before_update,is_procedure,status,field_name) values (%s,'%s',1,0,0,1,'%s')"%(step_id,table_name,parent_name)
            rows,iN = db.select(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
        table_id = rows[0][0]
        if str(default_type) == '13': #自动编号
            is_auto_sn = 1
        else:
            is_auto_sn = 0
  
        if '1' in save_para.split(','): 
            is_identity = 1
        else:
            is_identity = 0
        if '2' in save_para.split(','): 
            is_index = 1
        else:
            is_index = 0
        if '4' in save_para.split(','): 
            is_unique = 1
        else:
            is_unique = 0
        if '1' in saves.split(','): 
            is_add = 1
        else:
            is_add = 0
        if '2' in saves.split(','): 
            is_upd = 1
        else:
            is_upd = 0
        if '3' in saves.split(','): 
            is_audit = 1
        else:
            is_audit = 0
        if '4' in saves.split(','): 
            is_verify = 1
        else:
            is_verify = 0
    
        sql = "select id from menu_form_save_cols where field_id = %s and table_id=%s;"%(id,table_id)
        print sql
        rows,iN = db.select(sql)
        if iN == 0:
            sql = """insert into menu_form_save_cols (table_id,save_field_name,is_identity,is_number,is_unique,default_type,request_name
                        ,is_add,is_upd,is_index,is_del,is_audit,is_verify,menu_id,data_table,field_id,is_auto_sn)
                        values(%s,'%s',%s,%s,%s,8,'%s',%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s);
                  """%(table_id,field_col_name,is_identity,is_number,is_unique,col_name
                        ,is_add,is_upd,is_index,is_index,is_audit,is_verify,menu_id,table_name,id,is_auto_sn)
        else:
            sql = """update menu_form_save_cols SET 
                            table_id='%s',
                            save_field_name='%s',
                            is_identity='%s',
                            is_number='%s',
                            is_unique='%s',
                            default_type=8,
                            request_name='%s',
                            is_add='%s',
                            is_upd='%s',
                            is_index='%s',
                            is_del='%s',
                            is_audit='%s',
                            is_verify='%s',
                            is_auto_sn='%s',
                            menu_id='%s',
                            data_table='%s'
                        where field_id = %s;
                  """%(table_id,field_col_name,is_identity,is_number,is_unique,col_name
                        ,is_add,is_upd,is_index,is_index,is_audit,is_verify,is_auto_sn,menu_id,table_name,id)
        #print ToGBK(sql)
        db.executesql(sql)

    L = [[1,1,'','','',1,'']]
    L[0][0] = id
    L[0][1] = step_id
    L[0][2] = col_name
    L[0][3] = label
    L[0][4] = field_show
    L[0][5] = get_options_data(menu_id,'','',16,'','',field_type,'','')
    L[0][6] = get_options_data(menu_id,'','',3,'select id,cname from menu_form_func where menu_id=$s and status=1 and type in(1,2)','',enables,menu_id,'',False)

    names = 'list_cols_col_id list_cols_step_id list_cols_col_name list_cols_label list_cols_show list_cols_col_type list_cols_col_func'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'list_cols '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def saveStep52(request,data_list):
    field_id = data_list.get('field_id','')
    col_name = data_list.get('col_name','')
    checkFieldArray = data_list.get('checkFieldArray','')
    exprCondition = data_list.get('exprCondition','')
    exprLabel = data_list.get('exprLabel','')
    checkField = handleMutilValue(checkFieldArray,0)

    sql = "select step_id from menu_form_cols where id=%s"%(field_id)    
    rows,iN = db.select(sql)
    step_id = rows[0][0]

    more_cols = getCheckField(checkField,step_id)
    more_cols = strDuplicateRemoval(more_cols)
    #print more_cols
    sql = """update menu_form_calculate SET `on_change`="%s",
                 `expression`="%s",exprLabel='%s' where field_id=%s """%(more_cols,exprCondition,exprLabel,field_id)
    db.executesql(sql)

    sql = "select id from menu_form_calculate where field_id=%s"%field_id 
    rows,iN = db.select(sql)
    L = [['','',0]]
    L[0][0] = more_cols
    L[0][1] = exprCondition
    L[0][2] = rows[0][0]
    names = 'list_cal_cols list_cal_expression list_cal_id'.split()
    data = [dict(zip(names, d)) for d in L]
    L1 =['']
    L1[0] = data
    names = 'list_cal '.split()
    data = dict(zip(names, L1))
    formData = json.dumps(data,ensure_ascii=False)      
    
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功！",
        "formData":%s,
        }
        """%formData
    #print ToGBK(s)
    return s

def getCheckField(checkField,step_id):
    c_list = checkField.split(',')
    cols = checkField
    for e in c_list:
        if e!='':
            sql = """select ifnull(c.on_change,'') from menu_form_calculate c
                     left join `menu_form_cols` fc on fc.id =c.field_id
                     where fc.step_id=%s and fc.col_name='%s'"""%(step_id,e)
            print sql
            rows,iN = db.select(sql)
            if iN > 0:
                cols1 = rows[0][0]
                more_cols = getCheckField(cols1,step_id)
                cols += "," + more_cols
    return cols

def getDefaultvalue(request,type,default):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    cur_dept_id = request.session.get('cur_dept_id', '')
    cur_dept_name = request.session.get('cur_dept_name', '')

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
        value = getToday(7)
    elif type == 7:
        value = default
    elif type == 8:
        value = request_list[request_name]
        #多选框提交的数据是list,需要做下处理
        if is_number == 1 and isinstance(value,list):
            if len(value)>0:
                value = value[0]
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    return value

def getSaveValue(request,type,is_number,is_ch,default_value,label,link_table,link_field,dict,request_list,request_name):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    cur_dept_id = request.session.get('cur_dept_id', '')
    cur_dept_name = request.session.get('cur_dept_name', '')
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
        value = request_list[request_name]
        #多选框提交的数据是list,需要做下处理
        if is_number == 1 and isinstance(value,list):
            if len(value)>0:
                value = value[0]
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    elif type == 10:
        value = dict[link_table][link_field]
    if is_number == 1:
        value = value or 'NULL' 
    else:
        value = value or ''   
        
    return value

def getListValue(request,type,link_field,dict):
    usr_id = request.session.get('usr_id', 0)
    usr_name = request.session.get('usr_name', '')
    cur_dept_id = request.session.get('cur_dept_id', '')
    cur_dept_name = request.session.get('cur_dept_name', '')
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
        value = request.POST.get(link_field, '') or request.GET.get(link_field, '')
    elif type == 9:
        value = "%s_%s"%(time.time(),usr_id)
    elif type == 10:
        value = dict[link_field]
        
    return value

def get_filter_data(type,txt,title,default):
    if type==1:
        L = get_mtc_t_data(default,txt,title)
    elif type==2:
        L = get_dept_data1(default,title)
    elif type==3:
        L = get_roles_list('',default,title)
    elif type==4:
        L = get_menu_list(default,title)
    else:
        return ''
    return L

def packonChangeUrl(pk,field_id,href,target,para_cols):
    L = ['href','target','para']
    L[0] = href
    L[1] = target
    lT =[]
    if para_cols!='':
        pList = para_cols.split(',')
        for e in pList:
            L2= ['','']
            L2[0] = e
            L2[1] = e
            lT.append(L2)
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]
    names = 'href target para'.split()
    L1 = dict(zip(names, L))
    return L1

def packFormUrl(pk,field_id,href,target):
    L = ['href','target','para']
    L[0] = href
    L[1] = target
    sql = "select para_name,link_field from menu_form_url_para where field_id=%s"%field_id
    lT,iN = db.select(sql)
    names = 'para_name link_field'.split()
    L[2] = [dict(zip(names, d)) for d in lT]
    names = 'href target para'.split()
    L1 = dict(zip(names, L))
    return L1
	
def packPara(source,paraList,value_dict,request):
    sql = source
    for e in paraList:
        value = getListValue(request,e[0],e[1],value_dict)
        sql = sql.replace('$s',str(value),1)
    return sql

def paraIsNotNULL(paraList,request):
    for e in paraList:
        if e[0] == 8:
            value = request.POST.get(e[1], '') or request.GET.get(e[1], '')
            print "value=%s"%value
            if value =='' or value=='0':
                return False
    return True

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
                if e!='':
                    sTemp +="%s,"%e
            sTemp = sTemp[:-1]
    else:
        sTemp = value
    return sTemp

def decode_table_sql(final_sql):
    final_sql = final_sql.upper()
    #只保留一个空格
    import re
    final_sql = re.sub(r'\s+', ' ', final_sql)
    #print final_sql
    iPos = final_sql.find(' FROM ')
    table_sql = final_sql[iPos+6:]
    iPos1 = table_sql.find(' ')
    if iPos1>0:
        table_sql = table_sql[:iPos1]   
    #print table_sql
    field_sql = final_sql[:iPos]
    field_sql = field_sql.replace('SELECT','')
    field_sql = field_sql.replace('%Y-%M-%D','%Y-%m-%d')

    #解析字段结构
    field_list = field_sql.split(',')
    field_list1 = []
    n = 0
    sTemp = ''
    bFlag = 1
    col_name = ''
    for e1 in field_list:
        e1 = e1.strip()
        if e1.find('IFNULL(')>=0 and e1.find('DATE_FORMAT(')>=0:
            n = 2
        elif e1.find('IFNULL(')>=0:
            n = 1
        elif e1.find('DATE_FORMAT(')>=0:
            n = 1
        elif e1.find('IF(')>=0:
            n = 2
        if bFlag == 1:
            col_name = e1
        if n==0:
            sTemp = sTemp + e1
            col_name = col_name.replace('IFNULL(','')
            col_name = col_name.replace('DATE_FORMAT(','')
            col_name = col_name.replace('IF(','')
            try:
                col_name = col_name.split('.')[1]
            except:
                pass
            field_list1.append(col_name)
            sTemp = ''
            bFlag = 1
        else:
            n = n - 1
            sTemp = sTemp + e1 +","
            bFlag = 0

    return field_list1,table_sql