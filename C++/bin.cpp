#include <iostream>
#include <stdio.h>
#include <bitset>
using namespace std;

void int_to_bin(int value,char *x,int index=0) {

	if (value / 2 <= 0)
		return;
	else
	{
		x[index] = value % 2;
		int_to_bin(value / 2, x, ++index);
	}
}

void bin_to_int(char *x, int *value,int e=0)
{
	if (e>=strlen(x)) return;
	*value = *value*2 + x[e] - '0';
	bin_to_int(x, value, ++e);
	/*
	char *k = "1000";
	bin_to_int(k, &value);##value =2*2*2 =8
	*/
}
int main()
{
	char*k = "1000";
	int value = 0;
	bin_to_int(k, &value);

	cout << "bin_to_int:" << value << endl;
	char* s = "中文数据";
	cout << "s:" << strlen(s) << endl;

	bitset<64> bits;
	for (int i = 0; i<8; ++i)
		for (int j = 0; j<8; ++j)
			bits[i * 8 + j] = ((s[i] >> j) & 1);

	char *z = new char[strlen(s)] ;
	cout << "z-len:" << strlen(z) << endl;
	memset(z, 0, strlen(z));
	char zz[9] = {0};
	bitset<8> b;
	for (int i = 0; i < 8; ++i) {
		value = 0;
		for (int j = 0; j < 8; ++j)
		{
			zz[7-j] = bits[i * 8 + j]+'0';
			b[j] = bits[i * 8 + j];
		}
		bin_to_int(zz, &value);
		z[i] = (char)value;
		long kkk = b.to_ulong();
	}
	cout << "z:" << z << endl;
	cout << "---" << 'a' - 'A'<< endl;
	char *str ="中文d的123456";
	cout << "str_size:" << sizeof(str)<<endl;
	size_t size = strlen(str);
	int *x=new int[size];
	for (int i = 0; i < size; i++)
	{
		int val = (int)str[i];
		x[i] = val;
		cout << (char)val;
	}
	cout << endl << "size_x:" << sizeof(x) << endl;
	for (int i = 0; i < size; i++)
	{
		cout << (char)x[i];
	}
	getchar();
	return 0;
}