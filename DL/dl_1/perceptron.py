import numpy as np 
import functools
import itertools
class perceptron:
    '''
        感知器 
        y=  w*x + b------------------------y
        wi = wi + ▲wi
         b =  b + ▲b
       ▲wi = rate*(actual_value[label] - y)*x    --> y = activator(y) 这里需要对y激活
        ▲b = rate*(actual_value[label] - y)   【y 同上
    '''
    def __init__(self,input_nums):
        self.wights = [0.0 for _ in range(input_nums)]
        self.b =0

    #激活函数 activator (这里选取阶跃函数0|1)
    def step_fun(self,value=None):
        k =0
        if value >0:
            k =1
        return k

    def train(self,data,label,rate,nums=1):
        # 权重的更新 : wi = rate*(l - output)*data[i]  bi = rate*(l - output)
        
        for _ in range(nums):
            self.one_iter(data,label,rate)
            print(self)
        ''' [w1,w2]*[d1
                    d2
                    ] --->np.matmul (axis is equal) w1*d1+w2*d2          
        '''
    def one_iter(self,data,label,rate):

        for (_0,_1) in zip(label,data):
            self._upwight(_1,_0,rate)

    def __str__(self):
        return '(wights:%s,b:%s)'%(self.wights,self.b)

    #多个测试
    def tests(self,data):
        self.result =[]
        for _ in data:
            self.result.append(
                self.step_fun(np.dot(self.wights,_)+self.b)
                )
        print('result:',self.result)

    #返回单个 result =y
    def pretect(self,data):
        return self.step_fun(
            np.matmul(self.wights,data)+self.b
        )
        

    def _upwight(self,data,label,rate):
        # output = (label - self.step_fun(np.matmul(self.wights,data)+self.b))
        output = label - self.pretect(data)
        self.wights=np.add(self.wights,np.dot(rate*output,data))
        self.b = np.add(self.b,rate*output)
        # print(self)

if __name__=='__main__':
    data = [(1,0),(0,0),(1,1),(0,1)]
    label = [0,0,1,0]
    test = [(0,1),(1,0),(1,1),(0,0)]
    h = perceptron(2)
    h.train(data,label,0.1,10)
    h.tests(test)
    print(h)