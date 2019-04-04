# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import md5
import json
import time
import datetime
import random
import os
import base64
import httplib
import urllib 
import hmac
import hashlib
from HW_DT_TOOL                 import getToday
from HW_FILE_TOOL               import make_sub_path,readImage
import httplib
exec ('from %s.share import db,dActiveUser,mValidateUser,get_dept_data,HttpResponseCORS,m_prjname,ToGBK,front_url,ComplexEncoder'%prj_name) 

upload_path = "/home/webroot/data/%s/labor/"%(m_prjname)
def saveLaborInfo(request):
    usr_id = request.session.get('usr_id', 2)
    usr_name = request.session.get('usr_name', '')
    step = request.POST.get("step",1)
    today = datetime.date.today()
    year = today.year
    
    if str(step) == '1':      
        username = request.POST.get("username",'')
        idCardFaceImg = request.POST.get("idCardFaceImg",'')
        birthDate = request.POST.get("birthDate",'')
        nation = request.POST.get("nation",'')
        idNo = request.POST.get("idNo",'')
        place = request.POST.get("place",'')
        validateDate = request.POST.get("validateDate",'')
        sex = request.POST.get("sex",'')
        issuer = request.POST.get("issuer",'')
        if idCardFaceImg != '':
            pic_ext = idCardFaceImg.split(';')[0]
            pic_ext = pic_ext.split('/')[-1]
            pic_data = idCardFaceImg.split(';')[1] 
            pic_data = pic_data.split(',')[-1]
            filename = "head.%s"%(pic_ext)
        else:
            filename = ''
        if idNo == '':
            s = """
        {
        "errcode": -1,
        "errmsg": "参数错误"
        }
        """
            return HttpResponseCORS(request,s)
        sql = "select id,pic_path,year from labor_info where idcard_no = '%s'"%(idNo)
        rows,iN = db.select(sql)       
        if iN == 0:
            pic_path = "%s_%s"%(int(time.time()),random.randint(0,99))
            head_pic = "labor/%s/%s/%s"%(year,pic_path,filename)
            sql = """insert into labor_info (cname,gender,nation,birth,address,idcard_no,authority,valid_date,pic_path,year,ctime,cid)
                     values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now(),%s)
                  """%(username,sex,nation,birthDate,place,idNo,issuer,validateDate,pic_path,year,usr_id)
            print ToGBK(sql)
            db.executesql(sql)
            sql = "select last_insert_id();"
            rows,iN = db.select(sql)
            labor_id = rows[0][0]
        else:
            labor_id = rows[0][0]
            pic_path = rows[0][1]
            year = rows[0][2]
            head_pic = "labor/%s/%s/%s"%(year,pic_path,filename)
            sql = """update labor_info set cname='%s',gender='%s',nation='%s',birth='%s',address='%s',authority='%s',valid_date='%s'
                     where id = %s
                  """%(username,sex,nation,birthDate,place,issuer,validateDate,labor_id)
            print ToGBK(sql)
            db.executesql(sql)

        if idCardFaceImg != '':
            sql = """update labor_info set head_pic='%s'
                     where id = %s
                  """%(head_pic,labor_id)
            print ToGBK(sql)
            db.executesql(sql)
            savePic(pic_data,pic_path,year,filename)
    elif str(step) == '2':  
        #print request.POST
        labor_id = request.POST.get("labor_id",'')
        idCardImg = request.POST.get("idCardImg",'')
        if idCardImg != '':
            pic_ext = idCardImg.split(';')[0]
            pic_ext = pic_ext.split('/')[-1]
            pic_data = idCardImg.split(';')[1] 
            pic_data = pic_data.split(',')[-1]
            filename = "idCard.%s"%(pic_ext)
            sql = "select id,pic_path,year from labor_info where id = '%s'"%(labor_id)
            print sql
            rows,iN = db.select(sql)       
            pic_path = rows[0][1]
            year = rows[0][2]
            idcard_pic = "labor/%s/%s/%s"%(year,pic_path,filename)
            sql = """update labor_info set idcard_pic='%s'
                     where id = %s
                  """%(idcard_pic,labor_id)
            db.executesql(sql)
            savePic(pic_data,pic_path,year,filename)
        idCardImg1 = request.POST.get("idCardImg1",'')
        if idCardImg1 != '':
            pic_ext = idCardImg1.split(';')[0]
            pic_ext = pic_ext.split('/')[-1]
            pic_data = idCardImg1.split(';')[1] 
            pic_data = pic_data.split(',')[-1]
            filename = "idCard1.%s"%(pic_ext)
            sql = "select id,pic_path,year from labor_info where id = '%s'"%(labor_id)
            rows,iN = db.select(sql)       
            pic_path = rows[0][1]
            year = rows[0][2]
            idcard_pic1 = "labor/%s/%s/%s"%(year,pic_path,filename)
            sql = """update labor_info set idcard_pic1='%s'
                     where id = %s
                  """%(idcard_pic1,labor_id)
            db.executesql(sql)
            savePic(pic_data,pic_path,year,filename)

    elif str(step) == '3':  
        labor_id = request.POST.get("labor_id",'')
        proj_id = request.POST.get("proj_id") or 0
        bank_name = request.POST.get("bank_name",'')
        bank_username = request.POST.get("bank_username",'')
        bankNo = request.POST.get("bankNo",'')

        sql = """update labor_info set bank_name='%s',account_name='%s',account_no='%s' 
                     where id = %s
                  """%(bank_name,bank_username,bankNo,labor_id)
        db.executesql(sql)

        sql = "select bankCard_pic from labor_info where id = '%s'"%(labor_id)
        rows,iN = db.select(sql)  
        bankCard_pic = rows[0][0]
        sql = """update labor_bank_info set bank_name='%s',account_name='%s',account_no='%s',proj_id=%s,cid=%s
                     where labor_id = %s and bankCard_pic='%s'
                  """%(bank_name,bank_username,bankNo,proj_id,usr_id,labor_id,bankCard_pic)
        print sql
        db.executesql(sql)
        
        sql = "select id from labor_proj where labor_id=%s and proj_id=%s"%(labor_id,proj_id)
        rows,iN = db.select(sql)  
        if iN == 0:
            sql = """insert labor_proj (labor_id,proj_id,bank_name,account_name,account_no,bankCard_pic,ctime,cid)
                     values (%s,%s,'%s','%s','%s','%s',now(),'%s')
                  """%(labor_id,proj_id,bank_name,bank_username,bankNo,bankCard_pic,usr_id)
        else:
            sql = """update labor_proj set bank_name='%s',account_name='%s',account_no='%s',bankCard_pic='%s'
                     where id = %s
                  """%(bank_name,bank_username,bankNo,bankCard_pic,rows[0][0])
        db.executesql(sql)
    elif str(step) == '4':  
        labor_id = request.POST.get("labor_id",'')
        pictureImg = request.POST.get("pictureImg",'')
        proj_id = request.POST.get("proj_id",'')
        if pictureImg != '':
            pic_ext = pictureImg.split(';')[0]
            pic_ext = pic_ext.split('/')[-1]
            pic_data = pictureImg.split(';')[1] 
            pic_data = pic_data.split(',')[-1]
            filename = "scene_pic_%s.%s"%(proj_id,pic_ext)
            sql = "select id,pic_path,year from labor_info where id = '%s'"%(labor_id)
            rows,iN = db.select(sql)       
            pic_path = rows[0][1]
            year = rows[0][2]
            scene_pic = "labor/%s/%s/%s"%(year,pic_path,filename)
            sql = """update labor_info set scene_pic='%s'
                     where id = %s
                  """%(scene_pic,labor_id)
            db.executesql(sql)
            savePic(pic_data,pic_path,year,filename)
            sql = """update labor_proj set scene_pic='%s',utime=now()
                     where labor_id=%s and proj_id=%s
                  """%(scene_pic,labor_id,proj_id)
            db.executesql(sql)
    elif str(step) == '5':  
        labor_id = request.POST.get("labor_id",'')
        proj_id = request.POST.get("proj_id",'')
        h_press = request.POST.get("h_press") or 'NULL'
        l_press = request.POST.get("l_press") or 'NULL'
        temperature = request.POST.get("temperature") or 'NULL'
        heartRate = request.POST.get("heartRate") or 'NULL'
        sql = """update labor_proj set h_press=%s,l_press=%s,temperature=%s,heartRate=%s,utime=now()
                     where labor_id=%s and proj_id=%s
                  """%(h_press,l_press,temperature,heartRate,labor_id,proj_id)
        print sql
        db.executesql(sql)

    elif str(step) == '6':  
        print request.POST
        labor_id = request.POST.get("labor_id",'')
        proj_id = request.POST.get("proj_id",'')
        phone = request.POST.get("phone",'')
        workerSelect = request.POST.get("work",'')
        groupSelect = request.POST.get("group",'')
        sql = """update labor_proj set job='%s',team_id='%s',mobile='%s',status=1,utime=now()
                     where labor_id=%s and proj_id=%s
                  """%(workerSelect,groupSelect,phone,labor_id,proj_id)
        print sql
        db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "保存成功",
        "labor_id":%s
        } 
        """%(labor_id)
    return HttpResponseCORS(request,s)

def savePic(pic_data,pic_path,year,filename):
    path=os.path.join(upload_path,str(year))
    make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
    path=os.path.join(path,str(pic_path))
    make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path

    file_path=os.path.join(path,filename)
    data= base64.b64decode(pic_data)
    f=open(file_path,'wb')
    f.write(data)
    f.flush()
    f.close()
    return

def getLaborInfo(request):
    usr_id = request.session.get('usr_id', 2)
    usr_name = request.session.get('usr_name', '')
    labor_id = request.POST.get("labor_id",0)
    proj_id = request.POST.get("proj_id",0)
    idNo = request.POST.get("idNo",'')

    sql = """SELECT
    li.cname,li.gender,li.nation,li.birth,li.address,li.idcard_no,li.authority,li.valid_date,ifnull(li.head_pic, ''),
    ifnull(li.idcard_pic, ''),
    ifnull(li.idcard_pic1, ''),
	ifnull(lp.bank_name, li.bank_name),
	ifnull(
		lp.account_name,
		li.account_name
	),
	ifnull(
		lp.account_no,
		li.account_no
	),
	ifnull(
		lp.bankCard_pic,
		li.bankCard_pic
	),
	ifnull(lp.scene_pic, ''),
	ifnull(lp.job,0),
	ifnull(lp.team_id,0),
	lp.mobile,
	lp.status,
	lp.h_press,
	lp.l_press,
	lp.temperature,
	lp.heartRate,
	li.id
