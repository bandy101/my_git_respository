import requests
import os 
from os import path

prex = 'http://202.105.10.126:8055/video/'
# url = 'http://202.105.10.126:8055/video/20180911/15366527703302.mp4'
# paths ='./video/2.mp4'


def dwd(paths,url):
    try:
        pre_content_length = 0
        while True:
            res = requests.get(url,stream=True)
            content_length = int(res.headers['content-length'])
            print(res.headers['content-length'])

            if content_length < pre_content_length or (
                os.path.exists(paths) and os.path.getsize(paths) == content_length):
                break
            pre_content_length = content_length
            with open(paths, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d  total size:%d' % (os.path.getsize(paths), content_length))
    except Exception as e:
        print(e)
def get_token(url,name='demo',pwd='demo&123'):
    js_pwd ={
    "clientId":"098f6bcd4621d373cade4e832627b4f6",
    'userName':name,
    'password':pwd
    }
    try:
        res = requests.post(url,json=js_pwd,verify=False)
        res =json.loads(res.content)
        token = res['content']['token']
        return token
    except Exception e:
        print(e)

def get_
if __name__=='__main__':
    dwd(paths)