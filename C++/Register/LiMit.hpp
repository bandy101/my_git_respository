#pragma once
#include <windows.h>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// ��ȡBeauty.exe����·��
void getExePath(char *path, int size)
{
	char szBuf[1025] = { 0 };
	GetModuleFileName(NULL, (LPWSTR &)szBuf, sizeof(szBuf));
	char *p = strrchr(szBuf, '\\');
	*p = '\0';
	strncpy(path, szBuf, size - 1);
	path[size - 1] = '\0';
}

// ˽��ת���㷨�����ܹ�����
void privateConvert(char *pStr)
{
	int len = strlen(pStr);
	int i = 0;
	for (i = 0; i < len; i++)
	{
		pStr[i] = pStr[i] * pStr[i] % 128; // ��զдզд
		if ('\0' == pStr[i])
		{
			pStr[i] = 1;
		}
	}
}
