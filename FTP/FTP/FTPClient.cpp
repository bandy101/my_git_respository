#include<conio.h>
#include <iostream>
#include <winsock2.h>
#include <string>
#include <fstream>
#include "FTPClient.h"
#define MAX_SIZE 4096
#pragma comment(lib, "ws2_32.lib")
using namespace std;
//---控制连接接收
bool FTPClient::RecvReply()  //控制连接接收
{
	int nRecv;
	memset(ReplyMsg, 0, MAX_SIZE);//memset?
	nRecv = recv(SocketControl, ReplyMsg, MAX_SIZE, 0);
	if (nRecv == SOCKET_ERROR)
	{
		cout << "Socket receive error!" << endl;
		closesocket(SocketControl);
		return false;
	}
	//获取相应信息and响应码
	if (nRecv>4) {
		char *ReplyCodes = new char[3];
		memset(ReplyCodes, 0, 3);
		memcpy(ReplyCodes, ReplyMsg, 3);
		nReplycode = atoi(ReplyCodes); //??	
	}
	return true;
}

bool FTPClient::SendCommand()//向ftp服务器发送命令
{
	//控制连接发送数据
	int nSend;
	nSend = send(SocketControl,Command, strlen(Command), 0);
	if (nSend == SOCKET_ERROR) {
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
	memcpy(Command, "PASV", strlen("PASV"));
	memcpy(Command+strlen("PASV"), "\r\n", 2);
	if (!SendCommand())
		return false;
	//获取PASV命令的应答信息
	if (RecvReply()) {
		if (nReplycode != 227){
			cout << "PASV response error!" << endl;
			closesocket(SocketControl);
			return false;
		}
	}
	//分离PASV的应答信息
	char* part[6];
	if (strtok(ReplyMsg, "("))
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
	//向FTP服务器发送Connect请求
	int nConnect;
	nConnect = connect(SocketData, (sockaddr*)&serveraddr2, sizeof(serveraddr2));
	if (nConnect == SOCKET_ERROR) {
		cout << endl << "Server connect error!" << endl;
		return false;
	}
	return true;
}
//---ftp服务器发送mkd命令 create direction////
bool FTPClient::mkdirectory()
{
	if (!ishavedetail) {
		cout << "请输入你要创建的文件夹名：";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\b');
	}
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
	if (!ishavedetail)
	{
		cout << "请输入需要进入的文件夹路径";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\n');

	}
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "CWD", strlen("CWD"));
	memcpy(Command + strlen("CWD") + strlen(CmdBuf), "\r\n", 2);
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
///---------建立与Socket库绑定
bool FTPClient::FTPConnection(char* FTPIP, int port)
{
	WSADATA WSAData;//WSADATA:该结构被用来储存调用
					//AfxSocketInit 全局函数返回Windows Socket 初始化信息
	if (WSAStartup(MAKEWORD(2, 2), &WSAData) != 0)//WSAStartup:初始化当前线程通信环境，MAKEWORD:合并短整数
	{
		cout << "WSAStartup error!" << endl;
		return false;
	}
	//创建控制连接Socket
	SocketControl = socket(AF_INET, SOCK_STREAM, 0);
	if (SocketControl == INVALID_SOCKET)
	{
		cout << "Creat socket error!" << endl;
		return false;
	}
	//定义Socket地址和端口
	sockaddr_in serveraddr;
	memset(&serveraddr, 0, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_port = htons(port);//端口
	serveraddr.sin_addr.S_un.S_addr = inet_addr(FTPIP);//地址
													   //向FTP服务器发送Connect请求
	cout << "FTP >Control connect..."<<endl;
		int nConnect;
	nConnect = connect(SocketControl, (sockaddr*)&serveraddr, sizeof(serveraddr));
	if (nConnect == SOCKET_ERROR) {
		cout << endl << "Server connect error!" << endl;
		return false;
	}
	//获得Connect应答信息
	if (RecvReply())
	{
		if (nReplycode == 220)
			cout << ReplyMsg << endl;
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
	memcpy(Command, "USER", strlen("USER"));
	memcpy(Command + strlen("USER"), CmdBuf, strlen(CmdBuf));
	memcpy(Command + strlen("USER") + strlen(CmdBuf), "\r\n", 2);
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
			cout << "USER response error!" << endl;
			closesocket(SocketControl);
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
			CmdBuf[i] == getch();
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
		memcpy(Command, "PASS", strlen("PASS"));
		memcpy(Command + strlen("PASS"), CmdBuf, strlen(CmdBuf));
		memcpy(Command + strlen("PASS") + strlen(CmdBuf), "\r\n", 2);
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
}
//--上传文件
void FTPClient::storfile(char* FTPIP)
{
	if (!ishavedetail)
	{
		cout << "请输入上传文件名:";
		memset(CmdBuf, 0, MAX_SIZE);
		cin.getline(CmdBuf, MAX_SIZE, '\n');
	}
	ifstream f2;
	f2.open(CmdBuf, ios::in);
		if (!f2)
		{
			cout << "Cannot open file!" << endl;
			return;
		}
	string strPath(CmdBuf);
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
	char Ftpstor[MAX_SIZE];
	memset(Ftpstor, 0, MAX_SIZE);
	memcpy(Ftpstor, FTPIP, strlen(FTPIP));
	if (!DataConnect(Ftpstor))
		return;
	memset(Command, 0, MAX_SIZE);
	memcpy(Command, "STOR", strlen("STOR"));
	memcpy(Command + strlen("STOR"), CmdBuf, strlen(CmdBuf));
	memcpy(Command + strlen("STOR") + strlen(CmdBuf), "\r\n", 2);
	if (!SendCommand())
		return;
	//获取STOR 上传文件命令的应答信息
	if (RecvReply())
	{
		if (nReplycode == 125 || nReplycode == 150 || nReplycode == 226)
			cout << ReplyMsg << endl;
		else
		{
			cout << "STOR response error!" << endl;
			closesocket(SocketControl);
			return;
		}
	}
	char ListBuf2[MAX_SIZE];
	while (true)
	{
		memset(ListBuf2, 0, MAX_SIZE);
		f2.read(ListBuf2, MAX_SIZE);
		int nStor = send(SocketData, ListBuf2, MAX_SIZE, 0);
		if (nStor == SOCKET_ERROR)
		{
			cout << endl << "Socket send error!" << endl;
			closesocket(SocketData);
			return;
		}
		break;
	}
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
	memcpy(Command, "LIST", strlen("LIST"));
	memcpy(Command + strlen("LIST"), "\r\n", 2);
	if (!SendCommand())
		return;
	//获取LIST命令的应答信息
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
