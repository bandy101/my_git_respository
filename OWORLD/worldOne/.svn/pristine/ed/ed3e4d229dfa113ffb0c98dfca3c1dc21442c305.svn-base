# -*- coding: utf-8 -*-

import sys
import os,time
import json
# import pymssql
sys.path.append("/home/webroot/oWorld/common/")
# exec ('from share        import ToGBK')
# import MySQLdb
from HW_DB   import DataBaseParent_local,DataBaseParent_byerp,DataBaseParent_byaq
from HW_DT_TOOL                 import getToday
from HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG

#本地mysql数据库
local=DataBaseParent_local()  
#主系统MSSQL数据库
byerp = DataBaseParent_byerp()
byaq = DataBaseParent_byaq()

uc=unicode(str('s'), 'eucgb2312_cn')

#引入数据表
execfile('/home/webroot/oWorld/complaint/data/table.py')

def ToGBK(s):
    if type(s) != type(uc):
        return s
    try:
        s=str(s.decode("utf-8").encode("GBK"))
    except:
        s=s
    s = s.replace("\n","\r\n")
    return s

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
    #print src_total
    #print """%s:...."""%table
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
               #print 'fail__insert:',sql,time.ctime()
               # fileHandle.write(time.ctime()+':'+sql+"\r")  
               # exit()
               # writeLOG(log_file,sql)  
                pass
            #print '%s:insert___ok...source...%s...Data left:%s'%(table,datasource,src_total)
    else:
        #print "No data....!" 
        pass
    #print "------------------------------"    


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
    if table =='out_proj_tracking':
        sql+=""" and datasource=1"""
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
    if str_date=='' or str_date=='None' or str_date=='NULL' or str_date is None:
        return 'NULL'
    else:
        return """'%s'"""%str_date

#拼接update语句
def updateSql(table,field,key,SourceDataBase,datasource,id_list):    
    select_sql = selectSqlUpdate(table,key,id_list,datasource) #查询出需要更新的数据
    #print select_sql
    LT1 = ''
    LT1,iN1=SourceDataBase.select(select_sql)
    src_total=len(LT1)
    #print src_total
    #print """%s:...."""%table
    if src_total != 0 :
        for A in LT1 :
            src_total = src_total - 1
            #print """Data left : %s"""%(src_total)
            L = L_result_deal(list(A))
            L.append(datasource)
            L_ok = tuple(L)  

            sql,end_rowversion = updateSql_deal(table, L,datasource,key,A[0])
            #print sql 
            try:
                if sql: local.executesql(sql) 
            except:
                pass
               #print 'fail__update:',sql,time.ctime()
               # fileHandle.write(time.ctime()+':'+sql+"\r")  
               # exit()
               # writeLOG(log_file,sql)  
            #print '%s:update___ok...source...%s...Data left:%s'%(table,datasource,src_total)
    else:
        print "No data....!" 
    print "------------------------------"    

