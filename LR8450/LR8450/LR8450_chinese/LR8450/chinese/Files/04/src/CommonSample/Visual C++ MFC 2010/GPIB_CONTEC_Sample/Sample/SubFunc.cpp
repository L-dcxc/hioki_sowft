#include "stdafx.h"
#include ".\SubFunc.h"
#include ".\Gpibac.h"

// ************************************************** [チェック(判断)関数] ***
long CheckRet(CString Func, long Ret, CString *csBuf)
{
	long	RetCode;
	long	RetTmp;

	RetCode = 0;						// 正常時
	RetTmp = Ret & 0xff;				// マスク処理
	if(RetTmp >= 3){					// Retが3以上の場合はエラー
		RetCode = 1;					// 異常時
		switch(RetTmp)
		{
			case 3:		*csBuf = Func + _T(" : FIFO内にデータが残っています。"); 								break;	// 0x03
			case 80:	*csBuf = Func + _T(" : I/Oアドレスエラーです。[Config.exe]で確認してください。"); 		break;	// 0x50
			case 82:	*csBuf = Func + _T(" : レジストリ設定エラーです。[Config.exe]で確認してください。");	break;	// 0x52
			case 128:	*csBuf = Func + _T(" : 受信容量を超えたかSRQを受信していません。"); 					break;	// 0x80
			case 200:	*csBuf = Func + _T(" : スレッドが作成できません。"); 									break;	// 0xC8
			case 201:	*csBuf = Func + _T(" : 他のイベントが実行中です｡"); 									break;	// 0xC9
			case 210:	*csBuf = Func + _T(" : DMAが設定できません｡"); 											break;	// 0xD0
			case 240:	*csBuf = Func + _T(" : Escキーが押されました。"); 										break;	// 0xF0
			case 241:	*csBuf = Func + _T(" : ファイル入出力エラーです。"); 									break;	// 0xF1
			case 242:	*csBuf = Func + _T(" : アドレス指定が間違っています。"); 								break;	// 0xF2
			case 243:	*csBuf = Func + _T(" : バッファ指定エラーです。");										break;	// 0xF3
			case 244:	*csBuf = Func + _T(" : 配列サイズエラーです。");										break;	// 0xF4 	
			case 245:	*csBuf = Func + _T(" : バッファが小さすぎます。"); 										break;	// 0xF5
			case 246:	*csBuf = Func + _T(" : 不正なオブジェクト名です。"); 									break;	// 0xF6
			case 247:	*csBuf = Func + _T(" : デバイス名の横のチェックが無効です。"); 							break;	// 0xF7
			case 248:	*csBuf = Func + _T(" : 不正なデータ型です。"); 											break;	// 0xF8
			case 249:	*csBuf = Func + _T(" : これ以上デバイスを追加できません。"); 							break;	// 0xF9
			case 250:	*csBuf = Func + _T(" : デバイス名が見つかりません。"); 									break;	// 0xFA
			case 251:	*csBuf = Func + _T(" : デリミタがデバイス間で違っています。"); 							break;	// 0xFB
			case 252:	*csBuf = Func + _T(" : GPIBエラーです。"); 												break;	// 0xFC
			case 253:	*csBuf = Func + _T(" : デリミタのみを受信しました。"); 									break;	// 0xFD
			case 254:	*csBuf = Func + _T(" : タイムアウトしました。"); 										break;	// 0xFE
			case 255:	*csBuf = Func + _T(" : パラメータエラーです。"); 										break;	// 0xFF
		}
	}else{
		*csBuf = Func + _T(" : 正常終了しました。");
	}

	// -- [Ifc] [Srq] を受信した時の処理 -- //
    RetTmp = Ret & 0xff00;	// マスク処理
	switch(RetTmp)
	{
		case 0x100:		*csBuf = *csBuf + _T(" -- [SRQ]を受信<STATUS>");		break;	// 256(10)
		case 0x200:		*csBuf = *csBuf + _T(" -- [IFC]を受信<STATUS>");		break;	// 512(10)
		case 0x300:		*csBuf = *csBuf + _T(" -- [SRQ]と[IFC]を受信<STATUS>");	break;	// 768(10)
	}
	return	RetCode;
}

