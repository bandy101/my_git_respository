# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,AppId_tj,AppSecret_tj,AppId,AppSecret,m_sCorpSecret,my_urlencode,m_sCorpSecret_tj'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,m_sCorpSecret_lw,m_sCorpID,read_access_token_lw,write_access_token_lw,read_access_token_common,write_access_token_common'%prj_name)
exec ('from %s.share        import AppId_gy,AppSecret_gy,m_sCorpSecret_gy'%prj_name)  
import httplib
import sys  
import os
import time
import json
from django.http import HttpResponseRedirect,HttpResponse

###企业微信入口
def login_qy(request):
    fid = request.GET.get('fid','')
    code = request.GET.get('code','')
    state = request.GET.get('state',1)
    seq = request.GET.get('seq','')
    pk = request.GET.get('pk','')
    path = request.GET.get('path','')
    typeId = request.GET.get('typeId','')
    must_reply = request.GET.get('must_reply','')
    func_id = request.GET.get('func_id','')
    Secret=m_sCorpSecret
    projType='lw'
    if str(func_id)=='1000002':
        Secret=m_sCorpSecret_lw
        projType='lw'
    if str(func_id)=='1000003':
        Secret=m_sCorpSecret_tj
        fid='proj_refer/'+fid
        projType='tj'
    if str(func_id)=='1000004':
        Secret=m_sCorpSecret_gy
        projType='gy'
    # Secret=m_sCorpSecret
    # print Secret
    # type=''
    # if len(state)>1:
    #     type = state
    #     state = 1
    # if request.cookies.has_key('wx_usr_id'):  
    if request.session.get('usr_id_qy','') !='':
        userid = request.session['usr_id_qy']
        request.session['usr_id_qy'] = userid
        if fid !='':
            if fid == 'mtConfirmDetail':
                url='/lwerp/VenderCenter/dist/mtConfirmDetail.html?type=qy&projType=gy&menu_id=3000001&tab=my&mode=view&pk=%s'%(seq)
            elif fid == 'shd':
                url='/lwerp/VenderCenter/dist/addRKOrder.html?type=qy&projType=gy&menu_id=3000004&tab=my&mode=view&pk=%s'%(pk)
            elif fid == 'cgList_qy':
                url='/lwerp/VenderCenter/dist/cgList_qy.html?type=qy&projType=gy&menu_id=1501'
            elif fid == 'materialRkList':
                url='/lwerp/VenderCenter/dist/materialRkList.html?type=qy&projType=gy'
            elif fid == 'mtAuditList':
                url='/lwerp/VenderCenter/dist/mtAuditList.html?type=qy&projType=gy'
            elif fid == 'mtCheckList':
                url='/lwerp/VenderCenter/dist/mtCheckList.html?type=qy&projType=gy'
            elif fid == 'mtCheckDetail':
                url='/lwerp/VenderCenter/dist/mtCheckDetail.html?type=qy&projType=gy&pk=%s'%(seq)
            elif path == '':
                url='/lwerp/lw/src/html/%s.html?id=%s&type=qy&projType=%s'%(fid,state,projType)
                if seq!='':
                    url += '&xyId=%s'%(seq)
            elif path == 'material':
                type = request.GET.get('type','')
                url='/lwerp/lw/src/html/%s/%s.html?type=%s'%(path,fid,type)
                if seq!='':
                    url += '&id=%s'%(seq)
            else:
                url='/lwerp/lw/src/html/%s/%s.html?type=qy&projType=%s'%(path,fid,projType)
                if seq!='':
                    url += '&id=%s'%(seq)
                    url += '&xyId=%s'%(seq)
            return HttpResponseRedirect(url)
        else:
            return HttpResponseCORS(request,'1')
        
    if code!='':
        # return HttpResponseCORS(typeId)
        sToken =  ''
        if str(func_id)=='1000002':
            sToken =  read_access_token_lw()
        if str(func_id)=='1000003':
            sToken =  read_access_token_common('access_token_tj_qy')
        if str(func_id)=='1000004':
            sToken =  read_access_token_common('access_token_gy_qy')
        if sToken == '':
            conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
            url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,Secret)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            # print ddata
            sToken = ddata['access_token'] 
            conn.close()  
            
            if str(func_id)=='1000002':
                write_access_token_lw(body)
            if str(func_id)=='1000003':
                write_access_token_common(body,'access_token_tj_qy')
            if str(func_id)=='1000004':
                write_access_token_common(body,'access_token_gy_qy')
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/user/getuserinfo?access_token=%s&code=%s"%(sToken,code)
        conn.request('GET', '%s'%url)  
        #write_log(url)
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        # print ddata
        try:
            uName = ddata['UserId'] 
        except Exception, e:
            return HttpResponseCORS(request,'3')
            # return HttpResponseRedirect('/static/src/html/error.html')
        #uName='lishijie'
        rows,iN = db.select("select usr_id,usr_name,dept_id from users where login_id='%s' and status=1"%uName)
        #print rows
        if len(rows)==0:
            return HttpResponseCORS(request,'4')
            # return HttpResponseRedirect('/static/scr/html/error.html')
        else:
            userid=rows[0][0]
            # response.cookies['wx_usr_id']=userid
            response = HttpResponse()
            response.set_cookie('wx_usr_id', userid)
            request.session['usr_id_qy'] = userid
            request.session['usr_name'] = rows[0][1]
            request.session['dept_id'] = rows[0][2]
            # return HttpResponseCORS(userid)
            # session.usr_id = userid
            # session.usr_name = rows[0].usr_name
            # session.dept_id = rows[0].dept_id
        conn.close()   
    else:    #重定向以获取用户信息
        redirect_uri = request.get_full_path()
        redirect_uri = "https://lw.szby.cn" + redirect_uri
        redirect_uri = my_urlencode(redirect_uri)
        print redirect_uri
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo#wechat_redirect"%(m_sCorpID,redirect_uri)
        return HttpResponseRedirect(url)

    if fid !='':
        if fid == 'mtConfirmDetail':
            url='/lwerp/VenderCenter/dist/mtConfirmDetail.html?type=qy&projType=gy&menu_id=3000001&tab=my&mode=view&pk=%s'%(seq)
        elif fid == 'shd':
            url='/lwerp/VenderCenter/dist/addRKOrder.html?type=qy&projType=gy&menu_id=3000004&tab=my&mode=view&pk=%s'%(pk)
        elif fid == 'cgList_qy':
            url='/lwerp/VenderCenter/dist/cgList_qy.html?type=qy&projType=gy&menu_id=1501'
        elif fid == 'materialRkList':
            url='/lwerp/VenderCenter/dist/materialRkList.html?type=qy&projType=gy'
        elif fid == 'mtAuditList':
            url='/lwerp/VenderCenter/dist/mtAuditList.html?type=qy&projType=gy'
        elif fid == 'mtCheckList':
            url='/lwerp/VenderCenter/dist/mtCheckList.html?type=qy&projType=gy'
        elif fid == 'mtCheckDetail':
            url='/lwerp/VenderCenter/dist/mtCheckDetail.html?type=qy&projType=gy&pk=%s'%(seq)
        elif path == '':
            url='/lwerp/lw/src/html/%s.html?id=%s&type=qy&projType=%s'%(fid,state,projType)
            if seq!='':
                url += '&xyId=%s'%(seq)
        elif path == 'material':
            type = request.GET.get('type','')
            url='/lwerp/lw/src/html/%s/%s.html?type=%s'%(path,fid,type)
            if seq!='':
                url += '&id=%s'%(seq)
        else:
            url='/lwerp/lw/src/html/%s/%s.html?type=qy'%(path,fid)
            if seq!='':
                url += '&id=%s'%(seq)
        return HttpResponseRedirect(url)
    else:
        return HttpResponseCORS(request,'1')

