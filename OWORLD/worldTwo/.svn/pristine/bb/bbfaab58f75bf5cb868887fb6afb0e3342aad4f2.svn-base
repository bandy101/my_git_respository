# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]

exec ('from %s.share        import db,ToGBK,m_prjname,HttpResponseCORS,mValidateUser'%prj_name) 
import json
import MySQLdb
# workbook相关
from openpyxl.workbook import Workbook
# ExcelWriter，封装了很强大的excel写的功能
from openpyxl.writer.excel import ExcelWriter
# 一个eggache的数字转为列字母的方法
from openpyxl.utils import get_column_letter
from openpyxl.reader.excel import load_workbook

from common import packPara,addtwodimdict
from django.http import StreamingHttpResponse  

def exportExcel(request):
    menu_id = request.POST.get('menu_id','')
    ret,errmsg,d_value = mValidateUser(request,"view",menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    sql = " select menu_name from menu_func where menu_id=%s"%menu_id
    rows,iN = db.select(sql)
    title = rows[0][0]    

    L,NL = getListData(request,d_value)
    save_name = "/tmp/%s.xlsx"%usr_id
    exportFields = request.POST.get('exportFields', '')
    #print "create handle Excel Object"
    obj_handle_excel=HandleExcel()
    obj_handle_excel.write_to_excel_with_openpyxl(L,NL,exportFields,save_name,title)

    response = StreamingHttpResponse(file_iterator(save_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s.xlsx"'%(menu_id)

    return response

def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def getListData(request,d_value):
    menu_id = request.POST.get('menu_id', '')
    usr_id = d_value[0]
    dept_id = d_value[2]

    #print request.POST
    tab = request.POST.get('tab', '')
    data = request.POST.get('data', '{}')
    data_list = json.loads(data)
    aoData= request.POST.get('aoData', '')
    value_dict = dict()    
    sUrl = ''
    sql = " select gw_type2 from menu_data_source where menu_id=%s"%menu_id
    rows,iN = db.select(sql)
    gw_type = rows[0][0]
    value_dict['type_id'] = gw_type

    if usr_id in [1,2]:
       sql = "select mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp where  mp.menu_id=%s and mp.status=1 order by mp.sort"%menu_id
    else:
        sql = """select DISTINCT mp.page_name,mp.label,mp.sort,'',mp.has_add,'',mp.id from menu_list_pages mp 
                    left join role_menu rm on  rm.menu_id= mp.menu_id
                    left join usr_role ur on rm.role_id = ur.role_id
                    where mp.menu_id=%s and mp.status=1 and ur.usr_id = %s and FIND_IN_SET(mp.id,rm.tabs) order by sort"""%(menu_id,usr_id)
    TL,iN = db.select(sql)
    for n in range(0,len(TL)):
        if n==0 and tab=='':
            tab = TL[0][0]

    #获取当前页数据的参数
    sql = "select id,final_sql,ifnull(list_order,''),search_sql from menu_list_pages where menu_id=%s and page_name='%s'"%(menu_id,tab)
    TL,iN = db.select(sql)
    page_id = TL[0][0]
    final_sql = TL[0][1]
    list_order = TL[0][2] or ''
    search_sql = TL[0][3] or ''
 
    #获取筛选的参数
    sql = """SELECT filter_name,filter_sql,ifnull(defalut_value,'')
             FROM menu_list_filters
             where FIND_IN_SET(%s,pages) order by sort"""%(page_id)
    SL,iN = db.select(sql)
   
    #获取排序字段参数
    sql ="""SELECT col_name,field_show,IFNULL(field_order,''),is_number,is_ch
             ,IFNULL(value_sql,''),id,col_type1,label,0
             FROM menu_list_cols 
             where FIND_IN_SET(%s,pages) order by sort"""%(page_id)
    NL,iN = db.select(sql)

    select_size = 10
    startNo = 0
    orderby = ''
    orderbydir=''
    qqid=''
    #print aoData
    if aoData!='':
        jsonData = json.loads(aoData)
        for e in jsonData:
            if e['name']=='sEcho':
                sEcho = e['value']
            elif e['name']=='iDisplayLength':
                select_size = e['value']
            elif e['name']=='iDisplayStart':
                startNo = e['value']
            elif e['name']=='iSortCol_0':
                iCol = e['value']
                orderby = NL[int(iCol)][2] 
            elif e['name']=='sSortDir_0':
                orderbydir = e['value']
            elif e['name']=='sSearch':
                qqid = e['value']
                qqid = MySQLdb.escape_string(qqid)
        sEcho += 1
    else:sEcho=1       
    pageNo=(int(startNo)/int(select_size)) +1
    if pageNo==0:pageNo=1

    sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_list_pages_para` where page_id=%s order by sort"%(page_id)
    para_row,iN = db.select(sql)
    sql = packPara(final_sql,para_row,value_dict,request)

    if qqid!='' and search_sql!='':
        sql+=" AND %s LIKE '%%%s%%'"%(search_sql,qqid)
    for e in SL:
        if e[0] in data_list or e[0] in request.POST:
            if data_list.get(e[0],'') != '': 
                str = e[1].replace("$s",data_list.get(e[0],''))
                sql += " and (%s)"%(str)
            elif request.POST.get(e[0], '') != '': 
                str = e[1].replace("$s",request.POST.get(e[0], ''))
                sql += " and (%s)"%(str)
        elif e[2]!='':
            str = e[1].replace("$s",e[2])
            sql += " and (%s)"%(str)

    #ORDER BY 
    if orderby!='':
        sql+=' ORDER BY %s %s' % (orderby,orderbydir)
    else:
        sql+=" %s"%list_order

    #print ToGBK(sql) 
    rows,iN = db.select(sql)
    value_dict = dict()
    for n in range(0,len(rows)):
        for i in range(0,len(NL)):
            addtwodimdict(value_dict,n,NL[i][0],rows[n][i])

    para_dict = dict()
    for e in NL:
        if e[5] !='':
            sql = "select `para_type`,IFNULL(`link_field`,'') from `menu_list_cols_para` where col_id=%s order by sort"%(e[6])
            para_row,iN = db.select(sql)
            para_dict[e[0]] = para_row
        
    #print para_dict            
    L = []
    for n in range(0,len(rows)):
        L1=list(rows[n])
        for i in range(0,len(NL)):
            if NL[i][5]!='':
                sql = packPara(NL[i][5],para_row,value_dict[n],request)
                value_row,iN = db.select(sql)
                L1[i] = value_row[0][0]
        L.append(L1)

    return L,NL

class HandleExcel():
    '''Excel相关操作类'''
    def __init__(self):
        self.head_row_labels = [u'学生ID',u'学生姓名',u'联系方式',u'知识点ID',u'知识点名称']
    """
        function：
            读出*.xlsx中的每一条记录，把它保存在data_dic中返回
        Param:
            excel_name:  要读出的文件名
        Return:
            data_dic： 返回的记录的dict
    """
    def read_excel_with_openpyxl(self, excel_name="testexcel2007.xlsx"):
        # 读取excel2007文件
        wb = load_workbook(filename=excel_name)
        # 显示有多少张表
        print   "Worksheet range(s):" , wb.get_named_ranges()
        print   "Worksheet name(s):" , wb.get_sheet_names()
        # 取第一张表
        sheetnames = wb.get_sheet_names()
        ws = wb.get_sheet_by_name(sheetnames[0])
        # 显示表名，表行数，表列数
        print   "Work Sheet Titile:" ,ws.title
        print   "Work Sheet Rows:" ,ws.get_highest_row()
        print   "Work Sheet Cols:" ,ws.get_highest_column()
        # 获取读入的excel表格的有多少行，有多少列
        row_num=ws.get_highest_row()
        col_num=ws.get_highest_column()
        print "row_num: ",row_num," col_num: ",col_num
        # 建立存储数据的字典
        data_dic = {}
        sign=1
        # 把数据存到字典中
        for row in ws.rows:
            temp_list=[]
            # print "row",row
            for cell in row:
                 print cell.value,
                 temp_list.append(cell.value)
            print ""
            data_dic[sign]=temp_list
            sign+=1
        print data_dic
        return data_dic
    """
        function：
            读出*.xlsx中的每一条记录，把它保存在data_dic中返回
        Param:
            records: 要保存的，一个包含每一条记录的list
            save_excel_name:  保存为的文件名
            head_row_stu_arrive_star:
        Return:
            data_dic： 返回的记录的dict
    """
    def write_to_excel_with_openpyxl(self,records,NL,exportFields,save_excel_name="save.xlsx",title='range names'):
        # 新建一个workbook
        wb = Workbook()
        # 新建一个excelWriter
        from zipfile import ZipFile, ZIP_DEFLATED
        archive = ZipFile(save_excel_name, 'w', ZIP_DEFLATED)
        ew = ExcelWriter(workbook=wb,archive=archive)
        # 设置文件输出路径与名称
        dest_filename = save_excel_name.decode('utf-8')
        # 第一个sheet是ws
        ws = wb.worksheets[0]
        # 设置ws的名称
        ws.title = title
        # 写第一行，标题行
        exportFields = exportFields.split(',')
        j = 1
        for h_x in range(0,len(NL)):
            if NL[h_x][0] in exportFields:
                ws.cell(row=1, column=j).value = '%s' % (NL[h_x][8])
                j += 1
        # 写第二行及其以后的那些行
        i = 2
        for record in records:
            j = 1
            for x in range(0,len(record)):
                if NL[x][0] in exportFields:
                    ws.cell(row=i, column=j).value = record[x]
                    j += 1
            i += 1
        # 写文件
        ew.save(filename=dest_filename)
