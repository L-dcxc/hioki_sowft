Imports System.Text                     'Encodingのために定義


Public Class Form1


    Dim MsgBuf As String


    Dim MsgFlg As Integer

    Dim objExcel As Object
    Dim objBook As Object
    Dim objSheet As Object
    Dim yHan As Long            'Where to display Usage Guide Cell in EXCEL
    Dim xHan As Long            'Where to display Usage Guide Cell in EXCEL
    Dim yLine As Long           'Where to fill in EXCEL
    Dim xLine As Long           'Where to fill in EXCEL
    Dim MAXUNIT As Long         'Number of measurement units
    Dim MAXCH As Long           'Number of Measured Channels
    Dim SAMPLE As Long          'Data retrieval interval (in ms)
    Dim MAXNUM As Long          'Number of Measured Data
    Dim unit As Long
    Dim ch As Long
    Dim num As Long


    Private Sub Button1_Click_1(sender As System.Object, e As System.EventArgs) Handles Button1.Click

        '***************************************************************************************************
        ' USB SAMPLE PROGRAM NO.3
        '
        ' This program connects to this unit and captures the value of each CH and pastes it into EXCEL.
        '
        '***************************************************************************************************




        'Select EXCEL Worksheet
        On Error GoTo Err_Sheet
Chk_Err_Sheet:
        objSheet = objBook.worksheets(TextBox6.Text)
        GoTo No_Err_Sheet
Err_Sheet:


        On Error GoTo Err_Excel
Chk_Err_Excel:
        objSheet = objBook.worksheets.Add
        TextBox6.Text = objSheet.Name


No_Err_Sheet:


        'Selecting Legend Cells for EXCEL
        On Error GoTo Err_Han
Chk_Err_Han:
        yHan = objSheet.Range(TextBox9.Text).Row
        xHan = objSheet.Range(TextBox9.Text).Column
        GoTo No_Err_Han
Err_Han:
        TextBox9.Text = "A1"
        GoTo Chk_Err_Han
No_Err_Han:



        'Selecting Cells for EXCEL
        On Error GoTo Err_Cell
Chk_Err_Cell:
        yLine = objSheet.Range(TextBox7.Text).Row
        xLine = objSheet.Range(TextBox7.Text).Column
        GoTo No_Err_Cell
Err_Cell:
        TextBox7.Text = "A2"
        GoTo Chk_Err_Cell
No_Err_Cell:



        TextBox1.Text = "Measuring"

        SAMPLE = (TextBox3.Text * 1000) 'Data retrieval interval (in ms)

        MAXUNIT = 1

        MAXCH = TextBox4.Text

        MAXNUM = TextBox8.Text


        num = 0


        'Configuring the LR8450
        SendMsgCrLf(":HEAD OFF")

        For unit = 1 To MAXUNIT
            For ch = 1 To MAXCH
                If (unit = 1 And ch = 1) Then
                    objSheet.Cells(yHan, xLine).Value = "Time of dayTime of day"
                End If
                objSheet.Cells(yHan, xHan + ((unit - 1) * MAXCH) + ch).Value = "CH" & unit & "_" & ch
            Next ch
        Next unit


        start_timer()

        get_data()


        GoTo No_Err_Excel


Err_Excel:
        TextBox1.Text = "Unable to measure. Is Excel running?"


