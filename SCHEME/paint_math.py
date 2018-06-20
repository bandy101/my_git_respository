import numpy as np 
import matplotlib.pyplot as plt
import math
plt.figure(1)  
plt.subplot(211)  
x = np.linspace(1000000,10000000000,10000)
y_ = np.sqrt(x)
g = 1
value =0.0000000001
y = []
def sqrt(g,x):
    if (abs(g**2-x) < value):
        y.append(g)
    else:sqrt((x/g+g)/2,x)
for _ in x:
    g =1
    sqrt(g,_)
plt.plot(x, y)  
plt.subplot(212)  
plt.plot(x, y_)  
plt.show()  