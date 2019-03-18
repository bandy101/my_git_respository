# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname,HttpResponseCORS,HttpResponseJsonCORS,ComplexEncoder,mValidateUser'%prj_name) 
import json

def getFAInfo(request):
    code = request.POST.get('code') or request.GET.get('code', 0) 
    is_manager = 0

    menu_id = request.POST.get('menu_id', 1102)
    ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    if ret==0:
        sql = """select * from usr_role ur
            left join roles r on ur.role_id = r.role_id
            where r.role_name = '固定资产管理员' and ur.usr_id = %s"""%d_value[0]
        rows,iN = db.select(sql)
        if iN>0:
            is_manager = 1

    sql = """SELECT m1102.id,m1102.sn,m1102.name,fs2.cname,fs1.cname,m1102.brand,m1102.type,m1102.size,m1102.zc_price,m1102.buy_time
                   ,m.txt1,M1102.STATUS,m1102.cf_place,m1102.jy_usrname,'','',br.gw_status
            FROM _m1102_gdzc_warehousing m1102 
            LEFT JOIN FIXEDAST_SORT FS1 ON FS1.ID=M1102.SMLL_TYPE 
            LEFT JOIN FIXEDAST_SORT FS2 ON FS2.ID=M1102.BIG_TYPE 
            LEFT JOIN (select id,txt1 from mtc_t where type='ESTAT') M ON M.ID=M1102.STATUS 
            LEFT JOIN _M1108_PD_LIST PD ON PD.GDZC_ID=M1102.ID 
            LEFT JOIN _m1103_borrow br on br.gw_id = m1102.jy_gwid
            WHERE m1102.sn = '%s'
            """%code
    rows,iN = db.select(sql)
    if iN == 0:
        s = """
        {
        "errcode": -1,
        "errmsg": "板材信息不存在",
        }        """
        #print ToGBK(s)
        return HttpResponseJsonCORS(request,s)
 
    L=list(rows[0])
    if is_manager == 1 and L[11] == 3 and L[16] == 1:
        L[15] = 1
    else:
        L[15] = 0
    if is_manager == 1 and L[11] == 2 :
        L[14] = 1
    else:
        L[14] = 0

    names = 'id code name Primary_Classification Sub_Classification brand model spec zc_price buy_time status status_id cf_place jy_usrname return borrow'.split()
    data = dict(zip(names, L))
    fa_info = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息成功",
        "FA_info":%s,
        }        """%(fa_info)
    #print ToGBK(s)
    return HttpResponseJsonCORS(request,s)

def setFAInfo(request):
    print request.POST
    func = request.POST.get('func', '')
    if func == 'return':
        ret,errmsg,d_value = mValidateUser(request,"view",1105)
        if ret!=0:
            return HttpResponseCORS(request,errmsg)
        cid = d_value[0]
        cusrname = d_value[1]
        id = request.POST.get('id', '')
        location = request.POST.get('storePlace', '')
        
        sql = """INSERT INTO _m1105_restitution (status,cid,cusrname,ctime,gh_day,gh_man,location) 
                 VALUES (0,%s, '%s',now(),now(), '%s', '%s');"""%(cid,cusrname,cusrname,location)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        m_id = rows[0][0]
        sql = """INSERT INTO _m1105_guihuan_list ( m_id,status, cid, cusrname, ctime, name, brand, type, size, liability, Use_department, Use_project, purpose, Borrow_date, b_type, s_type, gdcz_id, br_id, b_name, s_name, gdzc_sn) 
                 select %s,0,%s,'%s',now(),zc.name,zc.brand,zc.type,zc.size,zc.jy_usrname,dp.cname,op.cname,mx.purpose,zc.jy_time,zc.big_type,zc.smll_type,zc.id,mx.id,fs1.cname,fs2.cname,zc.sn 
                 from _m1102_gdzc_warehousing zc 
				 left join fixedast_sort fs1 on fs1.id = zc.big_type 
				 left join fixedast_sort fs2 on fs2.id = zc.smll_type 
				 left join mtc_t m on m.id = zc.unit and m.type='EUNIT' 
				 left join _m1103_borrow_list mx on  mx.gdzc_id = zc.id and mx.status = 1 
				 left join dept dp on dp.id = mx.dept_id 
				 left join out_proj op on op.id = mx.proj_id 
				 where zc.id=%s
              """%(m_id,cid,cusrname,id)
        db.executesql(sql)
        sql = "select id from _m1103_borrow_list where gdzc_id=%s and status=1 order by id desc"%(id)
        rows,iN = db.select(sql)
        br_id = rows[0][0]

        sql = """update _m1103_borrow_list set status = 2,return_date=now() where id=%s
                      """%(br_id)
        db.executesql(sql)
        sql = """update _m1102_gdzc_warehousing set status = 1,jy_gwid=NULL,jy_usrname=NULL,jy_time=NULL,cf_place='%s' where id=%s
             """%(location,id)
        db.executesql(sql)

    elif func == 'borrow':    
        ret,errmsg,d_value = mValidateUser(request,"view",1103)
        if ret!=0:
            return HttpResponseCORS(request,errmsg)
        cid = d_value[0]
        cusrname = d_value[1]
        id = request.POST.get('id', '')
        sql = "select gw_id from _m1103_borrow_list where gdzc_id=%s order by id desc"%(id)
        rows,iN = db.select(sql)
        pk = rows[0][0]
        
        sql = "update _m1103_borrow set dj_date=now(),dj_usrid=%s,dj_usrname='%s',dj_status=1  where gw_id=%s"%(cid,cusrname,pk)
        db.executesql(sql)
        sql = "update _m1103_borrow_list set status = 1,dj_date=now() where gw_id=%s"%(pk)
        db.executesql(sql)
        sql = "update _m1102_gdzc_warehousing set status =2 where jy_gwid=%s"%(pk)
        db.executesql(sql)
        sql = """UPDATE gw_doc SET status = 8, status_txt = '已登记'  WHERE id = %s;
            """%(pk)
        db.executesql(sql)
        sql=" delete from gw_verify where gw_id = %s"%(pk)
        #print sql
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        }        """

    return HttpResponseJsonCORS(request,s)
    
