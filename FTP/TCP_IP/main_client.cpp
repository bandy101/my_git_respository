#include <iostream>
#include <winsock2.h>
#include <string.h>
#include "Servers.h"
#define MAX_SIZE 4096
using namespace std;
#define IP "127.0.0.1"
int main()
{
	Servers servers;
	servers.server_init(IP,9999);
	servers.server_begin();
	
	getchar();
	return 0;
}