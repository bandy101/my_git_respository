# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os,time
import json
import urllib
from HW_DB   import DataBaseParent_local
#本地mysql数据库
db=DataBaseParent_local()  
# uc=unicode(str('s'), 'eucgb2312_cn')
sys.path.append("/home/webroot/oWorld")
from common.HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG
#微信企业号变量
m_sCorpID = "wxc6d740ece61b7ec1"
m_sAgentId_lw = "1000002"
m_sCorpSecret_lw = "xNntgqKZxJmpZWmHJWNL6ev4u2ylp7BjwJS1VUQ9tgM"
host_url = 'http://lw.szby.cn'

def pushDeal():
    sql="""SELECT 
        CD.id
        ,CD.ctime
        ,IFNULL(UNIX_TIMESTAMP(CF.ctime),0)
        ,IFNULL(UNIX_TIMESTAMP(PA.ctime),0)
        ,IFNULL(CD.status,'')
        ,IFNULL(PA.situation,0)   #5
        ,CF.cid
        ,IFNULL(CD.level,0)
        ,IFNULL(IFNULL(DP.id,DP1.id),0)
        ,U.login_id
        FROM complaint_detail CD
        LEFT JOIN (select * from (select * from complaint_flow order by ctime desc) tem group by m_id order by ctime desc) CF ON CF.m_id = CD.id 
        LEFT JOIN (select * from (select * from message_push_auto order by ctime desc) tem group by m_id order by ctime desc) PA ON PA.m_id = CD.id
        LEFT JOIN labour_contract LC ON LC.id = CD.lc_id
        LEFT JOIN out_proj OP ON OP.id = LC.proj_id
        LEFT JOIN proj_tran_info TI ON TI.proj_id = OP.id
        LEFT JOIN dept DP ON DP.id = TI.tran_to_dpid
        LEFT JOIN assess_affirm AA ON AA.id = CD.aa_id
        LEFT JOIN out_proj OP1 ON OP1.id = AA.proj_id
        LEFT JOIN proj_tran_info TI1 ON TI1.proj_id = OP1.id
        LEFT JOIN dept DP1 ON DP1.id = TI1.tran_to_dpid
        LEFT JOIN users U ON U.usr_id = CF.cid
        WHERE (IFNULL(CD.status,'') ='' or CD.status=-1 or CD.status=0) 
        AND UNIX_TIMESTAMP()-CD.ctime>86400 
        AND UNIX_TIMESTAMP()-IFNULL(UNIX_TIMESTAMP(CF.ctime),0)>86400
        AND UNIX_TIMESTAMP()-IFNULL(UNIX_TIMESTAMP(PA.ctime),0)>86400
        AND (((IFNULL(CD.status,'')='' OR IFNULL(CD.status,'')=-1) AND IFNULL(PA.situation,0)<4) 
            OR (IFNULL(CD.status,'')=0 AND IFNULL(PA.situation,0)>4 AND IFNULL(PA.situation,0)<9))
        """
    rows,iN = db.select(sql)
    for e in rows:
        pk = e[0]
        ctime = e[1] #投诉创建时间
        ftime = e[2] #当前流程时间
        ptime = e[3] #最新推送时间
        status = str(e[4]) #当前流程节点
        situation = e[5] #推送节点
        c_usr_id = e[6] #当前领导id
        level = int(e[7]) #当前领导层级
        dept = e[8] #部门ID
        leader_login_id = e[9] #交办领导login_id
        leader = getLeader(dept)
        leader_id=0
        if status =='' or status =='-1':
            if situation==0:
                if level<3:
                    leader_id = leader[level][0]
                    leader_usr_id = leader[level][1]
                    situation_now = 1
                    if leader_id==0 and level==1:
                        leader_id = leader[level+1][0]
                        leader_usr_id = leader[level][1]
                        situation_now = 2
                    mWxPushMsg_Leader(pk,situation_now,leader_usr_id,'leader')
                else:
                    # leader_id =999
                    mWxPushMsg_Leader(pk,3,0,'sj')
            if situation ==1:
                if level<3:
                    leader_id = leader[2][0]
                    leader_usr_id = leader[2][1]
                    situation_now = 2
                    mWxPushMsg_Leader(pk,situation_now,leader_usr_id,'leader')
                else:
                    # leader_id =999
                    mWxPushMsg_Leader(pk,3,0,'sj')
            if situation == 2:
                mWxPushMsg_Leader(pk,3,0,'sj')
            if situation == 3:
                mWxPushMsg_Leader(pk,4,0,'jsz')
            # print leader_id
        if status == '0':
            if situation<5:
                situation_now = 4+level
                mWxPushMsg_Leader(pk,situation_now,leader_login_id,'leader')
            if situation==5:
                leader_id = leader[level][0]
                leader_usr_id = leader[level][1]
                situation_now = 6
                if leader_id==0 and level==1:
                    leader_id = leader[level+1][0]
                    leader_usr_id = leader[level][1]
                    situation_now = 7
                mWxPushMsg_Leader(pk,situation_now,leader_usr_id,'leader')
            if situation==6:
                leader_id = leader[2][0]
                leader_usr_id = leader[2][1]
                situation_now = 7
                mWxPushMsg_Leader(pk,situation_now,leader_usr_id,'leader')
            if situation==7:
                mWxPushMsg_Leader(pk,8,0,'sj')
            if situation==8:
                mWxPushMsg_Leader(pk,9,0,'jsz')
            # print leader_id 

