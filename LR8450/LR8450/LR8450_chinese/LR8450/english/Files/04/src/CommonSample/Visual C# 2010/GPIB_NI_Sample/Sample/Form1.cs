//*******************************************************************************
//このプログラムは、計測器に接続してコマンドの送受信を行います。
//コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
//応答があるコマンド（?が含まれるコマンド）の場合は、テキストボックスに応答が表示されます。
//
//ナショナルインスツルメンツ(株)のNI-488.2 .NET Frameworkに含まれる
//NationalInstruments.CommonとNationalInstruments.NI4882をプロジェクトに追加し、
//参照設定しています。
//
//動作確認環境：Microsoft Visual Studio 2010
//				Version 10.0.40219.1 SP1Rel
//				Microsoft .NET Framework
//				Version 4.0.30319 SP1Rel
//				Microsoft Visual C# 2010
//				NI-488.2 Version 17.0
//*******************************************************************************

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using NationalInstruments.NI4882;	 //GPIBクラスの参照

namespace Sample
{
	public partial class Form1 : Form
	{
		//---------------------------------------------------------------------------------------
		//フォームが開かれたときの処理
		//---------------------------------------------------------------------------------------
		public Form1()
		{
			InitializeComponent();
			//ボタンとテキストボックスの有効/無効の処理
			Button1.Enabled = true;
			Button2.Enabled = false;
			Button3.Enabled = false;
			TextBox1.Enabled = true;
			TextBox2.Enabled = true;
			TextBox3.Enabled = false;
			TextBox4.ReadOnly = true;
			TextBox5.Enabled = true;
		}

		//---------------------------------------------------------------------------------------
		//ボタンを押したときの処理
		//---------------------------------------------------------------------------------------

		//「接続」ボタンを押したときの処理
		private void Button1_Click(object sender, EventArgs e)
		{
			//接続
			if (OpenInterface(TextBox1.Text, TextBox2.Text, TextBox5.Text) == false)
			{
				return;
			}

			//ボタンとテキストボックスの有効/無効の処理
			Button1.Enabled = false;
			Button2.Enabled = true;
			Button3.Enabled = true;
			TextBox1.Enabled = false;
			TextBox2.Enabled = false;
			TextBox3.Enabled = true;
			TextBox5.Enabled = false;
		}

		//「切断」ボタンを押したときの処理
		private void Button2_Click(object sender, EventArgs e)
		{
			//切断
			CloseInterface();

			//ボタンとテキストボックスの有効/無効の処理
			Button1.Enabled = true;
			Button2.Enabled = false;
			Button3.Enabled = false;
			TextBox1.Enabled = true;
			TextBox2.Enabled = true;
			TextBox3.Enabled = false;
			TextBox5.Enabled = true;
		}

		//「送受信」ボタンを押したときの処理
		private void Button3_Click(object sender, EventArgs e)
		{
			Button3.Enabled = false;

			TextBox4.AppendText("<< " + TextBox3.Text + "\r\n");						//ログ出力
			if (TextBox3.Text.Contains("?") == false)									//コマンドに?が含まれない場合は、コマンド送信のみ
			{				
				SendMsg(TextBox3.Text); 												//コマンド送信
			}																			//コマンドに?が含まれる場合は、コマンド送信と応答受信
			else
			{
				SendQueryMsg(TextBox3.Text, ReceiveTimeout);							//コマンド送信と応答受信
				TextBox4.AppendText(">> " + MsgBuf + "\r\n");							//ログ出力
			}

			Button3.Enabled = true;
		}

		//「クリア」ボタンを押したときの処理
		private void Button4_Click(object sender, EventArgs e)
		{
			//テキストボックスの消去
			TextBox4.Clear();
		}

		//---------------------------------------------------------------------------------------
		//通信インタフェース固有の処理
		//---------------------------------------------------------------------------------------

		//(0)クラス内変数
		private Device GpibDevice;														//GPIBデバイス
		private string MsgBuf = ""; 													//受信データ
		private long ReceiveTimeout = 0;												//受信タイムアウトデフォルト時間

