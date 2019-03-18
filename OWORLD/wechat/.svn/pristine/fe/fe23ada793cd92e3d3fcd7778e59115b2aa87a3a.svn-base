#-*- coding: utf-8 -*-
prj_name=__name__.split('.')[0]
import time
import os
import json
import datetime
import random
import MySQLdb
exec ('from %s.share import db,dActiveUser,ComplexEncoder,mValidateUser,HttpResponseCORS,HttpResponseJsonCORS,fs_url,front_url,data_url,ToGBK,m_prjname'%prj_name)
exec ('from %s.wx_cb.wxpush        import mWxPushMsg_Log'%prj_name)   

from HW_FILE_TOOL               import make_sub_path
import httplib
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

error_url = '%s/wx/mui/error.html'%front_url
errmsg = """
    {
    "errcode": -1,
    "errmsg": "你没有权限浏览当前页",
    }
    """ 
def check_usr(request):
    """功能：验证用户是否有访问当前功能的权限"""
    d_value = ['']*10
    if request.session.has_key('login_data_wx'):  
        d_value = request.session.get('login_data_wx','')
        return 0,d_value
    else:
        errcode,errmsg,d_value = mValidateUser(request,'view',104)
    return errcode,d_value

upload_path = "/home/webroot/data/%s/attach_files/"%(m_prjname)
def attach_save(request):
    today = datetime.date.today()
    year = today.year
    month = today.month
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        menu_id = request.POST.get('menu_id', 0)
        id =  request.POST.get('pk','') 
        source =  request.POST.get('option','')    
        if source == '': source = 1
        random_no = request.POST.get('random_no', '')
        ret,d_value = check_usr(request)
        if ret != 0:
            return HttpResponseCORS(request,errmsg)        
        usr_id = d_value[0]
        usr_name = d_value[1]
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            s = """
                {
                "error": 1
                }
                """
            return HttpResponseJsonCORS(request,s)
        title = myFile.name
        f_ext=title.split('.')[-1]
        fname = "%s_%s_%s.%s"%(usr_id,time.time(),random.randint(0,99),f_ext)
        small_name = "small_%s"%(fname)
        if f_ext.upper() in['GIF','JPG','JPEG','PNG','BMP']:
            is_pic = 1
        else:is_pic=0
        if id=='':id='NULL'
        sql = """insert into file_pic (menu_id,gw_id,title,fname,file_size,is_pic,random_no,cid,cusrname,ctime,source)
                    values(%s,%s,'%s','%s',%s,%s,'%s',%s,'%s',now(),%s);
              """%(menu_id,id,title,fname,myFile.size,is_pic,random_no,usr_id,usr_name,source)
        #print sql
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        file_id = rows[0][0]
 
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
        sql = 'update file_pic set is_pic=%s where id=%s'%(is_pic,file_id)
        db.executesql(sql)
        if is_pic == 1: 
            img = Image.open(os.path.join(path,fname))
            x,y = img.size
            x1 = 80
            y1 = 80*y/x
            try:
                img = img.resize((x1, y1), Image.ANTIALIAS)
                img.save(os.path.join(path,small_name))
                pic_url = os.path.join(front_url,'attach',str(year),str(month),small_name)
            except:
                pic_url=""
        else: 
            pic_url=""
        url = os.path.join(front_url,'attach',str(year),str(month),fname)
        s = """{"files":[{        
            "error":false, 
            "file_id":%s,            
            "size":%s,
            "name":"%s",
            "thumbnail_url":"%s",
            "url":"%s",
            "delete_url":"%s/del_file/?fname=%s"
            }]}
            """%(file_id,myFile.size,myFile.name,pic_url,url,data_url,fname)
        return HttpResponseJsonCORS(request,s)

    s = """
        {
        "error": 2
        }
        """
    return HttpResponseJsonCORS(request,s) 

