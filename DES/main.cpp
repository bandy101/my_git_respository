#include <iostream>
#include <stdio.h>
#include <fstream>
#include <bitset>
#include <io.h>

using namespace std;
long size_s;

bitset<64> key;                // 64位密钥
bitset<48> subKey[16];         // 存放16轮子密钥


int IP[] = { 58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17, 9,  1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7 };

// 结尾置换表
int IP_1[] = { 40, 8, 48, 16, 56, 24, 64, 32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41,  9, 49, 17, 57, 25 };

/*------------------下面是生成密钥所用表-----------------*/

// 密钥置换表，将64位密钥变成56位
int PC_1[] = { 57, 49, 41, 33, 25, 17, 9,
1, 58, 50, 42, 34, 26, 18,
10,  2, 59, 51, 43, 35, 27,
19, 11,  3, 60, 52, 44, 36,
63, 55, 47, 39, 31, 23, 15,
7, 62, 54, 46, 38, 30, 22,
14,  6, 61, 53, 45, 37, 29,
21, 13,  5, 28, 20, 12,  4 };

// 压缩置换，将56位密钥压缩成48位子密钥
int PC_2[] = { 14, 17, 11, 24,  1,  5,
3, 28, 15,  6, 21, 10,
23, 19, 12,  4, 26,  8,
16,  7, 27, 20, 13,  2,
41, 52, 31, 37, 47, 55,
30, 40, 51, 45, 33, 48,
44, 49, 39, 56, 34, 53,
46, 42, 50, 36, 29, 32 };

// 每轮左移的位数
int shiftBits[] = { 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1 };

/*------------------下面是密码函数 f 所用表-----------------*/

// 扩展置换表，将 32位 扩展至 48位
int E[] = { 32,  1,  2,  3,  4,  5,
4,  5,  6,  7,  8,  9,
8,  9, 10, 11, 12, 13,
12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21,
20, 21, 22, 23, 24, 25,
24, 25, 26, 27, 28, 29,
28, 29, 30, 31, 32,  1 };

// S盒，每个S盒是4x16的置换表，6位 -> 4位
int S_BOX[8][4][16] = {
	{
		{ 14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7 },
		{ 0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8 },
		{ 4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0 },
		{ 15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13 }
	},
	{
		{ 15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10 },
		{ 3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5 },
		{ 0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15 },
		{ 13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9 }
	},
	{
		{ 10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8 },
		{ 13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1 },
		{ 13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7 },
		{ 1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12 }
	},
	{
		{ 7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15 },
		{ 13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9 },
		{ 10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4 },
		{ 3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14 }
	},
	{
		{ 2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9 },
		{ 14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6 },
		{ 4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14 },
		{ 11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3 }
	},
	{
		{ 12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11 },
		{ 10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8 },
		{ 9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6 },
		{ 4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13 }
	},
	{
		{ 4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1 },
		{ 13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6 },
		{ 1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2 },
		{ 6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12 }
	},
	{
		{ 13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7 },
		{ 1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2 },
		{ 7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8 },
		{ 2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11 }
	}
};

// P置换，32位 -> 32位
int P[] = { 16,  7, 20, 21,
29, 12, 28, 17,
1, 15, 23, 26,
5, 18, 31, 10,
2,  8, 24, 14,
32, 27,  3,  9,
19, 13, 30,  6,
22, 11,  4, 25 };

/**********************************************************************/
/*                                                                    */
/*                            下面是DES算法实现                         */
/*                                                                    */
/**********************************************************************/

