# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import os
import string
import time,cStringIO
from string import split, strip, join, whitespace, find, replace

from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib import colors
from reportlab.lib.codecharts import KutenRowCodeChart, hBoxText
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch,cm
from reportlab.lib import styles
from reportlab.lib.utils import ImageReader
try: from Shared.PIL import Image as PIL_Image
except: from PIL import Image as PIL_Image

from reportlab.pdfbase.cidfonts import CIDFont, findCMapFile


from reportlab.pdfgen import canvas
from django.http import HttpResponse 

import base64
import json
import datetime
from HW_DT_TOOL                 import getToday
from HW_FILE_TOOL               import make_sub_path,readImage
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS,ToGBK,fs_url,ToUnicode,my_urlencode,oSysInfo,front_url,m_prjname,m_corp_wxid,data_url'%prj_name) 
 
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('song', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))  #注册字体

pdf_path = "/home/webroot/data/%s/open"%(m_prjname)

import qrcode
def printFACode(ids):
    sql = """select sn,name,type,brand
             from _m1102_gdzc_warehousing 
             where FIND_IN_SET(id,'%s')
             """%(ids)
    rows,iN = db.select(sql)
    if iN == 0:  #记录不存在    
        response = HttpResponse(content_type='application/pdf')  
        #response['Content-Disposition'] = 'attachment; filename=1.pdf'   
        p = canvas.Canvas(response)   
        p.setPageSize((24*cm,12*cm))
        p.setFont('song',9)
        p.drawString(1*cm, 1*cm, "记录不存在.")   
        p.showPage()  
        p.save()  
        return response
    name = "固定资产.pdf"
    # Create the HttpResponse object with the appropriate PDF headers.  
    response = HttpResponse(content_type='application/pdf')  
    #response['Content-Disposition'] = 'attachment; filename=%s'%ToGBK(name)   
    # Create the PDF object, using the response object as its "file."  
    p = canvas.Canvas(response)   
    # Draw things on the PDF. Here's where the PDF generation happens.  
    # See the ReportLab documentation for the full list of functionality.  
    #设置画布大小   
    canvasWidth = 10.2*cm
    canvasHeight = 3*cm
    p.setPageSize((canvasWidth,canvasHeight))
    
    i = 0
    
    for e in rows:
        code = e[0]
        
        #img = qrcode.make(url1)
        url = "%s/rd/?func=FA&code=%s"%(data_url,code)
        filename = pdf_path + "/FAcode/%s.png"%(code)
        #img.save(filename)
        logo = ''#pdf_path + "/sys/favicon.ico"
        gen_qrcode(url,filename,logo)
        
        left = 0.2*cm + (i%2)*5.2*cm
        top = canvasHeight - 0.8*cm 
        width = 2*cm
        height = 2*cm
        bottom = top - height
        p.drawImage(filename,left,bottom,width,height)
        
        p.setFillColor('black')
        bottom = canvasHeight - 0.5*cm 
        left = left + 0.2*cm
        p.setFont('song', 12 )
        p.drawString(left,bottom,'惠州神工木业有限公司')

        p.setFont('song', 6 )
        left = left + 1.9*cm
        bottom = top - 8
        p.drawString(left,bottom,'名称：%s'%(e[1]))
        bottom = bottom - 15
        p.drawString(left,bottom,'型号：%s'%(e[2]))
        bottom = bottom - 15
        p.drawString(left,bottom,'品牌：%s'%(str(e[3])))
        bottom = bottom - 15
        p.drawString(left,bottom,'编号：%s'%(str(e[0])))
        if i%2 ==1:      
            p.showPage()  
        i += 1
        
    p.save()  
    return response
    
