#pragma once
#include <mysql.h>
#include <WinSock2.h>
#include <iostream>
#include <string>
#include <stdio.h>
#include <typeinfo>
#define MAX_SIZE 1000
//#include <cstring>
using namespace std;
class MySql
{
public:
	MySql(char *host,char *user,char *pwd,char *table,int port)
	{
		char *encode = "gb2312";
		pCon = mysql_init(NULL);
		pCon_ = mysql_init(NULL);
		datas = " "; error = " ";
		if (mysql_real_connect(pCon, host, user, pwd, table, port, NULL, 0)&& mysql_real_connect(pCon_, host, user, pwd, table, port, NULL, 0))
		{
			
			char *result = "SET NAMES 'gb2312'";
	/*		strcat(result,encode);
			strcat(result,"'");*/
			mysql_query(pCon, result);
			mysql_query(pCon, "select * from telemetry_message");
			result_msg = mysql_store_result(pCon);

			//mysql_close(pCon);
			mysql_query(pCon_, "SET NAMES 'gb2312'");
			mysql_query(pCon_, "select * from telemetry_image");
			result_img = mysql_store_result(pCon_);

		}
		else
		{
			error = "连接数据库失败！";  
		}
	}
	~MySql() {};
	bool read_data(int data_row = 36)
	{
		

		
		
		
		bool rd = true;
		while (row = mysql_fetch_row(result_msg))
		{
			row_img = mysql_fetch_row(result_img);
			for (int i=0; i < data_row; i++)
				try
			{
				if (row[i] == NULL) { datas += ","; }
				else
				{
					//bit i;
					datas += (char *)row[i];
					datas += ";";
				}

			}
			catch (exception)
			{
				rd = false;
				datas += ",";
			}
			datas += "\n";

			string img_name = row[27];
			name[img_num++] = img_name;
			//printf("%s\n", typeid(row[27]).name());//类型
			//memcpy(buf,(char*)row[2],strlen(row[2]));
			unsigned long *lengths = mysql_fetch_lengths(result_img); //lenghs[n] 该字段长度
			//cout << lengths[2] << endl;
			destIDs = (uint32_t *)malloc(lengths[2]);
			memcpy(destIDs, row_img[2], lengths[2]);
			ofstream fout(img_name.substr(9, sizeof(img_name)) , ios::binary);
			ofstream test("test.jpg", ios::binary);
			temp = (uint32_t *)malloc(lengths[2]);
			temp = destIDs;
			int j = 0;
			
			//cout << "s:" <<strlen( (char*)&s);
			int num_fields = mysql_num_fields(result_img);
			//cout << num_fields << endl;
			fout.write((char*)destIDs, lengths[2]);

				//cout << temp;
				//cout << destIDs << endl;
			
			//break;
			//fout.write((char *)(destIDs), sizeof(destIDs));
			//cout << *destIDs << endl;
		}
		//temp= (uint32_t *)malloc(destNum * sizeof(uint32_t));
		//temp = destIDs;
		//for (int i = 0; i<destNum; i++)
		//{
		//	printf("destIDs[%d]:%d\t", i + 1, *temp++);
		//}
		mysql_free_result(result_msg);
		mysql_close(pCon);
		return rd;
	}
public:
	string datas;
	string error;
	char buf[4096];
	uint32_t *destIDs, *temp;
	unsigned int destNum = 16000;
	string name[MAX_SIZE];
	int img_num = 0;
private:
	MYSQL_RES *result_img;
	MYSQL_RES *result_msg;
	MYSQL *pCon;
	MYSQL *pCon_;
	MYSQL_ROW row;
	MYSQL_ROW row_img;
	MYSQL_RES *result;
};