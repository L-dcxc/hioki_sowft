//*******************************************************************************
//このプログラムは、計測器に接続してコマンドの送受信を行います。
//コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
//応答があるコマンド（?が含まれるコマンド）の場合は、エディットボックスに応答が表示されます。
//
//(株)コンテックが公開しているGPIBのサンプルコードを参考にしています。
//サンプルコードのGpibac.h、SubFunc.cpp、SubFunc.hおよびApiGpib1.libをプロジェクトに追加しています。
//追加したSubFunc.cppにGpibInput関数を改造したGpibInputHioki関数を追加しています。
//
//動作確認環境：Microsoft Visual Studio 2010
//				Version 10.0.40219.1 SP1Rel
//				Microsoft .NET Framework
//				Version 4.0.30319 SP1Rel
//				Microsoft Visual C++ 2010
//				API-GPIB(98/PC) Ver5.80
//*******************************************************************************

// SampleDlg.cpp : 実装ファイル
//

#include "stdafx.h"
#include "Sample.h"
#include "SampleDlg.h"
#include "afxdialogex.h"
#include <locale.h>
#include "gpibac.h"
#include "SubFunc.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// アプリケーションのバージョン情報に使われる CAboutDlg ダイアログ

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// ダイアログ データ
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV サポート

// 実装
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()

//コンストラクタ
CSampleDlg::CSampleDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(CSampleDlg::IDD, pParent)
	, m_dwEdit1(0)
	, m_dwEdit2(0)
	, m_strEdit3(_T(""))
	, m_strEdit4(_T(""))
	, m_dwEdit5(0)
	, m_MyAddress(0)
	, m_DeviceAddress(0)
	, m_ReceiveTimeout(0)
	, m_ReceiveData(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CSampleDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_BUTTON1, m_Button1);
	DDX_Control(pDX, IDC_BUTTON2, m_Button2);
	DDX_Control(pDX, IDC_BUTTON3, m_Button3);
	DDX_Control(pDX, IDC_EDIT1, m_Edit1);
	DDX_Control(pDX, IDC_EDIT2, m_Edit2);
	DDX_Control(pDX, IDC_EDIT3, m_Edit3);
	DDX_Control(pDX, IDC_EDIT4, m_Edit4);
	DDX_Control(pDX, IDC_EDIT5, m_Edit5);
	DDX_Text(pDX, IDC_EDIT1, m_dwEdit1);
	DDX_Text(pDX, IDC_EDIT2, m_dwEdit2);
	DDX_Text(pDX, IDC_EDIT3, m_strEdit3);
	DDX_Text(pDX, IDC_EDIT4, m_strEdit4);
	DDX_Text(pDX, IDC_EDIT5, m_dwEdit5);
}

BEGIN_MESSAGE_MAP(CSampleDlg, CDialogEx)
	ON_WM_CLOSE()
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON1, &CSampleDlg::OnBnClickedButton1)
	ON_BN_CLICKED(IDC_BUTTON2, &CSampleDlg::OnBnClickedButton2)
	ON_BN_CLICKED(IDC_BUTTON3, &CSampleDlg::OnBnClickedButton3)
	ON_BN_CLICKED(IDC_BUTTON4, &CSampleDlg::OnBnClickedButton4)
END_MESSAGE_MAP()

//ダイアログが開かれたときの処理
BOOL CSampleDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// "バージョン情報..." メニューをシステム メニューに追加します。

	// IDM_ABOUTBOX は、システム コマンドの範囲内になければなりません。
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

	// このダイアログのアイコンを設定します。アプリケーションのメイン ウィンドウがダイアログでない場合、
	//  Framework は、この設定を自動的に行います。
	SetIcon(m_hIcon, TRUE);			// 大きいアイコンの設定
	SetIcon(m_hIcon, FALSE);		// 小さいアイコンの設定

	//メンバ変数の初期化
	m_ReceiveData = "";
	m_dwEdit1 = 0;
	m_dwEdit2 = 1;
	m_strEdit3 = "*IDN?";
	m_strEdit4 = "";
	m_dwEdit5 = 1;
	UpdateData(FALSE);

	//ボタンとエディットボックスの有効/無効の処理
	m_Button2.EnableWindow(FALSE);
	m_Button3.EnableWindow(FALSE);
	m_Edit1.EnableWindow(FALSE);
	m_Edit3.EnableWindow(FALSE);

	//ログエディットボックスを読み取り専用、最大文字数を無制限に設定
	m_Edit4.SetReadOnly(TRUE);
	m_Edit4.SetLimitText(0);

	return TRUE;  // フォーカスをコントロールに設定した場合を除き、TRUE を返します。
}

//エンターキーを押してもダイアログを閉じないようにする
void CSampleDlg::OnOK()
{
}

//ダイアログを閉じるときの処理
void CSampleDlg::OnClose()
{
	CDialogEx::OnClose();
}

void CSampleDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// ダイアログに最小化ボタンを追加する場合、アイコンを描画するための
//  下のコードが必要です。ドキュメント/ビュー モデルを使う MFC アプリケーションの場合、
//  これは、Framework によって自動的に設定されます。

void CSampleDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 描画のデバイス コンテキスト

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// クライアントの四角形領域内の中央
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// アイコンの描画
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

// ユーザーが最小化したウィンドウをドラッグしているときに表示するカーソルを取得するために、
//  システムがこの関数を呼び出します。
HCURSOR CSampleDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}

