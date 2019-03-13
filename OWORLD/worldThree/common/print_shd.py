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
from django.http import HttpResponse
from django.http import Http404

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
    flag =  request.POST.get('flag') or  request.GET.get('flag','') # 0:半 1 ：全张
    token = request.POST.get('accessToken') or  request.GET.get('accessToken','')
    # token = 'VURsNXBvQVZwR2k5eFpYS1Iva05SK2dXc21hV2xVa05GakkvdjdvTFJ0Zz0gMTU0MzM5MTcyNS44NyA5NzEwOTYgZWVhZDI4Mzg5MTU1MjAwMGEwZmM3NDU5NjBlYTI1MmY5OTYyMjU0ZQ=='
    
    _sql = """select usr_id from users_login_gy where token='%s'
           """%(token)
    print (_sql)
    _t,_ = db.select(_sql)
    print(_t)
    if not _t:
        raise Http404("没有权限访问")

    sql = """select op.cname,sh.sn,sh.ctime,su.cname,su.tel,sh.cusrname,ifnull(sh.qr_code,''),''
                   ,ht.req_no,cg.cusrname,m1.txt1,m2.txt1 
             from _m3000004_shd sh 
             left join _m1501_cgdd cg on sh.cgd_id = cg.id
             left join out_proj op on op.id = cg.proj_id
             left join suppliers su on su.id = cg.sup_id
             left join prj_mat_buy_ht ht on ht.id = cg.cght 
             left join mtc_t m1 on m1.type = 'cgzt' and m1.id = cg.cgzt
             left join mtc_t m2 on m2.type = 'cylgs' and m2.id = cg.gyl
             where sh.id=%s and sh.cid=%s
             """%(pk,_t[-1][-1])
    # print sql
    rows,iN = db.select(sql)
    if iN == 0:
        s = """
        {
            本张送货单不存在或您没有查看权限！
        }        """
        # return HttpResponseCORS(request,s)
        raise Http404(s)
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
    
    # 页面大小   (四联二分217*140mm ，四联 217*280mm)
    pageWidth = 21.7     
    pageHeight = 28.0
    amounT = 15 # 每页显示的数目 (四联二等分:5, 四联整张纸:15)
    if flag in [0,'0']:
        amounT = 5                     
    imgName = 'total'
    if amounT-15:
        pageWidth, pageHeight= 21.7, 14.0
        imgName = 'half'
    response = HttpResponse(content_type='application/pdf')   
    global pdf
    pdf = canvas.Canvas(response) # 实例化pdf

    # 设置pdf样式 

    # 1 inch = 2.54cm  1cm = 28.346 dpi
    pdf.setPageSize((pageWidth*cm,pageHeight*cm)) # 尺寸

    pages = len(data)//amounT + 1         # 页数
    for index in range(pages):
        pdf.setFont('song',25) # 设置标题字体
        
        # 加载图片 background
        two_dimensional_code_path = L2['qr_code']   # 二维码
        file_path = r"/home/webroot/data/lwerp/open/background/"+str(imgName)+".png"
        pdf.drawImage(file_path,0,0,pageWidth*cm,pageHeight*cm)                 # 背景
        pdf.drawImage(two_dimensional_code_path,17.61*cm,24.3*cm-(15-amounT)*40,2.82*cm,2.82*cm) # 二维码 

        tel = L2['sup_tel']                   # 电话
        usr_name = L2['usr_name']             # 制单人
        cg_usr_name = L2['cg_usr_name']       # 采购员
        shd_no = L2['shd_no']                 # 送货单号
        cgzt   = L2['cgzt']                   # 采购主体
        zt = L2['sup_name']                           # 送货单最上面大字
        project_name = L2['proj_name']     # 收货项目
        sh_date = L2['sh_date']                   # 送货日期
        all_amount  = 0.                       # 合计金额
        
        pdf.drawString(21,755-(15-amounT)*40,str(zt))    # 送货单最上面大字
        pdf.setFont('song',9) # 设置文字字体  

        pdf.drawString(135,21.5,str(cg_usr_name)) # 采购员
        pdf.drawString(55,21.5,str(usr_name))    # 制单人
        #  页码

        pdf.drawString(65,727-(15-amounT)*39.65,str(shd_no))    # 送货单号
        pdf.drawString(65,711-(15-amounT)*39.65,str(cgzt))    # 采购主体
        pdf.drawString(65,694-(15-amounT)*39.65,str(project_name))    # 收货项目

        pdf.drawString(220,727-(15-amounT)*39.65,str(sh_date)[:10])           # 送货(开单)日期
        pdf.drawString(361,727-(15-amounT)*39.65,str(tel))    # 电话
        # 购买方式
        buyWay = '赊购'.encode('utf-8')
        pdf.drawString(335,711-(15-amounT)*39.65,buyWay)
        # ---------------   #
        #   y坐标：Y + 100 = 上升 2.5格 -->1格：40
        x = 32  # 序号
        x1, y = 48, 638-(15-amounT)*40 # x：材料名称的x1坐标 y:第一行记录初始y坐标
        x2 = x1 +60     # 材料名称
        x3 = x2 + 90 # 规格
        x4 = x3 + 70 # 型号
        x5 = x4 +47 # 品牌
        x6 = x5 + 40 # 单位
        x7 = x6 + 22 # 数量
        x8 = x7 + 50 # 单价
        x9 = x8 + 37 # 金额
        x10 = x9 + 51 # 备注
        for i in range(min(len(data)-index*amounT,amounT)):
            i = int(index*amounT + i)    # 索引位置
            info = data[i]
            # 材料列表信息 

            serize = str(i+1)                       # 序号
            material_number = info['cl_code']       # 材料编码
            # x,y = 800,900
            material_name = info['cl_name']         # 材料名称
            standard = info['cl_spec']              # 规格
            material_model = info['cl_model']       # 型号
            material_brand = info['cl_brand']       # 品牌
            material_unit = info['cl_unit']         # 单位
            quantity_current = info['total_qty']    # 数量
            prince = info['price']                  # 单价
            amount = info['amount']                 # 金额
            remark = info['memo']                   # 备注
            all_amount =all_amount + float(amount)    # 合计金额
            drawText(x1+2,y,material_number,10)    # 写入材料编码
            
            pdf.drawString(x,y,serize) # 序号
            # _t = '一二三四五六七八九'    # 9个汉字 =17 个字母
            # 写入双行 18长度限制 3
            drawText(x2,y,material_name,17)     # 材料名称
            drawText(x3,y,standard,12)         # 规格
            drawText(x4,y,material_model,11)    # 型号
            drawText(x5,y,material_brand,9)     # 品牌
            drawText(x6,y,material_unit,5)     # 单位
            drawText(x7,y,quantity_current,5)     # 单位
            drawText(x8,y,prince,5)     # 单价
            drawText(x9,y,amount,25)     # 金额
            drawText(x10,y,remark,19)     # 备注
            y = y - 40  #  Y + 100 = 上升 2.5格 --1：40 
        pdf.drawString(460,46,str(all_amount))          # 总额
        pdf.drawString(115,46,str(process_all_amount(all_amount)))  # 大写
        pdf.drawString(542,21.5,"{}/{}".format(index+1,pages))                              # 页码
        pdf.showPage()

    # 其他变量
    # pdf.
    pdf.save()
    return response

