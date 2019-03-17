# -*- coding: utf-8 -*-

import sys
import os,time
# import pymssql
# sys.path.append("/home/webroot/oWorld/complaint")
# exec ('from share        import ToGBK')
# import MySQLdb
from HW_DB   import DataBaseParent_local,DataBaseParent_byerp,DataBaseParent_bkerp
#本地mysql数据库
local=DataBaseParent_local()  
#主系统MSSQL数据库
byerp = DataBaseParent_byerp()
bkerp = DataBaseParent_bkerp()
uc=unicode(str('s'), 'eucgb2312_cn')



if __name__ == "__main__":
    # usr_tj = 3323  #人员ID
    # # seq=1
    
    # ###测试数据###
    # pk=16631
    # memo='当前'
    # next_memo='下一步'
    # statusName ='正在跟进'

    # if statusName!='':
    #     memo+='%s</br>%s'%(memo,statusName)
    # # sql="""INSERT INTO out_proj_tracking (pid,stime,memo,next,cid,ctime,seq) 
    # #     VALUES (%s,getdate(),'%s','%s',%s,getdate(),3000000) """%(pk,memo,next_memo,usr_tj)
    # sql="""UPDATE out_proj_tracking SET memo ='ffff' WHERE seq = 3000000 """
    # #sql = ToGBK(sql)
    # print sql
    # bkerp.executesql(sql)
    # # seq = r[0][0]   #获取刚刚写入的seq
    # # print r

    # 测试读取主系统数据库
    sql="select id,memo from test_0123 "
    rows,iN=bkerp.select(sql)
    print iN
    sql="insert into test_0123(memo) values('test1')"
    bkerp.executesql(sql)
    # id_list='('
    # for e in rows:
    #     print "%s:%s"%(e[0],e[1])
    #     id_list+='%s,'%str(e[2])
    # print id_list
    # print rows[0][0]
    # print rows[0][1]
    # print rows[0][2]