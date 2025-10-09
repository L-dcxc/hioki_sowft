/***********************************************************************/
/*          API-GPIB(98/PC)W95,NT                 Header  File         */
/*                                                File Name SUBCLASS.H */
/***********************************************************************/

#ifndef __SUBFUNC_H__
#define __SUBFUNC_H__

// ************************************************************* [Check関数] ***
long CheckRet(CString Func, long Ret, CString *csBuf);

//************************************************************* [べき乗関数] ***
int Square(int x, int y);

//******************************************************* [文字列 -> 16進数] ***
DWORD chr2hex(TCHAR *ch);

//************************************************************* [初期化関数] ***
long GpibInit(CString *TextRet);

//************************************************************* [GpTalk関数] ***
long GpibPrint(long DevAddr, CString TextRet);

//*********************************************************** [GpListen関数] ***
long GpibInput(long DevAddr, CString *TextRet);

//HIOKI追加
//*********************************************************** [GpListen関数] ***
long GpibInputHioki(long DevAddr, CString *TextRet);

//********************************************************* [バイナリ受信用] ***
long GpibInputB(long DevAddr, BYTE *IntData);

//******************************************************* [コマンド送信関数] ***
long GpibCommand(CString *TextRet);

//*************************************************************** [終了関数] ***
void GpibExit(void);

//************************************************************ [WaitOPC関数] ***
void WaitOPC(long Dev);

//***************************************************** [文字列を数字に変換] ***
void Str2Num(char *str, DWORD str_len, int *num, DWORD num_len);

//*********************************************************** [グラフを描画] ***
// 第２引数でグラフ用ピクチャーダイアログを使用しています。
void DrawGraph(HWND hDlg, DWORD Picture, int *num, DWORD num_len, int min, int max);


#endif
