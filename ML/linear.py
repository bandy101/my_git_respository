from keras import Sequential
from keras.layers import Dense
import numpy as np

#---data---#
tr_x = np.linspace(-1,1,101)
tr_y = 0.33*np.random.randn(*tr_x.shape)+3*tr_x

# print(tr_y)

model = Sequential()
# model.add(Dense(input_dim=1,output_dim=1,activation='linear'))
model.add(Dense(1,input_shape=(1,),activation='linear'))
model.compile(loss='mse',optimizer='sgd')

weights = model.layers[0].get_weights()##获取该层张量
print(weights)
w_init = weights[0][0][0]
b_init = weights[1][0]
print('Linear regression model is initialized with weights w: %.2f, b: %.2f' % (w_init, b_init)) 

model.fit(tr_x,tr_y,verbose=0,epochs=200)

weights = model.layers[0].get_weights() 
w_init = weights[0][0][0]
b_init = weights[1][0]
print(weights)
print('Linear regression model is initialized with weights w: %.2f, b: %.2f' % (w_init, b_init)) 