//************************************************************ [べき乗関数] ***
int Pows(int x, int y)
{
	int tmp = 1;

	while (y-- > 0)										// y の回数分繰り返します。
		tmp *= x;										// tmp に x を掛けていきます。
	return(tmp);
}

//****************************************************** [文字列 -> 16進数] ***
DWORD chr2hex(TCHAR* ch)
{
	long	length;
	long 	Count;
	long	Ret;
	long	RetTmp;

	RetTmp = 0;
	length	= lstrlen(ch);								// 文字数を調べます。
	for(Count = 0;Count < length ;Count++){				// 文字数分だけ繰り返します。
		if((ch[Count] >= 0x30) && (ch[Count] <=0x39))	// ASCIIコードから数的な値を取得	
		  Ret = (ch[Count] - 0x30) * Pows(0x10,(length - (Count + 1)));	// 0 - 9 
		else if((ch[Count] >= 0x41) && (ch[Count] <= 0x46))
		  Ret = (ch[Count] - 0x37) * Pows(0x10,(length - (Count + 1)));	// A - F 
		else if((ch[Count] >= 0x61) && (ch[Count] <= 0x66))
		  Ret = (ch[Count] - 0x57) * Pows(0x10,(length - (Count + 1)));	// a - f 
		else
		  Ret = 0xff;									// 不正な場合FF(255)を返します。
	
		RetTmp = RetTmp + Ret;
	}
	return RetTmp;
}

//************************************************************ [初期化関数] ***
long GpibInit(CString *TextRet)
{
//	int		Delim,Eoi;
	int		Timeout,Ifctime,Ret;	
	CString	csBuf;
	DWORD	Master;


	Ret = GpExit();										// 2重初期化を防ぎます。
	Ret = GpIni();										// GPIBを初期化します。
	csBuf = _T("GpIni");

	if((Ret & 0xFF) != 0){								// GpIniが正常に行えたかチェック。
		CheckRet(_T("GpIni"), Ret, &csBuf);
		*TextRet = csBuf;
		return	1;
	}

	GpBoardsts(0x0a, &Master);							// マスタのアドレスを取得します。
	// マスタ、スレーブの判定
	if(Master == 0){
		Ifctime = 1;									// ここでは100μsecにしています。
		Ret = GpIfc(Ifctime);
		csBuf = _T("GpIfc");
		if((Ret & 0xFF) != 0){							// GpIfcが正常に行えたかチェック。
			CheckRet(_T("GpIfc"), Ret, &csBuf);
			*TextRet = csBuf;
			return	1;
		}
		Ret = GpRen();
		csBuf = _T("GpRen");
		if((Ret & 0xFF) != 0){							// GpRenが正常に行えたかチェック。
			CheckRet(_T("GpRen"), Ret, &csBuf);
			*TextRet = csBuf;
			return	1;
		}
	}

	/*Delim = 1;										// デリミタ：CR+LF
	Eoi = 1;											// EOI     ：使用する
	Ret = GpDelim(Delim, Eoi);
	csBuf = "GpDelim";
	if((Ret & 0xFF) != 0){								// GpDelimが正常に行えたかチェック。
		CheckRet("GpDelim", Ret, &csBuf);
		*TextRet = csBuf;
		return	1;
	}*/
	Timeout = 10000;									// 10秒
	Ret = GpTimeout(Timeout);
	csBuf = _T("GpTimeout");
	if((Ret & 0xFF) != 0){								// GpTimeoutが正常に行えたかチェック。
		*TextRet = csBuf;
		CheckRet(_T("GpTimeout"), Ret, &csBuf);
		return	1;
	}

	*TextRet = _T("初期化を完了しました。");			// 正常終了
	return	0;
}

