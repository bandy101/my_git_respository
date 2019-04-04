# -*- coding: utf-8 -*-
import os,sys,traceback
import time
import urllib
from HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG
from HW_DB_TOOL   import DataBaseParent
from aesMsgCrypt                import WXBizMsgCrypt
from django.http import HttpResponse
import json
from datetime import date, datetime 
import decimal
import re
import MySQLdb
#限制用 "from XXXX import *" 时可以导入的名字
__all__ = ['CLIENT_NAME','WEBSITE_PATH','m_sCorpID','m_sCorpSecret',
           'db','dActiveUser',
           'TIME_OUT','mValidateUser','get_YES_NO_data','get_dept_data',
           'get_mtc_t_data','HttpResponseCORS'
           ]

#获取客户名
CLIENT_NAME      = __name__.split('.')[0]
#配置失效时间为半个小时
TIME_OUT = 30 
try:
    db=DataBaseParent()     #关系数据库
except:
    raise Exception('db connect error')

def ToUnicode(s):#因python对字符串进行unicode编码后会在字符串的前面加上一个前辍u,该前辍对编码没有起到作用，且还限制了程序对该字符串的修改，本函数仅是去掉该前辍
    try:#可以直接转换成字符串的，直接转换，不可以直接转换的，先拆分，再组合
        s=str(s.decode("GBK").encode("utf-8"))
    except:
        s1=''
        s2=''
        L=[]
        s2=str(list(s.decode('GBK')))
        s2=s2.replace("u'","'")
        s2=s2.replace("\\","%")
        L=eval(s2)
        
        for e in L:
            s1+=e
        s=s1.encode("utf-8")
    return s

def ToGBK(s):
    try:
        s=str(s.decode("utf-8").encode("GBK"))
    except:
        s=s
    s = s.replace("\n","\r\n")
    return s

class cSysInfo:
    def __init__(self):
        self.Lsys={}
        self.ext_sys={}
        self.loaddata()

    def loaddata(self,sKey=''):         
        sql="""select 
                    s.`corp_name`,
                    `full_name`,
                    `logo`,
                    `icon`,
                    `prj_name`,
                    `db_name`,
                    `data_url`,
                    `front_url`,
                    `fs_url`,
                     corp_url, s.corp_id,a.agentid,concat(fs_url,'/sys/printLogo.png'),
                     '','',icp,aesKey
               from `sys_info` s
               left join wx_corp_agent a on a.corp_id = s.corp_id and a.`name` = '%s'  
            """ %(ToUnicode('授权登录'))
        lT,iN=db.select(sql)
        self.Lsys=list(lT[0])
        
        try:
            sql = "select ifnull(value,0) from sys_ext_info where name='muti_lang'"
            lT,iN=db.select(sql)
            if iN>0: 
                muti_lang = int(lT[0][0])
            else:
                muti_lang = 0
        except:
            muti_lang = 0
        self.Lsys[13] = muti_lang
        

    def get(self):
        return self.Lsys        

    def update(self):
        self.loaddata()
        
oSysInfo=cSysInfo()

#公共的常数，和一些共享的变量
WEBSITE_PATH=os.path.join('/home/webroot/oWorld/',CLIENT_NAME)
dActiveUser={}     
Lsys = oSysInfo.get()   
data_url = Lsys[6]  #"http://www.szoworld.cn:8099/data1"# Lsys[6]  #
front_url = Lsys[7]
fs_url = Lsys[8]
m_dbname = Lsys[5]
m_prjname = Lsys[4]
m_corp_name = Lsys[0]
m_aesKey = Lsys[16]
m_corp_wxid =  Lsys[10]
m_muti_lang = Lsys[13]

class GlobalVar:   
    usr_id = None
    usr_name = None
    cur_dept_id = None
    cur_dept_name = None
    type_id = None
    def set_value(self,d_value):   
        self.usr_id = d_value[0]
        self.usr_name = d_value[1]
        self.cur_dept_id = d_value[2]
        self.cur_dept_name = d_value[3]
        self.type_id = d_value[4]

g_data = GlobalVar()




def my_urlencode(str) :
    str = urllib.quote(str)
    
    return str.lower()

def strDuplicateRemoval(str):
    L = str.split(',')
    L1 = list(set(L))
    str = ','.join(L1)
    return str

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            #return obj.strftime('%Y-%m-%d %H:%M:%S')
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):  
            return str(obj)          
        else:
            return json.JSONEncoder.default(self, obj)

def get_YES_NO_data(sDF):
    a,b='',''
    if str(sDF) == '1':
        a = '1'
    else:
        b = '1'
    L = []
    L.append(['1',ToUnicode('是'),'',a])
    L.append(['0',ToUnicode('否'),'',b])
    return L

def get_mtc_t_data(sDF,type,title=ToUnicode('--请选择--'),single=True):
    sql="SELECT id,txt1 FROM mtc_t WHERE type='%s' order by sort" %type
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_mtc_sys_data(sDF,type,title=ToUnicode('--请选择--'),single=True):
    sql="SELECT id,txt1 FROM mtc_sys WHERE type='%s' order by sort" %type
    #print sql + str(single) + str(sDF)
    lT,iN = db.select(sql)
    ldf=[]
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        #print ldf
        for i in range(0,len(ldf)):
            ldf[i] = int(ldf[i] or 0)

    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    #print ldf
    for e in lT:
        if single:
            if sDF==str(e[0]):b='1'
            else:b=''
        else:
            if e[0] in ldf:
                b = '1'
            else:b=''    
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_field_type(sDF,type,title='',single=True):
    sql="SELECT id,memo FROM field_type order by sort" 
    lT,iN = db.select(sql)
    #print sDF
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_sel_cols(sDF,type,title='',single=True):
    lT =[]
    if type!='':
        sql="select id,label from menu_select_all_cols where sel_type=%s"%type 
        lT,iN = db.select(sql)
    ldf=[]
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        #print ldf
        for i in range(0,len(ldf)):
            ldf[i] = int(ldf[i] or 0)

    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    #print ldf
    for e in lT:
        if single:
            if sDF==str(e[0]):b='1'
            else:b=''
        else:
            if e[0] in ldf:
                b = '1'
            else:b=''    
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_dept_data(sDF,title=ToUnicode('--选择部门--'),single=True):
    sql="SELECT id,cname,parent_id,iLevel=1 FROM dept where del_flag = 0 ORDER BY sort" 
    lT,iN = db.select(sql)
    ldf=[]
    sDF=str(sDF)
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]

    for e in lT:
        if single:
            if sDF==str(e[0]):b='1'
            else:b=''
        else:
            if str(e[0]) in ldf:
                b = '1'
            else:b=''    
        txt=e[1]
        L.append([e[0],txt,b,e[2],e[3]])
    return L

