#include <iostream>
#include<afxcommandmanager.h>
#include<memory>
#include "DISK.h"
using namespace std;
char* reverse(char* s)
{	
	register char t,	//��ʱ��������ߵ���Ч��
	 *p = s,
	 *q = (s + (strlen(s) - 1)); //���һλ�ַ�

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
	char buffer[128]; //���建����
	FILE* pipe = _popen(cmd, "r"); //�򿪹ܵ�����ִ������
	if (!pipe)
		return 0; //����0��ʾ����ʧ��
	while (!feof(pipe)) {
		if (fgets(buffer, 128, pipe)) { //���ܵ������result��
			strcat(result, buffer);
		}
	}
}


vector<string> split(const string &s, const string &seperator) {
	vector<string> result;
	typedef string::size_type string_size;
	string_size i = 0;

	while (i != s.size()) {
		//�ҵ��ַ������׸������ڷָ�������ĸ��
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

		//�ҵ���һ���ָ������������ָ���֮����ַ���ȡ����
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

	char result[1024 * 4] = ""; //�����Ž�����ַ�������
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