/**
*  密码函数f，接收32位数据和48位子密钥，产生一个32位的输出
*/
bitset<32> f(bitset<32> R, bitset<48> k)
{
	bitset<48> expandR;
	// 第一步：扩展置换，32 -> 48
	for (int i = 0; i<48; ++i)
		expandR[47 - i] = R[32 - E[i]];
	// 第二步：异或
	expandR = expandR ^ k;
	// 第三步：查找S_BOX置换表
	bitset<32> output;
	int x = 0;
	for (int i = 0; i<48; i = i + 6)
	{
		int row = expandR[47 - i] * 2 + expandR[47 - i - 5];
		int col = expandR[47 - i - 1] * 8 + expandR[47 - i - 2] * 4 + expandR[47 - i - 3] * 2 + expandR[47 - i - 4];
		int num = S_BOX[i / 6][row][col];
		bitset<4> binary(num);
		output[31 - x] = binary[3];
		output[31 - x - 1] = binary[2];
		output[31 - x - 2] = binary[1];
		output[31 - x - 3] = binary[0];
		x += 4;
	}
	// 第四步：P-置换，32 -> 32
	bitset<32> tmp = output;
	for (int i = 0; i<32; ++i)
		output[31 - i] = tmp[32 - P[i]];
	return output;
}

/**
*  对56位密钥的前后部分进行左移
*/
bitset<28> leftShift(bitset<28> k, int shift)
{
	bitset<28> tmp = k;
	for (int i = 27; i >= 0; --i)
	{
		if (i - shift<0)
			k[i] = tmp[i - shift + 28];
		else
			k[i] = tmp[i - shift];
	}
	return k;
}

/**
*  生成16个48位的子密钥
*/
void generateKeys()
{
	bitset<56> realKey;
	bitset<28> left;
	bitset<28> right;
	bitset<48> compressKey;
	// 去掉奇偶标记位，将64位密钥变成56位
	for (int i = 0; i<56; ++i)
		realKey[55 - i] = key[64 - PC_1[i]];
	// 生成子密钥，保存在 subKeys[16] 中
	for (int round = 0; round<16; ++round)
	{
		// 前28位与后28位
		for (int i = 28; i<56; ++i)
			left[i - 28] = realKey[i];
		for (int i = 0; i<28; ++i)
			right[i] = realKey[i];
		// 左移
		left = leftShift(left, shiftBits[round]);
		right = leftShift(right, shiftBits[round]);
		// 压缩置换，由56位得到48位子密钥
		for (int i = 28; i<56; ++i)
			realKey[i] = left[i - 28];
		for (int i = 0; i<28; ++i)
			realKey[i] = right[i];
		for (int i = 0; i<48; ++i)
			compressKey[47 - i] = realKey[56 - PC_2[i]];
		subKey[round] = compressKey;
	}
}

/**
*  工具函数：将char字符数组转为二进制
*/
bitset<64> charToBitset(const char s[8])
{
	bitset<64> bits;
	for (int i = 0; i<8; ++i)
		for (int j = 0; j<8; ++j)
			bits[i * 8 + j] = ((s[i] >> j) & 1);
	return bits;
}

/**
*  DES加密
*/
bitset<64> encrypt(bitset<64>& plain)
{
	bitset<64> cipher;
	bitset<64> currentBits;
	bitset<32> left;
	bitset<32> right;
	bitset<32> newLeft;
	// 第一步：初始置换IP
	for (int i = 0; i<64; ++i)
		currentBits[63 - i] = plain[64 - IP[i]];
	// 第二步：获取 Li 和 Ri
	for (int i = 32; i<64; ++i)
		left[i - 32] = currentBits[i];
	for (int i = 0; i<32; ++i)
		right[i] = currentBits[i];
	// 第三步：共16轮迭代
	for (int round = 0; round<16; ++round)
	{
		newLeft = right;
		right = left ^ f(right, subKey[round]);
		left = newLeft;
	}
	// 第四步：合并L16和R16，注意合并为 R16L16
	for (int i = 0; i<32; ++i)
		cipher[i] = left[i];
	for (int i = 32; i<64; ++i)
		cipher[i] = right[i - 32];
	// 第五步：结尾置换IP-1
	currentBits = cipher;
	for (int i = 0; i<64; ++i)
		cipher[63 - i] = currentBits[64 - IP_1[i]];
	// 返回密文
	return cipher;
}

