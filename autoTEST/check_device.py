import requests


class Devices:
    '''
        检测设备
    '''

    def __init__(self,d_url):
        self.url = d_url
        self.red =None
        self.infrared_num=50
    
    def req(self):
        res = requests.get(self.url)
        return res

if __name__=='__main__':
    D = Devices('http://60.165.50.66:11000/lightSource.html')
    res = D.req()
    print(res.text.decode())