#劳务反映服务号入口
def index(request):
    fid = request.GET.get('fid','')
    code = request.GET.get('code','')
    state = request.GET.get('state',0)
    seq = request.GET.get('seq','')
    pk = request.GET.get('pk','')
    typeId = request.GET.get('typeId','')
    must_reply = request.GET.get('must_reply','')
    usr_id = request.session.get('usr_id','')
    t=time.time()
    date_ary=time.localtime(t)
    y=time.strftime("%Y-%m-%d %T",date_ary)    
    start_time = time.strptime("2019-01-26 18:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = time.strptime("2019-02-20 08:00:00", "%Y-%m-%d %H:%M:%S")

    if usr_id !='':
        rows,iN = db.select("select usr_id,ifnull(is_labor,0) from users_wx where usr_id='%s' and status=1 and ifnull(is_labor,0)=0"%usr_id)
        if iN ==0:
            if fid =='infoList' :
                url='/lwerp/lw/src/html/infoList.html?type=fw' 
            elif fid =='infoDetail':
                url='/lwerp/lw/src/html/infoDetail.html?type=fw'
            else: 
                # HttpResponseRedirect('/lwerp/lw/src/html/bindInfo.html')
                url='/lwerp/lw/src/html/bindInfo.html?itype=lw'
        else:
            if fid=='list' and iN >0:
                url='/lwerp/lw/src/html/complainLIst.html?type=fw'
                # return HttpResponseRedirect('/static/src/html/complainLIst.html?type=fw')
            elif fid =='mylist' and iN >0:
                url='/lwerp/lw/src/html/myComplainList.html?type=fw'
                # return HttpResponseRedirect('/static/src/html/myComplainList.html?type=fw')
            elif fid =='complainDetail' and iN >0:
                url='/lwerp/lw/src/html/complainDetail.html?type=fw' 
            elif fid =='infoList' and iN >0:
                url='/lwerp/lw/src/html/infoList.html?type=fw' 
            elif fid =='infoDetail' and iN >0:
                url='/lwerp/lw/src/html/infoDetail.html?type=fw' 
            elif fid =='LabourContractList':
                if date_ary>start_time and date_ary<end_time:                    
                    url='/lwerp/lw/src/html/ProjPay/pause.html' 
                else:
                    url='/lwerp/lw/src/html/ProjPay/projList.html' 
            elif fid =='ProgressList':
                url='/lwerp/lw/src/html/ProjPay/myUploadList.html' 
            elif fid =='uploadDetail':
                url='/lwerp/lw/src/html/ProjPay/uploadDetail.html?id=%s'%(seq)
            else:
                #if rows[0][1]==0:
                url='/lwerp/lw/src/html/bindDisplay.html?type=fw'
                #else:
                #    url='/lwerp/lw/src/html/ServicePlatform/bindSuccess2.html'

        if seq!='':
            url += '&xyId=%s'%(seq) 
        return HttpResponseRedirect(url) 
    else:
        if code!='':
            conn = httplib.HTTPSConnection('api.weixin.qq.com')  
            sToken = read_access_token()
            if sToken == '':            
                url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId,AppSecret)
                conn.request('GET', '%s'%url)  
                res = conn.getresponse()       
                body = res.read()  
                ddata=json.loads(body)
                sToken = ddata['access_token'] 
                conn.close()  
                write_access_token(body)
            url = "/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(AppId,AppSecret,code)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            access_token = ddata['access_token']
            openid = ddata['openid']

            url = "/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(sToken,openid)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            # print ddata
            nickname = ddata.get('nickname','')
            sql="select usr_id,IFNULL(status,0) from users_wx where openid='%s'"%openid
            rows,iN = db.select(sql)
            # print sql
            status=0
            if iN>0:
            	userid = rows[0][0]
                status = rows[0][1]
            else:
            	sql="""INSERT INTO users_wx(openid,nickname,ctime,status) VALUES('%s','%s',now(),0)"""%(openid,nickname)
                # print sql
            	db.executesql(sql)
            	rows,iN = db.select("select usr_id from users_wx where openid='%s'"%openid)
            	userid = rows[0][0]
            request.session['usr_id'] = userid
            if status==0:
                if fid =='infoList' :
                    url='/lwerp/lw/src/html/infoList.html?type=fw' 
                elif fid =='infoDetail':
                    url='/lwerp/lw/src/html/infoDetail.html?type=fw'
                else:
                    url='/lwerp/lw/src/html/bindInfo.html?itype=lw'
                # return HttpResponseRedirect('/static/src/html/bindInfo.html?type=fw')
            else:
                if fid=='list' and status==1:
                    url='/lwerp/lw/src/html/complainLIst.html?type=fw'
                elif fid =='mylist' and status==1:
                    url='/lwerp/lw/src/html/myComplainList.html?type=fw'
                elif fid =='complainDetail' and status==1:
                    url='/lwerp/lw/src/html/complainDetail.html?type=fw' 
                elif fid =='infoList' and status==1:
                    url='/lwerp/lw/src/html/infoList.html?type=fw' 
                elif fid =='infoDetail' and status==1:
                    url='/lwerp/lw/src/html/infoDetail.html?type=fw' 
                elif fid =='LabourContractList' and status==1:
                    if date_ary>start_time and date_ary<end_time:                    
                        url='/lwerp/lw/src/html/ProjPay/pause.html' 
                    else:
                        url='/lwerp/lw/src/html/ProjPay/projList.html' 
                elif fid =='ProgressList' and status==1:
                    url='/lwerp/lw/src/html/ProjPay/myUploadList.html' 
                elif fid =='uploadDetail':
                    url='/lwerp/lw/src/html/ProjPay/uploadDetail.html?id=%s'%(seq)
                else:
                    url='/lwerp/lw/src/html/bindDisplay.html?type=fw'
            if seq!='':
                url += '&xyId=%s'%(seq)
            return HttpResponseRedirect(url)	
	        # return HttpResponseCORS(request,ddata['nickname'])
	    # else:  #此处跳到请先关注页面
	    # 	return HttpResponseRedirect('/static/src/html/bindInfo.html')
    return HttpResponseCORS(request,'error')

