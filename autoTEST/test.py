from OPTest import optest
import XLSOP as X 



if __name__ =='__main__':
    T= optest()
    #T.get_all_item2(5)[0] 用户 
    requests = T.get_all_item2(5)[0]['item'][0]['request']
    query = requests['url']['query']
    # print(len(requests))
    method = requests['method']
    header = requests['header'][-1]
    fdata =T.sql_data_map_col()
    f_param=[]
    for q in query:
        try:
            value = dict(fdata[0])[q['key'].upper()]
            if value ==None:
                value=''
            f_param.append((q['key'],value))
        except:
            pass
    d_f_param =dict(f_param)
    X.start(1,paramer=d_f_param)
    print(header)