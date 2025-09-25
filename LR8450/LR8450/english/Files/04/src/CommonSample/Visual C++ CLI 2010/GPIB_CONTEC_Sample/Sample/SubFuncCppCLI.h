#pragma once

using namespace System;
using namespace System::Windows::Forms;
using namespace System::Runtime::InteropServices;
using namespace System::Drawing;
using namespace Microsoft::Win32;

namespace CGpibCLI
{

	// ************************************************** [チェック(判断)関数] **********************************
	long CheckRet(String^ Func, long Ret, String^ * sBuf)
	{
		long	RetCode;
		long	RetTmp;

		RetCode = 0;						// 正常時
		RetTmp = Ret & 0xff;				// マスク処理
		if(RetTmp >= 3){					// Retが3以上の場合はエラー
			RetCode = 1;					// 異常時
			switch(RetTmp)
			{
				case 3:		*sBuf = Func + " : FIFO内にデータが残っています。"; 							break;	// 0x03
				case 80:	*sBuf = Func + " : I/Oアドレスエラーです。[Config.exe]で確認してください。";	break;	// 0x50
				case 82:	*sBuf = Func + " : レジストリ設定エラーです。[Config.exe]で確認してください。";	break;	// 0x52
				case 128:	*sBuf = Func + " : 受信容量を超えたかSRQを受信していません。"; 					break;	// 0x80
				case 200:	*sBuf = Func + " : スレッドが作成できません。"; 								break;	// 0xC8
				case 201:	*sBuf = Func + " : 他のイベントが実行中です｡"; 									break;	// 0xC9
				case 210:	*sBuf = Func + " : DMAが設定できません｡"; 										break;	// 0xD0
				case 240:	*sBuf = Func + " : Escキーが押されました。"; 									break;	// 0xF0
				case 241:	*sBuf = Func + " : ファイル入出力エラーです。"; 								break;	// 0xF1
				case 242:	*sBuf = Func + " : アドレス指定が間違っています。"; 							break;	// 0xF2
				case 243:	*sBuf = Func + " : バッファ指定エラーです。";									break;	// 0xF3
				case 244:	*sBuf = Func + " : 配列サイズエラーです。";										break;	// 0xF4
				case 245:	*sBuf = Func + " : バッファが小さすぎます。"; 									break;	// 0xF5
				case 246:	*sBuf = Func + " : 不正なオブジェクト名です。"; 								break;	// 0xF6
				case 247:	*sBuf = Func + " : デバイス名の横のチェックが無効です。"; 						break;	// 0xF7
				case 248:	*sBuf = Func + " : 不正なデータ型です。"; 										break;	// 0xF8
				case 249:	*sBuf = Func + " : これ以上デバイスを追加できません。"; 						break;	// 0xF9
				case 250:	*sBuf = Func + " : デバイス名が見つかりません。"; 								break;	// 0xFA
				case 251:	*sBuf = Func + " : デリミタがデバイス間で違っています。"; 						break;	// 0xFB
				case 252:	*sBuf = Func + " : GPIBエラーです。"; 											break;	// 0xFC
				case 253:	*sBuf = Func + " : デリミタのみを受信しました。"; 								break;	// 0xFD
				case 254:	*sBuf = Func + " : タイムアウトしました。"; 									break;	// 0xFE
				case 255:	*sBuf = Func + " : パラメータエラーです。"; 									break;	// 0xFF
			}
		}else{
			*sBuf = Func + " : 正常終了しました。";			
		}

		// -- [Ifc] [Srq] を受信した時の処理 -- //
		RetTmp = Ret & 0xff00;				// マスク処理
		switch(RetTmp)
		{
			case 0x100:		*sBuf = *sBuf + " -- [SRQ]を受信<STATUS>";			break;	// 256(10)
			case 0x200:		*sBuf = *sBuf + " -- [IFC]を受信<STATUS>";			break;	// 512(10)
			case 0x300:		*sBuf = *sBuf + " -- [SRQ]と[IFC]を受信<STATUS>";	break;	// 768(10)
		}
		return	RetCode;
	}
		