#获得可点评部门
def getDepts(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]

    usr_ids = ''
    sql = "select ifnull(usr_ids,'') from work_log_right where dp_usr_id=%s;"%(usr_id)
    rows,iN = db.select(sql)
    if iN>0:
        usr_ids = rows[0][0]

    sql="""select d.id,case ifnull(d1.id,0) when 0 then d.cname else concat(d1.cname,'/',d.cname) end from (
           select dept_id from users where FIND_IN_SET(usr_id,'%s')
           UNION
           SELECT dept_id FROM dept_role_users 
            WHERE dr_id in (1,2,4) and usr_id = %s) dp
            left join dept d on dp.dept_id = d.id
            left join dept d1 on d.parent_id = d1.id and d1.ilevel !=1
            where d.del_flag=0
            order by d.sort
            """%(usr_ids,usr_id)
    print sql
    rows,iN = db.select(sql)
    names = 'id name'.split()
    data = [dict(zip(names, d)) for d in rows]

    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "data":%s
        }
        """%(s3)
    #print s
    return HttpResponseCORS(request,s)

#获得可点评人员
def getUsers(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    pageNo = request.POST.get('pageNo', '1')
    pageNo=int(pageNo)
    search = request.POST.get('search', '')
    dept_id = request.POST.get('dept_id', '')

    sql="""select UC.usr_id,UC.usr_name from (
                SELECT DISTINCT cid
                FROM work_log 
                where Find_in_set(%s,dp_users) ) w
                Left join users UC on UC.usr_id = W.cid
                where UC.status=1 
            """%(usr_id)
    if dept_id !='':
        sql += " and UC.dept_id = %s"%(dept_id)
    if search !='':
        sql += " and UC.usr_name like '%%%s%%'"%(search)
    sql += " order by UC.usr_name"
    print sql
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'usr_id usr_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "userList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(s3,iTotal_length,iTotal_Page,pageNo,select_size)
    #print s
    return HttpResponseCORS(request,s)

#日志类别
def getLogType(request):
    sql="""SELECT id,txt1 FROM mtc_t WHERE type='GZYZLB'
            """
    rows,iN = db.select(sql)
    names = 'id name'.split()
    data = [dict(zip(names, d)) for d in rows]

    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "data":%s
        }
        """%(s3)
    #print s
    return HttpResponseCORS(request,s)

#日志重要程度
def getLogPriority(request):
    sql="""SELECT id,txt1 FROM mtc_t WHERE type='ZYCD'
            """
    rows,iN = db.select(sql)
    names = 'id name'.split()
    data = [dict(zip(names, d)) for d in rows]

    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取数据成功",
        "data":%s
        }
        """%(s3)
    #print s
    return HttpResponseCORS(request,s)

#我的日志
def getMyLogList(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    pageNo = request.POST.get('pageNo', '1')
    pageNo=int(pageNo)
    cdate = request.POST.get('cdate', '')

    sql="""SELECT  
                    W.id,                                                                          
                    W.wtime,                                     
                    W.ctime,   
                    r_count,       
                    dp_count,             
                    W.cid,
                    W.type_txt,
                    W.priority_txt,                                                           
                    W.wdes,                                                                   
                    W.wresult,is_wwcyw,wwc_txt
                FROM work_log W
                where w.cid=%s """%(usr_id)
    if cdate != '':
        sql+=" and date_formt(wtime,'%%Y-%%m-%%d') = '%s'"%cdate
            
    sql+=" ORDER BY w.wtime desc,w.cid asc,w.id desc"
    print sql
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,1,100)
    names = 'id wtime ctime r_times p_times usr_id wtype priority wdes wresult is_wwcyw wwc_txt'.split()
    data = [dict(zip(names, d)) for d in rows]
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取日志列表成功",
        "userList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(s3,iTotal_length,iTotal_Page,pageNo,select_size)
    #print s
    return HttpResponseCORS(request,s)

# 他人日志
def getLogList(request):
    print request.POST
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    print "usr_id=%s"%usr_id
    pageNo = request.POST.get('pageNo', '1')
    pageNo=int(pageNo)
    cdate = request.POST.get('date', '')
    cuser_id = request.POST.get('usr_id', '')
    dept = request.POST.get('dept', '')

    if cdate=='':
        d = datetime.datetime.now()
        cdate1 = d.strftime('%Y-%m-%d')
        d = d - datetime.timedelta(days=7)
        cdate = d.strftime('%Y-%m-%d')
    else:
        cdate1 = cdate 
        d = datetime.datetime.strptime(cdate1, "%Y-%m-%d")
        cdate1 = d.strftime('%Y-%m-%d')
        d = d - datetime.timedelta(days=7)
        cdate = d.strftime('%Y-%m-%d')

    sql="""SELECT  
                    W.id,                                                                          
                    W.wtime,                                     
                    W.ctime,   
                    r_count,       
                    dp_count,             
                    UC.usr_name,
                    concat("%s/user_pic/small_",UC.pic),   
                    W.type_txt,
                    W.priority_txt,                                                           
                    W.wdes,                                                                   
                    W.wresult,is_wwcyw,wwc_txt
                FROM work_log W
                Left join users UC on UC.usr_id = W.cid
                where Find_in_set(%s,dp_users) """%(fs_url,usr_id)
    if cuser_id!='':
        sql += " and w.cid = '%s'"%cuser_id
    if dept != '':
        sql+=" AND UC.dept_id = %s"%dept
    if cdate != '':
        sql+=" and wtime <= '%s' and wtime>='%s'"%(cdate1,cdate)
            
    sql+=" ORDER BY w.wtime desc,w.cid asc,w.id desc"
    print sql
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id wtime ctime r_times p_times usr_name pic wtype priority wdes wresult is_wwcyw wwc_txt'.split()
    data = [dict(zip(names, d)) for d in rows]
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取日志列表成功",
        "userList":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }
        """%(s3,iTotal_length,iTotal_Page,pageNo,select_size)
    #print s
    return HttpResponseCORS(request,s)

