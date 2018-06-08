#pragma once
#include <mysql.h>
#include <WinSock2.h>
#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include "../FTP/FTPClient.h"
#define CORD_SIZE 100
//#include <cstring>
using namespace std;
class MySql
{
public:
	MySql(char *host, char *user, char *pwd, char *table, int port)
	{
		pCon = mysql_init(NULL);
		pCon_img = mysql_init(NULL);
		datas = " "; error = " "; cord_num = 0;
		if (mysql_real_connect(pCon, host, user, pwd, table, port, NULL, 0)&& mysql_real_connect(pCon_img, host, user, pwd, table, port, NULL, 0))
		{	
			//设置编码
			encode = "SET NAMES 'gb2312'";
			mysql_query(pCon, encode);
			mysql_query(pCon_img, encode);

			mysql_query(pCon, "select * from telemetry_message");
			mysql_query(pCon_img, "select * from telemetry_image");

			result_msg = mysql_store_result(pCon);
			result_img = mysql_store_result(pCon_img);

		}
		else
		{
			image_name = "连接数据库失败";
			error = "连接数据库失败！";
		}
	}
	~MySql() {};
	bool read_data_save_img(int data_row = 42)
	{
		bool rd = true;
		while (row = mysql_fetch_row(result_msg))
		{
			row_img = mysql_fetch_row(result_img);
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
			image_name = row[27];
			name[cord_num++] = image_name; //记录imge_表名
			unsigned long *lengths = mysql_fetch_lengths(result_img); //lenghs[n] 该字段长度
			destIDs = (uint32_t *)malloc(lengths[2]);
			memcpy(destIDs, row_img[2], lengths[2]);
			ofstream fout(image_name.substr(9, sizeof(image_name)), ios::binary);
			//ofstream fout(image_name, ios::binary);
			temp = (uint32_t *)malloc(lengths[2]);
			temp = destIDs;
			fout.write((char*)destIDs, lengths[2]);
			fout.close();
			//cord_num += 1;

		}
		mysql_free_result(result_img);
		mysql_free_result(result_msg);
		mysql_close(pCon_img);
		mysql_close(pCon);
		return rd;
	}
public:
	string datas;
	string error;
	char buf[4096];
	uint32_t *destIDs, *temp;
	unsigned int destNum = 16000;
	string image_name;
	int cord_num;
	string name[CORD_SIZE];
private:
	
	FTPClient ftp;
	char *encode;
	MYSQL_RES *result_img;
	MYSQL_RES *result_msg;
	MYSQL *pCon;
	MYSQL *pCon_img;
	MYSQL_ROW row;
	MYSQL_ROW row_img;
	MYSQL_RES *result;
};