FROM
	labor_info li
LEFT JOIN labor_proj lp ON lp.labor_id = li.id
AND lp.proj_id = '%s'
WHERE
	li.idcard_no = '%s'"""%(proj_id,idNo)
    print sql
    rows,iN = db.select(sql)     
    if iN == 0:
        L = ['']*25
        job_id = 0
        team_id = 0
    else:
        L = list(rows[0])
        job_id = rows[0][16]
        team_id = rows[0][17]
    sql = "select id,name,id=%s from addr_book where id in (select addr_book_id from addr_book_group where addr_group_id=6)"%(team_id)
    rows,iN = db.select(sql)      
    names = 'id name selected'.split()
    data1 = [dict(zip(names, d)) for d in rows]

    sql = "select id,txt1,id=%s from mtc_t where type = 'WTRADE' order by sort"%(job_id)
    rows,iN = db.select(sql)      
    names = 'id name  selected'.split()
    data2 = [dict(zip(names, d)) for d in rows]

    L[16]= data2
    L[17]= data1
    names = 'cname gender nation birth address idcard_no authority valid_date head_pic idcard_pic idcard_pic1 bank_name account_name account_no bankCard_pic scene_pic job team mobile status h_press l_press temperature heartRate labor_id'.split()
    data = dict(zip(names, L))
    s1 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "data":%s
        }
        """%(s1) 
    return HttpResponseCORS(request,s)

