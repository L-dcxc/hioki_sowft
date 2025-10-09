using System;
using System.Text;
using System.Windows.Forms;
using System.Drawing;
using System.Globalization;
using System.Runtime.InteropServices;
using Microsoft.Win32;
using CgpibCs;

namespace CSubFuncCs
{
	/// <summary>
	/// SubFunc の概要の説明です。
	/// </summary>
	public class CSubFunc
	{
		public CSubFunc()
		{
			// 
			// TODO: コンストラクタ ロジックをここに追加してください。
			//
		}

		Cgpib	gpib = new Cgpib();

		// ************************************************** [チェック(判断)関数] ***
		public int CheckRet(string Func, uint Ret, out string csBuf)
		{
			int	RetCode;
			int	RetTmp;

			csBuf = new String('0', 1);
			RetCode = 0;										// 正常時
			RetTmp = (int)Ret & 0xff;							// マスク処理
			if (RetTmp >= 3)
			{													// Retが3以上の場合はエラー
				RetCode = 1;									// 異常時
				switch (RetTmp)
				{
					case 80:	csBuf = Func + " : I/Oアドレスエラーです。[Config.exe]で確認してください。";	break;	// 0x50
					case 82:	csBuf = Func + " : レジストリ設定エラーです。[Config.exe]で確認してください。";	break;	// 0x52
					case 128:	csBuf = Func + " : 指定データ数受信又は[SRQ]は上がっていません"; 				break;	// 0x80
					case 140:	csBuf = Func + " : 非同期関数の実行中です"; 									break;	// 0x8C
					case 141:	csBuf = Func + " : 非同期関数が強制終了されました"; 							break;	// 0x8D
					case 200:	csBuf = Func + " : スレッドが作成できません。"; 								break;	// 0xC8
					case 201:	csBuf = Func + " : 他のイベントが実行中です｡"; 									break;	// 0xC9
					case 210:	csBuf = Func + " : DMAが設定できません｡"; 										break;	// 0xD0
					case 240:	csBuf = Func + " : Escキーが押されました。"; 									break;	// 0xF0
					case 241:	csBuf = Func + " : ファイル入出力エラーです。"; 								break;	// 0xF1
					case 242:	csBuf = Func + " : アドレス指定が間違っています。"; 							break;	// 0xF2
					case 243:	csBuf = Func + " : バッファ指定エラーです。";									break;	// 0xF3
					case 244:	csBuf = Func + " : 配列サイズエラーです。";										break;	// 0xF4
					case 245:	csBuf = Func + " : バッファが小さすぎます。"; 									break;	// 0xF5
					case 246:	csBuf = Func + " : 不正なオブジェクト名です。"; 								break;	// 0xF6
					case 247:	csBuf = Func + " : デバイス名の横のチェックが無効です。"; 						break;	// 0xF7
					case 248:	csBuf = Func + " : 不正なデータ型です。"; 										break;	// 0xF8
					case 249:	csBuf = Func + " : これ以上デバイスを追加できません。"; 						break;	// 0xF9
					case 250:	csBuf = Func + " : デバイス名が見つかりません。"; 								break;	// 0xFA
					case 251:	csBuf = Func + " : デリミタがデバイス間で違っています。"; 						break;	// 0xFB
					case 252:	csBuf = Func + " : GPIBエラーです。"; 											break;	// 0xFC
					case 253:	csBuf = Func + " : デリミタのみを受信しました。"; 								break;	// 0xFD
					case 254:	csBuf = Func + " : タイムアウトしました。"; 									break;	// 0xFE
					case 255:	csBuf = Func + " : パラメータエラーです。"; 									break;	// 0xFF
					default:	break;
				}
			}
			else
			{
				csBuf = Func + " : 正常終了しました。";
			}

			// -- [Ifc] [Srq] を受信した時の処理 -- //
			RetTmp = (int)Ret & 0xff00;							// マスク処理
			switch (RetTmp)
			{
				case 0x100:		csBuf = csBuf + " -- [SRQ]を受信<STATUS>";			break;		// 256(10)
				case 0x200:		csBuf = csBuf + " -- [IFC]を受信<STATUS>";			break;		// 512(10)
				case 0x300:		csBuf = csBuf + " -- [SRQ]と[IFC]を受信<STATUS>";	break;		// 768(10)
				default:		break;
			}
			return	RetCode;
		}
		
