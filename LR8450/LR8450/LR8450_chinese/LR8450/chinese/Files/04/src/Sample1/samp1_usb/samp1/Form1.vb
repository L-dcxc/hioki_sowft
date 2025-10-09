Imports System.Text                     'Encodingのために定義

Public Class Form1


    Dim MsgBuf As String


    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click

        '*******************************************************************************
        ' USB SAMPLE PROGRAM NO.1
        '
        ' This program conects to the MEMORY HiCORDR and starts communication.
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

        SerialPort1.PortName = TextCom.Text
        SerialPort1.Encoding = Encoding.GetEncoding("shift_jis")
        SerialPort1.Open()                                      'Connect


    End Sub

    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click


        SerialPort1.Close()                                     'Disconnect

    End Sub

    Private Sub SendMsgCrLf(ByVal strMsg As String)

        strMsg = strMsg & vbCrLf

        SerialPort1.WriteLine(strMsg)                           'Send Message

    End Sub

    Private Sub GetMsgCrLf(ByVal strMsg As String)

        strMsg = strMsg & vbCrLf
        SerialPort1.WriteLine(strMsg)                          'Send Message

        Dim Check As Integer
        Dim buf = New List(Of Byte)()
        Do                                                     'Wait until a response is received
            Check = SerialPort1.ReadByte()
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

    Private Sub TextCom_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextCom.TextChanged

    End Sub

    Private Sub TextBox1_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox1.TextChanged

    End Sub

    Private Sub Form1_Load(sender As System.Object, e As System.EventArgs) Handles MyBase.Load

    End Sub

End Class
