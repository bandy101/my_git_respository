import time
import os,shutil
from os import path



# tss1 = '20180516095435'
# timeArray = time.strptime(tss1, "%Y%m%d%H%M%S")
# timeStamp = int(time.mktime(timeArray))
# print (timeStamp)
# # count = 1
# # for d in os.listdir('mp4'):
# #     timeArray = time.strptime(d[9:-4], "%Y%m%d%H%M%S")
# #     timeStamp = int(time.mktime(timeArray))
# #     os.rename(path.join('mp4',d),path.join('mp4',str(timeStamp)+".mp4"))
# #     print()
# from os import path
# ps='H:\smoke2'
# new_Path=''


def create(new_Path,root):
    '''
        将ps文件夹下的-目录(name_dir)-里面的 '1.jpg' 文件 复制到 new_path 文件夹中
    '''
    for r in os.listdir(root):
        ps = path.join(root,r)
        for fold in os.listdir(ps):
            # for x in os.listdir(path.join(ps,fold)):
                # if x[-1:]== '4':
                if fold[:2] in ['01','06','07','11']:
                    pp = path.join(ps,fold)
                    shutil.copy(path.join(ps,fold),new_Path)
                    os.rename(path.join(new_Path,fold),path.join(new_Path,r+"_"+fold))
                    # break

def deltes(new_Path,root):
    '''
        将new_Path文件夹下的文件名称 与ps文件夹下的-目录-名称进行比对,然后删除文件new_Path文件夹没有的【ps文件夹下的-目录-】文件名称
    '''
    n = len(os.listdir(new_Path))
    for r in os.listdir(root):
        ps = path.join(root,r)
        for f in os.listdir(ps):
            l =n
            for k in os.listdir(new_Path):
                if(f == k[:-4]):
                    break
                else: 
                    l =l - 1
            if l<=0:
                shutil.rmtree(path.join(ps,f))
def others():
    consider_smoke = os.listdir('H:\分类任务\黑烟序列分类\other1')
    have_smoke = os.listdir('H:\分类任务\黑烟序列分类\yes1')
    consider_smoke = list(map(lambda x:x[:-7],consider_smoke))
    have_smoke = list(map(lambda x:x[:-7],have_smoke))
    consider_smoke,have_smoke = list(set(consider_smoke)),list(set(have_smoke))
    for name in os.listdir('H:\分类任务\黑烟序列分类\无'): ##待分类
        if name in have_smoke:
            print('移动成功！')
            shutil.move(path.join('H:\分类任务\黑烟序列分类\无',name),'H:\分类任务\黑烟序列分类\有')
        elif name in consider_smoke:
            print('移动成功！')
            shutil.move(path.join('H:\分类任务\黑烟序列分类\无',name),'H:\分类任务\黑烟序列分类\疑似')
        else:
            pass
            # shutil.move(path.join('H:\分类任务\黑烟序列分类\无',name),'H:\分类任务\黑烟序列分类\无')

if __name__ =='__main__':
    print('\t请输入操作标识* [1,2] *\n1->create(ps,new_Path)[复制文件],2->deltes(new_Path,ps)[删除文件]\n\t\t\n\t\t3->other*********')
    flag = input('input:')
    if flag=='1':
        root = input('请输入url----root:')
        new_Path = input('请输入url----new_Path:')
        print('正在进行操作······')
        create(new_Path,root)
        print('操作成功······')
    if flag=='2':
        root = input('请输入url----root:')
        new_Path = input('请输入url----new_Path:')
        print('正在进行操作······')
        deltes(new_Path,root)
        print('操作成功······')
    if flag=='3':  
        others()