def get_USTAT_data_delete(sDF,single=True):
    #返回用户的状态选择数据,0:禁用,1:有效
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    L=[['','--状态--','',b]]
    if sDF=='0':b='1'
    else:b=''
    L.append(['0','无效','',b])
    if sDF=='1':b='1'
    else:b=''
    L.append(['1','有效','',b])
    if sDF=='3':b='1'
    else:b=''
    L.append(['3','删除','',b])
    return L

def get_roles_list(sDF,deptid,title=ToUnicode('--选择角色--'),single=True):
    if sDF=='':b='1'
    else: b=''
    if title!='':
        L=[['',title,'',b,'']]
    else:
        L=[]
    sql="""select
                role_id
                ,ifnull(role_name,'')
            from roles
            where dept_id != 0
        """
    if str(deptid) != '' and str(deptid) != '0':
        sql+= " and dept_id = %s"%deptid
    sql+=" order by role_name"
    #print sql
    lT,iN = db.select(sql)
    if iN>0:
        for e in lT:
            id,name=e
            if str(id) == str(sDF):
                b = '1'
            else:
                b = ''
            L.append([id,name,'',b])
    return L

#获得流程一级分类
def get_gw_type_data1(sDF,title=ToUnicode('--请选择--'),single=True):
    sql="SELECT id,cname,i_level FROM gw_type WHERE i_level = 0 and status=1 ORDER BY id" 
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt= e[1]
        L.append([e[0],txt,b])
    return L

#获得流程二级分类
def get_gw_type_data2(sDF,parent_id,title=ToUnicode('--公文流程二级分类--'),single=True):
    lT=[]
    if parent_id!='':
        sql="SELECT id,cname,i_level FROM gw_type WHERE p_id = %s and status=1 ORDER BY id"%(parent_id)
        lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt= e[1]
        L.append([int(e[0]),txt,b])
    return L

def get_first_flow_data(sDF,gw_type,title=ToUnicode('--起始流程--'),single=True):
    lT=[]
    if gw_type !='':
        sql="SELECT id,cname FROM gw_flow_def where type_id=%s AND IFNULL(s_flag,0) = 1"%(gw_type)        
        lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt= e[1]
        L.append([int(e[0]),txt,b])
    return L

def get_flow_data(sDF,gw_type,has_flow,title=ToUnicode('--请选择--'),single=True):
    lT=[]
    if gw_type !='':
        sql="SELECT id,cname FROM gw_flow_def where type_id=%s"%(gw_type)  
        if has_flow!='':
            sql += " and id !=%s"%(has_flow) 
        lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt= e[1]
        L.append([int(e[0]),txt,b])
    return L

def get_all_tables(sDF,title='',single=True):
    sql="select table_name,ifnull(table_comment,'') from information_schema.tables where table_schema='%s' and table_type='base table';"%(m_dbname)
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    sDF = sDF.upper()
    for e in lT:
        table_name = e[0]
        table_name = table_name.upper()
        table_comment = e[1] 
        table_comment = table_comment.replace(ToUnicode('自动创建：'),'')
        txt = table_name
        if table_comment != '':
            txt += "(%s)"%(table_comment)
        if sDF==table_name:b='1'
        else:b=''
        L.append([table_name,txt,b])
    return L

def get_use_tables(sDF,page_id,title='',single=True):
    lT = []
    if page_id!='':
        sql="select table_name,table_ab from menu_list_tables where page_id=%s;"%page_id 
        #print sql
        lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    sDF = sDF.upper()
    #print sDF
    for e in lT:
        
        table_name = e[0]
        table_name = table_name.upper()
        table_ab = e[1]
        table_ab = table_ab.upper()
        table_name += " "+table_ab        
        if sDF==table_name:b='1' 
        else:b=''
        L.append([table_name,table_name,b])
    return L

def get_form_tables(sDF,step_id,title='--选择关联表--',single=True):
    lT=[]
    if step_id!='':
        sql="select table_name,table_ab from menu_form_tables where step_id=%s;"%step_id 
        #print sql
        lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    sDF = sDF.upper()
    #print sDF
    for e in lT:
        table_name = e[0]
        table_name = table_name.upper()
        table_ab = e[1]
        table_ab = table_ab.upper()
        table_name += " "+table_ab        
        if sDF==table_name:b='1' 
        else:b=''
        L.append([table_name,table_name,b])
    return L

def get_table_field(sDF,table_name,title=ToUnicode('--字段名称--'),single=True):
    lT=[]
    if table_name !='' and table_name!=None:
        table = table_name.split(' ')
        #print table
        sql="select column_name,ifnull(COLUMN_COMMENT,'') from information_schema.columns where table_schema='%s' and table_name='%s'"%(m_dbname,table[0])
        #print sql
        lT,iN = db.select(sql)
        if iN ==0:
            sql="select c.col_name,'' from menu_table_cols c left join menu_tables t on t.id=c.table_id where t.table_name='%s'"%(table[0])
            lT,iN = db.select(sql)
    
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    sDF = sDF.upper()
    for e in lT:
        if sDF==str(e[0]).upper():b='1'
        else:b=''
        if e[1] == '':
            txt = e[0]
        else:
            txt = e[0] +'('+e[1]+')'
        L.append([e[0].upper(),txt,b])
    return L

