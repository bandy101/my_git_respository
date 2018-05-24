#include <iostream>
using namespace std;
int main()
{
	char cmd[20];
	string k = "1234567890";
	cout <<"init"<< strlen(cmd) << endl;
	memset(cmd, 0, strlen(cmd));
	cout << "cmd:" << cmd << endl << "curent len:"<<strlen(cmd) << endl;
	memcpy(cmd, "USER ", strlen("USER "));
	memcpy(cmd, "USER ", strlen("USER "));
	memcpy(cmd+strlen("pasv"),"ab",2);
	cout << "memcpy->cmd:" << cmd << endl << "curent len:" << strlen(cmd) << endl;
	getchar();
}