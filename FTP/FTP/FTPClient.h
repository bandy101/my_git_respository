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
	bool RecvReply();//�������ӽ���
	bool SendCommand();//��FTP��������������
	bool DataConnect(char* ServerAddr);//��FTP��������������
	bool mkdirectory();//FTP����������MKD�������Ŀ¼
	bool changedir(); //����CWD����ı�Ŀ¼
	bool FTPConnection(char* FTPIP, int port);  //������Soccket���
	bool useuser(char *user);  // user���� ��֤�û���
	bool usepass(char *pwd); //pass���� ��֤����
	void subcommend(string& filepath, string& filename); //�����ת��IP��ַ
	void storfile(char* FTPIP,char* path);//�ϴ��ļ�
	void retrfile(char* FTPIP);//�����ļ�
	void listftp(char* FTPIP);  //�г�FTP������Ŀ¼
	void deletefile(); //ɾ���ļ�
	void quitftp(); //�˳��ͻ���
	void help();//˵���ĵ�
	void about();//����
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