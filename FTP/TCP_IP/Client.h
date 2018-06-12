#pragma once
#include <iostream>
#include <winsock2.h>
#include "../FTPMFC/SQL_operation.hpp"
#define MAX_SIZE 4096


#pragma comment(lib, "ws2_32.lib")
using namespace std;

class Client
{
public:
	Client();
	~Client() {};
	void send_recv(MySql *);
	int bytesToInt(byte* bytes, int size = 4)

	{

		int a = bytes[0] & 0xFF;

		a |= ((bytes[1] << 8) & 0xFF00);

		a |= ((bytes[2] << 16) & 0xFF0000);

		a |= ((bytes[3] << 24) & 0xFF000000);

		return a;

	}
private:
	SOCKET sockfd;
	char buf[4096];
	sockaddr_in their_addr;
	WSADATA WSAData;//WSADATA:该结构被用来储存调用
public:
	string error;
	char *datas;
};