# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
from complaint.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,m_sCorpID,m_sCorpSecret,m_sAgentId_gy,m_sCorpSecret_gy
from complaint.share        import checkSession,data_url,host_url,my_urlencode,read_access_token_common,write_access_token_common,byerp
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
from HW_DT_TOOL                 import getToday
from HW_FILE_TOOL               import make_sub_path,readImage
import MySQLdb
# testid = 469
from PIL import Image

import base64 
import urllib 
import hmac
import hashlib

testid = 1087
upload_path = "/home/webroot/data/%s/attach_files/licence"%(prj_name)
upload_path_mat = "/home/webroot/data/%s/attach_files/mat_souring"%(prj_name)
front_url = 'https://lw.szby.cn/attach/licence'
front_url_mat = 'https://lw.szby.cn/attach/mat_souring'

data_url = 'https://lw.szby.cn/complaint/gy/sign_up'

appid = 1256868860
bucket = 'gy'
secret_id = "AKID2zkJhsixlPzOqAqHbjfO4eGk2HTZpBh1"
secret_key = "HNGxb9YnrmV3QbZadYIqDNL7h5HICuPl"

def upload_licence(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        file_type = request.POST.get('file_type', '1')
        random_no = request.POST.get('random_no', '')
        if str(file_type) == '7':
            usr_id_gy = request.session.get('usr_id_qy','')
            upload_path1 = upload_path_mat
            front_url1 = front_url_mat
        else:
            usr_id_gy = request.session.get('usr_id_gy','') or testid
            upload_path1 = upload_path
            front_url1 = front_url

        if usr_id_gy ==0:
            s = """
            {
            "errcode": -1,
            "errmsg": "无权访问,请先关注"
            }        """
            return HttpResponseJsonCORS(s)
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            s = """
                {
                "error": true
                }
                """
            return HttpResponseJsonCORS(s)
        title = myFile.name
        f_ext=title.split('.')[-1]
        fname = "%s_%s_%s.%s"%(usr_id_gy,time.time(),random.randint(0,99),f_ext)

        path=os.path.join(upload_path1,str(usr_id_gy))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        destination = open(os.path.join(path,fname),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  

        if str(file_type) == '1':
            title = u'营业执照.%s'%(f_ext)
        elif str(file_type) == '2':
            title = u'组织机构代码证.%s'%(f_ext)
        elif str(file_type) == '3':
            title = u'税务登记证.%s'%(f_ext)
        elif str(file_type) == '4':
            title = u'身份证正面.%s'%(f_ext)
        elif str(file_type) == '5':
            title = u'身份证反面.%s'%(f_ext)

        import imghdr
        imgType = imghdr.what(os.path.join(path,fname))
        if imgType in['rgb','gif','pbm','pgm','ppm','tiff','rast','xbm','jpeg','bmp','png']:
            is_pic = 1
        else:
            is_pic=0

        if str(file_type) in ['1','2','3','4','5']:
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=%s"%(usr_id_gy,file_type)
            lT,iN=db.select(sql)
            if iN>0:
                L=list(lT[0])
                fname1=L[0]
                path1=os.path.join(upload_path1,str(usr_id_gy))
                if fname1!='':
                    path1=os.path.join(path1,fname1)
                    try:
                        os.remove(path1)
                    except:
                        pass                        
                sql="delete from suppliers_pic WHERE cid=%s and file_type=%s"%(usr_id_gy,file_type)
                db.executesql(sql)

        sql = """insert into suppliers_pic (title,fname,file_size,cid,ctime,file_type,is_pic,random_no)
                    values('%s','%s',%s,%s,now(),%s,%s,'%s');
              """%(title,fname,myFile.size,usr_id_gy,file_type,is_pic,random_no)
        #print sql
        db.executesql(sql)

        if is_pic == 1: 
            try:
                img = Image.open(os.path.join(path,fname))
                x,y = img.size
                if x>500:
                    x1 = 500
                    y1 = 500*y/x
                else:
                    x1 = x
                    y1 = y
                img = img.resize((x1, y1), Image.ANTIALIAS)
                path = os.path.join(path,'thumbnail')
                make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
                img.save(os.path.join(path,fname))
                pic_url = os.path.join(front_url1,str(usr_id_gy),'thumbnail',fname)
            except:
                pic_url=""
        else: 
            pic_url=""
        url = os.path.join(front_url1,str(usr_id_gy),fname)

        s = """{"files":[{        
            "error":false,             
            "size":%s,
            "name":"%s",
            "thumbnail_url":"%s",
            "url":"%s",
            "delete_url":"%s/del_attach_file/?fname=%s"
            }]}
            """%(myFile.size,myFile.name,pic_url,url,data_url,fname)
        print s
        return HttpResponseJsonCORS(s)

    s = """
        {
        "error": true
        }
        """
    return HttpResponseJsonCORS(s)

#删除附件文件
def del_attach_file(request):
    func =  request.GET.get('func','')    
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    usr_id_qy = request.session.get('usr_id_qy','') or 0
    if usr_id_gy ==0 and usr_id_qy==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s) 
    fname = request.GET.get('fname','')
    sql="SELECT fname,file_type,cid FROM suppliers_pic WHERE fname='%s'"%(fname)
    print sql
    lT,iN=db.select(sql)
    if iN>0:
        L=list(lT[0])
        cid = L[2]
        if L[1] == 7:
            path=os.path.join(upload_path_mat,'%s'%(cid))
        else:
            path=os.path.join(upload_path,'%s'%(cid)) 
        if fname!='':
            path=os.path.join(path,fname)
            try:
                os.remove(path)
            except:
                pass                        
    sql="delete from suppliers_pic WHERE fname='%s'"%(fname)
    db.executesql(sql)
    s = """
        {
        "error": false
        }
        """
    return HttpResponseJsonCORS(s)

def bizlicenseOcr(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    type = request.POST.get('type') or 1

    sql = "select id,fname from suppliers_pic where cid = %s and file_type=%s"%(usr_id_gy,type)
    print sql
    rows,iN = db.select(sql)
    fname = rows[0][1]
    card_img = os.path.join(front_url,str(usr_id_gy),fname)
    sMsg = """{
"appid":"%s",
"url":"%s"
}
"""%(appid,card_img)
    url = "/ocr/bizlicense"

    print sMsg
    Sign = getSign()
    headers = {"Content-Type": "application/json","Authorization": Sign} 

    conn = httplib.HTTPSConnection('recognition.image.myqcloud.com')  
    conn.request('POST', '%s'%url,sMsg,headers)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    code = ddata.get("code")
    message = ddata.get("message")
    if code != 0:
        s = """
            {
            "errcode": %s,
            "errmsg": "%s"
            }        """%(code,message)
        return HttpResponseJsonCORS(s)
    data = ddata.get("data")
    items = data.get("items")
    for e in items:
        if ToGBK(e.get('item')) == ToGBK(u'注册号'):
            busi_code = e.get('itemstring')
        if ToGBK(e.get('item')) == ToGBK(u'法定代表人'):
            faren = e.get('itemstring')
        if ToGBK(e.get('item')) == ToGBK(u'公司名称'):
            sup_name = e.get('itemstring')
        if ToGBK(e.get('item')) == ToGBK(u'地址'):
            addr = e.get('itemstring')
        if ToGBK(e.get('item')) == ToGBK(u'主体类型'):
            sup_type = e.get('itemstring')
        if ToGBK(e.get('item')) == ToGBK(u'营业期限'):
            allotted_time = e.get('itemstring')

    s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "busi_code": "%s",
            "faren": "%s",
            "sup_name": "%s",
            "addr": "%s",
            "sup_type": "%s",
            "allotted_time": "%s"
            }        """%(code,message,busi_code,faren,sup_name,addr,sup_type,allotted_time)
    return HttpResponseJsonCORS(s)

def IDCardOCR(request):
    #usr_id,session_key,errorMsg=checkSession(request)
    #if usr_id==0:
    #    return HttpResponseJsonCORS(errorMsg)
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    type = request.POST.get('type') or request.GET.get('type') 
    if str(type) == '4':
        card_type = 0
    elif str(type) == '5':
        card_type = 1

    sql = "select id,fname from suppliers_pic where cid = %s and file_type=%s"%(usr_id_gy,type)
    print sql
    rows,iN = db.select(sql)
    fname = rows[0][1]
    card_img = os.path.join(front_url,str(usr_id_gy),fname)

    sMsg = """{
"appid":%s,
"bucket":"%s",
"card_type":%s,
"url_list":[
"%s"
] 
}
    """%(appid,bucket,card_type,card_img)
    url = "/ocr/idcard"
    print sMsg
    Sign = getSign()
    headers = {"Content-Type": "application/json","Authorization": Sign} 

    conn = httplib.HTTPSConnection('recognition.image.myqcloud.com')  
    conn.request('POST', '%s'%url,sMsg,headers)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    return handleInfo(body,card_type)

def handleInfo(body,type):
    if type == 0:
        ddata=json.loads(body)
        result_list = ddata.get('result_list')
        result = result_list[0]
        code = result.get("code")
        message = result.get("message")
        if code != 0:
            s = """
            {
            "errcode": %s,
            "errmsg": "%s"
            }        """%(code,message)
            return HttpResponseJsonCORS(s)
        data = result.get("data")
        name = data.get("name")
        sex = data.get("sex")
        nation = data.get("nation")
        birth = data.get("birth")
        address = data.get("address")
        id = data.get("id")
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "name": "%s",
            "sex": "%s",
            "nation": "%s",
            "birth": "%s",
            "address": "%s",
            "id": "%s"
            }        """%(code,message,name,sex,nation,birth,address,id)
        return HttpResponseJsonCORS(s)
    elif type == 1:
        ddata=json.loads(body)
        result_list = ddata.get('result_list')
        result = result_list[0]
        code = result.get("code")
        message = result.get("message")
        if code != 0:
            s = """
            {
            "errcode": %s,
            "errmsg": "%s"
            }        """%(code,message)
            return HttpResponseJsonCORS(s)
        data = result.get("data")
        authority = data.get("authority")
        valid_date = data.get("valid_date")
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "authority": "%s",
            "valid_date": "%s"
            }        """%(code,message,authority,valid_date)
        return HttpResponseJsonCORS(s)

def getSign():
    sql = "select sign,expired from tencent_yun_sign where id =1"
    rows,iN = db.select(sql)
    if iN == 0:
        Sign,expired,current = generateSign()
        sql = "insert into tencent_yun_sign (id,sign,expired,current) values (1,'%s',%s,%s)"%(Sign,expired,current)
        db.executesql(sql)
    else:
        current = int(time.time())
        expired = rows[0][1]
        Sign = rows[0][0]
        if expired < current + 1000:
            Sign,expired,current = generateSign()
            sql = "update tencent_yun_sign set sign='%s',expired=%s,current=%s where id=1"%(Sign,expired,current)
            db.executesql(sql)
    return Sign

def generateSign():
    expired = int(time.time()) + 2592000;
    current = int(time.time())
    rdm = random.randint(100000,999999)
    srcStr = 'a=%s&b=%s&k=%s&e=%s&t=%s&r=%s'%(appid,bucket,secret_id,expired,current,rdm)

    SignTmp = hmac.new(secret_key,srcStr,hashlib.sha1).digest()
    Sign = base64.b64encode(SignTmp+srcStr)
    return Sign,expired,current

def getSupInfo(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    print request.POST
    id = request.POST.get('id','')
    audit_btn = 0
    if id !='':
        step = '2'
        usr_id_qy = request.session.get('usr_id_qy','') or testid
        print "usr_id_qy=%s"%usr_id_qy
        users = getAuditUserIds()
        if str(usr_id_qy) in users :     
            audit_btn = 1   #审核人员
    else:
        step = request.POST.get('step','2')
        sql = "select usr_id from users_gy where usr_id = %s and status=1"%usr_id_gy 
        print sql
        rows,iN=db.select(sql)
        if iN>0:
            s = """
            {
            "errcode": 10001,
            "errmsg": "用户已绑定供应商，无法进行供应商报名"
            }        """
            return HttpResponseJsonCORS(s)
        sql = "select status from suppliers_sign_up where cid = %s"%usr_id_gy
        rows,iN=db.select(sql)
        if iN >0 and str(step)=='1':
            if rows[0][0] ==1:
                s = """
                {
                "errcode": 10002,
                "errmsg": "用户提交供应商报名"
                }        """
                return HttpResponseJsonCORS(s)
            elif rows[0][0] == 2:
                s = """
                {
                "errcode": 10003,
                "errmsg": "供应商报名已通过"
                }        """
                return HttpResponseJsonCORS(s)
            #elif rows[0][0] == -1:
            #    s = """
            #    {
            #    "errcode": 10004,
            #    "errmsg": "供应商报名未通过"
            #    }        """
            #    return HttpResponseJsonCORS(s)

    if str(step) == '1':
        sql = "select id,busi_code,faren,sup_name,addr,sup_type,allotted_time,status,audit_memo,'' from suppliers_sign_up where cid = %s"%usr_id_gy
        rows,iN=db.select(sql)
        L=[]
        if iN>0:
            L = list(rows[0])
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=1"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[9] = os.path.join(front_url,str(usr_id_gy),fname1)            

        names = 'id busi_code faren sup_name addr sup_type allotted_time status audit_memo busi_pic'.split()
        data = [dict(zip(names, L))]
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
        s = """
            {
            "errcode": 0,
            "errmsg": "获取供应商报名信息成功",
            "data": %s
            }        """%(L)
        return HttpResponseJsonCORS(s)
    elif str(step) == '4':
        sql = """select lxr_name,lxr_phone,lxr_idcard,lxr_email,'','',''
               from suppliers_sign_up"""
        sql += " where cid = %s"%usr_id_gy
        print sql
        rows,iN=db.select(sql)
        L=[]
        if iN>0:
            L = list(rows[0])
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=4"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[4] = os.path.join(front_url,str(usr_id_gy),fname1)              
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=5"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[5] = os.path.join(front_url,str(usr_id_gy),fname1)            
            sql="SELECT ifnull(fname,''),'','',file_size,ctime,is_pic,title,cid FROM suppliers_pic WHERE cid = %s and file_type=6"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            L2 = []
            for e in lT1:
                L1=list(e)
                fname = e[0]
                cid = e[7]
                L1[0] = os.path.join(front_url,str(cid),fname)
                L1[1] = os.path.join(front_url,str(cid),'thumbnail',fname)
                L1[2] = "%s/del_attach_file/?fname=%s"%(data_url,fname)
                L2.append(L1)
            names = "url thumbnail delete_url file_size ctime is_pic title".split()
            L[6] = [dict(zip(names, d)) for d in L2]

        names = 'lxr_name lxr_phone lxr_idcard lxr_email idcard_pic idcard_pic1 attach'.split()        
        data = [dict(zip(names, L))]
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
        s = """
            {
            "errcode": 0,
            "errmsg": "获取供应商联系人信息成功",
            "data": %s
            }        """%(L)
        return HttpResponseJsonCORS(s)       
    else:
        sql = """select id,busi_code,faren,sup_name,addr,sup_type,allotted_time,'','',''
               ,ifnull(gy_phone,'')
               ,ifnull(manage_area,''),tax_type,ifnull(work_address,''),province,city
               ,ifnull(place,''),ifnull(gy_name,''),ifnull(memo,''),is_merge,ifnull(status,0) 
               ,ifnull(sw_address,''),ifnull(sw_bank_name,''),ifnull(sw_bank_no,''),ifnull(sw_no,''),ifnull(sw_phone,''),ifnull(zzjg_no,'')
               ,ifnull(commpany_memo,''),ifnull(remark,''),lxr_name,lxr_phone,lxr_idcard,lxr_email
               ,'','','',cid
               from suppliers_sign_up"""
        if id != '':
           sql += " where id = %s"%id
        else:
           sql += " where cid = %s"%usr_id_gy
        print sql
        rows,iN=db.select(sql)
        L=[]
        if iN>0:
            L = list(rows[0])
            usr_id_gy = L[-1]
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=1"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[7] = os.path.join(front_url,str(usr_id_gy),fname1)              
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=3"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[8] = os.path.join(front_url,str(usr_id_gy),fname1)            
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=2"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[9] = os.path.join(front_url,str(usr_id_gy),fname1)            
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=4"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[-4] = os.path.join(front_url,str(usr_id_gy),fname1)            
            sql="SELECT ifnull(fname,'') FROM suppliers_pic WHERE cid = %s and file_type=5"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            if iN1>0:
                L1=list(lT1[0])
                fname1=L1[0]
                L[-3] = os.path.join(front_url,str(usr_id_gy),fname1)            
            sql="SELECT ifnull(fname,''),'','',file_size,ctime,is_pic,title,cid  FROM suppliers_pic WHERE cid = %s and file_type=6"%(usr_id_gy)
            lT1,iN1=db.select(sql)
            L2 = []
            for e in lT1:
                L1=list(e)
                fname = e[0]
                cid = e[7]
                L1[0] = os.path.join(front_url,str(cid),fname)
                L1[1] = os.path.join(front_url,str(cid),'thumbnail',fname)
                L1[2] = "%s/del_attach_file/?fname=%s"%(data_url,fname)
                L2.append(L1)
            names = "url thumbnail delete_url file_size ctime is_pic title".split()
            L[-2] = [dict(zip(names, d)) for d in L2]
            L[-1] = audit_btn
        names = 'id busi_code faren sup_name addr sup_type allotted_time busi_pic tax_pic org_pic gy_phone manage_area tax_type work_address province city place gy_name memo is_merge status sw_address sw_bank_name sw_bank_no sw_no sw_phone zzjg_no commpany_memo remark lxr_name lxr_phone lxr_idcard lxr_email idcard_pic idcard_pic1 attach audit_btn'.split()
        data = [dict(zip(names, L))]
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
        s = """
            {
            "errcode": 0,
            "errmsg": "获取供应商报名信息成功",
            "data": %s
            }        """%(L)
        return HttpResponseJsonCORS(s)