		//************************************************************ [べき乗関数] ***
		public int Pows(int x, int y)
		{
			int	tmp = 1;

			while (y-- > 0)										// y の回数分繰り返します。
				tmp *= x;										// tmp に x を掛けていきます。
			return(tmp);
		}
		
		//****************************************************** [文字列 -> 16進数] ***
		public uint chr2hex(string ch)
		{
			int		length;
			int		Count;
			int		Ret;
			int		RetTmp;

			RetTmp = 0;
			length	= ch.Length;								// 文字数を調べます。
			for (Count = 0; Count < length; Count++)
			{													// 文字数分だけ繰り返します。
				if ((ch[Count] >= 0x30) && (ch[Count] <= 0x39))	// ASCIIコードから数的な値を取得
				{
					Ret = (ch[Count] - 0x30) * Pows(0x10,(length - (Count + 1)));	// 0 - 9
				}
				else if ((ch[Count] >= 0x41) && (ch[Count] <= 0x46))
				{
					Ret = (ch[Count] - 0x37) * Pows(0x10,(length - (Count + 1)));	// A - F
				}
				else if ((ch[Count] >= 0x61) && (ch[Count] <= 0x66))
				{
					Ret = (ch[Count] - 0x57) * Pows(0x10,(length - (Count + 1)));	// a - f
				}
				else
				{
					Ret = 0xff;									// 不正な場合FF(255)を返します。
				}
	
				RetTmp = RetTmp + Ret;
			}
			return (uint)RetTmp;
		}
		
		//************************************************************ [初期化関数] ***
		public int GpibInit(out string TextRet)
		{
//			uint	Delim,Eoi;
			uint	Ret;
			uint	Timeout,Ifctime;
			string	csBuf;
			uint	Master;


			Ret = gpib.Exit();									// 2重初期化を防ぎます。
			Ret = gpib.Ini();									// GPIBを初期化します。
			csBuf = "GpIni";

			if ((Ret & 0xFF) != 0)
			{													// GpIniが正常に行えたかチェック。
				CheckRet("GpIni", Ret, out csBuf);
				TextRet = csBuf.ToString(); 
				return	1;
			}
			
			Master = 0;
			gpib.Boardsts(0x0a, out Master);					// マスタのアドレスを取得します。
			// マスタ、スレーブの判定
			if (Master == 0)
			{
				Ifctime = 1;									// ここでは100μsecにしています。
				Ret = gpib.Ifc(Ifctime);
				csBuf = "GpIfc";
				if ((Ret & 0xFF) != 0)
				{												// GpIfcが正常に行えたかチェック。
					CheckRet("GpIfc", Ret, out csBuf);
					TextRet = csBuf.ToString();
					return	1;
				}
				Ret = gpib.Ren();
				csBuf = "GpRen";
				if ((Ret & 0xFF) != 0)
				{												// GpRenが正常に行えたかチェック。
					CheckRet("GpRen", Ret, out csBuf);
					TextRet = csBuf.ToString();
					return	1;
				}
			}

//			Delim = 1;										// デリミタ：CR+LF
//			Eoi = 1;											// EOI	：使用する
//			Ret = gpib.Delim(Delim, Eoi);
//			csBuf = "GpDelim";
//			if ((Ret & 0xFF) != 0)
//			{													// GpDelimが正常に行えたかチェック。
//				CheckRet("GpDelim", Ret, out csBuf);
//				TextRet = csBuf;
//				return	1;
//			}
			Timeout = 10000;									// 10秒
			Ret = gpib.Timeout(Timeout);
			csBuf = "GpTimeout";
			if ((Ret & 0xFF) != 0)
			{													// GpTimeoutが正常に行えたかチェック。
				TextRet = csBuf.ToString();
				CheckRet("GpTimeout", Ret, out csBuf);
				return	1;
			}

			TextRet = "初期化を完了しました。";					// 正常終了
			return	0;
		}
		
