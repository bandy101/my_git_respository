#pragma once
#include <iostream>
#include <winsock2.h>
#define MAX_SIZE 4096
#pragma comment(lib, "ws2_32.lib")
using namespace std;

class Client
{
public:
	Client();
	~Client();

private:
	SOCKET sockfd;
	char buf[4096];
public:
	string error;
	char *datas;
};