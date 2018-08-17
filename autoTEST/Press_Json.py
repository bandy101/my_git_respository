import json
import XLSOP as X 
from openpyxl.writer.excel import ExcelWriter 
from OPTest import optest

with open('cast.json',encoding='utf-8') as files:
    alls = json.load(files)
    req = alls['requests']
def search(name):
    for N in alls['folders']:
        if N['name']==name:
            folders_order = N
            break
    return N['id']
## 获取对应文件夹ID##
def get_folder_id(folder_name):
    folder_id = search(folder_name)
    return folder_id

##获取对应文件夹的所有接口（用户）##
def get_interface(user): 
    '''
        param:@user:文件夹 id
    '''
    users =[]
    for i in req:
        # print(i['id'])
        if i['folder']==user:
            users.append(i)
    return users


def auto_test(name_i,sql,index):
    global index
    T= optest()
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')

    values = get_interface(name_i)
    for i in values:
        sheet.write(index-1,0,i['name'])
        url,method,rawModeData= i['url'],i['method'],json.loads(i['rawModeData'])
        queryParams ,urls=[] ,url.split('?')[0].split('/')
        purl = X.prex +urls[3]
        fdata =sql.sql_data_map_col()
        for _ in i['queryParams']:
            queryParams.append((_['key'],_['value']))
        queryParams =dict(queryParams)
        head=[]
        for q in dict(queryParams).keys():
            head.append(q)
        for hd in head:
            if hd.upper() in d.keys():
                queryParams[hd] = d[hd.upper]
            ##queryParams对应的key不存在于数据库字段中
            else:
                pass


        if method=='GET':##x``
            if queryParams:
                url =purl
                res,is_ok,date = X.commit(url,queryParams,method)

                X.xls_add_head(head,sheet,index)
                index +=1
                X.xls_add_data(queryParams.values(),sheet,is_ok,date,index)
                #测试从数据库中导入的数据
                num = 3 #测试的次数
                for d in fdata:
                    d =dict(d)
                    num -=1
                    if not num:break

                    res,is_ok,date = X.commit(url,queryParams,method)
                    X.xls_add_data(queryParams.values(),sheet,is_ok,date,index)
                    index +=1
                index +=3
             #不存在queryParams           
            else:
                ##两种情况不存在queryParams（1：通过id的操作，2：获取全部的操作)
                if len(urls)>3:##1
                    X.xls_add_head(['id'],sheet,index)
                    index +=1
                    num =3#查询次数
                    for d in fdata:
                        d = dict(d)
                        num -=1
                        if not num:break
                        url = purl +'/'+d['ID']
                        res,is_ok,date = X.commit(url,queryParams,method)
                        values = []
                        values.append(d['ID'])
                        X.xls_add_data(values,sheet,is_ok,date,index)
                        index +=1
                    index +=3
                else:#2
                    url = purl
                    res,is_ok,date = X.commit(url,queryParams,method)
                    X.xls_add_head([],sheet,index)
                    index +=1
                    X.xls_add_data([],sheet,is_ok,date,index)
                    index +=1
                    index +=3
        if method=='POST'
if __name__=='__main__':
    global index
    index =1
    fid = get_folder_id('遥感监测站')
    users = get_interface(fid)
    print(len(users))
