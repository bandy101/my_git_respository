
// FTPMFCDlg.cpp : ʵ���ļ�
//

#include "stdafx.h"
#include "FTPMFC.h"
#include "FTPMFCDlg.h"
#include "afxdialogex.h"
#include "MFCFTPClient.hpp"
#include "../FTP/FTPClient.cpp"
#include <opencv2/opencv.hpp>
#include "opencv2/features2d/features2d.hpp"
#include "cv.h"
#include "highgui.h"
//#include <opencv2/opencv.hpp>
using namespace std;
using namespace cv;
//#include "Resource.h"s

#ifdef _DEBUG
#define new DEBUG_NEW
#define IDC_PICTURE                     1008
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
	DDX_Control(pDX, IDC_PICTURE, m_img);
}

BEGIN_MESSAGE_MAP(CFTPMFCDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_LOGIN, &CFTPMFCDlg::OnBnClickedLogin)
	ON_BN_CLICKED(IDC_STOR, &CFTPMFCDlg::OnBnClickedStor)
	ON_BN_CLICKED(IDC_MULSTOR, &CFTPMFCDlg::OnBnClickedMulstor)
	ON_STN_CLICKED(IDC_PICTURE, &CFTPMFCDlg::OnStnClickedPicture)
	ON_BN_CLICKED(IDC_BUTTON1, &CFTPMFCDlg::OnBnClickedButton1)
	ON_BN_CLICKED(IDC_BUTTON2, &CFTPMFCDlg::OnBnClickedButton2)
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
	m_record.SetWindowTextW(_T("���½��\r\n"));
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

void  CFTPMFCDlg::ShowMat(cv::Mat image, int IDC)
{
	//CDC* pDC = GetDlgItem(IDC)->GetDC();           //����ID��ô���ָ���ٻ�ȡ��ô��ڹ�����������ָ��  
	//HDC hDC = pDC->GetSafeHdc();                    // ��ȡ�豸�����ľ��  
	CStatic* pStc = (CStatic*)GetDlgItem(IDC);
	CRect rect;
	pStc->GetClientRect(rect);
	CDC* pDC = pStc->GetDC();
	HDC hDC = pDC->GetSafeHdc();
	//GetDlgItem(IDC)->GetClientRect(rect);        //��ȡ��ʾ��  
	//GetDlgItem(IDC_PICTURE)->GetClientRect(rect);
	Mat im; 
	resize(image, im, Size(rect.Width(), rect.Height()));
	//imshow("s", im);
	//cvResize(&(image.operator IplImage()), &(cimage.operator IplImage()), CV_INTER_LINEAR);
	IplImage imgTmp = im;
	IplImage *img = cvCloneImage(&imgTmp);
	//IplImage *src = cvLoadImage("09.png", 1);
	CvvImage iimg;                              //����һ��CvvImage����  
	iimg.CopyOf(img);
	iimg.DrawToHDC(hDC, &rect);
	cvReleaseImage(&img);
	ReleaseDC(pDC);
	iimg.Destroy();
}
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
	try {
		UpdateData(true);
		FTPIP = (LPCSTR)(CStringA)(m_ipaddr);
		FTPIP = trim(FTPIP);
		string port_ = (LPCSTR)(CStringA)(m_port);
		port_ = trim(port_);
		string::size_type sz;
		PORT = stoi(port_, &sz);
		if (!islogin) {
			if (!(ftp.FTPConnection(const_cast<char*>(FTPIP.c_str()), PORT)))
			{
				CString cs(FTPIP.c_str());
				//s.Format(_T("%s"), FTPIP.c_str());
				m_recodeinfo += cs;//string->CString;;;
				m_recodeinfo += ":";
				m_recodeinfo += m_port;
				info = "����ʧ�����������ӣ���ȷ��IP��PORT\r\n";
				m_recodeinfo = info;
				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount()); //������ʾ�ڵ�ǰ�༭��
				m_recodeinfo = "����������IP_PORT��\r\n";
				//return;
			}
			else
			{
				m_recodeinfo += FTPIP.c_str();
				m_recodeinfo += ":";
				m_recodeinfo += m_port;
				m_recodeinfo += "\r\n";
				user = (LPCSTR)(CStringA)(m_user);
				pwd = (LPCSTR)(CStringA)(m_pwd);
				user = trim(user);
				pwd = trim(pwd);
				bool user_ = ftp.useuser(const_cast<char*>(user.c_str()));
				bool pwd_ = ftp.usepass(const_cast<char*>(pwd.c_str()));
				CString ero(ftp.error.c_str());

				if (user_&&pwd_)
				{
					m_recodeinfo += ero;
					m_recodeinfo += "��½�ɹ������Ĳ���\r\n";
					GetDlgItem(IDC_LOGIN)->SetWindowText(LPCTSTR(CString("Out")));
					islogin = true;
				}
				else
				{
					m_recodeinfo += ero;
					m_recodeinfo += "�����û��������룡\r\n";
					ftp.error = "";
				}

				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount());//ʹ�༭�����ݴ��ڽ���
			}
		}//islogin
		else
		{
			islogin = false;
			GetDlgItem(IDC_LOGIN)->SetWindowText(LPCTSTR(CString("Login")));
			m_recodeinfo = "���½��\r\n";
			UpdateData(false);
		}
	}//try
	catch(exception)
	{
		m_recodeinfo = "��ȷ����������\r\n";
		UpdateData(false);
		m_recodeinfo = "";
	}
}

