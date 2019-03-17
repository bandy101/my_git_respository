# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import os
import string
import time,cStringIO
from string import split, strip, join, whitespace, find, replace

from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.paragraph import Paragraph
#from reportlab.pdfbase.canvasframe import Canvas,Handle
#from reportlab.platypus.tables import Table,TableStyle
#from reportlab.platypus.doctemplate import *
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
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS,ToGBK,fs_url,ToUnicode,m_prjname'%prj_name) 


from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('song', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))  #注册字体

pdf_path = "/home/webroot/data/%s/open/pdf/"%(m_prjname)
def upload_pic(request):
    make_sub_path(pdf_path)#检查目录是否存在，如果不存在，生成目录  make_sub_path
    pic =  request.POST.get('imgData','')
    field_id = request.POST.get('field_id','')
    file_url = ''
    if pic!='':
        pic_ext = pic.split(';')[0]
        pic_ext = pic_ext.split('/')[-1]
        pic_data = pic.split(';')[1] 
        pic_data = pic_data.split(',')[-1]
        
        save_name='%s_%s.%s'%(field_id,time.time(),pic_ext)
        file_path=os.path.join(pdf_path,save_name)
    
        data= base64.b64decode(pic_data)
        f=open(file_path,'wb')
        f.write(data)
        f.flush()
        f.close()

        file_url='%s/%s/%s'%(fs_url,'pdf',save_name)
  
    s = """
        {
        "errcode":0,
        "errmsg":"保存成功",
        "url":"%s"
        }
        """%(file_url)   
    return HttpResponseCORS(request,s)

def pdfData(request):
    #print request.POST
    field_id = request.POST.get('field_id','')
    pk = request.POST.get('pk','')
    sql = "select id,table_name,'',1 from menu_pdf_source where menu_id='%s'"%(pk)
    NL,iN = db.select(sql)
    L = []
    for e in NL:
        row = list(e)
        p1 = []
        sql ="""SELECT col_name FROM menu_pdf_cols 
            where table_id=%s
            """%(e[0])
        L1,iN1 = db.select(sql)
        for e1 in L1:
            p1.append(e1[0])
        row[2] = p1
        L.append(row)
    L1 = [0,'运算符',['(',')',',','+','-','*','/'],0] 
    L.append(L1)
    L1 = [0,'函数',['F_SUM','F_YEAR','F_MONTH','F_DAY','F_PAGE','F_PAGE_COUNT'],0] 
    L.append(L1)
    L1 = [0,'金额大写函数',['F_UPPER','F_BIT_10','F_BIT_9','F_BIT_8','F_BIT_7','F_BIT_6','F_BIT_5','F_BIT_4','F_BIT_3','F_BIT_2','F_BIT_1','F_BIT_0','F_BIT_-1','F_BIT_-2'],0] 
    L.append(L1)
    L1 = [0,'常量',['￥'],0] 
    L.append(L1)
    names = 'id table_name cols type'.split()
    data = [dict(zip(names, d)) for d in L]
    data1 = json.dumps(data,ensure_ascii=False)

    pdfData = []
    L = []
    sql = "select id,formName,formWidth,formHeight,canvasWidth,canvasHeight from menu_pdf where field_id=%s"%(field_id)
    rows,iN = db.select(sql)
    if iN>0:
        sql = "select show_col,`left`,`right`,top,width,height,field_type,alignStyle,size,color,img_src,cid,mndata from menu_pdf_settings where field_id = %s and auto_add=0"%(field_id)
        NL,iN = db.select(sql)
        names = 'value left right top width height field_type alignStyle size color img_src cid mndata'.split()
        data = [dict(zip(names, d)) for d in NL]
        
        L1 = list(rows[0])
        L1[0] = data
        L.append(L1)
        names = 'fields formName formWidth formHeight canvasWidth canvasHeight'.split()
        data = [dict(zip(names, d)) for d in L]
        pdfData = json.dumps(data,ensure_ascii=False)

            
    s = """
        {
        "errcode":0,
        "errmsg":"获取数据成功",
        "data":%s,
        "pdfData":%s,
        }
        """%(data1,pdfData)
    return HttpResponseCORS(request,s)


