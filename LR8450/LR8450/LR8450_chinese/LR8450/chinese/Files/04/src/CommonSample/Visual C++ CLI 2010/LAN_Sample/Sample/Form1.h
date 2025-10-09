//*******************************************************************************
//このプログラムは、計測器に接続してコマンドの送受信を行います。
//コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
//応答があるコマンド（?が含まれるコマンド）の場合は、テキストボックスに応答が表示されます。
//
//動作確認環境：Microsoft Visual Studio 2010
//				Version 10.0.40219.1 SP1Rel
//				Microsoft .NET Framework
//				Version 4.0.30319 SP1Rel
//				Microsoft Visual C++ 2010
//*******************************************************************************

#pragma once

namespace Sample {

	using namespace System;
	using namespace System::Collections;
	using namespace System::ComponentModel;
	using namespace System::Data;
	using namespace System::Diagnostics;
	using namespace System::Drawing;
	using namespace System::Text;
	using namespace System::Windows::Forms;

	/// <summary>
	/// Form1 の概要
	/// </summary>
	public ref class Form1 : public System::Windows::Forms::Form
	{
	public:
		Form1(void)
		{
			//---------------------------------------------------------------------------------------
			//フォームが開かれたときの処理
			//---------------------------------------------------------------------------------------
			InitializeComponent();
			this->button1->Enabled = true;
			this->button2->Enabled = false;
			this->button3->Enabled = false;
			this->textBox1->Enabled = true;
			this->textBox2->Enabled = true;
			this->textBox3->Enabled = false;
			this->textBox4->ReadOnly = true;
			this->textBox5->Enabled = true;
		}

	protected:
		/// <summary>
		/// 使用中のリソースをすべてクリーンアップします。
		/// </summary>
		~Form1()
		{
			if (components)
			{
				delete components;
			}
		}
	private: System::Windows::Forms::Button^  button1;
	private: System::Windows::Forms::Button^  button2;
	private: System::Windows::Forms::Button^  button3;
	private: System::Windows::Forms::Button^  button4;
	private: System::Windows::Forms::TextBox^  textBox1;
	private: System::Windows::Forms::TextBox^  textBox2;
	private: System::Windows::Forms::TextBox^  textBox3;
	private: System::Windows::Forms::TextBox^  textBox4;
	private: System::Windows::Forms::Label^  label1;
	private: System::Windows::Forms::Label^  label2;
	private: System::Windows::Forms::Label^  label3;
	private: System::Windows::Forms::Label^  Label5;
	private: System::Windows::Forms::TextBox^  textBox5;
	private: 

	private: System::Windows::Forms::Label^  Label4;
	protected: 

	private:
		/// <summary>
		/// 必要なデザイナー変数です。
		/// </summary>
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
		/// <summary>
		/// デザイナー サポートに必要なメソッドです。このメソッドの内容を
		/// コード エディターで変更しないでください。
		/// </summary>
		void InitializeComponent(void)
		{
			this->button1 = (gcnew System::Windows::Forms::Button());
			this->button2 = (gcnew System::Windows::Forms::Button());
			this->button3 = (gcnew System::Windows::Forms::Button());
			this->button4 = (gcnew System::Windows::Forms::Button());
			this->textBox1 = (gcnew System::Windows::Forms::TextBox());
			this->textBox2 = (gcnew System::Windows::Forms::TextBox());
			this->textBox3 = (gcnew System::Windows::Forms::TextBox());
			this->textBox4 = (gcnew System::Windows::Forms::TextBox());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->label2 = (gcnew System::Windows::Forms::Label());
			this->label3 = (gcnew System::Windows::Forms::Label());
			this->Label5 = (gcnew System::Windows::Forms::Label());
			this->textBox5 = (gcnew System::Windows::Forms::TextBox());
			this->Label4 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// button1
			// 
			this->button1->Location = System::Drawing::Point(234, 12);
			this->button1->Name = L"button1";
			this->button1->Size = System::Drawing::Size(73, 30);
			this->button1->TabIndex = 10;
			this->button1->Text = L"接続";
			this->button1->UseVisualStyleBackColor = true;
			this->button1->Click += gcnew System::EventHandler(this, &Form1::button1_Click);
			// 
			// button2
			// 
			this->button2->Location = System::Drawing::Point(313, 12);
			this->button2->Name = L"button2";
			this->button2->Size = System::Drawing::Size(73, 30);
			this->button2->TabIndex = 11;
			this->button2->Text = L"切断";
			this->button2->UseVisualStyleBackColor = true;
			this->button2->Click += gcnew System::EventHandler(this, &Form1::button2_Click);
			// 
			// button3
			// 
			this->button3->Location = System::Drawing::Point(313, 52);
			this->button3->Name = L"button3";
			this->button3->Size = System::Drawing::Size(73, 30);
			this->button3->TabIndex = 12;
			this->button3->Text = L"送受信";
			this->button3->UseVisualStyleBackColor = true;
			this->button3->Click += gcnew System::EventHandler(this, &Form1::button3_Click);
			// 
			// button4
			// 
			this->button4->Location = System::Drawing::Point(313, 92);
			this->button4->Name = L"button4";
			this->button4->Size = System::Drawing::Size(73, 30);
			this->button4->TabIndex = 13;
			this->button4->Text = L"クリア";
			this->button4->UseVisualStyleBackColor = true;
			this->button4->Click += gcnew System::EventHandler(this, &Form1::button4_Click);
			// 
			// textBox1
			// 
			this->textBox1->Location = System::Drawing::Point(69, 18);
			this->textBox1->Name = L"textBox1";
			this->textBox1->Size = System::Drawing::Size(76, 19);
			this->textBox1->TabIndex = 1;
			this->textBox1->Text = L"192.168.0.1";
			// 
			// textBox2
			// 
			this->textBox2->Location = System::Drawing::Point(190, 18);
			this->textBox2->Name = L"textBox2";
			this->textBox2->Size = System::Drawing::Size(38, 19);
			this->textBox2->TabIndex = 3;
			this->textBox2->Text = L"3500";
			this->textBox2->TextAlign = System::Windows::Forms::HorizontalAlignment::Right;
			// 
			// textBox3
			// 
			this->textBox3->Location = System::Drawing::Point(69, 98);
			this->textBox3->Name = L"textBox3";
			this->textBox3->Size = System::Drawing::Size(238, 19);
			this->textBox3->TabIndex = 8;
			this->textBox3->Text = L"*IDN\?";
			// 
			// textBox4
			// 
			this->textBox4->Location = System::Drawing::Point(12, 133);
			this->textBox4->Multiline = true;
			this->textBox4->Name = L"textBox4";
			this->textBox4->ScrollBars = System::Windows::Forms::ScrollBars::Both;
			this->textBox4->Size = System::Drawing::Size(295, 164);
			this->textBox4->TabIndex = 9;
			this->textBox4->WordWrap = false;
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->Location = System::Drawing::Point(12, 21);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(51, 12);
			this->label1->TabIndex = 0;
			this->label1->Text = L"IPアドレス";
			// 
			// label2
			// 
			this->label2->AutoSize = true;
			this->label2->Location = System::Drawing::Point(151, 21);
			this->label2->Name = L"label2";
			this->label2->Size = System::Drawing::Size(33, 12);
			this->label2->TabIndex = 2;
			this->label2->Text = L"ポート";
			// 
			// label3
			// 
			this->label3->AutoSize = true;
			this->label3->Location = System::Drawing::Point(23, 101);
			this->label3->Name = L"label3";
			this->label3->Size = System::Drawing::Size(40, 12);
			this->label3->TabIndex = 7;
			this->label3->Text = L"コマンド";
			// 
			// Label5
			// 
			this->Label5->AutoSize = true;
			this->Label5->Location = System::Drawing::Point(234, 61);
			this->Label5->Name = L"Label5";
			this->Label5->Size = System::Drawing::Size(17, 12);
			this->Label5->TabIndex = 6;
			this->Label5->Text = L"秒";
			// 
			// textBox5
			// 
			this->textBox5->Location = System::Drawing::Point(190, 58);
			this->textBox5->Name = L"textBox5";
			this->textBox5->Size = System::Drawing::Size(38, 19);
			this->textBox5->TabIndex = 5;
			this->textBox5->Text = L"1";
			this->textBox5->TextAlign = System::Windows::Forms::HorizontalAlignment::Right;
			// 
			// Label4
			// 
			this->Label4->AutoSize = true;
			this->Label4->Location = System::Drawing::Point(102, 61);
			this->Label4->Name = L"Label4";
			this->Label4->Size = System::Drawing::Size(82, 12);
			this->Label4->TabIndex = 4;
			this->Label4->Text = L"受信タイムアウト";
			// 
			// Form1
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 12);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(396, 308);
			this->Controls->Add(this->Label5);
			this->Controls->Add(this->textBox5);
			this->Controls->Add(this->Label4);
			this->Controls->Add(this->label3);
			this->Controls->Add(this->label2);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->textBox4);
			this->Controls->Add(this->textBox3);
			this->Controls->Add(this->textBox2);
			this->Controls->Add(this->textBox1);
			this->Controls->Add(this->button4);
			this->Controls->Add(this->button3);
			this->Controls->Add(this->button2);
			this->Controls->Add(this->button1);
			this->Name = L"Form1";
			this->Text = L"Form1";
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
	//---------------------------------------------------------------------------------------
	//ボタンを押したときの処理
	//---------------------------------------------------------------------------------------

