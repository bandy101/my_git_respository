#pragma once  
//#include "Resources/DISK.hpp"
#include "register.h"
#pragma once
#include <QMessageBox>
#include "LiMit.hpp"
#define _WIN32_DCOM

#include <iostream>
#include <comdef.h>
#include <Wbemidl.h>
//#include "../DataSearch/datasearch.cpp"
//#include "../DataSearch/datasearch.cpp"

# pragma comment(lib, "wbemuuid.lib")
using namespace std;

string get_disk_number()
{
	HRESULT hres;
	char * serilize;
	// Step 1: --------------------------------------------------
	// Initialize COM. ------------------------------------------

	hres = CoInitializeEx(0, COINIT_APARTMENTTHREADED);
	if (FAILED(hres))
	{
		cout << "Failed to initialize COM library. Error code = 0x"
			<< hex << hres << endl;
		return "error";                  // Program has failed.
	}

	// Step 2: --------------------------------------------------
	// Set general COM security levels --------------------------
	// Note: If you are using Windows 2000, you need to specify -
	// the default authentication credentials for a user by using
	// a SOLE_AUTHENTICATION_LIST structure in the pAuthList ----
	// parameter of CoInitializeSecurity ------------------------

	hres = CoInitializeSecurity(
		NULL,
		-1,                          // COM authentication
		NULL,                        // Authentication services
		NULL,                        // Reserved
		RPC_C_AUTHN_LEVEL_DEFAULT,   // Default authentication
		RPC_C_IMP_LEVEL_IMPERSONATE, // Default Impersonation  
		NULL,                        // Authentication info
		EOAC_NONE,                   // Additional capabilities
		NULL                         // Reserved
	);

	if (FAILED(hres))
	{
		cout << "Failed to initialize security. Error code = 0x"
			<< hex << hres << endl;
		CoUninitialize();
		return "error";                    // Program has failed.
	}

	// Step 3: ---------------------------------------------------
	// Obtain the initial locator to WMI -------------------------

	IWbemLocator *pLoc = NULL;

	hres = CoCreateInstance(
		CLSID_WbemLocator,
		0,
		CLSCTX_INPROC_SERVER,
		IID_IWbemLocator, (LPVOID *)&pLoc);

	if (FAILED(hres))
	{
		cout << "Failed to create IWbemLocator object."
			<< " Err code = 0x"
			<< hex << hres << endl;
		CoUninitialize();
		return "error";                 // Program has failed.
	}

	// Step 4: -----------------------------------------------------
	// Connect to WMI through the IWbemLocator::ConnectServer method

	IWbemServices *pSvc = NULL;

	// Connect to the root\cimv2 namespace with
	// the current user and obtain pointer pSvc
	// to make IWbemServices calls.
	hres = pLoc->ConnectServer(
		_bstr_t(L"ROOT\\CIMV2"), // Object path of WMI namespace 
		NULL,                    // User name. NULL = current user
		NULL,                    // User password. NULL = current
		0,                       // Locale. NULL indicates current
		NULL,                    // Security flags.
		0,                       // Authority (e.g. Kerberos)
		0,                       // Context object
		&pSvc                    // pointer to IWbemServices proxy
	);

	if (FAILED(hres))
	{
		cout << "Could not connect. Error code = 0x"
			<< hex << hres << endl;
		pLoc->Release();
		CoUninitialize();
		return "error";                // Program has failed.
	}

	cout << "Connected to ROOT\\CIMV2 WMI namespace" << endl;

	// Step 5: --------------------------------------------------
	// Set security levels on the proxy -------------------------

	hres = CoSetProxyBlanket(
		pSvc,                        // Indicates the proxy to set
		RPC_C_AUTHN_WINNT,           // RPC_C_AUTHN_xxx
		RPC_C_AUTHZ_NONE,            // RPC_C_AUTHZ_xxx
		NULL,                        // Server principal name
		RPC_C_AUTHN_LEVEL_CALL,      // RPC_C_AUTHN_LEVEL_xxx
		RPC_C_IMP_LEVEL_IMPERSONATE, // RPC_C_IMP_LEVEL_xxx
		NULL,                        // client identity
		EOAC_NONE                    // proxy capabilities
	);
	if (FAILED(hres))
	{
		cout << "Could not set proxy blanket. Error code = 0x"
			<< hex << hres << endl;
		pSvc->Release();
		pLoc->Release();
		CoUninitialize();
		return "error";               // Program has failed.
	}

	// Step 6: --------------------------------------------------
	// Use the IWbemServices pointer to make requests of WMI ----

	// For example, get the name of the operating system
	IEnumWbemClassObject* pEnumerator = NULL;
	hres = pSvc->ExecQuery(
		bstr_t("WQL"),
		bstr_t("SELECT * FROM Win32_PhysicalMedia"),
		WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY,
		NULL,
		&pEnumerator);

	if (FAILED(hres))
	{
		cout << "Query for physical media failed."
			<< " Error code = 0x"
			<< hex << hres << endl;
		pSvc->Release();
		pLoc->Release();
		CoUninitialize();
		return "error";               // Program has failed.
	}

	// Step 7: -------------------------------------------------
	// Get the data from the query in step 6 -------------------

	IWbemClassObject *pclsObj;
	ULONG uReturn = 0;
	DWORD x = 0;
	while (pEnumerator)
	{
		HRESULT hr = pEnumerator->Next(WBEM_INFINITE, 1,
			&pclsObj, &uReturn);

		if (0 == uReturn)
		{
			break;
		}

		VARIANT vtProp;

		// Get the value of the Name property
		hr = pclsObj->Get(L"SerialNumber", 0, &vtProp, 0, 0);

		wcout << "Serial Number  " << x << ":" << vtProp.bstrVal << endl;
		serilize = _com_util::ConvertBSTRToString(vtProp.bstrVal);
		x += 1;
		VariantClear(&vtProp);
		cout << "x:" << x << endl;
		break;
	}

	// Cleanup
	// ========

	pSvc->Release();
	pLoc->Release();
	pEnumerator->Release();
	pclsObj->Release();
	CoUninitialize();
	//getchar();
	return serilize;   // Program successfully completed.
}

