import socket
HOST='192.168..1'
PORT=9999
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
s.connect((HOST,PORT))       #要连接的IP与端口
while 1:
    cmd = input('send msg:')
    s.send(cmd.encode('utf-8'))      #把命令发送给对端
    data=s.recv(4096)     #把接收的数据定义为变量
    print (data.decode())         #输出变量
s.close()   #关闭连接