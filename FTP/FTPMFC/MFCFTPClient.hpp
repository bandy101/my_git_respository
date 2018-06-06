#pragma once
#include "../FTP/FTPClient.h"
#include <opencv2/opencv.hpp>
class MFCFTPClient : public FTPClient
{
public:
	//--�����������USER ��֤�û�����
	bool useuser(char *user)
	{
		cout << "FTP>�û���:";
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
		//���USER�����Ӧ����Ϣ
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
	//--�����������PASS ��֤��������
	bool usepass(char *pwd)
	{
		if (buser)
		{
			buser = false;
			cout << "FTP>����";
			memset(CmdBuf, 0, MAX_SIZE);
			memset(Command, 0, MAX_SIZE);
			memcpy(Command, "PASS ", strlen("PASS "));
			memcpy(Command + strlen("PASS "), pwd, strlen(pwd));
			memcpy(Command + strlen("PASS ") + strlen(pwd), "\r\n", 2);
			if (!SendCommand())
			{
				error += "send command"; return false;
			}
			//��ȡPASS�����Ӧ����Ϣ
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
		//----�ϴ�ͼƬ·���ȸı�Ŀ¼----���󴴽�Ŀ¼---//
		memset(Command, 0, MAX_SIZE);
		memcpy(Command, "MKD ", strlen("MKD "));
		memcpy(Command+strlen("MKD "), filename, strlen(filename));
		memcpy(Command + strlen("MKD")+ strlen(filename), CmdBuf, strlen(CmdBuf));
		memcpy(Command + strlen("MKD") + strlen(filename) + strlen(CmdBuf), "\r\n", 2);
		if (!SendCommand())
			return false;
		if (RecvReply())
		{
			if (nReplycode == 257)
				cout << ReplyMsg << endl;
			else
			{
				cout << "MKD response error!" << endl;
				error += "create file error!\r\n";
				closesocket(SocketControl);
				return false;
			}
		}
		return true;
	}
public:
	//string error;
};