def get_page_field(sDF,menu_id,title='',single=True):
    ldf=[]
    sDF=str(sDF)
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    lT=[]
    if menu_id !='':
        sql="select id,label from menu_list_pages where menu_id='%s' and status=1 order by sort"%(menu_id)
        #print sql
        lT,iN = db.select(sql)
    for e in lT:
        if single:
            if sDF==str(e[0]):b='1'
            else:b=''
        else:
            if str(e[0]) in ldf:
                b = '1'
            else:b=''    
        L.append([e[0],e[1],b])
    return L

def get_col_field(sDF,page_id,title='',single=True):
    lT=[]
    if page_id !='':
        sql="select id,table_name,table_ab from menu_list_tables where page_id='%s' "%(page_id)
        #print sql
        lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        table_name = e[1]
        table_ab = e[2]
        sql="select column_name from information_schema.columns where table_schema='kjerp' and table_name='%s'"%(table_name)
        lT1,iN1 = db.select(sql)
        for e1 in lT1:
            col1 = table_ab + '.'+e1[0]
            col2 = table_name + '.'+e1[0]
            col1 = col1.upper()
            col2 = col2.upper()
            #print sDF+"  "+col1
            if sDF==col1:b='1'
            else:b=''
            L.append([col1,col2,b])
    return L

def mValidateUser(request,mode,menu_id):
    """功能：验证用户是否有访问当前功能的权限"""
    d_value = ['']*10
    source = request.POST.get('source', '')
    if source == 'wx':
        usr_id = request.session.get('usr_id_qy') or 2110
        sql = "select login_id from users where usr_id='%s'"%(usr_id)
        rows,iN = db.select(sql)
        if iN==0:
            errCode = -1
            s = """
                {
                "errcode": -1,
                "errmsg": "你没有权限浏览当前页！",
                }        """
            return errCode,ToUnicode(s),d_value
        login_id = rows[0][0]  
    else:
        usr_id = request.session.get('usr_id', 0)
        AccessToken = request.POST.get('AccessToken', '')
        wxcpt=WXBizMsgCrypt('szoworld',m_aesKey)
        ret,login_id,sTimeStamp = wxcpt.DecryptMsg(AccessToken)   
        if (ret !=0):
            errCode = -1
            s = """
                {
                "errcode": -1,
                "errmsg": "验证信息有误，请重新登陆！",
                }        """
            return errCode,ToUnicode(s),d_value
    
        sql = "select usr_id from users where login_id='%s'"%(login_id)
        rows,iN = db.select(sql)
        if iN==0:
            errCode = -1
            s = """
                {
                "errcode": -1,
                "errmsg": "你没有权限浏览当前页！",
                }        """
            return errCode,ToUnicode(s),d_value
        usr_id = rows[0][0]  

    if source == 'wx':
        sql = """select u.usr_id,u.usr_name,ifnull(d.id,0),d.cname,0,0,0,0,'wx'
                    from users u
                    left join dept d on d.id=u.dept_id
                    where u.login_id='%s'
                    """%(login_id)
    elif menu_id!='':
        sql = """select u.usr_id,u.usr_name,ifnull(d.id,0),d.cname,md.gw_type2,time_to_sec(now())-time_to_sec(u.refresh_time),u.expire_time,u.id,u.source
                    from (select u.usr_id,u.usr_name,u.dept_id,ul.refresh_time,ul.expire_time,ul.id,ul.source  from users_login ul left join users u on u.usr_id=ul.usr_id where u.login_id='%s'  and token='%s' order by ul.login_time desc limit 1) u
                    left join dept d on d.id=u.dept_id
                    left join usr_role ur on ur.usr_id=u.usr_id
                    left join role_menu rm on rm.role_id = ur.role_id and rm.menu_id=%s
                    left join menu_data_source md on md.menu_id=rm.menu_id
                    """%(login_id,AccessToken,menu_id)
        if usr_id not in [1,2]:
            sql += " where rm.can_view = 1 "
    else:
        sql = """select u.usr_id,u.usr_name,ifnull(d.id,0),d.cname,0,time_to_sec(now())-time_to_sec(u.refresh_time),u.expire_time,u.id,u.source
                    from (select u.usr_id,u.usr_name,u.dept_id,ul.refresh_time,ul.expire_time,ul.id,ul.source  from users_login ul left join users u on u.usr_id=ul.usr_id where u.login_id='%s'  and token='%s' order by ul.login_time desc limit 1) u
                    left join dept d on d.id=u.dept_id
                    """%(login_id,AccessToken)
    #print sql
    rows,iN = db.select(sql)
    if iN==0:
        errCode = -1
        s = """
            {
            "errcode": -1,
            "errmsg": "你没有权限浏览当前页！",
            }        """
        return errCode,ToUnicode(s),d_value
    sec = rows[0][5] or 0
    expire_time = rows[0][6] or 0
    if rows[0][8]!='wx' and sec>expire_time:
        errCode = 1
        s = """
            {
            "errcode": 1,
            "errmsg": "登录超时！",
            }        """
        return errCode,ToUnicode(s),d_value
    sql = "update users_login set refresh_time=now() where id=%s"%rows[0][7]
    db.executesql(sql)
    d_value = list(rows[0])
    g_data.set_value(d_value)
    return 0,'',d_value

def addtwodimdict(thedict, key_a, key_b, val): 
    if thedict.get(key_a):
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})
    return 
def getRequestValue(request,key,default):
    return

