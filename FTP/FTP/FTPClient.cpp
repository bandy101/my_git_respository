#include<conio.h>
#include <iostream>
#include <winsock2.h>
//#include <Winineti.h>
#include <string>
#include <fstream>
#include "FTPClient.h"
#include <time.h>
#define MAX_SIZE 4096
#pragma comment(lib, "ws2_32.lib")

using namespace std;
//#define _WINSOCK_DEPRECATED_NO_WARNINGS to disable deprecated API warnings
//---控制连接接收
bool FTPClient::RecvReply()  //控制连接接收
{
	int nRecv;
	memset(ReplyMsg, 0, MAX_SIZE);// 数组ReplyMsg置0
	//cout << "string 1 ReplyMsg int :" << ReplyMsg << endl;
	nRecv = recv(SocketControl, ReplyMsg, MAX_SIZE, 0);//返回实际读入缓冲的数据的字节数
	//cout << "string 2 ReplyMsg int :" << ReplyMsg << endl;
	if (nRecv == SOCKET_ERROR)
	{
		cout << "Socket receive error!" << endl;
		error += "Socket receive error!";
		closesocket(SocketControl);
		return false;
	}
	//获取相应信息and响应码
	if (nRecv>4) {
		char *ReplyCodes = new char[3];
		memset(ReplyCodes, 0, 3);
		memcpy(ReplyCodes, ReplyMsg, 3);
		nReplycode = atoi(ReplyCodes); //将字符串转换为整数 220：main first load return value

	
	}
	return true;
}

bool FTPClient::SendCommand()//向ftp服务器发送命令
{
	//控制连接发送数据
	int nSend;
	printf("%s", Command);
	//error += Command;
	nSend = send(SocketControl,Command, strlen(Command), 0);//flag =0 ->write
	cout << "nSend:" << nSend << endl;
	if (nSend == SOCKET_ERROR) {
		error += Command;
		error += "\r\n";
		error += "Socket Socket send error!!";
		cout << "Socket send error!" << endl;
		return false;
	}
	return true;
}
//---pasv:被动模式----//发送PASV命令////
bool FTPClient::DataConnect(char* ServerAddr)
{
	//发送PASV命令
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "PASV ", strlen("PASV "));
	memcpy(Command+strlen("PASV "), "\r\n", 2);
	if (!SendCommand())
		return false;
	//获取PASV命令的应答信息
	if (RecvReply()) {
		if (nReplycode != 227){
			cout << "PASV response error!" << endl;
			error += ReplyMsg;
			error += "\r\n";
			error += "PASV response error!";
			closesocket(SocketControl);
			return false;
		}
	}
	//分离PASV的应答信息
	char* part[6];
	if (strtok(ReplyMsg,"("))
	{
		for (int i = 0; i<5; i++)
		{
			part[i] = strtok(NULL, ",");
			if (!part[i])
				return false;
		}
		part[5] = strtok(NULL, ")");
		if (!part[5])
			return false;
	}
	else
	{
		return false;
	}
	//获取FTP服务器数据端口
	unsigned short ServerPort;
	ServerPort = unsigned short((atoi(part[4]) << 8) + atoi(part[5])); //atoi函数把字符串转换成整型数
																	//创建数据连接Socket
	SocketData = socket(AF_INET, SOCK_STREAM, 0);
	if (SocketData == INVALID_SOCKET) {
		cout << "create socket error!" << endl;
		return false;
	}
	//定义Socket地址和端口
	sockaddr_in serveraddr2;
	memset(&serveraddr2, 0, sizeof(serveraddr2));
	serveraddr2.sin_family = AF_INET;
	serveraddr2.sin_port = htons(ServerPort);
	serveraddr2.sin_addr.S_un.S_addr = inet_addr(ServerAddr);

	//serveraddr2.sin_addr.S_un.S_addr = inet_pton(ServerAddr);
	//向FTP服务器发送Connect请求
	int nConnect;
	nConnect = connect(SocketData, (sockaddr*)&serveraddr2, sizeof(serveraddr2));
	if (nConnect == SOCKET_ERROR) {
		cout << endl << "Server connect error!" << endl;
		error += "PASV  connect error!!";
		return false;
	}
	return true;
}
//---ftp服务器发送mkd命令 create direction////


