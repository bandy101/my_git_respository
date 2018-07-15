import numpy as np 
import random

class FullConnectLayer(object):
    def __init__(self,input_size,output_size,activator):
        '''
        input_size:输入的维度，out_size:输出的维度
        '''
        self.input_size = input_size
        self.output_size = output_size
        self.activator = activator
        self.W = np.random.uniform(-0.1,0.1,(self.output_size,self.input_size))
        self.b = np.zeros((self.output_size,1))
        self.output= np.zeros((output_size,1))
    def forward(self,input_array):
        '''
        input_array:输入的向量，维度和input_size保持一致
        '''
        
        self.input = input_array    #(784,)->()
        print(self.W.T.shape)       #W:(784,784) (10,784)
        y =np.dot((self.W),list(input_array))
        print(y.shape)
        self.output = self.activator.forward(       #(784,1)---[10,784]*[784,1] -->[10,1]
            np.dot(self.W ,input_array)+self.b
        )
        ##W:(784,784) (10,784)
    def backward(self,delta_array):
        '''
        delta_array:上一层传来的误差项
        #delta = 隐含层误差项
        # _n =self.activator.backward(self.input)
        # print(    
        '''
        # self.W,list(delta_array)
        # _n = self.input*(1-self.input)
        # n_ = np.dot(self.W.T,delta_array)
        print(self.W.shape)
        print('delta_array:',delta_array.shape)          #(10,10)
        print('bcakward-value:',self.activator.backward(self.input).shape)
        self.delta = self.activator.backward(self.input).reshape(delta_array.shape[0],-1) * np.dot(self.W.T,delta_array)
        self.W_bard = np.dot(delta_array,self.input.T)  
        self.b_bard = self.delta_array
    
    def update(self,rate):
        '''
        使用梯度下降更新
        '''
        self.W +=rate*self.W_bard
        self.b += rate*self.b_bard

    def dump(self):
        print ('W: %s\nb:%s'%(self.W, self.b))