def HttpResponseCORS(request,s):
    response = HttpResponse(s)
    try:
        origin = request.META['HTTP_ORIGIN']  
    except:
        origin = front_url
    if origin.find("192.168") >0 :
        pass
    elif origin.find("127.0.0.1") >0 :
        pass
    else:
        origin = front_url
      
    #sql = "insert into sql_log (`sql`) values ('%s')"%(origin)
    #print sql
    #db.executesql(sql)
    
    response["Access-Control-Allow-Origin"] = "%s"%(origin)
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def HttpResponseJsonCORS(request,s):
    response = HttpResponse(s,content_type="application/json")
    try:
        origin = request.META['HTTP_ORIGIN']  
    except:
        origin = front_url

    if origin.find("192.168") >0 :
        pass
    elif origin.find("127.0.0.1") >0 :
        pass
    else:
        origin = front_url
    print origin
    response["Access-Control-Allow-Origin"] = "%s"%(origin)
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def sql_decode(final_sql):
    final_sql = final_sql.upper()
    #只保留一个空格
    import re
    final_sql = re.sub(r'\s+', ' ', final_sql)
    #print final_sql
    iPos = final_sql.find(' FROM ')
    table_sql = final_sql[iPos+6:]
    iPos1 = table_sql.find(' WHERE ')
    table_sql = table_sql[:iPos1]
    field_sql = final_sql[:iPos]
    field_sql = field_sql.replace('SELECT','')
    field_sql = field_sql.replace('%Y-%M-%D','%Y-%m-%d')

    #解析字段结构
    field_list = field_sql.split(',')
    field_list1 = []
    n = 0
    sTemp = ''
    bFlag = 1
    col_name = ''
    for e1 in field_list:
        e1 = e1.strip()
        L = ['col','order','name','label','col_type']
        if e1.find('IFNULL(')>=0 and e1.find('DATE_FORMAT(')>=0:
            n = 2
        elif e1.find('IFNULL(')>=0:
            n = 1
        elif e1.find('DATE_FORMAT(')>=0:
            n = 1
        elif e1.find('IF(')>=0:
            n = 2
        if bFlag == 1:
            col_name = e1
        if n==0:
            sTemp = sTemp + e1
            L[0] = sTemp
            L[1] = sTemp
            col_name = col_name.replace('IFNULL(','')
            col_name = col_name.replace('DATE_FORMAT(','')
            col_name = col_name.replace('IF(','')
            try:
                col_name = col_name.split('.')[1]
            except:
                pass
            L[3] = col_name
            col_name = 'F_' + col_name.lower()       
            L[2] = col_name
            L[4] = 1
            if L[0] == "'ADD'":
                L[1] = ''
                L[2] = 'add'
                L[3] = ToUnicode('添加')
                L[4] = 2
            elif L[0] == "'UPDATE'":
                L[1] = ''
                L[2] = 'update'
                L[3] = ToUnicode('修改')
                L[4] = 2
            elif L[0] == "'DELETE'":
                L[1] = ''
                L[2] = 'delete'
                L[3] = ToUnicode('删除')
                L[4] = 2
            field_list1.append(L)
            sTemp = ''
            bFlag = 1
        else:
            n = n - 1
            sTemp = sTemp + e1 +","
            bFlag = 0
    #解析表结构
    table_list = table_sql.split(' JOIN ')
    table_list1 = []
    iCount = len(table_list)
    mab = ''
    #print table_list
    lastJoin = ''
    for i in range(0,iCount):
        e = table_list[i].strip()
        e_list = e.split(' ')
        L = ['','','','','','',1]
        if i == 0:
            #L[0] = e_list[2]
            L[1] = e_list[0]
            L[2] = e_list[1]
            lastJoin = "%s JOIN"%e_list[2]
        elif i == (iCount-1):
            L[0] = lastJoin
            L[1] = e_list[0]
            L[2] = e_list[1]
            str = e_list[3]
            sl1 = str.split('=')
            sl2 = sl1[0].split('.')
            sl3 = sl1[1].split('.')
            if L[2] == sl2[0]:
                L[3] = sl2[1]
                L[4] = sl3[0]
                L[5] = sl3[1]
            else:
                L[3] = sl3[1]
                L[4] = sl2[0]
                L[5] = sl2[1]
        else:
            L[0] = lastJoin
            L[1] = e_list[0]
            L[2] = e_list[1]
            str = e_list[3]
            sl1 = str.split('=')
            sl2 = sl1[0].split('.')
            sl3 = sl1[1].split('.')
            if L[2] == sl2[0]:
                L[3] = sl2[1]
                L[4] = sl3[0]
                L[5] = sl3[1]
            else:
                L[3] = sl3[1]
                L[4] = sl2[0]
                L[5] = sl2[1]
            lastJoin = "%s JOIN"%e_list[4]
        L[6] = i+1
        table_list1.append(L)
        #print e_list
    #print table_list1
    return field_list1,table_list1

