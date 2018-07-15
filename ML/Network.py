from FullConnectLayer import FullConnectLayer
import numpy as np 

#----建立FUllconetedLayer api
class SigmoidActivator(object):
    def forward(self,weight_input):
        ##sigmoid
        return 1.0/(1.0+np.exp(-weight_input))  

    def backward(self,output):
        return output*(1-output)

class Network(object):
    def __init__(self,layers):
        self.layers = []
        for i in range(len(layers)-1):
            self.layers.append(FullConnectLayer(layers[i],layers[i+1],SigmoidActivator()))#[784,8,10]   
                                                                                            #[784,8][8,10]

    def predict(self,samples):
        output = samples
        for layer in self.layers:
            layer.forward(output)
            output = layer.output
        return output
    def train(self,data_set,labels,rate,epoch):
        for _ in range(epoch):
            print('labels:',labels.shape)
            for d in range(len(data_set)):
                self.train_one_sample(data_set[d],labels[d],rate)
    def train_one_sample(self,sample,lable,rate):
        print('sample:',sample.shape,'label:',lable.shape)
        self.predict(sample)       #更新 output 进行前向传导
        self.cal_gradient(lable)    #更新detal 误差项 进行后向传导
        self.update_weight(rate)

    def cal_gradient(self,label):
        #梯度反向传导 先获取输出层误差项
        print('delta:',self.layers[-1].activator.backward(self.layers[-1].output).T.shape)
        print(label)
        delta =self.layers[-1].activator.backward(self.layers[-1].output) * (label-self.layers[-1].output)        
        for layer in self.layers[::-1]:  #排序逆转：从输出层向前更新
            layer.backward(delta)
            delta = layer.delta
    def update_weight(self,rate):
        for layer in self.layers:
            layer.update(rate)
    
    def dump(self):
        for layer in self.layers:
            layer.dump()

