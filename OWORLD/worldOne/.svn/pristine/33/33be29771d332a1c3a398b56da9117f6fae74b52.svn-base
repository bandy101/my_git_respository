#coding:utf-8
import os,sys,traceback
import time
import urllib
from HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG
from HW_DB_TOOL   import DataBaseParent
from django.http import HttpResponse
import json
from datetime import date, datetime 
import decimal

#限制用 "from XXXX import *" 时可以导入的名字
__all__ = ['CLIENT_NAME','WEBSITE_PATH','AppId','m_sCorpID',
           'db','dActiveUser','host_url','my_urlencode','ToGBK','fs_url',
           'TIME_OUT','get_YES_NO_data','template_id_msg','template_id_result',
           'HttpResponseCORS','EncodingAESKey','Token','AppSecret','imgUrl',
           'write_access_token','read_access_token','checkSession','write_access_token_lw','read_access_token_lw',
           'm_sToken_lw','m_sEncodingAESKey_lw','m_sAgentId_lw','m_sCorpSecret_lw',
           'AppId_tj','Token_tj','EncodingAESKey_tj','AppSecret_tj','write_access_token_common','read_access_token_common',
           'm_sToken_tj','m_sEncodingAESKey_tj','m_sAgentId_tj','m_sCorpSecret_tj','template_id_msg_tj',
           'AppId_gy','Token_gy','EncodingAESKey_gy','AppSecret_gy','template_id_msg_gy','template_id_result_gy',
           'm_sToken_gy','m_sEncodingAESKey_gy','m_sAgentId_gy','m_sCorpSecret_gy'
           ]

#获取客户名
CLIENT_NAME      = __name__.split('.')[0]

#公共的常数，和一些共享的变量
WEBSITE_PATH=os.path.join('/home/webroot/',CLIENT_NAME)
dActiveUser={}        
data_url = "https://lw.szby.cn/complaint"
fs_url = "https://lw.szby.cn/fs"
imgUrl = "https://ww.szby.cn/fs/user_pic/"
# m_dbname = 'schedule'

#劳务服务号
AppId = 'wxec7aef65a74af367'   #APPID
Token = 'HIvEmG8dVTIIJR6220E'
EncodingAESKey = 'I7RMkwauatKQXUBFRmpCkuwwIAEOdJv1GW1UOKMwSIP'
AppSecret = '1ceffffb488d0f7f59e21c39c6afccc1'
template_id_msg = "NxtLcnJl08uw2PA4PzMZd5u2RMo0ob0C6FaOKed4y9c"
template_id_result = "pr2mVGFExjsqtXxYD5dlqMuiqoMEq7ACeG1_AGpThAM"
#项目推荐人服务号
AppId_tj = 'wx88c1d3c813d448dc'
Token_tj = 'HIvEmG8dVTIIJR6220T'
EncodingAESKey_tj = 'o4pHidRQdihjq7W8JhOmFBSQAFmLbpq1ouJZpcsoHxB'
AppSecret_tj = 'a33a6924ec99e7129efd7a69cf7611f5'
template_id_msg_tj = "iI6VBtxMz3Jt_CgkLH0OKenZYnxBLJDnF8pu3UeJpVQ"
#供应商服务号
AppId_gy = 'wxe703baaad2a1c9dc'
Token_gy = 'Fgfdg1F_W45Ed155w7wrfw'
EncodingAESKey_gy = 'MOTN3tKdlg8rTbcYtK32MW6IK9QG4oQbZH5ZzQUQSk6'
AppSecret_gy = '780065948cba96c5831c6b047a0ff7f8'
template_id_msg_gy = "7J5iK9tBv3xqwjHRo6r9j6Baq_VOPuxqDDbJPoACK5w"
template_id_result_gy = "NwwwjuHfSg1mOvN1oHObizd8VjllYy1Yh9lYOkia5Uk"
#微信企业号变量
m_sCorpID = "wxc6d740ece61b7ec1"
m_sCorpSecret = "DjsBjwM238hFgm2C9Ve1N0w4vHrlXhInkj8H3CgOkFZRQ3FtdPxcVvjPjZ2ImRzx"