def savePdfSetting(request):
    pk = request.POST.get('pk','')
    field_id = request.POST.get('field_id','')
    pdfData = request.POST.get('pdfData','')
    pdfData = json.loads(pdfData)
    #print pdfData
    fields = pdfData.get('fields','')
    formName = pdfData.get('formName','')
    formWidth = pdfData.get('formWidth','')
    formHeight  = pdfData.get('formHeight','')
    canvasWidth = pdfData.get('canvasWidth','')
    canvasHeight  = pdfData.get('canvasHeight','')
    sql = "select id from menu_pdf where field_id=%s"%(field_id)
    rows,iN = db.select(sql)
    if iN>0:
        sql = "update menu_pdf set formName='%s',formWidth=%s,formHeight=%s,canvasWidth=%s,canvasHeight=%s where field_id=%s"%(formName,formWidth,formHeight,canvasWidth,canvasHeight,field_id)
    else:
        sql = "insert into menu_pdf (formName,formWidth,formHeight,canvasWidth,canvasHeight,field_id) values ('%s',%s,%s,%s,%s,%s)"%(formName,formWidth,formHeight,canvasWidth,canvasHeight,field_id)
    db.executesql(sql)

    #获取明细表数据
    sql = "select id from menu_pdf_source where menu_id = %s and is_list =1;"%(pk)
    lT,iN=db.select(sql)
    if iN > 0:
        table_id = lT[0][0]
    else:
        table_id = 0

    sql = "delete from menu_pdf_settings where field_id=%s "%(field_id)
    db.executesql(sql)
    for e in fields:
        field_type = e.get('field_type','')
        value = e.get('value','')
        cols = ''
        cols = analyzeCol(value,cols)
        cid = e.get('cid','')
        width = e.get('width','')
        height = e.get('height','')
        right = e.get('right','')
        left = e.get('left','')
        top = e.get('top','')
        alignStyle = e.get('alignStyle','')
        size = e.get('size','')
        color = e.get('color','')
        img_src = e.get('img_src','')
        mndata = e.get('mndata','')
        is_list = 0
        if table_id != 0:
            sql = "select id from menu_pdf_cols where table_id = %s and FIND_IN_SET(col_name,'%s')"%(table_id,cols)
            lT,iN=db.select(sql)
            if iN>0:
                is_list = 1
            
        sql  = """insert into `menu_pdf_settings` (field_id,show_col,`left`,`right`,top,width,height
                                       ,field_type,alignStyle,size,color,img_src,cid,mndata,cols,is_list)
                         values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s);
               """%(field_id,value,left,right,top,width,height,field_type,alignStyle,size,color,img_src,cid,mndata,cols,is_list)
        db.executesql(sql)

    #处理列表的字段
    n = 0
    sql = "select show_col,count(1) from menu_pdf_settings where field_id = %s and is_list=1 group by show_col"%(field_id)
    rows,iN = db.select(sql)
    for e in rows:
        col_name = e[0]
        count = e[1]
        sql = "select id from menu_pdf_settings where field_id=%s and show_col='%s' order by top"%(field_id,col_name)
        rows1,iN1 = db.select(sql)
        n = 0
        for e1 in rows1:
            sql = "update menu_pdf_settings set rows=%s where id = %s"%(n,e1[0])
            db.executesql(sql)
            n += 1
    sql = "select rows from menu_pdf_settings where field_id=%s order by rows desc"%(field_id)
    rows,iN = db.select(sql)
    count = rows[0][0] + 1    
    sql = "update menu_pdf set rows=%s where field_id = %s"%(count,field_id)
    db.executesql(sql)

    sql = "update menu_pdf_settings s1,(select id from menu_pdf_settings where field_id = %s and show_col like '%%F_SUM(%%') s2 set s1.is_sum=1 where s1.id=s2.id"%(field_id)        
    db.executesql(sql)

    #处理大写金额字段
    sql = "select show_col,`left`,`right`,top,width,height,field_type,alignStyle,size,color,cols,is_sum,is_list from menu_pdf_settings where field_id=%s and show_col like '%%F_BIT_%%' order by `left`"%(field_id)
    rows1,iN1 = db.select(sql)
    if iN1>=2:
        col1 = rows1[0][0]
        left1 = rows1[0][1]
        pos1 = col1.find('(')
        func1 = col1[:pos1]
        bit1 = int(func1.split('_')[2])
        col2 = rows1[1][0]
        left2 = rows1[1][1]
        pos2 = col2.find('(')
        func2 = col2[:pos2]
        bit2 = int(func2.split('_')[2])
        for n in range(bit2+1,bit1):
            col3 = col1.replace('F_BIT_%s'%bit1,'F_BIT_%s'%n)
            left3 = left1 + ((left2 - left1)/(bit1-bit2))*(bit1-n)
            sql = """insert into `menu_pdf_settings` (field_id,show_col,`left`,`right`,top,width,height
                                       ,field_type,alignStyle,size,color,cols,is_sum,is_list,auto_add)
                         values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',1);
               """%(field_id,col3,left3,rows1[0][2],rows1[0][3],rows1[0][4],rows1[0][5],rows1[0][6],rows1[0][7],rows1[0][8],rows1[0][9],rows1[0][10],rows1[0][11],rows1[0][12])
            db.executesql(sql)

    s = """
        {
        "errcode":0,
        "errmsg":"保存成功",
        }
        """   
    return HttpResponseCORS(request,s)

