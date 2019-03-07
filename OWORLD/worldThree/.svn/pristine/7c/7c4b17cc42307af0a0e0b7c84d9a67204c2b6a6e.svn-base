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

pdf_path = "/home/webroot/data/lwerp/open/qr_code/shd"

import qrcode
def genShdCode(pk):
    url = "https://lw.szby.cn/complaint/login/login_qy?fid=shd&func_id=1000004&pk=%s"%(pk)
    filename = pdf_path + "/%s.png"%(pk)
    logo = ''#pdf_path + "/sys/favicon.ico"
    gen_qrcode(url,filename,logo)
    qr_code = "https://lw.szby.cn/fs/qr_code/shd/%s.png"%(pk)
    return qr_code 
    
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