No_Err_Excel:

    End Sub


    Private Sub get_data()

        Dim RecciveStr As String

        'Sending query command to LR8450
        SendMsgCrLf(":MEM:GETREAL")

        For unit = 1 To MAXUNIT
            For ch = 1 To MAXCH

                GetMsg2CrLf(":MEM:VREAL? CH" & unit & "_" & ch)

                'Receive query from LR8450
                RecciveStr = MsgBuf

                'Write ti EXCEL
                If (unit = 1 And ch = 1) Then
                    objSheet.Cells(yLine, xLine).Value = TimeOfDay
                End If
                objSheet.Cells(yLine, xLine + ((unit - 1) * MAXCH) + ch).Value = RecciveStr

            Next ch
        Next unit

        objSheet.Cells(yLine, 1).Show()

        yLine = yLine + 1
        TextBox7.Text = objSheet.Cells(yLine, xLine).address(rowAbsolute:=False, columnAbsolute:=False)

        num = num + 1

        If MAXNUM <> 0 And MAXNUM = num Then
            stop_timer()
        End If

    End Sub


    Private Sub start_timer()


        Timer1.Interval = SAMPLE
        Timer1.Enabled = True

    End Sub


    Private Sub stop_timer()

        Timer1.Enabled = False

        TextBox1.Text = "Measure End"

    End Sub


    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick

        get_data()

    End Sub


    Private Sub Button4_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button4.Click

        stop_timer()

    End Sub


    Private Sub Button5_Click_1(sender As System.Object, e As System.EventArgs) Handles Button5.Click

        objExcel = CreateObject("Excel.application")

        objExcel.Visible = True

        On Error GoTo Err_Book
Chk_Err_Book:
        objBook = objExcel.workbooks.open(TextBox5.Text)
        GoTo No_Err_Book
Err_Book:
        objBook = objExcel.workbooks.Add
        TextBox5.Text = "c:\" + objBook.Name
No_Err_Book:

    End Sub


    Private Sub Form_Load()

        'If you want to remember the values you set when you run the program and use the same settings the next time you run the program, enable the following.
        '    textSerial = GetSetting("samp3", "Startup", "Set1", "0")
        '    TextBox3 = GetSetting("samp3", "Startup", "Set3", "1")
        '    TextBox4 = GetSetting("samp3", "Startup", "Set4", "15")
        '    TextBox5 = GetSetting("samp3", "Startup", "Set5", "c:\Book1")
        '    TextBox6 = GetSetting("samp3", "Startup", "Set6", "Sheet1")
        '    TextBox7 = GetSetting("samp3", "Startup", "Set7", "A2")
        '    TextBox8 = GetSetting("samp3", "Startup", "Set8", "0")
        '    TextBox9 = GetSetting("samp3", "Startup", "Set9", "A1")

    End Sub


    Private Sub Form_Unload(ByVal Cancel As Integer)

        'オブジェクトの解放
        objExcel = Nothing
        objBook = Nothing
        objSheet = Nothing


        'If you want to remember the values you set when you run the program and use the same settings the next time you run the program, enable the following.
        '    SaveSetting "samp3", "Startup", "Set1", textSerial
        '    SaveSetting "samp3", "Startup", "Set3", TextBox3
        '    SaveSetting "samp3", "Startup", "Set4", TextBox4
        '    SaveSetting "samp3", "Startup", "Set5", TextBox5
        '    SaveSetting "samp3", "Startup", "Set6", TextBox6
        '    SaveSetting "samp3", "Startup", "Set7", TextBox7
        '    SaveSetting "samp3", "Startup", "Set8", TextBox8
        '    SaveSetting "samp3", "Startup", "Set9", TextBox9

    End Sub


    Private Sub Button2_Click_1(sender As System.Object, e As System.EventArgs) Handles Button2.Click

        SerialPort1.PortName = TextCom.Text
        SerialPort1.Open()                                      'Connect

    End Sub

    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click

        SerialPort1.Close()                                    'Disconnect


    End Sub

    Private Sub SendMsgCrLf(ByVal strMsg As String)

        strMsg = strMsg & vbCrLf
        SerialPort1.WriteLine(strMsg)                          'Send Message

    End Sub

    Private Sub GetMsg2CrLf(ByVal strMsg As String)

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

    Private Sub TextBox5_TextChanged(sender As System.Object, e As System.EventArgs)

    End Sub

    Private Sub Label3_Click(sender As System.Object, e As System.EventArgs)

    End Sub

    Private Sub Label10_Click(sender As System.Object, e As System.EventArgs)

    End Sub

    Private Sub TextBox3_TextChanged(sender As System.Object, e As System.EventArgs)

    End Sub

    Private Sub TextBox7_TextChanged(sender As System.Object, e As System.EventArgs) Handles TextBox7.TextChanged

    End Sub
End Class
