
// FTPMFCDlg.cpp : ʵ���ļ�
//

#include "stdafx.h"
#include "FTPMFC.h"
#include "FTPMFCDlg.h"
#include "afxdialogex.h"
#include "MFCFTPClient.hpp"
#include "../FTP/FTPClient.cpp"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// ����Ӧ�ó��򡰹��ڡ��˵���� CAboutDlg �Ի���

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV ֧��

// ʵ��
protected:
	DECLARE_MESSAGE_MAP()
};

//CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
//{
//}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CFTPMFCDlg �Ի���
string& trim(string &s)
{
	if (s.empty())
	{
		return s;
	}
	s.erase(0, s.find_first_not_of(" "));
	s.erase(s.find_last_not_of(" ") + 1);
	return s;
}

CFTPMFCDlg::CFTPMFCDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_FTPMFC_DIALOG, pParent)
	, m_ipaddr(_T(""))
	, m_port(_T(""))
	, m_recodeinfo(_T(""))
	, m_user(_T(""))
	, m_pwd(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CFTPMFCDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_RECORD, m_record);
	DDX_Text(pDX, IDC_IPADDR, m_ipaddr);
	DDX_Text(pDX, IDC_PORT, m_port);
	DDV_MaxChars(pDX, m_port, 4);
	DDX_Text(pDX, IDC_RECORD, m_recodeinfo);
	DDX_Text(pDX, IDC_USER, m_user);
	DDX_Text(pDX, IDC_PWD, m_pwd);
}

BEGIN_MESSAGE_MAP(CFTPMFCDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_LOGIN, &CFTPMFCDlg::OnBnClickedLogin)
	ON_BN_CLICKED(IDC_STOR, &CFTPMFCDlg::OnBnClickedStor)
END_MESSAGE_MAP()


// CFTPMFCDlg ��Ϣ�������

BOOL CFTPMFCDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// ��������...���˵�����ӵ�ϵͳ�˵��С�

	// IDM_ABOUTBOX ������ϵͳ���Χ�ڡ�
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// ���ô˶Ի����ͼ�ꡣ  ��Ӧ�ó��������ڲ��ǶԻ���ʱ����ܽ��Զ�
	//  ִ�д˲���
	SetIcon(m_hIcon, TRUE);			// ���ô�ͼ��
	SetIcon(m_hIcon, FALSE);		// ����Сͼ��

	// TODO: �ڴ���Ӷ���ĳ�ʼ������
	m_record.SetWindowTextW(_T("���½��\n"));
	info = "";
	MFCFTPClient ftp;
	return TRUE;  // ���ǽ��������õ��ؼ������򷵻� TRUE
}

void CFTPMFCDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		//CAboutDlg dlgAbout;
		//dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// �����Ի��������С����ť������Ҫ����Ĵ���
//  �����Ƹ�ͼ�ꡣ  ����ʹ���ĵ�/��ͼģ�͵� MFC Ӧ�ó���
//  �⽫�ɿ���Զ���ɡ�

void CFTPMFCDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // ���ڻ��Ƶ��豸������

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// ʹͼ���ڹ����������о���
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// ����ͼ��
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//���û��϶���С������ʱϵͳ���ô˺���ȡ�ù��
//��ʾ��
HCURSOR CFTPMFCDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void CFTPMFCDlg::OnBnClickedLogin()
{
	
	// TODO: �ڴ���ӿؼ�֪ͨ����������s
	UpdateData(true);
	//string FTPIP = (char *)m_ipaddr.GetBuffer(0);  
	FTPIP = (LPCSTR)(CStringA)(m_ipaddr);
	FTPIP = trim(FTPIP);
	string port_ = (LPCSTR)(CStringA)(m_port);
	port_ = trim(port_);
	//int PORT = atoi((char*)m_port.GetBuffer(0));
	string::size_type sz;
	int PORT=stoi(port_, &sz);
	 //= int(port_);
	//FTPIP = const_cast<char*>(FTPIP.c_str());
	if (!(ftp.FTPConnection(const_cast<char*>(FTPIP.c_str()),PORT)))
	{
		CString cs(FTPIP.c_str());
		//s.Format(_T("%s"), FTPIP.c_str());
		m_recodeinfo += cs;//string->CString;;;
		m_recodeinfo += ":";
		m_recodeinfo +=m_port;
		info = "  -!����ʧ�����������ӣ�";
		m_recodeinfo += info;
		UpdateData(false);
		m_recodeinfo = "���½��\n";
		//return;
	}
	else
	{
		m_recodeinfo += FTPIP.c_str();
		m_recodeinfo += m_port;
		string user = (LPCSTR)(CStringA)(m_user);
		string pwd = (LPCSTR)(CStringA)(m_pwd);
		user = trim(user);
		pwd = trim(pwd);
		bool user_ = ftp.useuser(const_cast<char*>(user.c_str()));
		bool pwd_ = ftp.usepass(const_cast<char*>(pwd.c_str()));
		CString ero(ftp.error.c_str());
		
		if (user_&&pwd_)
		{
			m_recodeinfo += ero;
			m_recodeinfo += "\n��½�ɹ������Ĳ���";
			
		}
		else
		{
			m_recodeinfo += ero;
			m_recodeinfo += "�����û��������룡";
			//UpdateData(false);
			//return;
		}
		UpdateData(false);
	}
}


void CFTPMFCDlg::OnBnClickedStor()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	BOOL isOpen = TRUE;     //�Ƿ��(����Ϊ����)  
	CString defaultDir = L"E:\\";   //Ĭ�ϴ򿪵��ļ�·��  
	CString fileName = L"";         //Ĭ�ϴ򿪵��ļ���  
	CString filter = L"�ļ� (*.txt; *.png; *.jpg;*.jpeg)|*.txt;*.png;*.jpg;*.jpeg||";   //�ļ����ǵ�����  
	CFileDialog openFileDlg(isOpen, NULL, fileName, OFN_HIDEREADONLY | OFN_READONLY, filter, NULL);
	openFileDlg.DoModal();
	CString filePath = openFileDlg.GetPathName();
	string filePath_ = (LPCSTR)(CStringA)(filePath);
	filePath_ = trim(filePath_);
	ftp.storfile(const_cast<char*>(FTPIP.c_str()), const_cast<char*>(filePath_.c_str()));
	CString error(ftp.error.c_str());
	m_recodeinfo += "�ϴ��ɹ���\n";
	m_recodeinfo += filePath;
	m_recodeinfo += error;
	m_recodeinfo += "�ϴ��ɹ���\n";
	UpdateData(false);
}


//void CFTPMFCDlg::OnBnClickedMulstor()
//{
//	// TODO: �ڴ���ӿؼ�֪ͨ����������
//}