/**
*  DES解密
*/
bitset<64> decrypt(bitset<64>& cipher)
{
	bitset<64> plain;
	bitset<64> currentBits;
	bitset<32> left;
	bitset<32> right;
	bitset<32> newLeft;
	// 第一步：初始置换IP
	for (int i = 0; i<64; ++i)
		currentBits[63 - i] = cipher[64 - IP[i]];
	// 第二步：获取 Li 和 Ri
	for (int i = 32; i<64; ++i)
		left[i - 32] = currentBits[i];
	for (int i = 0; i<32; ++i)
		right[i] = currentBits[i];
	// 第三步：共16轮迭代（子密钥逆序应用）
	for (int round = 0; round<16; ++round)
	{
		newLeft = right;
		right = left ^ f(right, subKey[15 - round]);
		left = newLeft;
	}
	// 第四步：合并L16和R16，注意合并为 R16L16
	for (int i = 0; i<32; ++i)
		plain[i] = left[i];
	for (int i = 32; i<64; ++i)
		plain[i] = right[i - 32];
	// 第五步：结尾置换IP-1
	currentBits = plain;
	for (int i = 0; i<64; ++i)
		plain[63 - i] = currentBits[64 - IP_1[i]];
	// 返回明文
	return plain;
}
//合并
void Merge()
{
	char name[20];
	string str1 = "F:/数据/1.jpg";
	string str2 = "F:/数据/2.jpg";
	string strBlock = "F:/数据/BLOCK.dat";
	FILE* f1,*f2,*f3;
	fopen_s(&f1,str1.c_str(), "rb+");
	fopen_s(&f2,str2.c_str(), "rb+");
	fopen_s(&f3,strBlock.c_str(), "rb+");

	// 获取文件的长度
	int iLen1 = _filelength(_fileno(f1));
	int iLen2 = _filelength(_fileno(f2));

	char *buf1 = new char[iLen1];
	memset(buf1, 0x0, iLen1);
	char *buf2 = new char[iLen2];
	memset(buf2, 0x0, iLen2);

	// 获取文件内容
	fread(buf1, iLen1, 1, f1);
	fread(buf2, iLen2, 1, f2);
	fclose(f1);
	fclose(f2);


	// 在文件头记录合并文件的个数
	int iCount = 2;
	fseek(f3, 0, SEEK_SET);
	fwrite(&iCount, sizeof(int), 1, f3);

	// 写入第一个文件
	memset(name, 0x0, 20);
	strcpy_s(name, str1.c_str());
	fwrite(name, 20, 1, f3);
	fwrite(&iLen1, sizeof(int), 1, f3);
	fwrite(buf1, iLen1, 1, f3);

	// 写入第二个文件
	memset(name, 0x0, 20);
	strcpy_s(name, str2.c_str());
	fwrite(name, 20, 1, f3);
	fwrite(&iLen2, sizeof(int), 1, f3);
	fwrite(buf2, iLen2, 1, f3);

	fclose(f3);



	//删除申请的内存     
	delete[] buf1;
	delete[] buf2;
}

//分离
void Split(string strBlock)
{
	char name[20];
	FILE* f3;
	//string strBlock = "F:/数据/BLOCK.dat";
	 fopen_s(&f3,strBlock.c_str(), "rb+");

	// 获取文件数量
	int iCount = 0;
	fseek(f3, 0, SEEK_SET);
	fread(&iCount, sizeof(int), 1, f3);

	for (int i = 0; i<iCount; i++)
	{
		memset(name, 0x0, sizeof(name));
		fread(&name, 20, 1, f3);
		// 输出名称
		cout << name << endl;
		int iLen = 0;
		// 读取文件长度
		//iLen = _filelength(_fileno(f3));
		fread(&iLen, sizeof(int), 1, f3);
		char *buff = new char[iLen];
		// 读取文件内容
		fread(buff, iLen, 1, f3);
		char fileLen[10];
		sprintf_s(fileLen, "%d", iLen);

		// 以文件长度做名称
		string s = fileLen;
		string strName = "";
		strName += s;
		strName += string(".txt");

		// 新建一个文件
		FILE* file;
		fopen_s(&file,strName.c_str(), "wb+");
		fwrite(buff, iLen, 1, file);
		fclose(file);
	}

	fclose(f3);
}

