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
    ##K <length 
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

def build_heap(lists,start):
    
    k = start
    le ,ri=2*start+1, 2*start+2
    if le<len(lists) and le>lists[start]:
        k=le
    if ri<len(lists) and ri>lists[start]:
        k=ri
    if k!=start:
        swap(lists,k,start)
    # else:
    #     build_heap(lists)
c = [3,4,5]
# start = len(lists)//2-1
a =[R.randint(0,100) for i in range(10)]
b= [31, 95, 98, 40, 61, 78, 20, 94, 6, 46]
print("origin:",a)
print("sort:",heap_sort(a))
