# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
import httplib
from django.db import connection
exec ('from %s.share import db,HttpResponseCORS,g_data,ToGBK,mValidateUser,fs_url,ComplexEncoder'%prj_name) 
from qr_code import genShdCode


#
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
from django.http import HttpResponse
#
def printShd(request):
    pk =  request.POST.get('pk') or  request.GET.get('pk','') 
    sql = """select op.cname,sh.sn,sh.ctime,su.cname,su.tel,sh.cusrname,ifnull(sh.qr_code,''),''
                   ,ht.req_no,cg.cusrname,m1.txt1,m2.txt1 
             from _m3000004_shd sh 
             left join _m1501_cgdd cg on sh.cgd_id = cg.id
             left join out_proj op on op.id = cg.proj_id
             left join suppliers su on su.id = cg.sup_id
             left join prj_mat_buy_ht ht on ht.id = cg.cght 
             left join mtc_t m1 on m1.type = 'cgzt' and m1.id = cg.cgzt
             left join mtc_t m2 on m2.type = 'cylgs' and m2.id = cg.gyl
             where sh.id=%s
             """%(pk)
    print sql
    rows,iN = db.select(sql)
    if iN == 0:
        s = """
        { 
        "errcode": -1,
        "errmsg": "获取送货单数据失败"
        }        """
        return HttpResponseCORS(request,s)

    L = list(rows[0])
    if L[6] == '':
        L[6] = genShdCode(pk)
        sql = "update _m3000004_shd set qr_code='%s' where id=%s"%(L[6],pk)
        db.executesql(sql)
    sql = "select cl_code,cl_name,cl_spec,cl_model,cl_type,cl_brand,cl_unit,replace(cast(ROUND(total_qty,2) as char),'.00',''),replace(cast(ROUND(qty,2) as char),'.00',''),ROUND(price,2),ROUND(amount,2),memo  from _m3000004_shd_list where m_id=%s"%(pk)
    rows1,iN1 = db.select(sql)
    names = 'cl_code cl_name cl_spec cl_model cl_type cl_brand cl_unit total_qty qty price amount memo'.split()
    L[7] = [dict(zip(names, d)) for d in rows1]

    names = 'proj_name shd_no sh_date sup_name sup_tel usr_name qr_code lists cght cg_usr_name cgzt gyl'.split()
    L2 = dict(zip(names, L))
    data = json.dumps(L2,ensure_ascii=False,cls=ComplexEncoder)    
    s = """
        {
        "errcode": 0,
        "errmsg": "获取送货单数据成功",
        "data":%s
        }        """%(data)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)

def printPdfShd(request):
    pk =  request.POST.get('pk') or  request.GET.get('pk','')
    sql = """select op.cname,sh.sn,sh.ctime,su.cname,su.tel,sh.cusrname,ifnull(sh.qr_code,''),''
                   ,ht.req_no,cg.cusrname,m1.txt1,m2.txt1 
             from _m3000004_shd sh 
             left join _m1501_cgdd cg on sh.cgd_id = cg.id
             left join out_proj op on op.id = cg.proj_id
             left join suppliers su on su.id = cg.sup_id
             left join prj_mat_buy_ht ht on ht.id = cg.cght 
             left join mtc_t m1 on m1.type = 'cgzt' and m1.id = cg.cgzt
             left join mtc_t m2 on m2.type = 'cylgs' and m2.id = cg.gyl
             where sh.id=%s
             """%(pk)
    # print sql
    rows,iN = db.select(sql)
    if iN == 0:
        s = """
        {
        "errcode": -1,
        "errmsg": "获取送货单数据失败"
        }        """
        return HttpResponseCORS(request,s)
    L = list(rows[0])
    if L[6] == '':
        L[6] = genShdCode(pk)
        sql = "update _m3000004_shd set qr_code='%s' where id=%s"%(L[6],pk)
        db.executesql(sql)
    sql = "select cl_code,cl_name,cl_spec,cl_model,cl_type,cl_brand,cl_unit,replace(cast(ROUND(total_qty,2) as char),'.00',''),replace(cast(ROUND(qty,2) as char),'.00',''),ROUND(price,2),ROUND(amount,2),memo  from _m3000004_shd_list where m_id=%s"%(pk)
    rows1,iN1 = db.select(sql)
    names = 'cl_code cl_name cl_spec cl_model cl_type cl_brand cl_unit total_qty qty price amount memo'.split()
    L[7] = [dict(zip(names, d)) for d in rows1] 

    names = 'proj_name shd_no sh_date sup_name sup_tel usr_name qr_code lists cght cg_usr_name cgzt gyl'.split()
    L2 = dict(zip(names, L))

    data = L2['lists'] # 材料明细内容数据
    #print ToGBK(s)
    


    # 页面大小   (四联二分217*140mm ，四联 217*280mm: 4.4 2.72)
    pageWidth = 21.7     
    pageHeight = 28.0
    response = HttpResponse(content_type='application/pdf')   

    pdf = canvas.Canvas(response) # 实例化pdf

    # 设置pdf样式 

    # 1 inch = 2.54cm  1cm = 28.346 dpi
    pdf.setPageSize((pageWidth*cm,pageHeight*cm)) # 尺寸
    pdf.setFont('song',9) # 设置字体
    
    # 加载图片 background
    two_dimensional_code_path = L2['qr_code']
    file_path = r"/home/webroot/data/lwerp/open/background/total.png"
    pdf.drawImage(file_path,0,0,pageWidth*cm,pageHeight*cm)                 # 背景
    pdf.drawImage(two_dimensional_code_path,17.3*cm,25.28*cm,2.6*cm,2.6*cm) # 二维码 

    # 加载内容

    amount = 15                     # 每页显示的数目 (四联二等分:5, 四联整张纸:15)
    pages = len(data)//amount + 1         # 页数
    # print data

    for index in range(pages):
        for i in range(min(len(data)-index*amount,amount)):
            i = int(index*amount + i)    # 索引位置
            print('i:',i)
            info = data[i]
            # 材料列表信息 
            x, y = 15, 18
            # for _ in info: 
            serize = str(i+1)
            material_number = info['cl_code']       # 材料编码
            material_name = info['cl_name']         # 材料名称
            standard = info['cl_spec']              # 规格
            material_model = info['cl_model']       # 型号
            material_brand = info['cl_brand']       # 品牌
            material_unit = info['cl_unit']         # 单位
            quantity_current = info['total_qty']    # 数量
            prince = info['price']                  # 数量
            amount = info['amount']                     
            remark = info['memo']
            # x, y = x+20, y+18
            pdf.drawString(x,y,material_number) # 处理
        pdf.showPage()
    pdf.save()
    return response

