#include "Servers.h"
#include <string.h>
#include <string>
#include <stdio.h>
#pragma comment(lib, "ws2_32.lib")
#define MAX_SIZE 4096
#define CLIENT_NUM 1
bool Servers::server_init(char *IP, int port) {
	WSADATA WSAData;//WSADATA:�ýṹ�������������
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:��ʼ����ǰ�߳�ͨ�Ż�����MAKEWORD:�ϲ�������
	{
		cout << "WSAStartup error!" << endl;
		return false;
	}

	socketServer = socket(AF_INET, SOCK_STREAM, 0);
	if (socketServer == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP����ָ��ʹ��TCPЭ��  
	{
		cout << "Creat socket error!" << endl;
		//return false;
	}
	memset(&serveraddr, 0, sizeof(serveraddr));  //bin_zero
	serveraddr.sin_family = AF_INET;   //������ʽ  ��ַ���� host byte order
	serveraddr.sin_port = htons(port);//�˿�	�����ӱ����ֽ�˳�� (Host Byte Order) ת����������short, network byte order��
	serveraddr.sin_addr.S_un.S_addr = inet_addr(IP);//ָ�����ӷ�������IP��
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
	while (1) {
		sin_size = sizeof(struct sockaddr_in);
		//otheraddr ���ؽ��ܵķ���
		SOCKET other = accept(socketServer, (struct sockaddr *)&otheraddr, &sin_size);
		if ((numbytes = recv(other, buf, MAX_SIZE, 0)) == SOCKET_ERROR) {
			////exit(1);
			cout << "Socket receive error!" << endl;

		}
		//char *other_addr = inet_ntoa(otheraddr.sin_addr);
		string data_0 = buf;
		int pos0 = data_0.rfind("@");
		data_0.insert(pos0+1, "1;");
		//int pos1 = data_0.rfind('tek');
		//data_0.insert(pos1+2,"")
		char data_c[MAX_SIZE];
		strcpy(data_c, data_0.c_str());
		cout << "buf:" << buf << endl;
		memcpy(recvs,&data_c, strlen(data_c));
		cout << "recvs:" << recvs << endl;
		string s = *buf + "dd";
		int nSend = send(other,recvs, strlen(recvs), 0); // 0:flag write
		if (nSend == SOCKET_ERROR) {
			cout << "Socket send error!" << endl;
			//return false;
		}
		closesocket(other); /* parent doesn't need this */
	}
}