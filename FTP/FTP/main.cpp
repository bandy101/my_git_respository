#include <iostream>
#include "FTPClient.h"

using namespace std;


int main(int argc,char* argv[])
{	
	SetConsoleTitleA("FTP客户端控制台版 v1.0");
	FTPClient ftp;
	//检测命令含参数
	if (argc != 2)
	{
		cout << "请输入FTP服务器IP地址:";
		string a, b;
		ftp.subcommend(a, b);
		while (!(const_cast<char*>(a.c_str())))
		{
			cout << "连接失败！请检查正确！" << endl;
			ftp.subcommend(a, b);
		}
		if (ftp.FTPConnection(const_cast<char*>	(a.c_str()), 21))
		{
			bool flag;
			do
			{
				ftp.useuser();
				flag = ftp.usepass();
			} while (!flag);
			cout << "tip :help命令获取帮助！" << endl;
			cout << endl;
			while (true)
			{
				cout << "FTP>";
				string order, detail;
				ftp.subcommend(order, detail);
				if (detail.length() != 0)
				{
					memset(ftp.CmdBuf, 0, MAX_SIZE);
					memcpy(ftp.CmdBuf, detail.data(), detail.length());
					ftp.ishavedetail = true;
				}
				if (order == "ls")
					ftp.listftp(const_cast<char*>(a.c_str()));
				else if(order == "stor")
					ftp.storfile(const_cast<char*>(a.c_str()));
				else if(order == "retr")
					ftp.retrfile(const_cast<char*>(a.c_str()));
				else if(order == "cwd")
					ftp.changedir();
				else if(order == "mkd")
					ftp.mkdirectory();
				else if(order == "help")
					ftp.help();
				else if(order == "dele")
					ftp.deletefile();
				else if(order == "about")
					ftp.about();
				else if(order == "quit")
				{
					ftp.quitftp();
					break;
				}
				else if(order == "user")
				{
					bool flag;
					do
					{
						ftp.useuser();
						flag = ftp.usepass();
					} while (!flag);
				}
				else
				{
					cout << "FTP>无此命令！查看help命令帮助" << endl;
					ftp.ishavedetail = false;
				}
			}
		}
	}
	getchar();
}