
// FTPMFC.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// CFTPMFCApp: 
// �йش����ʵ�֣������ FTPMFC.cpp
//

class CFTPMFCApp : public CWinApp
{
public:
	CFTPMFCApp();

// ��д
public:
	virtual BOOL InitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};
<<<<<<< HEAD

=======
>>>>>>> f2d1bff8386d248d0e43dde78561647827744fe8
extern CFTPMFCApp theApp;