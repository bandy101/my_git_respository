#pragma once
#include <mysql.h>
#include <WinSock2.h>
#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
//#include <cstring>
using namespace std;
class MySql
{
public:
	MySql(char *host, char *user, char *pwd, char *table, int port)
	{
		char *encode = "gb2312";
		pCon = mysql_init(NULL);
		datas = " "; error = " ";
		if (mysql_real_connect(pCon, host, user, pwd, table, port, NULL, 0))
		{

			char *result = "SET NAMES 'gb2312'";
			/*		strcat(result,encode);
			strcat(result,"'");*/
			mysql_query(pCon, result);
			mysql_query(pCon, "select * from telemetry_image");
		}
		else
		{
			error = "连接数据库失败！";
		}
	}
	~MySql() {};
	bool read_data_save_img(int data_row = 36)
	{


		result = mysql_store_result(pCon);
		bool rd = true;
		while (row = mysql_fetch_row(result))
		{

			for (int i = 0; i < data_row; i++)
				try
			{
				if (row[i] == NULL) { datas += ","; }
				else
				{
					datas += row[i];
					datas += ";";
				}

			}
			catch (exception)
			{
				rd = false;
				datas += ",";
			}
			datas += "\n";
			string image_name = row[26];
			int pos = image_name.rfind("/");
			unsigned long *lengths = mysql_fetch_lengths(result); //lenghs[n] 该字段长度
			destIDs = (uint32_t *)malloc(lengths[2]);
			memcpy(destIDs, row[2], lengths[2]);
			ofstream fout(image_name.substr(pos,sizeof(image_name)+1), ios::binary);
			temp = (uint32_t *)malloc(lengths[2]);
			temp = destIDs;
			fout.write((char*)destIDs, lengths[2]);
			fout.close();

		}
		mysql_free_result(result);
		mysql_close(pCon);
		return rd;
	}
public:
	string datas;
	string error;
	char buf[4096];
	uint32_t *destIDs, *temp;
	unsigned int destNum = 16000;
private:
	MYSQL *pCon;
	MYSQL_ROW row;
	MYSQL_RES *result;
};