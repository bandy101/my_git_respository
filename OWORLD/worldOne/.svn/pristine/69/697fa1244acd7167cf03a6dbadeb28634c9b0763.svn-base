# -*- coding: utf-8 -*-

import sys
import os,time
# import pymssql
# sys.path.append("/home/webroot/oWorld/complaint")
# exec ('from share        import ToGBK')
# import MySQLdb
from HW_DB   import DataBaseParent_local,DataBaseParent_byerp
#本地mysql数据库
local=DataBaseParent_local()  
#主系统MSSQL数据库
byerp = DataBaseParent_byerp()
uc=unicode(str('s'), 'eucgb2312_cn')

#引入数据表
execfile('table.py')

def data_deal(data):
    field = '' #字段集合
    for yy in data:
        ddd = yy[0]
        field = field+ddd+','
    field = field[:-1]    
    return field    

def data_deal_update(data):
    field = '' 
    for x in data:
        for y in x:
            y = str(y)
            field = field+y+','
    field = field[:-1]    
    return field   

#拼接insert语句
def insertSql(table,field,key,SourceDataBase,datasource,maxID):    
    select_sql = selectSql(table,key,maxID,datasource) #查询出需要通讯的数据
    #print select_sql
    LT1 = ''
    LT1,iN1=SourceDataBase.select(select_sql)
    src_total=len(LT1)
    print src_total
    print """%s:...."""%table
    if src_total != 0 :
        for A in LT1 :
            src_total = src_total - 1
            #print """Data left : %s"""%(src_total)
            L = L_result_deal(list(A))
            L.append(datasource)
            L_ok = tuple(L)  

            sql,end_rowversion = insertSql_deal(table, L,datasource)
            # print sql 
            try:
               if sql: local.executesql(sql) 
            except:
               print 'fail__insert:',sql,time.ctime()
               # fileHandle.write(time.ctime()+':'+sql+"\r")  
               # exit()
               # writeLOG(log_file,sql)  
            print '%s:insert___ok...source...%s...Data left:%s'%(table,datasource,src_total)
    else:
        print "No data....!" 
    print "------------------------------"    


#组装查询语句
def selectSql(table, key,maxID,datasource):
    if datasource == 1 :
        ARRAY = DD
    if datasource == 2:
        ARRAY = AQ  
    col,LL = [],ARRAY[table.lower()]
    for L in LL:
        L=list(L) 
        if L[2]=='datetime':
            L[0]='CONVERT(NVARCHAR(23), %s, 121)'%L[0]
        elif L[2]=='rowversion':
            L[0]='CONVERT(int, %s)'%L[0]
        elif L[2]=='text':
            L[0]='CONVERT(VARCHAR(8000), %s)'%L[0]       
        col.append(L[0])
    cols = ','.join(col)
     
    sql="""SELECT %s
           FROM %s
             where %s>%s  --WHERE
          """%(cols, table,key,maxID)
    if table =='gw_doc':
        sql+="""and type_id !=200 and type_id !=216 and type_id !=217"""
    if table =='cost_ea':
        sql+="""and Proj_id is NULL """
    sql+="""order by %s"""%(key)
    # print sql
    return sql


#查询备份系统对应源的最大ID
def Get_MaxID(table,key,datasource):
    sql = """select max(%s) from %s where datasource =%s """%(key,table,datasource)
    L,data=local.select(sql)
    for XX in L:
      YY = XX[0]
    if YY == None :
      return 0
    else:
      return YY

#字符处理
def L_result_deal(L):
    for m in range(len(L)): 
        if (L[m] is None) or (L[m]=='NULL') or (L[m]==''):
            if type(L[m])==type(1):
                L[m]='NULL'
            else:
                L[m]=''         
        if type(L[m])==type(uc):                
            L[m]=L[m].encode('utf8')                
        if type(L[m])==type('a'):
            L[m]=L[m].replace("'","''").strip()
    return L   
# def selectMax(table,key):
#     sql = """select max(%s) from %s.%s"""%(key,TargetDataBase,table)
#     return sql 