def sql_decode_form(final_sql):
    final_sql = final_sql.upper()
    #只保留一个空格
    import re
    final_sql = re.sub(r'\s+', ' ', final_sql)
    iPos = final_sql.find(' FROM ')
    table_sql = final_sql[iPos+6:]
    iPos1 = table_sql.find(' WHERE ')
    table_sql1 = table_sql[:iPos1]
    field_sql = final_sql[:iPos]
    field_sql = field_sql.replace('SELECT','')
    field_sql = field_sql.replace('%Y-%M-%D','%Y-%m-%d')

    #解析字段结构
    field_list = field_sql.split(',')
    field_list1 = []
    n = 0
    sTemp = ''
    bFlag = 1
    col_name = ''
    for e1 in field_list:
        e1 = e1.strip()
        L = ['col','order','name','label','col_type']
        if e1.find('IFNULL(')>=0 and e1.find('DATE_FORMAT(')>=0:
            n = 2
        elif e1.find('IFNULL(')>=0:
            n = 1
        elif e1.find('DATE_FORMAT(')>=0:
            n = 1
        elif e1.find('IF(')>=0:
            n = 2
        if bFlag == 1:
            col_name = e1
        if n==0:
            sTemp = sTemp + e1
            L[0] = sTemp
            L[1] = sTemp
            #print col_name
            col_name = col_name.replace('IFNULL(','')
            col_name = col_name.replace('DATE_FORMAT(','')
            col_name = col_name.replace('IF(','')
            col_name = col_name.replace("'",'')
            try:
                col_name = col_name.replace(".",'_')
            except:
                pass
            #print col_name
          
            L[3] = col_name
            col_name = 'F_' + col_name.lower()       
            L[2] = col_name
            L[4] = 1
            field_list1.append(L)
            sTemp = ''
            bFlag = 1
        else:
            n = n - 1
            sTemp = sTemp + e1 +","
            bFlag = 0
    #解析表结构
    table_list = table_sql1.split(' JOIN ')
    table_list1 = []
    iCount = len(table_list)
    mab = ''
    #print table_list
    lastJoin = ''
    for i in range(0,iCount):
        e = table_list[i].strip()
        e_list = e.split(' ')
        L = ['','','','','','',1]
        if i == 0:
            #L[0] = e_list[2]
            L[1] = e_list[0]
            try: 
                L[2] = e_list[1]
                lastJoin = "%s JOIN"%e_list[2]
            except:
                pass
        elif i == (iCount-1):
            L[0] = lastJoin
            L[1] = e_list[0]
            L[2] = e_list[1]
            str = e_list[3]
            sl1 = str.split('=')
            sl2 = sl1[0].split('.')
            sl3 = sl1[1].split('.')
            if L[2] == sl2[0]:
                L[3] = sl2[1]
                L[4] = sl3[0]
                L[5] = sl3[1]
            else:
                L[3] = sl3[1]
                L[4] = sl2[0]
                L[5] = sl2[1]
        else:
            L[0] = lastJoin
            L[1] = e_list[0]
            L[2] = e_list[1]
            str = e_list[3]
            sl1 = str.split('=')
            sl2 = sl1[0].split('.')
            sl3 = sl1[1].split('.')
            if L[2] == sl2[0]:
                L[3] = sl2[1]
                L[4] = sl3[0]
                L[5] = sl3[1]
            else:
                L[3] = sl3[1]
                L[4] = sl2[0]
                L[5] = sl2[1]
            lastJoin = "%s JOIN"%e_list[4]
        L[6] = i+1
        table_list1.append(L)
        #print e_list
    #print table_list1
    return field_list1,table_list1,table_sql

def sql_encode(col_rows,table_sql):
    final_sql = "SELECT DISTINCT "
    search_sql = "CONCAT("
    col_sql = ''
    n = 0
    for e in col_rows:
        if e[0] !='' and e[0] != None:
            col_sql += "%s,"%e[0]
        else:
            col_sql += "'',"
        if e[2] == 1:
            search_sql += "IFNULL(%s,''),"%e[0]
            n += 1
    col_sql = col_sql[:-1]
    if n == 0:
        search_sql = ''
    else:
        search_sql = search_sql[:-1] + ")"
    final_sql += col_sql +" "
    final_sql += table_sql 
         
    #print final_sql
    final_sql = final_sql.replace('%Y-%M-%D','%Y-%m-%d')

    return final_sql,search_sql

def encode_table_sql(table_rows):
    table_sql = "FROM "
    iCount = len(table_rows)
    i = 0
    for e in table_rows:
        if e[6] != '':
            table = "(%s)"%e[6]
        else:
            table = e[1]
        if i == 0:
            table_sql += "%s %s"%(table,e[2])
        else:
            table_sql += " %s %s %s ON %s.%s=%s.%s"%(e[0],table,e[2],e[2],e[3],e[4],e[5])
        i += 1
    #print table_sql
    return table_sql

def sql_form_encode(col_rows,table_sql):
    add_sql = sql_form_encode_func(col_rows,table_sql,1)
    update_sql = sql_form_encode_func(col_rows,table_sql,2)
    audit_sql = sql_form_encode_func(col_rows,table_sql,3)
    verify_sql = sql_form_encode_func(col_rows,table_sql,4)
    view_sql = sql_form_encode_func(col_rows,table_sql,5)
    return add_sql,update_sql,audit_sql,view_sql,verify_sql

def sql_form_encode_func(col_rows,table_sql,func):
    sql = "SELECT "
    col_sql = ''
    for e in col_rows:
        if str(func) in e[1].split(','):
            if e[0] == '':
                col_sql += "'',"
            else:
                col_sql += "%s,"%e[0]

    col_sql = col_sql[:-1]
    sql += col_sql +" "
    sql += table_sql 
    sql = sql.replace('%Y-%M-%D','%Y-%m-%d')

    return sql

def get_options_data_view(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single = True):
    if type==0 or type==None:
        return default
    L = get_options(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single,True)
    #print L
    value = ''
    for e in L:
        if str(e[2])=='1': 
            #print e
            if single:
                return e[1] or ToUnicode('是')
            else:
                value += "%s,"%e[1]
    if value==',': value = ToUnicode('是')
    return value

