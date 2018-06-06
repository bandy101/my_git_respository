#pragma once
#include <iostream>
#include <winsock.h>
#include <WinSock2.h>
class MySocket
{
	 public:
		     MySocket();
		     //~MySocket();
			     //重载向SOCKET类型转换的运算符
			      operator SOCKET() const;
		    //设置地址信息
			     void SetAddrInfo(std::string host, int port);
		     bool Connect();
		     //bool Disconnect();
			     bool Create(int af = AF_INET, int type = SOCK_STREAM, int protocol = IPPROTO_TCP);
		     bool Close();
		     //获取主机ip
			     std::string GetHostIP() const;
		     //获取主机端口
			     int GetPort() const;
		 private:
			     SOCKET sock;
			     SOCKADDR_IN addr_in; //记录连接的服务器的地址信息
			     bool conn_flag; //判断是否已连接
			 };