//******************************************************** [GpTalk()の応用] ***
long GpibPrint(long DevAddr, CString Str)
{
	char	srbuf[10000];								// 送信文字列
	TCHAR	szbuf[10000];
	DWORD	MyAddr, Cmd[16];							// マイアドレス、コマンド用
	CString	ErrText;									// エラー文字列
	long	Ret, RetTmp, srlen;							// 戻り値、予備戻り値、文字列の長さ

	Ret = GpBoardsts(0x08, &MyAddr);					// マイアドレス取得
	Cmd[0] = 2;											// コマンドの数
	Cmd[1] = MyAddr;									// マイアドレス(PC)
	Cmd[2] = DevAddr;									// スレーブ機器

	srlen = lstrlen(Str);								// 長さを測定
	lstrcpy(szbuf, Str);								// CString -> TCHAR
#ifdef _UNICODE
	sprintf_s(srbuf, srlen + 1, "%S", szbuf);			// TCHAR   -> char
#else
	strcpy_s(srbuf, sizeof(srbuf), szbuf);				// HIOKI編集(MBCS対応)
#endif
    Ret = GpTalk(Cmd, srlen, (UCHAR*)srbuf);			// 実際の送信

	if (Ret >= 3){										// エラーチェック
		RetTmp = CheckRet(_T("GpTalk"), Ret, &ErrText);
		ErrText += _T(" 継続しますか？");
		Ret = AfxMessageBox(ErrText, MB_YESNO);
		if (Ret == IDNO) return 1;						// 異常
	}
	return 0;											// 正常
}

//****************************************************** [GpListen()の応用] ***
long GpibInput(long DevAddr, CString *Str)
{
	BYTE	srbuf[10000];								// 受信データが10000より大きい場合は値を変更して下さい。
	DWORD	MyAddr,srlen, Cmd[16];						// マイアドレス、文字列の長さ、コマンド用
	CString	TmpStr, ErrText;							// 予備文字列、エラー文字列
	long	Ret, RetTmp;								// 戻り値、予備戻り値

   	memset( srbuf, '\0', 10000 );						// 初期化

    Ret = GpBoardsts(0x08, &MyAddr);					// マイアドレス取得
	Cmd[0] = 2;											// コマンドの数
	Cmd[1] = DevAddr;									// スレーブ機器
	Cmd[2] = MyAddr;									// マイアドレス(PC)
	srlen = sizeof(srbuf);								// 受信したデータの長さを測っています。
    Ret = GpListen(Cmd, &srlen, srbuf);					// 実際の送信
	if (Ret >= 3){										// エラーチェック
		RetTmp = CheckRet(_T("GpListen"), Ret, &ErrText);
		ErrText += _T(" 継続しますか？");
		Ret = AfxMessageBox(ErrText, MB_YESNO);
		if (Ret == IDNO) return 1;						// 異常 = 1を返す
	}
	*Str = srbuf;
	return 0;											// 正常 = 0を返す
}

//HIOKI追加
//****************************************************** [GpListen()の応用] ***
long GpibInputHioki(long DevAddr, CString *Str)
{
	BYTE	Srbuf[10000];								// 文字列のバッファ
	DWORD	Srlen;										// 文字列の長さ
	DWORD	MyAddr;										// マイアドレス
	DWORD	Cmd[16];									// メッセージ(コマンド)
	CString	ErrText;									// エラー文字列
	long	Ret;										// 戻り値

	Ret = GpBoardsts(0x08, &MyAddr);					// マイアドレス取得
	Cmd[0] = 2;											// コマンドの数
	Cmd[1] = DevAddr;									// スレーブ機器
	Cmd[2] = MyAddr;									// マイアドレス(PC)

	*Str = "";											// 初期化
	while (true){
		Srlen = sizeof(Srbuf) - 1;						// 最大受信数
		Ret = GpListen(Cmd, &Srlen, Srbuf);
		if (Ret <= 2){									// 受信終了
			Srbuf[Srlen] = '\0';
			CString Srtmp(Srbuf);
			*Str += Srtmp;
			break;
		}
		else if (Ret == 128){							// 受信データ域オーバー
			Srbuf[Srlen] = '\0';
			CString Srtmp(Srbuf);
			*Str += Srtmp;
			Cmd[0] = 0;									// コマンドを出さずにGpListenします。
		}
		else{
			CheckRet(_T("GpListen"), Ret, &ErrText);
			Ret = AfxMessageBox(ErrText, MB_OK);
			return 1;									// 異常 = 1を返す
		}
	}
	return 0;											// 正常 = 0を返す
}