def get_options_data(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single = True):
    if type==0 or type==None:
        return default
    L = get_options(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single)
    options =['',False]
    names = 'value label checked'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def get_options_data_search(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single,value_dict,para_cols):
    if type==0 or type==None:
        return default
    
    L = get_options_search(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single,value_dict,para_cols)
    options =['',False]
    names = 'value label checked tips'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def get_options_search(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single,value_dict,para_cols):
    L = []
    
    if type==26:   #材料
        sql="""select option_id,concat(number,'/',name),ifnull(size,'') from user_options o
               left join _m504_clgl m on m.id = o.option_id
               where option_id='%s'  and o.option_type='%s' order by o.ctime desc limit 1
            """%(default,type) 
    elif type == 3:
        sql = txt
        if sql=='':
            return L
        if para1 != '':
            sql = sql.replace("$s",str(para1),1)
        if para2 != '':
            sql = sql.replace("$s",str(para2),1)
        sql = sql.replace("{para1}",str(para1))
        sql = sql.replace("{para2}",str(para2))
        sql = sql.replace("{_self}",'')
        paras = para_cols.split(',')
        for e in paras: 
            if e =='': break
            sql = sql.replace("{%s}"%e,MySQLdb.escape_string(str(value_dict.get(e, ''))))
        
        if default != '':
            final_sql = sql.upper()
            import re
            final_sql = re.sub(r'\s+', ' ', final_sql)
            iPos = final_sql.find(',')
            final_sql = final_sql[:iPos]
            final_sql = final_sql.replace('SELECT ','')
            first_col = final_sql.replace('DISTINCT','')
            sql += " and %s = '%s'"%(first_col,default)
        sql += " limit 20"
    else:
        sql="""select option_id,option_value,option_tips from user_options where option_id='%s' and option_type='%s' order by ctime desc limit 1
             """%(default,type)
    print ToGBK(sql) 
    b = 1
    lT,iN=db.select(sql)
    for e in lT:
        txt=e[1]
        if str(e[0]) == str(default): b=1
        else:b=0
        L.append([e[0],txt,b,e[2]])
    return L

def get_options_data_level(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single = True):
    if type==0 or type==None:
        return default
    L = get_options_level(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single)
    options =['',False]
    names = 'value label checked parent_id disabled'.split()
    if L =='' or L == None:
        return []
    data = [dict(zip(names, d)) for d in L]
    options[0] = data
    options[1] = False
    names = 'options include_other_option'.split()
    L1 = dict(zip(names, options))
    return L1

def get_options(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single = True,view = False):
    if para1 == None: para1= 'NULL'
    if para2 == None: para2= 'NULL'
    if type==1:
        L = get_mtc_t_data1(default,txt,title,single)
    elif type==2:
        L = get_dept_data1(default,title,single)
    elif type==3:
        L = get_sql_data(usr_id,default,txt,para1,para2,title,single)
    elif type==4:
        L = get_roleslist(txt,default,pk,single)
    elif type==5:
        L = mUserRight(pk,pk,single)
    elif type==6:
        L = get_input_data(default,txt,title,single)
    elif type==7:
        L = get_gw_type_data1(default,title,single)
    elif type==10:
        L = get_all_tables(default,title,single)
    elif type==8:
        L = get_gw_type_data2(default,para1,title,single)
    elif type==9:
        L = get_first_flow_data(default,para1,title,single)
    elif type==11:
        L = get_use_tables(default,para1,title,single)
    elif type==12:
        L = get_table_field(default,para1,title,single)
    elif type==13:
        L = get_page_field(default,para1,title,single)
    elif type==14:
        L = get_col_field(default,para1,title,single)
    elif type==15:
        L = get_mtc_sys_data(default,txt,title,single)
    elif type==16:
        L = get_field_type(default,txt,title)
    elif type==17:
        L = get_form_tables(default,para1,title,single)
    elif type==18:
        L = get_flow_data(default,para1,para2,title,single)
    elif type==19:
        L = get_cw_data(menu_id,default,para1,para2,title,view)
    elif type==20:
        L = get_capital_info(menu_id,usr_id,default,para1,para2,title,view)
    elif type==21:
        L = get_proj_info(menu_id,usr_id,default,para1,para2,title,view)
    elif type==22:
        L = get_ht_info(menu_id,usr_id,default,para1,para2,title,view)
    elif type==23:
        L = get_sup_info(menu_id,usr_id,default,para1,para2,title,view)
    elif type==24:
        L = get_users_info(menu_id,usr_id,default,para1,para2,title,view)
    elif type==26:
        L = get_mat_info(menu_id,usr_id,default,para1,para2,title,view)
    else:
        return default
    return L

def get_options_level(menu_id,usr_id,pk,type,txt,title,default,para1,para2,single = True):
    if para1 == None: para1= 'NULL'
    if para2 == None: para2= 'NULL'
    L = []
    if type==2:
        L = get_dept_data(default,title,single)
    elif type==3:
        L = get_sql_data_level(usr_id,default,txt,para1,para2,title,single)
    elif type==19:
        L = get_cw_data(menu_id,default,para1,para2,title)

    return L

def get_capital_info(menu_id,usr_id,sDF,para1,para2,title=ToUnicode('--请选择--'),view = False):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    
    if usr_id=='':#资金帐号是根据授权用户提取的，因此，当usr_id为空时，应该返回空的列表
        return L
    
    if view==True:
        sql="""SELECT id,
                    concat(cname,'/',IFNULL(acct_name,''),'/',number),type FROM capital_manage 
                    where id='%s'
            """%(sDF)
    else:
        if menu_id != '230':
            sql="""SELECT id,
                    concat(cname,'/',IFNULL(acct_name,''),'/',number),type FROM capital_manage 
                    where (owner=%s or FIND_IN_SET(%s,right_users) or id='%s')
                """%(usr_id,usr_id,sDF)
        else:
            sql="""SELECT id,
                    concat(cname,'/',IFNULL(acct_name,''),'/',number),type FROM capital_manage 
                    where 1=1 
                """
        if menu_id in ['208','318']:
            sql1 = "select txt1 from mtc_t where type='SKFS' and id='%s'"%(para1)
        else:
            sql1 = "select txt1 from mtc_t where type='PAYC' and id='%s'"%(para1)
        print sql1
        lT1,iN1=db.select(sql1)
        if iN1>0: type_name = lT1[0][0]
        else:type_name=''
        if type_name in [ToUnicode('现金')]:#type为非空，取出指定类型的资金帐号，如:0、现金账，1、银行账
            sql+="AND type=0"
        elif type_name in [ToUnicode('支票'),ToUnicode('转账')]:#type为非空，取出指定类型的资金帐号，如:0、现金账，1、银行账
            sql+="AND type=1"
        else:
            sql+="AND type=2"
    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_sup_info(menu_id,usr_id,sDF,para1,para2,title=ToUnicode('--请选择--'),view = False):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    if view==True:
        sql="""select id,ifnull(cname,''),'','' from suppliers where id='%s'
            """%(sDF)
    else:
        sql="""select su.id,ifnull(su.cname,''),'',ifnull(u.qty,0)
from suppliers su
left join (select count(1) as qty,ab.sup_id from addr_book ab 
left join users_gy u on ab.id = u.addr_id
where u.status = 1
group by ab.sup_id) u on u.sup_id = su.id
where ifnull(su.status,0)!=-1  and  su.cname like '%%%s%%' order by su.id desc limit %s
            """%(sDF,20)

    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b,e[3]])
    return L