void Split_s(string filename)
{
	fstream pf, pf1;
	string tempstr = "";
	char number[10];

	pf.open(filename.c_str(), ios::in | ios::binary);

	if (!pf)
	{
		cout << "err" << endl;
	}

	int temp = pf.tellg();
	pf.seekg(0, ios_base::end);
	long flen = pf.tellg();  //获取加密文件byte长度
	pf.seekg(temp);

	cout << "file size is: " << flen << " byte" << endl;

	static const long size = flen/3;   // 这里限定了文件的分割大小；
	size_s = size;
	cout << "size" << size;
	int n = 3;
	//int n = flen / size + 1;  // 文件要分为多少分，为了保证最有一个文件最小，故+1；  ###----固定三份
	//cout << "number of file is: " << n << endl;


	//////////////////////////////////////////////////////////////////////////
	// 先分n-1的文件
	char *databuf = new char[size];

	for (int i = 0; i < n - 1; i++)
	{
		_itoa_s(i, number, 10);
		tempstr = filename + number;
		pf1.open(tempstr.c_str(), ios::out | ios::binary);

		pf.read(databuf, size * sizeof(char));
		pf1.write(databuf, size * sizeof(char));
		pf1.close();
		cout << "file :"<<&tempstr << endl;
	}

	delete[] databuf;

	//////////////////////////////////////////////////////////////////////////
	// 分最后一个文件，由于最后一个文件大小不定，所以单独列出来
	long endlen = flen - size * (n - 1);

	_itoa_s(n - 1, number, 10);
	tempstr = filename + number;
	pf1.open(tempstr.c_str(), ios::out | ios::binary);

	databuf = new char[endlen];

	pf.read(databuf, endlen * sizeof(char));
	pf1.write(databuf, endlen * sizeof(char));
	pf1.close();
	cout << "file :" << &tempstr << endl;

	pf.close();
	delete[] databuf;
}

void Merge_s(string filename)
{
	fstream pf, pf1;
	pf.open(filename.c_str(), ios::in | ios::binary);
	string tempstr = "";
	char number[10];
	tempstr = filename + "A";    //这里为了在同一个目录里面看效果，避免文件同名

	int temp = pf.tellg();
	pf.seekg(0, ios_base::end);
	long flen = pf.tellg();  //获取加密文件byte长度
	pf.seekg(temp);
	static const long size = flen / 3;   // 这里限定了文件的分割大小；
	char *databuf = new char[size];
	pf.close();
	pf1.open(tempstr.c_str(), ios::out | ios::binary);
	int n = 3;
	databuf = new char[size];

	for (int i = 0; i < n - 1; i++)
	{
		_itoa_s(i, number, 10);
		tempstr = filename + number+"encryptto_decrypt";
		pf.open(tempstr.c_str(), ios::in | ios::binary);

		pf.read(databuf, size * sizeof(char));
		pf1.write(databuf, size * sizeof(char));

		pf.close();

		cout << "file :" << &tempstr << endl;
	}

	delete[] databuf;

	//////////////////////////////////////////////////////////////////////////
	// 合并最后一个文件，由于文件大小不清楚，其实没有个文件都可以采用这样的方式
	// 合并，都可以避免文件的大小不一的问题，这里假设了出了最后一个文件，其他文
	// 件都是相同大小的

	_itoa_s(n - 1, number, 10);
	tempstr = filename + number+"encryptto_decrypt";
	pf.open(tempstr.c_str(), ios::in | ios::binary);

	temp = pf.tellg();
	pf.seekg(0, ios_base::end);
	flen = pf.tellg();
	pf.seekg(temp);

	databuf = new char[flen];

	pf.read(databuf, flen * sizeof(char));
	pf1.write(databuf, flen * sizeof(char));

	pf.close();
	pf1.close();
	delete[] databuf;
	cout << "file :" << &tempstr << endl;


	tempstr = filename + "A";
	cout << "file :" << &tempstr << endl;
}

