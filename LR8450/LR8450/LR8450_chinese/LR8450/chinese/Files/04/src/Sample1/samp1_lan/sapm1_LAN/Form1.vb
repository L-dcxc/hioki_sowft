Imports System.Net
Imports System.Net.Sockets
Imports System.Text                     
Public Class Form1


    Dim netStream As NetworkStream


    Dim MsgBuf As String


    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click

        '*******************************************************************************
        ' LAN SAMPLE PROGRAM NO.1
        '

        'This program conects to the MEMORY HiCORDR and starts communication.
        '*******************************************************************************

        If InStr(TextBox3.Text, "?") = 0 Then

            SendMsgCrLf(TextBox3.Text)                          'Sending Command
            TextBox1.Text = ""

        Else

            GetMsgCrLf(TextBox3.Text)                           'Sending Command and Receiving Response
            TextBox1.Text = MsgBuf

        End If

    End Sub

    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click

        Dim client As New TcpClient(TextIp.Text, Val(TextPort.Text))    'Define a TCP connection by specifying IP and port

        netStream = client.GetStream()       'Open netStream for sending and receiving TCP on LAN
        netStream.WriteTimeout = 1000
        netStream.ReadTimeout = 1000

    End Sub

    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click

        netStream.Close()           'Close netStream used to send and receive TCP on LAN                     

    End Sub

    Private Sub SendMsgCrLf(ByVal strMsg As String)

        Dim bytes() As Byte = Encoding.GetEncoding("shift_jis").GetBytes(strMsg & vbCrLf)

        netStream.Write(bytes, 0, bytes.Length)            'Send Message

    End Sub

    Private Sub GetMsgCrLf(ByVal strMsg As String)
        Dim Check As Integer

        Dim bytes() As Byte = Encoding.GetEncoding("shift_jis").GetBytes(strMsg & vbCrLf)
        netStream.Write(bytes, 0, bytes.Length)            'Send Message

        Dim buf = New List(Of Byte)()

        Do                                                    'Wait until a response is received
            Check = netStream.ReadByte()

            If Chr(Check) = vbLf Then
                Exit Do
            ElseIf Chr(Check) = vbCr Then
            Else
                buf.Add(Check)
            End If
        Loop

        MsgBuf = Encoding.GetEncoding("shift_jis").GetString(buf.ToArray)
        MsgBuf = MsgBuf & vbCrLf



    End Sub

    Private Sub TextIp_TextChanged(sender As System.Object, e As System.EventArgs) Handles TextIp.TextChanged

    End Sub


    Private Sub Label1_Click(sender As System.Object, e As System.EventArgs) Handles Label1.Click

    End Sub

    Private Sub TextBox2_TextChanged(sender As System.Object, e As System.EventArgs)

    End Sub

End Class
