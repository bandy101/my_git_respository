
// FTPMFC.h : PROJECT_NAME 应用程序的主头文件
//

#pragma once

#ifndef __AFXWIN_H__
	#error "在包含此文件之前包含“stdafx.h”以生成 PCH 文件"
#endif

#include "resource.h"		// 主符号


// CFTPMFCApp: 
// 有关此类的实现，请参阅 FTPMFC.cpp
//

class CFTPMFCApp : public CWinApp
{
public:
	CFTPMFCApp();

// 重写
public:
	virtual BOOL InitInstance();

// 实现

	DECLARE_MESSAGE_MAP()
};
<<<<<<< HEAD

=======
>>>>>>> f2d1bff8386d248d0e43dde78561647827744fe8
extern CFTPMFCApp theApp;