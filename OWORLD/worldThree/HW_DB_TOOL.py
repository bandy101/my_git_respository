# -*- coding: utf-8 -*-

"""DB共享类库"""
from django.db import connection
class DataBaseParent:
    def __init__(self):
        self.cursor="Initial Status"
        self.cursor=connection.cursor()
        if self.cursor=="Initial Status":
            raise Exception("Can't connect to Database server!")

    def select(self,sqlstr):
        cur=connection.cursor()
        cur.execute('SET NAMES utf8mb4')
        cur.execute(sqlstr)
        List=cur.fetchall()
        iTotal_length=len(List)
        self.description=cur.description
        cur.close()
        return List,iTotal_length

    def select_include_name(self,sqlstr):
        #选择结果包含List,iTotal_length,lFieldName
        #return list(self.select(sqlstr))+[self.description]
        cur=connection.cursor()
        cur.execute('SET NAMES utf8mb4')
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
        cur=connection.cursor()
        cur.execute('SET NAMES utf8mb4')
        r = cur.execute(sqlstr)
        cur.close()        
        return r

    def release(self):
        
        return 0

def mGetTransactionSQL(sqlstr):
    s="""BEGIN TRANSACTION
             %s
         IF @@ERROR=0
             COMMIT TRANSACTION
         ELSE ROLLBACK TRANSACTION""" % sqlstr
    return s

def addWhereToSQL(sqlstr,field,fieldtype,mode,value1='',value2=''):
    #在SQL语句中将field按mode寻找
    sqlstr=string.replace(sqlstr,'from','FROM')    
    sqlstr=string.replace(sqlstr,'where','WHERE')
    lT=string.split(sqlstr,'WHERE ')
    if len(lT)==2:
        if fieldtype=='NUMBER':
            if mode in ['=','>','>=','<','<=']:
                s=string.replace(sqlstr,'WHERE ',"WHERE %s%s%s AND "%(field,mode,value1))
            elif mode=='BETWEEN':
                s=string.replace(sqlstr,'WHERE ',"WHERE (%s BETWEEN %s AND %s) AND "%(field,value1,value2))
        elif fieldtype=='CHAR':
            value1=string.upper(string.replace(value1,"'","''"))
            if mode=='=':
                s=string.replace(sqlstr,'WHERE ',"WHERE UPPER(%s)%sN'%s' AND "%(field,mode,value1))
            elif mode=='START':
                s=string.replace(sqlstr,'WHERE ',"WHERE UPPER(%s) LIKE N'%s@@@' AND "%(field,value1))
            elif mode=='END':
                s=string.replace(sqlstr,'WHERE ',"WHERE UPPER(%s) LIKE N'@@@%s' AND "%(field,value1))
            elif mode=='INCLUDE':
                s=string.replace(sqlstr,'WHERE ',"WHERE UPPER(%s) LIKE N'@@@%s@@@' AND "%(field,value1))
            s=string.replace(s,'@@@','%')
    return s

def addOrderByToSQL(sqlstr,field,order):
    #在SQL语句中将field按order排序
    sqlstr=string.replace(sqlstr,'order by','ORDER BY')
    lT=string.split(sqlstr,'ORDER BY ')
    if len(lT)==2:
        s2=string.strip(lT[1])
        lT1=string.split(s2,'%s '%field)
        if len(lT1)>1:
            s3=string.strip(lT1[1])
            lT2=string.split(s3,',')
            if len(lT2)>1:
                lT2[0]=order
                s3=string.join(lT2,',')
            else:
                s3=order
            lT1[1]=s3                
            s2=string.join(lT1,'%s '%field)
            lT[1]=s2
            s=string.join(lT,'ORDER BY ')
        else:
            s=string.replace(sqlstr,'ORDER BY ','ORDER BY %s %s,'%(field,order))
    else:
        s="%s ORDER BY %s %s"%(sqlstr,field,order)
    return s