def default(request):
    fid = request.GET.get('fid','')
    seq = request.GET.get('seq','')
    url ="""https://lw.szby.cn/complaint/login/index?fid=%s&seq=%s"""%(fid,seq)
    usr_id = request.session.get('usr_id','')
    if usr_id !='':
        return HttpResponseRedirect(url)

    redirect_uri = request.get_full_path()

    url =my_urlencode(url)
    surl = """https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1#wechat_redirect
    """%(AppId,url)
    return HttpResponseRedirect(surl)

#推荐人服务号入口
def index_tj(request):
    fid = request.GET.get('fid','')
    code = request.GET.get('code','')
    state = request.GET.get('state',0)
    seq = request.GET.get('seq','')
    pk = request.GET.get('pk','')
    typeId = request.GET.get('typeId','')
    must_reply = request.GET.get('must_reply','')
    usr_id_tj = request.session.get('usr_id_tj','')
    if usr_id_tj !='':
        rows,iN = db.select("select usr_id from users_tj where usr_id='%s' and status=1"%usr_id_tj)
        if iN ==0:
            url='/lwerp/lw/src/html/bindInfo.html?itype=tj'
        else:
            if fid=='bindInfo':
                url='/lwerp/lw/src/html/bindDisplay.html?itype=tj'
            else:
                url='/lwerp/lw/src/html/proj_refer/%s.html?type=fw'%(fid)
        if seq!='':
            url += '&xyId=%s'%(seq) 
        return HttpResponseRedirect(url) 
        # return HttpResponseCORS(request,usr_id_tj)       
    else:
        if code!='':
            conn = httplib.HTTPSConnection('api.weixin.qq.com')  
            sToken = read_access_token_common('access_token_tj')
            if sToken == '':            
                url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_tj,AppSecret_tj)
                conn.request('GET', '%s'%url)  
                res = conn.getresponse()       
                body = res.read()  
                ddata=json.loads(body)
                sToken = ddata['access_token'] 
                conn.close()  
                write_access_token_common(body,'access_token_tj')
            url = "/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(AppId_tj,AppSecret_tj,code)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            access_token = ddata['access_token']
            openid = ddata['openid']

            url = "/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(sToken,openid)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            # print ddata
            nickname = ddata.get('nickname','')
            sql="select usr_id,IFNULL(status,0) from users_tj where openid='%s'"%openid
            rows,iN = db.select(sql)
            # print sql
            status=0
            if iN>0:
                userid = rows[0][0]
                status = rows[0][1]
            else:
                sql="""INSERT INTO users_tj(openid,nickname,ctime,status) VALUES('%s','%s',now(),0)"""%(openid,nickname)
                # print sql
                db.executesql(sql)
                rows,iN = db.select("select usr_id from users_tj where openid='%s'"%openid)
                userid = rows[0][0]
            request.session['usr_id_tj'] = userid
            if status==0:
                url='/lwerp/lw/src/html/bindInfo.html?itype=tj'
            else:
                if fid=='bindInfo':
                    url='/lwerp/lw/src/html/bindDisplay.html?itype=tj'
                else:
                    url='/lwerp/lw/src/html/proj_refer/%s.html?type=fw'%(fid)
            if seq!='':
                url += '&xyId=%s'%(seq) 
            return HttpResponseRedirect(url) 
            # return HttpResponseCORS(request,ddata['nickname'])
    return HttpResponseCORS(request,'error')

