#pragma once

#include <mysql.h>
#include <WinSock2.h>
#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include "MFCFTPClient.hpp"
//#include "Char_Int.hpp"
#define CORD_SIZE 100
#define CORD 42
#pragma execution_character_set("GB2312")
//#include <cstring>
using namespace std;
class MySql
{
public:
	int bytesToInt(byte* bytes, int size = 4)

	{

		int a = bytes[0] & 0xFF;

		a |= ((bytes[1] << 8) & 0xFF00);

		a |= ((bytes[2] << 16) & 0xFF0000);

		a |= ((bytes[3] << 24) & 0xFF000000);

		return a;

	}
	MySql(char *host, char *user, char *pwd, char *table, int port)
	{
		pCon = mysql_init(NULL);
		pCon_img = mysql_init(NULL);
		pCon_ziduan = mysql_init(NULL);
		datas = " "; error = " "; cord_num = 0;
		if (mysql_real_connect(pCon, host, user, pwd, table, port, NULL, 0)&& mysql_real_connect(pCon_img, host, user, pwd, table, port, NULL, 0))
		{	
			mysql_real_connect(pCon_ziduan, host, user, pwd, table, port, NULL, 0);
			//设置编码
			encode = "SET NAMES 'gb2312'";
			mysql_query(pCon, encode);
			mysql_query(pCon_img, encode);
			mysql_query(pCon_ziduan, encode);

			mysql_query(pCon, "select * from telemetry_message");
			mysql_query(pCon_img, "select * from telemetry_image");
			mysql_query(pCon_ziduan, "select COLUMN_NAME from information_schema.COLUMNS   where table_name = 'telemetry_message' and table_schema = 'equipment'");

			result_msg = mysql_store_result(pCon);
			result_img = mysql_store_result(pCon_img);
			result_zd = mysql_store_result(pCon_ziduan);
		}
		else
		{
			image_name = "连接数据库失败";
			error = "连接数据库失败！";
		}
	}
	~MySql() {};
	bool read_data_save_img(int data_row = 38)
	{
		bool rd = true;

		//获取字段名
		for (int i = 0; i < CORD; i++)
		{
			row_zd = mysql_fetch_row(result_zd);
			ziduan[i] = row_zd[0];
		}

		while (row = mysql_fetch_row(result_msg))
		{
			row_img = mysql_fetch_row(result_img);
			datas_ += "RS01440105001";
			datas_ += row[4];

			for (int i = 0; i < data_row; i++)
				try
			{
				if (row[i] == NULL)
				{
					datas += ziduan[i]; datas += ",";
					datas += ",";
					datas += ";";
				}
				else
				{
					datas += ziduan[i];
					datas += ",";
					datas += (char *)row[i];
					datas += ",";
					datas += ";";
				}

			}
			catch (exception)
			{
				rd = false;
				datas += ",";
			}
			//bit 类型数据
			for (int l = 0; l < 3; l++)
			{
				datas += ziduan[38 + l];
				datas += ",";
				d = (byte *)row[38 + l];
				da = bytesToInt(d);
				if (da != 1)
					datas += "0";
				else
					datas += "1";
				datas += ",";
				datas += ";";
			}
			datas += ziduan[41];
			datas += ",";
			datas += (char*)row[41];
			datas += ",";
			datas += ";";
			ss_ <<hex << int(datas.length());
			ss_ >> xor_value;
			switch (xor_value.length())
			{
				case 1:datas_ += "000"; break;
				case 2:datas_ += "00"; break;
				case 3:datas_ += "0"; break;
				default: break;

			}
			datas_ += xor_value;
			datas_ += "@@@";//固定分隔符
			datas_ += datas;
			datas_ += "tek";//@7固定分割符

			ss << hex << int(_xor(datas_));
			ss >> xor_value;
			if (xor_value.length() < 2)
				xor_value = "0" + xor_value;
			datas_ += xor_value;
			datas_ += "####";//结束符（4）
			datas_ += "\n";
			//xor值
			xor[cord_num] = _xor(datas);
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
		memset(trans, 0, MAX_SIZE);
		memcpy(trans, datas.c_str(), strlen(datas.c_str()));

		//操作单字节
		//for (int j = 0; j<strlen(trans) - 1; j++)
		//	cout << "\n:size:" << trans[j] << "\n";

		mysql_free_result(result_img);
		mysql_free_result(result_msg);
		mysql_free_result(result_zd);
		mysql_close(pCon_ziduan);
		mysql_close(pCon_img);
		mysql_close(pCon);
		return rd;
	}
	std::string char2hex(std::string const &s)
	{
		std::string ret;
		for (unsigned i = 0; i != s.size(); ++i)
		{
			char hex[5];
			sprintf(hex, "%#.2x ", (unsigned char)s[i]);
			ret += hex;
		}
		return ret;
	}

	int char2int(char input)
	{
		return input>96 ? (input - 87) : (input - 48);
	}

	int _xor(string ss) {

		string ret;
		ret = char2hex(ss);
		//ret = char2hex("A");
		std::cout << ret << std::endl;
		int fi_result = 0, x = 0;
		for (int i = 0; i < ss.length(); i++)
		{
			string s = ret.substr(x, 4);
			int result = char2int(s[2]) * 16 + char2int(s[3]);
			fi_result = fi_result^result;
			cout << fi_result << endl;
			x += 5;
		}
		return fi_result;
	}
public:
	string datas;
	string datas_;
	string error;
	char buf[4096];
	uint32_t *destIDs, *temp;
	unsigned int destNum = 16000;
	string image_name;
	int cord_num;
	string name[CORD_SIZE];
private:
	string xor_value;
	stringstream ss,ss_;
	byte *d;
	int da;
	char trans[4096];
	MFCFTPClient ftp;
	char *encode;
	char *ziduan[CORD];
	int xor[CORD];
	MYSQL_RES *result_img;
	MYSQL_RES *result_msg;
	MYSQL_RES *result_zd;
	MYSQL *pCon;
	MYSQL *pCon_img;
	MYSQL *pCon_ziduan;
	MYSQL_ROW row;
	MYSQL_ROW row_img;
	MYSQL_ROW row_zd;
	MYSQL_RES *result;
};