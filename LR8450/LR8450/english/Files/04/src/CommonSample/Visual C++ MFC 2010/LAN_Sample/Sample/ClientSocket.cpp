#include "StdAfx.h"
#include "ClientSocket.h"
#include <mmsystem.h>

//コンストラクタ
CClientSocket::CClientSocket()
	: m_WsaData()
	, m_Address()
	, m_Socket()
{
}

//デストラクタ
CClientSocket::~CClientSocket()
{
}

//オープン
int CClientSocket::Connect(const char *pszIpAddress, unsigned int Port)
{
	unsigned long Argp = 1;
	char OptVal = 1;
	int RetVal;
	int ErrCode;

	//Winsock初期化
	RetVal = ::WSAStartup(MAKEWORD(2, 0), &m_WsaData);
	if (RetVal != 0){
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	//ソケットの生成
	m_Socket = ::socket(AF_INET, SOCK_STREAM, 0);
	if (m_Socket == INVALID_SOCKET) {
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	//アドレス変換
	m_Address.sin_family = AF_INET;
	m_Address.sin_port = htons(static_cast<unsigned short>(Port));
	m_Address.sin_addr.s_addr = ::inet_addr(pszIpAddress);

	//接続
	RetVal = ::connect(m_Socket, reinterpret_cast<sockaddr *>(&m_Address), sizeof(m_Address));
	if (RetVal != 0) {
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	//非ブロッキングに設定
	RetVal = ::ioctlsocket(m_Socket, FIONBIO, &Argp);
	if (RetVal != 0) {
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	//送信の遅延(Nagleアルゴリズム)を無効に設定
	RetVal = ::setsockopt(m_Socket, IPPROTO_TCP, TCP_NODELAY, &OptVal, sizeof(OptVal));
	if (RetVal != 0) {
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	return 0;
}

//クローズ
int CClientSocket::Disconnect()
{
	int RetVal;
	int ErrCode;

	//クローズ
	RetVal = ::closesocket(m_Socket);
	if (RetVal != 0) {
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	//Winsock終了
	RetVal = ::WSACleanup();
	if (RetVal != 0) {
		ErrCode = ::GetLastError();
		return ErrCode;
	}

	return 0;
}

//送信
int CClientSocket::Send(const char *pszBuffer)
{
	int Offset;
	int Remain;
	int RetVal;
	int ErrCode;

	//ソケットへ送信
	Offset = 0;
	Remain = static_cast<int>(::strlen(pszBuffer));
	while (Remain > 0) {
		RetVal = ::send(m_Socket, pszBuffer + Offset, Remain, 0);
		if (RetVal == SOCKET_ERROR) {
			ErrCode = ::GetLastError();
			return ErrCode;
		}
		Offset += RetVal;
		Remain -= RetVal;
	}

	return 0;
}

//受信
int CClientSocket::Receive(CString &strBuffer, unsigned long Timeout)
{
	DWORD StartTime;
	int RetVal;
	int ErrCode;

	//ソケットから受信
	strBuffer = _T("");
	StartTime = ::timeGetTime();
	while (1) {
		::memset(m_szBuffer, 0, sizeof(m_szBuffer));
		RetVal = ::recv(m_Socket, m_szBuffer, sizeof(m_szBuffer) - 1, 0);
		if (RetVal == SOCKET_ERROR) {
			if (::WSAGetLastError() != WSAEWOULDBLOCK) {
				ErrCode = ::WSAGetLastError();
				return ErrCode;
			}
			break;
		}
		else if (RetVal == 0) {
			break;
		}
		else {
			m_szBuffer[RetVal] = '\0';
			CString strFragment(m_szBuffer);
			strBuffer = strBuffer + strFragment;
		}
		if (::timeGetTime() - StartTime >= Timeout) {
			ErrCode = WSAETIMEDOUT;
			return ErrCode;
		}
	}

	return 0;
}
