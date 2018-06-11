#include "Client.h"
#define MAX_SIZE 4096
#define IP "120.236.164.111"

//----测试端口地址-----//
/*
const char user[] = "root";         //username
const char pswd[] = "IkaZ3qSviy64";         //password
const char host[] = "192.168.20.16";    //or"127.0.0.1"
const char table[] = "equipment";        //database
unsigned int port = 3369;           //server port  
*/
Client::Client() {
	error = ""; datas = " ";
	// WSAStartup:初始化当前线程通信环境，MAKEWORD:合并短整数
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)
		cout << "WSAStartup error!" << endl;

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	memset(&their_addr, 0, sizeof(their_addr));  //bin_zero
	their_addr.sin_family = AF_INET;   //声明格式  地址家族 host byte order
	their_addr.sin_port = htons(9999);//端口
	their_addr.sin_addr.S_un.S_addr = inet_addr(IP);//指明连接服务器的IP地

	if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
		error += "Server connect error!\r\n";
	}
}


void Client::send_recv(MySql *sql)
{	
	int nSend = send(sockfd, buf, sizeof(buf), 0); // 0:flag write
	if (nSend == SOCKET_ERROR) {
		error += "Socket send error!\r\n";
	}

	string *name = sql->name;
	int pos, last_pos;
	string datas = sql->datas;
	char *data;
	last_pos = datas.rfind("\n");
	pos = datas.find("\n");
	int num = sql->cord_num;
	int first_times = 0;
	while (num) {
		memset(buf, 0, MAX_SIZE);
		strcpy(buf, datas.substr(first_times, pos- first_times).c_str());
		first_times = pos;
		nSend = send(sockfd, buf, strlen(buf), 0); // 0:flag write
		if (nSend == SOCKET_ERROR) {
			cout << "Socket send error!" << endl;
			error += "Socket send error!\r\n";
		}
		memset(buf, 0, MAX_SIZE);
		try
		{
			if (recv(sockfd, buf, MAX_SIZE, 0) == SOCKET_ERROR) {
				cout << "Socket receive error!" << endl;
				error += "Socket receive error!";
			}
			string recvs = buf;
			if (int p = recvs.rfind("@") != -1)
			{
				if (recvs.substr(p + 1, 1) == "1")
				{
					error = "上传数据成功！\r\n";
				}
				else
				{
					error = "数据上传失败！\r\n";
				}
			}
			closesocket(sockfd);
			SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);
			if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
				cout << endl << "Server connect error!" << endl;
			}
			//printf("Received: %s\n", buf);
			pos = datas.find("\n", pos + 1);
		}
		catch (exception)
		{
			closesocket(sockfd);
			SOCKET sockfd = socket(AF_INET, SOCK_STREAM, 0);
			if (connect(sockfd, (sockaddr *)&their_addr, sizeof(sockaddr)) <= SOCKET_ERROR) {
				cout << endl << "Server connect error!" << endl;
			}
			//printf("Received: %s\n", buf);
			pos = datas.find("\n", pos + 1);
		}

	}
	closesocket(sockfd);
}