	//「接続」ボタンを押したときの処理
	private: System::Void button1_Click(System::Object^  sender, System::EventArgs^  e) {
				 //接続
				 if(OpenInterface(textBox1->Text, textBox2->Text, textBox5->Text) == false){
					 return;
				 }

				 //ボタンとテキストボックスの有効/無効の処理
				 this->button1->Enabled = false;
				 this->button2->Enabled = true;
				 this->button3->Enabled = true;
				 this->textBox1->Enabled = false;
				 this->textBox2->Enabled = false;
				 this->textBox3->Enabled = true;
				 this->textBox5->Enabled = false;
			 }

	//「切断」ボタンを押したときの処理
	private: System::Void button2_Click(System::Object^  sender, System::EventArgs^  e) {
				 //切断
				 CloseInterface();

				 //ボタンとテキストボックスの有効/無効の処理
				 this->button1->Enabled = true;
				 this->button2->Enabled = false;
				 this->button3->Enabled = false;
				 this->textBox1->Enabled = true;
				 this->textBox2->Enabled = true;
				 this->textBox3->Enabled = false;
				 this->textBox5->Enabled = true;
			 }

	//「送受信」ボタンを押したときの処理
	private: System::Void button3_Click(System::Object^  sender, System::EventArgs^  e) {
				 button3->Enabled = false;

				 textBox4->AppendText("<< " + textBox3->Text + "\r\n");					//ログ出力
				 if(textBox3->Text->Contains("?") == false){							//コマンドに?が含まれない場合は、コマンド送信のみ
					 SendMsg(textBox3->Text);											//コマンド送信
				 }																		//コマンドに?が含まれる場合は、コマンド送信と応答受信
				 else
				 {
					 SendQueryMsg(textBox3->Text, ReceiveTimeout);						//コマンド送信と応答受信
					 textBox4->AppendText(">> " + MsgBuf + "\r\n"); 					//ログ出力
				 }

				 button3->Enabled = true;
			 }

