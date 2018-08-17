from OPTest import optest
import XLSOP as X 
import xlwt
from openpyxl.writer.excel import ExcelWriter 
import json
if __name__ =='__main__':
    T= optest()
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    test_num = 0
    global index
    index = 1  #插入数据的行所以
    #T.get_all_item2(5)[0] 用户
    for i  in T.get_all_item2(5)[0]['item']:
        test_num +=1
        # if test_num>6:break
        print(i['name'])
        sheet.write(index-1,0,i['name'])
        requests = i['request']
        interface = requests['url']['path'][2]
        path_num = len(requests['url']['path'])
        method = requests['method']
        header = requests['header'][-1]
        fdata =T.sql_data_map_col()
        if  method =='GET' or  method=='get':
            have_query = 'query' in requests['url'].keys()
            # print('have_query:',have_query)
            if have_query:
                url = X.prex+interface
                query = requests['url']['query']
                head=[]
                for q in query:
                    head.append(q['key'])
                # head.append('pageNum')
                # head.append('pageSize')
                url = X.prex+interface
                nums = 0
                need_head =True
                print('database size:',len(fdata))
                for d in fdata:
                    d = dict(d)
                    parms = []
                    nums +=1
                    if nums>5:break
                    values = []
                    # 将数据表中对应的head 数据提取出来
                    for hd in head:
                        if hd.upper() in d.keys():
                            values = d[hd.upper()]
                            parms.append((hd,values))
                        else:
                            if hd =='userType':
                                parms.append((hd,d['USER_TYPE']))
                            if hd =='userName':
                                parms.append((hd,d['NAME']))
                            if hd =='pageNum':
                                parms.append((hd,1))
                            if hd =='pageSize':
                                parms.append((hd,30))
                    parms = dict(parms)
                    print('parms:',parms.values())
                    res,is_ok,date = X.commit(url,parms,method)
                    if need_head:
                        X.xls_add_head(head,sheet,index)
                        index +=1
                        need_head =False
                    X.xls_add_data(parms.values(),sheet,is_ok,date,index)
                    index +=1
                    # print('index:',index)
                index +=3
                need_head =True
            else:
                print('index:',index)
                url = X.prex+interface
                if path_num>3:
                    urls = X.prex+interface+'/'
                    nums =0
                    for d in fdata:
                        d = dict(d)
                        nums +=1
                        if nums>3:break
                        url =urls+d['ID']
                        print(url)
                        parms={}
                        res,is_ok,date = X.commit(url,parms,method)
                        head =[]
                        head.append('ID')
                        print('index:',index)
                        if need_head:
                            X.xls_add_head(head,sheet,index)
                            index +=1 
                            need_head =False
                        values = []
                        values.append(d['ID'])
                        X.xls_add_data(values,sheet,is_ok,date,index)
                        index +=1
                    index +=3
                    need_head =True
                else :
                    res,is_ok,date = X.commit(url,parms,method)
                    head =[]
                    X.xls_add_head(head,sheet,index)
                    index +=1
                    parms={}
                    X.xls_add_data(parms.values(),sheet,is_ok,date,index)
                    index +=1
                index +=3
                need_head =True
        if  method =='POST' or method=='PUT':
            raw = requests['body']['raw']
            d_raw = json.loads(raw)
            key_v = list(d_raw.keys())[0]
            urls = X.prex+interface
            if method =='POST':
                for _ in range(3):
                    d_raw[key_v]='Test-'+str(_)
                    res,is_ok,date = X.commit(urls,d_raw,method)
                    if need_head:
                        X.xls_add_head(d_raw.keys(),sheet,index)
                        index +=1
                        need_head =False
                    X.xls_add_data(d_raw.values(),sheet,is_ok,date,index)
                    index +=1
                index +=3
                need_head =True
            if method =='PUT':
                ids =[]
                for d in fdata:
                    d = dict(d)
                    if (d['ID']!=1 and  d['ID']!=3):
                        print(type(d['ID']))
                        ids.append(d['ID'])
                print('ids:',ids)
                # for _ in range(3):
                #     d_raw['name']='Test-'+str(_)
                #     url = urls+'/'+ids[_]
                #     res,is_ok,date = X.commit(url,d_raw,method)
                #     if need_head:
                #         X.xls_add_head(d_raw.keys(),sheet,index)
                #         index +=1
                #         need_head =False
                #     X.xls_add_data(d_raw.values(),sheet,is_ok,date,index)
                #     index +=1
                # index +=3
                # need_head =True
    
    wbk.save('test.xls')

                    