	//************************************************************ [べき乗関数] **********************************
	int Pows(int x, int y)
	{
		int tmp = 1;

		while (y-- > 0)													// y の回数分繰り返します。
			tmp *= x;													// tmp に x を掛けていきます。
		return(tmp);
	}

	//****************************************************** [文字列 -> 16進数] **********************************
	unsigned long chr2hex(String^ ch)
	{
		long	length;
		long 	Count;
		long	Ret;
		long	RetTmp;

		RetTmp = 0;
		length	= ch->Length;											// 文字数を調べます。
		for(Count=0; Count<length; Count++){							// 文字数分だけ繰り返します。
			if((ch[Count] >= 0x30) && (ch[Count] <=0x39)){				// ASCIIコードから数的な値を取得	
				Ret = (ch[Count] - 0x30) * Pows(0x10,(length - (Count + 1)));	// 0 - 9 
			}
			else if((ch[Count] >= 0x41) && (ch[Count] <= 0x46)){
				Ret = (ch[Count] - 0x37) * Pows(0x10,(length - (Count + 1)));	// A - F 
			}
			else if((ch[Count] >= 0x61) && (ch[Count] <= 0x66)){
				Ret = (ch[Count] - 0x57) * Pows(0x10,(length - (Count + 1)));	// a - f 
			}
			else{
				Ret = 0xff;												// 不正な場合FF(255)を返します。
			}

			RetTmp = RetTmp + Ret;
		}
		return RetTmp;
	}

	//************************************************************ [初期化関数] **********************************
	long GpibInit(String^ * TextRet)
	{
	//	int				Delim,Eoi;
		int				Timeout, Ifctime, Ret;	
		String^			csBuf;
		unsigned long	Master;

		Ret = GpExit();													// 2重初期化を防ぎます。
		Ret = GpIni();													// GPIBを初期化します。
		csBuf = "GpIni";

		if((Ret & 0xFF) != 0){											// GpIniが正常に行えたかチェック。
			CheckRet("GpIni", Ret, &csBuf);
			*TextRet = csBuf;
			return	1;
		}

		GpBoardsts(0x0a, &Master);										// マスタのアドレスを取得します。
		// マスタ、スレーブの判定
		if(Master == 0){
			Ifctime = 1;												// ここでは100μsecにしています。
			Ret = GpIfc(Ifctime);
			csBuf = "GpIfc";
			if((Ret & 0xFF) != 0){										// GpIfcが正常に行えたかチェック。
				CheckRet("GpIfc", Ret, &csBuf);
				*TextRet = csBuf;
				return	1;
			}
			Ret = GpRen();
			csBuf = "GpRen";
			if((Ret & 0xFF) != 0){										// GpRenが正常に行えたかチェック。
				CheckRet("GpRen", Ret, &csBuf);
				*TextRet = csBuf;
				return	1;
			}
		}

		/*Delim = 1;													// デリミタ：CR+LF
		Eoi = 1;														// EOI     ：使用する
		Ret = GpDelim(Delim, Eoi);
		csBuf = "GpDelim";
		if((Ret & 0xFF) != 0){											// GpDelimが正常に行えたかチェック。
			CheckRet("GpDelim", Ret, &csBuf);
			*TextRet = csBuf;
			return	1;
		}*/
		Timeout = 10000;												// 10秒
		Ret = GpTimeout(Timeout);
		csBuf = "GpTimeout";
		if((Ret & 0xFF) != 0){											// GpTimeoutが正常に行えたかチェック。
			*TextRet = csBuf;
			CheckRet("GpTimeout", Ret, &csBuf);
			return	1;
		}

		*TextRet = "初期化を完了しました。";							// 正常終了
		return	0;
	}