def printQrCode(pk):
    sql = """select pl.bundle_code,p.stonename,sum(pl.square_real),count(1),ss.scsx_name from _m611_packing_list pl
            left join _m611_packing p on p.gw_id = pl.gw_id
            left join _m6031_stone_stock ss on ss.id = p.hl_id
            where p.gw_id = %s
            group by pl.bundle_code"""%(pk)
    rows,iN = db.select(sql)
    if iN == 0:  #记录不存在    
        response = HttpResponse(content_type='application/pdf')  
        response['Content-Disposition'] = 'attachment; filename=1.pdf'   
        p = canvas.Canvas(response)   
        p.setPageSize((24*cm,12*cm))
        p.setFont('song',9)
        p.drawString(1*cm, 1*cm, "记录不存在.")   
        p.showPage()  
        p.save()  
        return response
    
    name = rows[0][3]
    name = "%s.pdf"%(name)
    # Create the HttpResponse object with the appropriate PDF headers.  
    response = HttpResponse(content_type='application/pdf')  
    #response['Content-Disposition'] = 'attachment; filename=%s'%ToGBK(name)   
    # Create the PDF object, using the response object as its "file."  
    p = canvas.Canvas(response)   
    # Draw things on the PDF. Here's where the PDF generation happens.  
    # See the ReportLab documentation for the full list of functionality.  
    #设置画布大小   
    canvasWidth = 8*cm
    canvasHeight = 5*cm
    p.setPageSize((canvasWidth,canvasHeight))
    
    i = 0
      
    for e in rows:
        bundle_code = e[0]

        url = "http://pra.szhcsc.cn/qr/html/panelInfo.html?bundle_code=%s"%(my_urlencode(bundle_code))
        #url = my_urlencode(url)
        
        url1 = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx48f0396a58852d0c&redirect_uri=%s&response_type=code&scope=snsapi_base&state=123#wechat_redirect"%(url) 
        img = qrcode.make(url)
        filename = pdf_path + "/qrcode/%s.png"%(bundle_code)
        logo = pdf_path + "/sys/favicon.ico"
        gen_qrcode(url,filename,logo)
        #img.save(filename)
        
        left = 0.2*cm
        top = canvasHeight - 0.2*cm 
        width = 3.5*cm
        height = 3.5*cm
        bottom = top - height
        p.drawImage(filename,left,bottom,width,height)
        
        p.setFont('song', 8 )
        p.setFillColor('black')
        left = left + 3.8*cm
        bottom = top - 15
        p.drawString(left,bottom,'品名：%s'%(e[1]))
        bottom = bottom - 15
        p.drawString(left,bottom,'扎号：%s'%(e[0]))
        bottom = bottom - 15
        p.drawString(left,bottom,'片数：%s'%(str(e[3])))
        bottom = bottom - 15
        p.drawString(left,bottom,'平方数：%s㎡'%(str(e[2])))
        bottom = bottom - 30
        p.drawString(left,bottom,'扎数：%s'%(str(e[3])))
        bottom = bottom - 15
        p.drawString(left,bottom,'总平方数：%s㎡'%(str(e[2])))
        bottom = bottom - 30
        left = left - 3.8*cm
        p.setFont('song', 18 )
        p.drawString(left,bottom,'微信扫二维码下载电子码单')
        i += 1
        p.showPage()  
        
    p.save()  
    return response

def gen_qrcode(string, path, logo=""):  
    """
    生成中间带logo的二维码
    需要安装qrcode, PIL库
    :param string: 二维码字符串
    :param path: 生成的二维码保存路径
    :param logo: logo文件路径
    :return:
    """  
    qr = qrcode.QRCode(  
        version=2,  
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=8,  
        border=1  
    )  
    qr.add_data(string)  
    qr.make(fit=True)  
 
    img = qr.make_image()  
    img = img.convert("RGBA")  
 
    if logo and os.path.exists(logo):  
        icon = PIL_Image.open(logo)  
        img_w, img_h = img.size  
        factor = 4  
        size_w = int(img_w / factor)  
        size_h = int(img_h / factor)  
 
        icon_w, icon_h = icon.size  
        if icon_w > size_w:  
            icon_w = size_w  
        if icon_h > size_h:  
            icon_h = size_h  
        icon = icon.resize((icon_w, icon_h), PIL_Image.ANTIALIAS)  
 
        w = int((img_w - icon_w) / 2)  
        h = int((img_h - icon_h) / 2)  
        icon = icon.convert("RGBA")  
        img.paste(icon, (w, h), icon)  
    img.save(path)  