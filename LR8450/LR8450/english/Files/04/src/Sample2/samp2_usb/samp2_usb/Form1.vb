Public Class Form1


    Dim MsgBuf As String


    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click

        '*******************************************************************************
        ' USB SAMPLE PROGRAM NO.2
        '    
        ' Gets the stored data in the memory.
        '
        '*******************************************************************************

        Dim data As Double
        Dim i As Integer

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

        SerialPort1.PortName = TextCom.Text
        SerialPort1.Open()                                     'Connect


    End Sub

    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click

        SerialPort1.Close()                                    'Disconnect


    End Sub

    Private Sub SendMsgCrLf(ByVal strMsg As String)

        strMsg = strMsg & vbCrLf
        SerialPort1.WriteLine(strMsg)                          'Send Message

    End Sub

    Private Sub GetMsgCrLf(ByVal strMsg As String)

        strMsg = strMsg & vbCrLf
        SerialPort1.WriteLine(strMsg)                          'Send Message

        Dim Check As Integer
        MsgBuf = Nothing
        Do                                                     'Wait until a response is received
            Check = SerialPort1.ReadByte()
            If Chr(Check) = vbLf Then
                Exit Do
            ElseIf Chr(Check) = vbCr Then
            Else
                MsgBuf = MsgBuf & Chr(Check)
            End If
        Loop

    End Sub

    Private Sub TextCom_TextChanged(sender As System.Object, e As System.EventArgs) Handles TextCom.TextChanged

    End Sub
End Class
