#include<conio.h>
#include <iostream>
#include <winsock2.h>
#include <mysql.h>
#include <string.h>
#include <fstream>
#include "SQL_operation.hpp"
#define MAX_SIZE 4096
//#define IP "120.236.164.111"
#define IP "127.0.0.1"
#pragma comment(lib, "ws2_32.lib")
using namespace std;
int  numbytes;
struct hostent *he;


//const char user[] = "root";         //username
//const char pswd[] = "IkaZ3qSviy64";         //password
//const char host[] = "192.168.20.16";    //or"127.0.0.1"
//const char table[] = "equipment";        //database

 char *user = "root";         //username
 char *pswd = "IkaZ3qSviy64";         //password
 char *host = "192.168.20.16";    //or"127.0.0.1"
 char *table = "equipment";        //database
unsigned int port = 3369;           //server port  

//#include <errno.h>
//int main(int argc, char *argv[])
//
//{
//
//
//	WSADATA WSAData;//WSADATA:�ýṹ�������������
//	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:��ʼ����ǰ�߳�ͨ�Ż�����MAKEWORD:�ϲ�������
//	{
//		cout << "WSAStartup error!" << endl;
//		return false;
//	}
//	SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);
//
//	int  numbytes;
//	char buf[MAX_SIZE];
//	memset(buf, 0, MAX_SIZE);
//
//	
//	if (sockfd == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP����ָ��ʹ��TCPЭ��  
//	{
//		cout << INVALID_SOCKET <<"Creat socket error!" << endl;
//		return false;
//	}
//
//	//socketServer = socket(AF_INET, SOCK_STREAM, 0);
//	sockaddr_in their_addr; /* connector's address information */
//	memset(&their_addr, 0, sizeof(their_addr));  //bin_zero
//	their_addr.sin_family = AF_INET;   //������ʽ  ��ַ���� host byte order
//	their_addr.sin_port = htons(9019);//�˿�	�����ӱ����ֽ�˳�� (Host Byte Order) ת����������short, network byte order��
//	their_addr.sin_addr.S_un.S_addr = inet_addr(IP);//ָ�����ӷ�������IP��
//	//bzero(&(their_addr.sin_zero), ; /* zero the rest of the struct */
//	if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
//		cout << endl << "Server connect error!" << endl;
//	}
//
//	/*-----------------mysql-data----------------*/
//	MYSQL *pConn;
//	pConn = mysql_init(NULL);	
//	if (mysql_real_connect(pConn, host, user, pswd, table, port, NULL, 0))	
//	{
//		mysql_query(pConn, "SET NAMES 'gb2312'");
//	}
//	else
//	{
//		printf("�޷��������ݿ�:%s", mysql_error(pConn));
//	}
//	if (mysql_query(pConn, "select * from telemetry_message"))
//	{
//		printf("��ѯʧ��:%s", mysql_error(pConn));
//		return 0;
//	}
//	//mysql_store_result�ǰѲ�ѯ���һ����ȡ���ͻ��˵��������ݼ���������Ƚϴ�ʱ���ڴ档
//	//mysql_use_result���ǲ�ѯ������ڷ������ϣ��ͻ���ͨ��ָ�����ж�ȡ����ʡ�ͻ����ڴ档����һ��MYSQL*����ͬʱֻ����һ��δ�رյ�mysql_use_result��ѯ
//	MYSQL_RES *result = mysql_store_result(pConn);
//	MYSQL_ROW row;
//	int i = 0;
//	string r = "";
//	while (row = mysql_fetch_row(result))
//	{
//		for (; i < 36; i++)
//			try
//		{
//			r += row[i];
//			r += ";";
//		}
//		catch (exception)
//		{r += ","; }
//		cout<<r.c_str()<< endl;
//		//printf("%s\n", r);
//	}
//	mysql_free_result(result);
//	mysql_close(pConn);
//	char *data = "RS01440100012017 - 12 - 27 15:45 : 00001f@@@CO2,0.121, ; NO, 0.097, ; CO, 0.055, ; HC, 0.102, ; tek07####";
//	//char *data = (char*)r.c_str();
//	memcpy(buf, data, strlen(data));
//	int nSend = send(sockfd, buf,sizeof(buf), 0); // 0:flag write
//	if (nSend == SOCKET_ERROR) {
//		cout << "Socket send error!" << endl;
//		//return false;
//	}
//	memset(buf, 0, MAX_SIZE);
//	if ((numbytes = recv(sockfd, buf, MAX_SIZE, 0)) == SOCKET_ERROR){
//		////exit(1);
//		cout << "Socket receive error!" << endl;
//	}
//
//	//buf[numbytes] = '\0';
//	printf("Received: %s", buf);
//
//	closesocket(sockfd);
//	getchar();
//	return 0;
//
//}

int main()
{		
	char swp [4096];
	
	WSADATA WSAData;//WSADATA:�ýṹ�������������
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:��ʼ����ǰ�߳�ͨ�Ż�����MAKEWORD:�ϲ�������
	{
		cout << "WSAStartup error!" << endl;
		return false;
	}
	SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);

	int  numbytes;
	char buf[MAX_SIZE];
	memset(buf, 0, MAX_SIZE);

	
	if (sockfd == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP����ָ��ʹ��TCPЭ��  
	{
		cout << INVALID_SOCKET <<"Creat socket error!" << endl;
		return false;
	}

	//socketServer = socket(AF_INET, SOCK_STREAM, 0);
	sockaddr_in their_addr; /* connector's address information */
	memset(&their_addr, 0, sizeof(their_addr));  //bin_zero
	their_addr.sin_family = AF_INET;   //������ʽ  ��ַ���� host byte order
	their_addr.sin_port = htons(9999);//�˿�	�����ӱ����ֽ�˳�� (Host Byte Order) ת����������short, network byte order��
	their_addr.sin_addr.S_un.S_addr = inet_addr(IP);//ָ�����ӷ�������IP��
	//bzero(&(their_addr.sin_zero), ; /* zero the rest of the struct */
	if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
		cout << endl << "Server connect error!" << endl;
	}

	MySql  *sql= new MySql(host,user, pswd, table, port);
	cout << sql->error;
	sql->read_data(42);
	string datas = sql->datas;
	cout << "size:"<<strlen(datas.c_str()) << endl;
	string *name = sql->name;
	int pos,last_pos, nSend;
	char *data;
	last_pos = datas.rfind("\n");
	pos = datas.find("\n");
	cout << "pos:" << pos << endl;
	int x = 0;
	if (pos!=-1)
		while (pos != last_pos)
		{
			memset(buf, 0, MAX_SIZE);
			strcpy(buf, datas.substr(x, pos).c_str());
			x = pos;
			cout << "buf:"<< buf << endl;
			//memcpy(buf, swp, strlen(swp));
			 nSend = send(sockfd, buf,sizeof(buf), 0); // 0:flag write
			if (nSend == SOCKET_ERROR) {
					cout << "Socket send error!" << endl;	
				}
			memset(buf, 0, MAX_SIZE);
			if(recv(sockfd, buf, MAX_SIZE, 0) == SOCKET_ERROR){
					cout << "Socket receive error!" << endl;
				}
			char *data_0 = buf;
			closesocket(sockfd);
			SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);
			if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
				cout << endl << "Server connect error!" << endl;
			}	
			printf("Received: %s\n", buf);
			pos = datas.find("\n",pos+1);
			cout << "pos:" << pos << endl;
		}
	closesocket(sockfd);
	//cout << datas << endl;
	//cout << name[2];
	getchar();
}