		//(1)接続
		private bool OpenInterface(string BoardID, string PrimaryAddress, string timeout)
		{
			bool ret = false;

 			try
			{
				ReceiveTimeout = Convert.ToInt64(timeout) * 1000;
				GpibDevice = new Device(Convert.ToInt32(BoardID), Convert.ToByte(PrimaryAddress), 0, TimeoutValue.T10s);	//GPIBオブジェクトを作成
				ret = true;
			}
			catch(Exception e)
			{
				MessageBox.Show(e.Message);
			}

			return ret;
		}

		//(2)切断
		private bool CloseInterface()
		{
			bool ret = false;

			try
			{
				GpibDevice.Dispose();													//GPIBオブジェクトを廃棄
				ret = true;
			}
			catch(Exception e)
			{
				MessageBox.Show(e.Message);
			}

			return ret;
		}

		//(3)コマンド送信
		private bool SendMsg(string strMsg)
		{
			bool ret = false;

			try
			{
				strMsg += "\r\n";														//ターミネータ「CR+LF」を付加
				GpibDevice.Write(strMsg);												//送信バッファに書き込み
				ret = true;
			}
			catch(Exception e)
			{
				MsgBuf = "Error";
				MessageBox.Show(e.Message);
			}

			return ret;
		}

		//(4)受信
		private bool ReceiveMsg(long timeout)
		{
			bool ret = false;
			string rcv = "";
			StringBuilder buf = new StringBuilder();
			Stopwatch sw = new Stopwatch();

			MsgBuf = "";																//受信データをクリア
			sw.Start();																	//タイムアウト用ストップウォッチを開始
			//ターミネータ「LF」を受信するまでループ
			while(true)
			{
				try {
					rcv = "";
					rcv = GpibDevice.ReadString();										//受信バッファから読み取り
					rcv = rcv.Replace("\r", "");										//受信データ内の「CR」を削除
					if (rcv.IndexOf("\n") >= 0)											//ターミネータ「LF」を受信したら終了
					{
						rcv = rcv.Substring(0, rcv.IndexOf("\n"));						//受信データを「LF」の手前までで切り詰め
						buf.Append(rcv);												//受信データを保存
						MsgBuf = buf.ToString();
						break;
					}
					else
					{
						buf.Append(rcv);												//受信データを保存
					}
					//タイムアウト処理
					if (sw.ElapsedMilliseconds > timeout)
					{
						MsgBuf = "Timeout";
						MessageBox.Show(MsgBuf);
						return ret;
					}
				}
				catch (Exception e)
				{
					GpibStatusFlags statusFlag = GpibDevice.GetCurrentStatus();
					if ((statusFlag & GpibStatusFlags.IOComplete) == 0)
					{
						// IO Complete以外の例外
						MsgBuf = "Error";
						MessageBox.Show(e.Message);
						return ret;
					}
					else
					{
						// IO Complete例外
						rcv = rcv.Replace("\r", "");									//受信データ内の「CR」を削除
						if (rcv.IndexOf("\n") >= 0)										//ターミネータ「LF」を受信したら終了
						{
							rcv = rcv.Substring(0, rcv.IndexOf("\n"));					//受信データを「LF」の手前までで切り詰め
							buf.Append(rcv);											//受信データを保存
							MsgBuf = buf.ToString();
							break;
						}
						else
						{
							buf.Append(rcv);											//受信データを保存
						}
						//タイムアウト処理
						if (sw.ElapsedMilliseconds > timeout)
						{
							MsgBuf = "Timeout";
							MessageBox.Show(MsgBuf);
							return ret;
						}
					}
				}
			}
			sw.Stop();
			//ストップウォッチを停止
			ret = true;

			return ret;
		}

		//(5)コマンド送受信
		private bool SendQueryMsg(string strMsg, long timeout)
		{
			bool ret = false;

			ret = SendMsg(strMsg);														//コマンド送信
			if (ret)
			{
				ret = ReceiveMsg(timeout);												//送信が成功したら応答を受信
			}

			return ret;
		}

	}
}
