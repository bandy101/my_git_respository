#include
bool CPUID::GetSerialNumber(SerialNumber& serial)
{
	Executecpuid(1); // 执行cpuid，参数为 eax = 1
	bool isSupport = m_edx & (1 << 18); // edx是否为1代表CPU是否存在序列号
	if (false == isSupport) // 不支持，返回false
	{
		return false;
	}
	memcpy(&serial.nibble[4], &m_eax, 4); // eax为最高位的两个WORD

	Executecpuid(3); // 执行cpuid，参数为 eax = 3
	memcpy(&serial.nibble[0], &m_ecx, 8); // ecx 和 edx为低位的4个WORD

	return true;
}