	//******************************************************** [GpTalk()の応用] **********************************
	long GpibPrint(long DevAddr, String^ Str)
	{
		String^					srbuf = gcnew String(' ', 10000);		// 送信文字列
		unsigned long			MyAddr;									// マイアドレス
		array<unsigned long>^	Cmd = gcnew array<unsigned long>(16);	// コマンド用
		String^					ErrText;								// エラー文字列
		long					Ret, RetTmp, srlen;						// 戻り値、予備戻り値、文字列の長さ

		Ret = GpBoardsts(0x08, &MyAddr);								// マイアドレス取得
		Cmd[0] = 2;														// コマンドの数
		Cmd[1] = MyAddr;												// マイアドレス(PC)
		Cmd[2] = DevAddr;												// スレーブ機器

		srlen = Str->Length;											// 長さを測定
		srbuf = Str;										
		Ret = GpTalk(Cmd, srlen, srbuf);								// 実際の送信
		if (Ret >= 3){													// エラーチェック
			RetTmp = CheckRet("GpTalk", Ret, &ErrText);
			ErrText += " 継続しますか？";
			if (MessageBox::Show(ErrText, Application::ProductName, MessageBoxButtons::YesNo, MessageBoxIcon::Warning) == DialogResult::No){
				return 1;												// 異常
			}
		}
		return 0;														// 正常
	}

	//****************************************************** [GpListen()の応用] **********************************
	long GpibInput(long DevAddr, StringBuilder^ Str)
	{
		unsigned long			MyAddr, srlen;							// マイアドレス、文字列の長さ
		array<unsigned long>^	Cmd = gcnew array<unsigned long>(16);	// コマンド用
		String^					ErrText;								// エラー文字列
		long					Ret, RetTmp;							// 戻り値、予備戻り値

		Ret = GpBoardsts(0x08, &MyAddr);								// マイアドレス取得
		Cmd[0] = 2;														// コマンドの数
		Cmd[1] = DevAddr;												// スレーブ機器
		Cmd[2] = MyAddr;												// マイアドレス(PC)
		srlen = Str->Capacity;											// 受信したデータの長さを測っています。
		Ret = GpListen(Cmd, &srlen, Str);								// 実際の送信
		if (Ret >= 3){													// エラーチェック
			RetTmp = CheckRet("GpListen", Ret, &ErrText);
			ErrText += " 継続しますか？";
			if (MessageBox::Show(ErrText, Application::ProductName, MessageBoxButtons::YesNo, MessageBoxIcon::Warning) == DialogResult::No){
				return 1;												// 異常 = 1を返す
			}
		}
				
		return 0;														// 正常 = 0を返す
	}

	//HIOKI追加
	//****************************************************** [GpListen()の応用] **********************************
	long GpibInputHioki(long DevAddr, StringBuilder^ Str)
	{
		StringBuilder^			Srbuf = gcnew StringBuilder(10000);		// 文字列のバッファ
		unsigned long			Srlen;									// 文字列の長さ
		unsigned long			MyAddr;									// マイアドレス
		array<unsigned long>^	Cmd = gcnew array<unsigned long>(16);	// メッセージ(コマンド)
		String^					ErrText;								// エラー文字列
		long					Ret;									// 戻り値

		Ret = GpBoardsts(0x08, &MyAddr);								// マイアドレス取得
		Cmd[0] = 2;														// コマンドの数
		Cmd[1] = DevAddr;												// スレーブ機器
		Cmd[2] = MyAddr;												// マイアドレス(PC)

		Str->Clear();													// 初期化
		while (true)
		{
			Srlen = 10000;												// 最大受信数
			Ret = GpListen(Cmd, &Srlen, Srbuf);
			if (Ret <= 2)
			{															// 受信終了
				Srbuf->Remove(static_cast<int>(Srlen), Srbuf->Length - static_cast<int>(Srlen));
				Str->Append(Srbuf);
				break;
			}
			else if (Ret == 128)
			{															// 受信データ域オーバー
				Srbuf->Remove(static_cast<int>(Srlen), Srbuf->Length - static_cast<int>(Srlen));
				Str->Append(Srbuf);
				Cmd[0] = 0;												// コマンドを出さずにGpListenします。
			}
			else
			{
				CheckRet("GpListen", Ret, &ErrText);
				MessageBox::Show(ErrText, Application::ProductName, MessageBoxButtons::OK, MessageBoxIcon::Warning);
				return 1;												// 異常 = 1を返す
			}
		}
		return 0;														// 正常 = 0を返す
	}

