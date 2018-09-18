import requests
import os,shutil
from os import path
import json,time
import zipfile
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait

global PRE_URL
PRE_URL = 'http://218.28.71.220:1570/api/'
TSNO={
    "SFE-R600-B22W4419":"移动式",
    "SFE-R600-V22W3522":"S229环宇立交桥治超站1号机",
    "SFE-R600-V22W4495":"S229环宇立交桥治超站2号机",
    "SFE-R600-V23W1906":"S308大召营镇1号机",
    "SFE-R600-V23W1922":"S308大召营镇2号机",
    "SFE-R600-V23W1948":"S308新乡收费站1号机",
    "SFE-R600-V23W2819":"S308新乡收费站2号机",
    "SFE-R600-V23W2833":"G107好运饲料1号机",
    "SFE-R600-V23W2851":"G107好运饲料2号机",
    "SFE-R600-V23W2902":"G107铁道路桥1号机",
    "SFE-R600-V23W2926":"G107铁道路桥2号机",
    "SFE-R600-G22W2807":"广清大道(龙塘)",
    "SFE-R600-G22W2714":"治超站出口",
    "SFE-R600-G22W2772":"三棵竹一桥(源潭)",
    "SFE-R600-G22W2798":"清远大道(党校)"
}
##---mp4---http://218.28.71.220:1570/api/+\
#       record/SFE-R600-V23W1906/20180918144332.619583/video
# --确认---http://218.28.71.220:1570/api/record/SFE-R600-V23W1906/+\
#       20180918124537.883825/status
#all lists http://218.28.71.220:1570/api/record/SFE-R600-V23W1906/

#'exist'http://218.28.71.220:1570/api/status
'''
Accept	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding	gzip, deflate
Accept-Language	zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Connection	keep-alive
Host	218.28.71.220:1570
Upgrade-Insecure-Requests	1
User-Agent	Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0
'''
def pre_start():
    k = 'http://218.28.71.220:1570/api/status'
    res = requests.get(PRE_URL+'status',timeout=6000,verify= False,Ac)
    print(res.url)
    res  = json.loads(res.content)
    sites =res['content']
    print(sites)
if __name__ == '__main__':
    pre_start()