namespace Sample
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージ リソースが破棄される場合 true、破棄されない場合は false です。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
			this.TextBox2 = new System.Windows.Forms.TextBox();
			this.Label3 = new System.Windows.Forms.Label();
			this.Button4 = new System.Windows.Forms.Button();
			this.Label2 = new System.Windows.Forms.Label();
			this.Button3 = new System.Windows.Forms.Button();
			this.Button2 = new System.Windows.Forms.Button();
			this.Button1 = new System.Windows.Forms.Button();
			this.Label1 = new System.Windows.Forms.Label();
			this.TextBox4 = new System.Windows.Forms.TextBox();
			this.TextBox3 = new System.Windows.Forms.TextBox();
			this.TextBox1 = new System.Windows.Forms.TextBox();
			this.Label5 = new System.Windows.Forms.Label();
			this.TextBox5 = new System.Windows.Forms.TextBox();
			this.Label4 = new System.Windows.Forms.Label();
			this.SuspendLayout();
			// 
			// TextBox2
			// 
			this.TextBox2.Location = new System.Drawing.Point(178, 18);
			this.TextBox2.Name = "TextBox2";
			this.TextBox2.Size = new System.Drawing.Size(50, 19);
			this.TextBox2.TabIndex = 3;
			this.TextBox2.Text = "1";
			this.TextBox2.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			// 
			// Label3
			// 
			this.Label3.AutoSize = true;
			this.Label3.Location = new System.Drawing.Point(17, 101);
			this.Label3.Name = "Label3";
			this.Label3.Size = new System.Drawing.Size(40, 12);
			this.Label3.TabIndex = 7;
			this.Label3.Text = "コマンド";
			// 
			// Button4
			// 
			this.Button4.Location = new System.Drawing.Point(313, 92);
			this.Button4.Name = "Button4";
			this.Button4.Size = new System.Drawing.Size(73, 30);
			this.Button4.TabIndex = 13;
			this.Button4.Text = "クリア";
			this.Button4.UseVisualStyleBackColor = true;
			this.Button4.Click += new System.EventHandler(this.Button4_Click);
			// 
			// Label2
			// 
			this.Label2.AutoSize = true;
			this.Label2.Location = new System.Drawing.Point(107, 21);
			this.Label2.Name = "Label2";
			this.Label2.Size = new System.Drawing.Size(65, 12);
			this.Label2.TabIndex = 2;
			this.Label2.Text = "機器アドレス";
			// 
			// Button3
			// 
			this.Button3.Location = new System.Drawing.Point(313, 52);
			this.Button3.Name = "Button3";
			this.Button3.Size = new System.Drawing.Size(73, 30);
			this.Button3.TabIndex = 12;
			this.Button3.Text = "送受信";
			this.Button3.UseVisualStyleBackColor = true;
			this.Button3.Click += new System.EventHandler(this.Button3_Click);
			// 
			// Button2
			// 
			this.Button2.Location = new System.Drawing.Point(313, 12);
			this.Button2.Name = "Button2";
			this.Button2.Size = new System.Drawing.Size(73, 30);
			this.Button2.TabIndex = 11;
			this.Button2.Text = "切断";
			this.Button2.UseVisualStyleBackColor = true;
			this.Button2.Click += new System.EventHandler(this.Button2_Click);
			// 
			// Button1
			// 
			this.Button1.Location = new System.Drawing.Point(234, 12);
			this.Button1.Name = "Button1";
			this.Button1.Size = new System.Drawing.Size(73, 30);
			this.Button1.TabIndex = 10;
			this.Button1.Text = "接続";
			this.Button1.UseVisualStyleBackColor = true;
			this.Button1.Click += new System.EventHandler(this.Button1_Click);
			// 
			// Label1
			// 
			this.Label1.AutoSize = true;
			this.Label1.Location = new System.Drawing.Point(1, 21);
			this.Label1.Name = "Label1";
			this.Label1.Size = new System.Drawing.Size(59, 12);
			this.Label1.TabIndex = 0;
			this.Label1.Text = "マイアドレス";
			// 
			// TextBox4
			// 
			this.TextBox4.Location = new System.Drawing.Point(12, 133);
			this.TextBox4.Multiline = true;
			this.TextBox4.Name = "TextBox4";
			this.TextBox4.ScrollBars = System.Windows.Forms.ScrollBars.Both;
			this.TextBox4.Size = new System.Drawing.Size(295, 164);
			this.TextBox4.TabIndex = 9;
			this.TextBox4.WordWrap = false;
			// 
			// TextBox3
			// 
			this.TextBox3.Location = new System.Drawing.Point(63, 98);
			this.TextBox3.Name = "TextBox3";
			this.TextBox3.Size = new System.Drawing.Size(244, 19);
			this.TextBox3.TabIndex = 8;
			this.TextBox3.Text = "*IDN?";
			// 
			// TextBox1
			// 
			this.TextBox1.Location = new System.Drawing.Point(63, 18);
			this.TextBox1.Name = "TextBox1";
			this.TextBox1.Size = new System.Drawing.Size(38, 19);
			this.TextBox1.TabIndex = 1;
			this.TextBox1.Text = "0";
			this.TextBox1.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			// 
			// Label5
			// 
			this.Label5.AutoSize = true;
			this.Label5.Location = new System.Drawing.Point(232, 61);
			this.Label5.Name = "Label5";
			this.Label5.Size = new System.Drawing.Size(17, 12);
			this.Label5.TabIndex = 6;
			this.Label5.Text = "秒";
			// 
			// TextBox5
			// 
			this.TextBox5.Location = new System.Drawing.Point(178, 58);
			this.TextBox5.Name = "TextBox5";
			this.TextBox5.Size = new System.Drawing.Size(48, 19);
			this.TextBox5.TabIndex = 5;
			this.TextBox5.Text = "1";
			this.TextBox5.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			// 
			// Label4
			// 
			this.Label4.AutoSize = true;
			this.Label4.Location = new System.Drawing.Point(90, 61);
			this.Label4.Name = "Label4";
			this.Label4.Size = new System.Drawing.Size(82, 12);
			this.Label4.TabIndex = 4;
			this.Label4.Text = "受信タイムアウト";
			// 
			// Form1
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(396, 308);
			this.Controls.Add(this.Label5);
			this.Controls.Add(this.TextBox5);
			this.Controls.Add(this.Label4);
			this.Controls.Add(this.TextBox2);
			this.Controls.Add(this.Label3);
			this.Controls.Add(this.Button4);
			this.Controls.Add(this.Label2);
			this.Controls.Add(this.Button3);
			this.Controls.Add(this.Button2);
			this.Controls.Add(this.Button1);
			this.Controls.Add(this.Label1);
			this.Controls.Add(this.TextBox4);
			this.Controls.Add(this.TextBox3);
			this.Controls.Add(this.TextBox1);
			this.Name = "Form1";
			this.Text = "Form1";
			this.Load += new System.EventHandler(this.Form1_Load);
			this.ResumeLayout(false);
			this.PerformLayout();

        }

        #endregion

        internal System.Windows.Forms.TextBox TextBox2;
        internal System.Windows.Forms.Label Label3;
        internal System.Windows.Forms.Button Button4;
        internal System.Windows.Forms.Label Label2;
        internal System.Windows.Forms.Button Button3;
        internal System.Windows.Forms.Button Button2;
        internal System.Windows.Forms.Button Button1;
        internal System.Windows.Forms.Label Label1;
        internal System.Windows.Forms.TextBox TextBox4;
        internal System.Windows.Forms.TextBox TextBox3;
        internal System.Windows.Forms.TextBox TextBox1;
		internal System.Windows.Forms.Label Label5;
		internal System.Windows.Forms.TextBox TextBox5;
		internal System.Windows.Forms.Label Label4;

    }
}