# 返回字节数
def calLength(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length)//2 + length
    return length

# 多行绘制文本
def drawText(x,y,V,length):
    V = str(V)
    global pdf
    L = calLength(V)
    _tempI = None
    # pdf.drawString(200,200,str(L))
    if 2*length> L > length:
        for _tempI in range(3):
            try:
                pdf.drawString(x,y+5,V[:length+_tempI])
                pdf.drawString(x,y-5,V[length+_tempI:])
                break
            except:
                pass
        else:
            pdf.drawString(x,y-5,'内容加载错误!')

    elif L>2*length:
        for _tempI in range(3):
            try:
                pdf.drawString(x,y+5,V[:length+_tempI])
                break
            except:
                pass
        drawText(x,y-10,V[length+_tempI:],length)
        
    else:
        pdf.drawString(x,y,V)

# 转换对应金额至中文
def process_all_amount(value):
    prefix={0:'零',1:'壹',2:'贰',3:'叁',4:'肆',
        5:'伍',6:'陆',7:'柒',8:'捌',9:'玖'
        }
    suffix={0:'分',1:'角',2:'圆',3:'拾',4:'佰',
        5:'仟',6:'万',7:'拾',8:'佰',9:'仟',10:'亿',11:'拾',12:'佰'
        ,13:'仟',14:'万'}
    temp = [] # 转换容器
    value =  '{:.2f}'.format(float(value))
    _value = str(value).replace('.','')
    for i,v in enumerate(_value):
        v = int(v)
        if v%10:    # 不为0
            temp.extend((prefix[v],suffix[len(_value)-i-1])) # 前缀+后缀
        else:
            if suffix[len(_value)-i-1] in ['圆',] and int(float(value)):
                temp.append(suffix[len(_value)-i-1])
            else:
                if suffix[len(_value)-i-1] not in ['分','角'] and temp:
                    if temp[-1]!='零':
                        temp.append(prefix[v])
    return ''.join(temp)