def insertSql_deal(table_name, rL,datasource):
    if datasource == 1 :
        ARRAY = DD
    if datasource == 2:
        ARRAY = AQ    
    col,LL=[],ARRAY[table_name.lower()]
 
    ss=[]
    i=0
    end_rowversion=''
    for cL in LL:
        s = rL[i]
        dataType=cL[2]
        col.append(cL[0])
        if dataType.find('date')>-1:
            r = date_deal(s)
        elif dataType.find('char')>-1:
            r="'%s'"%(s or '')
        elif dataType.find('int')>-1  or dataType.find('uniqueidentifier')>-1 or dataType.find('decimal')>-1 or dataType.find('numeric')>-1 or dataType.find('bit')>-1 or dataType.find('tinyint')>-1 or dataType.find('money')>-1 or dataType.find('float')>-1:
            if s in ['',None]:r="NULL"
            else:r="'%s'"%s
            if dataType.find('bit')>-1:
            	if str(s)=='False':
            		r='0'
                if str(s)=='True':
                	r='1'
        else:
            r = "'%s'"%s
        ss.append(r)
        i+=1 
        if dataType.find('rowversion')>-1: #时间该字段为时间戳，则记录
            end_rowversion=s
            
    cols = ','.join(col)  

    s2 = ','.join(ss)
    sql="""INSERT %s (%s,datasource) VALUES(%s,%s)
        """%(table_name, cols, s2,datasource)
    #print 'end_rowversion:%s'% end_rowversion
    sql = sql.replace(']','`')
    sql = sql.replace('[','`')
    sql = sql.replace('\\','\\\\')
    return sql,end_rowversion

def date_deal(str_date):
    str_date=str(str_date)
    if str_date=='' or str_date=='NULL' or str_date is None:
        return 'NULL'
    else:
        return """'%s'"""%str_date

#拼接update语句
def updateSql(table,field,key,SourceDataBase,datasource,id_list):    
    select_sql = selectSqlUpdate(table,key,id_list,datasource) #查询出需要更新的数据
    print select_sql
    LT1 = ''
    LT1,iN1=SourceDataBase.select(select_sql)
    src_total=len(LT1)
    print src_total
    print """%s:...."""%table
    if src_total != 0 :
        for A in LT1 :
            src_total = src_total - 1
            #print """Data left : %s"""%(src_total)
            L = L_result_deal(list(A))
            L.append(datasource)
            L_ok = tuple(L)  

            sql,end_rowversion = updateSql_deal(table, L,datasource,key,A[0])
            # print sql 
            try:
               if sql: local.executesql(sql) 
            except:
               print 'fail__update:',sql,time.ctime()
               # fileHandle.write(time.ctime()+':'+sql+"\r")  
               # exit()
               # writeLOG(log_file,sql)  
            print '%s:update___ok...source...%s...Data left:%s'%(table,datasource,src_total)
    else:
        print "No data....!" 
    print "------------------------------"    

def GetUpdate(table,key):
    L =''
    sql = """select %s from %s where utime is not null"""%(key,table)
    rows,iN = SourceDataBase.select(sql)
    if iN>0:
    	L='(0'
        for e in rows:
        	L+=','+str(e[0])
        L+=')'
    return L

#组装查询语句
def selectSqlUpdate(table, key,id_list,datasource):
    if datasource == 1 :
        ARRAY = DD
    if datasource == 2:
        ARRAY = AQ  
    col,LL = [],ARRAY[table.lower()]
    for L in LL:
        L=list(L) 
        if L[2]=='datetime':
            L[0]='CONVERT(NVARCHAR(23), %s, 121)'%L[0]
        elif L[2]=='rowversion':
            L[0]='CONVERT(int, %s)'%L[0]
        elif L[2]=='text':
            L[0]='CONVERT(VARCHAR(8000), %s)'%L[0]       
        col.append(L[0])
    cols = ','.join(col)
     
    sql="""SELECT %s
           FROM %s
             where %s in %s  --WHERE
          """%(cols, table,key,id_list)
    if table =='gw_doc':
        sql+="""and type_id !=200 and type_id !=216 and type_id !=217"""
    if table =='cost_ea':
        sql+="""and Proj_id is NULL """
    sql+="""order by %s"""%(key)
    # print sql
    return sql

