from Network import Network
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from functools import reduce

mnist = input_data.read_data_sets('MNIST_data',one_hot=True)

samples = mnist.train.images
print(samples.shape)
labels = mnist.train.labels
def train_data_set():
    normalizer = Normalizer()
    data_set = []
    labels = []
    for i in range(0, 256):
        n = normalizer.norm(i)
        print('n',n)
        data_set.append(n)
        labels.append(n)
    return labels, data_set
class Normalizer(object):
    def __init__(self):
        self.mask = [
            0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80
        ]

    def norm(self, number):
        data = list(map(lambda m: 0.9 if number & m else 0.1, self.mask))
        # print('data',list(data))
        x = np.array(data).reshape(-1, 1)
        # print(x.shape)
        return x

    def denorm(self, vec):
        binary = list(map(lambda i: 1 if i > 0.5 else 0, vec[:,0]))
        for i in range(len(self.mask)):
            binary[i] = binary[i] * self.mask[i]
        return reduce(lambda x,y: x + y, binary)
def correct_ratio(network):
    normalizer = Normalizer()
    correct = 0.0
    for i in range(256):
        if normalizer.denorm(network.predict(normalizer.norm(i))) == i:
            correct += 1.0
    print ('correct_ratio: %.2f%%'%(correct / 256 * 100))

def train(network):
    labels, data_set = train_data_set()
    network.train(labels, data_set, 0.3, 50)
# network = Network([784,300,10])
# network.train(samples,labels,0.5,10)
net = Network([784, 784, 10])
# train(net)
net.train(samples, labels, 0.3, 50)
net.dump()
correct_ratio(net)