def split_Row(s,m,mode='S'):
    m=m/2
    uc=unicode(ToGBK(s),'gb18030')
    L_ASCII=[]
    for n in range(0,128):
        s=unicode(str(chr(n)),'gb18030')
        L_ASCII.append(s)
    L_right_char=[',','。','?','；',"'",':',']','}','.','，','、','”','：']
    L_left_char=['“']
    L_uc_right=[]
    #for e in L_right_char:
    #    s=unicode(str(e),'gb18030')
    #    L_uc_right.append(s)
    L_uc_left=[]
    #for e in L_left_char:
    #    s=unicode(str(e),'gb18030')
    #    L_uc_left.append(s)
        
    n=0
    int_r=0
    str_temp=''
    L=[]
    while n <len(uc):
        s=uc[n]
        str_temp+=s
        
        if s in L_ASCII:
            int_r+=0.5
        else:
            int_r+=1 
        if int_r>=m or n==len(uc)-1:
            while n+1<len(uc) and(uc[n+1] in L_uc_right):
                n+=1
                str_temp+=uc[n]
            s=str_temp
            L.append(s)
            int_r=0
            str_temp=''
        n+=1   
    return L

def split_txt(str,split_length):
    #分隔一段文本为list
    #格式为：['']['']
    if str == '' or str == None: str=' '
    L2=str.split('\n')            #分隔段落，每个段落一个大list
    L_txt=[]   #返回的list
    for m in L2:
        L_A=split_Row(m,split_length)
        for X in L_A:
            L_txt.append(X)
    return L_txt

def getMenu_id(field_id):
    sql = "select s.menu_id from `menu_form_cols` c left join `menu_form_steps` s on s.id=c.step_id where c.id=%s"%(field_id)
    rows,iN = db.select(sql)
    if iN >0:
        return rows[0][0]
    return 0

