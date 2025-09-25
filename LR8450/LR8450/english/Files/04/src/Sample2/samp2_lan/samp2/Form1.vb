Imports System.Net
Imports System.Net.Sockets
Imports System.Text



Public Class Form1


    Dim netStream As NetworkStream


    Dim MsgBuf As String


    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click

        '*******************************************************************************
        ' LAN SAMPLE PROGRAM NO.2
        '
        ' Gets the stored data in the memory.
        ' 
        '*******************************************************************************

        Dim data As Double
        Dim i As Integer

        'Configure

        SendMsgCrLf(":CONFIGURE:SAMPLE 50.0E-3")
        SendMsgCrLf(":CONFIGURE:RECTIME 0,0,0,5")
        SendMsgCrLf(":UNIT:STORE CH1_1,ON")
        SendMsgCrLf(":TRIGGER:MODE SINGLE")
        GetMsgCrLf(":START;:STOP;*OPC?")
        'Notes
        '"By specifying ":START;:STOP;*OPC?", you can wait for the capture of the specified record length to finish. 
        ' This is because the stop key does not interrupt the capture until the recording length is completed.

        SendMsgCrLf(":HEADER OFF")
        GetMsgCrLf(":MEMORY:MAXPOINT?")

        If (Val(MsgBuf) = 0) Then
            Exit Sub
        End If

        SendMsgCrLf(":MEMORY:POINT CH1_1,0")

        For i = 0 To 100
            GetMsgCrLf(":MEMORY:VDATA? 1")
            data = Val(MsgBuf)
            TextBox1.SelectedText = Format(data, "Scientific") & vbCrLf
        Next

    End Sub

    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click

        Dim client As New TcpClient(TextIp.Text, Val(TextPort.Text))    'Define a TCP connection by specifying IP and port

        netStream = client.GetStream()                     'Open netStream for sending and receiving TCP on LAN
        netStream.WriteTimeout = 100000
        netStream.ReadTimeout = 100000


    End Sub

    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click

        netStream.Close()                                  'Close netStream used to send and receive TCP on LAN


    End Sub

    Private Sub SendMsgCrLf(ByVal strMsg As String)

        strMsg = strMsg & vbCrLf
        netStream.Write(Encoding.ASCII.GetBytes(strMsg), 0, strMsg.Length)            'Send Message
    End Sub

    Private Sub GetMsgCrLf(ByVal strMsg As String)
        Dim Check As Integer

        strMsg = strMsg & vbCrLf
        netStream.Write(Encoding.ASCII.GetBytes(strMsg), 0, strMsg.Length)            'Send Message

        MsgBuf = Nothing
        Do                                                    'Wait until a response is received
            Check = netStream.ReadByte()

            If Chr(Check) = vbLf Then
                '                MsgBuf = MsgBuf & Chr(Check)
                Exit Do
            ElseIf Chr(Check) = vbCr Then
                '                MsgBuf = MsgBuf & Chr(Check)
            Else
                MsgBuf = MsgBuf & Chr(Check)
            End If
        Loop
        MsgBuf = MsgBuf & vbCrLf

    End Sub

    Private Sub TextIp_TextChanged(sender As System.Object, e As System.EventArgs) Handles TextIp.TextChanged

    End Sub
End Class
