#include "Servers.h"
#include <string.h>
#include <string>
#include <stdio.h>

#pragma comment(lib, "ws2_32.lib")
#define MAX_SIZE 4096
#define CLIENT_NUM 1
bool Servers::server_init(char *IP, int port) {
	WSADATA WSAData;//WSADATA:该结构被用来储存调用
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:初始化当前线程通信环境，MAKEWORD:合并短整数
	{
		cout << "WSAStartup error!" << endl;
		return false;
	}

	socketServer = socket(AF_INET, SOCK_STREAM, 0);
	if (socketServer == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP具体指明使用TCP协议  
	{
		cout << "Creat socket error!" << endl;
		//return false;
	}
	memset(&serveraddr, 0, sizeof(serveraddr));  //bin_zero
	serveraddr.sin_family = AF_INET;   //声明格式  地址家族 host byte order
	serveraddr.sin_port = htons(port);//端口	将它从本机字节顺序 (Host Byte Order) 转换过来。【short, network byte order】
	serveraddr.sin_addr.S_un.S_addr = inet_addr(IP);//指明连接服务器的IP地
	if (bind(socketServer, (struct sockaddr *)&serveraddr, sizeof(struct sockaddr)) == -1)
	{
		return false;
	}
	if (listen(socketServer, CLIENT_NUM) == -1)
	{
		return false;
	}
	return true;
}
void Servers::server_begin()
{

	int sin_size, numbytes;
	char buf[MAX_SIZE];
	memset(buf, 0, MAX_SIZE);
	char recvs[MAX_SIZE];
	memset(recvs, 0, MAX_SIZE);
	cout << "welcome create servers local" << endl;
	//other = accept(socketServer, (struct sockaddr *)&otheraddr, &sin_size);
	while (1) {
		sin_size = sizeof(struct sockaddr_in);
		//otheraddr 返回接受的服务
		other = accept(socketServer, (struct sockaddr *)&otheraddr, &sin_size);
		memset(buf, 0, MAX_SIZE);
		if ((numbytes = recv(other, buf, MAX_SIZE, 0)) == SOCKET_ERROR) {
			cout << "Socket receive error!" << endl;
			
			//closesocket(socketServer);   //关闭套接字  
			closesocket(other);   //关闭套接字       
			//WSACleanup();           //释放套接字资源; 
			//cout << "close connect";
			break;
		}
		else {
			cout << "buf:" << buf << endl;
		}
		//char *other_addr = inet_ntoa(otheraddr.sin_addr);
		string data_0 = buf;
		//-----成功标志----//
		//int pos0 = data_0.rfind("@");
		//data_0.insert(pos0+1, "1;");
		//---//
		data_0 = "Hellow_-" + data_0;
		char data_c[MAX_SIZE]; memset(data_c, 0, MAX_SIZE);
		strcpy(data_c, data_0.c_str());
		
		//memcpy(recvs,data_c, strlen(data_c));
		//cout << "recvs:" << data_c << endl;
		string s = *buf + "dd";
		int nSend = send(other, data_c, strlen(data_c), 0); // 0:flag write
		if (nSend == SOCKET_ERROR) {
			cout << "Socket send error!" << endl;
		}
		memset(buf, 0, MAX_SIZE);
	}
		closesocket(socketServer); /* parent doesn't need this */
		closesocket(other); /* parent doesn't need this */
	
}