def updateSql_deal(table_name, rL,datasource,key,key_value):
    if datasource == 1 :
        ARRAY = DD
    if datasource == 2:
        ARRAY = AQ    
    col,LL=[],ARRAY[table_name.lower()]
 
    ss=[]
    i=0
    data = ''
    end_rowversion=''
    for cL in LL:
        s = rL[i]
        dataType=cL[2]
        col.append(cL[0])
        if dataType.find('date')>-1:
            r = date_deal(s)
        elif dataType.find('char')>-1:
            r="'%s'"%(s or '')
        elif dataType.find('int')>-1  or dataType.find('uniqueidentifier')>-1 or dataType.find('decimal')>-1 or dataType.find('numeric')>-1 or dataType.find('bit')>-1 or dataType.find('tinyint')>-1 or dataType.find('money')>-1 or dataType.find('float')>-1:
            if s in ['',None]:r="NULL"
            else:r="'%s'"%s
            if dataType.find('bit')>-1:
            	if str(s)=='False':
            		r='0'
                if str(s)=='True':
                	r='1'
        else:
            r = "'%s'"%s
        ss.append(r)
        data+='%s'%cL[0]+'='+"%s"%r+','
        i+=1 
        if dataType.find('rowversion')>-1: #时间该字段为时间戳，则记录
            end_rowversion=s
    data=data[:-1]        
    # cols = ','.join(col)  
    # s2 = ','.join(ss)
    
    sql="""UPDATE %s SET %s WHERE %s = %s
        """%(table_name, data, key,key_value)
    #print 'end_rowversion:%s'% end_rowversion
    sql = sql.replace(']','`')
    sql = sql.replace('[','`')
    sql = sql.replace('\\','\\\\')
    return sql,end_rowversion

if __name__ == "__main__":
    # db_local = byerp.cursor()   
    # db_local.execute("select * from users where usr_id = 1")  
    # for e in db_local.fetchall(): 
    #     print e[0]

    
    # sql = """INSERT users (usr_id,login_id,usr_name,pinyin,memo,password,status,contact,last_login,last_ip,use_count,cid,ctime,uid,utime,dept_id,e_mail,mobil,tel,birthday,job_img,pic,bbs_name,bbs_img,bbs_readme,bbs_doc_count,usr_pin,key_pin,key_sn,sex,qqmsn,addr,job,sort,cookid,s_password,id_no,pc,is_cxy,h_id,del_flag,s_login_id,epass_key,epass_seq,BBSElite,prestige,last_online,post,point,sys_usr_id,style,work_status,zhiwei,empl_id,s1,fp_code,login_mode,fp_pos,ls_type,usr_name2,old_dept_id,sc_key,upd_pw,upd_pw_time,s_passwrod,login_lock,login_lock_time,datasource) VALUES('1','cs','测试1212','','','123',0,'',NULL,'',NULL,'1','2016-12-12 10:12:50.157','1','2016-12-12 10:13:16.247','188','','','',NULL,'','','','','',NULL,'','','',NULL,'','','','1',NULL,'','','',NULL,NULL,NULL,'','','',NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'',NULL,'','','1','',NULL,'',NULL,'',NULL,NULL,'',NULL,NULL,1)"""
    # sql ="update users set login_id = 'x1xx' where usr_id=20000439"
    # r = local.executesql(sql) 
    # print r
    # sql = "select * from users"
    # rows,iN = local.select(sql)  
    # for e in rows:
    # 	print e[0]
    # sql = "select * from users where usr_id = 1"
    # rows,iN = byerp.select(sql)
    # for e in rows :
    #     print e[0]

    print "erp........"
    # for (table_erp,data_erp) in DD.items():  
    #   SourceDataBase = byerp
    #   field = data_deal(data_erp)
    #   # print table_erp
    #   #print field
    #   strlist = field.split(',')
    #   for value in strlist: 
    #       key = value #第一个为自增ID
    #       break
    #   maxID = Get_MaxID(table_erp,key,1)
    #   insertSql(table_erp,field,key,SourceDataBase,1,maxID) #写入数据(主系统)   

    # print "update.........." 
    # for (table_erp,data_erp) in DD.items():  
    #   SourceDataBase = byerp
    #   field = data_deal(data_erp)
    #   strlist = field.split(',')
    #   for value in strlist: 
    #       key = value #第一个为自增ID
    #       break
    #   id_list = GetUpdate(table_erp,key)
    #   if id_list !='':
	   #    updateSql(table_erp,field,key,SourceDataBase,1,id_list) #更新数据(主系统)
