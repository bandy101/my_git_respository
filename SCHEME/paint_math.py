import numpy as np 
import matplotlib.pyplot as plt

plt.figure(1)  
x = np.linspace(0.000000001,1,10000)
g = 1
value =0.00001
y = ((((x/g)+g)/2)**2 -x)
plt.plot(x, y)  
plt.show()  