		//******************************************************** [GpTalk()の応用] ***
		public int GpibPrint(uint DevAddr, string Str)
		{
			string	srbuf = new string(' ', 10000);				// 送信文字列
			uint	MyAddr;										// マイアドレス用
			uint[]	Cmd = new uint[16];							// コマンド用
			string	ErrText;									// エラー文字列
			uint	Ret;										// 戻り値
			int		RetTmp;										// 予備戻り値
			uint	srlen;										// 文字列の長さ

			Ret = gpib.Boardsts(0x08, out MyAddr);				// マイアドレス取得
			Cmd[0] = 2;											// コマンドの数
			Cmd[1] = MyAddr;									// マイアドレス(PC)
			Cmd[2] = DevAddr;									// スレーブ機器

			srlen = (uint)Str.Length;							// 長さを測定
			srbuf = Str;										// CString -> char
			Ret = gpib.Talk(Cmd, srlen, srbuf);					// 実際の送信

			if (Ret >= 3)
			{													// エラーチェック
				RetTmp = CheckRet("GpTalk", Ret, out ErrText);
				ErrText += " 継続しますか？";
				DialogResult Resul = MessageBox.Show(ErrText, null, MessageBoxButtons.YesNo);
				if (Resul == DialogResult.No)
				{
						return 1;								// 異常
				}
			}
			return 0;											// 正常
		}
		
		//****************************************************** [GpListen()の応用] ***
		public int GpibInput(uint DevAddr, StringBuilder Str)
		{
			uint	MyAddr, srlen;								// マイアドレス、文字列の長さ用
			uint[]	Cmd = new uint[16];							// コマンド用
			string	/*TmpStr, */ErrText;						// 予備文字列、エラー文字列
			uint	Ret;										// 戻り値
			int		RetTmp;										// 予備戻り値

			Ret = gpib.Boardsts(0x08, out MyAddr);				// マイアドレス取得
			Cmd[0] = 2;											// コマンドの数
			Cmd[1] = DevAddr;									// スレーブ機器
			Cmd[2] = MyAddr;									// マイアドレス(PC)
			srlen = 10000;										// 受信したデータの長さを測っています。
			Ret = gpib.Listen(Cmd, ref srlen, Str);				// 実際の送信
			if (Ret >= 3)
			{													// エラーチェック
				RetTmp = CheckRet("GpListen", Ret, out ErrText);
				ErrText += " 継続しますか？";
				DialogResult Resul = MessageBox.Show(ErrText, null, MessageBoxButtons.YesNo);
				if (Resul == DialogResult.No) return 1;			// 異常 = 1を返す
			}
			Str.Remove(Convert.ToInt32(srlen), Str.Length - Convert.ToInt32(srlen));	// HIOKI追加(不要文字削除)
			return 0;											// 正常 = 0を返す
		}
		
		//HIOKI追加
		//****************************************************** [GpListen()の応用] ***
		public int GpibInputHioki(uint DevAddr, StringBuilder Str)
		{
			StringBuilder Srbuf = new StringBuilder(10000);		// 文字列のバッファ
			uint	Srlen;										// 文字列の長さ
			uint	MyAddr;										// マイアドレス
			uint[]	Cmd = new uint[16];							// メッセージ(コマンド)
			string	ErrText;									// エラー文字列
			uint	Ret;										// 戻り値

			Ret = gpib.Boardsts(0x08, out MyAddr);				// マイアドレス取得
			Cmd[0] = 2;											// コマンドの数
			Cmd[1] = DevAddr;									// スレーブ機器
			Cmd[2] = MyAddr;									// マイアドレス(PC)

			Str.Clear();										// 初期化
			while (true)
			{
				Srlen = 10000;									// 最大受信数
				Ret = gpib.Listen(Cmd, ref Srlen, Srbuf);
				if (Ret <= 2) 
				{												// 受信終了
					Srbuf.Remove(Convert.ToInt32(Srlen), Srbuf.Length - Convert.ToInt32(Srlen));
					Str.Append(Srbuf);
					break;
				}
				else if (Ret == 128)
				{												// 受信データ域オーバー
					Srbuf.Remove(Convert.ToInt32(Srlen), Srbuf.Length - Convert.ToInt32(Srlen));
					Str.Append(Srbuf);
					Cmd[0] = 0;									// コマンドを出さずにGpListenします。
				}
				else
				{												// エラーチェック
					CheckRet("GpListen", Ret, out ErrText);
					MessageBox.Show(ErrText, null, MessageBoxButtons.OK);
					return 1;									// 異常 = 1を返す
				}
			}
			return 0;											// 正常 = 0を返す
		}
		
