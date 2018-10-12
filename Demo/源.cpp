#include <windows.h>
#include <winioctl.h>
#include <stdio.h>
#include <iostream>
#include <cstringt.h>
#include <string>
#include <atlstr.h>
using namespace std;
BOOL GetDriveGeometry(DISK_GEOMETRY *pdg)
{
	HANDLE hDevice;               // handle to the drive to be examined
	BOOL bResult;                 // results flag
	DWORD junk;                   // discard results

	TCHAR *filePath = "C:/Windows/System32/drivers/disk.sys";

	hDevice = CreateFile("filePath",  // drive to open
		0,                // no access to the drive
		FILE_SHARE_READ | // share mode
		FILE_SHARE_WRITE,
		NULL,             // default security attributes
		OPEN_EXISTING,    // disposition
		0,                // file attributes
		NULL);            // do not copy file attributes
	//SCSI\DISK&VEN_NVME&PROD_SAMSUNG_MZVLW128\5 & 2DEFCFD & 0 & 000000

	if (hDevice == INVALID_HANDLE_VALUE) // cannot open the drive
	{
		DWORD erM = 0;
		LPVOID lpMsgBuf;
		CString theErr;
		erM = GetLastError();
		FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
			NULL,
			erM,
			MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
		(LPTSTR)&lpMsgBuf,
			0, NULL);
		theErr.Format("%s", lpMsgBuf);//theErrÏÔÊ¾Îª¡°¾Ü¾ø·ÃÎÊ¡±
		cout << hDevice;
		return (FALSE);
	}

	bResult = DeviceIoControl(hDevice,     // device to be queried
		IOCTL_DISK_GET_DRIVE_GEOMETRY,     // operation to perform
		NULL, 0,               // no input buffer
		pdg, sizeof(*pdg),     // output buffer
		&junk,                 // # bytes returned
		(LPOVERLAPPED)NULL);  // synchronous I/O

	CloseHandle(hDevice);

	return (bResult);
}

int main(int argc, char *argv[])
{
	DISK_GEOMETRY pdg;            // disk drive geometry structure
	BOOL bResult;                 // generic results flag
	ULONGLONG DiskSize;           // size of the drive, in bytes

	bResult = GetDriveGeometry(&pdg);

	if (bResult)
	{
		printf("Cylinders = %I64d/n", pdg.Cylinders);
		printf("Tracks per cylinder = %ld/n", (ULONG)pdg.TracksPerCylinder);
		printf("Sectors per track = %ld/n", (ULONG)pdg.SectorsPerTrack);
		printf("Bytes per sector = %ld/n", (ULONG)pdg.BytesPerSector);

		DiskSize = pdg.Cylinders.QuadPart * (ULONG)pdg.TracksPerCylinder *
			(ULONG)pdg.SectorsPerTrack * (ULONG)pdg.BytesPerSector;
		printf("Disk size = %I64d (Bytes) = %I64d (Mb)/n", DiskSize,
			DiskSize / (1024 * 1024));
	}
	else
	{
		printf("GetDriveGeometry failed. Error %ld./n", GetLastError());
	}
	getchar();
	return ((int)bResult);

}