	// ************************************************* [ バイナリ受信用関数 ] **********************************
	long GpibInputB(long DevAddr, StringBuilder^ IntData)
	{				
		StringBuilder^			szData	= gcnew StringBuilder(10000);
		unsigned long			Ret, RetTmp, MyAddr, srlen;
		array<unsigned long>^	Cmd = gcnew array<unsigned long>(8);
		String^					ErrText = "";
		String^					szDataVal;
		int						i;

		Ret = GpDelim(0, 1);											// デリミタを相手機器と合わせます。
		Ret = GpBoardsts(0x08, &MyAddr);								// マイアドレス取得
		Cmd[0] = 2;														// コマンドの数
		Cmd[1] = DevAddr;												// スレーブ機器
		Cmd[2] = MyAddr;												// マイアドレス(PC)
		srlen = 2;														// 受信したデータの長さを測っています。
		Ret = GpListen(Cmd, &srlen, szData);
		if (Ret != 128){												// 途中でデータを切っているためRet=128になります。
			if (Ret >= 3){												// エラーチェック
				RetTmp = CheckRet("GpListen", Ret, &ErrText);
				ErrText += " 継続しますか？";
				if (MessageBox::Show(ErrText, Application::ProductName, MessageBoxButtons::YesNo, MessageBoxIcon::Warning) == DialogResult::No){
					return 1;											// 異常 = 1を返す
				}
			}
		}
		Cmd[0] = 0;
								
		szDataVal = szData->ToString()->Substring(1, 1);
		for (i = 0; i < szDataVal->Length; i++)
		{
			if (Char::IsDigit(szDataVal, i) == false){
				break;
			}
		}			
		szDataVal = szDataVal->Substring(0, i);
		if (i == 0){
			srlen = 0;
		}
		else{
			srlen = int::Parse(szDataVal);
		}	
		Ret = GpListen(Cmd, &srlen, szData);

		for (i = 0; i < szData->Length; i++)
		{
			if (Char::IsDigit(szData->ToString(), i) == false){
				break;
			}
		}
		szDataVal = szData->ToString()->Substring(0, i);
		if (i == 0){
			srlen = 1;
		}
		else{
			srlen = int::Parse(szDataVal) + 1;
		}
		Ret = GpListen(Cmd, &srlen, IntData);

		Ret = GpDelim(3, 1);											// デリミタを戻します。
		return 0;
	}

	//****************************************************** [コマンド送信関数] **********************************
	long GpibCommand(long DevAddr)
	{
		array<unsigned long>^	Cmd = gcnew array<unsigned long>(16);
		String^					ErrText;
		long					Ret, RetTmp;

		Cmd[0] = 2;
		Cmd[1] = 0x3F;
		Cmd[2] = 0x5F;

		Ret = GpComand(Cmd);

		if (Ret != 0){
			RetTmp = CheckRet("GpComand", Ret, &ErrText);
			MessageBox::Show(ErrText, Application::ProductName, MessageBoxButtons::OK, MessageBoxIcon::Warning);
			return 1;
		}
		return 0;
	}

	//**************************************************************** [終了関数] ********************************
	void GpibExit()
	{
		unsigned long			Master;
		array<unsigned long>^	Cmd = gcnew array<unsigned long>(16);
		long					Ret;

		Ret = GpBoardsts(0x0a, &Master);								// マスタのアドレスを取得します。
		if(Ret == 80) return;											// 初期化されていない場合何もせずに戻ります。
			
		if(Master == 0){												// マスタの場合
			Cmd[0] = 2;													// コマンド(メッセージ)数
			Cmd[1] = 0x3f;												// アンリスン(リスナ解除)
			Cmd[2] = 0x5f;												// アントークン(トーカ解除)
			Ret = GpComand(Cmd);										// コマンドを送信します。
		}
		Ret = GpResetren();												// 相手機器のリモートを解除します。
				
		Ret = GpExit();
	}