def printPDF(request):
    field_id = request.GET.get('field_id','')
    pk = request.GET.get('pk','')
    menu_id = getMenu_id(field_id)
    if str(menu_id) == '611':
        return printQrCode(pk)
    if str(menu_id) == '1102':
        return printFACode(pk)
    value_dict,count =  setStaticData(pk,menu_id)
    
    #获取数据
    sql = """select formName,formWidth,canvasWidth,canvasHeight,rows from menu_pdf where field_id=%s"""%(field_id)
    rows,iN = db.select(sql)
    if iN == 0:  #记录不存在    
        response = HttpResponse(content_type='application/pdf')  
        response['Content-Disposition'] = 'attachment; filename=1.pdf'   
        p = canvas.Canvas(response)   
        p.setPageSize((24*cm,12*cm))
        p.setFont('song',9)
        p.drawString(1*cm, 1*cm, "该功能尚未配置.")   
        p.showPage()  
        p.save()  
        return response
    name = rows[0][0]
    formWidth = rows[0][1]
    canvasWidth = rows[0][2]
    canvasHeight = rows[0][3]
    row_count = rows[0][4]
    scale = canvasWidth *cm/formWidth
    #print "scale=%s"%scale
    
    name = "%s_%s.pdf"%(name,pk)
    # Create the HttpResponse object with the appropriate PDF headers.  
    response = HttpResponse(content_type='application/pdf')  
    #response['Content-Disposition'] = 'attachment; filename=%s'%ToGBK(name)   
    # Create the PDF object, using the response object as its "file."  
    p = canvas.Canvas(response)   
    # Draw things on the PDF. Here's where the PDF generation happens.  
    # See the ReportLab documentation for the full list of functionality.  
    #设置画布大小    
    p.setPageSize((canvasWidth*cm,canvasHeight*cm))

    sql = "select is_list from menu_pdf_settings where field_id=%s "%(field_id)
    rows,iN = db.select(sql)
    is_list = 0
    for e in rows:
        if e[0] == 1:
            print "e=%s"%e[0]
            is_list = 1
            break
    if is_list==0:count = 1
    pages = (count-1)/row_count + 1
    for n in range(0,pages):
        #加载背景图
        sql = "select img_src,`left`,top from menu_pdf_settings where field_id=%s and field_type='background_picture'"%(field_id)
        rows,iN = db.select(sql)
        if iN>0:
            img_src = rows[0][0]
            filename = img_src.split('/')[-1]
            file_path=os.path.join(pdf_path,filename)
            #image=ImageReader(file_path)
            p.drawImage(file_path,0,0,canvasWidth*cm,canvasHeight*cm)
        
        
        #加载图片
        sql = "select img_src,`left`,top,width,height from menu_pdf_settings where field_id=%s and field_type='picture'"%(field_id)
        rows,iN = db.select(sql)
        for e in rows:
            img_src = e[0]
            filename = img_src.split('/')[-1]
            file_path=os.path.join(pdf_path,filename)
            left = e[1] * scale
            top = canvasHeight*cm - e[2] * scale 
            width = e[3] * scale
            height = e[4] * scale
            bottom = top - height
            #image=ImageReader(file_path)
            p.drawImage(file_path,left,bottom,width,height)
        
        #加载文字
        sql = "select show_col,`left`,`right`,top,width,height,alignStyle,ifnull(size,10),ifnull(color,''),cols,is_list,rows,is_sum from menu_pdf_settings where field_id=%s and field_type='text' order by top"%(field_id)
        rows,iN = db.select(sql)
        for e in rows:
            show_col = packData(e[0],e[9],value_dict,n,count,row_count,e[10],e[11],e[12])
            left = e[1] * scale
            right = canvasWidth*cm - e[2] * scale
            top = canvasHeight*cm - e[3] * scale 
            width = e[4] * scale
            height = e[5] * scale
            bottom = top - 8
            size = e[7]
            size.replace('px','')
            p.setFont('song',int(size) - 2 )
            color = e[8]
            if color!='':
                p.setFillColor(color)
            else:
                p.setFillColor('black')
            align = e[6]
            if show_col =='(X)':
                file_path=os.path.join(pdf_path,'xx.gif')
                p.drawImage(file_path,left,bottom,10,10)
            else:
                if align == 'rightAlign':
                    p.drawRightString(right,bottom,show_col)
                else:
                    p.drawString(left,bottom,show_col)
        
        #加载多行文字
        sql = "select show_col,`left`,`right`,top,width,height,alignStyle,ifnull(size,10),ifnull(color,''),cols,is_list,rows,is_sum from menu_pdf_settings where field_id=%s and field_type='textarea'"%(field_id)
        rows,iN = db.select(sql)
        for e in rows:
            show_col = packData(e[0],e[9],value_dict,n,count,row_count,e[10],e[11],e[12])
            left = e[1] * scale
            right = canvasWidth*cm - e[2] * scale
            top = canvasHeight*cm - e[3] * scale 
            width = e[4] * scale
            height = e[5] * scale
            bottom = top - 10
            size = e[7]
            if size == '': size = 10
            p.setFont('song',int(size) - 2 )
            color = e[8]
            if color!='':
                p.setFillColor(color)
            else:
                p.setFillColor('black')
            align = e[6]
            s=split_txt(show_col,int(width/4) + 5)
            for A in s:
                p.drawString(left,bottom,A)
                bottom -= 12
        
            #if align == 'rightAlign':
            #    p.drawRightString(right,bottom,show_col)
            #else:
            #p.drawString(left,bottom,show_col)
        
        p.showPage()  
        
    p.save()  
    return response

