# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder'%prj_name) 
import json

def saveSchedule(request):
    step = request.POST.get('step', 1)
    if step=='':
        step = 1
    if str(step)=='1':
        return saveSchedule_step1(request)
    if str(step)=='2':
        return saveSchedule_step2(request)
    if str(step)=='3':
        return saveSchedule_step3(request)
    s = """
        {
        "errcode": -1,
        "errmsg": "无效操作",
        }
        """
    return HttpResponseCORS(request,s)

def saveSchedule_step1(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
 
    tab = request.POST.get('tab', '')
    step = request.POST.get('step', 1)
    if step=='':
        step = 1

    data =  request.POST.get('data','')
    data_list = json.loads(data)
    pk =  data_list.get('pk','')
    random_no = data_list.get('random_no','')
    plan_name = data_list.get('plan_name','')
    prj_id = data_list.get('prj_id','')
    # s = """
    #     {
    #     "errcode": 0,
    #     "errmsg": "%s",
    #     "pk":%s,
    #     }
    #     """%(prj_id,pk)
    # return HttpResponseCORS(request,s)
    if pk =='':
        sql="""insert into xcx_main(prj_id,ctime,cid,plan_name,random_no,cusrname)
        values(%s,now(),%s,'%s','%s','%s')
        """%(prj_id,usr_id,plan_name,random_no,usr_name)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        pk=rows[0][0]
    else:
        sql="""update xcx_main set 
            prj_id=%s,
            utime=now(),
            uid=%s,
            plan_name='%s',
            uusrname='%s'
            where id = %s
        """%(prj_id,usr_id,plan_name,usr_name,pk)
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s,
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def saveSchedule_step2(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
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
    multi_list = data_list.get('multi_list','')
    if pk!='':
        sql="""delete from xcx_floor where m_id=%s"""%pk  #先删除原本的
        db.executesql(sql)

        sql="insert into xcx_floor (m_id,sort,cname,ctime,cid) values"
        sort=0
        for e in multi_list:
            sort+=1
            sql+="""(%s,%s,'%s',now(),%s),"""%(pk,sort,e,usr_id)
        sql=sql[:-1]
        db.executesql(sql)
        s = """
            {
            "errcode": 0,
            "errmsg": "操作成功",
            "pk":%s,
            }
            """%(pk)
        return HttpResponseCORS(request,s)
    else:
        s = """
        {
        "errcode": -1,
        "errmsg": "无效操作",
        }
        """
        return HttpResponseCORS(request,s)

def saveSchedule_step3(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
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
    mul_menu = data_list.get('mul_menu','')
    if pk!='':
        sql="""delete from xcx_mat where m_id=%s"""%pk  #先删除原本的
        db.executesql(sql)
        sql="""delete from xcx_detail where m_id=%s"""%pk  #先删除原本的
        db.executesql(sql)
        
        for x in mul_menu:
            cname0=x['text']
            value0=x['value']
            sql0="""insert into xcx_mat(m_id,ilevel,cname,parent_id,mark) values(%s,0,'%s',0,'%s')"""%(pk,cname0,value0)
            db.executesql(sql0)
            sql0 = "select last_insert_id();"
            rows0,iN = db.select(sql0)
            parent_id0=rows0[0][0]
            if 'children' in x:
                for y in x['children']:
                    cname1=y['text']
                    value1=y['value']
                    sql1="""insert into xcx_mat(m_id,ilevel,cname,parent_id,mark) values (%s,1,'%s',%s,'%s')"""%(pk,cname1,parent_id0,value1)
                    db.executesql(sql1)
                    sql1 = "select last_insert_id();"
                    rows1,iN = db.select(sql1)
                    parent_id1=rows1[0][0]
                    if 'children' in y:
                        sql2="insert into xcx_mat(m_id,ilevel,cname,parent_id,mark) values"
                        for z in y['children']:
                            cname2=z['text']
                            value2=z['value']
                            sql2+="(%s,2,'%s',%s,'%s'),"%(pk,cname2,parent_id1,value2)
                        sql2=sql2[:-1]
                        db.executesql(sql2)

        sql="""select id from xcx_floor where m_id=%s"""%pk
        floor_data,iN=db.select(sql)
        sql="""select id from xcx_mat where m_id=%s and iLevel=2"""%pk
        mat_data,iN=db.select(sql)
        sql="insert into xcx_detail(m_id,floor_id,mat_id,ctime,cid) values"
        if iN>0:
            for e in floor_data:
                for i in mat_data:
                    sql+="""(%s,%s,%s,now(),%s),"""%(pk,e[0],i[0],usr_id)
            sql=sql[:-1]
            db.executesql(sql)
        s = """
            {
            "errcode": 0,
            "errmsg": "操作成功",
            "pk":%s,
            }
            """%(pk)
        return HttpResponseCORS(request,s)
    else:
        s = """
        {
        "errcode": -1,
        "errmsg": "无效操作",
        }
        """
        return HttpResponseCORS(request,s)

def getScheduleData(request,step,pk):
    scheduleData={}
    scheduleData_step2=[]
    scheduleData_step3=[]
    if step=='':
        step = 1
    if str(step)=='2':
        sql="""select id,sort,cname from xcx_floor where m_id=%s order by sort
        """%pk
        rows,iN=db.select(sql)
        scheduleData_step2=rows
        # for e in rows:
        #     row=list(e)
        #     scheduleData.append(row)
        names = 'id sort cname'.split()
        L = [dict(zip(names, d)) for d in scheduleData_step2]
        scheduleData_step2=L
        # scheduleData_step2 = json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)
    if str(step)=='3':
        sql="""select id,ilevel,parent_id,cname,mark from xcx_mat where m_id=%s order by ilevel"""%pk  
        rows,iN=db.select(sql)
        scheduleData_step3=rows 
        names = 'id ilevel parent_id cname value'.split()
        L = [dict(zip(names, d)) for d in scheduleData_step3]
        scheduleData_step3=L
        # scheduleData_step3 = json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)
    scheduleData['step2']=scheduleData_step2
    scheduleData['step3']=scheduleData_step3
    # names = 'step2 step3'.split()
    # L = [dict(zip(names, d)) for d in scheduleData]
    # scheduleData=json.dumps(L,ensure_ascii=False,cls=ComplexEncoder)
    return json.dumps(scheduleData,ensure_ascii=False)

def getScheduleList(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    pk =  request.POST.get('pk','')

    L=[]
    if pk=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "没有获取到PK值",
        }        """
        return HttpResponseCORS(request,s)
    # pk=1
    # sql=""" 
    #     select xd.id,mt.cname,mt.mark,mt1.cname,mt1.mark,mt2.cname,mt2.mark,xf.id,xf.cname,IFNULL(xd.schedule,0) from xcx_detail xd
    #     left join xcx_floor xf on xf.id = xd.floor_id 
    #     left join xcx_mat mt on mt.id = xd.mat_id 
    #     left join xcx_mat mt1 on mt1.id = mt.parent_id and mt1.ilevel=1
    #     left join xcx_mat mt2 on mt2.id = mt1.parent_id and mt2.ilevel=0
    #     where xd.m_id = %s
    #     order by xf.sort 
    #     """%pk
    # rows,iN=db.select(sql)
    # names = 'id cname_3 value_3 cname_2 value_2 cname_1 value_1 floor_id floor_cname schedule'.split()
    # data = [dict(zip(names, d)) for d in rows]
    # L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""select id,ilevel,parent_id,cname,mark from xcx_mat where m_id=%s order by ilevel,id """%pk  
    rows,iN=db.select(sql)
    names = 'id ilevel parent_id cname value'.split()
    data = [dict(zip(names, d)) for d in rows]
    L1 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""
        select xd.id,mt.cname,mt.id,mt1.cname,mt1.mark,mt2.cname,mt2.mark,xf.id,xf.cname,IFNULL(DATE_FORMAT(xd.plan_date,'%%Y-%%m-%%d'),'')
        from xcx_detail xd
        left join xcx_floor xf on xf.id = xd.floor_id 
        left join xcx_mat mt on mt.id = xd.mat_id 
        left join xcx_mat mt1 on mt1.id = mt.parent_id and mt1.ilevel=1
        left join xcx_mat mt2 on mt2.id = mt1.parent_id and mt2.ilevel=0
        where xd.m_id = %s
        order by xf.sort,mt.id 
        """%pk
    rows,iN=db.select(sql)
    sql="""
        select id from xcx_mat where ilevel=2 and m_id=%s order by parent_id
        """%pk
    rows1,iN=db.select(sql)
    total=iN

    table_data=[]
    n=0
    for e in rows:
        n+=1
        if n==1 or n%total==1:
            tem=[]
            tem.append(e[8])
        tem_array=[]
        tem_array.append(e[0])
        tem_array.append(e[9])
        tem.append(tem_array)
        if n%total==0 and n>1:
            table_data.append(tem)
    table_data=json.dumps(table_data,ensure_ascii=False)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取进度列表成功",
        "table_data":%s,
        "table_col":%s,
        }        """%(table_data,L1)
    return HttpResponseCORS(request,s)

def getProjList(request):
    L=[]
    sql="""
        select id,cname,gc_no,1 from out_proj
        where id in (select prj_id from xcx_main)
        """
    rows,iN=db.select(sql)
    names = 'id cname gc_no right'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取项目列表成功",
        "data":%s
        }        """%(L)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def getPlanList(request):
    proj_id =  request.POST.get('proj_id','')
    openid =  request.POST.get('openid','')
    print request.POST
    if proj_id=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "没有获取到proj_id值"
        }        """
        return HttpResponseJsonCORS(s)

    L=[]
    sql="""
        select id,plan_name from xcx_main where prj_id=%s
        """%proj_id
    print sql 
    rows,iN=db.select(sql)
    names = 'id plan_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取计划列表成功",
        "data":%s
        }        """%(L)
    return HttpResponseJsonCORS(s)

def getFloorList(request):
    pk = request.POST.get('pk','')
    if pk=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "没有获取到PK值"
        }        """
        return HttpResponseJsonCORS(s)
    L=[]
    sql="""
        select id,cname from xcx_floor where m_id=%s order by sort
        """%pk
    rows,iN=db.select(sql)
    names = 'id cname gc_no right'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取楼层列表成功",
        "data":%s
        }        """%(L)
    return HttpResponseJsonCORS(s)

def getFloorDetail(request):
    floor_id = request.POST.get('floor_id','')
    print request.POST
    if floor_id=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "没有获取到楼层ID值"
        }        """
        return HttpResponseJsonCORS(s)
    L=[]
    sql="""
        select xd.id,IFNULL(xd.schedule,'0'),mt2.cname,mt1.cname,mt0.cname,mt2.parent_id,mt1.parent_id  
        from xcx_detail xd
        left join xcx_mat mt2 on mt2.id = xd.mat_id and mt2.iLevel=2
        left join xcx_mat mt1 on mt1.id = mt2.parent_id and mt1.ilevel=1
        left join xcx_mat mt0 on mt0.id = mt1.parent_id and mt0.ilevel=0
        where xd.floor_id=%s
        order by mt1.parent_id,mt2.parent_id
        """%floor_id
    # sql="""
    #     select xd.id,IFNULL(xd.schedule,'0')
    #     from xcx_mat mt
    #     left join xcx_detail xd on xd.m_id = mt.m_id
    #     where xd.floor_id=%s
    #     """%floor_id
    rows,iN=db.select(sql)
    l0=0
    l1=0
    tem_l0=[]
    tem_l1=[]
    tem_l2=[]
    for e in rows:
        tem_l2=[]
        tem_l2.append(e[0])
        tem_l2.append(e[1])
        tem_l2.append(e[2])
        name=e[3]
        if l0!=e[6]:
            if l0 !=0:
                L.append(tem_l0)
            tem_l0=[]
            tem_l1=[]
            tem_l0.append(e[4])
            tem_l1.append(e[3])
            tem_l1.append(tem_l2)
            tem_l0.append(tem_l1)
        else:
            if l1==e[5]:
                tem_l1.append(tem_l2)
            else:
                tem_l1=[]
                tem_l1.append(e[3])
                tem_l1.append(tem_l2)
                tem_l0.append(tem_l1)
        l0=e[6]
        l1=e[5]
    L.append(tem_l0)
    L = json.dumps(L,ensure_ascii=False)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取楼层详细信息成功",
        "data":%s
        }        """%(L)
    return HttpResponseJsonCORS(s)

def editTable(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    id =  request.POST.get('id','')
    date =  request.POST.get('date','')
    sql="""
        update xcx_detail set plan_date ='%s' where id = %s
        """%(date,id)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "更改计划成功",
        }        """
    return HttpResponseCORS(request,s)

