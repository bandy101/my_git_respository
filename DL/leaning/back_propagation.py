from perceptron import perceptron
import numpy as np


class bp(perceptron):
    '''
        y = f(W^T*X)
        神经元:激活函数（可导）[tanh,sigmoid]<-->感知器:阶跃函数
        sigmoid:1/(1+e^(-x)) 值域-->[0,1]   x->(-inf,inf) 关于x(0,0.5)对称 and sigmoid' =y*(1-y)

        对于->输出层节点的误差项 delta_i = yi*(1-yi)*(ti-yi) --->(yi:输出的值,ti实际的值(label值))
        对于->隐藏层节点的误差项 delta_i = yi*(1-yi)*[E_W_ki*dekta_k]

        -----W_ji <- W_ji + rate*delta_j*x_ji
        其中,W_ji是i节点到j节点的权重，rate是一个成为学习速率的常数，delta_j是节点j的误差项，x_ji是节点i传递给节点j的输入。
        [输出层误差项]向量表达形式->: delta = y*(1-y)*(t-y)
        [隐藏层误差项]向量表达形式->: delta_l = yl*(1-yl)*W.T(transpose)*delta_(l+1)
            W <- W + rate*delta*x^T(x的向量化)
            b <- b + rate*delta
         
        
    '''
class sigmoidactivator:
    def forward(self,inputs):
        return 1/(1+np.exp(-inputs))

    def backward(self,out):
        return out*(1-out)

class FullConnectLayer:
    def __init__(self,input_size,output_size,activator):
        self.input_size, self.output_size=input_size ,output_size
        self.activator = activator
        self.W = np.random.uniform(-0.1,0.1,(output_size,input_size))
        self.b = np.zeros((output_size,1))
        self.output = np.zeros((output_size,1))

    def __str__(self):
        return ('W:%s,b:%s'%(self.W,self.b))

    def forward(self,input_array):
        # BP需要用到   forward---->backward(更新参数)---->forward---->backward -----ok？---break
        self.input = input_array 
        #y = f(W^T*X)
        self.output = self.activator.forward(np.dot(self.W,input_array)+self.b)
    
    def backward(self,input_array,delta_array,rate):
        self.delta = self.activator.backward(input_array)*(np.dot(self.W.T,delta_array))
        self.w_grad= np.dot(self.input.T,delta_array)
        self.b_grad= delta_array #??
        '''W <- W + rate*delta*x^T(x的向量化)
        b <- b + rate*delta'''
    def update(self,rate):
        self.W += rate*self.w_grad
        self.b += rate *self.b_grad

class NeuralNet:
    '''
        构建网络api接口
    '''
    def __init__(self):
        
