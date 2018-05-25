
// FTPMFCDlg.h : 头文件
//

#pragma once
#include "afxwin.h"
#include "MFCFTPClient.hpp"
#include "../FTP/FTPClient.h"

// CFTPMFCDlg 对话框
class CFTPMFCDlg : public CDialogEx
{
// 构造
public:
	CFTPMFCDlg(CWnd* pParent = NULL);	// 标准构造函数

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_FTPMFC_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CEdit m_record;
	FTPClient ftp;
	afx_msg void OnBnClickedLogin();
	CString m_ipaddr;
	CString m_port;
	CString info;
	CString m_recodeinfo;
	string FTPIP;
	afx_msg void OnBnClickedStor();
//	afx_msg void OnBnClickedMulstor();
	CString m_user;
	CString m_pwd;
};