def setStaticData(pk,menu_id):
    #获取主表数据
    value_dict = dict()    
    sql = """select id,table_name,table_sql from menu_pdf_source where menu_id = %s and is_list =0;"""%(menu_id)
    #print sql
    lT,iN=db.select(sql)
    if iN == 0:
        return value_dict,0
    else:
        table_id = lT[0][0]
        table_sql = lT[0][2]
    sql = "select col_name,show_col from menu_pdf_cols where table_id=%s and col_name != '审批流程'"%(table_id)
    lT,iN=db.select(sql)
    if iN == 0:
        return value_dict,0
    else:
        sql = "select "
        for e in lT:
            sql += " %s,"%e[1]
        sql = sql[:-1]
        sql += ' '
        sql += table_sql
        sql = sql.replace('$s',pk)
        print ToGBK(sql)
        rows,iN=db.select(sql)
        L=list(rows[0])
        for n in range(len(L)):
            if L[n] is None:L[n]=''
            value_dict[lT[n][0]] = L[n]
    sql="""SELECT GFD.cname,U.usr_name,case GFH.opt when 1 then '通过' when 0 then '<font color=red>退回</font>' else '' end,
                   ifnull(GFH.memo,''),ifnull(date_format(GFH.send_flow_time,'%%Y-%%m-%%d %%H:%%i'),''),D.finish
                   FROM gw_flow_his GFH
                   LEFT JOIN gw_flow_def GFD ON GFD.id=GFH.flow_id
                   LEFT JOIN users U ON U.usr_id=GFH.cid
                   LEFT JOIN gw_doc D ON D.id = GFH.m_id
                   WHERE GFH.m_id=%s AND GFH.ctime IS NOT NULL AND GFH.opt=1 AND NOT EXISTS
                   (SELECT 1 FROM gw_flow_his FH2 WHERE FH2.id > GFH.id AND FH2.cid = GFH.cid AND FH2.flow_id=GFH.flow_id AND FH2.m_id = D.id AND FH2.ctime IS NOT NULL)
                   ORDER BY GFH.id ASC
            """%pk
    lT,iN=db.select(sql)
    L1=list(lT)
    s = ''
    for n in range(len(L1)):
        L1[n]=list(L1[n])
        for i in range(len(L1[n])):
            if i==3:
                L1[n][i]=L1[n][i].replace('\n','')#去掉回车换行符，一会打印表单时，另外根据表单的宽度进行手工换行
        s+='【%s】 %s：%s(%s %s)\n'%(L1[n][0],L1[n][1],L1[n][2],L1[n][3],L1[n][4])
    if iN>0 and L1[0][5]==1:
        s += ' 办结'
    value_dict['flow'] = s
    count = 1
    #获取明细表数据
    sql = "select id,table_name,table_sql from menu_pdf_source where menu_id = %s and is_list =1;"%(menu_id)
    lT,iN=db.select(sql)
    if iN == 0:
        return value_dict,count
    else:
        table_id = lT[0][0]
        table_sql = lT[0][2]
    sql = "select col_name,show_col from menu_pdf_cols where table_id=%s"%(table_id)
    lT,iN=db.select(sql)
    if iN == 0:
        return value_dict,count
    else:
        sql = "select "
        for e in lT:
            sql += " %s,"%e[1]
        sql = sql[:-1]
        sql += table_sql
        sql = sql.replace('$s',pk)

        #print ToGBK(sql)
        rows,iN1=db.select(sql)
        for n in range(0,iN):
            L3 = []
            for e1 in rows:
                L3.append(e1[n])
            value_dict[lT[n][0]] = L3
        count = iN1
    return value_dict,count

def analyzeCol(value,cols):
    str = value
    pos1 = str.find('{')
    pos2 = str.find('}')
    if pos1>=0:
        cols += ',%s'%str[pos1+1:pos2]
    else:
        return cols
    str = str[pos2+1:]
    if len(str)>1:
        cols = analyzeCol(str,cols)
    return cols

def chn_cap(value):
    dc={0:'零',1:'壹',2:'贰',3:'叁',4:'肆',
        5:'伍',6:'陆',7:'柒',8:'捌',9:'玖'
        }
    pos1 = value.find('(')
    pos2 = value.find(')')
    func = value[:pos1]
    bit = int(func.split('_')[2])
    
    f_value = float(value[pos1+1:pos2])
    if f_value < pow(10,bit-1):
        return ''
    elif f_value < pow(10,bit):
        return '(X)'
    else:
        i_value = (int(f_value/pow(10,bit)))%10
    return dc[i_value]