Register::Register(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	init();

}

Register::~Register()
{

}

void Register::ClickButton()
{	
	//--开始判断Lisence--//

	//获取授权码
	Award = ui.awd_code->text();
	if (Is_limit(Award))
	{	//授权
		QMessageBox::about(this, QString::fromLocal8Bit("提示"), QString::fromLocal8Bit("<b>授权成功</b>"));
		//w=new DataSearch(this);  ////将类指针实例化

		//w->show();
	}
	else
	{	//授权码错误
		QMessageBox::about(this, QString::fromLocal8Bit("提示"), QString::fromLocal8Bit("<font color=""green"" >注册码</font><br><font color=""red"" ><b>&nbsp;错误</b></font>"));
		//this->hide();
		//DataS *ks = new DataS(this);
		//ks->show();
		//this->deleteLater();
		data_ui = TRUE;
		//delete &ui;
		//K.setupUi(this);

	}
	//---------------#---------------//
	
}

//授权
bool Register::Is_limit(QString str)
{
	if (str.toStdString() == disk_id)
		return TRUE;
	else
	{
		return FALSE;
	}
}
void Register::init()
{
	//--标志--//
	flag = TRUE;       //保留
	is_limit = FALSE; //授权码是否合格
	data_ui = FALSE; //另外一个窗口是否授权打开
	//
	string str = get_disk_number();
	disk_id = str.substr(0, str.length() - 1); //disk_id
	Lisence = QString::fromStdString(disk_id);
	ui.reg_code->setText(Lisence);

	privateConvert(const_cast<char*>(disk_id.c_str()));
	//ui.awd_code->setText(QString::fromStdString(disk_id));   //show_award_code
	ui.awd_code->setFocus();

	//is_limit = Is_limit();
	connect(ui.active, SIGNAL(clicked()), this, SLOT(ClickButton()));
}