def saveSupName(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    step = request.POST.get('step','1')
    print request.POST
    if str(step) == '1':
        sup_name = request.POST.get('sup_name','')
        sup_name = MySQLdb.escape_string(sup_name)
        sup_name = sup_name.strip()

        sql="""select id from suppliers_sign_up where sup_name = '%s' and cid != %s
               union 
               select id from suppliers where cname = '%s' and status=1"""%(sup_name,usr_id_gy,sup_name)
        #print ToGBK(sql)
        rows,iN=db.select(sql)
        if iN>0:
            s = """
               {
               "errcode": -1,
               "errmsg": "供应商名称重复"
               }        """
            return HttpResponseJsonCORS(s)

        busi_code = request.POST.get('busi_code','')
        faren = request.POST.get('faren','')
        addr = request.POST.get('addr','')
        sup_type = request.POST.get('sup_type','')
        allotted_time = request.POST.get('allotted_time','')

        sql="""select id from suppliers_sign_up where cid = %s"""%(usr_id_gy)
        rows,iN=db.select(sql)
        if iN>0:
            sql = """update suppliers_sign_up set busi_code='%s',faren='%s',sup_name='%s',addr='%s',sup_type='%s',allotted_time='%s' where cid= %s
              """%(busi_code,faren,sup_name,addr,sup_type,allotted_time,usr_id_gy) 
        else:
            sql = """insert into suppliers_sign_up (busi_code,faren,sup_name,addr,sup_type,allotted_time,cid,ctime)
                 values ('%s','%s','%s','%s','%s','%s','%s',now())
              """%(busi_code,faren,sup_name,addr,sup_type,allotted_time,usr_id_gy)      
        db.executesql(sql)
    elif  str(step) == '2':
        addr = request.POST.get('addr','')
        gy_phone = request.POST.get('gy_phone','')
        gy_name = request.POST.get('gy_name','')
        manage_area = request.POST.get('manage_area','')
        place = request.POST.get('place[cont]','')
        province = request.POST.get('place[province_value]','')
        city = request.POST.get('place[city_value]','')
        tax_type = request.POST.get('tax_type','')
        work_address = request.POST.get('work_address','')
        memo = request.POST.get('memo','')
        is_merge = request.POST.get('is_merge','')
        
        sql = """update suppliers_sign_up set addr='%s',gy_name='%s',gy_phone='%s',manage_area='%s',province='%s'
                 ,city='%s',place='%s',tax_type=%s,work_address='%s',memo='%s',is_merge=%s,utime=now() where cid= %s
              """%(addr,gy_name,gy_phone,manage_area,province,city,place,tax_type,work_address,memo,is_merge,usr_id_gy)
        print ToGBK(sql)
        db.executesql(sql)
        errcode = mWxPushMsg_Sign_up(request,usr_id_gy)
        if errcode == 0:
            sql = """update suppliers_sign_up set status = 1 where cid= %s
              """%(usr_id_gy)
            #print sql  
            db.executesql(sql)
    elif  str(step) == '3':
        sw_address = request.POST.get('sw_address','')
        sw_bank_name = request.POST.get('sw_bank_name','')
        sw_bank_no = request.POST.get('sw_bank_no','')
        sw_no = request.POST.get('sw_no','')
        sw_phone = request.POST.get('sw_phone','')
        zzjg_no = request.POST.get('zzjg_no','')
        commpany_memo = request.POST.get('commpany_memo','')
        remark = request.POST.get('remark','')

        sql = """update suppliers_sign_up set sw_address='%s',sw_bank_name='%s',sw_bank_no='%s',sw_no='%s',sw_phone='%s'
                 ,zzjg_no='%s',commpany_memo='%s',remark='%s',join_time=now() where cid= %s
              """%(sw_address,sw_bank_name,sw_bank_no,sw_no,sw_phone,zzjg_no,commpany_memo,remark,usr_id_gy)
        print ToGBK(sql)
        db.executesql(sql)
    elif  str(step) == '4':
        valid_date = request.POST.get('valid_date','')
        name = request.POST.get('name','')
        authority = request.POST.get('authority','')
        sex = request.POST.get('sex','')
        phone = request.POST.get('phone','')
        birth = request.POST.get('birth','')
        address = request.POST.get('address','')
        id = request.POST.get('id','')
        nation = request.POST.get('nation','')
        email = request.POST.get('email','')
        sql = """select a.id from addr_book a
                 left join addr_book_group g on a.id = g.addr_book_id
                 left join users_gy u on u.addr_id = a.id
                  where g.addr_group_id = 2 and a.license = '%s' and u.status = 1 """%(id)
        lT1,iN1=db.select(sql)
        if iN1>0:
            s = """
                {
                "errcode": -1,
                "errmsg": "该身份证已绑定其他供应商，添加失败"
                }        """
            return HttpResponseJsonCORS(s)

        if birth == '':
            sql = """update suppliers_sign_up set lxr_name='%s',lxr_phone='%s'
                 ,lxr_idcard='%s',lxr_email='%s' where cid= %s
              """%(name,phone,id,email,usr_id_gy)
        else:
            sql = """update suppliers_sign_up set lxr_valid_date='%s',lxr_name='%s',lxr_authority='%s',lxr_sex='%s',lxr_phone='%s'
                 ,lxr_birth='%s',lxr_address='%s',lxr_idcard='%s',lxr_nation='%s',lxr_email='%s' where cid= %s
              """%(valid_date,name,authority,sex,phone,birth,address,id,nation,email,usr_id_gy)
        print ToGBK(sql)
        db.executesql(sql)
        sup_join(usr_id_gy)
        errcode = mWxPushMsg_Join(request,usr_id_gy)
        if errcode == 0:
            sql = """update suppliers_sign_up set status = 3 where cid= %s
              """%(usr_id_gy)
            #print sql  
            db.executesql(sql)
        s = """
        {
        "errcode": 0,
        "errmsg": "恭喜您报名成功！"
        }        """
        # s=ToGBK(s)

        return HttpResponseJsonCORS(s)

    s = """
        {
        "errcode": 0,
        "errmsg": "保存成功"
        }        """
    # s=ToGBK(s)

    return HttpResponseJsonCORS(s)

def sup_join(usr_id_gy):
    #sql = "select name from sys.columns where object_id=object_id('suppliers')"
    #rows,iN = byerp.select(sql)
    sql = """select sup_name,addr,busi_code,allotted_time,sw_no 
             ,faren,lxr_name,lxr_phone,remark
             ,manage_area,sw_bank_name,sw_bank_no,province,city
             ,tax_type+1,sw_address,sw_phone,zzjg_no,commpany_memo
             ,lxr_idcard,lxr_email,case lxr_sex when '男' then 1 else 0 end,lxr_birth
             from suppliers_sign_up where cid = %s"""%(usr_id_gy)
    rows,iN=db.select(sql)
    sup_name = rows[0][0]
    idcard = rows[0][19]
    sql = "select id from suppliers where cname='%s'"%(sup_name)
    rows1,iN = byerp.select(sql)  
    if iN>0:
        id = rows1[0][0]
    else:
        sql = "select max(code) from suppliers"
        rows2,iN = byerp.select(sql)  
        code1 = rows2[0][0][2:]
        code = 'SP' + str(int(code1) + 1)
        sql = "insert into suppliers (code,cname,jg_lb,cid,ctime) values ('%s','%s',2,1,getdate())"%(code,sup_name) 
        byerp.executesql(sql)
        sql = "select id from suppliers where cname='%s'"%(sup_name)
        rows2,iN = byerp.select(sql)  
        id = rows2[0][0]
    
    sql = """update suppliers set [addr]='%s',[busi_code]='%s',[busi_valid_date]='%s',[tax_code]='%s',[is_busi]=1
                                ,[faren]='%s',[gysct]='%s',[tel]='%s',[status]=1,[memo]='%s'
                                ,[busi_scope]='%s',[khbank]='%s',bank_info='%s',province='%s',city='%s'
                                ,[nsrsf]=%s,[swdjdz]='%s',[swdjdh]='%s',[jgdmzbh]='%s',[jg_memo]='%s'
                                ,utime = getdate()
                            where id='%s'
          """%(rows[0][1],rows[0][2],rows[0][3],rows[0][4]
              ,rows[0][5],rows[0][6],rows[0][7],rows[0][8]
              ,rows[0][9],rows[0][10],rows[0][11],rows[0][12],rows[0][13]
              ,rows[0][14],rows[0][15],rows[0][16],rows[0][17],rows[0][18]
              ,id)
    print ToGBK(sql)
    byerp.executesql(sql)

    sql = "select id from addr_book where license='%s'"%(idcard)
    rows1,iN = byerp.select(sql)  
    if iN>0:
        ab_id = rows1[0][0]
        sql = "select id from addr_book_group where addr_book_id=%s and addr_group_id = 2 "%(ab_id)
        rows2,iN2 = byerp.select(sql) 
        if iN2 == 0:
            sql = "insert into addr_book_group (addr_book_id,addr_group_id,ctime) values ('%s',2,getdate())"%(ab_id) 
            byerp.executesql(sql)
    else:
        sql = "insert into addr_book (license,status,cid,ctime) values ('%s',1,1,getdate())"%(idcard) 
        byerp.executesql(sql)
        sql = "select id from addr_book where license='%s'"%(idcard)
        rows2,iN = byerp.select(sql)  
        ab_id = rows2[0][0]
        sql = "insert into addr_book_group (addr_book_id,addr_group_id,ctime) values ('%s',2,getdate())"%(ab_id) 
        byerp.executesql(sql)
    sql = "update addr_book set name='%s',sex=%s,mobile='%s',email='%s',sup_id=%s,coname='%s',utime = getdate() where id = %s"%(rows[0][6],rows[0][21],rows[0][7],rows[0][20],id,sup_name,ab_id)
    #print ToGBK(sql)
    byerp.executesql(sql)

    sql = "update users_gy set status=1,addr_id='%s',usr_name='%s',phone='%s',bandtime=now() where usr_id=%s"%(ab_id,rows[0][6],rows[0][7],usr_id_gy)
    db.executesql(sql)
    sql = "update addr_book set sup_id=%s,coname='%s',name='%s',mobile='%s' where id=%s"%(id,sup_name,rows[0][6],rows[0][7],ab_id)
    db.executesql(sql)

    return
#企业号信息推送
import httplib
def mWxPushMsg_Sign_up(request,usr_id_gy):   

    L =Get_data_sign_up(request,usr_id_gy)
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
    toUser+='|lishijie|liusq'   
    sUrl='%s/complaint/login/login_qy?fid=auditApply&path=apply_gy&func_id=1000004&seq=%s'%(host_url,L[0])
    stitle = """供应商报名"""
    description = """供应商名称:%s\r\n报名时间:%s"""%(L[1],L[2])
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
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

    """%(m_sAgentId_gy,stitle,sUrl,description)
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
    
    return errcode

def mWxPushMsg_Join(request,usr_id_gy):   

    L =Get_data_sign_up(request,usr_id_gy)
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
    toUser+='|liuxy'
    toUser+='|lishijie|liusq'   
    sUrl='%s/complaint/login/login_qy?fid=auditApply&path=apply_gy&func_id=1000004&seq=%s'%(host_url,L[0])
    stitle = """供应商加入"""
    description = """供应商名称:%s\r\n加入时间:%s"""%(L[1],L[3])
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
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

    """%(m_sAgentId_gy,stitle,sUrl,description)
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
    
    return errcode

def Get_data_sign_up(request,usr_id_gy):
    sql="""SELECT id,sup_name,utime,join_time
            FROM suppliers_sign_up 
            WHERE cid = %s
            """%(usr_id_gy)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def getRecvUser():
    sql = """select GROUP_CONCAT(u.login_id) from roles r
           left join usr_role ur  on ur.role_id = r.role_id
           left join users u on ur.usr_id = u.usr_id
           where r.role_name = '供应商加入审核（供应商服务平台）'"""
    rows,iN = db.select(sql)
    users=rows[0][0]
    users = users.replace(',','|')
    return users

def getAuditUserIds():
    sql = """select u.usr_id from roles r
             left join usr_role ur  on ur.role_id = r.role_id
             left join users u on ur.usr_id = u.usr_id
             where r.role_name = '供应商加入审核（供应商服务平台）'"""
    rows,iN = db.select(sql)
    users= []
    for e in rows:
        users.append(str(e[0]))
    users.append('2938')
    users.append('2110')
    users.append('2572')
    return users
