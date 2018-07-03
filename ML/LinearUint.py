
from Perceptron import Percptron 

f = lambda x:x

class LinearUint(Percptron):
    def __init__(self,input_dim):
        Percptron.__init__(self,input_dim,f)

def get_data():
    inputs = [[5],[3],[8],[1.4],[10.1]]
    labels = [5500,2300,7600,1800,11400]
    return inputs,labels

def train_linear_uint():
    p = LinearUint(1)
    inputs,labels = get_data()
    p.train(inputs,labels,100,0.01)
    return p

p = train_linear_uint()
print(p)
print(p.predict([15]))