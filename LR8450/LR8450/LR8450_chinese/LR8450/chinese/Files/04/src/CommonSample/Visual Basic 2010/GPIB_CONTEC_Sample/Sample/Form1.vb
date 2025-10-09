'*******************************************************************************
'このプログラムは、計測器に接続してコマンドの送受信を行います。
'コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
'応答があるコマンド（?が含まれるコマンド）の場合は、テキストボックスに応答が表示されます。
'
'(株)コンテックが公開しているGPIBのサンプルコードを参考にしています。
'サンプルコードのGpibvb.vbおよびSubFunc.vbをプロジェクトに追加しています。
'追加したGpibvb.vbにGpibInput関数を改造したGpibInputHioki関数を追加しています。
'
'動作確認環境：Microsoft Visual Studio 2010
'              Version 10.0.40219.1 SP1Rel
'              Microsoft .NET Framework
'              Version 4.0.30319 SP1Rel
'              Microsoft Visual Basic 2010
'              API-GPIB(98/PC) Ver5.80
'*******************************************************************************
Imports System.Runtime.InteropServices
Imports System.Text

Public Class Form1
    '---------------------------------------------------------------------------------------
    'フォームが開かれたときの処理
    '---------------------------------------------------------------------------------------
    Private Sub Form1_Load(sender As Object, e As System.EventArgs) Handles Me.Load
        'ボタンとテキストボックスの有効/無効の処理
        Button1.Enabled = True
        Button2.Enabled = False
        Button3.Enabled = False
        TextBox1.Enabled = False
        TextBox2.Enabled = True
        TextBox3.Enabled = False
        TextBox4.ReadOnly = True
        TextBox5.Enabled = True

        'PinnedハンドルをCmdに分配する
        If gChCmd.IsAllocated = False Then
            gChCmd = GCHandle.Alloc(Cmd, GCHandleType.Pinned)
        End If
        'Pinnedハンドルでオブジェクトのアドレスを取得
        pCmd = gChCmd.AddrOfPinnedObject()
    End Sub

    '---------------------------------------------------------------------------------------
    'ボタンを押したときの処理
    '---------------------------------------------------------------------------------------

    '「接続」ボタンを押したときの処理
    Private Sub Button1_Click(sender As System.Object, e As System.EventArgs) Handles Button1.Click
        '接続
        If OpenInterface(TextBox2.Text, TextBox5.Text) = False Then
            Exit Sub
        End If

        'マイアドレスを表示
        TextBox1.Text = MyAddress.ToString()

        'ボタンとテキストボックスの有効/無効の処理
        Button1.Enabled = False
        Button2.Enabled = True
        Button3.Enabled = True
        TextBox2.Enabled = False
        TextBox3.Enabled = True
        TextBox5.Enabled = False
    End Sub

    '「切断」ボタンを押したときの処理
    Private Sub Button2_Click(sender As System.Object, e As System.EventArgs) Handles Button2.Click
        '切断
        CloseInterface()

        'ボタンとテキストボックスの有効/無効の処理
        Button1.Enabled = True
        Button2.Enabled = False
        Button3.Enabled = False
        TextBox2.Enabled = True
        TextBox3.Enabled = False
        TextBox5.Enabled = True
    End Sub

    '「送受信」ボタンを押したときの処理
    Private Sub Button3_Click(sender As System.Object, e As System.EventArgs) Handles Button3.Click
        Button3.Enabled = False

        TextBox4.AppendText("<< " + TextBox3.Text + vbCrLf)                             'ログ出力
        If InStr(TextBox3.Text, "?") = 0 Then                                           'コマンドに?が含まれない場合は、コマンド送信のみ
            SendMsg(TextBox3.Text)                                                      'コマンド送信
        Else                                                                            'コマンドに?が含まれる場合は、コマンド送信と応答受信
            SendQueryMsg(TextBox3.Text)                                                 'コマンド送信と応答受信
            TextBox4.AppendText(">> " + MsgBuf + vbCrLf)                                'ログ出力
        End If

        Button3.Enabled = True
    End Sub

    '「クリア」ボタンを押したときの処理
    Private Sub Button4_Click(sender As System.Object, e As System.EventArgs) Handles Button4.Click
        'テキストボックスの消去
        TextBox4.Clear()
    End Sub

    '---------------------------------------------------------------------------------------
    '通信インタフェース固有の処理
    '---------------------------------------------------------------------------------------

    '(0)クラス内変数
    Private MyAddress As Integer = 0                                                    'マイアドレス
    Private DeviceAddress As Integer = 0                                                '機器アドレス
    Private MsgBuf As String = ""                                                       '受信データ
    Private ReceiveTimeout As Long = 0                                                  '受信タイムアウト時間（ms）
    Private gChCmd As GCHandle                                                          'Cmd配列用GCHandle

    '(1)接続
    Private Function OpenInterface(ByVal PrimaryAddress As String, ByVal Timeout As String) As Boolean
        Dim mode As Integer
        Dim eoi As Integer
        Dim delim As Integer
        Dim message As String = ""
        Dim ret As Integer

        ret = GpibInit(message)                                                         'GPIBの初期化
        If ret <> 0 Then
            MsgBox(message)
            Return False
        End If

        ret = GpBoardsts(&HAS, mode)                                                    'マスタ/スレーブモードの読み出し
        If ret <> 0 Then
            CheckRet("GpBoardsts", ret, message)                                        'GpBoardstsの戻り値をチェック
            MsgBox(message)
            Return False
        End If
        If mode <> 0 Then
            message = "この機器はマスタではありません｡設定を確認してください｡"
            MsgBox(message)
            Return False
        End If

        ret = GpBoardsts(&H8S, MyAddress)                                               'マイアドレスの取得
        If mode <> 0 Then
            CheckRet("GpBoardsts", ret, message)                                        'GpBoardstsの戻り値をチェック
            MsgBox(message)
            Return False
        End If

        eoi = 1                                                                         '0:使用しない / 1:使用する
        delim = 3                                                                       '0:未使用 / 1:CR+LF / 2:CR / 3:LF
        ret = GpDelim(delim, eoi)                                                       'デリミタコード(EOI)送出の設定
        If ret <> 0 Then
            CheckRet("GpDelim", ret, message)                                           'GpDelimの戻り値をチェック
            MsgBox(message)
            Return False
        End If

        ReceiveTimeout = CInt(Timeout) * 1000
        ret = GpTimeout(ReceiveTimeout)                                                 'タイムアウト時間の設定
        If ret <> 0 Then
            CheckRet("GpTimeout", ret, message)                                         'GpTimeoutの戻り値をチェック
            MsgBox(message)
            Return False
        End If

        DeviceAddress = CInt(PrimaryAddress)

        Return True
    End Function

    '(2)切断
    Private Function CloseInterface() As Boolean
        GpibExit()                                                                      'GPIBの終了

        Return True
    End Function

    '(3)コマンド送信
    Private Function SendMsg(ByVal strMsg As String) As Boolean
        Dim ret As Integer

        ret = GpibPrint(DeviceAddress, strMsg)                                          '送信データを書き込み
        If ret <> 0 Then
            Return False
        End If

        Return True
    End Function

    '(4)受信
    Private Function ReceiveMsg() As Boolean
        Dim buf As New StringBuilder(8388608)
        Dim ret As Integer

        ret = GpibInputHioki(DeviceAddress, buf)                                        '受信バッファに読み込み
        If ret <> 0 Then
            MsgBuf = "Error"
            Return False
        End If
        MsgBuf = buf.ToString()                                                         '受信データを保存

        Return True
    End Function

    '(5)コマンド送受信
    Private Function SendQueryMsg(ByVal strMsg As String) As Boolean
        Dim ret As Boolean = False

        ret = SendMsg(strMsg)                                                           'コマンド送信
        If ret Then
            ret = ReceiveMsg()                                                          '送信が成功したら応答を受信
        End If

        Return ret
    End Function

End Class

