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
testid = 0
def attach_save(request):
    #print request.POST
    func =  request.POST.get('func','')    
    if func == 'Progress':
        return attach_save_progress(request)
    today = datetime.date.today()
    year = today.year
    month = today.month
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        pk =  request.POST.get('pk','')    
        random_no = request.POST.get('random_no', '')
        usr_id = request.session.get('usr_id','') or testid
        # file_type = request.POST.get('file_type', '')
        if usr_id ==0:
            s = """
            {
            "errcode": -1,
            "errmsg": "无权访问,请先关注"
            }        """
            return HttpResponseJsonCORS(s)
        # print '_____' 
        # print request.POST
        # print '_____' 
        # print request.FILES
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
        fname = "%s_%s_%s.%s"%(usr_id,time.time(),random.randint(0,99),f_ext)
        if f_ext.upper() in['GIF','JPG','PNG','BMP']:
            is_pic = 1
        else:is_pic=0
        if pk=='':pk='NULL'
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

        sql = """insert into file_pic_lw (lc_id,title,fname,file_size,is_pic,random_no,cid,ctime,file_type)
                    values(%s,'%s','%s',%s,%s,'%s',%s,now(),'tstj');
              """%(pk,title,fname,myFile.size,is_pic,random_no,usr_id)
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
            "url":"%s",
            "delete_url":"%s/fileUpload/del_attach_file?fname=%s"
            }]}
            """%(myFile.size,myFile.name,pic_url,url,data_url,fname)
        return HttpResponseJsonCORS(s)

    s = """
        {
        "error": true
        }
        """
    return HttpResponseJsonCORS(s)

def attach_save_progress(request):
    today = datetime.date.today()
    year = today.year
    month = today.month
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        random_no = request.POST.get('random_no', '')
        usr_id = request.session.get('usr_id','') or testid
        if usr_id ==0:
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
        fname = "pd_%s_%s_%s.%s"%(usr_id,time.time(),random.randint(0,99),f_ext)

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

        sql = """insert into file_pic_pp (title,fname,file_size,is_pic,random_no,cid,ctime)
                    values('%s','%s',%s,%s,'%s',%s,now());
              """%(title,fname,myFile.size,is_pic,random_no,usr_id)
        #print sql
        db.executesql(sql)
        sql = "update file_pic_pp f,progress_declare pd set f.m_id=pd.id where f.random_no=pd.random_no and f.random_no='%s'"%(random_no)
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
            "url":"%s",
            "delete_url":"%s/fileUpload/del_attach_file?fname=%s&func=Progress"
            }]}
            """%(myFile.size,myFile.name,pic_url,url,data_url,fname)
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
        fname = "qy_%s_%s_%s.%s"%(usr_id_qy,time.time(),random.randint(0,99),f_ext)
        if f_ext.upper() in['GIF','JPG','PNG','BMP']:
            is_pic = 1
        else:is_pic=0
        if pk=='':pk='NULL'
        sql = """insert into file_pic_lw (m_id,title,fname,file_size,is_pic,random_no,cid,ctime,file_type,file_type_id)
                    values(%s,'%s','%s',%s,%s,'%s',%s,now(),'%s',%s);
              """%(pk,title,fname,myFile.size,is_pic,random_no,usr_id_qy,file_type,btntype)
        # print sql
        db.executesql(sql)
        make_sub_path(upload_path)
        path=os.path.join(upload_path,str(year))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        path=os.path.join(path,str(month))
        make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
        destination = open(os.path.join(path,fname),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  
        # if is_pic == 1: pic_url = "%s/get_file/?fname=%s"%(data_url,fname)
        # else: pic_url=""
        # s = """{"files":[{        
        #     "error":false,             
        #     "size":%s,
        #     "fname":"%s"
        #     }]}
        #     """%(myFile.size,fname)

        if is_pic == 1: pic_url = "%s/fileUpload/file_down?fname=%s"%(data_url,fname)
        else: pic_url=""
        s = """{"files":[{        
            "error":false,             
            "size":%s,
            "name":"%s",
            "thumbnail_url":"%s",
            "url":"%s/fileUpload/file_down?fname=%s",
            "delete_url":"%s/fileUpload/del_attach_file?fname=%s"
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
    func =  request.GET.get('func','')    
    if func == 'Progress':
        table = 'file_pic_pp'    
    else:
        table = 'file_pic_lw'    
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s) 
    fname = request.GET.get('fname','')
    sql="SELECT fname,YEAR(ctime),MONTH(ctime) FROM %s WHERE fname='%s' and cid = %s"%(table,fname,usr_id)
    print sql
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
    sql="delete from %s WHERE fname='%s' and cid=%s"%(table,fname,usr_id)
    db.executesql(sql)
    s = """
        {
        "error": false
        }
        """
    return HttpResponseJsonCORS(s)

def file_down(request):
    fname = request.GET.get('fname','')
    
    sql="SELECT fname,YEAR(ctime),MONTH(ctime),ifnull(title,'') FROM file_pic_lw WHERE fname='%s'"%fname
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

# def file_list(request):
#     menu_id = request.POST.get('menu_id', 0)
#     pk =  request.POST.get('pk','')    
#     random_no = request.POST.get('random_no', '')
#     if pk != '':
#         sql="SELECT '',file_size,ifnull(title,''),'','','',fname,YEAR(ctime),MONTH(ctime),is_pic FROM file_pic WHERE menu_id=%s and gw_id=%s"%(menu_id,pk)
#     else:
#         sql="SELECT '',file_size,ifnull(title,''),'','','',fname,YEAR(ctime),MONTH(ctime),is_pic FROM file_pic WHERE menu_id=%s and random_no='%s'"%(menu_id,random_no)
#     #print sql    
#     lT,iN=db.select(sql)
#     if len(lT)==0:
#         s = """{"files":[]}
#             """
#         return HttpResponseJsonCORS(s)
#     L = []
#     for e in lT:
#         L1 = list(e)
#         fname = e[6]
#         L1[0] = False
#         if e[9]==1: 
#             L1[3] = "%s/get_file/?fname=%s"%(data_url,fname)
#         else: L1[3]=""
#         L1[4] = "%s/get_file/?fname=%s"%(data_url,fname)
#         L1[5] = "%s/del_file/?fname=%s"%(data_url,fname)
#         L.append(L1)
#     names = 'error size name thumbnail_url url delete_url'.split()
#     data = [dict(zip(names, d)) for d in L]
#     fileList = json.dumps(data,ensure_ascii=False)  

#     s = """{"files":%s}
#         """%(fileList)
#     #print ToGBK(s)
#     return HttpResponseJsonCORS(s)

# def alert(msg): #kindeditor
#     s = """
#         {
#         "error": 1,
#         "message": "%s",
#         }
#         """%msg  
#     return HttpResponseJsonCORS(s)

# editor_path = "/home/webroot/data/kjerp/open/editor_files/"
# def editor_attach_save(request):
#     #print request.POST
#     ext_arr = {
#             'image':('gif', 'jpg', 'jpeg', 'png', 'bmp'),
#             'flash':('swf', 'flv'),
#             'media':('swf', 'flv', 'mp3', 'wav', 'wma', 'wmv', 'mid', 'avi', 'mpg', 'asf', 'rm', 'rmvb'),
#             'file' :('doc', 'docx', 'xls', 'xlsx', 'ppt', 'htm', 'html', 'txt', 'zip', 'rar', 'gz', 'bz2','7z','pdf'),
#             }
#     today = datetime.date.today()
#     year = today.year
#     month = today.month
#     if request.method == "POST":    # 请求方法为POST时，进行处理  
#         usr_id = request.session.get('usr_id',0)
#         myFile =request.FILES.get("imgFile", None)    # 获取上传的文件，如果没有文件，则默认为None  
#         if not myFile:  
#             return alert('没有找到上传的文件！')
#         title = myFile.name
#         name_ext=title.split('.')[-1].lower() #后缀名
#         dir_name= request.GET.get('dir','').strip()  #文件目录
#         #检查目录名
#         dirName=ext_arr.get(dir_name)

#         if dir_name == '':
#             for e in ['image','flash','media','file']:
#                 v=ext_arr[e]
#                 if name_ext in v:
#                     dir_name=e
#                     dirName=ext_arr.get(dir_name)
#                     break
#             else:
#                 return alert('上传文件扩展名不正确.')
#         elif name_ext not in dirName:
#             return alert('上传文件扩展名不正确.')
        
#         fname = "%s_%s_%s.%s"%(usr_id,time.time(),random.randint(0,99),name_ext)
#         make_sub_path(editor_path)
#         path=os.path.join(editor_path,str(usr_id))
#         make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
#         path=os.path.join(path,dir_name)
#         make_sub_path(path) #检查目录是否存在，如果不存在，生成目录  make_sub_path
#         destination = open(os.path.join(path,fname),'wb+')    # 打开特定的文件进行二进制的写操作  
#         for chunk in myFile.chunks():      # 分块写入文件  
#             destination.write(chunk)  
#         destination.close()  
#         file_url='%s/%s/%s/%s/%s'%(fs_url,'editor_files',usr_id,dir_name,fname)
#         s = """{      
#             "error":0,             
#             "url":"%s",
#             }
#             """%(file_url)
#         #print s
#         return HttpResponseJsonCORS(s)


#     return alert('未知错误.')

# def file_manage_json(request): #kindeditor
#     ext_arr = {
#             'image':('gif', 'jpg', 'jpeg', 'png', 'bmp'),
#             'flash':('swf', 'flv'),
#             'media':('swf', 'flv', 'mp3', 'wav', 'wma', 'wmv', 'mid', 'avi', 'mpg', 'asf', 'rm', 'rmvb'),
#             'file' :('doc', 'docx', 'xls', 'xlsx', 'ppt', 'htm', 'html', 'txt', 'zip', 'rar', 'gz', 'bz2','pdf'),
#             }
#     usr_id = request.session.get('usr_id',0)
#     PATH=os.path.join(editor_path, str(usr_id))
#     make_sub_path(PATH)
    
#     dir_name= request.POST.get('dir','').strip()
#     goPath= request.POST.get('path','').strip() #上级目录
#     if dir_name and dir_name not in ext_arr:
#         return "Invalid Directory name.";
    
#     if goPath :
#         go=goPath.split('/')[1]
#         if goPath in ('.','/','./','','../'):
#             pass
#         elif goPath in ext_arr:
#             dir_name=goPath
#             PATH=os.path.join(PATH, goPath)
#         elif go in ext_arr:
#             dir_name=go
#             PATH=os.path.join(PATH, go)
            
#     elif dir_name:
#         PATH=os.path.join(PATH, dir_name)
#         make_sub_path(PATH)
#     #
#     file_list=[]
#     i=0
#     for e in os.listdir(PATH):
#         if e[0]=='.': continue
#         mypath=os.path.join(PATH, e)
#         if not os.path.isfile(mypath):
#             d={'is_dir':True, 'has_file':len(os.listdir(mypath)), 'filesize':0, 'is_photo':False, 'filetype':''}
#         else:
#             file_ext=e.split('.')[-1]
#             d={'is_dir':False,
#                'has_file':False,
#                'filesize':os.path.getsize(mypath),
#                'dir_path':'',
#                'is_photo':file_ext in ext_arr['image'],
#                'filetype':file_ext
#                }
        
        
#         t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(mypath)))
#         d.update({'filename':e, 'datetime':t})
#         i+=1
#         file_list.append(d)
        
#     path=form.get('path')
#     order=form.get('order','').lower() or 'name'
#     d_order['order']=order
#     sorted(file_list, cmp=cmp_func)
#     file_url='%s/%s/%s/%s'%(fs_url,'editor_files',usr_id,dir_name)
#     result={'moveup_dir_path':'./',
#             'current_dir_path':'/',
#             'current_url':file_url,
#             'total_count': len(file_list),
#             'file_list':file_list
#             }
#     return HttpResponseJsonCORS(result)

