#include <iostream>
#include <stdio.h>
#include <sstream>
#include <typeinfo>
#pragma comment(lib, "ws2_32.lib")
typedef unsigned char BYTE;
using namespace std;
long long string_to_bit(const string& str)//transfer hex-string to bit  
{

	long long result = strtoll(str.c_str(), NULL, 2);//第三个参数base为合法字符范围，base=2,为0、1，base=16，合法字符则为0-F，开头的0x自动忽略  
	return result;
}
string string_to_hex(const string& str) //transfer string to hex-string  
{
	string result = "0x";
	string tmp;
	stringstream ss;
	for (int i = 0; i<str.size(); i++)
	{
		ss << hex << int(str[i]) << endl;
		ss >> tmp;
		result += tmp;
	}
	return result;
}
static int str_to_hex(char *string,  char *cbuf, int len)
{
	BYTE high, low;
	int idx, ii = 0;
	for (idx = 0; idx<len; idx += 2)
	{
		high = string[idx];
		low = string[idx + 1];

		if (high >= '0' && high <= '9')
			high = high - '0';
		else if (high >= 'A' && high <= 'F')
			high = high - 'A' + 10;
		else if (high >= 'a' && high <= 'f')
			high = high - 'a' + 10;
		else
			return -1;

		if (low >= '0' && low <= '9')
			low = low - '0';
		else if (low >= 'A' && low <= 'F')
			low = low - 'A' + 10;
		else if (low >= 'a' && low <= 'f')
			low = low - 'a' + 10;
		else
			return -1;

		cbuf[ii++] = high << 4 | low;
	}
	return 0;
}

void outc(char c)
{
	unsigned char k = 0x80;
	for (int i = 0; i<8; i++, k >>= 1) {
		if (c & k) {
			printf("1");
		}
		else {
			printf("0");
		}
	}
	printf(" ");
}

//int main()
//{
//	printf("---------\n");
//	cout << string_to_hex("A");
//	cout<<string_to_bit(string_to_hex("A"));
//	cout << (int)(string_to_hex("A"))^10;
//	char *x = "A";
//	char buf[4096];
//	memset(buf, 0,4096);
//	str_to_hex(x, buf, 1000);
//	cout <<"buf:"<< buf;
//	//outc('A');
//	printf("\n");
//	outc('升');
//	getchar();
//	return 0;
//}

#include <iostream>
#include <string>
#include <cstdio>
#include <sstream>
using namespace std;

//ASCII码中将字符转换成对应的十进制数 
int char2int(char input)
{
	return input>64 ? (input - 55) : (input - 48);
}
//ASCII码中将十进制数转换成对应的字符 
int int2char(char input)
{
	return input>9 ? (input + 55) : (input + 48);
}
//将十六进制字符串HexStr1和HexStr2异或得到HexStr
void hexstrxor(char * HexStr1, char * HexStr2, char * HexStr)
{
	int i, iHexStr1Len, iHexStr2Len, iHexStrLenLow, iHexStrLenGap;
	//转换成大写并求长度, strupr是非标准的C函数，在Linux下不支持，所以需要
	//自己实现或者使用glib中的g_string_ascii_up () 
	strupr(HexStr1);
	strupr(HexStr2);
	iHexStr1Len = strlen(HexStr1);
	iHexStr2Len = strlen(HexStr2);
	//获取最小的长度 
	iHexStrLenLow = iHexStr1Len<iHexStr2Len ? iHexStr1Len : iHexStr2Len;
	//获取长度差值 iHexStrLenGap = abs( iHexStr1Len-iHexStr2Len ); 
	//两个十六进制的字符串进行异或 
	for (i = 0; i<iHexStrLenLow; i++)
	{
		*(HexStr + i) = char2int(HexStr1[i]) ^ char2int(HexStr2[i]);
		*(HexStr + i) = int2char(*(HexStr + i));
	}
	if (iHexStr1Len>iHexStr2Len)
		memcpy(HexStr + i, HexStr1 + i, iHexStrLenGap);
	else if (iHexStr1Len<iHexStr2Len) memcpy(HexStr + i, HexStr2 + i, iHexStrLenGap);
	*(HexStr + iHexStrLenLow + iHexStrLenGap) = 0x00;
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

std::string hex2char(std::string const &s)
{
	std::string ret;
	std::istringstream iss(s);
	for (std::string buf; std::getline(iss, buf, ' ');)
	{
		unsigned int value;
		sscanf(buf.c_str(), "%x", &value);
		ret += ((char)value);
	}
	return ret;
}

int main()
{
	std::string ret;
	ret = char2hex("A代码源真飞升");
	std::cout << ret << std::endl;
	std::cout << hex2char(ret) << std::endl;
	getchar();
	return 0;
}

int main(int argc, char * argv[]) 
{ //两个十六进制的字符串以及异或的结果result
	char HexStr1[] = "F1A37CD826BE0A38"; 
	char HexStr2[] = "4FBC926A2EED4F0A"; 
	char result[17] = {0}; 
	//调用异或方法 
	hexstrxor( HexStr1, HexStr2, result ); 
	//打印异或结果 
	printf( "\nresult=[%s]\n", result ); return 0; 
}