def default_tj(request):
    fid = request.GET.get('fid','')
    if fid=='list':
        fid='projStatusList'
    if fid=='login':
        fid='bindInfo'
    seq = request.GET.get('seq','')
    # return HttpResponseCORS(request,fid)
    url ="""https://lw.szby.cn/complaint/login/index_tj?fid=%s&seq=%s"""%(fid,seq)
    url =my_urlencode(url)
    surl = """https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1#wechat_redirect
    """%(AppId_tj,url)
    return HttpResponseRedirect(surl)

#供应商服务号入口
def index_gy(request):
    fid = request.GET.get('fid','')
    code = request.GET.get('code','')
    state = request.GET.get('state',0)
    seq = request.GET.get('seq','')
    pk = request.GET.get('pk','')
    typeId = request.GET.get('typeId','')
    must_reply = request.GET.get('must_reply','')
    usr_id_gy = request.session.get('usr_id_gy','')
    print fid,usr_id_gy
    if usr_id_gy !='':
        rows,iN = db.select("select usr_id from users_gy where usr_id='%s' and status=1"%usr_id_gy)
        if iN ==0:
            if fid =='infoList' :
                url='/lwerp/lw/src/html/infoList.html?type=fw&projType=gy' 
            elif fid =='infoDetail':
                url='/lwerp/lw/src/html/infoDetail.html?type=fw&projType=gy'
            elif fid =='apply_form_name':
                url='/lwerp/lw/src/html/apply_gy/apply_form_name.html?type=fw&projType=gy&id=%s'%seq
            elif fid =='materialList_fw':
                url='/lwerp/lw/src/html/material/materialList_fw.html'
            elif fid =='materialList_fw':
                url='/lwerp/lw/src/html/material/materialList_fw.html'
            else: 
                url='/lwerp/lw/src/html/bindInfo.html?itype=gy'
        else:
            if fid=='list' and iN >0:
                url='/lwerp/lw/src/html/providerComplainList.html?type=fw&projType=gy'
            elif fid =='mylist' and iN >0:
                url='/lwerp/lw/src/html/myComplainList.html?type=fw&projType=gy'
            elif fid =='complainDetail' and iN >0:
                url='/lwerp/lw/src/html/complainDetail.html?type=fw&projType=gy' 
            elif fid =='infoList' and iN >0:
                url='/lwerp/lw/src/html/infoList.html?type=fw&projType=gy' 
            elif fid =='infoDetail' and iN >0:
                url='/lwerp/lw/src/html/infoDetail.html?type=fw&itype=gy&projType=gy' 
            elif fid=='payInfoDetail' and iN>0:
                url='/lwerp/lw/src/html/payInfoDetail.html?type=fw&itype=gy&projType=gy'
            elif fid =='bidResult' and iN>0:
                url='/lwerp/lw/src/html/bid_feedBack/bidResult.html?id=%s'%seq
            elif fid =='accuseProjList' and iN>0:
                url='/lwerp/lw/src/html/policy_accuse/accuseProjList.html?type=fw&projType=gy'
            elif fid =='myAccuseList' and iN>0:
                url='/lwerp/lw/src/html/policy_accuse/myAccuseList.html?type=fw&projType=gy'
            else:
                url='/lwerp/lw/src/html/bindDisplay.html?itype=gy'

        if seq!='':
            url += '&xyId=%s'%(seq) 
        return HttpResponseRedirect(url) 
    else:
        if code!='':
            conn = httplib.HTTPSConnection('api.weixin.qq.com')  
            sToken = read_access_token_common('access_token_gy')
            if sToken == '':            
                url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
                conn.request('GET', '%s'%url)  
                res = conn.getresponse()       
                body = res.read()  
                ddata=json.loads(body)
                sToken = ddata['access_token'] 
                conn.close()  
                write_access_token_common(body,'access_token_gy')
            url = "/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(AppId_gy,AppSecret_gy,code)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            access_token = ddata['access_token']
            openid = ddata['openid']

            url = "/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(sToken,openid)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            print body
            ddata=json.loads(body)
            subscribe = ddata.get('subscribe','')
            unionid = ddata.get('unionid','')
    
            if str(subscribe) != '1':
                url = 'https://lw.szby.cn/lwerp/lw/src/html/noAttention.html'
                return HttpResponseRedirect(url)    
                
            # print ddata
            nickname = ddata.get('nickname','')
            sql="select usr_id,IFNULL(status,0),ifnull(unionid,'') from users_gy where openid='%s'"%openid
            rows,iN = db.select(sql)
            # print sql
            status=0
            if iN>0:
                userid = rows[0][0]
                status = rows[0][1]
                if unionid !='' and rows[0][2] == '':
                    sql="update users_gy set unionid='%s' where openid='%s'"%(unionid,openid)
                    db.executesql(sql)
            else:
                sql="""INSERT INTO users_gy(openid,nickname,ctime,status,unionid) VALUES('%s','%s',now(),0,'%s')"""%(openid,nickname,unionid)
                # print sql
                db.executesql(sql)
                rows,iN = db.select("select usr_id from users_gy where openid='%s'"%openid)
                userid = rows[0][0]
            request.session['usr_id_gy'] = userid
            if status==0:
                if fid =='infoList' :
                    url='/lwerp/lw/src/html/infoList.html?type=fw&projType=gy' 
                elif fid =='infoDetail':
                    url='/lwerp/lw/src/html/infoDetail.html?type=fw&projType=gy'
                elif fid =='apply_form_name':
                    url='/lwerp/lw/src/html/apply_gy/apply_form_name.html?type=fw&projType=gy&id=%s'%seq
                elif fid =='materialList_fw':
                    url='/lwerp/lw/src/html/material/materialList_fw.html'
                elif fid =='materialDetail_fw':
                    url='/lwerp/lw/src/html/material/materialDetail_fw.html?id=%s'%seq
                else:
                    url='/lwerp/lw/src/html/bindInfo.html?itype=gy'
                # return HttpResponseRedirect('/static/src/html/bindInfo.html?type=fw')
            else:
                if fid=='list' and status==1:
                    url='/lwerp/lw/src/html/providerComplainList.html?type=fw&projType=gy'
                elif fid =='mylist' and status==1:
                    url='/lwerp/lw/src/html/myComplainList.html?type=fw&projType=gy'
                elif fid =='complainDetail' and status==1:
                    url='/lwerp/lw/src/html/complainDetail.html?type=fw&projType=gy' 
                elif fid =='infoList' and status==1:
                    url='/lwerp/lw/src/html/infoList.html?type=fw&projType=gy' 
                elif fid =='infoDetail' and status==1:
                    url='/lwerp/lw/src/html/infoDetail.html?type=fw&itype=gy&projType=gy' 
                elif fid=='payInfoDetail' and status==1:
                    url='/lwerp/lw/src/html/payInfoDetail.html?type=fw&itype=gy&projType=gy'
                elif fid =='bidResult' and status==1:
                    url='/lwerp/lw/src/html/bid_feedBack/bidResult.html?id=%s'%seq
                elif fid =='accuseProjList' and status==1:
                    url='/lwerp/lw/src/html/policy_accuse/accuseProjList.html?type=fw&projType=gy'
                elif fid =='myAccuseList' and status==1:
                    url='/lwerp/lw/src/html/policy_accuse/myAccuseList.html?type=fw&projType=gy'
                else:
                    url='/lwerp/lw/src/html/bindDisplay.html?type=fw&itype=gy'
            if seq!='':
                url += '&xyId=%s'%(seq)
            return HttpResponseRedirect(url)    
            # return HttpResponseCORS(request,ddata['nickname'])
        # else:  #此处跳到请先关注页面
        #   return HttpResponseRedirect('/static/src/html/bindInfo.html')
    return HttpResponseCORS(request,'error')

def default_gy(request):
    fid = request.GET.get('fid','')
    seq = request.GET.get('seq','')
    # return HttpResponseCORS(request,fid)
    url ="""https://lw.szby.cn/complaint/login/index_gy?fid=%s&seq=%s"""%(fid,seq)
    url =my_urlencode(url)

    surl = """https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1#wechat_redirect
    """%(AppId_gy,url)
    return HttpResponseRedirect(surl)