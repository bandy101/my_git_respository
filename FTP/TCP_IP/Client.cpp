#include "Client.h"
#define MAX_SIZE 4096
#define IP "120.236.164.111"

//----���Զ˿ڵ�ַ-----//
/*
const char user[] = "root";         //username
const char pswd[] = "IkaZ3qSviy64";         //password
const char host[] = "192.168.20.16";    //or"127.0.0.1"
const char table[] = "equipment";        //database
unsigned int port = 3369;           //server port  
*/
Client::Client() {
	error = " "; datas = " ";
	WSADATA WSAData;//WSADATA:�ýṹ�������������
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:��ʼ����ǰ�߳�ͨ�Ż�����MAKEWORD:�ϲ�������
	{
		cout << "WSAStartup error!" << endl;
	}
	SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);
	sockaddr_in their_addr; 
	memset(&their_addr, 0, sizeof(their_addr));  //bin_zero
	their_addr.sin_family = AF_INET;   //������ʽ  ��ַ���� host byte order
	their_addr.sin_port = htons(9019);//�˿�
	their_addr.sin_addr.S_un.S_addr = inet_addr(IP);//ָ�����ӷ�������IP��
	if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
		error += "Server connect error!\r\n";
	}
	//memcpy(buf, data, strlen(data));
	int nSend = send(sockfd, buf, sizeof(buf), 0); // 0:flag write
	if (nSend == SOCKET_ERROR) {
		error += "Socket send error!\r\n";
	}
	while (1) {
		memset(buf, 0, MAX_SIZE);
		if ((recv(sockfd, buf, MAX_SIZE, 0)) == SOCKET_ERROR) {
			error += "Socket receive error!\r\n";
			break;
		}
		strcat(datas,buf); //return datas
	}
}