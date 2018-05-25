#pragma once
#define MAX_SIZE 4096
#include<conio.h>
#include <iostream>
#include <winsock2.h>
#include <string>
#include <fstream>

#pragma comment(lib, "ws2_32.lib")

using namespace std;

class FTPClient {
public:
	bool RecvReply();//控制连接接收
	bool SendCommand();//向FTP服务器发送命令
	bool DataConnect(char* ServerAddr);//向FTP服务器发送命令
	bool mkdirectory();//FTP服务器发送MKD命令，创建目录
	bool changedir(); //发送CWD命令，改变目录
	bool FTPConnection(char* FTPIP, int port);  //建立与Soccket库绑定
	bool useuser(char *user);  // user命令 认证用户名
	bool usepass(char *pwd); //pass命令 认证密码
	void subcommend(string& filepath, string& filename); //输入和转换IP地址
	void storfile(char* FTPIP,char* path);//上传文件
	void retrfile(char* FTPIP);//下载文件
	void listftp(char* FTPIP);  //列出FTP服务器目录
	void deletefile(); //删除文件
	void quitftp(); //退出客户端
	void help();//说明文档
	void about();//关于
	bool ishavedetail;
	char CmdBuf[MAX_SIZE];
	char Command[MAX_SIZE];
	char ReplyMsg[MAX_SIZE];
public:
	int nReplycode;
	bool bConnected;
	bool buser;
	string error ="PARENT";
	SOCKET SocketControl;
	SOCKET SocketData;
};