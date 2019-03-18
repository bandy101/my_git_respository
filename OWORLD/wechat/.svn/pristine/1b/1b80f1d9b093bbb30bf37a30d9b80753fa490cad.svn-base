# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname,HttpResponseCORS'%prj_name) 
import json

from qr_code import printFACode

def batchOperation(request):
    menu_id = request.GET.get('menu_id','')
    btn_id = request.GET.get('btn_id','')
    sql = "SELECT execFunc FROM menu_list_buttons where id = %s"%(btn_id)
    rows,iN = db.select(sql)
    execFunc = rows[0][0]
    if execFunc == 'printFACodes':  #批量打印二维码
        ids = request.POST.get('id') or request.GET.get('id','')
        return printFACode(ids)

    return HttpResponseCORS(request,'')

def handleMutilValue(value,is_number):
    sTemp = ','
    if isinstance(value,list):
        if is_number == 1:
            if len(value)>0:
                sTemp = value[0] or 0
            else:
                sTemp = 0
        else:
            for e in value:
                sTemp +="%s,"%e
    else:
        if is_number == 1:
            sTemp = value or 0
        else:
            sTemp = value
        
    return sTemp