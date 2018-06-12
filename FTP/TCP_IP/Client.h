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

private:
	SOCKET sockfd;
	char buf[4096];
	sockaddr_in their_addr;
	WSADATA WSAData;//WSADATA:该结构被用来储存调用
public:
	string error;
	char *datas;
};