def GetUpdate(table,key):
    #查出最后更新时间
    sql="""select ctime from data_update_log order by id desc limit 1"""
    row,iN=local.select(sql)
    lastUtime=row[0][0]

    L =''
    sql = """select %s from %s where utime is not null """%(key,table)
    #获取当前日期
    # t=time.time()
    # date_ary=time.localtime(t)
    # x=time.strftime("%Y-%m-%d",date_ary)
    sql+="""and convert(varchar(19),utime,121)>'%s' """%lastUtime
    #print sql
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
             where %s in %s  
          """%(cols, table,key,id_list)
    # if table =='prj_mat_buy_ht':
    #     sql+="""and ISNULL(finish,0)=0 """
    sql+=""" order by %s"""%(key)
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

#组装查询语句
def selectSql_erp(table, sWhere='', orderby=''):
    col,LL = [],DD[table.lower()]
    if table in ['out_proj','labour_contract','labour_contract_invalid','prj_mat_buy_ht']:
        for L in LL:
            L=list(L) 
            if L[2]=='datetime':
                L[0]='CONVERT(NVARCHAR(23), FR.%s, 121)'%L[0]
            elif L[2]=='timestamp':
                L[0]='CONVERT(int, FR.%s)'%L[0]
            elif L[2]=='text':
                L[0]='CONVERT(VARCHAR(8000), FR.%s)'%L[0]  
            else:
                L[0]='FR.%s'%L[0]
            col.append(L[0])
        cols = ','.join(col)
        if table == 'out_proj':
            sql="""SELECT %s,convert(varchar(19),GETDATE(),121)
               FROM %s FR
               LEFT JOIN gw_doc g on FR.m_id = g.id
                 %s  --WHERE
                 %s  --ORDER BY
              """%(cols, table, sWhere, orderby)
        else:
            sql="""SELECT %s,convert(varchar(19),GETDATE(),121)
               FROM %s FR
               LEFT JOIN gw_doc g on FR.gw_id = g.id
                 %s  --WHERE
                 %s  --ORDER BY
              """%(cols, table, sWhere, orderby)
    else:
        for L in LL:
            L=list(L) 
            if L[2]=='datetime':
                L[0]='CONVERT(NVARCHAR(23), %s, 121)'%L[0]
            elif L[2]=='timestamp':
                L[0]='CONVERT(int, %s)'%L[0]
            elif L[2]=='text':
                L[0]='CONVERT(VARCHAR(8000), %s)'%L[0]       
            col.append(L[0])
        cols = ','.join(col)
         
        sql="""SELECT %s,convert(varchar(19),GETDATE(),121)
               FROM %s FR
                 %s  --WHERE
                 %s  --ORDER BY
              """%(cols, table, sWhere, orderby)
    #print sql
    return sql

#字符处理
def L_result_deal_erp(L):
    if (L is None) or (L=='NULL') or (L==''):
        if type(L)==type(1):
            L='NULL'
        else:
            L=''         
    if type(L)==type(uc):                
        L=L.encode('utf8')                
    if type(L)==type('a'):
        L=L.replace("'","''").strip()
    return L  

def insertSql_deal_erp(table_name, rL):
    col,LL=[],DD[table_name.lower()]
    ss=[]
    i=0
    end_rowversion=''
    for cL in LL:
        s = rL[i]
        i+=1 
        dataType=cL[2]
        if dataType.find('timestamp')>-1: #时间该字段为时间戳，则记录
            end_rowversion=s
            continue
        col_name = cL[0]
        col.append(col_name)
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
            
    cols = ','.join(col)  

    s2 = ','.join(ss)
    sql="""INSERT %s (%s) VALUES (%s)
        """%(table_name, cols, s2)
    #print 'end_rowversion:%s'% end_rowversion
    sql = sql.replace(']','`')
    sql = sql.replace('[','`')
    sql = sql.replace('\\','\\\\')
    return sql,end_rowversion

def updateSql_deal_erp(table_name, rL,where):
    col,LL=[],DD[table_name.lower()]
 
    ss=[]
    i=0
    data = ''
    end_rowversion=''
    for cL in LL:
        s = rL[i]
        i+=1 
        dataType=cL[2]
        if dataType.find('timestamp')>-1: #时间该字段为时间戳，则记录
            end_rowversion=s
            continue
        col_name = cL[0]
        col.append(col_name)
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
        data+='%s'%col_name+'='+"%s"%r+','
    data=data[:-1]        

    # cols = ','.join(col)  
    # s2 = ','.join(ss)
    sql="""UPDATE %s SET %s %s
        """%(table_name, data, where)
    #print 'end_rowversion:%s'% end_rowversion
    sql = sql.replace(']','`')
    sql = sql.replace('[','`')
    sql = sql.replace('\\','\\\\')
    return sql,end_rowversion

## *** 同步时调用的方法 增加与修改  
def exec_synchro_addAupd_from_erp_to_local():  
    sql="""SELECT id, table_EN_name, end_rowversion, identity_key,last_synchro_time
          FROM z_synchro_table 
          WHERE status=1
          ORDER BY id
       """ 
    lT,iN=local.select(sql)
    n=0
    for e in lT:
        table_id, table_name, start_rowversion, identity_key ,last_synchro_time =  e
        #print 'table_id:%s, table_name:%s'%(table_id, table_name)
      
        if start_rowversion is None or start_rowversion=='':   #从未通讯，则拿全部
            sWhere = " WHERE 1=1 "
            orderby = ' ORDER BY FR.id ASC' 
        else:         
            if table_name in ['out_proj','labour_contract','labour_contract_invalid','prj_mat_buy_ht']:
                sWhere = " WHERE (isnull(g.cur_flow_time,g.ctime) >='%s' or isnull(FR.utime,FR.ctime)>='%s') and g.finish=1"%(last_synchro_time,last_synchro_time)
                orderby = ' ORDER BY g.ctime ASC'
            else:
                sWhere = " WHERE RV >=%s"%(start_rowversion)
                orderby = ' ORDER BY RV ASC'
       
        sql_1 = selectSql_erp(table_name, sWhere, orderby)  #获取 组装查询sql 
        print sql_1
        lT1,iN1=byerp.select(sql_1)
        src_total=len(lT1)
        end_rowversion='NULL'
        m=0
        print src_total
        if src_total!=0:
            for A in lT1: 
                L = L_result_deal_erp(list(A)) 
                sql = ''
                where ="WHERE %s='%s'"%(identity_key,L[0])
                sql_2 = "SELECT %s FROM %s %s"%(identity_key, table_name,where)
              
                lT2,iN2 = local.select(sql_2)
                if iN2>0:
                    sql,end_rowversion = updateSql_deal_erp(table_name, L, where)
                else:
                    sql,end_rowversion = insertSql_deal_erp(table_name, L)
                try:
                    if sql: local.executesql(sql) 
                except:
                    #print ToGBK(sql), time.ctime()
                    pass
                m+=1
                #end_rowversion=L[-1]
        else:
            end_rowversion=start_rowversion or 'NULL'
        if end_rowversion == '': end_rowversion = int(time.time())
        if src_total>0:
            last_synchro_time = lT1[0][-1] 
            sql="UPDATE z_synchro_table SET end_rowversion=%s,syn_count=%s, last_synchro_time='%s' WHERE id=%s"%(end_rowversion,src_total,last_synchro_time,table_id)
            #print sql
            local.executesql(sql)
    return

def syncInvoiceData():
    sql="""select id,gw_id,req_no,pjname,gysname,sh_yf,prj_id,Sup_id,is_from_hxsh from prj_mat_pay where wx_list_status in (1,3)
       """ 
    lT,iN=byaq.select(sql)

    for A in lT: 
        L = L_result_deal_erp(list(A)) 
        
        sql = ''
        where ="WHERE id='%s'"%(L[0])
        sql_2 = "SELECT id FROM prj_mat_pay1 %s"%(where)
        lT2,iN2 = local.select(sql_2)
        if iN2==0:
            sql = """insert into prj_mat_pay1 (id,gw_id,req_no,pjname,gysname,sh_yf,prj_id,Sup_id,uuid,is_from_hxsh) values (%s,%s,'%s','%s','%s','%s',%s,%s,REPLACE(UUID(),'-',''),%s)
                  """%(L[0],L[1],L[2],L[3],L[4],L[5],L[6],L[7],L[8])
        else:
            sql = """update prj_mat_pay1 set gw_id=%s,req_no='%s',pjname='%s',gysname='%s',sh_yf='%s',prj_id=%s,Sup_id=%s,is_from_hxsh=%s %s
                  """%(L[1],L[2],L[3],L[4],L[5],L[6],L[7],L[8],where)
        try:
            if sql: local.executesql(sql) 
        except:
            #print ToGBK(sql), time.ctime()
            pass
        sql = """update prj_mat_pay1 mp,suppliers su set mp.gysct = su.gysct,mp.gys_tel = su.tel
                 where mp.Sup_id = su.id and mp.id=%s"""%(L[0])
        local.executesql(sql) 
        
        sql = "select uuid from prj_mat_pay1 where id=%s"%(L[0])
        lT2,iN2 = local.select(sql)
        if iN2==0:
            uuid = ''
            continue 
        else:
            uuid = lT2[0][0]

        #同步明细表    
        sql2 = """where M_Id in (0,"""
        sql = "select PMB_id from prj_mat_pay_buy where m_id = %s"%(L[0])
        lT1,iN1=byaq.select(sql)
        for e in lT1:
            sql2 += "%s,"%e[0]
        sql2=sql2[:-1]    
        sql2 += ")"
        sql = "delete from prj_mat_list %s "%(sql2)
        local.executesql(sql) 

        sql1 = """select l.id,l.m_id,m.rec_date,m.Out_No,l.mat_name,isnull(l.Spec,'') + ' ' + isnull(l.Model,''),u.cname,l.act_price,l.Check_Amc,l.act_money from Prj_Mat_List l
                  left join Prj_Mat_Master m on m.id = l.m_id
                  left join units u on u.id =l.unit
                  %s and isnull(mat_status,0) != 2"""%(sql2)
        lT1,iN1=byerp.select(sql1)
        for A1 in lT1: 
            L1 = L_result_deal_erp(list(A1)) 
            sql = """insert into Prj_Mat_List (id,m_id,rec_date,Out_No,mat_cname,spec,unit,act_price,Check_Amc,act_money,pmp_id) 
                     values (%s,%s,'%s','%s','%s','%s','%s',%s,%s,%s,%s)
                  """%(L1[0],L1[1],L1[2],L1[3],L1[4],L1[5],L1[6],L1[7],L1[8],L1[9],L[0])
            try:
                #print ToGBK(sql)
                if sql: local.executesql(sql) 
            except:
                #print ToGBK(sql), time.ctime()
                #print sql
                pass

        #同步其他费用表    
        sql2 = """where M_Id in (0,"""
        sql3 = """where pb.id in (0,"""
        sql = "select PMB_id from prj_mat_pay_buy where m_id = %s"%(L[0])
        lT1,iN1=byaq.select(sql)
        for e in lT1:
            sql2 += "%s,"%e[0]
            sql3 += "%s,"%e[0]
        sql2=sql2[:-1]    
        sql2 += ")"
        sql3=sql3[:-1]    
        sql3 += ")"
        sql = "delete from Prj_Mat_Master_other where pmp_id = %s "%(L[0])
        #print sql
        local.executesql(sql) 

        sql1 = """SELECT    PL.id,pb.id,
                    convert(varchar(10),PL.ctime,121), 
                    CW1.cname,                        
                    CW2.cname,                     
                    PL.amount                       
            FROM Prj_Mat_Master_other PL
            LEFT JOIN Prj_Mat_Master pb ON pb.gw_id = PL.gw_id
            LEFT JOIN cw_sort CW2 ON CW2.code=PL.U_type
            LEFT JOIN cw_sort CW1 ON  CW1.id=CW2.p_id
                  %s """%(sql3)
        lT1,iN1=byerp.select(sql1)
        for A1 in lT1: 
            L1 = L_result_deal_erp(list(A1)) 
            sql = """insert into Prj_Mat_Master_other (id,m_id,ctime,b_type,l_type,money,pmp_id) 
                     values (%s,%s,'%s','%s','%s','%s',%s)
                  """%(L1[0],L1[1],L1[2],L1[3],L1[4],L1[5],L[0])
            try:
                #print ToGBK(sql)
                if sql: local.executesql(sql) 
            except:
                pass

        #推送给供应商
        sql = """select UG.openid FROM USERS_GY UG LEFT JOIN ADDR_BOOK AB ON AB.ID=UG.ADDR_ID LEFT JOIN SUPPLIERS SP ON SP.ID=AB.SUP_ID WHERE UG.status =1 and sp.id=%s"""%(L[7])
        #sql = """select UG.openid FROM USERS_GY UG LEFT JOIN ADDR_BOOK AB ON AB.ID=UG.ADDR_ID LEFT JOIN SUPPLIERS SP ON SP.ID=AB.SUP_ID WHERE UG.nickname like '%滤色镜%'"""
        #print sql
        lT2,iN2 = local.select(sql)
        if iN2 ==0 : #推送失败      
            sql = "update prj_mat_pay set wx_list_status = 5 where id = %s"%(L[0])
            #print sql
            byaq.executesql(sql) 
        else:
            ret = -1
            for e in lT2:
                toUser = e[0] 
                #print toUser
                errcode = mWxPushMsg_fw_gy(uuid,toUser)
                if errcode == 0: ret = 0
            #print errcode
            if ret == 0:
                sql = "update prj_mat_pay set wx_list_status = 2 where id = %s"%(L[0])
            else:
                sql = "update prj_mat_pay set wx_list_status = 5 where id = %s"%(L[0])
                ret = errcode
            #print sql
            byaq.executesql(sql) 
            sql = "update prj_mat_pay1 set push_time=now(),errcode=%s where id = %s"%(ret,L[0])
            local.executesql(sql) 

    return

m_sCorpID = "wxc6d740ece61b7ec1"
m_sCorpSecret_lw = "xNntgqKZxJmpZWmHJWNL6ev4u2ylp7BjwJS1VUQ9tgM"
m_sAgentId_lw = "1000002"
#劳务企业号
def write_access_token_lw(access_token):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token_lw')
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token_lw():
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token_lw')
    access_token = openTXT(log_file)
    if access_token=='':
        return ''

    ddata=json.loads(access_token)
    token =  ddata['access_token'] 
    if  token !='' :  
        t1 = ddata['time'] 
        t=time.time() 
        if (t - t1)<7000:
            return token
    return ''

def pushProgress():
    sql = """select pd.id,UX.usr_name,OP.cname,pd.cur_progress,pd.ctime
            FROM progress_declare pd 
            LEFT JOIN users_wx UX ON UX.usr_id = pd.cid
            LEFT JOIN out_proj OP ON OP.id = pd.proj_id
            where pd.status =0 and pd.alert_leader = 0 and TIMESTAMPDIFF(DAY,pd.ctime,now())>2;"""
    #print sql
    lT,iN = local.select(sql)

    sToken =  read_access_token_lw()
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_lw)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_lw(body)

    
    for e in lT:    
        id = e[0]
        cusrname = e[1]  
        proj_name = e[2]
        cur_progress = e[3]
        ctime = e[4]
        toUser = '|mengxp|zhongzhg|hanruiming'
        toUser += '|lishijie'
        sUrl='http://lw.szby.cn/complaint/login/login_qy?fid=uploadDetail&path=ProjPay&seq=%s'%(id)
        stitle = u"""进度款上报提醒"""
        description = u"""上报人:%s
上报项目：%s
上报进度：%s%%
上报日期：%s

该申请已上报三天未处理，请查阅并协助申请进度款！"""%(cusrname,proj_name,cur_progress,ctime)
    # print toUser
        stitle=json.dumps(stitle)
        description = json.dumps(description)
        sMsg ="""{
              "touser": "%s",
                     """%(toUser)
        sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_lw,stitle,sUrl,description)
        #print sMsg

        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/message/send?access_token=%s"%(sToken)
        #print url
        conn.request('POST', '%s'%url,sMsg)  

        res = conn.getresponse()       
        body = res.read()  
        conn.close()  

        ddata=json.loads(body)
        errcode = ddata['errcode']    
        errmsg = ddata.get('errmsg','')
        sql = "update progress_declare set alert_leader = 1 where id=%s"%(id)
        local.executesql(sql)
        sql = """insert into progress_push_log (pd_id, recv_users, push_time, errcode, msg, iType) 
                 VALUES (%s, '%s', now(), %s, '%s', 1);"""%(id,toUser,errcode,errmsg)
        local.executesql(sql)
    return

def write_access_token_common(access_token,itype):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/%s'%itype)
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token_common(itype):
    log_file=os.path.join('/home/webroot/oWorld/complaint/%s'%itype)
    access_token = openTXT(log_file)
    if access_token=='':
        return ''

    ddata=json.loads(access_token)
    token =  ddata['access_token'] 
    if  token !='' :  
        t1 = ddata['time'] 
        t=time.time() 
        if (t - t1)<7000:
            return token
    return ''

template_id = 'hxpG0gof0Lci-sgfWoKa0BgcTHbPRq734rCzLaxLFPA'
AppId_gy = 'wxe703baaad2a1c9dc'
AppSecret_gy = '780065948cba96c5831c6b047a0ff7f8'
import httplib
def mWxPushMsg_fw_gy(pk,toUser):   
    now=getToday()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken =  read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')

    sql = "select pjname,sh_yf,gysname from prj_mat_pay1 where uuid='%s'"%(pk)
    lT,iN = local.select(sql)
    if iN == 0:
        return -1

    sUrl='http://lw.szby.cn/lwerp/lw/src/html/receiptList.html?seq=%s'%(pk)
    description="""感谢您的查看。"""
    stitle = """亲爱的合作伙伴，您现在收到的是本项目需开票的相关信息，请确认。"""
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    pjname = json.dumps("%s %s"%(lT[0][0],u' 项目部'))
    sh_yf = json.dumps(lT[0][1])
    gysname = json.dumps(lT[0][2])

    sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "url":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#173177"
            },
            "keyword1": {
            "value":%s,
            "color":"#173177"
            },
            "keyword2": {
            "value":%s,
            "color":"#173177"
            },
            "keyword3": {
            "value":%s,
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }

            }
            }
    """%(toUser,template_id,sUrl,stitle,pjname,sh_yf,gysname,description)
    print sMsg 
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return errcode

def mWxPushMsg_fw_gy_cgd(pk):  
    users = ''
    sup_name = ''
    sql = """select op.cname,cg.sup_id,cg.sn,su.cname from _m1501_cgdd cg
                 left join out_proj op on cg.proj_id = op.id
                 left join suppliers su on cg.sup_id = su.id
                 where cg.id=%s"""%(pk)
    print sql
    rows,iN = local.select(sql)
    if iN > 0:
        proj_name = rows[0][0]
        sup_id = rows[0][1]
        sn = rows[0][2]
        sup_name = rows[0][3]
        sql = """select GROUP_CONCAT(u.openid) from users_gy u 
                     left join addr_book ab on u.addr_id = ab.id
                     where ab.sup_id = %s and u.status = 1"""%(sup_id)
        rows1,iN1 = local.select(sql)
        users = rows1[0][0]

 
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken =  read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    template_id = 'Vctkp00KQC21rJHLRUM0WfdqBRJR8k-zzK8deXu6I54'
    stitle ="""您提交的材料确认表已确认。"""
    stitle=json.dumps(stitle)
    keyword1 = json.dumps(sup_name)
    keyword2 = json.dumps("%s--%s"%(proj_name,sn))
    remark = json.dumps("请您登陆【供应商服务平台】进行送货单打印，并把打印的单据与货物一并提交给项目仓管。")
    for e in users.split(','):
        sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#ff0000"
            },
            "keyword1": {
            "value":%s,
            "color":"#173177"
            },
            "keyword2": {
            "value":%s,
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }
            }
            }
        """%(e,template_id,stitle,keyword1,keyword2,remark)

        conn = httplib.HTTPSConnection('api.weixin.qq.com')  
        url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
        #print url
        conn.request('POST', '%s'%url,sMsg)  
        res = conn.getresponse()       
        body = res.read()  
        print body
        conn.close()  
        ddata=json.loads(body)
        errcode = ddata['errcode']
        errmsg = ddata['errmsg']

    return 

def mWxPushMsg_fw_gy_rkd(pk):  
    users = ''
    rk_time = ''
    sql = """select op.cname,cg.sup_id,sh.sn,now() 
                 from _m3000004_shd sh 
                 left join _m1501_cgdd cg on sh.cgd_id = cg.id
                 left join out_proj op on cg.proj_id = op.id
                 left join suppliers su on cg.sup_id = su.id
                 where sh.id = %s"""%(pk)
    print sql
    rows,iN = local.select(sql)
    if iN > 0:
        proj_name = rows[0][0]
        sup_id = rows[0][1]
        sn = rows[0][2]
        rk_time = rows[0][3]
        sql = """select GROUP_CONCAT(u.openid) from users_gy u 
                     left join addr_book ab on u.addr_id = ab.id
                     where ab.sup_id = %s and u.status = 1"""%(sup_id)
        rows1,iN1 = local.select(sql)
        users = rows1[0][0]

 
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken =  read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    template_id = 'd5E5geMETzRH7vII9lmlqR1QFKSIsMSG9gb9W4Zj9F4'
    stitle ="""您提交的送货单已完成入库，请您在每月25日后，在【供应商服务平台】发起对账申请。"""
    stitle=json.dumps(stitle)
    keyword1 = json.dumps("%s--%s"%(proj_name,sn))
    remark = json.dumps("感谢您对本公司的支持。")
    for e in users.split(','):
        sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#008000"
            },
            "keyword1": {
            "value":%s,
            "color":"#173177"
            },
            "keyword2": {
            "value":"%s",
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }
            }
            }
        """%(e,template_id,stitle,keyword1,rk_time,remark)

        conn = httplib.HTTPSConnection('api.weixin.qq.com')  
        url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
        #print url
        conn.request('POST', '%s'%url,sMsg)  
        res = conn.getresponse()       
        body = res.read()  
        print body
        conn.close()  
        ddata=json.loads(body)
        errcode = ddata['errcode']
        errmsg = ddata['errmsg']

    return 

#同步采购单状态
def syncCgd():
    sql = "select id,cgd_gwid from _m1501_cgdd where status1 = 4"
    lT,iN=local.select(sql)
    for e in lT:
        id = e[0]
        gw_id = e[1]
        sql = "select finish from gw_doc where id=%s"%(gw_id)    
        lT1,iN1=byerp.select(sql)
        if iN1 == 0:  #删除
            sql="update _m1501_cgdd set status1 = 1,cgd_gwid=NULL,cgd_id=NULL,cgd_no='' where id =%s"%(id)
            local.executesql(sql) 
            sql="update _m1501_cgsq set gw_id=NULL,status=0 where id =%s"%(id)
            local.executesql(sql) 
        else:
            if lT1[0][0] == 1: #办结
                #通知供应商
                mWxPushMsg_fw_gy_cgd(id)
                sql="update _m1501_cgdd set status = 6,status1 = 3 where id =%s"%(id)
                local.executesql(sql)
    sql = "select id,rk_gwid from _m3000004_rkd where status = 1"
    lT,iN=local.select(sql)
    for e in lT:
        sql = "select finish from gw_doc where id=%s"%(e[1])    
        lT1,iN1=byerp.select(sql)
        if iN1 == 0:  #删除
            sql="update _m3000004_rkd set status = 0,rk_gwid=NULL,rk_id=NULL,req_no='' where id =%s"%(e[0])
            local.executesql(sql) 
            sql="update _m3000004_shd set rkd_gwid=NULL,rkd_id=NULL,rkd_no='',status=0 where id =%s"%(e[0])
            local.executesql(sql) 
        else:
            if lT1[0][0] == 1: #办结
                #通知供应商
                mWxPushMsg_fw_gy_rkd(e[0])
                sql="update _m3000004_rkd set status = 2 where id =%s"%(e[0])
                local.executesql(sql)
                sql="update _m3000004_shd set status = 2 where id =%s"%(e[0])
                local.executesql(sql)

    return 

#更新材料款付款信息
def updateClkInfo():
    sql = "select id,cgd_gwid from _m1501_cgdd where status1 = 4 "
    lT,iN=local.select(sql)
    
    return 

if __name__ == "__main__":
    #获取当前日期
    t=time.time()
    date_ary=time.localtime(t)
    x=time.strftime("%Y-%m-%d",date_ary)
    y=time.strftime("%Y-%m-%d %T",date_ary)    
    print x
    exec_synchro_addAupd_from_erp_to_local()

    '''sql = "select id from labour_contract_invalid"
    lT,iN = local.select(sql)
    for e in lT:
        id = e[0]
        sql = "select id from labour_contract_invalid where id=%s"%(id)
        lT1,iN1 = byerp.select(sql)
        if iN1 == 0:
            sql = "delete from labour_contract_invalid where id=%s"%(id)
            print sql
            local.executesql(sql) 
    '''
    #print "erp........"


    sql="""SELECT GROUP_CONCAT(table_EN_name separator ",")
          FROM z_synchro_table 
          WHERE status=1
       """ 
    lT,iN=local.select(sql)
    tables = lT[0][0]
    tables = tables.split(',')
    tables.append('empl_job')
    tables.append('out_proj_tracking')
    for (table_erp,data_erp) in DD.items():  
        #print table_erp
        if table_erp not in tables:
            SourceDataBase = byerp
            field = data_deal(data_erp)
            strlist = field.split(',')
            for value in strlist: 
                key = value #第一个为自增ID
                break
            maxID = Get_MaxID(table_erp,key,1)
            insertSql(table_erp,field,key,SourceDataBase,1,maxID) #写入数据(主系统)   

    #print "update erp.........." 
    for (table_erp,data_erp) in DD.items():  
        if table_erp not in tables:
            SourceDataBase = byerp
            field = data_deal(data_erp)
            strlist = field.split(',')
            for value in strlist: 
                key = value #第一个为自增ID
                break
            id_list = GetUpdate(table_erp,key)
            if id_list !='':
                updateSql(table_erp,field,key,SourceDataBase,1,id_list) #更新数据(主系统)

    #print "aq........"
    for (table_aq,data_aq) in AQ.items():  
        SourceDataBase = byaq
        field = data_deal(data_aq)
        strlist = field.split(',')
        for value in strlist: 
            key = value #第一个为自增ID
            break
        maxID = Get_MaxID(table_aq,key,2)
        insertSql(table_aq,field,key,SourceDataBase,2,maxID) #写入数据(财务)   

    #print "update aq.........." 
    for (table_aq,data_aq) in AQ.items():  
        SourceDataBase = byaq
        field = data_deal(data_aq) 
        strlist = field.split(',')
        for value in strlist: 
            key = value #第一个为自增ID
            break
        id_list = GetUpdate(table_aq,key)
        if id_list !='':
            updateSql(table_aq,field,key,SourceDataBase,2,id_list) #更新数据(主系统)
            
    sql="""INSERT INTO data_update_log(ctime,ctime1) VALUES('%s','%s')"""%(x,y)
    local.executesql(sql) 
    #print 'success...'

    #同步需要推送发票清单的数据
    syncInvoiceData()

    #定期推送未处理的进度款上报记录
    cur_hour = time.strftime('%H',time.localtime())
    if int(cur_hour) == 15:
        pushProgress()
    
    syncCgd()
    updateClkInfo()

