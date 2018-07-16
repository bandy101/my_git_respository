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

    def forward(self,inputs):  ##激活函数
        return 1.0/(1+np.exp(-inputs))

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
        # print(input_array)
        self.output = self.activator.forward(np.dot(self.W,input_array)+self.b)
    def backward(self,input_array,delta_array):
        print('W.T',self.W.T.shape)
        print('delta_array:',delta_array.shape)
        self.delta = self.activator.backward(self.input)*np.dot(self.W.T,delta_array) ##sigmoid 导数
        self.w_grad= np.dot(delta_array,self.input.T)
        self.b_grad= delta_array #??
        '''W <- W + rate*delta*x^T(x的向量化)
            b <- b + rate*delta'''
    def update(self,rate):
        self.W += rate*self.w_grad
        self.b += rate *self.b_grad 
    
    def train(self,datas,labels,rate,echos):
        self.one_iter(datas,labels,rate)
        if echos:
            self.train(datas,labels,rate,echos-1)

    def one_iter(self,datas,labels,rate):
        delta = self.activator.backward(self.output)*(labels-self.output)
        for d,l in zip(datas,labels):
            
            self.update(rate)

    def dump(self):
        print ('W: %s\nb:%s'%(self.W, self.b))

class NeuralNet:
    '''
        构建网络api接口
    '''
    def __init__(self,layers):
        self.layers =[]
        for _ in range(len(layers)-1):
            self.layers.append(FullConnectLayer \
                (layers[_],layers[_+1],sigmoidactivator()))
        
    def train(self,datas,labels,rate,epoch):
        if epoch:
            self.train_on_sample(datas,labels,rate)
            self.train(datas,labels,rate,epoch-1)

    def train_on_sample(self,datas,labels,rate):
        for d in range(len(datas)):
            output = datas[d]
            for layer in self.layers:
                layer.forward(output)
                output = layer.output
                # layer.dump()

            print(labels[d][0].shape)
            delta = self.layers[-1].activator.backward(self.layers[-1].output) \
                *(np.expand_dims(labels[d],1)-self.layers[-1].output)
            #从后面往前算出误差项 delta
            for layer in self.layers[::-1]:
                layer.backward(layer.input,delta)
                delta = layer.delta
            self.update_weight(rate)
    def update_weight(self,rate):
        for layer in self.layers:
            layer.update(rate)

    def dump(self):
        for layer in self.layers:
            layer.dump()

if __name__ == '__main__':
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets('MNIST_data',one_hot=True)
    samples = mnist.train.images
    print('samples:',samples[0].shape)
    labels = mnist.train.labels
    print('lables:',labels.shape)
    net = NeuralNet([784, 784, 10])
    # train(net)
    net.train(samples, labels, 0.3, 10)
    net.dump()
    # correct_ratio(net)