m_sToken_lw = "3enQoTh5kMF6F9g0"
m_sEncodingAESKey_lw = "lixO6FnyXshfPlrFnRzvRMlrBoSOw0QXwmUw8uXC3vI"
m_sAgentId_lw = "1000002"
m_sCorpSecret_lw = "xNntgqKZxJmpZWmHJWNL6ev4u2ylp7BjwJS1VUQ9tgM"

m_sToken_tj = "mD1kOzolrifgnFa1QNC8HyCu"
m_sEncodingAESKey_tj = "w4rhV2Yrcnrjh32jckLlQjwlPNrm9tjySgxOOx1OBaK"
m_sAgentId_tj = "1000003"
m_sCorpSecret_tj = "FKbnh6Q6Q47tiwiJMtdDFxuKtprGabsfyw8J00Mg_2Q"
#供应商
m_sToken_gy = "I49cOVAW4A9v3yuQ6hLM7YUWS"
m_sEncodingAESKey_gy = "NEdgCMvdz3F7xPoQSWcPWztHbUoqJ6zMx4fqoCCJ1UP"
m_sAgentId_gy = "1000004"
m_sCorpSecret_gy = "-dPOYV8jdk68lgtpmN6YZSHNcncyYamtFsmH8jeeTVY"

host_url = 'https://lw.szby.cn'
#配置失效时间为半个小时
TIME_OUT = 30 
try:
    db=DataBaseParent()     #关系数据库
except:
    raise Exception('db connect error')
    # print 'db connect error'

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
m_corp_name = ToUnicode('中建南方')

def ToGBK(s):
    try:
        s=str(s.decode("utf-8").encode("GBK"))
    except:
        s=s
    s = s.replace("\n","\r\n")
    return s

def my_urlencode(str) :
    str = urllib.quote(str)
    str = str.replace('/', '%2F')
    return str

def checkSession(request):
    usr_id = request.session.get('usr_id','')
    if usr_id =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)

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

#劳务服务号
def write_access_token(access_token):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token')
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token():
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token')
    access_token = openTXT(log_file)
    if access_token=='':
        return ''

    ddata=json.loads(access_token)
    token =  ddata['access_token'] 
    if  token !='' :  
        t1 = ddata['time'] 
        t=time.time() 
        if (t - t1)<7000:
            return token
    return ''

#劳务企业号
def write_access_token_lw(access_token):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token_lw')
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token_lw():
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token_lw')
    access_token = openTXT(log_file)
    if access_token=='':
        return ''

    ddata=json.loads(access_token)
    token =  ddata['access_token'] 
    if  token !='' :  
        t1 = ddata['time'] 
        t=time.time() 
        if (t - t1)<7000:
            return token
    return ''

#access_token_tj_qy 推荐人企业号
##access_token_tj 推荐人服务号
def write_access_token_common(access_token,itype):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/%s'%itype)
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token_common(itype):
    log_file=os.path.join('/home/webroot/oWorld/complaint/%s'%itype)
    access_token = openTXT(log_file)
    if access_token=='':
        return ''

    ddata=json.loads(access_token)
    token =  ddata['access_token'] 
    if  token !='' :  
        t1 = ddata['time'] 
        t=time.time() 
        if (t - t1)<7000:
            return token
    return ''

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