def getScheduleDetail(request):
    pk =  request.POST.get('pk','')
    L=[]
    if pk=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "没有获取到PK值"
        }        """
        return HttpResponseJsonCORS(s)

    sql="""select id,ilevel,parent_id,cname,mark from xcx_mat where m_id=%s order by ilevel,id """%pk  
    rows,iN=db.select(sql)
    names = 'id ilevel parent_id cname value'.split()
    data = [dict(zip(names, d)) for d in rows]
    L1 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""
        select xd.id,mt.cname,mt.id,mt1.cname,mt1.mark,mt2.cname,mt2.mark,xf.id,xf.cname,IFNULL(DATE_FORMAT(xd.plan_date, '%%Y-%%m-%%d'),'') 
        from xcx_detail xd
        left join xcx_floor xf on xf.id = xd.floor_id 
        left join xcx_mat mt on mt.id = xd.mat_id 
        left join xcx_mat mt1 on mt1.id = mt.parent_id and mt1.ilevel=1
        left join xcx_mat mt2 on mt2.id = mt1.parent_id and mt2.ilevel=0
        where xd.m_id = %s
        order by xf.sort,mt.id 
        """%pk
    rows,iN=db.select(sql)
    sql="""
        select id from xcx_mat where ilevel=2 and m_id=%s order by parent_id
        """%pk
    rows1,iN=db.select(sql)
    total=iN

    table_data=[]
    n=0
    for e in rows:
        n+=1
        if n==1 or n%total==1:
            tem=[]
            tem.append(e[8])
        tem_array=[]
        tem_array.append(e[0])
        tem_array.append(e[9])
        tem.append(tem_array)
        if n%total==0 and n>1:
            table_data.append(tem)
    table_data=json.dumps(table_data,ensure_ascii=False)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取进度列表成功",
        "table_data":%s,
        "table_col":%s
        }        """%(table_data,L1)
    return HttpResponseJsonCORS(s)

def saveSechedule(request):
    table_id = request.POST.get('table_id','')
    schedule = request.POST.get('schedule','')
    usr_id=1
    if table_id=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "没有获取到table_id值"
        }        """
        return HttpResponseJsonCORS(s)
    
    sql="""
        update xcx_detail set status = '%s' where id = %s
        """%(table_id,schedule)
    db.executesql(sql)
    sql="""
        insert into xcx_log (detail_id,ctime,cid,schedule)
        values(%s,now(),%s,'%s')
        """%(table_id,usr_id,schedule)
    db.executesql(sql)
    s = """
        {
        "errcode": 0,
        "errmsg": "更新进度列成功"
        }        """
    return HttpResponseJsonCORS(s)

def getUsers(request,openid,username):
    sql="""

        """