void en_des(string file, string k)
{
	//获取长度
	fstream pf;
	pf.open(file.c_str(), ios::in | ios::binary);
	pf.seekg(0, ios_base::end);
	long total_flen = pf.tellg();
	pf.close();
	char buffer[8];
	key = charToBitset(k.c_str());
	// 生成16个子密钥
	generateKeys();
	// 密文写入 a.txt
	//bitset<64> cipher = encrypt(plain);
	fstream file1, files;
	files.open(file, ios::binary | ios::in);
	file1.open(file + "encrypt", ios::binary | ios::out);
	long flen;

	while (!files.eof())
	{
		memset(&buffer, 0, sizeof(buffer));
		flen = total_flen - file1.tellg();
		if (flen == 0) break;
		if (flen < 8)
		files.read(buffer, flen+1);
		else
		{
			files.read(buffer, 8);

		}
		//cout << flen << endl;
		bitset<64> plain = charToBitset(buffer);
		bitset<64> cipher = encrypt(plain);
		//if (flen < 8&& flen!=0)
		//{
		//	file1.write((char*)&cipher, flen);
		//	break;
		//}
		//else
		//{
		//	file1.write((char*)&cipher, sizeof(cipher));
		//}
		file1.write((char*)&cipher, sizeof(cipher));
	}
	file1.close();
	files.close();
}

void de_des(string file, string k)
{

	//长度
	fstream pf;
	pf.open(file.c_str(), ios::in | ios::binary);
	pf.seekg(0, ios_base::end);
	long total_flen = pf.tellg();

	fstream file1, files;
	bitset<64> temp;
	key = charToBitset(k.c_str());
	generateKeys();
	file1.open(file, ios::binary | ios::in);
	files.open(file + "to_decrypt", ios::binary | ios::out);
	long flen;
	while (!file1.eof()) {
		memset(&temp, 0, sizeof(temp));
		flen = total_flen - file1.tellg();
		if (flen == 0) break;
		if (flen < 8)
			file1.read((char*)&temp, flen);
		else
		{
			file1.read((char*)&temp, sizeof(temp));
			//cout << sizeof(temp) << endl;
		}
		


		//if (temp != 0) {
		//
		//	bitset<64> temp_plain = decrypt(temp);
		//	files.write((char*)&temp_plain, sizeof(temp_plain));
		//}
		//if (flen < 8)
		//{
		//	bitset<64> temp_plain = decrypt(temp);
		//	files.write((char*)&temp_plain, flen);
		//}
		//else
		//{
		//	bitset<64> temp_plain = decrypt(temp);
		//	files.write((char*)&temp_plain, sizeof(temp_plain));
		//}
		bitset<64> temp_plain = decrypt(temp);
		files.write((char*)&temp_plain, sizeof(temp_plain));

	}
	file1.close();
	files.close();
}

void des_final(string files,string key1,string key2,string key3)
{
	Split_s(files);
	en_des(files+"0", key1);
	en_des(files+"1", key2);
	en_des(files+"2", key3);
	de_des(files + "0encrypt", key1);
	de_des(files + "1encrypt", key2);
	de_des(files + "2encrypt", key3);
	Merge_s(files);
}


int main()
{	
	string files = "test.txt";
	string key1, key2, key3,id;
	key1 = id+"12345678";
	key2 = id+"2345678";
	key3 = id+"45678910";
	des_final(files, key1, key2, key3);
	//Merge_s(files);
	//Split_s(files);
	//Merge_s(files);
	getchar();
	return 0;
}