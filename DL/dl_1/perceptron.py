import numpy as np 


class perceptron:
    '''
        感知器 
        y=  w*x + b
    '''
    def __init__(self,input_nums):
        self.wights = [0 for _ in range(input_axis)]
        self.b =0
        
        self.w1 = 0
        self.w2 = 0
        
    #激活函数 activator (这里选取阶跃函数0|1)
    def step_fun(self,value=None):
        k =0
        if value >0:
            k =1
        return k
    
    def train(self,data,label,rate,nums=1):
        # 权重的更新 : wi = rate*(l - output)*data[i]  bi = rate*(l - output)
        for _ in range(nums):
            for (d,l) in zip(data,label):
                w1 = rate*(l-self.step_fun(self.w1*d[0]+self.w2*d[1]+self.b))*d[0]
                w2 = rate*(l-self.step_fun(self.w1*d[0]+self.w2*d[1]+self.b))*d[1]
                bi = rate*(l-self.step_fun(self.w1*d[0]+self.w2*d[1]+self.b))
                self.w1 +=w1
                self.w2 +=w2
                self.b +=bi

    def __str__(self):
        print('wights:%s'%(self.wights),self.b)

    def test(self,data):
        result =[]
        print('w,b:',self.w1,self.w2,self.b)
        for (_0,_1) in data:
            result.append(
                self.step_fun(self.w1*_0+self.w2*_1+self.b)
                )
        print('result:',result)
    
    def pretect

    def _upwight(self,)
if __name__=='__main__':
    data = [(1,0),(0,0),(1,1),(0,1)]
    label = [0,0,1,0]
    test = [(0,1),(1,0),(1,1),(0,0)]
    h = perceptron()
    h.train(data,label,0.1,10)
    h.test(test)