#pragma once
#include <iostream>
#include <winsock2.h>
#include <string.h>
#pragma comment(lib, "ws2_32.lib")
#define MAX_SIZE 4096
using namespace std;
class Servers {
public:
	bool server_init(char *IP, int port);
	void server_begin();
private:
	SOCKET socketServer;
	SOCKET socketData;
	SOCKET other;
	sockaddr_in serveraddr;
	sockaddr_in otheraddr;
};