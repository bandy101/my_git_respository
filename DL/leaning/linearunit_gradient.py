from perceptron import perceptron

class linearUnit(perceptron):
    '''
        #线性单元
            使用一个可导的线性函数来替代感知器的阶跃函数，这种感知器就叫做线性单元。线性单元在面对线性不可分的数据集时，会收敛到一个最佳的近似上。

            替换了激活函数之后，线性单元将返回一个实数值而不是0,1分类。因此线性单元用来解决回归问题而不是分类问题。

        #线性模型
            output  y = W^T * X --->x0*w0(b,x0=1)+x1*w1.....

            训练模型有两种方法：
                监督学习: 要提供这样一堆训练样本：每个训练样本既包括输入特征，也包括对应的输出(也叫做标记，label)。
                无监督学习: 训练样本中只有而没有。模型可以总结出特征的一些规律，但是无法知道其对应的答案。
        
        #随机梯度下降算法(Stochastic Gradient Descent, SGD)
            梯度：【梯度是一个向量，它指向函数值上升最快的方向
                函数y=f(x)的极值点，就是它的导数f'(x)=0的那个点。因此我们可以通过解方程，求得函数的极值点，每次修改x值
                使函数朝着最小值那个方向迭代（取函数梯度相反方向） 
        
        ▲ 推导公式！ 微分导数
    '''
    def __init__(self,input_num):
        perceptron.__init__(self,input_num)

    def step_fun(self,x):
        return  x
if __name__=='__main__':
    data = [5, 3, 8, 1.4, 10.1]
    label = [5500, 2300, 7600, 1800, 11400]
    test = [[3.4],15,[1.5],6.3] 
    h = linearUnit(1)
    h.train(data,label,0.01,10)
    h.tests(test)
    print(h)