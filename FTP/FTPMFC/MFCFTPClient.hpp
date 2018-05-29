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
public:
	//string error;
};
