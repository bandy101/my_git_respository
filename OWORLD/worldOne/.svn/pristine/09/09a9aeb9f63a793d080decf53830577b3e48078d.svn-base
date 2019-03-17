# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,read_access_token_common,write_access_token_common,checkSession,data_url,AppId,AppSecret'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse

testid = 1
def getSituation(request):
    type = request.POST.get('type','')
    sql="""SELECT flow_id,cname FROM flow WHERE ftype='ts'"""
    if type == 'accuse':
        sql += " and flow_id not in (-1,3)"
    else:
        sql += " and flow_id not in (3)"
    rows,iN=db.select(sql)

    names = 'flow_id cname'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取状态列表成功",
        "data":%s
        }        """%(L)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def getUsers(request):
    dept_id = request.POST.get('dept_id','')
    search = request.POST.get('search','')
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    sql="""SELECT U.usr_id,U.login_id,U.usr_name,IFNULL(U.pic,''),D.cname,D.id,getFirstHanZiCode(U.usr_name)
                FROM users U
                left join dept D on D.id=U.dept_id
                WHERE U.status = 1 
                #and isnull(U.del_flag,0)=0 
            """
    if dept_id!='':
        sql += """ and U.dept_id=%s"""%dept_id
    if search!='':
        sql += """ and U.usr_name like '%%%s%%'"""%search
    sql += " order by convert(U.usr_name USING gbk) COLLATE gbk_chinese_ci asc  "
    #print sql
    # rows,iN = db.select(sql)
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'usr_id login_id usr_name pic dept_name dept_id letter'.split()
    data = [dict(zip(names, d)) for d in rows]
    s = json.dumps(data,ensure_ascii=False)
    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取人员信息成功",
        "usersArray":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(s,iTotal_length,iTotal_Page,pageNo,select_size)
    return HttpResponseJsonCORS(s1)

def getDepts(request):
    parent_id = request.POST.get('parent_id',0)
    sql="""SELECT id,cname,parent_id
                FROM dept 
                WHERE  IFNULL(del_flag,0)=0 
            """
    if parent_id!=0:
        sql += """ and parent_id=%s"""%parent_id
    sql += " ORDER BY parent_id "
    #print sql
    rows,iN = db.select(sql)
    names = 'id name parent_id'.split()
    data = [dict(zip(names, d)) for d in rows]
    s = json.dumps(data,ensure_ascii=False)

    s1 = """
        {
        "errcode": 0,
        "errmsg": "获取部门列表成功",
        "deptArray":%s
        }"""%(s)
    return HttpResponseJsonCORS(s1)

AppId_gy = 'wxe703baaad2a1c9dc'
AppSecret_gy = '780065948cba96c5831c6b047a0ff7f8'

def makeMenu(request):
    # print sToken
    '''
    sMsg="""
        {
        "button":[
        {  
             "type":"view",
             "name":"反映情况",
             "url":"http://lw.szby.cn/complaint/login/default?fid=list",
             "sub_button":[]
         },
        {  
             "type":"view",
             "name":"我反映的情况",
             "url":"http://lw.szby.cn/complaint/login/default?fid=mylist",
             "sub_button":[]
         },
        {  
             "type":"view",
             "name":"身份绑定",
             "url":"http://lw.szby.cn/complaint/login/default?fid=login",
             "sub_button":[]
         }]

        }

        {
        "button":[
        {
        "name":"情况上报",
        "sub_button":[
            {  
             "type":"view",
             "name":"反映情况",
             "url":"http://lw.szby.cn/complaint/login/default?fid=list"
             },
            {  
             "type":"view",
             "name":"我反映的情况",
             "url":"http://lw.szby.cn/complaint/login/default?fid=mylist"
             }
          ]
        }, 
        {  
             "type":"view",
             "name":"信息查询",
             "url":"http://lw.szby.cn/complaint/login/default?fid=infoList",
             "sub_button":[]
        }, 
        {  
             "type":"view",
             "name":"身份绑定",
             "url":"http://lw.szby.cn/complaint/login/default?fid=login",
             "sub_button":[]
         }]

        }

        {
        "button":[
        {
        "name":"情况上报",
        "sub_button":[
            {  
             "type":"view",
             "name":"反映情况",
             "url":"http://lw.szby.cn/complaint/login/default_gy?fid=list"
             },
            {  
             "type":"view",
             "name":"我反映的情况",
             "url":"http://lw.szby.cn/complaint/login/default_gy?fid=mylist"
             }
          ]
        }, 
        {  
             "type":"view",
             "name":"信息查询",
             "url":"http://lw.szby.cn/complaint/login/default_gy?fid=infoList",
             "sub_button":[]
        }, 
        {  
             "type":"view",
             "name":"身份绑定",
             "url":"http://lw.szby.cn/complaint/login/default_gy?fid=login",
             "sub_button":[]
         }]

        }"""
    '''

    #工程综合部
    sMsg="""
        {
        "button":[
        {
        "name":"情况上报",
        "sub_button":[
            {  
             "type":"view",
             "name":"反映情况",
             "url":"https://lw.szby.cn/complaint/login/default?fid=list"
             },
            {  
             "type":"view",
             "name":"我反映的情况",
             "url":"https://lw.szby.cn/complaint/login/default?fid=mylist"
             }
          ]
        }, 
        {
        "name":"进度款上报",
        "sub_button":[
            {  
             "type":"view",
             "name":"进度款上报",
             "url":"https://lw.szby.cn/complaint/login/default?fid=LabourContractList"
             },
            {  
             "type":"view",
             "name":"我的上报记录",
             "url":"https://lw.szby.cn/complaint/login/default?fid=ProgressList"
             }
          ]
        }, 
        {
        "name":"我的",
        "sub_button":[
            {  
             "type":"view",
             "name":"信息查询",
             "url":"https://lw.szby.cn/complaint/login/default?fid=infoList"
             },
            {  
             "type":"view",
             "name":"身份绑定",
             "url":"https://lw.szby.cn/complaint/login/default?fid=login"
             }
          ]
        }, 
        ]
        }"""
    
    #材料采购部
    sMsg="""
        {
        "button":[
        {
        "name":"情况上报",
        "sub_button":[
            {  
             "type":"view",
             "name":"反映情况",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=list"
             },
            {  
             "type":"view",
             "name":"我反映的情况",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=mylist"
             }
          ]
        }, 
        {
        "name":"廉政管理",
        "sub_button":[
            {  
             "type":"view",
             "name":"投诉举报",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=accuseProjList"
             },
            {  
             "type":"view",
             "name":"我的投诉",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=myAccuseList"
             }
          ]
        }, 
        {
        "name":"供应商服务",
        "sub_button":[
            {  
             "type":"view",
             "name":"材料寻源",
             "url":"https://lw.szby.cn/lwerp/lw/src/html/material/materialList_fw.html"
             },
            {  
             "type":"view",
             "name":"供应商报名",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=apply_form_name"
             },
            {  
             "type":"view",
             "name":"信息查询",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=infoList"
             },
            {  
             "type":"view",
             "name":"身份绑定",
             "url":"https://lw.szby.cn/complaint/login/default_gy?fid=login"
             }
          ]
        }, 
        ]
        }"""
    #App_Id = AppId
    #App_Secret = AppSecret
    App_Id = AppId_gy
    App_Secret = AppSecret_gy
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    #sToken = read_access_token()
    sToken = read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(App_Id,App_Secret)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        #write_access_token(body)
        write_access_token_common(body,'access_token_gy')

    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    url = "/cgi-bin/menu/create?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode'] 
    # print errcode   
    return HttpResponseCORS(request,errcode)

def getTypeList(request):
    sql="""SELECT id,txt1,icon FROM mtc_t WHERE type='XXLB'
        """
    rows,iN = db.select(sql)
    names = 'id type_name icon'.split()
    data = [dict(zip(names, d)) for d in rows]
    type_list = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息分类列表成功",
        "type_list":%s
        }"""%(type_list)
    return HttpResponseJsonCORS(s)

