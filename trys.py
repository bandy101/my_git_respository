import matplotlib.pyplot as plt
import numpy as np 
import math
from scipy import optimize  
from mpl_toolkits.axisartist.axislines import SubplotZero
def f_1(x, A, B):  
    return A*x + B  
  
#二次曲线方程  
def f_2(x, A, B, C):  
    return A*x*x + B*x + C  
  
#三次曲线方程  
def f_3(x, A, B, C, D):  
    return A*x*x*x + B*x*x + C*x + D  
def test():
    plt.figure()  
      
    #拟合点  
    x0 = [1, 2, 3, 4, 5]  
    y0 = [1, 3, 8, 18, 36]  

    #绘制散点  
    plt.scatter(x0[:], y0[:], 25, "red")  

    #直线拟合与绘制  
    A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]  
    x1 = np.arange(0, 6, 0.01)  
    y1 = A1*x1 + B1  
    plt.plot(x1, y1, "blue")  

    #二次曲线拟合与绘制  
    A2, B2, C2 = optimize.curve_fit(f_2, x0, y0)[0]  
    x2 = np.arange(0, 6, 0.01)  
    y2 = A2*x2*x2 + B2*x2 + C2   
    plt.plot(x2, y2, "green")  

    #三次曲线拟合与绘制  
    A3, B3, C3, D3= optimize.curve_fit(f_3, x0, y0)[0]  
    x3 = np.arange(0, 6, 0.01)  
    y3 = A3*x3*x3*x3 + B3*x3*x3 + C3*x3 + D3   
    plt.plot(x3, y3, "purple")  

    plt.title("test")  
    plt.xlabel('x')  
    plt.ylabel('y')  

    plt.show()  

0.9942133890017211
0.9942300991878248
1-sqrt(1-b) b 
y = sqrt(x)  x∈(0,1)  y>x   
0.9240401368341544
if __name__=='__main__':
    
    x_ = np.arange(90)
    x = np.arange(100)
    y1 = np.tan(45/180)
    y_ = y1*x
    y = np.sin(x*0.5)+10    
    fg = plt.figure(1)  
    # ax = SubplotZero(fg,1,1,1)
    # fg.add_subplot(ax)
    # ax.axis["xzero"].label.set_text("新建y=0坐标")
    # ax.axis["xzero"].label.set_color('green')
    # ax.axis["xzero"].set_visible(True)
    # ax.axis["新建1"] = ax.new_floating_axis(nth_coord=0, value=2,axis_direction="bottom")
    # ax.axis["新建1"].toggle(all=True)
    # ax.axis["新建1"].label.set_text("y = 2横坐标")
    # ax.axis["新建1"].label.set_color('blue')
    # ax.axis["xzero"].set_axisline_style("-|>")
    # ax.set_ylim(-3, 3)
    # ax.set_yticks([-1,-0.5,0,0.5,1])
    # ax.set_xlim([-5, 8])
    # ax.grid(True, linestyle='-.')
    # xx = np.arange(-4, 2*np.pi, 0.01)
    # ax.plot(xx, np.sin(xx)) 
    bc = np.linspace(0,1,100)
    v = np.log(bc)
    plt.subplot(211)  
    plt.plot(bc, v)  
    plt.subplot(211)  
    # 设置x轴范围  
    # plt.xlim(-100, 100)  
    # 设置y轴范围  
    # plt.ylim(-50, 50)  

    plt.plot(bc, -v)    
    plt.show()  