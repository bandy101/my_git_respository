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
//	WSADATA WSAData;//WSADATA:该结构被用来储存调用
//	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:初始化当前线程通信环境，MAKEWORD:合并短整数
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
//	if (sockfd == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP具体指明使用TCP协议  
//	{
//		cout << INVALID_SOCKET <<"Creat socket error!" << endl;
//		return false;
//	}
//
//	//socketServer = socket(AF_INET, SOCK_STREAM, 0);
//	sockaddr_in their_addr; /* connector's address information */
//	memset(&their_addr, 0, sizeof(their_addr));  //bin_zero
//	their_addr.sin_family = AF_INET;   //声明格式  地址家族 host byte order
//	their_addr.sin_port = htons(9019);//端口	将它从本机字节顺序 (Host Byte Order) 转换过来。【short, network byte order】
//	their_addr.sin_addr.S_un.S_addr = inet_addr(IP);//指明连接服务器的IP地
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
//		printf("无法连接数据库:%s", mysql_error(pConn));
//	}
//	if (mysql_query(pConn, "select * from telemetry_message"))
//	{
//		printf("查询失败:%s", mysql_error(pConn));
//		return 0;
//	}
//	//mysql_store_result是把查询结果一次性取到客户端的离线数据集，当结果比较大时耗内存。
//	//mysql_use_result则是查询结果放在服务器上，客户端通过指针逐行读取，节省客户端内存。但是一个MYSQL*连接同时只能有一个未关闭的mysql_use_result查询
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
	
	WSADATA WSAData;//WSADATA:该结构被用来储存调用
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:初始化当前线程通信环境，MAKEWORD:合并短整数
	{
		cout << "WSAStartup error!" << endl;
		return false;
	}
	SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);

	int  numbytes;
	char buf[MAX_SIZE];
	memset(buf, 0, MAX_SIZE);

	
	if (sockfd == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP具体指明使用TCP协议  
	{
		cout << INVALID_SOCKET <<"Creat socket error!" << endl;
		return false;
	}

	//socketServer = socket(AF_INET, SOCK_STREAM, 0);
	sockaddr_in their_addr; /* connector's address information */
	memset(&their_addr, 0, sizeof(their_addr));  //bin_zero
	their_addr.sin_family = AF_INET;   //声明格式  地址家族 host byte order
	their_addr.sin_port = htons(9999);//端口	将它从本机字节顺序 (Host Byte Order) 转换过来。【short, network byte order】
	their_addr.sin_addr.S_un.S_addr = inet_addr(IP);//指明连接服务器的IP地
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