	// OPCのチェック ////////////////////////////////////////////////////////////////////////////////
	void WaitOPC(long Dev)
	{
		long			Ret;
		StringBuilder^	RdData = gcnew StringBuilder(10000);

		Ret = GpibPrint(Dev, "*OPC?");									// 工程作業が完了しているか
		Ret = GpibInput(Dev, RdData);
	}

	//**************************************************** [文字列を数字に変換] **********************************
	void Str2Num(String^ str, unsigned long str_len , array<int>^ num, unsigned long num_len)
	{
		unsigned long	i, j, cnt;
		String^			start;

		start = str;
		j = 0;
		cnt = 0;
		for (i=0; i<str_len; i++) {
			/* string to integer */
			if (str[i] == ',') {
				start = str->Substring(j, i-j);
				try{
					num[cnt] = Convert::ToInt32(start);
				}
				catch (...){
					num[cnt] = 0;
				}
				j = i + 1;
				cnt++;
				if (cnt >= num_len){
					break;
				}
			}
		}
		if (cnt >= num_len){
			try
			{
				num[cnt] = Convert::ToInt32(start);
			}
			catch (...)
			{
				num[cnt] = 0;
			}

		}
	}

	//********************************************************** [グラフを描画] ********************************
	// 第２引数でグラフ用ピクチャーダイアログを使用しています。
	void DrawGraph(Control^ Picture, array<int>^ num, unsigned long num_len, int min, int max)
	{
		Rectangle		Rect = Picture->ClientRectangle;
		Pen^			hPen_Black;
		Pen^			hPen_Red;
		Pen^			hPen_White;
		array<Point>^	point = gcnew array<Point>(4);
		int				x_max, y_max;
		int				x_width, y_width;
		float			x_unit, y_unit;
		unsigned long	i;

		/* Initialize */
		x_max = Rect.Right;
		y_max = Rect.Bottom;
		Graphics^ g = Picture->CreateGraphics();

		hPen_Black	= gcnew Pen(Color::Black, 1);			/* Black */
		hPen_Red	= gcnew Pen(Color::Red, 1);				/* Red   */
		hPen_White	= gcnew Pen(Color::White, 1);			/* White */
		/* Draw Structure */
		SolidBrush^ whiteBrush = gcnew SolidBrush(Color::White);
		g->FillRectangle(whiteBrush, Picture->ClientRectangle);
		for (i = 0; i <= 10; i++)
		{
			g->DrawLine(hPen_Black, (x_max / 10) * i, 0, (x_max / 10) * i, y_max);
		}
		for (i = 0; i <= 10; i++)
		{
			g->DrawLine(hPen_Black, 0, (y_max / 10) * i, x_max, (y_max / 10) * i);
		}
		point[0].X = (x_max / 10) * 5 - 1;	point[0].Y = 0;
		point[1].X = (x_max / 10) * 5 + 1;	point[1].Y = 0;
		point[2].X = (x_max / 10) * 5 + 1;	point[2].Y = y_max;
		point[3].X = (x_max / 10) * 5 - 1;	point[3].Y = y_max;
		g->DrawLines(hPen_Red, point);
		point[0].X = 0;		point[0].Y = (y_max / 10) * 5 - 1;
		point[1].X = 0;		point[1].Y = (y_max / 10) * 5 + 1;
		point[2].X = x_max;	point[2].Y = (y_max / 10) * 5 + 1;
		point[3].X = x_max;	point[3].Y = (y_max / 10) * 5 - 1;
		g->DrawLines(hPen_Red, point);
		/* Draw Graph */
		x_width = (int)num_len;
		y_width = max - min;
		x_unit = (float)((float)x_max / (float)x_width);
		y_unit = (float)((float)y_max / (float)y_width);
		for (i = 0; i < (num_len - 1); i++)
		{
			g->DrawLine(hPen_Black, x_unit * i, (y_width - (num[i] - min)) * y_unit, x_unit * (i + 1), (y_width - (num[i+1] - min)) * y_unit);
		}
	}
}