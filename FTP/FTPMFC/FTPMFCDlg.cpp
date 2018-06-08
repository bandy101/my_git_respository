
// FTPMFCDlg.cpp : 实现文件
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


// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
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


// CFTPMFCDlg 对话框
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


// CFTPMFCDlg 消息处理程序

BOOL CFTPMFCDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
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

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO: 在此添加额外的初始化代码
	m_record.SetWindowTextW(_T("请登陆！\r\n"));
	info = "";
	MFCFTPClient ftp;
	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
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

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void  CFTPMFCDlg::ShowMat(cv::Mat image, int IDC)
{
	//CDC* pDC = GetDlgItem(IDC)->GetDC();           //根据ID获得窗口指针再获取与该窗口关联的上下文指针  
	//HDC hDC = pDC->GetSafeHdc();                    // 获取设备上下文句柄  
	CStatic* pStc = (CStatic*)GetDlgItem(IDC);
	CRect rect;
	pStc->GetClientRect(rect);
	CDC* pDC = pStc->GetDC();
	HDC hDC = pDC->GetSafeHdc();
	//GetDlgItem(IDC)->GetClientRect(rect);        //获取显示区  
	//GetDlgItem(IDC_PICTURE)->GetClientRect(rect);
	Mat im; 
	resize(image, im, Size(rect.Width(), rect.Height()));
	//imshow("s", im);
	//cvResize(&(image.operator IplImage()), &(cimage.operator IplImage()), CV_INTER_LINEAR);
	IplImage imgTmp = im;
	IplImage *img = cvCloneImage(&imgTmp);
	//IplImage *src = cvLoadImage("09.png", 1);
	CvvImage iimg;                              //创建一个CvvImage对象  
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
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR CFTPMFCDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void CFTPMFCDlg::OnBnClickedLogin()
{

	// TODO: 在此添加控件通知处理程序代码s
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
				info = "连接失败请重新连接！请确认IP或PORT\r\n";
				m_recodeinfo = info;
				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount()); //输入显示在当前编辑框
				m_recodeinfo = "请重新输入IP_PORT！\r\n";
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
					m_recodeinfo += "登陆成功！放心操作\r\n";
					GetDlgItem(IDC_LOGIN)->SetWindowText(LPCTSTR(CString("Out")));
					islogin = true;
				}
				else
				{
					m_recodeinfo += ero;
					m_recodeinfo += "请检查用户名和密码！\r\n";
					ftp.error = "";
				}

				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount());//使编辑框内容处于焦点
			}
		}//islogin
		else
		{
			islogin = false;
			GetDlgItem(IDC_LOGIN)->SetWindowText(LPCTSTR(CString("Login")));
			m_recodeinfo = "请登陆！\r\n";
			UpdateData(false);
		}
	}//try
	catch(exception)
	{
		m_recodeinfo = "请确认输入无误！\r\n";
		UpdateData(false);
		m_recodeinfo = "";
	}
}

void CFTPMFCDlg::OnBnClickedStor()
{
	// TODO: 在此添加控件通知处理程序代码
	if (islogin) {
		ftp.error = "";
		BOOL isOpen = TRUE;     //是否打开(否则为保存)  
		CString defaultDir = L"E:\\";   //默认打开的文件路径  
		CString fileName = L"";         //默认打开的文件名  
		CString filter = L"文件 (*.txt; *.png; *.jpg;*.jpeg)|*.txt;*.png;*.jpg;*.jpeg||";   //文件过虑的类型  
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
				m_recodeinfo += "上传失败!\r\n";
				m_recodeinfo += error; m_recodeinfo + "\r\n";
				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount());
			}
			else
			{															
				
				cv::Mat frame = cv::imread(filePath_);
				ShowMat(frame, IDC_PICTURE);

				m_recodeinfo += "上传成功：\r\n";
				m_recodeinfo += filePath;
				m_recodeinfo += "\r\n";
				UpdateData(false);
				m_record.LineScroll(m_record.GetLineCount());
				
			}
		}
	}
	else {
		m_recodeinfo = "请先登陆！";
		UpdateData(false);
		m_recodeinfo = "";
	}
}


//void CFTPMFCDlg::OnBnClickedMulstor()
//{
//	// TODO: 在此添加控件通知处理程序代码
//}


void CFTPMFCDlg::OnBnClickedMulstor()
{
	// TODO: 在此添加控件通知处理程序代码
	if (islogin)
	{
		m_recodeinfo += "尙无该功能\r\n";

	}
	else
	{
		m_recodeinfo += "请先登陆！\r\n";
	}
	UpdateData(false);
	m_record.LineScroll(m_record.GetLineCount());
}


void CFTPMFCDlg::OnStnClickedPicture()
{
	// TODO: 在此添加控件通知处理程序代码
	//m_img.LOad
}


void CFTPMFCDlg::OnBnClickedButton1()
{
	// TODO: 在此添加控件通知处理程序代码
	char *user = "root";         //username
	char *pswd = "IkaZ3qSviy64";         //password
	char *host = "192.168.20.16";    //or"127.0.0.1"
	char *table = "equipment";        //database
	unsigned int port = 3369;           //server port  
	sql = new MySql(host, user, pswd, table, port);
	m_recodeinfo += "数据库连接成功！\r\n";
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
	// TODO: 在此添加控件通知处理程序代码
	ftp.error = " ";
	char *in_path = "test\\\\";
	ftp.changedir(in_path);
	CString x(ftp.error.c_str());
	m_recodeinfo += x;
	UpdateData(false); 
}
