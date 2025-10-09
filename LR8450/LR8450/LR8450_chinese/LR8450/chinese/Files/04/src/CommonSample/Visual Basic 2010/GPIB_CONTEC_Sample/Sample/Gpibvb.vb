Option Strict Off
Option Explicit On
Module GPIBVB1
	
	Declare Function GpIni Lib "apigpib1.dll" () As Integer
	Declare Function GpIfc Lib "apigpib1.dll" (ByVal Ifctime As Integer) As Integer
	Declare Function GpRen Lib "apigpib1.dll" () As Integer
	Declare Function GpResetren Lib "apigpib1.dll" () As Integer
	Declare Function GpTalk Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkBinary Lib "apigpib1.dll" Alias "GpTalk" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListen Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenBinary Lib "apigpib1.dll" Alias "GpListen" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpPoll Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr) As Integer
	Declare Function GpSrq Lib "apigpib1.dll" (ByVal Eoi As Integer) As Integer
	Declare Function GpStb Lib "apigpib1.dll" (ByVal Stb As Integer) As Integer
	Declare Function GpDelim Lib "apigpib1.dll" (ByVal Delim As Integer, ByVal Eoi As Integer) As Integer
	Declare Function GpTimeout Lib "apigpib1.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpChkstb Lib "apigpib1.dll" (ByRef Stb As Integer, ByRef Eoi As Integer) As Integer
	Declare Function GpReadreg Lib "apigpib1.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpDma Lib "apigpib1.dll" (ByVal Dmamode As Integer, ByVal Dmach As Integer) As Integer
	Declare Function GpExit Lib "apigpib1.dll" () As Integer
	Declare Function GpComand Lib "apigpib1.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpStstop Lib "apigpib1.dll" (ByVal Stp As Integer) As Integer
	Declare Function GpDmastop Lib "apigpib1.dll" () As Integer
	Declare Function GpPpollmode Lib "apigpib1.dll" (ByVal Pmode As Integer) As Integer
	Declare Function GpStppoll Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByVal Stppu As Integer) As Integer
	Declare Function GpExppoll Lib "apigpib1.dll" (ByRef Pprdata As Integer) As Integer
	Declare Function GpStwait Lib "apigpib1.dll" (ByVal Buscode As Integer) As Integer
	Declare Function GpWaittime Lib "apigpib1.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpReadbus Lib "apigpib1.dll" (ByRef Bussta As Integer) As Integer
	Declare Function GpSfile Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpRfile Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpSdc Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpDcl Lib "apigpib1.dll" () As Integer
	Declare Function GpGet Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpGtl Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpLlo Lib "apigpib1.dll" () As Integer
	Declare Function GpTct Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	
	Declare Function GpCrst Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCopc Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCwai Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCcls Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCtrg Lib "apigpib1.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCpre Lib "apigpib1.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCese Lib "apigpib1.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCsre Lib "apigpib1.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	
	Declare Function GpQidn Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopt Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpud Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQrdt Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQcal Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlrn Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQtst Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopc Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQemc Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQgmc Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlmc Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQist Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpre Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQese Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQesr Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpsc Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQsre Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQstb Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQddt Lib "apigpib1.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTaLaBit Lib "apigpib1.dll" (ByVal GpTaLaSts As Integer) As Integer
	Declare Function GpBoardsts Lib "apigpib1.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpSrqEvent Lib "apigpib1.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqEventEx Lib "apigpib1.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqOn Lib "apigpib1.dll" () As Integer
	Declare Function GpDevFind Lib "apigpib1.dll" (ByVal Fstb As IntPtr) As Integer
	Declare Function GpInpB Lib "apigpib1.dll" (ByVal Port As Short) As Byte
	Declare Function GpInpW Lib "apigpib1.dll" (ByVal Port As Short) As Short
	Declare Function GpInpD Lib "apigpib1.dll" (ByVal Port As Short) As Integer
	Declare Function GpOutB Lib "apigpib1.dll" (ByVal Port As Short, ByVal Dat As Byte) As Byte
	Declare Function GpOutW Lib "apigpib1.dll" (ByVal Port As Short, ByVal Dat As Short) As Short
	Declare Function GpOutD Lib "apigpib1.dll" (ByVal Port As Short, ByVal Dat As Integer) As Integer
	Declare Function GpSetEvent Lib "apigpib1.dll" (ByVal EventOn As Integer) As Integer
	Declare Function GpSetEventSrq Lib "apigpib1.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSetEventDet Lib "apigpib1.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DetOn As Integer) As Integer
	Declare Function GpSetEventDec Lib "apigpib1.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DecOn As Integer) As Integer
	Declare Function GpSetEventIfc Lib "apigpib1.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal IfcOn As Integer) As Integer
	Declare Function GpEnableNextEvent Lib "apigpib1.dll" () As Integer
	Declare Function GpSrqEx Lib "apigpib1.dll" (ByVal Stb As Integer, ByVal Eoi As Integer, ByVal SrqSend As Integer) As Integer
	Declare Function GpUpperCode Lib "apigpib1.dll" (ByVal UpperCode As Integer) As Integer
	Declare Function GpCnvSettings Lib "apigpib1.dll" (ByVal Header As String, ByVal Footer As String, ByVal Sep As String, ByVal Suffix As Integer) As Integer
	Declare Function GpCnvSettingsToStr Lib "apigpib1.dll" (ByVal Plus As Integer, ByVal Digit As Integer, ByVal Cutdown As Integer) As Integer
	Declare Function GpCnvStrToDbl Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByRef DblData As Double) As Integer
	Declare Function GpCnvStrToDblArray Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByVal DblData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvStrToFlt Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByRef FltData As Single) As Integer
	Declare Function GpCnvStrToFltArray Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByVal FltData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvDblToStr Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As Double) As Integer
	Declare Function GpCnvDblArrayToStr Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvFltToStr Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As Single) As Integer
	Declare Function GpCnvFltArrayToStr Lib "apigpib1.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpPollEx Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr, ByVal Psrq As IntPtr) As Integer
	Declare Function GpSlowMode Lib "apigpib1.dll" (ByVal SlowMode As Integer) As Integer
	Declare Function GpCnvCvSettings Lib "apigpib1.dll" (ByRef Settings As Integer) As Integer
	Declare Function GpCnvCvi Lib "apigpib1.dll" (ByVal TwoByteData As IntPtr, ByRef IntData As Short) As Integer
	Declare Function GpCnvCviArray Lib "apigpib1.dll" (ByVal TwoByteData As IntPtr, ByVal IntDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvs Lib "apigpib1.dll" (ByVal FourByteData As IntPtr, ByRef FloatData As Single) As Integer
	Declare Function GpCnvCvsArray Lib "apigpib1.dll" (ByVal FourByteData As IntPtr, ByVal FloatDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvd Lib "apigpib1.dll" (ByVal EightByteData As IntPtr, ByRef DoubleData As Double) As Integer
	Declare Function GpCnvCvdArray Lib "apigpib1.dll" (ByVal EightByteData As IntPtr, ByVal DoubleDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	
	Declare Function GpTalkEx Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkExBinary Lib "apigpib1.dll" Alias "GpTalkEx" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenEx Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenExBinary Lib "apigpib1.dll" Alias "GpListenEx" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpTalkAsync Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenAsync Lib "apigpib1.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpCommandAsync Lib "apigpib1.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpCheckAsync Lib "apigpib1.dll" (ByVal WaitFlag As Integer, ByRef ErrCode As Integer) As Integer
	Declare Function GpStopAsync Lib "apigpib1.dll" () As Integer
	Declare Function GpDevFindEx Lib "apigpib1.dll" (ByVal Pad As Short, ByVal Sad As Short, ByRef Result As Short) As Integer
	Declare Function GpBoardstsEx Lib "apigpib1.dll" (ByVal SetFlag As Integer, ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpCommand Lib "apigpib1.dll" Alias "GpComand" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpSmoothMode Lib "apigpib1.dll" (ByVal Mode As Integer) As Integer
	
	
	
	Declare Function GpIni2 Lib "apigpib2.dll" () As Integer
	Declare Function GpIfc2 Lib "apigpib2.dll" (ByVal Ifctime As Integer) As Integer
	Declare Function GpRen2 Lib "apigpib2.dll" () As Integer
	Declare Function GpResetren2 Lib "apigpib2.dll" () As Integer
	Declare Function GpTalk2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkBinary2 Lib "apigpib2.dll" Alias "GpTalk2" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListen2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenBinary2 Lib "apigpib2.dll" Alias "GpListen2" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpPoll2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr) As Integer
	Declare Function GpSrq2 Lib "apigpib2.dll" (ByVal Eoi As Integer) As Integer
	Declare Function GpStb2 Lib "apigpib2.dll" (ByVal Stb As Integer) As Integer
	Declare Function GpDelim2 Lib "apigpib2.dll" (ByVal Delim As Integer, ByVal Eoi As Integer) As Integer
	Declare Function GpTimeout2 Lib "apigpib2.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpChkstb2 Lib "apigpib2.dll" (ByRef Stb As Integer, ByRef Eoi As Integer) As Integer
	Declare Function GpReadreg2 Lib "apigpib2.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpDma2 Lib "apigpib2.dll" (ByVal Dmamode As Integer, ByVal Dmach As Integer) As Integer
	Declare Function GpExit2 Lib "apigpib2.dll" () As Integer
	Declare Function GpComand2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpStstop2 Lib "apigpib2.dll" (ByVal Stp As Integer) As Integer
	Declare Function GpDmastop2 Lib "apigpib2.dll" () As Integer
	Declare Function GpPpollmode2 Lib "apigpib2.dll" (ByVal Pmode As Integer) As Integer
	Declare Function GpStppoll2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByVal Stppu As Integer) As Integer
	Declare Function GpExppoll2 Lib "apigpib2.dll" (ByRef Pprdata As Integer) As Integer
	Declare Function GpStwait2 Lib "apigpib2.dll" (ByVal Buscode As Integer) As Integer
	Declare Function GpWaittime2 Lib "apigpib2.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpReadbus2 Lib "apigpib2.dll" (ByRef Bussta As Integer) As Integer
	Declare Function GpSfile2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpRfile2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpSdc2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpDcl2 Lib "apigpib2.dll" () As Integer
	Declare Function GpGet2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpGtl2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpLlo2 Lib "apigpib2.dll" () As Integer
	Declare Function GpTct2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	
	Declare Function GpCrst2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCopc2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCwai2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCcls2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCtrg2 Lib "apigpib2.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCpre2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCese2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCsre2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	
	Declare Function GpQidn2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopt2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpud2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQrdt2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQcal2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlrn2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQtst2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopc2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQemc2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQgmc2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlmc2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQist2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpre2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQese2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQesr2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpsc2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQsre2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQstb2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQddt2 Lib "apigpib2.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTaLaBit2 Lib "apigpib2.dll" (ByVal GpTaLaSts As Integer) As Integer
	Declare Function GpBoardsts2 Lib "apigpib2.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpSrqEvent2 Lib "apigpib2.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqEventEx2 Lib "apigpib2.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqOn2 Lib "apigpib2.dll" () As Integer
	Declare Function GpDevFind2 Lib "apigpib2.dll" (ByVal Fstb As IntPtr) As Integer
	Declare Function GpInpB2 Lib "apigpib2.dll" (ByVal Port As Short) As Byte
	Declare Function GpInpW2 Lib "apigpib2.dll" (ByVal Port As Short) As Short
	Declare Function GpInpD2 Lib "apigpib2.dll" (ByVal Port As Short) As Integer
	Declare Function GpOutB2 Lib "apigpib2.dll" (ByVal Port As Short, ByVal Dat As Byte) As Byte
	Declare Function GpOutW2 Lib "apigpib2.dll" (ByVal Port As Short, ByVal Dat As Short) As Short
	Declare Function GpOutD2 Lib "apigpib2.dll" (ByVal Port As Short, ByVal Dat As Integer) As Integer
	Declare Function GpSetEvent2 Lib "apigpib2.dll" (ByVal EventOn As Integer) As Integer
	Declare Function GpSetEventSrq2 Lib "apigpib2.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSetEventDet2 Lib "apigpib2.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DetOn As Integer) As Integer
	Declare Function GpSetEventDec2 Lib "apigpib2.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DecOn As Integer) As Integer
	Declare Function GpSetEventIfc2 Lib "apigpib2.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal IfcOn As Integer) As Integer
	Declare Function GpEnableNextEvent2 Lib "apigpib2.dll" () As Integer
	Declare Function GpSrqEx2 Lib "apigpib2.dll" (ByVal Stb As Integer, ByVal Eoi As Integer, ByVal SrqSend As Integer) As Integer
	Declare Function GpUpperCode2 Lib "apigpib2.dll" (ByVal UpperCode As Integer) As Integer
	Declare Function GpCnvSettings2 Lib "apigpib2.dll" (ByVal Header As String, ByVal Footer As String, ByVal Sep As String, ByVal Suffix As Integer) As Integer
	Declare Function GpCnvSettingsToStr2 Lib "apigpib2.dll" (ByVal Plus As Integer, ByVal Digit As Integer, ByVal Cutdown As Integer) As Integer
	Declare Function GpCnvStrToDbl2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByRef DblData As Double) As Integer
	Declare Function GpCnvStrToDblArray2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByVal DblData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvStrToFlt2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByRef FltData As Single) As Integer
	Declare Function GpCnvStrToFltArray2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByVal FltData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvDblToStr2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As Double) As Integer
	Declare Function GpCnvDblArrayToStr2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvFltToStr2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As Single) As Integer
	Declare Function GpCnvFltArrayToStr2 Lib "apigpib2.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpPollEx2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr, ByVal Psrq As IntPtr) As Integer
	Declare Function GpSlowMode2 Lib "apigpib2.dll" (ByVal SlowMode As Integer) As Integer
	Declare Function GpCnvCvSettings2 Lib "apigpib2.dll" (ByRef Settings As Integer) As Integer
	Declare Function GpCnvCvi2 Lib "apigpib2.dll" (ByVal TwoByteData As IntPtr, ByRef IntData As Short) As Integer
	Declare Function GpCnvCviArray2 Lib "apigpib2.dll" (ByVal TwoByteData As IntPtr, ByVal IntDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvs2 Lib "apigpib2.dll" (ByVal FourByteData As IntPtr, ByRef FloatData As Single) As Integer
	Declare Function GpCnvCvsArray2 Lib "apigpib2.dll" (ByVal FourByteData As IntPtr, ByVal FloatDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvd2 Lib "apigpib2.dll" (ByVal EightByteData As IntPtr, ByRef DoubleData As Double) As Integer
	Declare Function GpCnvCvdArray2 Lib "apigpib2.dll" (ByVal EightByteData As IntPtr, ByVal DoubleDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	
	Declare Function GpTalkEx2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkExBinary2 Lib "apigpib2.dll" Alias "GpTalkEx2" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenEx2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenExBinary2 Lib "apigpib2.dll" Alias "GpListenEx2" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpTalkAsync2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenAsync2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpCommandAsync2 Lib "apigpib2.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpCheckAsync2 Lib "apigpib2.dll" (ByVal WaitFlag As Integer, ByRef ErrCode As Integer) As Integer
	Declare Function GpStopAsync2 Lib "apigpib2.dll" () As Integer
	Declare Function GpDevFindEx2 Lib "apigpib2.dll" (ByVal Pad As Short, ByVal Sad As Short, ByRef Result As Short) As Integer
	Declare Function GpBoardstsEx2 Lib "apigpib2.dll" (ByVal SetFlag As Integer, ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpCommand2 Lib "apigpib2.dll" Alias "GpComand2" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpSmoothMode2 Lib "apigpib2.dll" (ByVal Mode As Integer) As Integer
	
	
	
	Declare Function GpIni3 Lib "apigpib3.dll" () As Integer
	Declare Function GpIfc3 Lib "apigpib3.dll" (ByVal Ifctime As Integer) As Integer
	Declare Function GpRen3 Lib "apigpib3.dll" () As Integer
	Declare Function GpResetren3 Lib "apigpib3.dll" () As Integer
	Declare Function GpTalk3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkBinary3 Lib "apigpib3.dll" Alias "GpTalk3" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListen3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenBinary3 Lib "apigpib3.dll" Alias "GpListen3" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpPoll3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr) As Integer
	Declare Function GpSrq3 Lib "apigpib3.dll" (ByVal Eoi As Integer) As Integer
	Declare Function GpStb3 Lib "apigpib3.dll" (ByVal Stb As Integer) As Integer
	Declare Function GpDelim3 Lib "apigpib3.dll" (ByVal Delim As Integer, ByVal Eoi As Integer) As Integer
	Declare Function GpTimeout3 Lib "apigpib3.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpChkstb3 Lib "apigpib3.dll" (ByRef Stb As Integer, ByRef Eoi As Integer) As Integer
	Declare Function GpReadreg3 Lib "apigpib3.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpDma3 Lib "apigpib3.dll" (ByVal Dmamode As Integer, ByVal Dmach As Integer) As Integer
	Declare Function GpExit3 Lib "apigpib3.dll" () As Integer
	Declare Function GpComand3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpStstop3 Lib "apigpib3.dll" (ByVal Stp As Integer) As Integer
	Declare Function GpDmastop3 Lib "apigpib3.dll" () As Integer
	Declare Function GpPpollmode3 Lib "apigpib3.dll" (ByVal Pmode As Integer) As Integer
	Declare Function GpStppoll3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByVal Stppu As Integer) As Integer
	Declare Function GpExppoll3 Lib "apigpib3.dll" (ByRef Pprdata As Integer) As Integer
	Declare Function GpStwait3 Lib "apigpib3.dll" (ByVal Buscode As Integer) As Integer
	Declare Function GpWaittime3 Lib "apigpib3.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpReadbus3 Lib "apigpib3.dll" (ByRef Bussta As Integer) As Integer
	Declare Function GpSfile3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpRfile3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpSdc3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpDcl3 Lib "apigpib3.dll" () As Integer
	Declare Function GpGet3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpGtl3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpLlo3 Lib "apigpib3.dll" () As Integer
	Declare Function GpTct3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	
	Declare Function GpCrst3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCopc3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCwai3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCcls3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCtrg3 Lib "apigpib3.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCpre3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCese3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCsre3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	
	Declare Function GpQidn3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopt3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpud3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQrdt3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQcal3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlrn3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQtst3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopc3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQemc3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQgmc3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlmc3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQist3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpre3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQese3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQesr3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpsc3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQsre3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQstb3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQddt3 Lib "apigpib3.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTaLaBit3 Lib "apigpib3.dll" (ByVal GpTaLaSts As Integer) As Integer
	Declare Function GpBoardsts3 Lib "apigpib3.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpSrqEvent3 Lib "apigpib3.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqEventEx3 Lib "apigpib3.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqOn3 Lib "apigpib3.dll" () As Integer
	Declare Function GpDevFind3 Lib "apigpib3.dll" (ByVal Fstb As IntPtr) As Integer
	Declare Function GpInpB3 Lib "apigpib1.dll" (ByVal Port As Short) As Byte
	Declare Function GpInpW3 Lib "apigpib1.dll" (ByVal Port As Short) As Short
	Declare Function GpInpD3 Lib "apigpib1.dll" (ByVal Port As Short) As Integer
	Declare Function GpOutB3 Lib "apigpib3.dll" (ByVal Port As Short, ByVal Dat As Byte) As Byte
	Declare Function GpOutW3 Lib "apigpib3.dll" (ByVal Port As Short, ByVal Dat As Short) As Short
	Declare Function GpOutD3 Lib "apigpib3.dll" (ByVal Port As Short, ByVal Dat As Integer) As Integer
	Declare Function GpSetEvent3 Lib "apigpib3.dll" (ByVal EventOn As Integer) As Integer
	Declare Function GpSetEventSrq3 Lib "apigpib3.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSetEventDet3 Lib "apigpib3.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DetOn As Integer) As Integer
	Declare Function GpSetEventDec3 Lib "apigpib3.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DecOn As Integer) As Integer
	Declare Function GpSetEventIfc3 Lib "apigpib3.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal IfcOn As Integer) As Integer
	Declare Function GpEnableNextEvent3 Lib "apigpib3.dll" () As Integer
	Declare Function GpSrqEx3 Lib "apigpib3.dll" (ByVal Stb As Integer, ByVal Eoi As Integer, ByVal SrqSend As Integer) As Integer
	Declare Function GpUpperCode3 Lib "apigpib3.dll" (ByVal UpperCode As Integer) As Integer
	Declare Function GpCnvSettings3 Lib "apigpib3.dll" (ByVal Header As String, ByVal Footer As String, ByVal Sep As String, ByVal Suffix As Integer) As Integer
	Declare Function GpCnvSettingsToStr3 Lib "apigpib3.dll" (ByVal Plus As Integer, ByVal Digit As Integer, ByVal Cutdown As Integer) As Integer
	Declare Function GpCnvStrToDbl3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByRef DblData As Double) As Integer
	Declare Function GpCnvStrToDblArray3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByVal DblData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvStrToFlt3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByRef FltData As Single) As Integer
	Declare Function GpCnvStrToFltArray3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByVal FltData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvDblToStr3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As Double) As Integer
	Declare Function GpCnvDblArrayToStr3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvFltToStr3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As Single) As Integer
	Declare Function GpCnvFltArrayToStr3 Lib "apigpib3.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpPollEx3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr, ByVal Psrq As IntPtr) As Integer
	Declare Function GpSlowMode3 Lib "apigpib3.dll" (ByVal SlowMode As Integer) As Integer
	Declare Function GpCnvCvSettings3 Lib "apigpib3.dll" (ByRef Settings As Integer) As Integer
	Declare Function GpCnvCvi3 Lib "apigpib3.dll" (ByVal TwoByteData As IntPtr, ByRef IntData As Short) As Integer
	Declare Function GpCnvCviArray3 Lib "apigpib3.dll" (ByVal TwoByteData As IntPtr, ByVal IntDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvs3 Lib "apigpib3.dll" (ByVal FourByteData As IntPtr, ByRef FloatData As Single) As Integer
	Declare Function GpCnvCvsArray3 Lib "apigpib3.dll" (ByVal FourByteData As IntPtr, ByVal FloatDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvd3 Lib "apigpib3.dll" (ByVal EightByteData As IntPtr, ByRef DoubleData As Double) As Integer
	Declare Function GpCnvCvdArray3 Lib "apigpib3.dll" (ByVal EightByteData As IntPtr, ByVal DoubleDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	
	Declare Function GpTalkEx3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkExBinary3 Lib "apigpib3.dll" Alias "GpTalkEx3" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenEx3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenExBinary3 Lib "apigpib3.dll" Alias "GpListenEx3" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpTalkAsync3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenAsync3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpCommandAsync3 Lib "apigpib3.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpCheckAsync3 Lib "apigpib3.dll" (ByVal WaitFlag As Integer, ByRef ErrCode As Integer) As Integer
	Declare Function GpStopAsync3 Lib "apigpib3.dll" () As Integer
	Declare Function GpDevFindEx3 Lib "apigpib3.dll" (ByVal Pad As Short, ByVal Sad As Short, ByRef Result As Short) As Integer
	Declare Function GpBoardstsEx3 Lib "apigpib3.dll" (ByVal SetFlag As Integer, ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpCommand3 Lib "apigpib3.dll" Alias "GpComand3" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpSmoothMode3 Lib "apigpib3.dll" (ByVal Mode As Integer) As Integer
	
	
	
	Declare Function GpIni4 Lib "apigpib4.dll" () As Integer
	Declare Function GpIfc4 Lib "apigpib4.dll" (ByVal Ifctime As Integer) As Integer
	Declare Function GpRen4 Lib "apigpib4.dll" () As Integer
	Declare Function GpResetren4 Lib "apigpib4.dll" () As Integer
	Declare Function GpTalk4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkBinary4 Lib "apigpib4.dll" Alias "GpTalk4" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListen4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenBinary4 Lib "apigpib4.dll" Alias "GpListen4" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpPoll4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr) As Integer
	Declare Function GpSrq4 Lib "apigpib4.dll" (ByVal Eoi As Integer) As Integer
	Declare Function GpStb4 Lib "apigpib4.dll" (ByVal Stb As Integer) As Integer
	Declare Function GpDelim4 Lib "apigpib4.dll" (ByVal Delim As Integer, ByVal Eoi As Integer) As Integer
	Declare Function GpTimeout4 Lib "apigpib4.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpChkstb4 Lib "apigpib4.dll" (ByRef Stb As Integer, ByRef Eoi As Integer) As Integer
	Declare Function GpReadreg4 Lib "apigpib4.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpDma4 Lib "apigpib4.dll" (ByVal Dmamode As Integer, ByVal Dmach As Integer) As Integer
	Declare Function GpExit4 Lib "apigpib4.dll" () As Integer
	Declare Function GpComand4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpStstop4 Lib "apigpib4.dll" (ByVal Stp As Integer) As Integer
	Declare Function GpDmastop4 Lib "apigpib4.dll" () As Integer
	Declare Function GpPpollmode4 Lib "apigpib4.dll" (ByVal Pmode As Integer) As Integer
	Declare Function GpStppoll4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByVal Stppu As Integer) As Integer
	Declare Function GpExppoll4 Lib "apigpib4.dll" (ByRef Pprdata As Integer) As Integer
	Declare Function GpStwait4 Lib "apigpib4.dll" (ByVal Buscode As Integer) As Integer
	Declare Function GpWaittime4 Lib "apigpib4.dll" (ByVal Timeout As Integer) As Integer
	Declare Function GpReadbus4 Lib "apigpib4.dll" (ByRef Bussta As Integer) As Integer
	Declare Function GpSfile4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpRfile4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByVal Srlen As Integer, ByVal Fname As String) As Integer
	Declare Function GpSdc4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpDcl4 Lib "apigpib4.dll" () As Integer
	Declare Function GpGet4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpGtl4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpLlo4 Lib "apigpib4.dll" () As Integer
	Declare Function GpTct4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	
	Declare Function GpCrst4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCopc4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCwai4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCcls4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCtrg4 Lib "apigpib4.dll" (ByVal Adr As Integer) As Integer
	Declare Function GpCpre4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCese4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	Declare Function GpCsre4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByVal Stb As Integer) As Integer
	
	Declare Function GpQidn4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopt4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpud4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQrdt4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQcal4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlrn4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQtst4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQopc4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQemc4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQgmc4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQlmc4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQist4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpre4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQese4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQesr4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQpsc4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQsre4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQstb4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpQddt4 Lib "apigpib4.dll" (ByVal Adr As Integer, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTaLaBit4 Lib "apigpib4.dll" (ByVal GpTaLaSts As Integer) As Integer
	Declare Function GpBoardsts4 Lib "apigpib4.dll" (ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpSrqEvent4 Lib "apigpib4.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqEventEx4 Lib "apigpib4.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSrqOn4 Lib "apigpib4.dll" () As Integer
	Declare Function GpDevFind4 Lib "apigpib4.dll" (ByVal Fstb As IntPtr) As Integer
	Declare Function GpInpB4 Lib "apigpib4.dll" (ByVal Port As Short) As Byte
	Declare Function GpInpW4 Lib "apigpib4.dll" (ByVal Port As Short) As Short
	Declare Function GpInpD4 Lib "apigpib4.dll" (ByVal Port As Short) As Integer
	Declare Function GpOutB4 Lib "apigpib4.dll" (ByVal Port As Short, ByVal Dat As Byte) As Byte
	Declare Function GpOutW4 Lib "apigpib4.dll" (ByVal Port As Short, ByVal Dat As Short) As Short
	Declare Function GpOutD4 Lib "apigpib4.dll" (ByVal Port As Short, ByVal Dat As Integer) As Integer
	Declare Function GpSetEvent4 Lib "apigpib4.dll" (ByVal EventOn As Integer) As Integer
	Declare Function GpSetEventSrq4 Lib "apigpib4.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal SrqOn As Integer) As Integer
	Declare Function GpSetEventDet4 Lib "apigpib4.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DetOn As Integer) As Integer
	Declare Function GpSetEventDec4 Lib "apigpib4.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal DecOn As Integer) As Integer
	Declare Function GpSetEventIfc4 Lib "apigpib4.dll" (ByVal hwnd As Integer, ByVal wMsg As Short, ByVal IfcOn As Integer) As Integer
	Declare Function GpEnableNextEvent4 Lib "apigpib4.dll" () As Integer
	Declare Function GpSrqEx4 Lib "apigpib4.dll" (ByVal Stb As Integer, ByVal Eoi As Integer, ByVal SrqSend As Integer) As Integer
	Declare Function GpUpperCode4 Lib "apigpib4.dll" (ByVal UpperCode As Integer) As Integer
	Declare Function GpCnvSettings4 Lib "apigpib4.dll" (ByVal Header As String, ByVal Footer As String, ByVal Sep As String, ByVal Suffix As Integer) As Integer
	Declare Function GpCnvSettingsToStr4 Lib "apigpib4.dll" (ByVal Plus As Integer, ByVal Digit As Integer, ByVal Cutdown As Integer) As Integer
	Declare Function GpCnvStrToDbl4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByRef DblData As Double) As Integer
	Declare Function GpCnvStrToDblArray4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByVal DblData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvStrToFlt4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByRef FltData As Single) As Integer
	Declare Function GpCnvStrToFltArray4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByVal FltData As IntPtr, ByRef ArraySize As Integer) As Integer
	Declare Function GpCnvDblToStr4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As Double) As Integer
	Declare Function GpCnvDblArrayToStr4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal DblData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvFltToStr4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As Single) As Integer
	Declare Function GpCnvFltArrayToStr4 Lib "apigpib4.dll" (ByVal Str_Renamed As String, ByRef StrSize As Integer, ByVal FltData As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpPollEx4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByVal Pstb As IntPtr, ByVal Psrq As IntPtr) As Integer
	Declare Function GpSlowMode4 Lib "apigpib4.dll" (ByVal SlowMode As Integer) As Integer
	Declare Function GpCnvCvSettings4 Lib "apigpib4.dll" (ByRef Settings As Integer) As Integer
	Declare Function GpCnvCvi4 Lib "apigpib4.dll" (ByVal TwoByteData As IntPtr, ByRef IntData As Short) As Integer
	Declare Function GpCnvCviArray4 Lib "apigpib4.dll" (ByVal TwoByteData As IntPtr, ByVal IntDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvs4 Lib "apigpib4.dll" (ByVal FourByteData As IntPtr, ByRef FloatData As Single) As Integer
	Declare Function GpCnvCvsArray4 Lib "apigpib4.dll" (ByVal FourByteData As IntPtr, ByVal FloatDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	Declare Function GpCnvCvd4 Lib "apigpib4.dll" (ByVal EightByteData As IntPtr, ByRef DoubleData As Double) As Integer
	Declare Function GpCnvCvdArray4 Lib "apigpib4.dll" (ByVal EightByteData As IntPtr, ByVal DoubleDataArray As IntPtr, ByVal ArraySize As Integer) As Integer
	
	Declare Function GpTalkEx4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpTalkExBinary4 Lib "apigpib4.dll" Alias "GpTalkEx4" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenEx4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As String) As Integer
	Declare Function GpListenExBinary4 Lib "apigpib4.dll" Alias "GpListenEx4" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpTalkAsync4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpListenAsync4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr, ByRef Srlen As Integer, ByVal Srbuf As IntPtr) As Integer
	Declare Function GpCommandAsync4 Lib "apigpib4.dll" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpCheckAsync4 Lib "apigpib4.dll" (ByVal WaitFlag As Integer, ByRef ErrCode As Integer) As Integer
	Declare Function GpStopAsync4 Lib "apigpib4.dll" () As Integer
	Declare Function GpDevFindEx4 Lib "apigpib4.dll" (ByVal Pad As Short, ByVal Sad As Short, ByRef Result As Short) As Integer
	Declare Function GpBoardstsEx4 Lib "apigpib4.dll" (ByVal SetFlag As Integer, ByVal Reg As Integer, ByRef Preg As Integer) As Integer
	Declare Function GpCommand4 Lib "apigpib4.dll" Alias "GpComand4" (ByVal Cmd As IntPtr) As Integer
	Declare Function GpSmoothMode4 Lib "apigpib4.dll" (ByVal Mode As Integer) As Integer
	
	
	
	' For Help
	Declare Function WinHelp Lib "user32"  Alias "WinHelpA"(ByVal hwnd As Integer, ByVal lpHelpFile As String, ByVal wCommand As Integer, ByVal dwData As Integer) As Integer
	Declare Function RegOpenKeyEx Lib "advapi32.dll"  Alias "RegOpenKeyExA"(ByVal hKey As Integer, ByVal lpSubKey As String, ByVal ulOptions As Integer, ByVal samDesired As Integer, ByRef phkResult As Integer) As Integer
	Declare Function RegQueryValueEx Lib "advapi32.dll"  Alias "RegQueryValueExA"(ByVal hKey As Integer, ByVal lpValueName As String, ByVal lpReserved As Integer, ByRef lpType As Integer, ByVal lpData As String, ByRef lpcbData As Integer) As Integer
	Declare Function RegCloseKey Lib "advapi32.dll" (ByVal hKey As Integer) As Integer
	Declare Function GetVersion Lib "kernel32" () As Integer
	Public HelpFileName As String
	
	' For Async Functions
	Declare Function GlobalAlloc Lib "kernel32" (ByVal wFlags As Integer, ByVal dwBytes As Integer) As Integer
	Declare Function GlobalFree Lib "kernel32" (ByVal hMem As Integer) As Integer

	Public Const GMEM_FIXED As Short = &H0S
	Public Const GMEM_ZEROINIT As Short = &H40s
	Public Const GPTR As Boolean = (GMEM_FIXED Or GMEM_ZEROINIT)
	
	
	'Define in the Windows
	Public Const HELP_CONTEXT As Short = &H1s
	Public Const HELP_QUIT As Short = &H2s
	Public Const HELP_CONTENTS As Short = &H3s
	'GP-IB Help Contexts
	Public Const HLP_SAMPLES_MASTER As Short = 275
	Public Const HLP_SAMPLES_SLAVE As Short = 276
	Public Const HLP_SAMPLES_MLTMETER As Short = 463
	Public Const HLP_SAMPLES_DVS As Short = 278
	Public Const HLP_SAMPLES_OSCILLO As Short = 279
	Public Const HLP_SAMPLES_MLTLINE As Short = 383
	Public Const HLP_SAMPLES_PARALLEL As Short = 381
	Public Const HLP_SAMPLES_POLLING As Short = 382
End Module