	//「クリア」ボタンを押したときの処理
	private: System::Void button4_Click(System::Object^  sender, System::EventArgs^  e) {
				 //テキストボックスの消去
				 textBox4->Clear();
			 }

	//---------------------------------------------------------------------------------------
	//通信インタフェース固有の処理
	//---------------------------------------------------------------------------------------

	//(0)クラス内変数
	private: System::Net::Sockets::TcpClient^ LanSocket;								//LANソケット
	private: String^ MsgBuf;															//受信データ
	private: Int64 ReceiveTimeout;														//受信タイムアウトデフォルト時間（ms）

	//(1)接続
	private: Boolean OpenInterface(String^ ipaddress, String^ port, String^ timeout) {
				 Boolean ret = false;
				 System::Net::IPAddress^ ip = gcnew System::Net::IPAddress(0);			//IPアドレス

				 try
				 {
					 ReceiveTimeout = Convert::ToInt64(timeout) * 1000;
					 if (System::Net::IPAddress::TryParse(ipaddress, ip))
					 {
						 LanSocket = gcnew System::Net::Sockets::TcpClient();			//LANソケットオブジェクトを作成
						 LanSocket->NoDelay = true; 									//送信の遅延(Nagleアルゴリズム)を無効にする
						 LanSocket->Connect(ip, Convert::ToInt32(port));				//接続
					 }
					 ret = true;
				 }
				 catch(Exception^ e)
				 {
					 MessageBox::Show(e->Message);
				 }

				 return ret;
			 }

