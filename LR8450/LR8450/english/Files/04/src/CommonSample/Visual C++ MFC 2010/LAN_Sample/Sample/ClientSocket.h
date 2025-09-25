#pragma once

class CClientSocket
{
private:
	WSADATA m_WsaData;											//WinSock情報
	sockaddr_in m_Address;										//接続先情報
	SOCKET m_Socket;											//ソケット
	char m_szBuffer[1024];										//受信バッファ

public:
	CClientSocket();
	virtual ~CClientSocket();
	int Connect(const char *pszIpAddress, unsigned int Port);
	int Disconnect();
	int Send(const char *pszBuffer);
	int Receive(CString &strBuffer, unsigned long Timeout);
};