#获取日志详情
def getLog(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    id = request.POST.get('id', '1')

    if id=='':
        s = """
                {
                "errcode": -1,
                "errmsg": "参数错误",
                }
                """
        return HttpResponseCORS(request,s)
    else:  
        sql="""SELECT
                       W.id                                 
                       ,W.wtime  
                       ,W.type_txt                              
                       ,W.priority_txt                                                               
                       ,W.wdes                        
                       ,W.wresult                       
                       ,W.proj_id                       
                       ,ifnull(W.proj_name,'')                     
                       ,W.cid         
                       ,UC.usr_name
                       ,concat("%s/user_pic/small_",UC.pic)   
                       ,date_format(W.ctime,'%%Y-%%m-%%d %%T')
                       ,dp_count
                       ,W.is_wwcyw
                       ,W.wwc_txt
                       ,'',''
                   FROM work_log W
                   LEFT JOIN users UC ON UC.usr_id=W.cid
                   WHERE W.id=%s
        """%(fs_url,id)
        #print sql
        rows,iN = db.select(sql)
        L=list(rows[0])

        #判断非填写人用户是否已经阅读此日志，如果没有阅读，增在阅读记录上增加一条
        if iN > 0:
            if L[8] != usr_id:
                sql = """select m_id,usr_id from work_log_read where m_id = %s and usr_id = %s
                    """ %(L[0],usr_id)
                rows1,iN1=db.select(sql)
                if iN1 == 0:
                    sql = """insert into work_log_read (m_id,usr_id,r_time)
                            values (%s,%s,now())
                        """ %(L[0],usr_id)
                    db.executesql(sql)
                    sql = "update work_log set r_count = r_count+1 where id=%s"%(id)
                    db.executesql(sql)

            sql="""
            select
            L.log_id,                                       
            L.dp_memo,                                  
            U.usr_name,                               
            date_format(L.dp_time,'%%Y-%%m-%%d %%T'), 
            L.dp_usid,                                
            concat("%s/user_pic/small_",U.pic)                                        
            from work_log_dp L
            left join USERS U on L.dp_usid = U.usr_id
            where L.log_id = %s
            order by dp_time desc
            """%(fs_url,id)
            lT1,iN1=db.select(sql)
            names = 'log_id dp_memo usr_name dp_time dp_usid pic'.split()
            L[-2] = [dict(zip(names, d)) for d in lT1]

            sql="SELECT ifnull(fname,''),'','',file_size,ctime,is_pic,title,date_format(ctime,'%%Y'),date_format(ctime,'%%m') FROM file_pic WHERE gw_id=%s and menu_id=104"%(id)
            print sql
            lT1,iN1=db.select(sql)
            L2 = []
            for e in lT1:
                L1=list(e)
                fname = e[0]
                year = int(e[7])
                month = int(e[8])
                L1[0] = os.path.join(front_url,'attach',str(year),str(month),fname)
                L1[1] = os.path.join(front_url,'attach',str(year),str(month),"small_%s"%fname)
                L1[2] = "%s/del_file/?fname=%s"%(data_url,fname)
                L2.append(L1)
            names = "url thumbnail delete_url file_size ctime is_pic title".split()
            L[-1] = [dict(zip(names, d)) for d in L2]

            names = 'id wtime type priority wdes wresult proj_id proj_name cid usr_name pic ctime p_times is_wwcyw wwc_txt comment attach'.split()
            data = dict(zip(names, L))
        else:
            s = """
                {
                "errcode": -1,
                "errmsg": "该条日志已被删除",
                }
                """
            return HttpResponseCORS(request,s)
            
    s3 = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
            {
            "errcode": 0,
            "errmsg": "获取日志信息成功",
            "data": %s
            }        """%(s3)
    return HttpResponseCORS(request,s)

def getDPUsers(usr_id):
    users = ''
    temp = ''
    leader = 0
    sql = """SELECT r.dr_id,r.usr_id 
            FROM users u
            LEFT JOIN dept_role_users r ON r.dept_id = u.dept_id
            WHERE u.usr_id = %s and  r.dr_id in (1,2,4)
          """%(usr_id)  
    lT,iN=db.select(sql)   
    for e in lT:
        if e[1] == int(usr_id):
            leader = e[0]
    for e in lT:
        if leader == 1:   #第一负责人
            if e[0] ==4:
                temp += "%s,"%e[1]
        elif leader == 2:   #第二负责人
            if e[0] in (1,4):
                temp += "%s,"%e[1]
        elif leader == 4:   #分管领导
            continue
        else:               #普通员工
            if e[0] in (1,4,2):
                temp += "%s,"%e[1]

    sql = """select ifnull(group_concat(usr_id),'') from (
                select usr_id from users where Find_in_set(usr_id,'%s')
                UNION
                select dp_usr_id from work_log_right where Find_in_set(%s,usr_ids)) dp
                where dp.usr_id != %s """%(temp,usr_id,usr_id)
    lT,iN=db.select(sql)
    if iN>0:
        users = lT[0][0]
    return users

#日志填写
def putLog(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    type_txt = request.POST.get('type_txt', '')
    priority = request.POST.get('priority', '')
    priority_txt = request.POST.get('priority_txt', '')
    wdes = request.POST.get('wdes', '')
    wdes = MySQLdb.escape_string(wdes)
    wresult = request.POST.get('wresult', '')
    wresult = MySQLdb.escape_string(wresult)
    proj_id = request.POST.get('proj_id', '')
    if proj_id == '': proj_id = 'NULL'
    proj_name = request.POST.get('proj_name', '')
    is_wwcyw = request.POST.get('is_wwcyw', '')
    wwc_txt = request.POST.get('wwc_txt', '')
    wwc_txt = MySQLdb.escape_string(wwc_txt)
    wtime = request.POST.get('wtime', '')
    random_no = request.POST.get('random_no', '')

    dp_users = getDPUsers(usr_id)
    if id=='':
        sql="""INSERT INTO work_log (wtime,type,priority,wdes,wresult,proj_id
                              ,random_no,cid,ctime,proj_name,is_wwcyw,wwc_txt,type_txt,priority_txt,dp_users)
                       VALUES('%s',%s,%s,'%s','%s',%s,'%s',%s,now(),'%s',%s,'%s','%s','%s','%s')
                    """%(wtime,type,priority,wdes,wresult,proj_id,random_no,usr_id
                        ,proj_name,is_wwcyw,wwc_txt,type_txt,priority_txt,dp_users)
        print ToGBK(sql)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        id = rows[0][0]
    else:
        sql="""update work_log set wtime='%s'
                                    ,type=%s
                                    ,priority='%s'
                                    ,wdes='%s'
                                    ,wresult='%s'
                                    ,proj_id=%s
                                    ,uid=%s
                                    ,utime =now()
                                    ,proj_name='%s'
                                    ,is_wwcyw=%s
                                    ,wwc_txt='%s'
                                    ,type_txt='%s'
                                    ,priority_txt='%s'
                                    ,dp_users='%s'
                                    where id=%s
                 """%(wtime,type,priority,wdes,wresult,proj_id,usr_id,proj_name,is_wwcyw,wwc_txt,type_txt,priority_txt,dp_users,id)
        #print sql
        db.executesql(sql)

    sql = "update file_pic set gw_id=%s where menu_id=104 and random_no='%s'"%(id,random_no)
    db.executesql(sql)
    if int(priority)>1:
        push_log_msg(id,dp_users)
    s = """
            {
            "errcode": 0,
            "errmsg": "保存日志信息成功"
            }        """
    return HttpResponseCORS(request,s)

#日志点评
def putComment(request):
    ret,d_value = check_usr(request)
    if ret != 0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    id = request.POST.get('id', '')
    memo = request.POST.get('memo', '')
    memo = MySQLdb.escape_string(memo)

    sql="""insert work_log_dp (log_id,dp_memo,dp_usid,dp_time) values (%s,'%s',%s,now());
                   """%(id,memo,usr_id)
    db.executesql(sql)
    sql = "select last_insert_id();"
    rows,iN = db.select(sql)
    dp_id = rows[0][0]
    sql = "select priority from work_log where id = %s "%(id)
    rows,iN = db.select(sql)
    sql = "update work_log set dp_count = dp_count+1 where id=%s"%(id)
    db.executesql(sql)
    if iN>0 and rows[0][0]>0:
        push_log_comment(dp_id,usr_id)
    s = """
            {
            "errcode": 0,
            "errmsg": "保存日志点评成功"
            }        """
    return HttpResponseCORS(request,s)

def push_log_msg(id,dp_users) :
    sql="""SELECT WB.id
                    ,left(WB.wdes,500)
                    ,WB.wresult
                    ,ifnull(U.usr_name,'')
                    ,WB.cid
                    ,WB.ctime
            FROM work_log WB 
            LEFT JOIN users U ON U.usr_id = WB.cid
            WHERE WB.id=%s
        """%(id)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    L=list(rows[0])
    title = """【%s】发表了新的重要日志"""%(L[3])
    description = L[1]
    func = 'logDetail'
    usr_id = L[4]
    usr_name = L[3]
    sql = "select ifnull(group_concat(ifnull(wxqy_id,login_id)),'') from users where FIND_IN_SET(usr_id,'%s')"%(dp_users)
    print sql
    rows,iN = db.select(sql)
    L=list(rows[0])
    if L[0] != '':
        toUser = L[0].replace(',','|')
        print toUser
        return mWxPushMsg_Log(id,title,description,toUser,func,usr_id,usr_name)
    return

def push_log_comment(id,usr_id) :
    sql="""SELECT WB.id
                    ,left(ifnull(dp.dp_memo,''),500)
                    ,ifnull(U.usr_name,'')
                    ,ifnull(U1.usr_name,'')
                    ,dp.dp_time
                    ,ifnull(dp_users,'')
                    ,WB.cid
            FROM work_log WB 
            LEFT JOIN users U ON U.usr_id = WB.cid
            LEFT JOIN work_log_dp dp ON dp.log_id = WB.id
            LEFT JOIN users U1 ON U1.usr_id = dp.dp_usid
            WHERE dp.id=%s
        """%(id)
    #print ToGBK(sql)
    rows,iN = db.select(sql)
    L=list(rows[0])
    title = """【%s】点评了【%s】的日志"""%(L[3],L[2])
    description = L[1]  
    func = 'logDetail'
    usr_name = L[3]
    log_id = L[0]
    dp_users = L[5] + ',%s'%(L[6])
    sql = "select ifnull(group_concat(ifnull(wxqy_id,login_id)),'') from users where FIND_IN_SET(usr_id,'%s') and usr_id!=%s"%(dp_users,usr_id)
    print sql
    rows,iN = db.select(sql)
    L=list(rows[0])
    if L[0] != '':
        toUser = L[0].replace(',','|')
        return mWxPushMsg_Log(log_id,title,description,toUser,func,usr_id,usr_name)
    return