void CFTPMFCDlg::OnBnClickedStor()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	if (islogin) {
		ftp.error = "";
		BOOL isOpen = TRUE;     //�Ƿ��(����Ϊ����)  
		CString defaultDir = L"E:\\";   //Ĭ�ϴ򿪵��ļ�·��  
		CString fileName = L"";         //Ĭ�ϴ򿪵��ļ���  
		CString filter = L"�ļ� (*.txt; *.png; *.jpg;*.jpeg)|*.txt;*.png;*.jpg;*.jpeg||";   //�ļ����ǵ�����  
		CFileDialog openFileDlg(isOpen, NULL, fileName, OFN_HIDEREADONLY | OFN_READONLY, filter, NULL);
		openFileDlg.DoModal();
		CString filePath = openFileDlg.GetPathName();
		//string filePath = "09.png";
		if (filePath != "")
		{
			string filePath_ = (LPCSTR)(CStringA)(filePath);
			filePath_ = trim(filePath_);
			//string filePath = "09.png";
			char *in_path="tests\\0";
			if (!ftp.mkdirectory(in_path)) 
			{ 
				ftp.FTPConnection(const_cast<char*>(FTPIP.c_str()), PORT); 
				ftp.useuser(const_cast<char*>(user.c_str()));
				ftp.usepass(const_cast<char*>(pwd.c_str()));
				ftp.error = "";
			}
			

			ftp.storfile(const_cast<char*>(FTPIP.c_str()), const_cast<char*>(filePath_.c_str()),in_path);
			//ftp.storfile(const_cast<char*>(FTPIP.c_str()), const_cast<char*>(filePath.c_str()));
			CString error(ftp.error.c_str());
			if (error != "")
			{	
				m_recodeinfo += "�ϴ�ʧ��!\r\n";
				m_recodeinfo += error; m_recodeinfo + "\r\n";
				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount());
			}
			else
			{															
				
				cv::Mat frame = cv::imread(filePath_);
				ShowMat(frame, IDC_PICTURE);

				m_recodeinfo += "�ϴ��ɹ���\r\n";
				m_recodeinfo += filePath;
				m_recodeinfo += "\r\n";
				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount());
				
			}
		}
	}
	else {
		m_recodeinfo = "���ȵ�½��";
		UpdateData(false);
		m_recodeinfo = "";
	}
}


//void CFTPMFCDlg::OnBnClickedMulstor()
//{
//	// TODO: �ڴ���ӿؼ�֪ͨ����������
//}


void CFTPMFCDlg::OnBnClickedMulstor()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	if (islogin)
	{
		m_recodeinfo += "���޸ù���\r\n";

	}
	else
	{
		m_recodeinfo += "���ȵ�½��\r\n";
	}
	UpdateData(false);
	m_record.LineScroll(m_record.GetLineCount());
}


void CFTPMFCDlg::OnStnClickedPicture()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	//m_img.LOad
}


void CFTPMFCDlg::OnBnClickedButton1()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	char *user = "root";         //username
	char *pswd = "IkaZ3qSviy64";         //password
	char *host = "192.168.20.16";    //or"127.0.0.1"
	char *table = "equipment";        //database
	unsigned int port = 3369;           //server port  
	sql = new MySql(host, user, pswd, table, port);
	m_recodeinfo += "���ݿ����ӳɹ���\r\n";
	sql->read_data_save_img(42);
	string *img_path_name = sql->name;
	//CString name((*img_path_name).c_str());
	for (int i = 0; i < sql->cord_num; i++)
	{
		CString name((*img_path_name).c_str());
		m_recodeinfo += name;
		m_recodeinfo += "\r\n";
		img_path_name++;
	}
	
	//m_recodeinfo += sql->image_name.substr(9,sizeof(sql->image_name)).c_str();
	UpdateData(false);

}


void CFTPMFCDlg::OnBnClickedButton2()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	ftp.error = " ";
	char *in_path = "test\\\\";
	ftp.changedir(in_path);
	CString x(ftp.error.c_str());
	m_recodeinfo += x;
	UpdateData(false); 
}
