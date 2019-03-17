# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder'%prj_name) 
import json


def application(request):
    sql="select * from user"
    row,iN=db.select(sql)

    return HttpResponseCORS(request,row[0][0])
