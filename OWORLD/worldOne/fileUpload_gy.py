# -*- coding: utf-8 -*-
prj_name=__name__.split('.')[0]
import time
import os
import json
import datetime
import random
from HW_DT_TOOL                 import getToday
from HW_FILE_TOOL               import make_sub_path,readImage
import httplib
from share import db,HttpResponseCORS,ToGBK,ToUnicode,HttpResponseJsonCORS,data_url
from PIL import Image

upload_path = "/home/webroot/data/%s/attach_files/"%(prj_name)
front_url = 'http://lw.szby.cn/attach'

testid = 1
def attach_save(request):
    #print request.POST
    today = datetime.date.today()
    year = today.year
    month = today.month
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        pk =  request.POST.get('pk','')    
        random_no = request.POST.get('random_no', '')
        usr_id_gy = request.session.get('usr_id_gy','') or testid
        # file_type = request.POST.get('file_type', '')
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
        fname = "gy_%s_%s_%s.%s"%(usr_id_gy,time.time(),random.randint(0,99),f_ext)

        make_sub_path(upload_path)
        path=os.path.join(upload_path,str(year))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        path=os.path.join(path,str(month))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        destination = open(os.path.join(path,fname),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  

        import imghdr
        imgType = imghdr.what(os.path.join(path,fname))
        if imgType in['rgb','gif','pbm','pgm','ppm','tiff','rast','xbm','jpeg','bmp','png']:
            is_pic = 1
        else:is_pic=0
        if pk=='':pk='NULL'
        sql = """insert into file_pic_gy (title,fname,file_size,is_pic,random_no,cid,ctime,file_type)
                    values('%s','%s',%s,%s,'%s',%s,now(),'tstj');
              """%(title,fname,myFile.size,is_pic,random_no,usr_id_gy)
        #print sql
        db.executesql(sql)

        if is_pic == 1: 
            img = Image.open(os.path.join(path,fname))
            x,y = img.size
            if x>80:
                x1 = 80
                y1 = 80*y/x
            else:
                x1 = x
                y1 = y
            img = img.resize((x1, y1), Image.ANTIALIAS)
            path = os.path.join(path,'thumbnail')
            make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
            img.save(os.path.join(path,fname))
            pic_url = os.path.join(front_url,str(year),str(month),'thumbnail',fname)
        else: 
            pic_url=""
        url = os.path.join(front_url,str(year),str(month),fname)

        s = """{"files":[{        
            "error":false,             
            "size":%s,
            "name":"%s",
            "thumbnail_url":"%s",
            "url":"%s/fileUpload_gy/file_down?fname=%s",
            "delete_url":"%s/fileUpload_gy/del_attach_file?fname=%s"
            }]}
            """%(myFile.size,myFile.name,pic_url,data_url,fname,data_url,fname)
        return HttpResponseJsonCORS(s)

    s = """
        {
        "error": true
        }
        """
    return HttpResponseJsonCORS(s)

def attach_save_qy(request):
    #print request.POST
    today = datetime.date.today()
    year = today.year
    month = today.month
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        pk =  request.POST.get('pk','')    
        random_no = request.POST.get('random_no', '')
        usr_id_qy = request.session.get('usr_id_qy','') or testid
        file_type=''
        btntype=request.POST.get('btnType', '') or 'NULL'
        # print request.POST
        if str(btntype)=='0':
            file_type='jb'
        if str(btntype)=='-1':
            file_type='sbld'
        if str(btntype)=='1':
            file_type='tjsl'
        if str(btntype)=='2':
            file_type='jgsb'
        if str(btntype)=='3':
            file_type='jgqr'
        if str(btntype)=='4':
            file_type='jsz'
        if usr_id_qy ==0:
            s = """
            {
            "errcode": -1,
            "errmsg": "无权访问,请先关注"
            }        """
            return HttpResponseJsonCORS(s)
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
        # print myFile
        if not myFile:  
            s = """
                {
                "error": true
                }
                """
            return HttpResponseJsonCORS(s)
        title = myFile.name
        f_ext=title.split('.')[-1]
        fname = "qy_gy_%s_%s_%s.%s"%(usr_id_qy,time.time(),random.randint(0,99),f_ext)

        make_sub_path(upload_path)
        path=os.path.join(upload_path,str(year))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        path=os.path.join(path,str(month))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        destination = open(os.path.join(path,fname),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  

        import imghdr
        imgType = imghdr.what(os.path.join(path,fname))
        if imgType in['rgb','gif','pbm','pgm','ppm','tiff','rast','xbm','jpeg','bmp','png']:
            is_pic = 1
        else:is_pic=0

        if pk=='':pk='NULL'
        sql = """insert into file_pic_gy (m_id,title,fname,file_size,is_pic,random_no,cid,ctime,file_type,file_type_id)
                    values(%s,'%s','%s',%s,%s,'%s',%s,now(),'%s',%s);
              """%(pk,title,fname,myFile.size,is_pic,random_no,usr_id_qy,file_type,btntype)
        # print sql
        db.executesql(sql)

        if is_pic == 1: 
            img = Image.open(os.path.join(path,fname))
            x,y = img.size
            if x>80:
                x1 = 80
                y1 = 80*y/x
            else:
                x1 = x
                y1 = y
            img = img.resize((x1, y1), Image.ANTIALIAS)
            path = os.path.join(path,'thumbnail')
            make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
            img.save(os.path.join(path,fname))
            pic_url = os.path.join(front_url,str(year),str(month),'thumbnail',fname)
        else: 
            pic_url=""
        url = os.path.join(front_url,str(year),str(month),fname)

        s = """{"files":[{        
            "error":false,             
            "size":%s,
            "name":"%s",
            "thumbnail_url":"%s",
            "url":"%s/fileUpload_gy/file_down?fname=%s",
            "delete_url":"%s/fileUpload_gy/del_attach_file?fname=%s"
            }]}
            """%(myFile.size,myFile.name,pic_url,data_url,fname,data_url,fname)
        return HttpResponseJsonCORS(s)

    s = """
        {
        "error": true
        }
        """
    return HttpResponseJsonCORS(s) 
 
#删除附件文件
def del_attach_file(request):
    usr_id_gy = request.session.get('usr_id_gy','') or testid
    if usr_id_gy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s) 
    fname = request.GET.get('fname','')
    sql="SELECT fname,YEAR(ctime),MONTH(ctime) FROM file_pic_gy WHERE fname='%s' and cid = %s"%(fname,usr_id_gy)
    lT,iN=db.select(sql)
    if iN>0:
        L=list(lT[0])
        ext=L[0].split('.')[-1]
        year=L[1]
        month=L[2]
    path=os.path.join(upload_path,'%s/%s'%(year,month))
    if fname!='':
        path=os.path.join(path,fname)
        try:
            os.remove(path)
        except:
            pass                        
    sql="delete from file_pic_gy WHERE fname='%s' and cid=%s"%(fname,usr_id)
    db.executesql(sql)
    s = """
        {
        "error": false
        }
        """
    return HttpResponseJsonCORS(s)

def file_down(request):
    fname = request.GET.get('fname','')
    
    sql="SELECT fname,YEAR(ctime),MONTH(ctime),ifnull(title,'') FROM file_pic_gy WHERE fname='%s'"%fname
    lT,iN=db.select(sql)
    if len(lT)==0:return '找不到文件'
    L=lT[0]
    fname=L[0]
    year=L[1]
    month=L[2]
    title=L[3]
    path=os.path.join(upload_path,str(year),str(month),fname)
        
    showMode=0
    if fname.split('.')[-1].upper() not in ('JPG','GIF','PNG','BMP'):
        showMode = 1
    return readImage(path,showMode,title)