def mValidateUser(request,mode,menu_id):
    """功能：验证用户是否有访问当前功能的权限"""
    usr_id = request.session.get('usr_id', 0)
    AccessToken = request.POST.get('AccessToken', '')
    import base64,time
    token = base64.b64decode(AccessToken)
    d_value = ['']*10
    login_id = token.split(' ')[0]
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
    if menu_id!='':
        sql = """select u.usr_id,u.usr_name,d.id,d.cname,md.gw_type2,time_to_sec(timediff(now(),u.refresh_time)),u.expire_time,u.id,u.source
                    from (select u.usr_id,u.usr_name,u.dept_id,ul.refresh_time,ul.expire_time,ul.id,ul.source  from users_login ul left join users u on u.usr_id=ul.usr_id where u.login_id='%s'  and token='%s' order by ul.login_time desc limit 1) U
                    left join dept d on d.id=u.dept_id
                    left join usr_role ur on ur.usr_id=u.usr_id
                    left join role_menu rm on rm.role_id = ur.role_id and rm.menu_id=%s
                    left join menu_data_source md on md.menu_id=rm.menu_id
                    """%(login_id,AccessToken,menu_id)
        if usr_id not in [1,2]:
            sql += " where rm.can_view = 1 "
    else:
        sql = """select u.usr_id,u.usr_name,d.id,d.cname,0,time_to_sec(timediff(now(),u.refresh_time)),u.expire_time,u.id,u.source
                    from (select u.usr_id,u.usr_name,u.dept_id,ul.refresh_time,ul.expire_time,ul.id,ul.source  from users_login ul left join users u on u.usr_id=ul.usr_id where u.login_id='%s'  and token='%s' order by ul.login_time desc limit 1) U
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
        origin = "http://lw.szby.cn"

    response["Access-Control-Allow-Origin"] = "%s"%(origin)
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def HttpResponseJsonCORS(s):
    response = HttpResponse(s,content_type="application/json")
    try:
        origin = request.META['HTTP_ORIGIN']  
    except:
        origin = "http://lw.szby.cn"
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

import pymssql
class DataBaseParent:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.cursor="Initial Status"
        try:
            self.db = pymssql.connect(host=self.host, user=self.user, password=self.password,database=self.database) #主系统
            self.cursor=self.db.cursor()
        except:
            pass
        if self.cursor=="Initial Status":
            raise Exception("Can't connect to Database server!")

    def select(self,sqlstr):
        cur=self.db.cursor()
        try:
            cur.execute(sqlstr)
        except:
            self.db.close()
            self.db = pymssql.connect(host=self.host, user=self.user, password=self.password,database=self.database) #主系统
            cur=self.db.cursor()
            cur.execute(sqlstr)
        List=cur.fetchall()
        iTotal_length=len(List)
        self.description=cur.description
        cur.close()
        return List,iTotal_length

    def select_include_name(self,sqlstr):
        #选择结果包含List,iTotal_length,lFieldName
        #return list(self.select(sqlstr))+[self.description]
        cur=self.db.cursor()
        try:
            cur.execute(sqlstr)
        except:
            self.db.close()
            self.db = pymssql.connect(host=self.host, user=self.user, password=self.password,database=self.database) #主系统
            cur=self.db.cursor()
            cur.execute(sqlstr)
 
        index = cur.description
        List=cur.fetchall()
        iTotal_length=len(List)
        result = []
        for res in List:
            row = {}
            for i in range(len(index)-1):
                row[index[i][0]] = res[i]
            result.append(row)
        cur.close()
        return result,iTotal_length

    def select_for_grid(self,sqlstr,pageNo=1,select_size=10):
        List,iTotal_length=self.select(sqlstr)
        if iTotal_length%select_size==0:
            iTotal_Page=iTotal_length/select_size
        else:
            iTotal_Page=iTotal_length/select_size+1

        start,end=(pageNo-1)*select_size,pageNo*select_size
        if end>=iTotal_length:end=iTotal_length        
        if iTotal_length==0 or start>iTotal_length or start<0:
            return [],iTotal_length,iTotal_Page,pageNo,select_size
        
        return List[start:end],iTotal_length,iTotal_Page,pageNo,select_size

    def executesql(self,sqlstr):
        cur=self.db.cursor()
        try:
            r = cur.execute(sqlstr)
        except:
            cur.close()        
            self.db.close()
            self.db = pymssql.connect(host=self.host, user=self.user, password=self.password,database=self.database) #主系统
            cur=self.db.cursor()
            r = cur.execute(sqlstr)
        self.db.commit()
        cur.close()        
        return r

    def release(self):
        self.db.close()
        return 0

byaq = DataBaseParent('59.38.126.90:7668', 'lw_sync', 'BYgf_%%_2047','byaq')
byerp = DataBaseParent('124.172.117.12:8666', 'liyafeng', '1331699mbn@','byerp')
print "DataBaseParent_byerp"
#byerp_bk = DataBaseParent('120.25.166.24', 'byerp_test', '2wsx4rfv','byerp_test')
#print "DataBaseParent_byerp_bk"