appid = 1256868860
bucket = "labor"
secret_id = "AKID2zkJhsixlPzOqAqHbjfO4eGk2HTZpBh1"
secret_key = "HNGxb9YnrmV3QbZadYIqDNL7h5HICuPl"

def bankCardOCR(request):
    labor_id = request.POST.get("labor_id",'')
    bankCardImg = request.POST.get("bankCardImg",'')
    if bankCardImg != '':
        pic_ext = bankCardImg.split(';')[0]
        pic_ext = pic_ext.split('/')[-1]
        pic_data = bankCardImg.split(';')[1] 
        pic_data = pic_data.split(',')[-1]
        filename = "bankCard_%s.%s"%(int(time.time()),pic_ext)
        sql = "select id,pic_path,year from labor_info where id = '%s'"%(labor_id)
        rows,iN = db.select(sql)       
        pic_path = rows[0][1]
        year = rows[0][2]
        bankCard_pic = "labor/%s/%s/%s"%(year,pic_path,filename)
        sql = """update labor_info set bankCard_pic='%s'
                 where id = %s
              """%(bankCard_pic,labor_id)
        db.executesql(sql)
        sql = """insert into labor_bank_info (labor_id,bankCard_pic,ctime) values (%s,'%s',now())
              """%(labor_id,bankCard_pic)
        db.executesql(sql)

        savePic(pic_data,pic_path,year,filename)

        card_img = os.path.join(front_url,bankCard_pic)
        sMsg = """{
"appid":"%s",
"bucket":"%s",
"url":"%s"
}
"""%(appid,bucket,card_img)
        url = "/ocr/bankcard"
        Sign = getSign()
        headers = {"Content-Type": "application/json","Authorization": Sign} 

        conn = httplib.HTTPSConnection('recognition.image.myqcloud.com')  
        conn.request('POST', '%s'%url,sMsg,headers)  

        res = conn.getresponse()       
        body = res.read()  
        conn.close()  
        print body
        ddata=json.loads(body)
        code = ddata.get("code")
        message = ddata.get("message")
        if code != 0:
            s = """
            {
            "errcode": %s,
            "errmsg": "%s"
            }        """%(code,message)
            return HttpResponseCORS(request,s)
        data = ddata.get("data")
        items = data.get("items")
        bankCard_no = ''
        bankCard_type = ''
        bankCard_name = ''
        bank_info = ''

        for e in items:
            if e.get("item") == "卡号":
                bankCard_no = e.get("itemstring")
            if e.get("item") == "卡类型":
                bankCard_type = e.get("itemstring")
            if e.get("item") == "卡名字":
                bankCard_name = e.get("itemstring")
            if e.get("item") == "银行信息":
                bank_info = e.get("itemstring")
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            "bankCard_no": "%s",
            "bankCard_type": "%s",
            "bankCard_name": "%s",
            "bank_info": "%s"
            }        """%(code,message,bankCard_no,bankCard_type,bankCard_name,bank_info)
        return HttpResponseCORS(request,s)    
    s = """
        {
        "errcode": -1,
        "errmsg": "参数错误",
        }
        """
    return HttpResponseCORS(request,s)    

def getSign():
    sql = "select sign,expired from labour_sign where id =1"
    rows,iN = db.select(sql)
    if iN == 0:
        Sign,expired,current = generateSign()
        sql = "insert into labour_sign (id,sign,expired,current) values (1,'%s',%s,%s)"%(Sign,expired,current)
        db.executesql(sql)
    else:
        current = int(time.time())
        expired = rows[0][1]
        Sign = rows[0][0]
        if expired < current + 1000:
            Sign,expired,current = generateSign()
            sql = "update labour_sign set sign='%s',expired=%s,current=%s where id=1"%(Sign,expired,current)
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

def test(request):
    name = '韩瑞明'
    gender = '男'
    deptCode = 'SG20180421002'
    mobile = '18927491149'
    idcard = '152322199201063316'
    body = upload(name,gender,deptCode,mobile,idcard)
    return HttpResponseCORS(request,body)
    
def upload(name,gender,deptCode,mobile,idcard):
    appid = 'hjzs'
    md5key = '!wn6yZh%4sBS8**C'
    timestamp = (int(time.time()))                  #秒级时间戳
    
    para = dict()   
    para["name"] = name
    para["gender"] = gender
    para["deptCode"] = deptCode
    para["mobile"] = mobile
    para["idcard"] = idcard
    para["appid"] = appid
    para["timestamp"] = str(timestamp)

    sign = makeSign(para,md5key)

    para["sign"] = sign

    para_str = ''
    for key in para: 
        para_str += '&' + key+'=' + para[key]
    #params= json.dumps(para,ensure_ascii=False)
    params = urllib.urlencode(para)
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    print params
    conn = httplib.HTTPConnection('www.winuim.com:8383')  
    url = "/CommonData/lwg"
    print url

    conn.request('POST', url, params, headers)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    print ToGBK(body)
    ddata=json.loads(body)
    errcode = ddata.get('Ret')   
    return body

def makeSign(para,md5key):
    para1 = sorted(para.items(), key=lambda para:para[0])
    src_str = ''
    #print para1
    for e in para1:
        src_str += "%s%s"%(e[0],e[1])
    src_str += md5key
    #print src_str
    m1 = md5.new()   
    m1.update(src_str)   
    sign = m1.hexdigest() 
    #print sign
    return sign