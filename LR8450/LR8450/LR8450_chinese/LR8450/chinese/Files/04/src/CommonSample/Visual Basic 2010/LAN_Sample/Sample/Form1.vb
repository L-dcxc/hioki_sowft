'*******************************************************************************
'このプログラムは、計測器に接続してコマンドの送受信を行います。
'コマンドの欄に送信したいコマンドを入力し、[送受信]ボタンを押すと送信されます。
'応答があるコマンド（?が含まれるコマンド）の場合は、テキストボックスに応答が表示されます。
'
'動作確認環境：Microsoft Visual Studio 2010
'              Version 10.0.40219.1 SP1Rel
'              Microsoft .NET Framework
'              Version 4.0.30319 SP1Rel
'              Microsoft Visual Basic 2010
'*******************************************************************************

Imports System.Diagnostics
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
        TextBox1.Enabled = True
        TextBox2.Enabled = True
        TextBox3.Enabled = False
        TextBox4.ReadOnly = True
        TextBox5.Enabled = True

    End Sub

    '---------------------------------------------------------------------------------------
    'ボタンを押したときの処理
    '---------------------------------------------------------------------------------------

    '「接続」ボタンを押したときの処理
    Private Sub Button1_Click(sender As System.Object, e As System.EventArgs) Handles Button1.Click
        '接続
        If OpenInterface(TextBox1.Text, TextBox2.Text, TextBox5.Text) = False Then
            Exit Sub
        End If

        'ボタンとテキストボックスの有効/無効の処理
        Button1.Enabled = False
        Button2.Enabled = True
        Button3.Enabled = True
        TextBox1.Enabled = False
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
        TextBox1.Enabled = True
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
            SendQueryMsg(TextBox3.Text, ReceiveTimeout)                                 'コマンド送信と応答受信
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
    Private LanSocket As System.Net.Sockets.TcpClient                                   'LANソケット
    Private MsgBuf As String = ""                                                       '受信データ
    Private ReceiveTimeout As Long = 0                                                  '受信タイムアウト時間（ms）

    '(1)接続
    Private Function OpenInterface(ByVal ipaddress As String, ByVal port As String, ByVal timeout As String) As Boolean
        Dim ret As Boolean = False
        Dim ip As System.Net.IPAddress = New System.Net.IPAddress(0)                    'IPアドレス

        Try
            ReceiveTimeout = CInt(timeout) * 1000
            If System.Net.IPAddress.TryParse(ipaddress, ip) Then
                LanSocket = New System.Net.Sockets.TcpClient                            'LANソケットオブジェクトを作成
                LanSocket.NoDelay = True                                                '送信の遅延(Nagleアルゴリズム)を無効にする
                LanSocket.Connect(ip, Convert.ToInt32(port))                            '接続
                ret = True
            End If

        Catch Ex As Exception
            MsgBox(Ex.Message)
        End Try

        OpenInterface = ret
    End Function

    '(2)切断
    Private Function CloseInterface() As Boolean
        Dim ret As Boolean = False

        Try
            LanSocket.Close()                                                           'LANソケットクローズ
            ret = True
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try

        CloseInterface = ret
    End Function

    '(3)コマンド送信
    Private Function SendMsg(ByVal strMsg As String) As Boolean
        Dim ret As Boolean = False
        Dim SendBuffer(1024) As Byte

        Try
            strMsg += vbCrLf                                                            'ターミネータ「CR+LF」を付加
            SendBuffer = System.Text.Encoding.Default.GetBytes(strMsg)                  'バイト型に変換
            LanSocket.GetStream().Write(SendBuffer, 0, SendBuffer.Length)               '送信バッファに書き込み
            ret = True
        Catch Ex As Exception
            MsgBox(Ex.Message)
        End Try

        SendMsg = ret
    End Function

    '(4)受信
    Private Function ReceiveMsg(ByVal timeout As Long) As Boolean
        Dim ret As Boolean = False
        Dim ary(65535) As Byte
        Dim rcv As String
        Dim len As Integer
        Dim buf As New StringBuilder()
        Dim sw As New Stopwatch()

        Try
            MsgBuf = ""                                                                 '受信データをクリア

            sw.Start()                                                                  'タイムアウト用ストップウォッチを開始
            'ターミネータ「LF」を受信するまでループ
            Do
                If LanSocket.GetStream().DataAvailable = True Then                      '受信バッファにデータがあれば読み取り
                    len = LanSocket.GetStream().Read(ary, 0, ary.Length)                '受信バッファから読み取り
                    rcv = Encoding.Default.GetString(ary).Substring(0, len)
                    rcv = rcv.Replace(vbCr, "")                                         '受信データ内の「CR」を削除
                    If rcv.IndexOf(vbLf) >= 0 Then                                      'ターミネータ「LF」を受信したら終了
                        rcv = rcv.Substring(0, rcv.IndexOf(vbLf))                       '受信データを「LF」の手前までで切り詰め
                        buf.Append(rcv)                                                 '受信データを保存
                        MsgBuf = buf.ToString()
                        Exit Do
                    Else
                        buf.Append(rcv)                                                 '受信データを保存
                    End If
                End If

                'タイムアウト処理
                If sw.ElapsedMilliseconds > timeout Then
                    MsgBuf = "Timeout"
                    MsgBox(MsgBuf)
                    ReceiveMsg = ret
                    Exit Function
                End If

            Loop
            sw.Stop()                                                                   'ストップウォッチを停止
            ret = True

        Catch Ex As Exception
            MsgBuf = "Error"
            MsgBox(Ex.Message)
        End Try

        ReceiveMsg = ret
    End Function

    '(5)コマンド送受信
    Private Function SendQueryMsg(ByVal strMsg As String, ByVal timeout As Long) As Boolean
        Dim ret As Boolean = False

        ret = SendMsg(strMsg)                                                           'コマンド送信
        If ret Then
            ret = ReceiveMsg(timeout)                                                   '送信が成功したら応答を受信
        End If

        SendQueryMsg = ret
    End Function

End Class

