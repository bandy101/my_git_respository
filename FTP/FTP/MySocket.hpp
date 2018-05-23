#pragma once
#include <iostream>
#include <winsock.h>
#include <WinSock2.h>
class MySocket
{
	 public:
		     MySocket();
		     //~MySocket();
			     //������SOCKET����ת���������
			      operator SOCKET() const;
		    //���õ�ַ��Ϣ
			     void SetAddrInfo(std::string host, int port);
		     bool Connect();
		     //bool Disconnect();
			     bool Create(int af = AF_INET, int type = SOCK_STREAM, int protocol = IPPROTO_TCP);
		     bool Close();
		     //��ȡ����ip
			     std::string GetHostIP() const;
		     //��ȡ�����˿�
			     int GetPort() const;
		 private:
			     SOCKET sock;
			     SOCKADDR_IN addr_in; //��¼���ӵķ������ĵ�ַ��Ϣ
			     bool conn_flag; //�ж��Ƿ�������
			 };