		// ************************************************* [ バイナリ受信用関数 ] ***
		public int GpibInputB(uint DevAddr, StringBuilder IntData)
		{
			StringBuilder	szData = new StringBuilder(10000);
			uint			Ret, MyAddr, srlen;
			int				RetTmp;
			uint[]			Cmd = new uint[8];
			string			ErrText = "";
			string			szDataVal;
			int				i;

			Ret = gpib.Delim(0, 1);								// デリミタを相手機器と合わせます。
			Ret = gpib.Boardsts(0x08, out MyAddr);				// マイアドレス取得
			Cmd[0] = 2;											// コマンドの数
			Cmd[1] = DevAddr;									// スレーブ機器
			Cmd[2] = MyAddr;									// マイアドレス(PC)
			srlen = 2;											// 受信したデータの長さを測っています。
			Ret = gpib.Listen(Cmd, ref srlen, szData);
			if (Ret != 128)
			{													// 途中でデータを切っているためRet=128になります。
				if (Ret >= 3)
				{												// エラーチェック
					RetTmp = CheckRet("GpListen", Ret, out ErrText);
					ErrText += " 継続しますか？";
					DialogResult Resul = MessageBox.Show(ErrText, null, MessageBoxButtons.YesNo);
					if (Resul == DialogResult.No)
					{
						return 1;							// 異常 = 1を返す
					}
				}
			}
			Cmd[0] = 0;
			szDataVal = szData.ToString().Substring(1, 1);
			for (i = 0; i < szDataVal.Length; i++)
			{
				if (Char.IsDigit(szDataVal, i) == false)
				{
					break;
				}
			}			
			szDataVal = szDataVal.Substring(0, i);
			if (i == 0)
			{
				srlen = 0;
			}
			else
			{
				srlen = uint.Parse(szDataVal);
			}

			Ret = gpib.Listen(Cmd, ref srlen, szData);
			
			for (i = 0; i < szData.Length; i++)
			{
				if (Char.IsDigit(szData.ToString(), i) == false)
				{
					break;
				}
			}
			szDataVal = szData.ToString().Substring(0, i);
			if (i == 0)
			{
				srlen = 1;
			}
			else
			{
				srlen = uint.Parse(szDataVal) + 1;
			}

			Ret = gpib.Listen(Cmd, ref srlen, IntData);
			Ret = gpib.Delim(3, 1);								// デリミタを戻します。
			return 0;
		}
		
		//****************************************************** [コマンド送信関数] ***
		public int GpibCommand(uint DevAddr)
		{
			uint[]	Cmd = new uint[16];
			string	ErrText;
			uint	Ret;
			int		RetTmp;

			Cmd[0] = 2;
			Cmd[1] = 0x3F;
			Cmd[2] = 0x5F;

			Ret = gpib.Comand(Cmd);

			if (Ret != 0)
			{
				RetTmp = CheckRet("GpComand", Ret, out ErrText);
				MessageBox.Show(ErrText, null, MessageBoxButtons.OK);
				return 1;
			}
			return 0;
		}
		
		//**************************************************************** [終了関数] ***
		public void GpibExit()
		{
			uint	Master;
			uint[]	Cmd = new uint[16];
			uint	Ret;

			Master = 0;
			Ret = gpib.Boardsts(0x0a, out Master);				// マスタのアドレスを取得します。
			if (Ret == 80)
			{
				return;											// 初期化されていない場合何もせずに戻ります。
			}
	
			if (Master == 0)
			{													// マスタの場合
				Cmd[0] = 2;										// コマンド(メッセージ)数
				Cmd[1] = 0x3f;									// アンリスン(リスナ解除)
				Cmd[2] = 0x5f;									// アントークン(トーカ解除)

				Ret = gpib.Comand(Cmd);							// コマンドを送信します。
				Ret = gpib.Resetren();							// 相手機器のリモートを解除します。
			}
	
			Ret = gpib.Exit();
		}
		
