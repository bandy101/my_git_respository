#include
bool CPUID::GetSerialNumber(SerialNumber& serial)
{
	Executecpuid(1); // ִ��cpuid������Ϊ eax = 1
	bool isSupport = m_edx & (1 << 18); // edx�Ƿ�Ϊ1����CPU�Ƿ�������к�
	if (false == isSupport) // ��֧�֣�����false
	{
		return false;
	}
	memcpy(&serial.nibble[4], &m_eax, 4); // eaxΪ���λ������WORD

	Executecpuid(3); // ִ��cpuid������Ϊ eax = 3
	memcpy(&serial.nibble[0], &m_ecx, 8); // ecx �� edxΪ��λ��4��WORD

	return true;
}