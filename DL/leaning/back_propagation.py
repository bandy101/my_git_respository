from perceptron import perceptron



class bp(perceptron):
    '''
        y = f(W^T*X)
        神经元:激活函数（可导）[tanh,sigmoid]<-->感知器:阶跃函数
        sigmoid:1/(1+e^(-x)) 值域-->[0,1]   x->(-inf,inf) 关于x(0,0.5)对称 and sigmoid' =y*(1-y)
        