		// OPCのチェック ////////////////////////////////////////////////////////////////////////////////
		public void WaitOPC(uint Dev)
		{
			int				Ret;
			StringBuilder	RdData = new StringBuilder(10000);

			Ret = GpibPrint(Dev, "*OPC?");						// 工程作業が完了しているか
			Ret = GpibInput(Dev, RdData);
		}
		
		//**************************************************** [文字列を数字に変換] ***
		public void Str2Num(string str, uint str_len , ref int[] num, uint num_len)
		{
			int		i, j=0, cnt;
			string	start;

			start = str;
			cnt = 0;
			for (i = 0; i < str_len; i++)
			{
				/* string to integer */
				if (str[i] == ',')
				{
					if (i == 1)
					{
						start = str.Substring(j, i-j);
					}
					else
					{
						start = str.Substring(j, i-j);
					}
					try
					{
						num[cnt] = Convert.ToInt32(start);
					}
					catch (System.FormatException)
					{
						num[cnt] = 0;
					}
					j = i + 1;
					cnt++;
					if (cnt >= num_len)
					{
						break;
					}
				}
			}
			if (cnt >= num_len)
			{
				try
				{
					num[cnt] = Convert.ToInt32(start);
				}
				catch (System.FormatException)
				{
					num[cnt] = 0;
				}
			}
		}
		
		//********************************************************** [グラフを描画] ***
		// 第２引数でグラフ用ピクチャーダイアログを使用しています。
		public void DrawGraph(Control Picture, int[] num, uint num_len, int min, int max)
		{
			Rectangle	Rect = Picture.ClientRectangle;
			Pen			hPen_Black, hPen_Red, hPen_White;
			Point[]		point = new Point[4];
			int			x_max, y_max;
			int			x_width, y_width;
			float		x_unit, y_unit;
			uint		i;

			/* Initialize */
			x_max = Rect.Right;
			y_max = Rect.Bottom;
			Graphics g = Picture.CreateGraphics();

			hPen_Black	= new Pen(Color.Black, 1);				/* Black */
			hPen_Red	= new Pen(Color.Red, 1);				/* Red   */
			hPen_White	= new Pen(Color.White, 1);				/* White */	
			/* Draw Structure */
			SolidBrush whiteBrush = new SolidBrush(Color.White);
			g.FillRectangle(whiteBrush, Picture.ClientRectangle);
			for (i = 0; i <= 10; i++)
			{
				g.DrawLine(hPen_Black, (x_max / 10) * i, 0, (x_max / 10) * i, y_max);
			}
			for (i = 0; i <= 10; i++)
			{
				g.DrawLine(hPen_Black, 0, (y_max / 10) * i, x_max, (y_max / 10) * i); 
			}
			point[0].X = (x_max / 10) * 5 - 1;	point[0].Y = 0;
			point[1].X = (x_max / 10) * 5 + 1;	point[1].Y = 0;
			point[2].X = (x_max / 10) * 5 + 1;	point[2].Y = y_max;
			point[3].X = (x_max / 10) * 5 - 1;	point[3].Y = y_max;
			g.DrawLines(hPen_Red, point);
			point[0].X = 0;		point[0].Y = (y_max / 10) * 5 - 1;
			point[1].X = 0;		point[1].Y = (y_max / 10) * 5 + 1;
			point[2].X = x_max;	point[2].Y = (y_max / 10) * 5 + 1;
			point[3].X = x_max;	point[3].Y = (y_max / 10) * 5 - 1;
			g.DrawLines(hPen_Red, point);
			/* Draw Graph */
			x_width = (int)num_len;
			y_width = max - min;
			x_unit = (float)((float)x_max / (float)x_width);
			y_unit = (float)((float)y_max / (float)y_width);
			for (i = 0; i < (num_len - 1); i++)
			{
				g.DrawLine(hPen_Black, x_unit * i, (y_width - (num[i] - min)) * y_unit, x_unit * (i + 1), (y_width - (num[i+1] - min)) * y_unit);
			}
		}
	}
}
