
// FTPMFCDlg.h : ͷ�ļ�
//

#pragma once
#include "afxwin.h"
<<<<<<< HEAD


=======
#include "MFCFTPClient.hpp"
#include "../FTP/FTPClient.h"
#include "opencv2/opencv.hpp"
#include "CvvImage.h"
>>>>>>> f2d1bff8386d248d0e43dde78561647827744fe8
// CFTPMFCDlg �Ի���
class CFTPMFCDlg : public CDialogEx
{
// ����
public:
	CFTPMFCDlg(CWnd* pParent = NULL);	// ��׼���캯��

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_FTPMFC_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV ֧��


// ʵ��
protected:
	HICON m_hIcon;

	// ���ɵ���Ϣӳ�亯��
	virtual BOOL OnInitDialog();
<<<<<<< HEAD
=======
	void ShowMat(cv::Mat image, int IDC);
>>>>>>> f2d1bff8386d248d0e43dde78561647827744fe8
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
<<<<<<< HEAD
	afx_msg void OnBnClickedButton2();
	CString IP_addr;
	CString E_Port;
	CEdit m_record;
};
=======
	CEdit m_record;
	MFCFTPClient ftp;
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
	bool islogin = false;
	afx_msg void OnBnClickedMulstor();
	afx_msg void OnStnClickedPicture();
	CStatic m_img;
};

>>>>>>> f2d1bff8386d248d0e43dde78561647827744fe8
