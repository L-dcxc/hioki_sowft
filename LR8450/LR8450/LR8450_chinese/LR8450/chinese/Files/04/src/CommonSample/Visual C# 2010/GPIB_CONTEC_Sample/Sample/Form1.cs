//*******************************************************************************
//このプログラムは、計測器に接続してコマンドの送受信を行います。
//コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
//応答があるコマンド（?が含まれるコマンド）の場合は、テキストボックスに応答が表示されます。
//
//(株)コンテックが公開しているGPIBのサンプルコードを参考にしています。
//サンプルコードのCgpibCs.csおよびSubFunc.csをプロジェクトに追加しています。
//追加したSubFunc.csにGpibInput関数を改造したGpibInputHioki関数を追加しています。
//
//動作確認環境：Microsoft Visual Studio 2010
//				Version 10.0.40219.1 SP1Rel
//				Microsoft .NET Framework
//				Version 4.0.30319 SP1Rel
//				Microsoft Visual C# 2010
//				API-GPIB(98/PC) Ver5.80
//*******************************************************************************

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using CgpibCs;
using CSubFuncCs;

namespace Sample
{
	public partial class Form1 : Form
	{
		public Form1()
		{
			InitializeComponent();
		}

		//---------------------------------------------------------------------------------------
		//フォームが開かれたときの処理
		//---------------------------------------------------------------------------------------
		private void Form1_Load(object sender, EventArgs e)
		{
			//ボタンとテキストボックスの有効/無効の処理
			Button1.Enabled = true;
			Button2.Enabled = false;
			Button3.Enabled = false;
			TextBox1.Enabled = false;
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
			if (OpenInterface(TextBox2.Text, TextBox5.Text) == false) {
				return;
			}

			//マイアドレスを表示
			TextBox1.Text = MyAddress.ToString();

			//ボタンとテキストボックスの有効/無効の処理
			Button1.Enabled = false;
			Button2.Enabled = true;
			Button3.Enabled = true;
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
			TextBox2.Enabled = true;
			TextBox3.Enabled = false;
			TextBox5.Enabled = true;
		}

		//「送受信」ボタンを押したときの処理
		private void Button3_Click(object sender, EventArgs e)
		{
			Button3.Enabled = false;

			TextBox4.AppendText("<< " + TextBox3.Text + "\r\n");						//ログ出力
			if (TextBox3.Text.Contains("?") == false) {									//コマンドに?が含まれない場合は、コマンド送信のみ
				SendMsg(TextBox3.Text); 												//コマンド送信
			}																			//コマンドに?が含まれる場合は、コマンド送信と応答受信
			else {
				SendQueryMsg(TextBox3.Text);											//コマンド送信と応答受信
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
		private Cgpib Gpib = new Cgpib();
		private CSubFunc SubFunc = new CSubFunc();
		private uint MyAddress = 0;														//マイアドレス
		private uint DeviceAddress = 0;													//機器アドレス
		private string MsgBuf = ""; 													//受信データ
		private uint ReceiveTimeout = 0;												//受信タイムアウト時間（ms）

		//(1)接続
		private bool OpenInterface(string primaryAddress, string timeout)
		{
			uint mode;
			uint eoi;
			uint delim;
			string message;
			uint ret;

			ret = (uint)SubFunc.GpibInit(out message);									//GPIBの初期化
			if (ret != 0) {
				MessageBox.Show(message);
				return false;
			}

			ret = Gpib.Boardsts(0x0a, out mode);										//マスタ/スレーブモードの読み出し
			if (ret != 0) {
				SubFunc.CheckRet("GpBoardsts", ret, out message);						//GpBoardstsの戻り値をチェック
				MessageBox.Show(message);
				return false;
			}
			if (mode != 0) {
				MessageBox.Show("この機器はマスタではありません。");
				return false;
			}

			ret = Gpib.Boardsts(0x08, out MyAddress);									//マイアドレスの取得
			if (ret != 0) {
				SubFunc.CheckRet("GpBoardsts", ret, out message);						//GpBoardstsの戻り値をチェック
				MessageBox.Show(message);
				return false;
			}

			eoi = 1;																	//0:使用しない / 1:使用する
			delim = 3;																	//0:未使用 / 1:CR+LF / 2:CR / 3:LF
			ret = Gpib.Delim(delim, eoi); 												//デリミタコード(EOI)送出の設定
			if (ret != 0) {
				SubFunc.CheckRet("GpDelim", ret, out message);							//GpDelimの戻り値をチェック
				MessageBox.Show(message);
				return false;
			}

			ReceiveTimeout = Convert.ToUInt32(timeout) * 1000;
			ret = Gpib.Timeout(ReceiveTimeout);											//タイムアウト時間の設定
			if (ret != 0) {
				SubFunc.CheckRet("GpTimeout", ret, out message); 						//GpTimeoutの戻り値をチェック
				MessageBox.Show(message);
				return false;
			}

			DeviceAddress = Convert.ToUInt32(primaryAddress);

			return true;
		}

		//(2)切断
		private bool CloseInterface()
		{
			SubFunc.GpibExit(); 														//GPIBの終了

			return true;
		}

		//(3)コマンド送信
		private bool SendMsg(string strMsg)
		{
			int ret;

			ret = SubFunc.GpibPrint(DeviceAddress, strMsg);								//送信データを書き込み
			if (ret != 0) {
				return false;
			}

			return true;
		}

		//(4)受信
		private bool ReceiveMsg()
		{
			StringBuilder buf = new StringBuilder(8388608);
			int ret;

			ret = SubFunc.GpibInputHioki(DeviceAddress, buf);							//受信バッファに読み込み
			if (ret != 0) {
				MsgBuf = "Error";
				return false;
			}
			MsgBuf = buf.ToString();													//受信データを保存

			return true;
		}

		//(5)コマンド送受信
		private bool SendQueryMsg(string strMsg)
		{
			bool ret;

			ret = SendMsg(strMsg);														//コマンド送信
			if (ret == true) {
				ret = ReceiveMsg(); 													//送信が成功したら応答を受信
			}

			return ret;
		}

	}
}
