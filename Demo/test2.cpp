/*
测试程序
作者：    闲人
*/

#include <iostream>
#include "cpuid.h"
using namespace std;

void PrintCacheInfo(CacheInfo& L)
{
	cout<<"Cache Level:\t\t"<<L.level<<endl;
	cout<<"Cache Size:\t\t"<<L.size<<"-KB"<<endl;
	cout<<"Cache Way:\t\t"<<L.way<<"-way"<<endl;
	cout<<"Cache Line Size:\t"<<L.linesize<<"-byte line size"<<endl<<endl;
}

void PrintSerial(SerialNumber& serial)
{
	cout<<"Serial Number:\t";
	for (int i = 0; i < 6; i++)
	{
		cout<<hex<<serial.nibble[5-i];
		if (5 != i)
		{
			cout<<"-";
		}
	}
}

/*int main()
{
	CPUID *cpuid = CPUID::Instance();

	cout<<"CPU VID:\t"<<cpuid->GetVID()<<endl;
	cout<<"CPU Brand:\t"<<cpuid->GetBrand()<<endl;
	cout<<"Hyper-Threading support:\t"<<boolalpha<<cpuid->IsHyperThreading()<<endl;
	cout<<"Enable Intel Speedstep:\t\t"<<boolalpha<<cpuid->IsEST()<<endl;
	cout<<"Enable MMX:\t\t\t"<<boolalpha<<cpuid->IsMMX()<<endl<<endl;

	CacheInfo L[3];
	int cachenum = cpuid->GetCacheInfo(L[0], L[1], L[2]);
	while (cachenum > 0)
	{
		PrintCacheInfo(L[--cachenum]);
	}

	SerialNumber serial;
	if (cpuid->GetSerialNumber(serial))
	{
		PrintSerial(serial);
	}
	else
	{
		cout<<"Serial Number is not support."<<endl;
	}

	system("pause");
	return 0;
}*/