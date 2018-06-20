#------堆排序------#
#--从下至上调整---从左至右，#
#构建初始堆+交换堆顶元素和末尾元素并重建堆两部分组成。其中构建初始堆经推导复杂度为O(n)，在交换并重建堆的过程中，需交换n-1次，而重建堆的过程中，
#根据完全二叉树的性质，[log2(n-1),log2(n-2)...1]逐步递减，近似为nlogn。所以堆排序时间复杂度一般认为就是O(nlogn)级。
#完全二叉树 i左节点的:i*2+1
import random as R

def swap(lists,x,y):
    temp = lists[x]
    lists[x] = lists[y] 
    lists[y] =temp


def heap_sort(lists):
    length = len(lists)
    #从下至上调整----#构建大顶堆 顺序排序-
    top_heap = length//2 -1
    while top_heap>=0:
        heap_fy(top_heap,length,lists)
        top_heap -=1
     
    #重复建堆
    num = length -1
    while num>0:
        swap(lists,0,num)
        heap_fy(0,num,lists)
        num -=1
    return lists
def heap_fy(parent_point,length,lists): 
    k = parent_point*2+1
    temp = lists[parent_point]
    ##k<length   because from subscript 0 start 
    while k<length:
        #指向较大的子节点
        if (k+1)<length and lists[k]<lists[k+1]:
            k +=1
        if lists[k]>temp:
            lists[parent_point] = lists[k]
            parent_point = k
        else:
              break
        k =2*k+1      ##   important 重点
    lists[parent_point] = temp


def _heap_sort(lists):
    last_p = len(lists)//2-1   #subscript from 0 start
    while last_p >0:
        build_heap(lists,last_p)
        last_p -=1
    return lists
def build_heap(lists,last_p):
    temp = lists[last_p]
    l,k= 2*last_p+1,2*last_p+1
    if l>=len(lists):return
    if (l+1)<len(lists) and lists[l]>lists[l+1]  :
        k +=1
    if lists[k]>temp:
        lists[last_p] = lists[k]
        last_p = k
        
    k =2*k+1
    if k<len(lists):
        build_heap(lists,k)
    lists[last_p] = temp
    # while k < len(lists):
    #     build_heap(lists,k)
    #     k = 2*k+1

global i
i=1

def quicksort(lists,left,right):
    global i
    if  (left>=right):
        return
    temp = lists[left]  ##基准数
    l,r = left,right
    while l!=r:
        while lists[r]>=temp and l<r:
            r -=1
        while lists[l]<=temp and l<r:
            l +=1
            
        # print("l:%d,r:%d"%(l,r))
        # print("####################")
        if l<r: 
            # print("temp:",temp)
            print("l:%d,r:%d"%(l,r))
            swap(lists,l,r)
            print(lists)
    lists[left] = lists[l]
    lists[l] = temp
    print("%d:"%i,lists)
    i +=1
    quicksort(lists,left,l-1)
    quicksort(lists,l+1,right)

def quicksort_1(lists,p,r):
    if p>=r:return

    i = p + R.randint(0,r-p)
    swap(lists,p,i)
    x = lists[p]
    j = p
    i = p+1
    while i<=r:
        if a[i]<x:
            try:
                swap(lists,j,i)
            except:pass
            j=j+1
    try:
        swap(lists,p,j)
    except:pass
    quicksort_1(lists,p,j-1)
    quicksort_1(lists,j+1,r)

a='631758924'
a = list('631758924')

#ads
###解密qq
p =[]
def queue(a):
    if (len(a)==1):
        p.append(a[0])
        return
    i =0
    while i<len(a)-1:
        p.append(a[i])
        a.append(a[i+1])
        i +=2
    queue(a[i:])
queue(a)
print(p)

c = [3,4,5]
# start = len(lists)//2-1
a =[R.randint(0,100) for i in range(10)]


b= [31, 95, 98, 40, 61, 78, 20, 94, 6, 46]
# print("origin:",b)
# quicksort_1(b,0,len(b)-1)
# print("sort:",b)
