# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,byaq,byerp,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,m_sCorpID,m_sCorpSecret,m_sAgentId_gy,m_sCorpSecret_gy'%prj_name)
exec ('from %s.share        import imgUrl,read_access_token,fs_url,write_access_token,checkSession,data_url,host_url,my_urlencode,read_access_token_common,write_access_token_common'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
from HW_DT_TOOL                 import getToday
import MySQLdb

testid = 1087
#testid = 0
def getMsgList(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注。"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    typeID =  request.POST.get('typeID','')

    # sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.ctime,0 AS isread
    #     FROM msg_send MS 
    #     LEFT JOIN users U ON U.usr_id=MS.cid
    #     LEFT JOIN dept DP ON DP.id = U.dept_id
    #     LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
    #     WHERE 1=1
    #     """
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.ctime,IFNULL(MSL.isread,0)
        FROM complaint_sup_msg_send_list MSL 
        LEFT JOIN complaint_sup_msg_send MS ON MS.id = MSL.m_id
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
        WHERE MSL.to_usr_id = %s AND MS.is_send = 1
        """%(usr_id_gy)
    if typeID !='':
        sql+="AND MS.mtype=%s "%typeID
    sql+="ORDER BY MSL.ctime DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id title cid usr_name dept_name type_name ctime isread'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def msgDetail(request):  
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    dept = 0
    pk = request.POST.get('pk','')
    # pk = 72
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
 
    sql = """select su.id,su.cname from users_gy u
             left join addr_book ab on u.addr_id = ab.id
             left join suppliers su on ab.sup_id = su.id
             where u.usr_id = '%s'"""%(usr_id_gy)
    print sql
    rows,iN=db.select(sql)
    sup_id = rows[0][0]

    sql = "select ifnull(ms.fb_status,0),Find_in_set(%s,ms.fb_pass),Find_in_set(%s,ms.fb_reject) from complaint_sup_msg_send ms where ms.id=%s"%(sup_id,sup_id,pk)
    print sql
    rows,iN=db.select(sql)
    fb_status = rows[0][0]
    if fb_status == 1:
        if rows[0][2] == 1:
            fb_status = -1
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.memo,MS.ctime,IFNULL(tb.status,0)
                 ,case IFNULL(tb.id,0) when 0 then IFNULL(msl.isjoin,0) else 1 end,MS.mtype,MS.cantalk,%s
        FROM complaint_sup_msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
        LEFT JOIN complaint_sup_msg_send_list MSL ON MSL.m_id = MS.id
        left join users_gy gy on gy.usr_id = MSL.to_usr_id
        left join addr_book ab on ab.id = gy.addr_id
        left join complaint_sup_toubiao tb on ms.id = tb.m_id and tb.sup_id = ab.sup_id
        WHERE MS.id=%s AND MSL.to_usr_id=%s
        """%(fb_status,pk,usr_id_gy)
    # print sql
    rows,iN=db.select(sql)

	#if iN == 0 :
    #    s = """
    #    {
    #    "errcode": -1,
    #    "errmsg": "该条信息已被删除"
    #    }        """
    #    return HttpResponseJsonCORS(s)
    
    names = 'id title cid usr_name dept_name type_name memo ctime status isjoin mtype cantalk feedback_status'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    #L = L.replace('/fs/editor_files','%s/editor_files'%fs_url)

    sql="""SELECT FB.id
        ,CASE FB.itype WHEN 'qy' THEN U.usr_name ELSE UG.usr_name END
        ,CASE FB.itype WHEN 'qy' THEN CONCAT('%s',U.pic) ELSE UG.headimgurl END
        ,FB.memo,DATE_FORMAT(FB.ctime,'%%Y-%%m-%%d %%H:%%i:%%s')
        FROM complaint_sup_msg_feedback FB
        LEFT JOIN users U ON U.usr_id = FB.cid
        LEFT JOIN users_gy UG ON UG.usr_id = FB.cid
        WHERE FB.m_id=%s
        ORDER BY FB.ctime DESC 
        """%(imgUrl,pk)
    rows,iN=db.select(sql)
    names = 'id usr_name pic memo ctime'.split()
    data = [dict(zip(names, d)) for d in rows]
    feedback = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s,
        "feedback":%s
        }        """%(L,feedback)
    # s=ToGBK(s)
    # 
    #阅读记录
    sql="""UPDATE complaint_sup_msg_send_list SET readtime=now(),isread = 1 WHERE m_id=%s AND to_usr_id = %s AND IFNULL(isread,0)=0"""%(pk,usr_id_gy)
    db.executesql(sql)
    return HttpResponseJsonCORS(s)

def putFeedback(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    memo = request.POST.get('memo','')
    memo = MySQLdb.escape_string(memo)
    sql="""INSERT INTO complaint_sup_msg_feedback(m_id,cid,ctime,memo,itype) VALUES(%s,%s,now(),'%s','fw')"""%(pk,usr_id_gy,memo)
    db.executesql(sql) 
    sql="""UPDATE complaint_sup_msg_send SET has_new=1 WHERE id=%s"""%pk
    db.executesql(sql)
    mWxPushMsg_Comment_qy(request,pk)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
    return HttpResponseJsonCORS(s)

def joinToubiao(request):  
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    is_join = request.POST.get('is_join','')
    cont = request.POST.get('cont','')
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT status FROM users_gy WHERE usr_id = %s """%usr_id_gy
    rows,iN=db.select(sql)
    if rows[0][0] !=1:
        s = """
        {
        "errcode": -2,
        "errmsg": "未绑定，不能参与投标"
        }        """
        return HttpResponseJsonCORS(s)

    if str(is_join) == '-1':  #不参与投标
        sql="""UPDATE complaint_sup_msg_send_list SET isjoin=-1,jointime=now(),memo='%s' WHERE m_id=%s AND to_usr_id=%s """%(cont,pk,usr_id_gy)
        db.executesql(sql)
        mWxPushMsg_NotJoin(request,pk,cont)
        s = """
        {
        "errcode": 0,
        "errmsg": "提交不参与投标成功"
        }        """
        return HttpResponseJsonCORS(s)
    
    sql = """select ifnull(tb.id,0)
             from complaint_sup_msg_send_list l
             left join users_gy gy on gy.usr_id = l.to_usr_id
             left join addr_book ab on ab.id = gy.addr_id
             left join complaint_sup_toubiao tb on l.m_id = tb.m_id and tb.sup_id = ab.sup_id
             WHERE l.m_id=%s AND l.to_usr_id=%s"""%(pk,usr_id_gy)
    rows,iN=db.select(sql)
    if iN>0:
        if rows[0][0]>0:
            s = """
        {
        "errcode": -3,
        "errmsg": "已参与投标，无需重复投标"
        }        """
            return HttpResponseJsonCORS(s)
   
    sql="""UPDATE complaint_sup_msg_send_list SET isjoin=1,jointime=now() WHERE m_id=%s AND to_usr_id=%s """%(pk,usr_id_gy)
    db.executesql(sql)
    sql = """INSERT INTO complaint_sup_toubiao (m_id,jointime, status, stime, sup_id, cid, msl_id) 
             select l.m_id,l.jointime,l.status,l.stime,ab.sup_id,gy.usr_id,l.id
             from complaint_sup_msg_send_list l
             left join complaint_sup_msg_send s on s.id = l.m_id
             left join users_gy gy on gy.usr_id = l.to_usr_id
             left join addr_book ab on ab.id = gy.addr_id
             WHERE l.m_id=%s AND l.to_usr_id=%s """%(pk,usr_id_gy)
    db.executesql(sql)
    mWxPushMsg_NewJoin(request,pk)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交投标申请成功"
        }        """
    return HttpResponseJsonCORS(s)

def payInfo(request):
    usr_id_gy = request.session.get('usr_id_gy','') or 0
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 2000001
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT PMP.pjname,SP.cname,PMP.bank_name,PMP.bank_no,PMP.cgzt_txt,PMP.pay_money 
        FROM prj_mat_pay PMP
        LEFT JOIN suppliers SP ON SP.id = PMP.sup_id
        WHERE PMP.id=%s
        """%pk
    rows,iN=db.select(sql)
    names = 'pjname spname bank_name bank_no pay_unit pay_money'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取付款信息成功",
        "data":%s
        }        """%(L)
    return HttpResponseJsonCORS(s)

def getInvoiceData(request):
    uuid = request.POST.get('seq') or request.GET.get('seq','')

    sql = "select req_no,pjname,gysname,gysct,gys_tel,sh_yf,'','','','',id,gw_id from prj_mat_pay1 where uuid='%s'"%(uuid)
    print sql
    rows,iN=db.select(sql)
    names = 'req_no proj_name gys_name gys_lxr gys_tel sh_yf lists others return_goods deduct_money'.split()
    if iN==0:
        s = """
        { 
        "errcode": -1,
        "errmsg": "获取发票清单信息失败"
        }        """
        return HttpResponseJsonCORS(s)

    L = list(rows[0])
    
    id = L[-2] 
    gw_id = L[-1] 
    sql1 = """select ml.rec_date,ml.Out_No,ml.mat_cname,ml.spec,ml.unit,ml.act_price,ml.Check_Amc,ml.act_money from prj_mat_list ml
              left join prj_mat_pay1 mp on mp.id = ml.pmp_id
              where mp.uuid='%s'"""%(uuid)
    
    rows1,iN1=db.select(sql1)
    names1 = 'rec_date Out_No mat_cname spec unit act_price Check_Amc act_money'.split()
    data1 = [dict(zip(names1, d)) for d in rows1]
    L[6] = data1

    sql1 = """select ml.ctime,ml.money,ml.b_type,ml.l_type from Prj_Mat_Master_other ml
              left join prj_mat_pay1 mp on mp.id = ml.pmp_id
              where mp.uuid='%s'"""%(uuid)
    
    rows1,iN1=db.select(sql1)
    names1 = 'rec_date money b_type l_type'.split()
    data1 = [dict(zip(names1, d)) for d in rows1]
    L[7] = data1

    sql1 = "select pms_id from prj_mat_pay_thd where gw_id = %s"%(gw_id)
    rows1,iN1=byaq.select(sql1)
    if iN1>0:
        pms_ids = ''
        for e in rows1:
           pms_ids = '%s,'%(e[0])
        pms_ids = pms_ids[:-1]
        sql1 = """SELECT
                    convert(varchar(10),pb.Collar_date,121) as '日期'
                    ,isnull(pb.Req_No,'') as '退货单号 ' 
                    ,isnull(mt.cname,'') as '物料名称  '                 
                    ,case isnull(ml.spec,'')+'+'+isnull(ml.Model,'') when '+' then '' else isnull(ml.spec,'')+'+'+isnull(ml.Model,'') end as '规格型号    '      
                    ,isnull(JL.cname,'') as '单位      '             
                    ,isnull(ml.act_price,0) as '单价        '      
                    ,isnull(ml.Check_Amc,0)    as '数量           ' 
                    ,isnull(ml.act_money,0) as '金额                '
                    ,'' as '发票号码'
                    ,'' as '发票金额'
                from Prj_Mat_List ml
                LEFT JOIN mat mt ON mt.id = ml.Mat_id
                LEFT JOIN units JL ON JL.id = mt.unit and JL.[status] = 1
                LEFT JOIN Prj_Mat_Master pb ON pb.id = ml.M_Id
                where 1=1 AND isnull(ml.mat_status,0)!='2' AND pb.Id in (%s) 
                order by pb.Collar_date desc"""%(pms_ids)
        rows1,iN1=byerp.select(sql1)
        names1 = 'Collar_date Req_No mat_name spec unit act_price Check_Amc act_money'.split()
        data1 = [dict(zip(names1, d)) for d in rows1]
        L[8] = data1
    sql1 = "select sum(amount) from prj_mat_pay_other where gw_id = %s"%(gw_id)
    rows1,iN1=byaq.select(sql1)
    if iN1>0:
        L[9] = rows1[0][0]

    data = dict(zip(names, L)) 
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)


    #标记已读
    sql = "update prj_mat_pay set wx_list_status = 4 where id = %s"%(id)
    print sql
    try:
        byaq.executesql(sql) 
    except:
        pass
    s = """
        {
        "errcode": 0,
        "errmsg": "获取发票清单信息成功",
        "data":%s
        }        """%(L)
    return HttpResponseJsonCORS(s)

def exportInvoiceExcel(request):
    uuid = request.GET.get('seq','')
    save_name = "%s.xls"%uuid
    sql = "select req_no,pjname,gysname,gysct,gys_tel,sh_yf,is_from_hxsh,gw_id from prj_mat_pay1 where uuid='%s'"%(uuid)
    print sql
    rows,iN=db.select(sql)
    if iN==0:
        s = """获取发票清单信息失败!"""
        return HttpResponse(s)
    is_from_hxsh = rows[0][6]
    gw_id = rows[0][7]
    if is_from_hxsh ==1:
        txt = '是'
    else:
        txt = '否'
    s = '''
<HTML >
    <HEAD><TITLE>深圳市宝鹰建设集团股份有限公司</TITLE>
        <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
    </HEAD>
    <BODY leftMargin="0" rightMargin="0" topMargin="0" marginheight="0" marginwidth="0">
    <TABLE width="921" height="30" align="center" bgcolor="white" border="0" cellPadding="0" cellSpacing="0" ><tbody><TR><TD>
    <div class='' style='width:921;margin:10px auto 10px auto;'>
                        <h4 style='text-align:right;'>%s</h4>
                        <h1 style='text-align:center;'>发票清单</h1><br/>
                        <h3 style='text-align:center;'>收货月份:%s</h3>
                        <h4 style='text-align:left;'>收货单位：%s 项目部 </h4>
                        <h4 style='text-align:right;float:right;'>是否通过供应链采购：%s </h4>
                    </div>
                </TD></TR>'''%(rows[0][0],rows[0][5],rows[0][1],txt)
    s += '''
	<TR><TD><TABLE width="921" height="30" align="center" bgcolor="white" border="0" cellPadding="0" cellSpacing="0" >
	<tbody><TR>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">日期</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">送货单号</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">物料名称</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">规格型号</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">单位</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">单价</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">数量</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">金额</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">发票号码</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">发票金额</TD>
	</TR>'''
    sql1 = """select date_format(ml.rec_date,'%%Y-%%m-%%d'),ml.Out_No,ml.mat_cname,ml.spec,ml.unit,ml.act_price,ml.Check_Amc,ifnull(ml.act_money,0) from prj_mat_list ml
              left join prj_mat_pay1 mp on mp.id = ml.pmp_id
              where mp.uuid='%s'"""%(uuid)
    
    rows1,iN1=db.select(sql1)
    total_money = 0
    for e in rows1:	
        total_money += e[7]
        s += '''
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;vnd.ms-excel.numberformat:@">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7])
    
    s += '''
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">入库金额合计</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;vnd.ms-excel.numberformat:@"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(total_money)

    sql1 = """select date_format(ml.ctime,'%%Y-%%m-%%d'),ml.money,ml.b_type,ml.l_type
              from Prj_Mat_Master_other ml
              left join prj_mat_pay1 mp on mp.id = ml.pmp_id
              where mp.uuid='%s'"""%(uuid)
    rows1,iN1=db.select(sql1)
    total_money1 = 0
    for e in rows1:	
        total_money1 += e[1]
        total_money += e[1]
    if iN1>0:
        s += '''<TR><td height="29" align="center" colspan="10" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">入库单--其他费用</td></TR>'''
        s += '''
    <TR>
	<TD width="100" height="29" align="center" colspan="2" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">日期</TD>
	<TD width="100" height="29" align="center" colspan="2" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">费用大类</TD>
	<TD width="90" height="29" align="center" colspan="3" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">费用子类</TD>
	<TD width="90" height="29" align="center" colspan="1" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">金额</TD>
	<TD width="90" height="29" align="center" colspan="2" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;"></TD>
	</TR>'''
    for e in rows1:	
        s += '''
	<TR><TD width="100" height="29"  colspan="2" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29"  colspan="2" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29"  colspan="3" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29"  colspan="1" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29"  colspan="2" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(e[0],e[2],e[3],e[1])

    if iN1>0:
        s += '''
	<TR><TD width="100" height="29" align="center" colspan="2" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">其他费用金额合计</TD>
	<TD width="90" height="29"  colspan="2" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29"  colspan="3" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29"  colspan="1" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29"  colspan="2" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(total_money1)

    sql1 = "select pms_id from prj_mat_pay_thd where gw_id = %s"%(gw_id)
    rows1,iN1=byaq.select(sql1)
    if iN1>0:
        pms_ids = ''
        for e in rows1:
           pms_ids = '%s,'%(e[0])
        pms_ids = pms_ids[:-1]
        sql1 = """SELECT
                    convert(varchar(10),pb.Collar_date,121) as '日期'
                    ,isnull(pb.Req_No,'') as '退货单号 ' 
                    ,isnull(mt.cname,'') as '物料名称  '                 
                    ,case isnull(ml.spec,'')+'+'+isnull(ml.Model,'') when '+' then '' else isnull(ml.spec,'')+'+'+isnull(ml.Model,'') end as '规格型号    '      
                    ,isnull(JL.cname,'') as '单位      '             
                    ,isnull(ml.act_price,0) as '单价        '      
                    ,isnull(ml.Check_Amc,0)    as '数量           ' 
                    ,isnull(ml.act_money,0) as '金额                '
                    ,'' as '发票号码'
                    ,'' as '发票金额'
                from Prj_Mat_List ml
                LEFT JOIN mat mt ON mt.id = ml.Mat_id
                LEFT JOIN units JL ON JL.id = mt.unit and JL.[status] = 1
                LEFT JOIN Prj_Mat_Master pb ON pb.id = ml.M_Id
                where 1=1 AND isnull(ml.mat_status,0)!='2' AND pb.Id in (%s) 
                order by pb.Collar_date desc"""%(pms_ids)
        rows1,iN1=byerp.select(sql1)
        if iN1>0:
            s += '''<TR><td height="29" align="center" colspan="10" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">退货单材料明细</td></TR>'''
            s += '''
	<TR>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">日期</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">退货单号</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">物料名称</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">规格型号</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">单位</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">单价</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">数量</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">金额</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">发票号码</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">发票金额</TD>
	</TR>'''
            total_money1 = 0
            for e in rows1:	
                total_money1 += e[7]
                s += '''
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;vnd.ms-excel.numberformat:@">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7])

            s += '''
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">入库金额合计</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;vnd.ms-excel.numberformat:@"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(total_money1)
            total_money = total_money - total_money1

    sql1 = "select isnull(sum(amount),0) from prj_mat_pay_other where gw_id = %s"%(gw_id)
    rows1,iN1=byaq.select(sql1)
    if iN1>0:
        total_money1 = rows1[0][0]
        if total_money1>0:
            s += '''
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">扣款金额合计</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;vnd.ms-excel.numberformat:@"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>'''%(total_money1)
        total_money = total_money - total_money1

    s += '''
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">本期合计</TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;">%s</TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	</TR>
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">前期开票金额 </TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;">
	</TD><TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD></TR>
	<TR><TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;background-color:#EAEAEA;">本期开票金额 </TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="90" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD>
	<TD width="100" height="29" align="center" class="TD1" style="border:1px solid #808080;"></TD></TR>
	</tbody></TABLE></TD></TR>
	<TR><TD><div class='' style='width:921;margin:50px auto 10px auto;'>
                        <h4 style='text-align:left;'>备注：<font color='red'>*不作为结算付款依据</font></h4>
                        <div style='float:left;width:400;'>
                            <h4 style='text-align:left;float:left'>供应商联系人：%s &nbsp;&nbsp;电话：%s</h4>
                        </div>
                        <h4 style='text-align:right;float:right;'>供应商名称：%s （盖章）</h4>
                    </div>
                </TD></TR>
	<TR><TD>
                            <h3 style='text-align:right;float:right;margin:15px auto 0px auto;'>年&nbsp;&nbsp;月&nbsp;&nbsp;日</h3>
    </TD></TR>
	</tbody></TABLE>
    </body></html>
            '''%(total_money,rows[0][3],rows[0][4],rows[0][2])
    response = HttpResponse(s)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"'%(save_name)

    return response
	
import httplib
def mWxPushMsg_NewJoin(request,pk):   
    year=getToday()[:4]  
    sql="""SELECT title FROM complaint_sup_msg_send WHERE id = %s"""%pk
    rows,iN=db.select(sql)
    msgTitle=rows[0][0]

    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    toUser = getRecvUser()
    toUser += '|liusq|gulq'
    sUrl='%s/complaint/login/login_qy?fid=infoDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,pk)
    stitle = """供应商招标新投标信息"""
    surl = my_urlencode(sUrl)
    description = """您发布的%s，有新投标报名信息啦。"""%(msgTitle)
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_gy,stitle,url,description)
    # print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return HttpResponseCORS(request,errcode)

def mWxPushMsg_NotJoin(request,pk,cont):   
    year=getToday()[:4]  
    sql="""SELECT title FROM complaint_sup_msg_send WHERE id = %s"""%pk
    rows,iN=db.select(sql)
    msgTitle=rows[0][0]
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    sql = """select su.id,su.cname from users_gy u
             left join addr_book ab on u.addr_id = ab.id
             left join suppliers su on ab.sup_id = su.id
             where u.usr_id = '%s'"""%(usr_id_gy)
    rows,iN=db.select(sql)
    sup_name=rows[0][1]

    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    toUser = getRecvUser()
    toUser += '|liusq'
    sUrl='%s/complaint/login/login_qy?fid=infoDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,pk)
    stitle = """不参与投标报名通知"""
    surl = my_urlencode(sUrl)
    description = """标题：%s\r\n供应商：%s\r\n不参与原因：%s\r\n"""%(msgTitle,sup_name,cont)
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_gy,stitle,url,description)
    # print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return HttpResponseCORS(request,errcode)


def mWxPushMsg_Comment_qy(request,pk):   
    year=getToday()[:4]  
    sql="""SELECT title FROM complaint_sup_msg_send WHERE id = %s"""%pk
    rows,iN=db.select(sql)
    msgTitle=rows[0][0]

    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    toUser = getRecvUser()
    toUser += '|liusq|gulq'
    sUrl='%s/complaint/login/login_qy?fid=infoDetail&func_id=1000004&seq=%s&must_reply=true'%(host_url,pk)
    stitle = """新留言提醒"""
    surl = my_urlencode(sUrl)
    description = """您发布的“%s”信息，有新的留言信息，请及时查看。"""%(msgTitle)
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_gy,stitle,url,description)
    # print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return HttpResponseCORS(request,errcode)

def getRecvUser():
    sql = """select GROUP_CONCAT(u.login_id) from roles r
           left join usr_role ur  on ur.role_id = r.role_id
           left join users u on ur.usr_id = u.usr_id
           where r.role_name = '招标专员（供应商服务平台）'"""
    rows,iN = db.select(sql)
    users=rows[0][0]
    users = users.replace(',','|')
    return users