// ************************************************* [ バイナリ受信用関数 ] ***
long GpibInputB(long DevAddr, BYTE *IntData)
{
	BYTE	szData[10000];
	DWORD	Ret, RetTmp, MyAddr, Cmd[8], srlen;
	CString	ErrText = _T("");

	memset(szData, '\0', 10000);

	Ret = GpDelim(0, 1);								// デリミタを相手機器と合わせます。
    Ret = GpBoardsts(0x08, &MyAddr);					// マイアドレス取得
	Cmd[0] = 2;											// コマンドの数
	Cmd[1] = DevAddr;									// スレーブ機器
	Cmd[2] = MyAddr;									// マイアドレス(PC)
	srlen = 2;											// 受信したデータの長さを測っています。
	Ret = GpListen(Cmd, &srlen, szData);
	if (Ret != 128){									// 途中でデータを切っているためRet=128になります。
		if (Ret >= 3){									// エラーチェック
			RetTmp = CheckRet(_T("GpListen"), Ret, &ErrText);
			ErrText += _T(" 継続しますか？");
			Ret = AfxMessageBox(ErrText, MB_YESNO);
			if (Ret == IDNO) return 1;					// 異常 = 1を返す
		}
	}
	Cmd[0] = 0;
	srlen = _ttoi((LPCTSTR)&szData[1]);
	Ret = GpListen(Cmd, &srlen, szData);
	srlen = (_ttoi((LPCTSTR)&szData)) + 1;
	Ret = GpListen(Cmd, &srlen, IntData);

	Ret = GpDelim(3, 1);								// デリミタを戻します。
	return 0;
}

//****************************************************** [コマンド送信関数] ***
long GpibCommand(long DevAddr)
{
	DWORD	Cmd[16];
	CString	ErrText;
	long	Ret, RetTmp;

	Cmd[0] = 2;
	Cmd[1] = 0x3F;
	Cmd[2] = 0x5F;

	Ret = GpComand(Cmd);

	if (Ret != 0){
		RetTmp = CheckRet(_T("GpComand"), Ret, &ErrText);
		AfxMessageBox(ErrText, MB_OK);
		return 1;
	}
	return 0;
}

//**************************************************************** [終了関数] ***
void GpibExit()
{
	DWORD	Master, Cmd[16];
	long	Ret;

	Ret = GpBoardsts(0x0a, &Master);					// マスタのアドレスを取得します。
	if(Ret == 80) return;								// 初期化されていない場合何もせずに戻ります。
	
	if(Master == 0){									// マスタの場合
		Cmd[0] = 2;										// コマンド(メッセージ)数
		Cmd[1] = 0x3f;									// アンリスン(リスナ解除)
		Cmd[2] = 0x5f;									// アントークン(トーカ解除)
		Ret = GpComand(Cmd);							// コマンドを送信します。
	}
		Ret = GpResetren();								// 相手機器のリモートを解除します。
	
	Ret = GpExit();
}

// OPCのチェック ////////////////////////////////////////////////////////////////////////////////
void WaitOPC(long Dev)
{
	long	Ret;
	CString RdData;

	Ret = GpibPrint(Dev, _T("*OPC?"));					// 工程作業が完了しているか
	Ret = GpibInput(Dev, &RdData);
}

//**************************************************** [文字列を数字に変換] ***
void Str2Num(char *str, DWORD str_len, int *num, DWORD num_len)
{
	DWORD i, cnt;
	char *start;

	start = str;
	cnt = 0;
	for (i=0; i<str_len; i++) {
		/* string to integer */
		if (str[i] == ',') {
			str[i] = '\0';
			num[cnt] = atoi(start);
			str[i] = ',';
			start = &str[i+1];
			cnt++;
			if (cnt >= num_len) break;
		}
	}
	if (cnt >= num_len) {
		num[cnt] = atoi(start);
	}
}

