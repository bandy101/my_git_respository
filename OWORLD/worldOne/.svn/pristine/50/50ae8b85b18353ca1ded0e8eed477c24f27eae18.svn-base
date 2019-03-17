# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os,time
import json
import httplib
import urllib
# from HW_DT_TOOL                 import getToday
from HW_DB   import DataBaseParent_local
sys.path.append("/home/webroot/oWorld")
from common.HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG
# from share        import read_access_token_common,write_access_token_common
#本地mysql数据库
local=DataBaseParent_local()  

def push():
    sql="""INSERT INTO tracking_push_log(prj_id,ctime,status) VALUES(1,now(),1) """
    local.executesql(sql)

if __name__ == "__main__":
    print 'Push start.......'
    push()  
        