def get_users_info(menu_id,usr_id,sDF,para1,para2,title=ToUnicode('--请选择--'),view = False):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    if view==True:
        sql="""select usr_id,ifnull(usr_name,'') from users where usr_id='%s'
            """%(sDF)
    else:
        sql="""select usr_id,ifnull(usr_name,'') from users where ifnull(status,0) = 1  order by usr_name asc
            """
    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_mat_info(menu_id,usr_id,sDF,para1,para2,title=ToUnicode('--请选择--'),view = False):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    if view==True:
        sql="""select id,concat(number,'/',name) from _m504_clgl where id='%s'
            """%(sDF)
    else:
        sql="""select id,concat(number,'/',name,'(',ifnull(type,''),' ,',ifnull(size,''),')') from  `_m504_clgl`  where status != -1 and state = 1
            """
    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_proj_info(menu_id,usr_id,sDF,para1,para2,title=ToUnicode('--请选择--'),view = False):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
       
    if view==True:
        sql="""select id,concat('(',ifnull(gc_no,''),')',ifnull(cname,'')),0,0,m_id from out_proj where id='%s'
            """%(sDF)
    else:
        sql="""select id,concat('(',ifnull(gc_no,''),')',ifnull(cname,'')),0,0 from out_proj where ifnull(status,1)!=-1 order by id desc
            """
    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        if view==True:
            #txt = '<a href="commonDataTable.html?menu_id=302&tab=all&mode=view&pk=%s" target="_blank">%s</a>'%(e[4],e[1])
            txt = """<a href="#" onclick="javascript:window.open('commonWindow.html?menu_id=302&tab=all&mode=view&pk=%s','','width=1300, height= 800,top=100,left=100,toolbar=no, menubar=no, scrollbars=no, resizable=yes,location=no, status=no,alwaysRaised=yes,depended=yes')">%s</a>"""%(e[4],e[1])
        else:
            txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_proj_info_by_user(menu_id,usr_id,sDF,type,title=ToUnicode('--请选择--')):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
       
    sql="""select option_id,option_value,0,0 from user_options where usr_id='%s' and option_type=21 order by ctime desc limit 20
            """%(usr_id)
    print sql
    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_ht_info(menu_id,usr_id,sDF,para1,para2,title=ToUnicode('--请选择--'),view = False):
    sDF=str(sDF)
    
    if sDF!='':
        b=''
    else:
        b='1'
    if title!='':
        L=[['',title,'',b]]
    else:
        L=[]
    if para1 =='' or para1 == None:
        para1 = 'NULL'
    if view==True:
        sql="""select id,concat(ifnull(code,''),'/',ifnull(cname,'')) from contract_sg_file where id='%s'
            """%(sDF)
    else:
        sql="""select id,concat(ifnull(code,''),'/',ifnull(cname,'')) from contract_sg_file where proj_id=%s and status!=-1 order by itype
            """%(para1)
    print sql
    lT,iN=db.select(sql)
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_cw_data(menu_id,sDF,para1,para2,title='--请选择--',view = False):
    if view == True:
        sql_str = """
          SELECT cw.id                          
              ,concat(cw.code,'/',ifnull(cw1.cname,''),'-',cw.cname)              
              ,cw.p_id                        
              ,0                  
          FROM cw_sort cw 
          LEFT JOIN cw_sort cw1 ON cw.p_id=cw1.id
          where cw.id = '%s'
        """%(sDF)
    else:
        sql_str = """
          SELECT cw.id                          
              ,concat(cw.code,'/',ifnull(cw1.cname,''),'-',cw.cname)              
              ,cw.p_id                        
              ,ifnull(cw2.c,0) > 0                   
          FROM cw_sort cw 
          LEFT JOIN cw_sort cw1 ON cw.p_id=cw1.id
          LEFT join (select sum(1) as c,p_id from cw_sort group by p_id) cw2 on cw2.p_id = cw.id
          where cw.is_disable!=1 and cw1.is_disable!=1
        """
        if menu_id in ['207']:
            if str(para1) in ['0','2']:
                sql_str+=" AND cw.code LIKE 'B%' "
            elif str(para1) in ['1','3']:
                sql_str+=" AND cw.code LIKE 'A%' "
        elif menu_id in ['203']:
            if str(para1) in ['0']:
                sql_str+=" AND cw.code LIKE 'B%' "
            elif str(para1) in ['1']:
                sql_str+=" AND cw.code LIKE 'A%' "
            elif str(para1) in ['2']:
                sql_str+=" AND cw.code LIKE 'A%' "
        elif menu_id in ['300']:
            if str(para1) in ['1']:
                sql_str+=" AND cw.code LIKE 'A%' "
            elif str(para1) in ['2']:
                sql_str+=" AND cw.code LIKE 'B%' "
        elif menu_id in ['216']:
            sql_str+=" AND cw.code LIKE 'A%' "
        sql_str+=" ORDER BY cw.p_id,cw.sort ASC "
    print sql_str
    ldf=[]
    sDF=str(sDF)
    if not sDF is None and sDF != '':
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]

    lT,iN = db.select(sql_str)    
    for e in lT:
        if str(e[0]) in ldf:
            b = '1'
        else:b=''    
        txt=e[1]
        L.append([e[0],txt,b,e[2],e[3]])
    return L