	//(2)切断
	private: Boolean CloseInterface() {
				 Boolean ret = false;

				 try
				 {
					LanSocket->Close();													//LANソケットクローズ
					 ret = true;
				 }
				 catch(Exception^ e)
				 {
					 MessageBox::Show(e->Message);
				 }

				 return ret;
			 }

	//(3)コマンド送信
	private: Boolean SendMsg(String^ strMsg) {
				 Boolean ret = false;
				 array<Byte>^ SendBuffer = gcnew array<Byte>(1024);

				 try
				 {
					 strMsg += "\r\n";													//ターミネータ「CR+LF」を付加
					 SendBuffer = System::Text::Encoding::Default->GetBytes(strMsg);	//バイト型に変換
					 LanSocket->GetStream()->Write(SendBuffer, 0, SendBuffer->Length);	//送信バッファに書き込み
					 ret = true;
				 }
				 catch(Exception^ e)
				 {
					 MessageBox::Show(e->Message);
				 }

				 return ret;
			 }

	//(4)受信
	private: Boolean ReceiveMsg(Int64 timeout) {
				 Boolean ret = false;
				 array<Byte>^ ary = gcnew array<Byte>(65536);
				 String^ rcv;
				 Int32 len;
				 StringBuilder^ buf = gcnew StringBuilder();
				 Stopwatch^ sw = gcnew Stopwatch();
				 
				 try
				 {
					 MsgBuf = "";														//受信データをクリア

					 sw->Start();														//タイムアウト用ストップウォッチを開始
					 //ターミネータ「LF」を受信するまでループ
					 while(true){
						 if (LanSocket->GetStream()->DataAvailable == true) 			//受信バッファにデータがあれば読み取り
						 {
							 len = LanSocket->GetStream()->Read(ary, 0, ary->Length);	//受信バッファから読み取り
							 rcv = Encoding::Default->GetString(ary)->Substring(0, len);
							 rcv = rcv->Replace("\r", "");								//受信データ内の「CR」を削除
							 if (rcv->IndexOf("\n") >= 0)								//ターミネータ「LF」を受信したら終了
							 {
								 rcv = rcv->Substring(0, rcv->IndexOf("\n"));			//受信データを「LF」の手前までで切り詰め
								 buf->Append(rcv);										//受信データを保存
								 MsgBuf = buf->ToString();
								 break;
							 }
							 else
							 {
								 buf->Append(rcv);										//受信データを保存
							 }
						 }
						 //タイムアウト処理
						 if (sw->ElapsedMilliseconds > Convert::ToInt64(timeout))
						 {
							 MsgBuf = "Timeout";
							 MessageBox::Show(MsgBuf);
							 return ret;
						 }
					 }
					 sw->Stop();														//ストップウォッチを停止
					 ret = true;
				 }
				 catch(Exception^ e)
				 {
					 MsgBuf = "Error";
					 MessageBox::Show(e->Message);
					 ret = false;
				 }

				 return ret;
			 }

	//(5)コマンド送受信
	private: Boolean SendQueryMsg(String^ strMsg, Int64 timeout) {
				 Boolean ret = false;

				 ret = SendMsg(strMsg); 												//コマンド送信
				 if (ret)
				 {
					 ret = ReceiveMsg(timeout);											//送信が成功したら応答を受信
				 }

				 return ret;
			 }

};
}

