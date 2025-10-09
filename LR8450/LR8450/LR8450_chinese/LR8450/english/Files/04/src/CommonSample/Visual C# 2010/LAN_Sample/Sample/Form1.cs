//*******************************************************************************
//このプログラムは、計測器に接続してコマンドの送受信を行います。
//コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
//応答があるコマンド（?が含まれるコマンド）の場合は、テキストボックスに応答が表示されます。
//
//動作確認環境：Microsoft Visual Studio 2010
//				Version 10.0.40219.1 SP1Rel
//				Microsoft .NET Framework
//				Version 4.0.30319 SP1Rel
//				Microsoft Visual C# 2010
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
		private System.Net.Sockets.TcpClient LanSocket; 								//LANソケット
		private string MsgBuf = ""; 													//受信データ
		private long ReceiveTimeout = 0;												//受信タイムアウト時間（ms）

		//(1)接続
		private bool OpenInterface(string ipaddress, string port, string timeout)
		{
			bool ret = false;
			System.Net.IPAddress ip = new System.Net.IPAddress(0);						//IPアドレス

 			try
			{
				ReceiveTimeout = Convert.ToInt64(timeout) * 1000;
				if (System.Net.IPAddress.TryParse(ipaddress, out ip))
				{
					LanSocket = new System.Net.Sockets.TcpClient();						//LANソケットオブジェクトを作成
					LanSocket.NoDelay = true;											//送信の遅延(Nagleアルゴリズム)を無効にする
					LanSocket.Connect(ip, Convert.ToInt32(port));						//接続
					ret = true;
				}
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
				LanSocket.Close();														//LANソケットクローズ
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
			byte[] SendBuffer = new byte[1024];

			try
			{
				strMsg += "\r\n";														//ターミネータ「CR+LF」を付加
				SendBuffer = System.Text.Encoding.Default.GetBytes(strMsg); 			//バイト型に変換
				LanSocket.GetStream().Write(SendBuffer, 0, SendBuffer.Length);			//送信バッファに書き込み
				ret = true;
			}
			catch(Exception e)
			{
				MessageBox.Show(e.Message);
			}

			return ret;
		}

		//(4)受信
		private bool ReceiveMsg(long timeout)
		{
			bool ret = false;
			byte[] ary = new byte[65536];
			string rcv;
			int len;
			StringBuilder buf = new StringBuilder();
			Stopwatch sw = new Stopwatch();
		 
			try
			{
				MsgBuf = "";															//受信データをクリア

				sw.Start();																//タイムアウト用ストップウォッチを開始
				//ターミネータ「LF」を受信するまでループ
				while(true){
					if (LanSocket.GetStream().DataAvailable == true)					//受信バッファにデータがあれば読み取り
					{
						len = LanSocket.GetStream().Read(ary, 0, ary.Length);			//受信バッファから読み取り
						rcv = Encoding.Default.GetString(ary).Substring(0, len);
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
					}
					//タイムアウト処理
					if (sw.ElapsedMilliseconds > timeout)
					{
						MsgBuf = "Timeout";
						MessageBox.Show(MsgBuf);
						return ret;
					}
				}
				sw.Stop();																//ストップウォッチを停止
				ret = true;
			}
			catch(Exception e)
			{
				MsgBuf = "Error";
				MessageBox.Show(e.Message);
			}

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
