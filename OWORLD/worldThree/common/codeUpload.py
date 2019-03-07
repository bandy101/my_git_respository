# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname,HttpResponseCORS,ComplexEncoder,data_url'%prj_name) 
import json
import MySQLdb

def getCodeLists(request):
    pk =  request.POST.get('pk','') or request.GET.get('pk','')
    sql = """select bundle_code,slice_code,s_long,s_wide,s_thick,`square`, `square_real`,pic
              ,corner1_length,corner1_width,corner2_length,corner2_width
              ,corner3_length,corner3_width,corner4_length,corner4_width,cornerSquare
            from _m611_packing_list where gw_id='%s' order by slice_code"""%(pk)    
    names = 'bundle_code slice_code length width thick square realSquare picUpload corner1_length corner1_width corner2_length corner2_width corner3_length corner3_width corner4_length corner4_width cornerSquare'.split()
    NL,iN = db.select(sql)
    L = []
    for e in NL:
        L1 = list(e)
        L1[7] = packFilesUrl(e[7])
        L.append(L1)
    data = [dict(zip(names, d)) for d in L]
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取编码明细表成功",
        "lists":%s,
        }        """%(data)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)

def getSaleLists(request):
    hl_number =  request.POST.get('hl_number') or request.POST.get('hl_number1','')
    price =  request.POST.get('price','') 
    sale_gwid =  request.POST.get('sale_gwid','') 
    random_no =  request.POST.get('random_no','') 
    #print request.POST
    if sale_gwid != '':
        sql = """select bundle_code,plank_sn,sc_long,wide,thick,square_real,bc_picture,is_sale,sale_price from _m6144_plank_stock 
             where hl_number = '%s' and (is_sale =0 or sale_gwid=%s) order by plank_sn"""%(hl_number,sale_gwid)  
    else:
        sql = """select bundle_code,plank_sn,sc_long,wide,thick,square_real,bc_picture,is_sale,sale_price from _m6144_plank_stock 
             where hl_number = '%s' and (is_sale =0 or random_no='%s') order by plank_sn"""%(hl_number,random_no)  
    print sql
    names = 'bundle_code slice_code length width thick square picUpload selected sale_price'.split()
    NL,iN = db.select(sql)
    L = []
    for e in NL:
        L1 = list(e)
        L1[6] = packFilesUrl(e[6])
        L.append(L1) 
    data = [dict(zip(names, d)) for d in L]
    data = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder) 

    s = """
        {
        "errcode": 0,
        "errmsg": "获取明细表成功",
        "lists":%s,
        }        """%(data)
    #print ToGBK(s)
    return HttpResponseCORS(request,s)

def packFilesUrl(file_ids):
    L1 = []
    fid_list = file_ids.split(',')
    for e in fid_list:
        L = ['file_id','size','name','thumbnail_url','url','delete_url']
        if e=='': continue
        sql = "select title,fname,file_size,is_pic from file_pic where id =%s"%e
        lT,iN=db.select(sql)
        if iN>0:
            L[0] = e   
            L[1] = lT[0][2]    
            L[2] = lT[0][0]    
            if lT[0][3] == 1: 
                L[3] = "%s/get_file/?fname=%s"%(data_url,lT[0][1])
            else:
                L[3] = ''
            L[4] = "%s/get_file/?fname=%s"%(data_url,lT[0][1])
            L[5] = "%s/del_file/?fname=%s"%(data_url,lT[0][1])
            L1.append(L)
    names = 'file_id size name thumbnail_url url delete_url'.split()
    data = [dict(zip(names, d)) for d in L1]

    return data