def get_sql_data_level(usr_id,sDF,txt,para1,para2,title='--请选择--',single=True):
    ldf=[]
    sDF=str(sDF)
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b,'',0]]
    else:
        L=[]

    sql=txt
    if para1 != '':
        sql = sql.replace("$s",str(para1),1)
    if para2 != '':
        sql = sql.replace("$s",str(para2),1)
    sql = sql.replace("{para1}",str(para1))
    sql = sql.replace("{para2}",str(para2))
    sql = sql.replace("{_self}",str(sDF))
    sql = sql.replace("{_cid}",str(usr_id))

    sql = sql.replace("$s",'')
    if sql=='':
        return 
    #print sql
    lT,iN = db.select(sql)
    for e in lT:
        if single:
            if sDF==str(e[0]):b='1'
            else:b=''
        else:
            if str(e[0]) in ldf:
                b = '1'
            else:b=''    
        txt=e[1]
        L.append([e[0],txt,b,e[2],e[3]])
    return L

def mUserRight(user_id,pk,single=True):
    L=[]
    if user_id =='':user_id='NULL'
    sql="""SELECT nt.id,nt.cname,IFNULL(nr.user_id,0)
                from news_type nt
                left join news_right nr on nr.user_id=%s and nr.news_id=nt.id
                WHERE nt.news_group='info'
            """%(user_id)
    lT,iN = db.select(sql)
    if len(lT)>0:
        L=list(lT)
        for n in range(len(L)):
            L[n]=list(L[n])
            L[n][1] = L[n][1]
            if pk=='':
                if str(L[n][0]) not in ('34','44'):
                    L[n][2]=1
    return L

def get_input_data(sDF,txt,title='',single=True):
    ldf=[]
    #print "sDF=%s txt=%s"%(sDF,ToGBK(txt))
    sDF=str(sDF)
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    if txt=='':
        txt = "1,"
    lT = txt.split('|')
    for e in lT: 
        e1 = e.split(',')
        #print e1
        if single:
            if sDF==str(e1[0]):b='1'
            else:b=''
        else:
            if str(e1[0]) in ldf:
                b = '1'
            else:b=''    
        txt=e1[1]
        L.append([e1[0],txt,b])
    return L

def get_sql_data(usr_id,sDF,txt,para1,para2,title='--请选择--',single=True): 
    ldf=[]
    sDF=str(sDF)
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]

    sql=txt
    if para1 != '':
        sql = sql.replace("$s",str(para1),1)
    if para2 != '':
        sql = sql.replace("$s",str(para2),1)
    sql = sql.replace("{para1}",str(para1))
    sql = sql.replace("{para2}",str(para2))
    sql = sql.replace("{_self}",str(sDF))
    sql = sql.replace("{_cid}",str(usr_id))
    if sql=='':
        return 
    sql = sql.replace("$s",'NULL')
   
    print "usr_id = %s"%usr_id
    print sql
    #print "sDF = %s"%sDF
    try:
        lT,iN = db.select(sql)
    except:
        lT = []
    for e in lT:
        if single:
            if sDF.upper()==str(e[0]).upper():b='1'
            else:b=''
        else:
            if str(e[0]) in ldf:
                b = '1'
            else:b=''    
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_mtc_t_data1(sDF,type,title='--请选择--',single=True):
    ldf=[]
    sDF=str(sDF)
    if not sDF is None and sDF != '' and single==False:
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = str(ldf[i])
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]

    sql="SELECT id,txt1 FROM mtc_t WHERE type='%s' order by sort" %type
    #print sql
    lT,iN = db.select(sql)

    for e in lT:
        if single:
            if sDF==str(e[0]):b='1'
            else:b=''
        else:
            if str(e[0]) in ldf:
                b = '1'
            else:b=''    
        txt=e[1]
        L.append([e[0],txt,b])
    return L

def get_roleslist(dept,sDF,pk,single=True):
    L=[]
    ldf=[]
    if pk!='':
        sql = "select role_id from usr_role where usr_id=%s"%pk
        print sql
        lT,iN = db.select(sql)
        for e in lT:
            ldf.append(e[0])
    elif not sDF is None and sDF != '':
        ldf=sDF.split(',')
        for i in range(0,len(ldf)):
            ldf[i] = int(ldf[i])
    
    sql="""select rl.role_id,rl.role_name,''
            from roles rl
            left join dept dp on dp.id = rl.dept_id
            where dp.del_flag = 0
        """
    if dept == '':
        sql+=" and dp.parent_id = 0"
    else:
        sql+=" and dp.id=%s"%dept
        
    sql+=" order by rl.dept_id,rl.role_id"
    lT,iN = db.select(sql)
    if len(lT)>0:
        L=list(lT)
        for n in range(len(L)):
            L[n]=list(L[n])
            L[n][1] = L[n][1]
            if L[n][0] in ldf:
                L[n][2]=1
    return L

def get_dept_data1(sDF,title='--请选择--',single=True):
    sql="SELECT id,cname,'',ifnull(ilevel,0) FROM dept where id!=1 and del_flag = 0 order by sort" 
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        iLevel = int(e[3]) - 1
        txt= "---"*iLevel +e[1]
        L.append([e[0],txt,b])
    return L

def get_menu_list(sDF,title='--请选择--',single=True):
    sql="SELECT menu_id,menu_name FROM menu_func where menu=1 order by sort" 
    lT,iN = db.select(sql)
    sDF=str(sDF)
    if sDF=='':b='1'
    else:b=''
    if title!='':
        L=[['',title,b]]
    else:
        L=[]
    for e in lT:
        if sDF==str(e[0]):b='1'
        else:b=''
        txt= e[1]
        L.append([e[0],txt,b])
    return L
