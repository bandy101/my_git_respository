# -*- coding: utf-8 -*-

"""DB共享类库"""
# from django.db import connection
import MySQLdb
db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="24ea8194",db="complaint",charset="utf8")

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
        cur.execute('SET NAMES utf8mb4')
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