//「接続」ボタンを押したときの処理
void CSampleDlg::OnBnClickedButton1()
{
	UpdateData(TRUE);

	//接続
	if (OpenInterface(m_dwEdit2, m_dwEdit5) != TRUE) {
		return;
	}

	//マイアドレスを表示
	m_dwEdit1 = m_MyAddress;
	UpdateData(FALSE);

	//ボタンとエディットボックスの有効/無効の処理
	m_Button1.EnableWindow(FALSE);
	m_Button2.EnableWindow(TRUE);
	m_Button3.EnableWindow(TRUE);
	m_Edit2.EnableWindow(FALSE);
	m_Edit3.EnableWindow(TRUE);
	m_Edit5.EnableWindow(FALSE);
}

//「切断」ボタンを押したときの処理
void CSampleDlg::OnBnClickedButton2()
{
	//切断
	CloseInterface();

	//ボタンとエディットボックスの有効/無効の処理
	m_Button1.EnableWindow(TRUE);
	m_Button2.EnableWindow(FALSE);
	m_Button3.EnableWindow(FALSE);
	m_Edit2.EnableWindow(TRUE);
	m_Edit3.EnableWindow(FALSE);
	m_Edit5.EnableWindow(TRUE);
}

//「送受信」ボタンを押したときの処理
void CSampleDlg::OnBnClickedButton3()
{
	m_Edit3.EnableWindow(FALSE);

	UpdateData(TRUE);
	m_strEdit4 += _T("<< ") + m_strEdit3 + _T("\r\n");									//ログ出力
	UpdateData(FALSE);
	if (m_strEdit3.Find(_T("?")) == -1) {												//コマンドに?が含まれない場合は、コマンド送信のみ
		SendMsg(m_strEdit3);															//コマンド送信
	}
	else {																				//コマンドに?が含まれる場合は、コマンド送信と応答受信
		SendQueryMsg(m_strEdit3);														//コマンド送信と応答受信
		m_strEdit4 += _T(">> ") + m_ReceiveData + _T("\r\n");							//ログ出力
		UpdateData(FALSE);
	}

	m_Edit3.EnableWindow(TRUE);
}

//「クリア」ボタンを押したときの処理
void CSampleDlg::OnBnClickedButton4()
{
	//ログ出力エディットボックスの消去
	UpdateData(TRUE);
	m_strEdit4 = _T("");
	UpdateData(FALSE);
}

//(1)接続
BOOL CSampleDlg::OpenInterface(DWORD PrimaryAddress, DWORD Timeout)
{
	DWORD Mode;
	DWORD Eoi;
	DWORD Delim;
	CString ErrorMessage;
	DWORD Result;

	Result = static_cast<DWORD>(GpibInit(&ErrorMessage));								//GPIBの初期化
	if (Result != 0) {
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	Result = GpBoardsts(0x0a, &Mode);													//マスタ/スレーブモードの読み出し
	if (Result != 0) {
		CheckRet(CString(_T("GpBoardsts")), Result, &ErrorMessage);						//GpBoardstsの戻り値をチェック
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}
	if (Mode != 0) {
		MessageBox(_T("この機器はマスタではありません。"), AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	Result = GpBoardsts(0x08, &m_MyAddress);											//マイアドレスの取得
	if (Result != 0) {
		CheckRet(CString(_T("GpBoardsts")), Result, &ErrorMessage);						//GpBoardstsの戻り値をチェック
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	Eoi = 1;																			//0:使用しない / 1:使用する
	Delim = 3;																			//0:未使用 / 1:CR+LF / 2:CR / 3:LF
	Result = GpDelim(Delim, Eoi); 														//デリミタコード(EOI)送出の設定
	if (Result != 0) {
		CheckRet(CString(_T("GpDelim")), Result, &ErrorMessage);						//GpDelimの戻り値をチェック
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	m_ReceiveTimeout = Timeout * 1000;
	Result = GpTimeout(m_ReceiveTimeout);												//タイムアウト時間の設定
	if (Result != 0) {
		CheckRet(CString(_T("GpTimeout")), Result, &ErrorMessage); 						//GpTimeoutの戻り値をチェック
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	m_DeviceAddress = static_cast<long>(PrimaryAddress);

	return TRUE;
}

//(2)切断
BOOL CSampleDlg::CloseInterface()
{
	GpibExit();																			//GPIBの終了

	return TRUE;
}

//(3)コマンド送信
BOOL CSampleDlg::SendMsg(CString SendData)
{
	long Result;

	Result = GpibPrint(m_DeviceAddress, SendData);										//送信データを書き込み
	if (Result != 0) {
		return FALSE;
	}

	return TRUE;
}

//(4)応答受信
BOOL CSampleDlg::ReceiveMsg()
{
	CString Buffer;
	long Result;

	Result = GpibInputHioki(m_DeviceAddress, &Buffer);									//受信バッファに読み込み
	if (Result != 0) {
		m_ReceiveData = _T("Error");
		return FALSE;
	}
	m_ReceiveData = Buffer;																//受信データを保存

	return TRUE;
}

//(5)コマンド送受信
BOOL CSampleDlg::SendQueryMsg(CString SendData)
{
	BOOL Result;

	Result = SendMsg(SendData);															//コマンド送信
	if (Result == TRUE) {
		Result = ReceiveMsg();															//送信が成功したら応答を受信
	}

	return Result;
}
