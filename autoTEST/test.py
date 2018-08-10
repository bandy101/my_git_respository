from OPTest import optest
import XLSOP as X 



if __name__ =='__main__':
    T= optest()
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    index = 0  #插入数据的行所以
    #T.get_all_item2(5)[0] 用户 
    for i  in T.get_all_item2(5)[0]['item']:
        print(i['name'])
        requests = i['request']
        interface = requests['path'][2]
        path_num = len(requests['path'])
        method = requests['method']
        header = requests['header'][-1]
        fdata =T.sql_data_map_col()
    # requests = T.get_all_item2(5)[0]['item'][0]['request']
        have_query = 'query' in requests.keys()
        if have_query:
            url = X.prex+interface
            query = requests['url']['query']
            head=[]
            for q in query:
                head.append(q['key'])
            head.append('pageNum')
            head.append('pageSize')
            url = X.prex+interface
            for d in fdata:
                parms = []
                nums +=1
                if nums>5:break
                values = []
                for hd in head:
                    if hd.upper() in d.keys():
                        values = d[hd.upper()]
                        parms.append((hd,values))
                parms = dict(parms)
                res,is_ok,date = X.commit(url,parms,method)
                X.xls_add_head(head,sheet,index)
                X.xls_add_data(parms.values(),sheet,is_ok,date,index+1)
                index +=1
            index +=3
        else:
            url = X.prex+interface
            if path_num>3:
                url = X.prex+interface+'/'
                nums =0
                for d in fdata:
                    nums +=1
                    if nums>5:break
                    url =url+d['ID']
                    

