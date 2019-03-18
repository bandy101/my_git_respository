# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname,data_url,ToGBK'%prj_name) 
exec ('from %s.share        import get_options_data,get_options_data_search,get_options_data_level,get_options_data_view'%prj_name) 
import json 
import MySQLdb
import copy

def getPageDataExt(pk,menu_id,usr_id,mode,request,formData,showData,gridData,calData):
    sql = "select ifnull(formFunc,'') from menu_data_source where menu_id='%s' "%(menu_id)
    rows,iN = db.select(sql)
    func = ''
    if iN>0:
        func = rows[0][0]
    if func == 'getPageDataClbj':  #材料报价审批
        return getPageDataClbj(pk,menu_id,usr_id,mode,request,formData,showData,gridData,calData)
    return formData,showData,gridData,calData

def getPageDataClbj(pk,menu_id,usr_id,mode,request,formData,showData,gridData,calData):
    value_dict = dict()    
    value_dict['pk'] = pk

    step = request.POST.get('step','')
    mode =  request.POST.get('mode') 
    if str(step) == '1':
        return formData,showData,gridData,calData

    sql = """select s.cname,l.gys_id from _m406_clbj_gys l
               left join suppliers s on l.gys_id = s.id
               where l.gw_id = '%s' order by l.sort"""%(pk)
    rows,iN = db.select(sql)

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
                  ,mfc.btn_type
                  ,mfc.btn_color
                  ,mfc.url
                  ,ifnull(mfc.is_sum,0)
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
                left join menu_form_cols mfc1 on mfc1.id = mfc.parent_id
                left join menu_form_steps ms on ms.id = mfc1.step_id
                where mfc1.col_name='bj_list' and mfc.status = 1 and ms.menu_id='%s'
                order by mfc.sort """%(menu_id)
    names = 'cid label field_type required size readonly value hide max_length hint field_options table_col table_data btn_type btn_color url is_sum'.split()
    L=[]
    rows1,iN1 = db.select(sql)
    for e in rows1:
        L1 = list(e)    
        value_dict[e[0]] = e[6]
        L1[3] = getFuncValue(e[3],mode)
        if str(step) == '2':
            L1[5] = getFuncValue(e[5],mode)
        else:
            L1[5] = 1
        L1[7] = getFuncValue(e[7],mode)

        para1,para2='',''
        single = True
        if e[17]==5:
            single = False
        if str(step) == '2':
            if str(e[17]) in ['3','5','6','26']:  #监听数字改变
                L1[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                if e[-3]!='':
                    L1[15] = packonChangeUrl(pk,usr_id,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(e[17]) in ['32','34','35']:  #带搜素的下拉框
                L1[10] = get_options_data_search(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single,value_dict,e[-2])
                L1[15] = packonChangeUrl(pk,usr_id,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            elif str(e[17]) in ['18']:  #带分级的下拉框
                L1[10] = get_options_data_level(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
                L1[15] = packonChangeUrl(pk,usr_id,e[-1],"%s/getData/?func=refresh&menu_id=%s&pk=%s&field_id=%s&audit=0&mode=%s"%(data_url,menu_id,pk,e[-1],mode),"_refresh",e[-2])
            else:
                if L1[15] != '':
                    L1[15] = packFormUrl(pk,L1[-1],L1[15],L1[-4])
        else:
            if str(e[17]) =='16':  #多选弹出框
                L1[10] = get_mutisel_options(e[-1],e[6])
            elif str(e[17]) in ['5']:  
                L1[10] = get_options_data(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            elif str(e[17]) in ['3','6','18','26','32']:  
                print e[6]
                L1[6] = get_options_data_view(menu_id,usr_id,pk,e[19],e[20],e[21],e[6],para1,para2,single)
            else:
                if L1[15] != '':
                    L1[15] = packFormUrl(pk,L1[-1],L1[15],L1[-4])
            if str(e[17]) not in ['1','13','14','17','22','33']:  
                L1[2] = 'displayText'

        if e[0] == 'clbj_price':
            price = L1
        elif e[0] == 'clbj_cost':
            cost = L1
        L.append(L1)
    rows1 = L
    L =[]
    names1=[]
    for e in rows1:
        L1 = list(e)    
        if e[0] == 'clbj_price':
            n = 0
            for e1 in rows:
                L2 = copy.deepcopy(price)
                L2[0] = 'clbj_price_%s'%n
                L2[1] = '单价(%s)'%e1[0]
                L.append(L2)
                names1.append(L2[0])
                L3 = copy.deepcopy(cost)
                L3[0] = 'clbj_cost_%s'%n
                L3[1] = '总价(%s)'%e1[0]
                L.append(L3)
                names1.append(L3[0])
                n += 1
        elif e[0] == 'clbj_cost':
            pass
        else:
            L.append(L1)
            names1.append(L1[0])
    rows1 = L
    #print names1

    sql = "select id,cl_mat_name,cl_size,brand,cl_type,cl_unit,cl_mat_type,cl_mat_code,cl_count,'','',craft,memo from _m406_clbj_list where gw_id = '%s'"%(pk)
    rows2,iN2 = db.select(sql)

    L = []
    for e in rows2:
        row = list(e)   
        iCount = len(row) 
        row1 = ['']*(iCount-2+(len(rows))*2)
        n = 0
        sql = """select bj.price,bj.cost from _m406_clbj_gysbj bj
                   left join _m406_clbj_gys gys on bj.gys_id =gys.gys_id and bj.gw_id = gys.gw_id
                   where bj.m_id = '%s'
                   order by gys.sort """%(e[0])
        rows3,iN3 = db.select(sql)
        #print sql
        for i in range(0,iCount):
            value_dict[rows1[n][0]] = row[i]
            if i<9 or i>10:
                single = True
                if rows1[n][17]==5:
                    single = False
                row1[n] = row[i]
                if str(step) == '2':
                    if str(rows1[n][17]) =='16':  #多选弹出框
                        row1[n] = get_mutisel_options(rows1[n][-1],row[i])
                    elif str(rows1[n][17]) in ['3','5','6','26']:  #监听数字改变
                        row1[n] = get_options_data(menu_id,usr_id,pk,rows1[n][19],rows1[n][20],rows1[n][21],row[i],para1,para2,single)
                    elif str(rows1[n][17]) in ['32','34','35']:  #监听数字改变
                        row1[n] = get_options_data_search(menu_id,usr_id,pk,rows1[n][19],rows1[n][20],rows1[n][21],row[i],para1,para2,single,value_dict,rows1[n][-2])
                    elif str(rows1[n][17]) in ['18']:  #带分级的下拉框
                        row1[n] = get_options_data_level(menu_id,usr_id,pk,rows1[n][19],rows1[n][20],rows1[n][21],row[i],para1,para2,single)
                else:
                    if str(rows1[n][17]) in ['5','3','6','18','26','32']:  
                        row1[n] = get_options_data_view(menu_id,usr_id,pk,rows1[n][19],rows1[n][20],rows1[n][21],row[i],para1,para2,single)
                if row1[n] == None:
                    row1[n] = ''
                n += 1
            elif i == 9:
                for e1 in rows3:
                    row1[n] = e1[0]
                    row1[n+1] = e1[1]
                    n += 2
        L.append(row1)
    rows2 = L

    L = []
    for e in formData:
        L1 = list(e)
        if e[0] == 'bj_list':
            table_col = [dict(zip(names, d)) for d in rows1]
            table_data = [dict(zip(names1, d)) for d in rows2]
            #print table_data
            L1[11] = table_col
            L1[12] = table_data
        L.append(L1)


    cL = []
    for e in calData:
        L1 = list(e)
        if e[0] == 'clbj_cost':
            n = 0
            for e1 in rows:
                L2 = copy.deepcopy(L1)
                L2[0] = u'clbj_cost_%s'%(n)
                L2[1] =  [u'clbj_price_%s'%n, u'clbj_count']
                L2[2] =  u'{clbj_count}*{clbj_price_%s}'%n
                cL.append(L2)
                n += 1
        else:
            cL.append(L1)

    return L,showData,gridData,cL

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

def packonChangeUrl(pk,usr_id,field_id,href,target,para_cols):
    #print "field_id = %s para_cols=%s"%(field_id,para_cols)
    sql = """select `field_type` ,`field_options_type`,ifnull(m.url,''),col_name  from `menu_form_cols` c
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