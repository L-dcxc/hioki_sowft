//*******************************************************************************
//このプログラムは、計測器に接続してコマンドの送受信を行います。
//コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
//応答があるコマンド（?が含まれるコマンド）の場合は、エディットボックスに応答が表示されます。
//
//ナショナルインスツルメンツ(株)が公開しているGPIBのサンプルコードを参考にしています。
//サンプルコードのni4882.h および ni4882.objをプロジェクトに追加しています。
//
//動作確認環境：Microsoft Visual Studio 2010
//				Version 10.0.40219.1 SP1Rel
//				Microsoft .NET Framework
//				Version 4.0.30319 SP1Rel
//				Microsoft Visual C++ 2010
//				NI-488.2 Version 17.0
//*******************************************************************************

// SampleDlg.cpp : 実装ファイル
//

#include "stdafx.h"
#include "Sample.h"
#include "SampleDlg.h"
#include "afxdialogex.h"
#include <locale.h>
#include <mmsystem.h>

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
	, m_nEdit1(0)
	, m_nEdit2(0)
	, m_strEdit3(_T(""))
	, m_strEdit4(_T(""))
	, m_dwEdit5(0)
	, m_ReceiveTimeout(0)
	, m_GpibDevice(0)
	, m_ReceiveData(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

CSampleDlg::~CSampleDlg()
{
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
	DDX_Text(pDX, IDC_EDIT1, m_nEdit1);
	DDX_Text(pDX, IDC_EDIT2, m_nEdit2);
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
	m_nEdit1 = 0;
	m_nEdit2 = 1;
	m_strEdit3 = "*IDN?";
	m_strEdit4 = "";
	m_dwEdit5 = 1;
	UpdateData(FALSE);

	//ボタンとエディットボックスの有効/無効の処理
	m_Button2.EnableWindow(FALSE);
	m_Button3.EnableWindow(FALSE);
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
	if (OpenInterface(m_nEdit1, m_nEdit2, m_dwEdit5) != TRUE) {
		return;
	}

	//ボタンとエディットボックスの有効/無効の処理
	m_Button1.EnableWindow(FALSE);
	m_Button2.EnableWindow(TRUE);
	m_Button3.EnableWindow(TRUE);
	m_Edit1.EnableWindow(FALSE);
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
	m_Edit1.EnableWindow(TRUE);
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
BOOL CSampleDlg::OpenInterface(int BoardID, int DeviceAddress, DWORD Timeout)
{
	CString ErrorMessage;

	m_ReceiveTimeout = Timeout * 1000;													//受信タイムアウト時間の保管

	m_GpibDevice = ibdev(BoardID, DeviceAddress, 0, T10s, 1, 0);						//GPIBデバイスの初期化
	if ((Ibsta() & ERR) != 0) {
		ErrorMessage = GetNIErrorMessage();
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	ibclr(m_GpibDevice);																//GPIBデバイスのクリア
	if ((Ibsta() & ERR) != 0) {
		ErrorMessage = GetNIErrorMessage();
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	return TRUE;
}

//(2)切断
BOOL CSampleDlg::CloseInterface()
{
	CString ErrorMessage;

	ibonl(m_GpibDevice, 0);																//GPIBデバイスをオフラインにする
	if ((Ibsta() & ERR) != 0) {
		ErrorMessage = GetNIErrorMessage();
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	return TRUE;
}

//(3)コマンド送信
BOOL CSampleDlg::SendMsg(CString SendData)
{
	size_t Length;
	CString ErrorMessage;

#ifdef _UNICODE
	wcstombs_s(&Length, m_TransferBuffer, sizeof(m_TransferBuffer), SendData, _TRUNCATE);	//ワイド文字列をマルチバイト文字列に変換
	Length = strlen(m_TransferBuffer);
#else
	_tcscpy_s(m_TransferBuffer, sizeof(m_TransferBuffer), SendData);
	Length = _tcslen(m_TransferBuffer);
#endif
	ibwrt(m_GpibDevice, m_TransferBuffer, Length);										//送信データを書き込み
	if ((Ibsta() & ERR) != 0) {
		ErrorMessage = GetNIErrorMessage();
		MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
		return FALSE;
	}

	return TRUE;
}

//(4)応答受信
BOOL CSampleDlg::ReceiveMsg()
{
	DWORD StartTime;
	CString ErrorMessage;
	BOOL Result = FALSE;

	m_ReceiveData = _T("");																//受信データをクリア
	StartTime = timeGetTime();
	//ターミネータ「LF」を受信するまでループ
	for (;;) {																			//応答受信まで待つ
		ibrd(m_GpibDevice, m_TransferBuffer, sizeof(m_TransferBuffer) - 1);				//受信バッファに読み込み
		if ((Ibsta() & ERR) != 0) {
			//エラー有り
			if ((Ibsta() & TIMO) == 0) {
				//タイムアウト以外のエラー
				m_ReceiveData = _T("Error");
				ErrorMessage = GetNIErrorMessage();
				MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
				Result = FALSE;
				break;
			}
			if (Ibcnt() != 0) {
				m_TransferBuffer[Ibcnt()] = '\0';
				CString strText(m_TransferBuffer, Ibcnt());
				strText.Replace(_T("\r"), _T(""));										//受信データ内の「CR」を削除
				int Index = strText.Find(_T("\n"));
				if (Index >= 0) {														//ターミネータ「LF」を受信したら終了
					m_ReceiveData = m_ReceiveData + strText.Mid(0, Index);				//「LF」の手前までの受信データを保存
					Result = TRUE;
					break;
				}
				else {
					m_ReceiveData = m_ReceiveData + strText;							//受信データを保存
				}
			}
		}
		else {
			//エラー無し
			if (Ibcnt() != 0) {
				m_TransferBuffer[Ibcnt()] = '\0';
				CString strText(m_TransferBuffer, Ibcnt());
				strText.Replace(_T("\r"), _T(""));										//受信データ内の「CR」を削除
				int Index = strText.Find(_T("\n"));
				if (Index >= 0) {														//ターミネータ「LF」を受信したら終了
					m_ReceiveData = m_ReceiveData + strText.Mid(0, Index);				//「LF」の手前までの受信データを保存
					Result = TRUE;
					break;
				}
				else {
					m_ReceiveData = m_ReceiveData + strText;							//受信データを保存
				}
			}
		}
		 //タイムアウト処理
		if (timeGetTime() > StartTime + m_ReceiveTimeout) {								//受信タイムアウト時間経ってもCR+LFが受信できなければタイムアウト
			m_ReceiveData = _T("Timeout");
			ErrorMessage = GetLastErrorMessage(ERROR_TIMEOUT);
			MessageBox(ErrorMessage, AfxGetAppName(), MB_ICONERROR | MB_OK);
			Result = FALSE;
			break;
		}
	}

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

//エラーメッセージ取得
CString CSampleDlg::GetNIErrorMessage()
{
	CString strMessage;
	const static TCHAR *pErrorMnemonic[] = {
		_T("EDVR"),	_T("ECIC"),	_T("ENOL"),	_T("EADR"),	_T("EARG"),
		_T("ESAC"),	_T("EABO"),	_T("ENEB"),	_T("EDMA"),	_T(""),
		_T("EOIP"),	_T("ECAP"),	_T("EFSO"),	_T(""),		_T("EBUS"),
		_T("ESTB"),	_T("ESRQ"),	_T(""),		_T(""),		_T(""),
		_T("ETAB"),	_T("ELCK"),	_T("EARM"),	_T("EHDL"),	_T(""),
		_T(""),		_T("EWIP"),	_T("ERST"),	_T("EPWR")
	};

	strMessage.Format(_T("ibsta = 0x%04x, iberr = %d, %s"), Ibsta(), Iberr(), pErrorMnemonic[Iberr()]);

	return strMessage;
}

//エラーメッセージ取得
CString CSampleDlg::GetLastErrorMessage(DWORD MessageId)
{
	PVOID pBuffer = NULL;
	CString ErrorMessage;

	if (FormatMessage(
		FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_MAX_WIDTH_MASK,
		NULL, MessageId, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), reinterpret_cast<PTSTR>(&pBuffer), 0, NULL) == 0 || pBuffer == NULL) {
		return ErrorMessage;
	}
	ErrorMessage = static_cast<PTSTR>(pBuffer);
	LocalFree(pBuffer);

	return ErrorMessage;
}