//********************************************************** [グラフを描画] ***
// 第２引数でグラフ用ピクチャーダイアログを使用しています。
void DrawGraph(HWND hDlg, DWORD Picture, int *num, DWORD num_len, int min, int max)
{
	HWND	Disp_handle;
	RECT	Rect;
	HDC		hDC;
	HPEN	hPen_Black, hPen_Red, hPen_White;
	HBRUSH	hBrush1, hBrush2, hBrush3;
	POINT	Point[4];
	int		x_max, y_max;
	int		x_width, y_width;
	float	x_unit, y_unit;
	DWORD	i;

	/* Initialize */
	Disp_handle = GetDlgItem(hDlg, Picture);
	GetClientRect(Disp_handle, &Rect);
	x_max = Rect.right;
	y_max = Rect.bottom;
	hDC = GetDC(Disp_handle);

	hPen_Black = CreatePen(PS_SOLID, 1, RGB(0, 0, 0));		/* Black */
	hPen_Red   = CreatePen(PS_SOLID, 1, RGB(255, 0, 0));	/* Red   */
	hPen_White = CreatePen(PS_SOLID, 1, RGB(255, 255, 255));/* White */	
	/* Draw Structure */
	hBrush3 = (HBRUSH)SelectObject(hDC, hPen_White);
	Rectangle(hDC, Rect.left, Rect.top, Rect.right, Rect.bottom);
	hBrush1 = (HBRUSH)SelectObject(hDC, hPen_Black);
	for (i=0; i<=10; i++) {
		MoveToEx(hDC, (x_max / 10) * i, 0, NULL);
		LineTo(  hDC, (x_max / 10) * i, y_max);
	}
	for (i=0; i<=10; i++) {
		MoveToEx(hDC, 0,   (y_max / 10) * i, NULL);
		LineTo(hDC, x_max, (y_max / 10) * i);
	}
	hBrush2 = (HBRUSH)SelectObject(hDC, hPen_Red);
	Point[0].x = (x_max / 10) * 5 - 1; Point[0].y = 0;
	Point[1].x = (x_max / 10) * 5 + 1; Point[1].y = 0;
	Point[2].x = (x_max / 10) * 5 + 1; Point[2].y = y_max;
	Point[3].x = (x_max / 10) * 5 - 1; Point[3].y = y_max;
	Polyline(hDC, &Point[0], 4);
	Point[0].x = 0;     Point[0].y = (y_max / 10) * 5 - 1;
	Point[1].x = 0;     Point[1].y = (y_max / 10) * 5 + 1;
	Point[2].x = x_max; Point[2].y = (y_max / 10) * 5 + 1;
	Point[3].x = x_max; Point[3].y = (y_max / 10) * 5 - 1;
	Polyline(hDC, &Point[0], 4);
	/* Draw Graph */
	hBrush1 = (HBRUSH)SelectObject(hDC, hPen_Black);
	x_width = num_len;
	y_width = max - min;
	x_unit = (float)((float)x_max / (float)x_width);
	y_unit = (float)((float)y_max / (float)y_width);
	for (i=0; i<num_len-1; i++) {
		MoveToEx(hDC, (int)(x_unit * i)      , (int)((y_width - (num[i] - min)) * y_unit) , NULL);
		LineTo(  hDC, (int)(x_unit * (i + 1)), (int)((y_width - (num[i+1] - min)) * y_unit));
	}
	/* ending */
	SelectObject(hDC, hBrush1);
	DeleteObject(hPen_Black);
	SelectObject(hDC, hBrush2);
	DeleteObject(hPen_Red);
	SelectObject(hDC, hBrush3);
	DeleteObject(hPen_White);
	ReleaseDC(Disp_handle, hDC);
}


