#include <iostream>
#include<afxcommandmanager.h>
#include<memory>
#include "DISK.h"
using namespace std;
char* reverse(char* s)
{	
	register char t,	//临时变量，提高调用效率
	 *p = s,
	 *q = (s + (strlen(s) - 1)); //最后一位字符

	while (p < q)
	{
		cout << "p:" << p << "q:" << q << endl;
		t = *p; 
		*p++ = *q; 
		*q-- = t;
		//p++, q--;
	}
	return s;

}
#include <vector>
#include <iostream>
#include <intrin.h>
#include <string>
using namespace std;


int execmd(char* cmd, char* result) {
	char buffer[128]; //定义缓冲区
	FILE* pipe = _popen(cmd, "r"); //打开管道，并执行命令
	if (!pipe)
		return 0; //返回0表示运行失败
	while (!feof(pipe)) {
		if (fgets(buffer, 128, pipe)) { //将管道输出到result中
			strcat(result, buffer);
		}
	}
}


vector<string> split(const string &s, const string &seperator) {
	vector<string> result;
	typedef string::size_type string_size;
	string_size i = 0;

	while (i != s.size()) {
		//找到字符串中首个不等于分隔符的字母；
		int flag = 0;
		while (i != s.size() && flag == 0) {
			flag = 1;
			for (string_size x = 0; x < seperator.size(); ++x)
				if (s[i] == seperator[x]) {
					++i;
					flag = 0;
					break;
				}
		}

		//找到又一个分隔符，将两个分隔符之间的字符串取出；
		flag = 0;
		string_size j = i;
		while (j != s.size() && flag == 0) {
			for (string_size x = 0; x < seperator.size(); ++x)
				if (s[j] == seperator[x]) {
					flag = 1;
					break;
				}
			if (flag == 0)
				++j;
		}
		if (i != j) {
			result.push_back(s.substr(i, j - i));
			i = j;
		}
	}
	return result;
}

void main(void)
{
	/*
	char pCpuId[32] = "";
	get_cpuId(pCpuId);
	cout << pCpuId << endl;
	system("pause");

	return;*/

	char result[1024 * 4] = ""; //定义存放结果的字符串数组
	if (1 == execmd("wmic CPU get ProcessorID", result)) {
		string re = result;
		cout<<re.length()<<"----r"<<re.substr(40);
		//vector<string> v  = split(re, "\n");
		//cout << "start:"<<v.at(0);
	}
	//char * res = system("wmic CPU get ProcessorID");
	GetHardDiskNO();
	system("pause");
	getchar();
	
	return;
}
