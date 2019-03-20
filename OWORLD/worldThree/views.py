#coding:utf-8
# urlStr:https://e.szby.cn/data_gy/common/printShd/
prj_name=__name__.split('.')[0]
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect  
from login import login_func,logout_func,menu_func
from login_wx import login_wx_func
from select import select_func
from getData import getData_func
from home import home_func
from fileUpload import attach_save,del_attach_file,file_down,file_list,editor_attach_save,file_manage_json
exec ('from %s.share import db,dActiveUser,mValidateUser,oSysInfo,HttpResponseCORS,ComplexEncoder,data_url,my_urlencode'%prj_name) 
import json
# Create your views here.
def sysinfo(request):
    L = oSysInfo.get()

    muti_lang = L[13]
    if muti_lang == 1:
        sql = "select id,name from muti_language where enabled=1"
        lT,iN=db.select(sql)
        L[14] = lT
    else:
        L[14] = []
    sql = "select ifnull(value,'') from sys_ext_info where name='attach_preview'"
    try:
        lT,iN=db.select(sql)
        if iN>0: 
            attach_preview = lT[0][0]
        else:
            attach_preview = ''
    except:
        attach_preview = 0
    L[16] = attach_preview
    names = 'corp_name full_name logo icon prj_name db_name data_url front_url fs_url corp_url corpid agentid printLogo enable_muti_language muti_languages icp attach_preview'.split()
    data = [dict(zip(names, L))]
    info = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)    
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息成功",
        "info":%s,
        }        """%(info)
    return HttpResponseCORS(request,s)

def translate(request):
    lang_id = request.POST.get('lang_id') or 1

    sql = """select f.variable,
                    case ifnull(l.label,'') when '' then f.cname else l.label end
             from  frontend_variable f
             left join muti_lang_frontend l on f.id = l.field_id and l.lang_id = '%s'
          """%(lang_id)
    lT,iN=db.select(sql)
    names = 'variable translate'.split()
    data = [dict(zip(names, d)) for d in lT]
    info = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)    
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息成功",
        "info":%s,
        }        """%(info)
    return HttpResponseCORS(request,s)

#重定向
def rd(request):  
    func = request.GET.get('func','') 
    if func.lower() == 'fa':
        code = request.GET.get('code','') 
        sql = "select corp_id,agentid from wx_corp_agent where name = '固定资产管理'"
        rows1,iN1 = db.select(sql)
        corp_id = rows1[0][0]
        agentid = rows1[0][1]
        url = "%s/index_wx/?FAcode=%s"%(data_url,code)
        url = my_urlencode(url)
        url1 = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&agentid=%s&state=FA_Code#wechat_redirect"%(corp_id,url,agentid)
        return HttpResponseRedirect(url1)
    return HttpResponseCORS(request,'')

def login(request):
    s = login_func(request)
    return s

def logout(request):
    s = logout_func(request)
    return s

def getMenu(request):
    s = menu_func(request)
    return s

def index_wx(request):
    s = index_wx_func(request)
    return s

def login_wx(request):
    s = login_wx_func(request)
    return s

def get_data_wx(request):
    s = get_data_wx_func(request)
    return s

def select(request):
    s = select_func(request)
    return s

def getData(request):
    s = getData_func(request)
    return s

def upload_file(request):  
    s = attach_save(request)
    return s

def del_file(request):  
    s = del_attach_file(request)
    return s

def get_file(request):  
    s = file_down(request)
    return s

def get_file_list(request):  
    s = file_list(request)
    return s

def home(request):  
    s = home_func(request)
    return s

def editor_upload(request):  
    #print request.POST
    method= request.POST.get('method') or request.GET.get('method','')
    if method == 'upload':
        s = editor_attach_save(request)
    elif method == 'file_manage':
        s = file_manage_json(request)
    else:
        s = ''
    return s

