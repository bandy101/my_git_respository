from functools import reduce

class Percptron(object):
    def __init__(self,input_dim,activator):
        '''
        初始化感知器，设置参数个数，以及激活函数
        '''
        self.activator = activator
        #权重初始化0
        self.weights = [0.0 for _ in range(input_dim)]
        #偏置项初始化0
        self.bias = 0.0
    
    def __str__(self):
        '''
        打印学习到的权重、偏置项
        '''
        return 'weights\t:%s\nbias\t:%f\n'%(self.weights,self.bias)

    def predict(self,input_vec):
        '''
        输入向量，输出打印感知器结果
        '''
        # y = f(w*x+b)
        self.out = self.activator(
            reduce(lambda a,b:a+b,
            map(lambda x_y: x_y[0]*x_y[1],
            zip(input_vec,self.weights)),
            0.0)
            +self.bias
            )
        return self.out
    
    def train(self,input_vecs,labels,iteration,rate):
        '''
        输入训练数据：一组向量、及每组向量对应的label，和训练次数、学习率
        '''
        for i in range(iteration):
            self._one_iteration_(input_vecs,labels,rate)

    def _one_iteration_(self,input_vecs,labels,rate):
        '''
        一次迭代，把所有的训练数据过一遍
        '''
        samples = zip(input_vecs,labels)
        for (input_vec,label) in samples:
            #计算机在当前权重下输出
            output = self.predict(input_vec)
            #更新权重
            self._update_weights(input_vec,output,label,rate)
    
    def _update_weights(self,input_vec,output,label,rate):
        '''
        利用感知器规则更新权重 delta
        '''
        delta = label - output
        self.weights = list(map(
            lambda x:x[1]+x[0]*rate*delta,
            zip(input_vec,self.weights)
        ))
        #更新bias
        self.bias += rate+delta
        # self.weights + =y(w*x+b)  向量化编程

def get_datas():
    input_vecs = [[0,0],[0,1],[1,0],[1,1]]
    labels = [0,1,1,0]
    return input_vecs,labels

def activator(x):
    return 1 if x>0.0 else 0

def train_and_perceptron():

    p = Percptron(2,activator)
    inputs,labels = get_datas()
    p.train(inputs,labels,1000,0.01)
    return p

if __name__ =='__main__':
    #训练and感知器
    and_percepron = train_and_perceptron()
    print (and_percepron)
    print(and_percepron.predict([0,0]))