def getTypeList_gy(request):
    sql="""SELECT id,txt1,icon FROM mtc_t WHERE type='XXFL'
        """
    rows,iN = db.select(sql)
    names = 'id type_name icon'.split()
    data = [dict(zip(names, d)) for d in rows]
    type_list = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息分类列表成功",
        "type_list":%s
        }"""%(type_list)
    return HttpResponseJsonCORS(s)

def getMtcType(request):
    mtc_type = request.POST.get('mtc_type','WTRADE')
    sql="""SELECT id,txt1 FROM mtc_t WHERE type='%s' """%(mtc_type)
    rows,iN = db.select(sql)
    names = 'id type_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    type_list = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息分类列表成功",
        "type_list":%s
        }"""%(type_list)
    return HttpResponseJsonCORS(s)

#查找劳务团队
def getLaborTeam(request):
    leaderName = request.POST.get('leaderName','') or ''
    if leaderName=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "团队名字不能为空"
        }"""
        return HttpResponseJsonCORS(s)
    sql="""SELECT ab.id,ab.name FROM addr_book ab 
        WHERE ab.status=1 AND ab.name='%s' AND ab.id IN (select addr_book_id from addr_book_group WHERE addr_group_id=7)
        LIMIT 1"""%(leaderName)
    rows,iN = db.select(sql)
    if iN<1:
        s = """
        {
        "errcode": -1,
        "errmsg": "经查无此人，请确认后填写。"
        }"""
        return HttpResponseJsonCORS(s)
    names = 'team_id team_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取团队信息成功",
        "data":%s
        }"""%(L)
    return HttpResponseJsonCORS(s)

#查找项目
def getProj(request):
    proj_no = request.POST.get('proj_no','')
    team_id = request.POST.get('team_id','') or 0
    if proj_no=='' or team_id=='':
        s = """
        {
        "errcode": -1,
        "errmsg": "缺少项目编号或劳务团队ID"
        }"""
        return HttpResponseJsonCORS(s)
    if str(team_id)!='0':
        sql="""SELECT OP.id,OP.cname
               FROM addr_book AB
               LEFT JOIN labour_contract LC ON AB.id = LC.teams_id
               LEFT JOIN out_proj OP ON OP.id = LC.proj_id
               WHERE AB.id=%s AND OP.gc_no='%s' """%(team_id,proj_no)
    else:
        sql="""SELECT OP.id,OP.cname
               FROM out_proj OP
               WHERE OP.gc_no='%s' """%(proj_no)
    rows,iN = db.select(sql)
    if iN<1:
        s = """
        {
        "errcode": -1,
        "errmsg": "经查无此项目，请重新填写。"
        }"""
        return HttpResponseJsonCORS(s)
    names = 'proj_id proj_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取项目信息成功",
        "data":%s
        }"""%(L)
    return HttpResponseJsonCORS(s)