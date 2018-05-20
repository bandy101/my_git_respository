import os
import sys
from os import path

global c
c = []
for x in range(33,127):
    c.append(chr(x))
global chars
chars =[]
global char
char=[]
global num,l
num=6
l=0
def add(nums):
    global char,l,chars
    # l=0
    print('-----',nums)
    if nums>1:
        for i in c:
            if nums==num:
                char=[]
                l=0
            # print(i)
            print('######L:',l,len(char),char)
            while l+nums>num:
            # if l+nums>num and :
            # if nums>=3:
                char = char[:-1]
                
                # if l>0:
                l -=1
                print('l:',l,char)
                    # print('l>0',l)
                    # print('l>0',l)
            char.append(i)
            l +=1
            print('nums:%d,L:%d'%(nums,l),char)
            add(nums-1)
    else:
        for i in c:
            char.append(i)
            l +=1
            print('nums:%d,L:%d'%(nums,l),char)
            # if len(char)==num:
            chars.append(''.join(char))
            char = char[:-1]
            l -=1
        with open('zidian.txt','a') as f:
            for _ in chars:
                f.write(_+'\n')
        chars=[]
        # char =char[:-1]
        # l -=1
# c = ['x','y','z']
while num<16:
    # global num
    num +=1
    add(num)
    # chars =set(chars)
    # with open('zidian.txt','a') as f:
    #     for _ in chars:
    #         f.write(_+'\n')
    # chars =list(chars)
    chars=[]
chars.sort()
# chars =set(chars)
print(len(chars))
# print(chars)
# chars = []
# s = []
# for i in range(3):
#     chars.append(str(i))
#     if len(chars)!=2:
#         for j in range(3):
#             if len(chars)!=2:
#                 chars.append(str(j))
#                 print('j',j)
#                 s.append(''.join(chars))
#                 chars = chars[:-1]
#         chars =[]
# print (s)