import httplib
#通知领导
def mWxPushMsg_Leader(pk,situation,leader_login_id,ptype):
    L =Get_data(pk)
    if ptype =='leader':
    	toUser = leader_login_id
    elif ptype =='sj':
    	toUser = getSJ()
    elif ptype =='jsz':
    	toUser = getJSZ()
    else:
    	return 'error'
    # toUser = 'liujq'
    print ptype
    sToken =  read_access_token_lw()
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_lw)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_lw(body)
    file_id=L[0]
    proj_name = L[2]
    cusrname = L[1]
    complaintObject = L[3]
    sUrl='%s/complaint/login/login_qy?fid=complainDetail&seq=%s&must_reply=true'%(host_url,file_id)
    stitle ="""超期提醒"""
    description = """【%s】发起了针对“%s”关于“%s”的劳务投诉，超期未办理，请及时查阅介入。"""%(cusrname,complaintObject,proj_name)
    surl = my_urlencode(sUrl)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)

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

    """%(m_sAgentId_lw,stitle,url,description)
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
    # print errcode 
    errcode = 0

    toUser1 = toUser.replace('|',"','")
    toUser1 = "('" + toUser1 + "')" 
    sql = "select GROUP_CONCAT(usr_name) from users where login_id in %s"%toUser1
    rows1,iN1 = db.select(sql)
    if iN1> 0:
        to_user_name = rows1[0][0]
    else:
        to_user_name = ''

    if str(errcode) == '0':
        sql="""INSERT INTO message_push_auto(m_id,ctime,situation,to_users,errcode,to_user_name)
            VALUES(%s,now(),%s,'%s',0,'%s') 
            """%(pk,situation,toUser,to_user_name)
        db.executesql(sql)
    else:
        errmsg = ddata.get('errmsg','')        
        sql="""INSERT INTO message_push_auto(m_id,ctime,situation,to_users,errcode,errmsg,to_user_name)
            VALUES(%s,now(),%s,'%s',%s,'%s','%s') 
            """%(pk,situation,toUser,errcode,errmsg,to_user_name)
        db.executesql(sql)
    return errcode

def mWxPushMsg_SJ(pk,situation):
    return '通知审计'

def mWxPushMsg_JSZ(pk,situation):
    return '通知监事长'

def getLeader(dept):
    sql="""SELECT IFNULL(U.usr_id,0),U.login_id,DP.id,CONCAT(DP.cname,'第一负责人'),1
           FROM dept DP
           LEFT JOIN users U ON DP.header = U.usr_id
           WHERE DP.id = %s
           UNION ALL
           SELECT IFNULL(U.usr_id,0),U.login_id,DP.id,CONCAT(DP.cname,'分管领导'),2
           FROM dept DP
           LEFT JOIN users U ON DP.sub_director = U.usr_id
           WHERE DP.id = %s
           UNION ALL
           SELECT IFNULL(U.usr_id,0),U.login_id,DP.id,CONCAT(DP.cname,'领导'),3
           FROM dept DP
           LEFT JOIN users U ON DP.header = U.usr_id
           WHERE DP.id = 37
        """%(dept,dept)
    # print sql
    rows,iN=db.select(sql)
    return rows

def Get_data(pk):
    L=[]
    sql="""SELECT CD.id,UX.usr_name,IFNULL(OP.cname,OP1.cname),CD.complaintObject
        FROM complaint_detail CD 
        LEFT JOIN users_wx UX ON UX.usr_id = CD.cid
        LEFT JOIN labour_contract LC ON LC.id = CD.lc_id
        LEFT JOIN out_proj OP ON OP.id = LC.proj_id
        LEFT JOIN assess_affirm AA ON AA.id = CD.aa_id
        LEFT JOIN out_proj OP1 ON OP1.id = AA.proj_id
        WHERE CD.id = %s
        """%(pk)
    rows,iN = db.select(sql)
    # L=list(rows[0])
    L=rows[0]
    return L

def getSJ():
    toUser=''
    sql="""SELECT IFNULL(U.login_id,'') ,U.usr_name
        FROM users U
        WHERE U.dept_id =175 and U.status=1 
        """
    rows,iN = db.select(sql)
    for e in rows:
        toUser+='%s|'%(e[0])
    return toUser

def getJSZ():
    toUser=''
    sql="""SELECT IFNULL(U.login_id,'')
               FROM dept DP
               LEFT JOIN users U ON DP.header = U.usr_id
               WHERE DP.id = 76
            """
    rows,iN=db.select(sql)
    toUser=rows[0][0]
    return toUser

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

def my_urlencode(str) :
    str = urllib.quote(str)
    str = str.replace('/', '%2F')
    return str

def pushDealResult():
    sql="""SELECT CD.id,IFNULL(PA.situation,0),UNIX_TIMESTAMP(),IFNULL(UNIX_TIMESTAMP(CF.ctime),0)
        FROM complaint_detail CD
        LEFT JOIN (select * from (select * from complaint_flow order by id desc) tem group by m_id order by id desc) CF ON CF.m_id = CD.id 
        LEFT JOIN (select * from (select * from message_push_auto order by id desc) tem group by m_id order by id desc) PA ON PA.m_id = CD.id
        WHERE CD.status=1 AND (((UNIX_TIMESTAMP()-UNIX_TIMESTAMP(CF.ctime))>CF.dealDays*86400 AND IFNULL(PA.situation,0)<10) OR
        (UNIX_TIMESTAMP()-IFNULL(UNIX_TIMESTAMP(PA.ctime),0)>86400 AND IFNULL(PA.situation,0)=10))
    """
    rows,iN=db.select(sql)
    if iN>0:
        for e in rows:
            pk = e[0]
            situation = e[1]
            if situation<10:
                mWxPushMsg_Leader(pk,10,0,'sj')
            else:
                mWxPushMsg_Leader(pk,11,0,'jsz')
if __name__ == "__main__":
    print 'Push start.......'
    pushDeal()  #受理前
    pushDealResult()   #受理后提交前

