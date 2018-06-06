import socket

def servers(addrs='127.0.0.1',port=9999):
    '''
        create a servers
    '''
    servers= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    servers.bind((addrs,port))
    servers.listen(1)
    print('welcome local PC!')
    # sock,addr= servers.accept()
    # servers.send(b'welcome use!')
    while True: 
        sock,addr= servers.accept()
        data = sock.recv(4096)
        data =data.decode()
        if data:
            data +='local PC,'
            sock.send(data.encode('utf-8'))
        else:
            break
    servers.close()

if __name__=='__main__':
    servers()