def chn_upper(value):
    dc={0:'零',1:'壹',2:'贰',3:'叁',4:'肆',
        5:'伍',6:'陆',7:'柒',8:'捌',9:'玖'
        }
    bit={0:'分',1:'角',2:'元',3:'拾',4:'佰',
        5:'仟',6:'万',7:'拾',8:'佰',9:'仟',10:'亿',11:'拾',12:'佰'
        }
    pos1 = value.find('F_UPPER(')
    pos2 = value.find(')',pos1)
    f_value = float(value[pos1+8:pos2])
    return num2chn(f_value)

def IIf( b, s1, s2):
    if b:
        return s1
    else:
        return s2
def num2chn(nin=None):
    cs =('零','壹','贰','叁','肆','伍','陆','柒','捌','玖','◇','分','角','圆','拾','佰','仟','万','拾','佰','仟','亿','拾','佰','仟','万')

    st = ''; st1=''
    s = '%0.2f' % (nin)
    sln =len(s)

    if sln >15: return ''

    fg = (nin<1)

    for i in range(0, sln-3):
        ns = ord(s[sln-i-4]) - ord('0')
        st=IIf((ns==0)and(fg or (i==8)or(i==4)or(i==0)), '', cs[ns]) + IIf((ns==0)and((i<>8)and(i<>4)and(i<>0)or fg
        and(i==0)),'', cs[i+13]) + st
        fg = (ns==0)

    fg = False

    for i in [1,2]:
        ns = ord(s[sln-i]) - ord('0')
        st1 = IIf((ns==0)and((i==1)or(i==2)and(fg or (nin<1))), '', cs[ns]) + IIf((ns>0), cs[i+10], IIf((i==2) or fg, '', '整')) + st1
        fg = (ns==0)

    st.replace('亿万','万')

    return IIf( nin==0, '零', st + st1)

def packData(show,cols,value_dict,page,count,page_rows,is_list,rows,is_sum):
    value = show
    col_list = cols.split(',')
    for e in col_list:
        if e =='':continue
        if is_sum == 1:
            v_list = value_dict.get(e,'')
            sum = 0
            for e1 in v_list:
                sum += float(e1)   
            if value.find('F_BIT_')<0:
                if page < (count-1)/page_rows:
                    value = '   /    '
                else:
                    value = value.replace('F_SUM({%s})'%e,'%.02f'%sum) 
            else:
                if page < (count-1)/page_rows:
                    value = ''
                else:
                    value = value.replace('F_SUM({%s})'%e,str(sum)) 
                    value = chn_cap(value)
        elif is_list == 1:
            v_list = value_dict.get(e,'')
            n = page*page_rows + rows
            if n<count:
                if type(v_list)==list: 
                    vl = v_list[n]
                else:vl = v_list
                if vl == None: vl= ''
                value = value.replace('{%s}'%e,str(vl)) 
            else: value=''
        else:
            if e == '审批流程':
                v = value_dict.get('flow','')
            else:
                v = value_dict.get(e,'')
            value = value.replace('{%s}'%e,str(v)) 
    #print "%s page=%s count=%s page_rows=%s"%(ToGBK(show),page,count,page_rows)
    if value.find('F_BIT_')>=0:
        value = chn_cap(value)
    if value.find('F_UPPER(')>=0:
        value = chn_upper(value)
    if str(value).find('F_YEAR(')>=0:
        value = F_YEAR(value)
    if str(value).find('F_MONTH(')>=0:
        value = F_MONTH(value)
    if str(value).find('F_DAY(')>=0:
        value = F_DAY(value)
    if str(value).find('F_PAGE_COUNT')>=0:
        v = "%s"%(page+1)
        value = value.replace('F_PAGE_COUNT',v)
    elif str(value).find('F_PAGE')>=0:
        v = "%s/%s"%(page+1,(count-1)/page_rows + 1)
        value = value.replace('F_PAGE',v)
    return value

def F_YEAR(value):
    pos1 = value.find('F_YEAR(')
    pos2 =  value.find(')',pos1)
    day = value[pos1+7:pos2]
    year = day[0:4]
    return year
def F_MONTH(value):
    pos1 = value.find('F_MONTH(')
    pos2 =  value.find(')',pos1)
    day = value[pos1+8:pos2]
    day1 = day[5:7]
    return day1
def F_DAY(value):
    pos1 = value.find('F_DAY(')
    pos2 =  value.find(')',pos1)
    day = value[pos1+6:pos2]
    day1 = day[8:10]
    return day1