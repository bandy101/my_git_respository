#pragma once
#include "../FTP/FTPClient.h"
#include <opencv2/opencv.hpp>
class MFCFTPClient : public FTPClient
{
public:
	//--向服务器发送USER 认证用户命令
	bool useuser(char *user)
	{
		cout << "FTP>用户名:";
		memset(CmdBuf, 0, MAX_SIZE);
		memset(Command, 0, MAX_SIZE);
		memcpy(Command, "USER ", strlen("USER "));
		memcpy(Command + strlen("USER "), user, strlen(user));
		memcpy(Command + strlen("USER ") + strlen(user), "\r\n", 2);
		//cout << "Command:" << Command << endl;
		if (!SendCommand())
		{
			error += "user send command error!\r\n"; return false;
		}
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
				error += "user error!\r\n";
				return false;
			}
		}
		buser = true;
		return true;
	}
	//--向服务器发送PASS 认证密码命令
	bool usepass(char *pwd)
	{
		if (buser)
		{
			buser = false;
			cout << "FTP>密码";
			memset(CmdBuf, 0, MAX_SIZE);
			memset(Command, 0, MAX_SIZE);
			memcpy(Command, "PASS ", strlen("PASS "));
			memcpy(Command + strlen("PASS "), pwd, strlen(pwd));
			memcpy(Command + strlen("PASS ") + strlen(pwd), "\r\n", 2);
			if (!SendCommand())
			{
				error += "send command"; return false;
			}
			//获取PASS命令的应答信息
			if (RecvReply())
			{
				if (nReplycode == 230)//230:User logged in,procced;//331:User Name okay,need password;
					cout << ReplyMsg << endl;
				else
				{
					cout << "PASS response error!" << endl;
					error += "pass or user error!\r\n";
					return false;
				}
			}
			return true;
		}
		return false;
	}
	bool mkdirectory(char *filename)
	{
		//----上传图片路径先改变目录----错误创建目录---//
		memset(Command, 0, MAX_SIZE);
		memcpy(Command, "MKD ", strlen("MKD "));
		memcpy(Command+strlen("MKD "), filename, strlen(filename));
		//memcpy(Command + strlen("MKD ")+ strlen(filename), CmdBuf, strlen(CmdBuf));
		//memcpy(Command + strlen("MKD ") + strlen(filename) + strlen(CmdBuf), "\r\n", 2);
		memcpy(Command + strlen("MKD ") + strlen(filename), "\r\n", 2);
		if (!SendCommand())
			return false;
		if (RecvReply())
		{
			if (nReplycode == 257)
				cout << ReplyMsg << endl;
			else
			{
				cout << "MKD response error!" << endl;
				//error += "create file error!\r\n";
				//closesocket(SocketControl);
				return false;
			}
		}
		return true;
	}

	bool changedir(char *in_path)
	{	

		memset(CmdBuf, 0, MAX_SIZE);
		memcpy(CmdBuf, in_path, strlen(in_path));
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
			{
				error += ReplyMsg;
			}
			else
			{
				cout << "CWD response error!" << endl;
				error += "change dir error!\r\n";
				closesocket(SocketControl);
				return false;
			}
		}
		return true;
	}

	void storfile(char* FTPIP, char *path_,char *stor_path)
	{
		//if (!ishavedetail)
		//{
		//cout << "请输入上传文件名:";
		//memset(CmdBuf, 0, MAX_SIZE);
		//cin.getline(CmdBuf, MAX_SIZE, '\n');
		//}
		char str3[100];
		memset(str3, 0, 100);
		strcpy(str3, stor_path);
		strcat(str3, "\\");
		//strcat(stor_path, "\\");
		//memcpy(stor_path, "\\", strlen("\\"));
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
		//memcpy(Command + strlen("STOR "), stor_path, strlen(stor_path));
		memcpy(Command + strlen("STOR "), str3, strlen(str3));
		memcpy(Command + strlen("STOR ")+ strlen(str3), CmdBuf, strlen(CmdBuf));
		//memcpy(Command + strlen("STOR ")  + strlen("test\\") + strlen(CmdBuf), "\r\n", 2);
		memcpy(Command + strlen("STOR ") +strlen(str3) +strlen(CmdBuf), "\r\n", 2);
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
			//error += ListBuf2;
			int nStor = send(SocketData, ListBuf2, MAX_SIZE, 0);

			if (nStor == SOCKET_ERROR)
			{
				cout << endl << "Socket send error!" << endl;
				error += "Socket send error!";
				closesocket(SocketData);
				return;
			}



			if (f2.eof())
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
public:
	//string error;
};