bool FTPClient::mkdirectory()
{
	//if (!ishavedetail) {
		cout << "请输入你要创建的文件夹名：";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\b');
	//}
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "MKD", strlen("MKD"));
	memcpy(Command + strlen("MKD"), CmdBuf, strlen(CmdBuf));
	memcpy(Command + strlen("MKD") + strlen(CmdBuf), "\r\n", 2);
	if (!SendCommand())
		return false;
	if (RecvReply())
	{
		if (nReplycode == 257)
			cout << ReplyMsg << endl;
		else
		{
			cout << "MKD response error!" << endl;
			closesocket(SocketControl);
			return false;
		}
	}
	return true;
}
//--ftp服务器发送CWD（改变工作目录命令）---///
bool FTPClient::changedir()
{
	//if (!ishavedetail)
	//{
		cout << "请输入需要进入的文件夹路径";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\n');

	//}
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "CWD ", strlen("CWD "));
	memcpy(Command + strlen("CWD ") + strlen(CmdBuf), "\r\n", 2);
		if (!SendCommand())
			return false;
	//---------------获得cwd命令应答信息------------------
	if (RecvReply())
	{
		cout << "nReplycode:" << nReplycode << endl;
		if (nReplycode == 250) //257
			cout << ReplyMsg << endl;
		else
		{
			cout << "CWD response error!" << endl;
			closesocket(SocketControl);
			return false;
		}
	}
	return true;
}
//---------建立与Socket库绑定
bool FTPClient::FTPConnection(char* FTPIP, int port)
{
	cout << "FTPCONNECT:" << FTPIP << endl;
	WSADATA WSAData;//WSADATA:该结构被用来储存调用
					//AfxSocketInit 全局函数返回Windows Socket 初始化信息
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:初始化当前线程通信环境，MAKEWORD:合并短整数
	{
		cout << "WSAStartup error!" << endl;
		return false;
	}
	//创建控制连接Socket
	//int socket(int domain, int type, int protocol);socket() 只是返回你以后在系统调用种可能用到的 socket 描述符
	SocketControl = socket(AF_INET, SOCK_STREAM, 0); //AF_INET指明使用TCP / IP协议族；
	if (SocketControl == INVALID_SOCKET)//SOCK_STREAM, IPPROTO_TCP具体指明使用TCP协议  
	{
		cout << "Creat socket error!" << endl;
		return false;
	}
	//定义Socket地址和端口
	sockaddr_in serveraddr;  //结构体
	memset(&serveraddr, 0, sizeof(serveraddr));  //
	serveraddr.sin_family = AF_INET;   //声明格式  地址家族 host byte order
	//端口.sin_port = 0（o）; /* 随机选择一个没有使用的端口 */
	serveraddr.sin_port = htons(port);//端口	将它从本机字节顺序 (Host Byte Order) 转换过来。【short, network byte order】
	//htons(0) 随机一个没有使用的端口
	serveraddr.sin_addr.S_un.S_addr = inet_addr(FTPIP);//指明连接服务器的IP地址     //inet_addr(),将IP地址从点数格式转换成无符号长整型。
	//
	//bzero(&(dest_addr.sin_zero), ; /* zero the rest of the struct */		//向FTP服务器发送Connect请求
	//inet_addr()返回的地址已经是网络字节格式，所以你无需再调用 函数htonl()。 
	//将一个in_addr结构体输出成点数格式 inet_ntoa 和inet_addr 功能相反	
	cout << "FTP >Control connect..."<<endl;
		int nConnect;
		////connect 和bind函数类似功能将套接字和机器上一定端口相连
		//int bind(int sockfd, struct sockaddr *my_addr, int addrlen);
	nConnect = connect(SocketControl, (sockaddr*)&serveraddr, sizeof(serveraddr)); //bind
	if (nConnect <=SOCKET_ERROR) {
		cout << endl << "Server connect error!" << endl;
		return false;
	}
	//获得Connect应答信息
	if (RecvReply())
	{
		if (nReplycode == 220)
			cout << "ReplyMsg:"<<ReplyMsg << endl;
		else
		{
			cout << "Connet response error!" << endl;
			closesocket(SocketControl);
			return false;
		}
	}
	bConnected = true;
	return true;
}
//--向服务器发送USER 认证用户命令
bool FTPClient::useuser()
{
	cout << "FTP>用户名:";
	memset(CmdBuf, 0, MAX_SIZE);
	cin.getline(CmdBuf, MAX_SIZE, '\n');
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "USER ", strlen("USER "));
	memcpy(Command + strlen("USER "), CmdBuf, strlen(CmdBuf));
	memcpy(Command + strlen("USER ") + strlen(CmdBuf), "\r\n", 2);
	cout << "Command:" << Command << endl;
	if (!SendCommand())
		return false;
	//获得USER命令的应答信息
	if (RecvReply())
	{
		if (nReplycode == 331)//230:User logged in,procced;//331:User Name okay,need password;
			cout << ReplyMsg << endl;
		else
		{
			//cout << "USER response error!" << endl;
			//closesocket(SocketControl);
			//return false;
			buser = false;
			return false;
		}
	}
	buser = true;
	return true;
}
//--向服务器发送PASS 认证密码命令
bool FTPClient::usepass()
{
	if (buser)
	{
		buser = false;
		cout << "FTP>密码";
		memset(CmdBuf, 0, MAX_SIZE);
		cout.flush();
		for (int i = 0; i<MAX_SIZE; i++)
		{
			CmdBuf[i] = _getch();
			if (CmdBuf[i] == '\r')
			{
				CmdBuf[i] = '\0';
				break;
			}
			else
				cout << "*";
		}
		cout << endl;
		memset(Command, 0, MAX_SIZE);
		memcpy(Command, "PASS ", strlen("PASS "));
		memcpy(Command + strlen("PASS "), CmdBuf, strlen(CmdBuf));
		memcpy(Command + strlen("PASS ") + strlen(CmdBuf), "\r\n", 2);
		if (!SendCommand())
			return false;
		//获取PASS命令的应答信息
		if (RecvReply())
		{
			if (nReplycode == 230)//230:User logged in,procced;//331:User Name okay,need password;
				cout << ReplyMsg << endl;
			else
			{
				cout << "PASS response error!" << endl;
				return false;
			}
		}
		return true;
	}
	return false;
}
//--上传文件
void FTPClient::storfile(char* FTPIP,char *path_)
{
	//if (!ishavedetail)
	//{
		//cout << "请输入上传文件名:";
		//memset(CmdBuf, 0, MAX_SIZE);
		//cin.getline(CmdBuf, MAX_SIZE, '\n');
	//}
	ifstream f2;
	//char *path;
	//path = "G:\\git\\my_git_respository\\FTP\\FTP\\python.txt";
	//path = "python.txt";
	f2.open(path_, ios::binary);
		if (!f2)
		{
			cout << "Cannot open file!" << endl;
			error += "Cannot open file!";
			return;
		}
	string strPath(path_);
	cout << "str:" << strPath << endl;
	string filepath, filename;
	int nPos = strPath.rfind('\\');
	if (-1 != nPos)
	{
		filename = strPath.substr(nPos + 1, strPath.length() - nPos - 1);
		filepath = strPath.substr(0, nPos);
		cout << "filename:" << filename << endl;
		cout << "filepath:" << filepath << endl;
		memset(CmdBuf, 0, MAX_SIZE);
		memcpy(CmdBuf, filename.data(), strlen(filename.data()));
	}
	else
		cout << "nPos:" << nPos << endl;
	char Ftpstor[MAX_SIZE];
	memset(Ftpstor, 0, MAX_SIZE);
	memcpy(Ftpstor, FTPIP, strlen(FTPIP));
	if (!DataConnect(Ftpstor))
		return;
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "STOR ", strlen("STOR "));
	memcpy(Command + strlen("STOR "), CmdBuf, strlen(CmdBuf));
	//memcpy(Command + strlen("STOR ") + strlen("test_\\") + strlen(CmdBuf), "\r\n", 2);
	memcpy(Command + strlen("STOR ")  +strlen(CmdBuf), "\r\n", 2);
	if (!SendCommand())
		return;
	//获取STOR 上传文件命令的应答信息
	if (RecvReply())
	{
		cout << ReplyMsg << endl;
		if (nReplycode == 125 || nReplycode == 150 || nReplycode == 226)
			cout << ReplyMsg << endl;
		else
		{
			cout << "STOR response error111!" << endl;
			error += "STOR response error111";
			closesocket(SocketControl);
			//Sleep(1);
			return;
		}
	}
	char ListBuf2[MAX_SIZE];
	while (true)
	{

		memset(ListBuf2, 0, MAX_SIZE);
	
		f2.read(ListBuf2, MAX_SIZE);
		error += ListBuf2;
		int nStor = send(SocketData, ListBuf2, MAX_SIZE, 0);

		if (nStor == SOCKET_ERROR)
		{
			cout << endl << "Socket send error!" << endl;
			error += "Socket send error!";
			closesocket(SocketData);
			return;
		}
	
			
		
		if  (f2.eof())
			break;
	}
		//break;
	f2.close();
	closesocket(SocketData);
	if (RecvReply())
	{
		if (nReplycode == 226)
			cout << ReplyMsg << endl;
		else
		{
			cout << "STOR response error!" << endl;
			closesocket(SocketControl);
			return;
		}
	}
}
//--下载文件
void FTPClient::retrfile(char* FTPIP)
{
	if (!ishavedetail)
	{
		cout << "请输入下载文件名:";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\n');
	}
	char Ftpretr[MAX_SIZE];
	memset(Ftpretr, 0, MAX_SIZE);
	memcpy(Ftpretr, FTPIP, strlen(FTPIP));
	if (!DataConnect(Ftpretr))
		return;
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "RETR", strlen("RETR"));
	memcpy(Command + strlen("RETR"), CmdBuf, strlen(CmdBuf));
	memcpy(Command + strlen("RETR") + strlen(CmdBuf), "\r\n", 2);
	cout << "请输入保存的文件名：";
	memset(CmdBuf, 0, MAX_SIZE);
	cin.getline(CmdBuf, MAX_SIZE, '\n');
		if (!SendCommand())
			return;
	//获取retr 下载文件命令的应答信息
	if (RecvReply())
	{
		cout << "nReplycode:" << nReplycode;
		if (nReplycode == 125 || nReplycode == 150 || nReplycode == 226)
			cout << ReplyMsg << endl;
		else
		{
			cout << "RETR response error!" << endl;
			closesocket(SocketControl);
			return;
		}
	}
	ofstream f1(CmdBuf);
	if (f1)
	{
		cout << "file can not open!" << endl;
		return;
	}
	int nRetr;
	char ListBuf1[MAX_SIZE];
	while (true)
	{
		memset(ListBuf1, 0, MAX_SIZE);
		nRetr = recv(SocketData, ListBuf1, MAX_SIZE, 0);
			f1.write(ListBuf1, MAX_SIZE);
		if (nRetr == SOCKET_ERROR)
		{
			cout << endl << "Socket receive error!" << endl;
			closesocket(SocketData);
			return;
		}
		if (nRetr <= 0)
			break;
	}
	f1.close();
	closesocket(SocketData);
	if (RecvReply())
	{
		if (nReplycode == 226)
			cout << ReplyMsg << endl;
		else
		{
			cout << "RETR response error!" << endl;
			closesocket(SocketControl);
			return;
		}
	}
}
//--FTP发送list命令
void FTPClient::listftp(char* FTPIP)
{	
	char FtpServer[MAX_SIZE];
	memset(FtpServer, 0, MAX_SIZE);
	memcpy(FtpServer, FTPIP, strlen(FTPIP));
	if (!DataConnect(FtpServer))
		return;
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "LIST ", strlen("LIST "));
	memcpy(Command + strlen("LIST "), "\r\n", 2);
	if (!SendCommand())
		return;
	//获取LIST命令的应答信息
	Sleep(1);
	if (RecvReply())
	{	
		//125:Data connection alreadlyopen;transfer staring.
		//150:File status okay,about to data connection;
		//226:closing data connection ;150:Opening ASCII mode data connection for/bin/ls
		if (nReplycode == 125 || nReplycode == 150 || nReplycode == 226)
			cout << ReplyMsg << endl;
		else
		{
			cout << "LIST response error!" << endl;
			closesocket(SocketControl);
			//Sleep(1);
			return;
		}
	}
	//获得list命令目录信息
	int nRecv;
	char ListBuf[MAX_SIZE];
	while (true)
	{
		memset(ListBuf, 0, MAX_SIZE);
		nRecv = recv(SocketData, ListBuf, MAX_SIZE, 0);
		if (nRecv == SOCKET_ERROR)
		{
			cout << endl << "Socket send error!" << endl;
			closesocket(SocketData);
			return;
		}
		if (nRecv <= 0)
			break;
		cout << ListBuf;
	}
	closesocket(SocketData);
	if (RecvReply())
	{
		if (nReplycode == 226) //226:closing data connection;
			cout << ReplyMsg << endl;
		else
		{
			cout << "LIST response error!" << endl;
			closesocket(SocketControl);
			return;
		}
	}
}
//--删除文件
void FTPClient::deletefile()
{
	if (!ishavedetail)
	{
		cout << "请输入删除的文件名:";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\n');
	}
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "DELE", strlen("DELE"));
	memcpy(Command + strlen("DELE"), CmdBuf, strlen(CmdBuf));
	memcpy(Command + strlen("DELE") + strlen(CmdBuf), "\r\n", 2);
	if (!SendCommand())
		return;
	//获取DELE删除文件命令的应答信息
	if (RecvReply())
	{
		if (nReplycode == 250)
			cout << ReplyMsg << endl;
		else
		{
			cout << "DELE response error!" << endl;
			closesocket(SocketControl);
			return;
		}
	}
}
//--退出客户端
void FTPClient::quitftp()
{
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "QUIT", strlen("QUIT"));
	memcpy(Command + strlen("QUIT"), "\r\n", 2);
	if (!SendCommand())
		return;
	//获取QUIT删除文件命令的应答信息
	if (RecvReply())
	{
		if (nReplycode == 221) //221:goodbay closing session;
		{
			cout << ReplyMsg << endl;
			bConnected = false;
			closesocket(SocketControl);
			return;
		}
		else
		{
			cout << "QUIT response error!" << endl;
			closesocket(SocketControl); 
				return;
		}
		}
		WSACleanup();
	}
//--输入和转换IP地址
void FTPClient::subcommend(string& filepath, string& filename)
{
	memset(CmdBuf, 0, MAX_SIZE);
	cin.getline(CmdBuf, MAX_SIZE, '\n');
	string strPath(CmdBuf);
	int nPos = strPath.rfind(' ');
	if (-1 != nPos)
	{
		filename = strPath.substr(nPos + 1, strPath.length() - nPos - 1);
		filepath = strPath.substr(0, nPos);
	}
	else
		filepath = CmdBuf;
}
void FTPClient::about()
{
	cout << "--------关于FTP客户端控制台版-----------" << endl;
	cout << "2018-5-23" << endl;
}

void FTPClient::help()
{
	cout << "---------FTPClient控制台版帮助-----------" << endl;
	cout << "ls 列出所有目录文件\n";
	cout << "stor 上传文件\n";
	cout << "retr 下载文件\n";
	cout << "dele 删除文件\n";
	cout << "cwd 进入指定目录\n";
	cout << "help 帮助\n";
	cout << "about 关于\n";
	cout << "------------" << endl;
}