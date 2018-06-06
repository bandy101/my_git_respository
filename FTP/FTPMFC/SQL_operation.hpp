#pragma once
#include <mysql.h>
#include <WinSock2.h>
#include <iostream>
#include <string>
#include <stdio.h>
//#include <cstring>
using namespace std;
class MySql
{
public:
	MySql(MYSQL *con,char *host,char *user,char *pwd,char *table,int port,char *encode="gb2312")
	{
		pCon = mysql_init(NULL);
		datas = " "; error = " ";
		if (mysql_real_connect(pCon, host, user, pwd, table, port, NULL, 0))
		{
			
			char *result = "SET NAMES '";
			strcat(result,encode);
			strcat(result,"'");
			mysql_query(pCon, result);
		}
		else
		{
			error = "连接数据库失败！";  
		}
	}
	bool read_data(int data_row = 36)
	{
		result= mysql_store_result(pCon);
		bool rd = true;
		while (row = mysql_fetch_row(result))
		{
			for (int i=0; i < data_row; i++)
				try
			{
				datas += row[i];
				datas += ";";
			}
			catch (exception)
			{
				rd = false;
				datas += ",";
			}
			//cout << datas.c_str() << endl;
		}
		mysql_free_result(result);
		mysql_close(pCon);
		return rd;
	}
public:
	string datas;
	string error;
private:
	MYSQL *pCon;
	MYSQL_ROW row;
	MYSQL_RES *result;
};