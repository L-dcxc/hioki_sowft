
// SampleDlg.h : ヘッダー ファイル
//

#pragma once
#include "afxwin.h"


// CSampleDlg ダイアログ
class CSampleDlg : public CDialogEx
{
// コンストラクション
public:
	CSampleDlg(CWnd* pParent = NULL);	// 標準コンストラクター

// ダイアログ データ
	enum { IDD = IDD_SAMPLE_DIALOG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV サポート


// 実装
protected:
	HICON m_hIcon;

	// 生成された、メッセージ割り当て関数
	virtual BOOL OnInitDialog();
	virtual void OnOK();
	afx_msg void OnClose();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedButton1();
	afx_msg void OnBnClickedButton2();
	afx_msg void OnBnClickedButton3();
	afx_msg void OnBnClickedButton4();
	CButton m_Button1;
	CButton m_Button2;
	CButton m_Button3;
	CEdit m_Edit1;
	CEdit m_Edit2;
	CEdit m_Edit3;
	CEdit m_Edit4;
	CEdit m_Edit5;
	CString m_strEdit1;
	DWORD m_dwEdit2;
	CString m_strEdit3;
	CString m_strEdit4;
	DWORD m_dwEdit5;
	DWORD m_ReceiveTimeout;										//受信タイムアウト時間(ms)
	HANDLE m_SerialPort;										//シリアルポートのハンドル
	CString m_ReceiveData;										//受信データ
	char m_TransferBuffer[65536];								//転送バッファ
	char m_ReceiveBuffer[65536];								//受信バッファ
	BOOL OpenInterface(CString PortName, DWORD BaudRate, DWORD Timeout);
	BOOL CloseInterface();
	BOOL SendMsg(CString SendData);
	BOOL ReceiveMsg();
	BOOL SendQueryMsg(CString SendData);
	CString GetLastErrorMessage(DWORD MessageId);
};
