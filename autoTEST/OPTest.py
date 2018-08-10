import requests
import numpy
import os
from os import path

import json
import pymssql
import XLSOP as X
class optest:
    '''
        自动测试接口类
    '''
    def __init__(self,js_path='cast.json'):
        self.js_path = js_path
        self.conn =self.conn_sql()
        self.jsons = self.get_json()
        self.itmes1 = self.get_all_item1()
    def get_json(self):
        '''
            处理需要测试的json数据
        '''
        with open(self.js_path,encoding='utf-8') as files:
            alls = json.load(files)
            # itmes = alls['item'][5]['item'][0]
            # itm = itmes['item'][0]
            # request = itm['request']
            # METHOD = request['method']
            # query = request['url']['query']
        return alls
    def conn_sql(self):
        '''
            连接数据库
        '''
        server,user = '192.168.20.151','platformuser'
        password,database= 'Zx123456','PLATFORM_OUTSIDE'
        conn = pymssql.connect(server, user, password, database)
        return conn
    
    def sql_data_map_col(self):
        '''
            返回数据表 字段名和对应的值（字典）
        '''
        names,datas = self.get_tb_colnums_name(),self.get_tb_data()
        fdata= []
        for i in datas:
            fdata.append(list(zip(names,i)))
        # print(fdata)
        # fdata = dict(fdata)
        return fdata
    def get_tb_colnums_name(self,tb_name='SYS_USER'):
        result = self.conn.cursor()
        result.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= '"+tb_name+"' ")
        alls =result.fetchall()
        names=[]
        for n in alls:
            names.append(n[3])
        return names

    def get_tb_data(self,tb_name='SYS_USER'):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM "+tb_name+" ")
        datas =cursor.fetchall()
        return datas
    
    def get_header(self,D):
        '''
            D == request
        '''
        return D['header'][0]
    
    def get_all_item1(self):

        return self.jsons['item']

    def get_all_item2(self,index):
        return self.itmes1[index]['item']
        
if __name__=='__main__':
    T= optest()
    D = T.jsons
    print(T.jsons.keys())
    print(len(D['item']))
    #T.get_all_item2(5)[0] 用户 
    # for x in T.get_all_item2(5):
    #     print(x['name'])
    requests = T.get_all_item2(5)[0]['item'][5]['request']
    raw = requests['body']['raw']
    d_raw = json.loads(raw)
    print(d_raw.values())
