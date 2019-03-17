# -*- coding: utf-8 -*-

import sys
import os,time
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# -*- coding: utf-8 -*-

"""DB共享类库"""
# from django.db import connection
#import pymssql
import MySQLdb
#db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="24ea8194",db="hcpra",charset="utf8")
#dbName = "hcpra"

#db = MySQLdb.connect(host="rm-wz93f3y09yxpa3gc3o.mysql.rds.aliyuncs.com",user="kjerp",passwd="1qaz3edc",db="kjerp",charset="utf8")
#dbName = "kjerp"

db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="24ea8194",db="pram",charset="utf8")
dbName = "pram"

#db = MySQLdb.connect(host="127.0.0.1",user="sgmy",passwd="1q2w9o0p",db="pram",charset="utf8")
#dbName = "pram"

class DataBaseParent_local:
    def __init__(self):
        self.cursor="Initial Status"
        self.cursor=db.cursor()
        if self.cursor=="Initial Status":
            raise Exception("Can't connect to Database server!")

    def select(self,sqlstr):
        cur=db.cursor()
        cur.execute(sqlstr)
        List=cur.fetchall()
        iTotal_length=len(List)
        self.description=cur.description
        cur.close()
        return List,iTotal_length

    def select_include_name(self,sqlstr):
        #选择结果包含List,iTotal_length,lFieldName
        #return list(self.select(sqlstr))+[self.description]
        cur=db.cursor()
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
        cur=db.cursor()
        r = cur.execute(sqlstr)
        db.commit()
        cur.close()        
        return r
        
    def insert(self,sql,param):
        cur=self.cursor
        n = cur.execute(sql,param) 
        db.commit()
        cur.close()        
        return n

    def release(self):
        
        return 0

#本地mysql数据库
local=DataBaseParent_local()  
uc=unicode(str('s'), 'eucgb2312_cn')
def exec_sort():
    sql = "select date_table from category"
    lT,iN=local.select(sql)
    for e in lT:
        table_name =  e[0].lower()
        sql = "SELECT * FROM information_schema.columns WHERE table_schema='%s' AND table_name = '%s' AND column_name = 'p_ids'"%(dbName,table_name)
        lT1,iN1=local.select(sql)
        if iN1 == 0:
            sql = "ALTER TABLE %s ADD COLUMN `p_ids`  varchar(1000) "%(table_name)
            local.executesql(sql)
        sql = "SELECT * FROM information_schema.columns WHERE table_schema='%s' AND table_name = '%s' AND column_name = 'child_ids'"%(dbName,table_name)
        lT1,iN1=local.select(sql)
        if iN1 == 0:
            sql = "ALTER TABLE %s ADD COLUMN `child_ids`  text "%(table_name)
            local.executesql(sql)

        sql = "select id,ifnull(p_id,-1) from %s order by id asc"%(table_name)
        lT1,iN1=local.select(sql)
        for e1 in lT1:
            id = e1[0]
            parent_id = e1[1]
            sql = "select ifnull(p_ids,'') from %s where id=%s"%(table_name,parent_id)
            #print sql
            lT2,iN2 = local.select(sql)
            if iN2 >0: 
                p_ids = lT2[0][0] + ',%s'%(parent_id)
            else:
                p_ids = ''
            sql = "update %s set p_ids='%s' where id=%s"%(table_name,p_ids,id)
            local.executesql(sql)
            sql = "select id,ifnull(child_ids,'') from %s where find_in_set(%s,child_ids) or id = %s"%(table_name,parent_id,parent_id)
            lT2,iN2 = local.select(sql)
            for e2 in lT2:
                child_ids = e2[1] + ',%s'%(id)
                p_id = e2[0]
                sql = "update %s set child_ids='%s',has_child=1 where id=%s"%(table_name,child_ids,p_id)
                local.executesql(sql)

    return
from xml.etree import ElementTree as ET
def import_area():
    # 打开xml文件，读取内容
    str_xml = open('pram/LocList.xml', 'r').read()

    # 将字符串解析成xml对象，root代指xml文件的根节点
    root = ET.XML(str_xml)
    CountryRegion = root.getchildren()
    for e in CountryRegion:
        code = e.get('Code')
        name = e.get('Name')
        sql = "insert into city_sort (cname,level,code) values ('%s',1,'%s')"%(name,code)
        local.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = local.select(sql)
        p_id = rows[0][0]
        State = e.getchildren()
        for e1 in State:
            code1 = e1.get('Code')
            name1 = e1.get('Name')
            sql = "insert into city_sort (cname,level,code,p_id) values ('%s',2,'%s',%s)"%(name1,code1,p_id)
            local.executesql(sql)
            sql = "select last_insert_id();"
            rows,iN = local.select(sql)
            p_id1 = rows[0][0]
            City = e1.getchildren()
            for e2 in City:
                code2 = e2.get('Code')
                name2 = e2.get('Name')
                sql = "insert into city_sort (cname,level,code,p_id) values ('%s',3,'%s',%s)"%(name2,code2,p_id1)
                local.executesql(sql)
    return

if __name__ == "__main__":
    print "synchro..."
    exec_sort()
    #import_area()