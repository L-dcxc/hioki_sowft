using System;
using System.Text;
using System.Runtime.InteropServices;

/***********************************************************************/
/*          API-GPIB(98/PC)W95,NT                 Header  File         */
/*                                                File Name CgpibCs.cs */
/***********************************************************************/


public enum CgpibConst
{
	HLP_SAMPLES				= 274,
	HLP_SAMPLES_MASTER		= 275,
	HLP_SAMPLES_SLAVE		= 276,
	HLP_SAMPLES_MLTMETER	= 463,
	HLP_SAMPLES_DVS			= 278,
	HLP_SAMPLES_OSCILLO		= 279,
	HLP_SAMPLES_POLLING		= 382,
	HLP_SAMPLES_PARALLEL	= 381,
	HLP_SAMPLES_MLTLINE		= 383,

	ID_TIMER				= 1,
	ID_TIMER_TERMINATE		= 2,
	ID_TIMER_TRANSMISSION	= 3,
	ID_TIMER_RECEPTION		= 4,
	TIMERCOUNT				= 100,
	TIMERCOUNT_TERMINATE	= 3000
}

namespace CgpibCs
{
	/// <summary>
	/// Cgpib の概要の説明です。
	/// </summary>
	public class Cgpib
	{
		/// <summary>
		/// アンマネージDLL(apigpib(1,2,3,4).DLL)のインポート
		/// </summary>
		public const string szHelpFileName95	= "..\\..\\..\\..\\..\\Gpib5td.hlp";
		public const string	szHelpFileNameNT	= "..\\..\\..\\..\\..\\Gpibntd.hlp";

		[DllImport("apigpib1.dll")] static extern uint GpIni();
		[DllImport("apigpib1.dll")] static extern uint GpIfc(uint IfcTime);
		[DllImport("apigpib1.dll")] static extern uint GpRen();
		[DllImport("apigpib1.dll")] static extern uint GpResetren();
		[DllImport("apigpib1.dll")] static extern uint GpTalk(uint[] Cmd, uint Srlen, string Srbuf);
        [DllImport("apigpib1.dll")] static extern uint GpTalk(uint[] Cmd, uint Srlen, byte[] Srbufb);
		[DllImport("apigpib1.dll")] static extern uint GpListen(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib1.dll")] static extern uint GpListen(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib1.dll")] static extern uint GpPoll(uint[] Cmd, uint[] Pstb);
		[DllImport("apigpib1.dll")] static extern uint GpSrq(uint Eoi);
		[DllImport("apigpib1.dll")] static extern uint GpStb(uint Stb);
		[DllImport("apigpib1.dll")] static extern uint GpDelim(uint Delim, uint Eoi);
		[DllImport("apigpib1.dll")] static extern uint GpTimeout(uint Timeout);
		[DllImport("apigpib1.dll")] static extern uint GpChkstb(ref uint Stb, ref uint Eoi);
		[DllImport("apigpib1.dll")] static extern uint GpReadreg(uint Reg, ref uint Preg);
		[DllImport("apigpib1.dll")] static extern uint GpDma(uint Dmamode, uint Dmach);
		[DllImport("apigpib1.dll")] static extern uint GpExit();
		[DllImport("apigpib1.dll")] static extern uint GpComand(uint[] Cmd);
		[DllImport("apigpib1.dll")] static extern uint GpDmainuse();
		[DllImport("apigpib1.dll")] static extern uint GpStstop(uint Stp);
		[DllImport("apigpib1.dll")] static extern uint GpDmastop();
		[DllImport("apigpib1.dll")] static extern uint GpPpollmode(uint Pmode);
		[DllImport("apigpib1.dll")] static extern uint GpStppoll(uint[] Cmd, uint Stppu);
		[DllImport("apigpib1.dll")] static extern uint GpExppoll(ref uint Pprdata);
		[DllImport("apigpib1.dll")] static extern uint GpStwait(uint Buscode);
		[DllImport("apigpib1.dll")] static extern uint GpWaittime(uint Timeout);
		[DllImport("apigpib1.dll")] static extern uint GpReadbus(ref uint Bussta);
		[DllImport("apigpib1.dll")] static extern uint GpSfile(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib1.dll")] static extern uint GpRfile(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib1.dll")] static extern uint GpSdc(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpDcl();
		[DllImport("apigpib1.dll")] static extern uint GpGet(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpGtl(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpLlo();
		[DllImport("apigpib1.dll")] static extern uint GpTct(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpCrst(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpCopc(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpCwai(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpCcls(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpCtrg(uint Adr);
		[DllImport("apigpib1.dll")] static extern uint GpCpre(uint Adr, uint Stb);
		[DllImport("apigpib1.dll")] static extern uint GpCese(uint Adr, uint Stb);
		[DllImport("apigpib1.dll")] static extern uint GpCsre(uint Adr, uint Stb);
		[DllImport("apigpib1.dll")] static extern uint GpQidn(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQopt(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQpud(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQrdt(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQcal(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQlrn(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQtst(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQopc(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQemc(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQgmc(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQlmc(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQist(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQpre(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQese(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQesr(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQpsc(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQsre(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQstb(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpQddt(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib1.dll")] static extern uint GpTaLaBit(uint TaLaSts);
		[DllImport("apigpib1.dll")] static extern uint GpBoardsts(uint Reg, ref uint Preg);
		[DllImport("apigpib1.dll")] static extern uint GpSrqEvent(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib1.dll")] static extern uint GpSrqEventEx(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib1.dll")] static extern uint GpSrqOn();
		[DllImport("apigpib1.dll")] static extern uint GpDevFind(uint[] Fstb);
		[DllImport("apigpib1.dll")] static extern byte GpInpB(short Port);
		[DllImport("apigpib1.dll")] static extern short GpInpW(short Port);
		[DllImport("apigpib1.dll")] static extern int  GpInpD(short Port);
		[DllImport("apigpib1.dll")] static extern byte GpOutB(short Port, byte Dat);
		[DllImport("apigpib1.dll")] static extern short GpOutW(short Port, short Dat);
		[DllImport("apigpib1.dll")] static extern int  GpOutD(short Port, int Dat);
		[DllImport("apigpib1.dll")] static extern uint GpSetEvent(uint EventOn);
		[DllImport("apigpib1.dll")] static extern uint GpSetEventSrq(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib1.dll")] static extern uint GpSetEventDet(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib1.dll")] static extern uint GpSetEventDec(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib1.dll")] static extern uint GpSetEventIfc(int hWnd, ushort wMsg, uint IfcOn);
		[DllImport("apigpib1.dll")] static extern uint GpEnableNextEvent();
		[DllImport("apigpib1.dll")] static extern uint GpSrqEx(uint Stb, uint SrqFlag, uint EoiFlag);
		[DllImport("apigpib1.dll")] static extern uint GpUpperCode(uint UpperCode);
		[DllImport("apigpib1.dll")] static extern uint GpCnvSettings(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag);
		[DllImport("apigpib1.dll")] static extern uint GpCnvSettingsToStr(uint PlusFlag, uint Digit, uint CutDown);
		[DllImport("apigpib1.dll")] static extern uint GpCnvStrToDbl(string Str, ref double DblData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvStrToDblArray(string Str, double[] DblData, ref uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpCnvStrToFlt(string Str, ref float FltData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvStrToFltArray(string Str, float[] FltData, ref uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpCnvDblToStr(StringBuilder Str, ref uint StrSize, double DblData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvDblArrayToStr(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpCnvFltToStr(StringBuilder Str, ref uint StrSize, float FltData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvFltArrayToStr(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpPollEx(uint[] Cmd, uint[] Pstb, uint[] Psrq);
		[DllImport("apigpib1.dll")] static extern uint GpSlowMode(uint SlowTime);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCvSettings(uint Settings);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCvi(byte[] Str, ref short ShtData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCviArray(byte[] Str, short[] ShtData, uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCvs(byte[] Str, ref float FltData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCvsArray(byte[] Str, float[] FltData, uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCvd(byte[] Str, ref double DblData);
		[DllImport("apigpib1.dll")] static extern uint GpCnvCvdArray(byte[] Str, double[] DblData, uint ArraySize);
		[DllImport("apigpib1.dll")] static extern uint GpTalkEx(uint[] Cmd, ref uint Srlen, string Srbuf);
        [DllImport("apigpib1.dll")] static extern uint GpTalkEx(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib1.dll")] static extern uint GpListenEx(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib1.dll")] static extern uint GpListenEx(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib1.dll")] static extern uint GpTalkAsync(uint[] Cmd, ref uint Srlen, string Srbuf);
        [DllImport("apigpib1.dll")] static extern uint GpTalkAsync(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib1.dll")] static extern uint GpListenAsync(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib1.dll")] static extern uint GpListenAsync(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib1.dll")] static extern uint GpCommandAsync(uint[] Cmd);
		[DllImport("apigpib1.dll")] static extern uint GpCheckAsync(uint WaitFlag, ref uint ErrCode);
		[DllImport("apigpib1.dll")] static extern uint GpStopAsync();
		[DllImport("apigpib1.dll")] static extern uint GpDevFindEx(short Pad, short Sad, ref short Lstn);
		[DllImport("apigpib1.dll")] static extern uint GpBoardstsEx(uint SetFlag, uint Reg, ref uint Preg);
		[DllImport("apigpib1.dll")] static extern uint GpSmoothMode(uint Mode);
		
		[DllImport("apigpib2.dll")] static extern uint GpIni2();
		[DllImport("apigpib2.dll")] static extern uint GpIfc2(uint IfcTime);
		[DllImport("apigpib2.dll")] static extern uint GpRen2();
		[DllImport("apigpib2.dll")] static extern uint GpResetren2();
		[DllImport("apigpib2.dll")] static extern uint GpTalk2(uint[] Cmd, uint Srlen, string Srbuf);
        [DllImport("apigpib2.dll")] static extern uint GpTalk2(uint[] Cmd, uint Srlen, byte[] Srbufb);
        [DllImport("apigpib2.dll")] static extern uint GpListen2(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib2.dll")] static extern uint GpListen2(uint[] Cmd, ref uint Srlen, byte[] Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpPoll2(uint[] Cmd, uint[] Pstb);
		[DllImport("apigpib2.dll")] static extern uint GpSrq2(uint Eoi);
		[DllImport("apigpib2.dll")] static extern uint GpStb2(uint Stb);
		[DllImport("apigpib2.dll")] static extern uint GpDelim2(uint Delim, uint Eoi);
		[DllImport("apigpib2.dll")] static extern uint GpTimeout2(uint Timeout);
		[DllImport("apigpib2.dll")] static extern uint GpChkstb2(ref uint Stb, ref uint Eoi);
		[DllImport("apigpib2.dll")] static extern uint GpReadreg2(uint Reg, ref uint Preg);
		[DllImport("apigpib2.dll")] static extern uint GpDma2(uint Dmamode, uint Dmach);
		[DllImport("apigpib2.dll")] static extern uint GpExit2();
		[DllImport("apigpib2.dll")] static extern uint GpComand2(uint[] Cmd);
		[DllImport("apigpib2.dll")] static extern uint GpDmainuse2();
		[DllImport("apigpib2.dll")] static extern uint GpStstop2(uint Stp);
		[DllImport("apigpib2.dll")] static extern uint GpDmastop2();
		[DllImport("apigpib2.dll")] static extern uint GpPpollmode2(uint Pmode);
		[DllImport("apigpib2.dll")] static extern uint GpStppoll2(uint[] Cmd, uint Stppu);
		[DllImport("apigpib2.dll")] static extern uint GpExppoll2(ref uint Pprdata);
		[DllImport("apigpib2.dll")] static extern uint GpStwait2(uint Buscode);
		[DllImport("apigpib2.dll")] static extern uint GpWaittime2(uint Timeout);
		[DllImport("apigpib2.dll")] static extern uint GpReadbus2(ref uint Bussta);
		[DllImport("apigpib2.dll")] static extern uint GpSfile2(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib2.dll")] static extern uint GpRfile2(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib2.dll")] static extern uint GpSdc2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpDcl2();
		[DllImport("apigpib2.dll")] static extern uint GpGet2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpGtl2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpLlo2();
		[DllImport("apigpib2.dll")] static extern uint GpTct2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpCrst2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpCopc2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpCwai2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpCcls2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpCtrg2(uint Adr);
		[DllImport("apigpib2.dll")] static extern uint GpCpre2(uint Adr, uint Stb);
		[DllImport("apigpib2.dll")] static extern uint GpCese2(uint Adr, uint Stb);
		[DllImport("apigpib2.dll")] static extern uint GpCsre2(uint Adr, uint Stb);
		[DllImport("apigpib2.dll")] static extern uint GpQidn2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQopt2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQpud2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQrdt2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQcal2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQlrn2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQtst2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQopc2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQemc2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQgmc2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQlmc2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQist2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQpre2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQese2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQesr2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQpsc2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQsre2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQstb2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpQddt2(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib2.dll")] static extern uint GpTaLaBit2(uint TaLaSts);
		[DllImport("apigpib2.dll")] static extern uint GpBoardsts2(uint Reg, ref uint Preg);
		[DllImport("apigpib2.dll")] static extern uint GpSrqEvent2(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib2.dll")] static extern uint GpSrqEventEx2(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib2.dll")] static extern uint GpSrqOn2();
		[DllImport("apigpib2.dll")] static extern uint GpDevFind2(uint[] Fstb);
		[DllImport("apigpib2.dll")] static extern byte GpInpB2(short Port);
		[DllImport("apigpib2.dll")] static extern short GpInpW2(short Port);
		[DllImport("apigpib2.dll")] static extern int  GpInpD2(short Port);
		[DllImport("apigpib2.dll")] static extern byte GpOutB2(short Port, byte Dat);
		[DllImport("apigpib2.dll")] static extern short GpOutW2(short Port, short Dat);
		[DllImport("apigpib2.dll")] static extern int  GpOutD2(short Port, int Dat);
		[DllImport("apigpib2.dll")] static extern uint GpSetEvent2(uint EventOn);
		[DllImport("apigpib2.dll")] static extern uint GpSetEventSrq2(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib2.dll")] static extern uint GpSetEventDet2(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib2.dll")] static extern uint GpSetEventDec2(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib2.dll")] static extern uint GpSetEventIfc2(int hWnd, ushort wMsg, uint IfcOn);
		[DllImport("apigpib2.dll")] static extern uint GpEnableNextEvent2();
		[DllImport("apigpib2.dll")] static extern uint GpSrqEx2(uint Stb, uint SrqFlag, uint EoiFlag);
		[DllImport("apigpib2.dll")] static extern uint GpUpperCode2(uint UpperCode);
		[DllImport("apigpib2.dll")] static extern uint GpCnvSettings2(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag);
		[DllImport("apigpib2.dll")] static extern uint GpCnvSettingsToStr2(uint PlusFlag, uint Digit, uint CutDown);
		[DllImport("apigpib2.dll")] static extern uint GpCnvStrToDbl2(string Str, ref double DblData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvStrToDblArray2(string Str, double[] DblData, ref uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpCnvStrToFlt2(string Str, ref float FltData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvStrToFltArray2(string Str, float[] FltData, ref uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpCnvDblToStr2(StringBuilder Str, ref uint StrSize, double DblData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvDblArrayToStr2(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpCnvFltToStr2(StringBuilder Str, ref uint StrSize, float FltData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvFltArrayToStr2(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpPollEx2(uint[] Cmd, uint[] Pstb, uint[] Psrq);
		[DllImport("apigpib2.dll")] static extern uint GpSlowMode2(uint SlowTime);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCvSettings2(uint Settings);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCvi2(byte[] Str, ref short ShtData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCviArray2(byte[] Str, short[] ShtData, uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCvs2(byte[] Str, ref float FltData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCvsArray2(byte[] Str, float[] FltData, uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCvd2(byte[] Str, ref double DblData);
		[DllImport("apigpib2.dll")] static extern uint GpCnvCvdArray2(byte[] Str, double[] DblData, uint ArraySize);
		[DllImport("apigpib2.dll")] static extern uint GpTalkEx2(uint[] Cmd, ref uint Srlen, string Srbuf);
        [DllImport("apigpib2.dll")] static extern uint GpTalkEx2(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib2.dll")] static extern uint GpListenEx2(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib2.dll")] static extern uint GpListenEx2(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib2.dll")] static extern uint GpTalkAsync2(uint[] Cmd, ref uint Srlen, string Srbuf);
        [DllImport("apigpib2.dll")] static extern uint GpTalkAsync2(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib2.dll")] static extern uint GpListenAsync2(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib2.dll")] static extern uint GpListenAsync2(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib2.dll")] static extern uint GpCommandAsync2(uint[] Cmd);
		[DllImport("apigpib2.dll")] static extern uint GpCheckAsync2(uint WaitFlag, ref uint ErrCode);
		[DllImport("apigpib2.dll")] static extern uint GpStopAsync2();
		[DllImport("apigpib2.dll")] static extern uint GpDevFindEx2(short Pad, short Sad, ref short Lstn);
		[DllImport("apigpib2.dll")] static extern uint GpBoardstsEx2(uint SetFlag, uint Reg, ref uint Preg);
		[DllImport("apigpib2.dll")] static extern uint GpSmoothMode2(uint Mode);
		
		[DllImport("apigpib3.dll")] static extern uint GpIni3();
		[DllImport("apigpib3.dll")] static extern uint GpIfc3(uint IfcTime);
		[DllImport("apigpib3.dll")] static extern uint GpRen3();
		[DllImport("apigpib3.dll")] static extern uint GpResetren3();
		[DllImport("apigpib3.dll")] static extern uint GpTalk3(uint[] Cmd, uint Srlen, string Srbuf);
        [DllImport("apigpib3.dll")] static extern uint GpTalk3(uint[] Cmd, uint Srlen, byte[] Srbufb);
        [DllImport("apigpib3.dll")] static extern uint GpListen3(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib3.dll")] static extern uint GpListen3(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib3.dll")] static extern uint GpPoll3(uint[] Cmd, uint[] Pstb);
		[DllImport("apigpib3.dll")] static extern uint GpSrq3(uint Eoi);
		[DllImport("apigpib3.dll")] static extern uint GpStb3(uint Stb);
		[DllImport("apigpib3.dll")] static extern uint GpDelim3(uint Delim, uint Eoi);
		[DllImport("apigpib3.dll")] static extern uint GpTimeout3(uint Timeout);
		[DllImport("apigpib3.dll")] static extern uint GpChkstb3(ref uint Stb, ref uint Eoi);
		[DllImport("apigpib3.dll")] static extern uint GpReadreg3(uint Reg, ref uint Preg);
		[DllImport("apigpib3.dll")] static extern uint GpDma3(uint Dmamode, uint Dmach);
		[DllImport("apigpib3.dll")] static extern uint GpExit3();
		[DllImport("apigpib3.dll")] static extern uint GpComand3(uint[] Cmd);
		[DllImport("apigpib3.dll")] static extern uint GpDmainuse3();
		[DllImport("apigpib3.dll")] static extern uint GpStstop3(uint Stp);
		[DllImport("apigpib3.dll")] static extern uint GpDmastop3();
		[DllImport("apigpib3.dll")] static extern uint GpPpollmode3(uint Pmode);
		[DllImport("apigpib3.dll")] static extern uint GpStppoll3(uint[] Cmd, uint Stppu);
		[DllImport("apigpib3.dll")] static extern uint GpExppoll3(ref uint Pprdata);
		[DllImport("apigpib3.dll")] static extern uint GpStwait3(uint Buscode);
		[DllImport("apigpib3.dll")] static extern uint GpWaittime3(uint Timeout);
		[DllImport("apigpib3.dll")] static extern uint GpReadbus3(ref uint Bussta);
		[DllImport("apigpib3.dll")] static extern uint GpSfile3(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib3.dll")] static extern uint GpRfile3(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib3.dll")] static extern uint GpSdc3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpDcl3();
		[DllImport("apigpib3.dll")] static extern uint GpGet3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpGtl3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpLlo3();
		[DllImport("apigpib3.dll")] static extern uint GpTct3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpCrst3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpCopc3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpCwai3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpCcls3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpCtrg3(uint Adr);
		[DllImport("apigpib3.dll")] static extern uint GpCpre3(uint Adr, uint Stb);
		[DllImport("apigpib3.dll")] static extern uint GpCese3(uint Adr, uint Stb);
		[DllImport("apigpib3.dll")] static extern uint GpCsre3(uint Adr, uint Stb);
		[DllImport("apigpib3.dll")] static extern uint GpQidn3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQopt3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQpud3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQrdt3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQcal3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQlrn3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQtst3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQopc3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQemc3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQgmc3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQlmc3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQist3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQpre3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQese3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQesr3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQpsc3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQsre3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQstb3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpQddt3(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpTaLaBit3(uint TaLaSts);
		[DllImport("apigpib3.dll")] static extern uint GpBoardsts3(uint Reg, ref uint Preg);
		[DllImport("apigpib3.dll")] static extern uint GpSrqEvent3(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib3.dll")] static extern uint GpSrqEventEx3(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib3.dll")] static extern uint GpSrqOn3();
		[DllImport("apigpib3.dll")] static extern uint GpDevFind3(uint[] Fstb);
		[DllImport("apigpib3.dll")] static extern byte GpInpB3(short Port);
		[DllImport("apigpib3.dll")] static extern short GpInpW3(short Port);
		[DllImport("apigpib3.dll")] static extern int  GpInpD3(short Port);
		[DllImport("apigpib3.dll")] static extern byte GpOutB3(short Port, byte Dat);
		[DllImport("apigpib3.dll")] static extern short GpOutW3(short Port, short Dat);
		[DllImport("apigpib3.dll")] static extern int  GpOutD3(short Port, int Dat);
		[DllImport("apigpib3.dll")] static extern uint GpSetEvent3(uint EventOn);
		[DllImport("apigpib3.dll")] static extern uint GpSetEventSrq3(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib3.dll")] static extern uint GpSetEventDet3(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib3.dll")] static extern uint GpSetEventDec3(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib3.dll")] static extern uint GpSetEventIfc3(int hWnd, ushort wMsg, uint IfcOn);
		[DllImport("apigpib3.dll")] static extern uint GpEnableNextEvent3();
		[DllImport("apigpib3.dll")] static extern uint GpSrqEx3(uint Stb, uint SrqFlag, uint EoiFlag);
		[DllImport("apigpib3.dll")] static extern uint GpUpperCode3(uint UpperCode);
		[DllImport("apigpib3.dll")] static extern uint GpCnvSettings3(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag);
		[DllImport("apigpib3.dll")] static extern uint GpCnvSettingsToStr3(uint PlusFlag, uint Digit, uint CutDown);
		[DllImport("apigpib3.dll")] static extern uint GpCnvStrToDbl3(string Str, ref double DblData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvStrToDblArray3(string Str, double[] DblData, ref uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpCnvStrToFlt3(string Str, ref float FltData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvStrToFltArray3(string Str, float[] FltData, ref uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpCnvDblToStr3(StringBuilder Str, ref uint StrSize, double DblData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvDblArrayToStr3(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpCnvFltToStr3(StringBuilder Str, ref uint StrSize, float FltData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvFltArrayToStr3(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpPollEx3(uint[] Cmd, uint[] Pstb, uint[] Psrq);
		[DllImport("apigpib3.dll")] static extern uint GpSlowMode3(uint SlowTime);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCvSettings3(uint Settings);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCvi3(byte[] Str, ref short ShtData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCviArray3(byte[] Str, short[] ShtData, uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCvs3(byte[] Str, ref float FltData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCvsArray3(byte[] Str, float[] FltData, uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCvd3(byte[] Str, ref double DblData);
		[DllImport("apigpib3.dll")] static extern uint GpCnvCvdArray3(byte[] Str, double[] DblData, uint ArraySize);
		[DllImport("apigpib3.dll")] static extern uint GpTalkEx3(uint[] Cmd, ref uint Srlen, string Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpTalkEx3(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib3.dll")] static extern uint GpListenEx3(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpListenEx3(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib3.dll")] static extern uint GpTalkAsync3(uint[] Cmd, ref uint Srlen, string Srbuf);
		[DllImport("apigpib3.dll")] static extern uint GpTalkAsync3(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib3.dll")] static extern uint GpListenAsync3(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib3.dll")] static extern uint GpListenAsync3(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib3.dll")] static extern uint GpCommandAsync3(uint[] Cmd);
		[DllImport("apigpib3.dll")] static extern uint GpCheckAsync3(uint WaitFlag, ref uint ErrCode);
		[DllImport("apigpib3.dll")] static extern uint GpStopAsync3();
		[DllImport("apigpib3.dll")] static extern uint GpDevFindEx3(short Pad, short Sad, ref short Lstn);
		[DllImport("apigpib3.dll")] static extern uint GpBoardstsEx3(uint SetFlag, uint Reg, ref uint Preg);
		[DllImport("apigpib3.dll")] static extern uint GpSmoothMode3(uint Mode);
		
		[DllImport("apigpib4.dll")] static extern uint GpIni4();
		[DllImport("apigpib4.dll")] static extern uint GpIfc4(uint IfcTime);
		[DllImport("apigpib4.dll")] static extern uint GpRen4();
		[DllImport("apigpib4.dll")] static extern uint GpResetren4();
		[DllImport("apigpib4.dll")] static extern uint GpTalk4(uint[] Cmd, uint Srlen, string Srbuf);
        [DllImport("apigpib4.dll")] static extern uint GpTalk4(uint[] Cmd, uint Srlen, byte[] Srbufb);
        [DllImport("apigpib4.dll")] static extern uint GpListen4(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib4.dll")] static extern uint GpListen4(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib4.dll")] static extern uint GpPoll4(uint[] Cmd, uint[] Pstb);
		[DllImport("apigpib4.dll")] static extern uint GpSrq4(uint Eoi);
		[DllImport("apigpib4.dll")] static extern uint GpStb4(uint Stb);
		[DllImport("apigpib4.dll")] static extern uint GpDelim4(uint Delim, uint Eoi);
		[DllImport("apigpib4.dll")] static extern uint GpTimeout4(uint Timeout);
		[DllImport("apigpib4.dll")] static extern uint GpChkstb4(ref uint Stb, ref uint Eoi);
		[DllImport("apigpib4.dll")] static extern uint GpReadreg4(uint Reg, ref uint Preg);
		[DllImport("apigpib4.dll")] static extern uint GpDma4(uint Dmamode, uint Dmach);
		[DllImport("apigpib4.dll")] static extern uint GpExit4();
		[DllImport("apigpib4.dll")] static extern uint GpComand4(uint[] Cmd);
		[DllImport("apigpib4.dll")] static extern uint GpDmainuse4();
		[DllImport("apigpib4.dll")] static extern uint GpStstop4(uint Stp);
		[DllImport("apigpib4.dll")] static extern uint GpDmastop4();
		[DllImport("apigpib4.dll")] static extern uint GpPpollmode4(uint Pmode);
		[DllImport("apigpib4.dll")] static extern uint GpStppoll4(uint[] Cmd, uint Stppu);
		[DllImport("apigpib4.dll")] static extern uint GpExppoll4(ref uint Pprdata);
		[DllImport("apigpib4.dll")] static extern uint GpStwait4(uint Buscode);
		[DllImport("apigpib4.dll")] static extern uint GpWaittime4(uint Timeout);
		[DllImport("apigpib4.dll")] static extern uint GpReadbus4(ref uint Bussta);
		[DllImport("apigpib4.dll")] static extern uint GpSfile4(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib4.dll")] static extern uint GpRfile4(uint[] Cmd, uint Srlen, string Fname);
		[DllImport("apigpib4.dll")] static extern uint GpSdc4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpDcl4();
		[DllImport("apigpib4.dll")] static extern uint GpGet4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpGtl4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpLlo4();
		[DllImport("apigpib4.dll")] static extern uint GpTct4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpCrst4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpCopc4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpCwai4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpCcls4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpCtrg4(uint Adr);
		[DllImport("apigpib4.dll")] static extern uint GpCpre4(uint Adr, uint Stb);
		[DllImport("apigpib4.dll")] static extern uint GpCese4(uint Adr, uint Stb);
		[DllImport("apigpib4.dll")] static extern uint GpCsre4(uint Adr, uint Stb);
		[DllImport("apigpib4.dll")] static extern uint GpQidn4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQopt4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQpud4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQrdt4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQcal4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQlrn4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQtst4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQopc4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQemc4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQgmc4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQlmc4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQist4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQpre4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQese4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQesr4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQpsc4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQsre4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQstb4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpQddt4(uint Adr, ref uint Srlen, StringBuilder Srbuf);
		[DllImport("apigpib4.dll")] static extern uint GpTaLaBit4(uint TaLaSts);
		[DllImport("apigpib4.dll")] static extern uint GpBoardsts4(uint Reg, ref uint Preg);
		[DllImport("apigpib4.dll")] static extern uint GpSrqEvent4(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib4.dll")] static extern uint GpSrqEventEx4(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib4.dll")] static extern uint GpSrqOn4();
		[DllImport("apigpib4.dll")] static extern uint GpDevFind4(uint[] Fstb);
		[DllImport("apigpib4.dll")] static extern byte GpInpB4(short Port);
		[DllImport("apigpib4.dll")] static extern short GpInpW4(short Port);
		[DllImport("apigpib4.dll")] static extern int  GpInpD4(short Port);
		[DllImport("apigpib4.dll")] static extern byte GpOutB4(short Port, byte Dat);
		[DllImport("apigpib4.dll")] static extern short GpOutW4(short Port, short Dat);
		[DllImport("apigpib4.dll")] static extern int  GpOutD4(short Port, int Dat);
		[DllImport("apigpib4.dll")] static extern uint GpSetEvent4(uint EventOn);
		[DllImport("apigpib4.dll")] static extern uint GpSetEventSrq4(int hWnd, ushort wMsg, uint SrqOn);
		[DllImport("apigpib4.dll")] static extern uint GpSetEventDet4(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib4.dll")] static extern uint GpSetEventDec4(int hWnd, ushort wMsg, uint DetOn);
		[DllImport("apigpib4.dll")] static extern uint GpSetEventIfc4(int hWnd, ushort wMsg, uint IfcOn);
		[DllImport("apigpib4.dll")] static extern uint GpEnableNextEvent4();
		[DllImport("apigpib4.dll")] static extern uint GpSrqEx4(uint Stb, uint SrqFlag, uint EoiFlag);
		[DllImport("apigpib4.dll")] static extern uint GpUpperCode4(uint UpperCode);
		[DllImport("apigpib4.dll")] static extern uint GpCnvSettings4(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag);
		[DllImport("apigpib4.dll")] static extern uint GpCnvSettingsToStr4(uint PlusFlag, uint Digit, uint CutDown);
		[DllImport("apigpib4.dll")] static extern uint GpCnvStrToDbl4(string Str, ref double DblData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvStrToDblArray4(string Str, double[] DblData, ref uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpCnvStrToFlt4(string Str, ref float FltData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvStrToFltArray4(string Str, float[] FltData, ref uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpCnvDblToStr4(StringBuilder Str, ref uint StrSize, double DblData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvDblArrayToStr4(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpCnvFltToStr4(StringBuilder Str, ref uint StrSize, float FltData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvFltArrayToStr4(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpPollEx4(uint[] Cmd, uint[] Pstb, uint[] Psrq);
		[DllImport("apigpib4.dll")] static extern uint GpSlowMode4(uint SlowTime);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCvSettings4(uint Settings);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCvi4(byte[] Str, ref short ShtData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCviArray4(byte[] Str, short[] ShtData, uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCvs4(byte[] Str, ref float FltData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCvsArray4(byte[] Str, float[] FltData, uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCvd4(byte[] Str, ref double DblData);
		[DllImport("apigpib4.dll")] static extern uint GpCnvCvdArray4(byte[] Str, double[] DblData, uint ArraySize);
		[DllImport("apigpib4.dll")] static extern uint GpTalkEx4(uint[] Cmd, ref uint Srlen, string Srbuf);
        [DllImport("apigpib4.dll")] static extern uint GpTalkEx4(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib4.dll")] static extern uint GpListenEx4(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib4.dll")] static extern uint GpListenEx4(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib4.dll")] static extern uint GpTalkAsync4(uint[] Cmd, ref uint Srlen, string Srbuf);
        [DllImport("apigpib4.dll")] static extern uint GpTalkAsync4(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
        [DllImport("apigpib4.dll")] static extern uint GpListenAsync4(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf);
        [DllImport("apigpib4.dll")] static extern uint GpListenAsync4(uint[] Cmd, ref uint Srlen, byte[] Srbufb);
		[DllImport("apigpib4.dll")] static extern uint GpCommandAsync4(uint[] Cmd);
		[DllImport("apigpib4.dll")] static extern uint GpCheckAsync4(uint WaitFlag, ref uint ErrCode);
		[DllImport("apigpib4.dll")] static extern uint GpStopAsync4();
		[DllImport("apigpib4.dll")] static extern uint GpDevFindEx4(short Pad, short Sad, ref short Lstn);
		[DllImport("apigpib4.dll")] static extern uint GpBoardstsEx4(uint SetFlag, uint Reg, ref uint Preg);
		[DllImport("apigpib4.dll")] static extern uint GpSmoothMode4(uint Mode);
						
		[DllImport("user32.dll")] static extern short GetAsyncKeyState(int vKey);
		// For Help
		[DllImport("user32.dll")] static extern uint WinHelp(int hwnd, string lpHelpFile, int wCommand, uint dwData);

		public Cgpib()
		{
		}

		public uint Ini()
		{
			uint ret = GpIni();
			return ret;
		}

		public uint Ifc(uint IfcTime)
		{
			uint ret = GpIfc(IfcTime);
			return ret;
		}

		public uint Ren()
		{
			uint ret = GpRen();
			return ret;
		}

		public uint Resetren()
		{
			uint ret = GpResetren();
			return ret;
		}

		public uint Talk(uint[] Cmd, uint Srlen, string srBuffer)
		{
			uint ret = GpTalk(Cmd, Srlen, srBuffer);
			return ret;
		}

        public uint TalkBinary(uint[] Cmd, uint Srlen, byte[] srBufb)
        {
            uint ret = GpTalk(Cmd, Srlen, srBufb);
            return ret;
        }

		public uint Listen(uint[] Cmd, ref uint Srlen, StringBuilder srBuffer)
		{
			uint ret = GpListen(Cmd, ref Srlen, srBuffer);
			return ret;
		}

        public uint ListenBinary(uint[] Cmd, ref uint Srlen, byte[] srBufb)
        {
            uint ret = GpListen(Cmd, ref Srlen, srBufb);
            return ret;   
        }

		public uint Poll(uint[] Cmd, uint[] Pstb)
		{
			uint ret = GpPoll(Cmd, Pstb);
			return ret;
		}

		public uint Srq(uint Eoi)
		{
			uint ret = GpSrq(Eoi);
			return ret;
		}

		public uint Stb(uint Stb)
		{
			uint ret = GpStb(Stb);
			return ret;
		}

		public uint Delim(uint Delim, uint Eoi)
		{
			uint ret = GpDelim(Delim, Eoi);
			return ret;
		}

		public uint Timeout(uint Timeout)
		{
			uint ret = GpTimeout(Timeout);
			return ret;
		}

		public uint Chkstb(out uint Stb, out uint Eoi)
		{
			Stb = 0;
			Eoi = 0;
			uint ret = GpChkstb(ref Stb, ref Eoi);
			return ret;
		}

		public uint Readreg(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpReadreg(Reg, ref Preg);
			return ret;
		}

		public uint Dma(uint Dmamode, uint Dmach)
		{
			uint ret = GpDma(Dmamode, Dmach);
			return ret;
		}

		public uint Exit()
		{
			uint ret = GpExit();
			return ret;
		}

		public uint Comand(uint[] Cmd)
		{
			uint ret = GpComand(Cmd);
			return ret;
		}

		public uint Dmainuse()
		{
			uint ret = GpDmainuse();
			return ret;
		}

		public uint Ststop(uint Stp)
		{
			uint ret = GpStstop(Stp);
			return ret;
		}

		public uint Dmastop()
		{
			uint ret = GpDmastop();
			return ret;
		}

		public uint Ppollmode(uint Pmode)
		{
			uint ret = GpPpollmode(Pmode);
			return ret;
		}

		public uint Stppoll(uint[] Cmd, uint Stppu)
		{
			uint ret = GpStppoll(Cmd, Stppu);
			return ret;
		}

		public uint Exppoll(out uint Pprdata)
		{
			Pprdata = 0;
			uint ret = GpExppoll(ref Pprdata);
			return ret;
		}

		public uint Stwait(uint Buscode)
		{
			uint ret = GpStwait(Buscode);
			return ret;
		}

		public uint Waittime(uint Timeout)
		{
			uint ret = GpWaittime(Timeout);
			return ret;
		}

		public uint Readbus(out uint Bussta)
		{
			Bussta = 0;
			uint ret = GpReadbus(ref Bussta);
			return ret;
		}

		public uint Sfile(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpSfile(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Rfile(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpRfile(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Sdc(uint Adr)
		{
			uint ret = GpSdc(Adr);
			return ret;
		}

		public uint Dcl()
		{
			uint ret = GpDcl();
			return ret;
		}

		public uint Get(uint Yradr)
		{
			uint ret = GpGet(Yradr);
			return ret;
		}

		public uint Gtl(uint Adr)
		{
			uint ret = GpGtl(Adr);
			return ret;
		}

		public uint Llo()
		{
			uint ret = GpLlo();
			return ret;
		}

		public uint Tct(uint Adr)
		{
			uint ret = GpTct(Adr);
			return ret;
		}

		public uint Crst(uint Adr)
		{
			uint ret = GpCrst(Adr);
			return ret;
		}

		public uint Copc(uint Adr)
		{
			uint ret = GpCopc(Adr);
			return ret;
		}

		public uint Cwai(uint Adr)
		{
			uint ret = GpCwai(Adr);
			return ret;
		}

		public uint Ccls(uint Adr)
		{
			uint ret = GpCcls(Adr);
			return ret;
		}

		public uint Ctrg(uint Adr)
		{
			uint ret = GpCtrg(Adr);
			return ret;
		}

		public uint Cpre(uint Adr, uint Stb)
		{
			uint ret = GpCpre(Adr, Stb);
			return ret;
		}

		public uint Cese(uint Adr, uint Stb)
		{
			uint ret = GpCese(Adr, Stb);
			return ret;
		}

		public uint Csre(uint Adr, uint Stb)
		{
			uint ret = GpCsre(Adr, Stb);
			return ret;
		}

		public uint Qidn(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQidn(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopt(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopt(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpud(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpud(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qrdt(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQrdt(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qcal(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQcal(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlrn(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlrn(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qtst(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQtst(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopc(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopc(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qemc(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQemc(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qgmc(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQgmc(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlmc(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlmc(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qist(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQist(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpre(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpre(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qese(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQese(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qesr(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQesr(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpsc(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpsc(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qsre(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQsre(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qstb(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQstb(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qddt(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQddt(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint TaLaBit(uint TaLaSts)
		{
			uint ret = GpTaLaBit(TaLaSts);
			return ret;
		}

		public uint Boardsts(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpBoardsts(Reg, ref Preg);
			return ret;
		}

		public uint SrqEvent(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEvent(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqEventEx(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEventEx(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqOn()
		{
			uint ret = GpSrqOn();
			return ret;
		}

		public uint DevFind(uint[] Fstb)
		{
			uint ret = GpDevFind(Fstb);
			return ret;
		}

		public byte InpB(short Port)
		{
			byte ret = GpInpB(Port);
			return ret;
		}

		public short InpW(short Port)
		{
			short ret = GpInpW(Port);
			return ret;
		}
		
		public int InpD(short Port)
		{
			int ret = GpInpD(Port);
			return ret;
		}

		public byte OutB(short Port, byte Dat)
		{
			byte ret = GpOutB(Port, Dat);
			return ret;
		}
		
		public short OutW(short Port, short Dat)
		{
			short ret = GpOutW(Port, Dat);
			return ret;
		}

		public int OutD(short Port, int Dat)
		{
			int ret = OutD(Port, Dat);
			return ret;
		}

		public uint SetEvent(uint EventOn)
		{
			uint ret = GpSetEvent(EventOn);
			return ret;
		}

		public uint SetEventSrq(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSetEventSrq(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SetEventDet(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDet(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventDec(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDec(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventIfc(int hWnd, ushort wMsg, uint IfcOn)
		{
			uint ret = GpSetEventIfc(hWnd, wMsg, IfcOn);
			return ret;
		}

		public uint EnableNextEvent()
		{
			uint ret = GpEnableNextEvent();
			return ret;
		}

		public uint SrqEx(uint Stb, uint SrqFlag, uint EoiFlag)
		{
			uint ret = GpSrqEx(Stb, SrqFlag, EoiFlag);
			return ret;
		}

		public uint UpperCode(uint UpperCode)
		{
			uint ret = GpUpperCode(UpperCode);
			return ret;
		}

		public uint CnvSettings(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag)
		{
			uint ret = GpCnvSettings(HeaderStr, UnitStr, SepStr, SfxFlag);
			return ret;
		}

		public uint CnvSettingsToStr(uint PlusFlag, uint Digit, uint CutDown)
		{
			uint ret = GpCnvSettingsToStr(PlusFlag, Digit, CutDown);
			return ret;
		}

		public uint CnvStrToDbl(string Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvStrToDbl(Str, ref DblData);
			return ret;
		}

		public uint CnvStrToDblArray(string Str, double[] DblData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToDblArray(Str, DblData, ref ArraySize);
			return ret;
		}

		public uint CnvStrToFlt(string Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvStrToFlt(Str, ref FltData);
			return ret;
		}

		public uint CnvStrToFltArray(string Str, float[] FltData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToFltArray(Str, FltData, ref ArraySize);
			return ret;
		}

		public uint CnvDblToStr(StringBuilder Str, ref uint StrSize, double DblData)
		{
			uint ret = GpCnvDblToStr(Str, ref StrSize, DblData);
			return ret;
		}

		public uint CnvDblArrayToStr(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvDblArrayToStr(Str, ref StrSize, DblData, ArraySize);
			return ret;
		}

		public uint CnvFltToStr(StringBuilder Str, ref uint StrSize, float FltData)
		{
			uint ret = GpCnvFltToStr(Str, ref StrSize, FltData);
			return ret;
		}

		public uint CnvFltArrayToStr(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvFltArrayToStr(Str, ref StrSize, FltData, ArraySize);
			return ret;
		}

		public uint PollEx(uint[] Cmd, uint[] Pstb, uint[] Psrq)
		{
			uint ret = GpPollEx(Cmd, Pstb, Psrq);
			return ret;
		}

		public uint SlowMode(uint SlowTime)
		{
			uint ret = GpSlowMode(SlowTime);
			return ret;
		}

		public uint CnvCvSettings(uint Settings)
		{
			uint ret = GpCnvCvSettings(Settings);
			return ret;
		}

		public uint CnvCvi(byte[] Str, out short ShtData)
		{
			ShtData = 0;
			uint ret = GpCnvCvi(Str, ref ShtData);
			return ret;
		}

		public uint CnvCviArray(byte[] Str, short[] ShtData, uint ArraySize)
		{
			uint ret = GpCnvCviArray(Str, ShtData, ArraySize);
			return ret;
		}

		public uint CnvCvs(byte[] Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvCvs(Str, ref FltData);
			return ret;
		}

		public uint CnvCvsArray(byte[] Str, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvCvsArray(Str, FltData, ArraySize);
			return ret;
		}

		public uint CnvCvd(byte[] Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvCvd(Str, ref DblData);
			return ret;
		}

		public uint CnvCvdArray(byte[] Str, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvCvdArray(Str, DblData, ArraySize);
			return ret;
		}

		public uint TalkEx(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkEx(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkExBinary(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkEx(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenEx(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenEx(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenExBinary(uint[] Cmd, ref uint Srlen, byte[] srBufb)
        {
            uint ret = GpListenEx(Cmd, ref Srlen, srBufb);
            return ret;
        }

		public uint TalkAsync(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkAsync(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkAsyncBinary(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkAsync(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenAsync(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenAsync(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenAsyncBinary(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenAsync(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint CommandAsync(uint[] Cmd)
		{
			uint ret = GpCommandAsync(Cmd);
			return ret;
		}

		public uint CheckAsync(uint WaitFlag, out uint ErrCode)
		{
			ErrCode = 0;
			uint ret = GpCheckAsync(WaitFlag, ref ErrCode);
			return ret;
		}

		public uint StopAsync()
		{
			uint ret = GpStopAsync();
			return ret;
		}

		public uint DevFindEx(short Pad, short Sad, out short Lstn)
		{
			Lstn = 0;
			uint ret = GpDevFindEx(Pad, Sad, ref Lstn);
			return ret;
		}

		public uint BoardstsEx(uint SetFlag, uint Reg, ref uint Preg)
		{
			uint ret = GpBoardstsEx(SetFlag, Reg, ref Preg);
			return ret;
		}

		public uint SmoothMode(uint Mode)
		{
			uint ret = GpSmoothMode(Mode);
			return ret;
		}

		/******2******/
		public uint Ini2()
		{
			uint ret = GpIni2();
			return ret;
		}

		public uint Ifc2(uint IfcTime)
		{
			uint ret = GpIfc2(IfcTime);
			return ret;
		}

		public uint Ren2()
		{
			uint ret = GpRen2();
			return ret;
		}

		public uint Resetren2()
		{
			uint ret = GpResetren2();
			return ret;
		}

		public uint Talk2(uint[] Cmd, uint Srlen, string srBuffer)
		{
			uint ret = GpTalk2(Cmd, Srlen, srBuffer);
			return ret;
		}

        public uint TalkBinary2(uint[] Cmd, uint Srlen, byte[] srBufb)
        {
            uint ret = GpTalk2(Cmd, Srlen, srBufb);
            return ret;
        }

		public uint Listen2(uint[] Cmd, ref uint Srlen, StringBuilder srBuffer)
		{
			uint ret = GpListen2(Cmd, ref Srlen, srBuffer);
			return ret;
		}

        public uint ListenBinary2(uint[] Cmd, ref uint Srlen, byte[] srBufb)
        {
            uint ret = GpListen2(Cmd, ref Srlen, srBufb);
            return ret;
        }

		public uint Poll2(uint[] Cmd, uint[] Pstb)
		{
			uint ret = GpPoll2(Cmd, Pstb);
			return ret;
		}

		public uint Srq2(uint Eoi)
		{
			uint ret = GpSrq2(Eoi);
			return ret;
		}

		public uint Stb2(uint Stb)
		{
			uint ret = GpStb2(Stb);
			return ret;
		}

		public uint Delim2(uint Delim, uint Eoi)
		{
			uint ret = GpDelim2(Delim, Eoi);
			return ret;
		}

		public uint Timeout2(uint Timeout)
		{
			uint ret = GpTimeout2(Timeout);
			return ret;
		}

		public uint Chkstb2(out uint Stb, out uint Eoi)
		{
			Stb = 0;
			Eoi = 0;
			uint ret = GpChkstb2(ref Stb, ref Eoi);
			return ret;
		}

		public uint Readreg2(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpReadreg2(Reg, ref Preg);
			return ret;
		}

		public uint Dma2(uint Dmamode, uint Dmach)
		{
			uint ret = GpDma2(Dmamode, Dmach);
			return ret;
		}

		public uint Exit2()
		{
			uint ret = GpExit2();
			return ret;
		}

		public uint Comand2(uint[] Cmd)
		{
			uint ret = GpComand2(Cmd);
			return ret;
		}

		public uint Dmainuse2()
		{
			uint ret = GpDmainuse2();
			return ret;
		}

		public uint Ststop2(uint Stp)
		{
			uint ret = GpStstop2(Stp);
			return ret;
		}

		public uint Dmastop2()
		{
			uint ret = GpDmastop2();
			return ret;
		}

		public uint Ppollmode2(uint Pmode)
		{
			uint ret = GpPpollmode2(Pmode);
			return ret;
		}

		public uint Stppoll2(uint[] Cmd, uint Stppu)
		{
			uint ret = GpStppoll2(Cmd, Stppu);
			return ret;
		}

		public uint Exppoll2(out uint Pprdata)
		{
			Pprdata = 0;
			uint ret = GpExppoll2(ref Pprdata);
			return ret;
		}

		public uint Stwait2(uint Buscode)
		{
			uint ret = GpStwait2(Buscode);
			return ret;
		}

		public uint Waittime2(uint Timeout)
		{
			uint ret = GpWaittime2(Timeout);
			return ret;
		}

		public uint Readbus2(out uint Bussta)
		{
			Bussta = 0;
			uint ret = GpReadbus2(ref Bussta);
			return ret;
		}

		public uint Sfile2(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpSfile2(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Rfile2(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpRfile2(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Sdc2(uint Adr)
		{
			uint ret = GpSdc2(Adr);
			return ret;
		}

		public uint Dcl2()
		{
			uint ret = GpDcl2();
			return ret;
		}

		public uint Get2(uint Yradr)
		{
			uint ret = GpGet2(Yradr);
			return ret;
		}

		public uint Gtl2(uint Adr)
		{
			uint ret = GpGtl2(Adr);
			return ret;
		}

		public uint Llo2()
		{
			uint ret = GpLlo2();
			return ret;
		}

		public uint Tct2(uint Adr)
		{
			uint ret = GpTct2(Adr);
			return ret;
		}

		public uint Crst2(uint Adr)
		{
			uint ret = GpCrst2(Adr);
			return ret;
		}

		public uint Copc2(uint Adr)
		{
			uint ret = GpCopc2(Adr);
			return ret;
		}

		public uint Cwai2(uint Adr)
		{
			uint ret = GpCwai2(Adr);
			return ret;
		}

		public uint Ccls2(uint Adr)
		{
			uint ret = GpCcls2(Adr);
			return ret;
		}

		public uint Ctrg2(uint Adr)
		{
			uint ret = GpCtrg2(Adr);
			return ret;
		}

		public uint Cpre2(uint Adr, uint Stb)
		{
			uint ret = GpCpre2(Adr, Stb);
			return ret;
		}

		public uint Cese2(uint Adr, uint Stb)
		{
			uint ret = GpCese2(Adr, Stb);
			return ret;
		}

		public uint Csre2(uint Adr, uint Stb)
		{
			uint ret = GpCsre2(Adr, Stb);
			return ret;
		}

		public uint Qidn2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQidn2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopt2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopt2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpud2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpud2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qrdt2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQrdt2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qcal2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQcal2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlrn2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlrn2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qtst2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQtst2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopc2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopc2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qemc2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQemc2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qgmc2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQgmc2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlmc2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlmc2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qist2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQist2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpre2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpre2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qese2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQese2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qesr2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQesr2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpsc2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpsc2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qsre2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQsre2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qstb2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQstb2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qddt2(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQddt2(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint TaLaBit2(uint TaLaSts)
		{
			uint ret = GpTaLaBit2(TaLaSts);
			return ret;
		}

		public uint Boardsts2(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpBoardsts2(Reg, ref Preg);
			return ret;
		}

		public uint SrqEvent2(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEvent2(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqEventEx2(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEventEx2(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqOn2()
		{
			uint ret = GpSrqOn2();
			return ret;
		}

		public uint DevFind2(uint[] Fstb)
		{
			uint ret = GpDevFind2(Fstb);
			return ret;
		}

		public byte InpB2(short Port)
		{
			byte ret = GpInpB2(Port);
			return ret;
		}

		public short InpW2(short Port)
		{
			short ret = GpInpW2(Port);
			return ret;
		}
		
		public int InpD2(short Port)
		{
			int ret = GpInpD2(Port);
			return ret;
		}

		public byte OutB2(short Port, byte Dat)
		{
			byte ret = GpOutB2(Port, Dat);
			return ret;
		}
		
		public short OutW2(short Port, short Dat)
		{
			short ret = GpOutW2(Port, Dat);
			return ret;
		}

		public int OutD2(short Port, int Dat)
		{
			int ret = OutD2(Port, Dat);
			return ret;
		}

		public uint SetEvent2(uint EventOn)
		{
			uint ret = GpSetEvent2(EventOn);
			return ret;
		}

		public uint SetEventSrq2(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSetEventSrq2(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SetEventDet2(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDet2(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventDec2(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDec2(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventIfc2(int hWnd, ushort wMsg, uint IfcOn)
		{
			uint ret = GpSetEventIfc2(hWnd, wMsg, IfcOn);
			return ret;
		}

		public uint EnableNextEvent2()
		{
			uint ret = GpEnableNextEvent2();
			return ret;
		}

		public uint SrqEx2(uint Stb, uint SrqFlag, uint EoiFlag)
		{
			uint ret = GpSrqEx2(Stb, SrqFlag, EoiFlag);
			return ret;
		}

		public uint UpperCode2(uint UpperCode)
		{
			uint ret = GpUpperCode2(UpperCode);
			return ret;
		}

		public uint CnvSettings2(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag)
		{
			uint ret = GpCnvSettings2(HeaderStr, UnitStr, SepStr, SfxFlag);
			return ret;
		}

		public uint CnvSettingsToStr2(uint PlusFlag, uint Digit, uint CutDown)
		{
			uint ret = GpCnvSettingsToStr2(PlusFlag, Digit, CutDown);
			return ret;
		}

		public uint CnvStrToDbl2(string Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvStrToDbl2(Str, ref DblData);
			return ret;
		}

		public uint CnvStrToDblArray2(string Str, double[] DblData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToDblArray2(Str, DblData, ref ArraySize);
			return ret;
		}

		public uint CnvStrToFlt2(string Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvStrToFlt2(Str, ref FltData);
			return ret;
		}

		public uint CnvStrToFltArray2(string Str, float[] FltData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToFltArray2(Str, FltData, ref ArraySize);
			return ret;
		}

		public uint CnvDblToStr2(StringBuilder Str, ref uint StrSize, double DblData)
		{
			uint ret = GpCnvDblToStr2(Str, ref StrSize, DblData);
			return ret;
		}

		public uint CnvDblArrayToStr2(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvDblArrayToStr2(Str, ref StrSize, DblData, ArraySize);
			return ret;
		}

		public uint CnvFltToStr2(StringBuilder Str, ref uint StrSize, float FltData)
		{
			uint ret = GpCnvFltToStr2(Str, ref StrSize, FltData);
			return ret;
		}

		public uint CnvFltArrayToStr2(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvFltArrayToStr2(Str, ref StrSize, FltData, ArraySize);
			return ret;
		}

		public uint PollEx2(uint[] Cmd, uint[] Pstb, uint[] Psrq)
		{
			uint ret = GpPollEx2(Cmd, Pstb, Psrq);
			return ret;
		}

		public uint SlowMode2(uint SlowTime)
		{
			uint ret = GpSlowMode2(SlowTime);
			return ret;
		}

		public uint CnvCvSettings2(uint Settings)
		{
			uint ret = GpCnvCvSettings2(Settings);
			return ret;
		}

		public uint CnvCvi2(byte[] Str, out short ShtData)
		{
			ShtData = 0;
			uint ret = GpCnvCvi2(Str, ref ShtData);
			return ret;
		}

		public uint CnvCviArray2(byte[] Str, short[] ShtData, uint ArraySize)
		{
			uint ret = GpCnvCviArray2(Str, ShtData, ArraySize);
			return ret;
		}

		public uint CnvCvs2(byte[] Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvCvs2(Str, ref FltData);
			return ret;
		}

		public uint CnvCvsArray2(byte[] Str, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvCvsArray2(Str, FltData, ArraySize);
			return ret;
		}

		public uint CnvCvd2(byte[] Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvCvd2(Str, ref DblData);
			return ret;
		}

		public uint CnvCvdArray2(byte[] Str, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvCvdArray2(Str, DblData, ArraySize);
			return ret;
		}

		public uint TalkEx2(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkEx2(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkExBinary2(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkEx2(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenEx2(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenEx2(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenExBinary2(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenEx2(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint TalkAsync2(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkAsync2(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkAsyncBinary2(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkAsync2(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenAsync2(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenAsync2(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenAsyncBinary2(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenAsync2(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint CommandAsync2(uint[] Cmd)
		{
			uint ret = GpCommandAsync2(Cmd);
			return ret;
		}

		public uint CheckAsync2(uint WaitFlag, out uint ErrCode)
		{
			ErrCode = 0;
			uint ret = GpCheckAsync2(WaitFlag, ref ErrCode);
			return ret;
		}

		public uint StopAsync2()
		{
			uint ret = GpStopAsync2();
			return ret;
		}

		public uint DevFindEx2(short Pad, short Sad, out short Lstn)
		{
			Lstn = 0;
			uint ret = GpDevFindEx2(Pad, Sad, ref Lstn);
			return ret;
		}

		public uint BoardstsEx2(uint SetFlag, uint Reg, ref uint Preg)
		{
			uint ret = GpBoardstsEx2(SetFlag, Reg, ref Preg);
			return ret;
		}

		public uint SmoothMode2(uint Mode)
		{
			uint ret = GpSmoothMode2(Mode);
			return ret;
		}
		
		/******3******/
		public uint Ini3()
		{
			uint ret = GpIni3();
			return ret;
		}

		public uint Ifc3(uint IfcTime)
		{
			uint ret = GpIfc3(IfcTime);
			return ret;
		}

		public uint Ren3()
		{
			uint ret = GpRen3();
			return ret;
		}

		public uint Resetren3()
		{
			uint ret = GpResetren3();
			return ret;
		}

		public uint Talk3(uint[] Cmd, uint Srlen, string srBuffer)
		{
			uint ret = GpTalk3(Cmd, Srlen, srBuffer);
			return ret;
		}

        public uint TalkBinary3(uint[] Cmd, uint Srlen, byte[] srBufb)
        {
            uint ret = GpTalk3(Cmd, Srlen, srBufb);
            return ret;
        }

		public uint Listen3(uint[] Cmd, ref uint Srlen, StringBuilder srBuffer)
		{
			uint ret = GpListen3(Cmd, ref Srlen, srBuffer);
			return ret;
		}

        public uint ListenBinary3(uint[] Cmd, ref uint Srlen, byte[] srBufb)
        {
            uint ret = GpListen3(Cmd, ref Srlen, srBufb);
            return ret;
        }

		public uint Poll3(uint[] Cmd, uint[] Pstb)
		{
			uint ret = GpPoll3(Cmd, Pstb);
			return ret;
		}

		public uint Srq3(uint Eoi)
		{
			uint ret = GpSrq3(Eoi);
			return ret;
		}

		public uint Stb3(uint Stb)
		{
			uint ret = GpStb3(Stb);
			return ret;
		}

		public uint Delim3(uint Delim, uint Eoi)
		{
			uint ret = GpDelim3(Delim, Eoi);
			return ret;
		}

		public uint Timeout3(uint Timeout)
		{
			uint ret = GpTimeout3(Timeout);
			return ret;
		}

		public uint Chkstb3(out uint Stb, out uint Eoi)
		{
			Stb = 0;
			Eoi = 0;
			uint ret = GpChkstb3(ref Stb, ref Eoi);
			return ret;
		}

		public uint Readreg3(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpReadreg3(Reg, ref Preg);
			return ret;
		}

		public uint Dma3(uint Dmamode, uint Dmach)
		{
			uint ret = GpDma3(Dmamode, Dmach);
			return ret;
		}

		public uint Exit3()
		{
			uint ret = GpExit3();
			return ret;
		}

		public uint Comand3(uint[] Cmd)
		{
			uint ret = GpComand3(Cmd);
			return ret;
		}

		public uint Dmainuse3()
		{
			uint ret = GpDmainuse3();
			return ret;
		}

		public uint Ststop3(uint Stp)
		{
			uint ret = GpStstop3(Stp);
			return ret;
		}

		public uint Dmastop3()
		{
			uint ret = GpDmastop3();
			return ret;
		}

		public uint Ppollmode3(uint Pmode)
		{
			uint ret = GpPpollmode3(Pmode);
			return ret;
		}

		public uint Stppoll3(uint[] Cmd, uint Stppu)
		{
			uint ret = GpStppoll3(Cmd, Stppu);
			return ret;
		}

		public uint Exppoll3(out uint Pprdata)
		{
			Pprdata = 0;
			uint ret = GpExppoll3(ref Pprdata);
			return ret;
		}

		public uint Stwait3(uint Buscode)
		{
			uint ret = GpStwait3(Buscode);
			return ret;
		}

		public uint Waittime3(uint Timeout)
		{
			uint ret = GpWaittime3(Timeout);
			return ret;
		}

		public uint Readbus3(out uint Bussta)
		{
			Bussta = 0;
			uint ret = GpReadbus3(ref Bussta);
			return ret;
		}

		public uint Sfile3(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpSfile3(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Rfile3(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpRfile3(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Sdc3(uint Adr)
		{
			uint ret = GpSdc3(Adr);
			return ret;
		}

		public uint Dcl3()
		{
			uint ret = GpDcl3();
			return ret;
		}

		public uint Get3(uint Yradr)
		{
			uint ret = GpGet3(Yradr);
			return ret;
		}

		public uint Gtl3(uint Adr)
		{
			uint ret = GpGtl3(Adr);
			return ret;
		}

		public uint Llo3()
		{
			uint ret = GpLlo3();
			return ret;
		}

		public uint Tct3(uint Adr)
		{
			uint ret = GpTct3(Adr);
			return ret;
		}

		public uint Crst3(uint Adr)
		{
			uint ret = GpCrst3(Adr);
			return ret;
		}

		public uint Copc3(uint Adr)
		{
			uint ret = GpCopc3(Adr);
			return ret;
		}

		public uint Cwai3(uint Adr)
		{
			uint ret = GpCwai3(Adr);
			return ret;
		}

		public uint Ccls3(uint Adr)
		{
			uint ret = GpCcls3(Adr);
			return ret;
		}

		public uint Ctrg3(uint Adr)
		{
			uint ret = GpCtrg3(Adr);
			return ret;
		}

		public uint Cpre3(uint Adr, uint Stb)
		{
			uint ret = GpCpre3(Adr, Stb);
			return ret;
		}

		public uint Cese3(uint Adr, uint Stb)
		{
			uint ret = GpCese3(Adr, Stb);
			return ret;
		}

		public uint Csre3(uint Adr, uint Stb)
		{
			uint ret = GpCsre3(Adr, Stb);
			return ret;
		}

		public uint Qidn3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQidn3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopt3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopt3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpud3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpud3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qrdt3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQrdt3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qcal3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQcal3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlrn3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlrn3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qtst3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQtst3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopc3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopc3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qemc3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQemc3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qgmc3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQgmc3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlmc3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlmc3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qist3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQist3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpre3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpre3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qese3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQese3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qesr3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQesr3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpsc3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpsc3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qsre3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQsre3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qstb3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQstb3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qddt3(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQddt3(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint TaLaBit3(uint TaLaSts)
		{
			uint ret = GpTaLaBit3(TaLaSts);
			return ret;
		}

		public uint Boardsts3(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpBoardsts3(Reg, ref Preg);
			return ret;
		}

		public uint SrqEvent3(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEvent3(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqEventEx3(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEventEx3(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqOn3()
		{
			uint ret = GpSrqOn3();
			return ret;
		}

		public uint DevFind3(uint[] Fstb)
		{
			uint ret = GpDevFind3(Fstb);
			return ret;
		}

		public byte InpB3(short Port)
		{
			byte ret = GpInpB3(Port);
			return ret;
		}

		public short InpW3(short Port)
		{
			short ret = GpInpW3(Port);
			return ret;
		}
		
		public int InpD3(short Port)
		{
			int ret = GpInpD3(Port);
			return ret;
		}

		public byte OutB3(short Port, byte Dat)
		{
			byte ret = GpOutB3(Port, Dat);
			return ret;
		}
		
		public short OutW3(short Port, short Dat)
		{
			short ret = GpOutW3(Port, Dat);
			return ret;
		}

		public int OutD3(short Port, int Dat)
		{
			int ret = OutD3(Port, Dat);
			return ret;
		}

		public uint SetEvent3(uint EventOn)
		{
			uint ret = GpSetEvent3(EventOn);
			return ret;
		}

		public uint SetEventSrq3(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSetEventSrq3(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SetEventDet3(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDet3(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventDec3(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDec3(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventIfc3(int hWnd, ushort wMsg, uint IfcOn)
		{
			uint ret = GpSetEventIfc3(hWnd, wMsg, IfcOn);
			return ret;
		}

		public uint EnableNextEvent3()
		{
			uint ret = GpEnableNextEvent3();
			return ret;
		}

		public uint SrqEx3(uint Stb, uint SrqFlag, uint EoiFlag)
		{
			uint ret = GpSrqEx3(Stb, SrqFlag, EoiFlag);
			return ret;
		}

		public uint UpperCode3(uint UpperCode)
		{
			uint ret = GpUpperCode3(UpperCode);
			return ret;
		}

		public uint CnvSettings3(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag)
		{
			uint ret = GpCnvSettings3(HeaderStr, UnitStr, SepStr, SfxFlag);
			return ret;
		}

		public uint CnvSettingsToStr3(uint PlusFlag, uint Digit, uint CutDown)
		{
			uint ret = GpCnvSettingsToStr3(PlusFlag, Digit, CutDown);
			return ret;
		}

		public uint CnvStrToDbl3(string Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvStrToDbl3(Str, ref DblData);
			return ret;
		}

		public uint CnvStrToDblArray3(string Str, double[] DblData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToDblArray3(Str, DblData, ref ArraySize);
			return ret;
		}

		public uint CnvStrToFlt3(string Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvStrToFlt3(Str, ref FltData);
			return ret;
		}

		public uint CnvStrToFltArray3(string Str, float[] FltData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToFltArray3(Str, FltData, ref ArraySize);
			return ret;
		}

		public uint CnvDblToStr3(StringBuilder Str, ref uint StrSize, double DblData)
		{
			uint ret = GpCnvDblToStr3(Str, ref StrSize, DblData);
			return ret;
		}

		public uint CnvDblArrayToStr3(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvDblArrayToStr3(Str, ref StrSize, DblData, ArraySize);
			return ret;
		}

		public uint CnvFltToStr3(StringBuilder Str, ref uint StrSize, float FltData)
		{
			uint ret = GpCnvFltToStr3(Str, ref StrSize, FltData);
			return ret;
		}

		public uint CnvFltArrayToStr3(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvFltArrayToStr3(Str, ref StrSize, FltData, ArraySize);
			return ret;
		}

		public uint PollEx3(uint[] Cmd, uint[] Pstb, uint[] Psrq)
		{
			uint ret = GpPollEx3(Cmd, Pstb, Psrq);
			return ret;
		}

		public uint SlowMode3(uint SlowTime)
		{
			uint ret = GpSlowMode3(SlowTime);
			return ret;
		}

		public uint CnvCvSettings3(uint Settings)
		{
			uint ret = GpCnvCvSettings3(Settings);
			return ret;
		}

		public uint CnvCvi3(byte[] Str, out short ShtData)
		{
			ShtData = 0;
			uint ret = GpCnvCvi3(Str, ref ShtData);
			return ret;
		}

		public uint CnvCviArray3(byte[] Str, short[] ShtData, uint ArraySize)
		{
			uint ret = GpCnvCviArray3(Str, ShtData, ArraySize);
			return ret;
		}

		public uint CnvCvs3(byte[] Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvCvs3(Str, ref FltData);
			return ret;
		}

		public uint CnvCvsArray3(byte[] Str, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvCvsArray3(Str, FltData, ArraySize);
			return ret;
		}

		public uint CnvCvd3(byte[] Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvCvd3(Str, ref DblData);
			return ret;
		}

		public uint CnvCvdArray3(byte[] Str, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvCvdArray3(Str, DblData, ArraySize);
			return ret;
		}

		public uint TalkEx3(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkEx3(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkExBinary3(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkEx3(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenEx3(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenEx3(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenExBinary3(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenEx3(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint TalkAsync3(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkAsync3(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkAsyncBinary3(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkAsync3(Cmd, ref Srlen, Srbufb);
            return ret;
        }

        public uint ListenAsync3(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenAsync3(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenAsyncBinary3(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenAsync3(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint CommandAsync3(uint[] Cmd)
		{
			uint ret = GpCommandAsync3(Cmd);
			return ret;
		}

		public uint CheckAsync3(uint WaitFlag, out uint ErrCode)
		{
			ErrCode = 0;
			uint ret = GpCheckAsync3(WaitFlag, ref ErrCode);
			return ret;
		}

		public uint StopAsync3()
		{
			uint ret = GpStopAsync3();
			return ret;
		}

		public uint DevFindEx3(short Pad, short Sad, out short Lstn)
		{
			Lstn = 0;
			uint ret = GpDevFindEx3(Pad, Sad, ref Lstn);
			return ret;
		}

		public uint BoardstsEx3(uint SetFlag, uint Reg, ref uint Preg)
		{
			uint ret = GpBoardstsEx3(SetFlag, Reg, ref Preg);
			return ret;
		}

		public uint SmoothMode3(uint Mode)
		{
			uint ret = GpSmoothMode3(Mode);
			return ret;
		}

		/******4******/
		public uint Ini4()
		{
			uint ret = GpIni4();
			return ret;
		}

		public uint Ifc4(uint IfcTime)
		{
			uint ret = GpIfc4(IfcTime);
			return ret;
		}

		public uint Ren4()
		{
			uint ret = GpRen4();
			return ret;
		}

		public uint Resetren4()
		{
			uint ret = GpResetren4();
			return ret;
		}

		public uint Talk4(uint[] Cmd, uint Srlen, string srBuffer)
		{
			uint ret = GpTalk4(Cmd, Srlen, srBuffer);
			return ret;
		}

        public uint TalkBinary4(uint[] Cmd, uint Srlen, byte[] srBufb)
        {
            uint ret = GpTalk4(Cmd, Srlen, srBufb);
            return ret;
        }

		public uint Listen4(uint[] Cmd, ref uint Srlen, StringBuilder srBuffer)
		{
			uint ret = GpListen4(Cmd, ref Srlen, srBuffer);
			return ret;
		}

        public uint ListenBinary4(uint[] Cmd, ref uint Srlen, byte[] srBufb)
        {
            uint ret = GpListen4(Cmd, ref Srlen, srBufb);
            return ret;
        }

		public uint Poll4(uint[] Cmd, uint[] Pstb)
		{
			uint ret = GpPoll4(Cmd, Pstb);
			return ret;
		}

		public uint Srq4(uint Eoi)
		{
			uint ret = GpSrq4(Eoi);
			return ret;
		}

		public uint Stb4(uint Stb)
		{
			uint ret = GpStb4(Stb);
			return ret;
		}

		public uint Delim4(uint Delim, uint Eoi)
		{
			uint ret = GpDelim4(Delim, Eoi);
			return ret;
		}

		public uint Timeout4(uint Timeout)
		{
			uint ret = GpTimeout4(Timeout);
			return ret;
		}

		public uint Chkstb4(out uint Stb, out uint Eoi)
		{
			Stb = 0;
			Eoi = 0;
			uint ret = GpChkstb4(ref Stb, ref Eoi);
			return ret;
		}

		public uint Readreg4(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpReadreg4(Reg, ref Preg);
			return ret;
		}

		public uint Dma4(uint Dmamode, uint Dmach)
		{
			uint ret = GpDma4(Dmamode, Dmach);
			return ret;
		}

		public uint Exit4()
		{
			uint ret = GpExit4();
			return ret;
		}

		public uint Comand4(uint[] Cmd)
		{
			uint ret = GpComand4(Cmd);
			return ret;
		}

		public uint Dmainuse4()
		{
			uint ret = GpDmainuse4();
			return ret;
		}

		public uint Ststop4(uint Stp)
		{
			uint ret = GpStstop4(Stp);
			return ret;
		}

		public uint Dmastop4()
		{
			uint ret = GpDmastop4();
			return ret;
		}

		public uint Ppollmode4(uint Pmode)
		{
			uint ret = GpPpollmode4(Pmode);
			return ret;
		}

		public uint Stppoll4(uint[] Cmd, uint Stppu)
		{
			uint ret = GpStppoll4(Cmd, Stppu);
			return ret;
		}

		public uint Exppoll4(out uint Pprdata)
		{
			Pprdata = 0;
			uint ret = GpExppoll4(ref Pprdata);
			return ret;
		}

		public uint Stwait4(uint Buscode)
		{
			uint ret = GpStwait4(Buscode);
			return ret;
		}

		public uint Waittime4(uint Timeout)
		{
			uint ret = GpWaittime4(Timeout);
			return ret;
		}

		public uint Readbus4(out uint Bussta)
		{
			Bussta = 0;
			uint ret = GpReadbus4(ref Bussta);
			return ret;
		}

		public uint Sfile4(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpSfile4(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Rfile4(uint[] Cmd, uint Srlen, string Fname)
		{
			uint ret = GpRfile4(Cmd, Srlen, Fname);
			return ret;
		}

		public uint Sdc4(uint Adr)
		{
			uint ret = GpSdc4(Adr);
			return ret;
		}

		public uint Dcl4()
		{
			uint ret = GpDcl4();
			return ret;
		}

		public uint Get4(uint Yradr)
		{
			uint ret = GpGet4(Yradr);
			return ret;
		}

		public uint Gtl4(uint Adr)
		{
			uint ret = GpGtl4(Adr);
			return ret;
		}

		public uint Llo4()
		{
			uint ret = GpLlo4();
			return ret;
		}

		public uint Tct4(uint Adr)
		{
			uint ret = GpTct4(Adr);
			return ret;
		}

		public uint Crst4(uint Adr)
		{
			uint ret = GpCrst4(Adr);
			return ret;
		}

		public uint Copc4(uint Adr)
		{
			uint ret = GpCopc4(Adr);
			return ret;
		}

		public uint Cwai4(uint Adr)
		{
			uint ret = GpCwai4(Adr);
			return ret;
		}

		public uint Ccls4(uint Adr)
		{
			uint ret = GpCcls4(Adr);
			return ret;
		}

		public uint Ctrg4(uint Adr)
		{
			uint ret = GpCtrg4(Adr);
			return ret;
		}

		public uint Cpre4(uint Adr, uint Stb)
		{
			uint ret = GpCpre4(Adr, Stb);
			return ret;
		}

		public uint Cese4(uint Adr, uint Stb)
		{
			uint ret = GpCese4(Adr, Stb);
			return ret;
		}

		public uint Csre4(uint Adr, uint Stb)
		{
			uint ret = GpCsre4(Adr, Stb);
			return ret;
		}

		public uint Qidn4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQidn4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopt4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopt4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpud4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpud4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qrdt4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQrdt4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qcal4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQcal4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlrn4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlrn4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qtst4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQtst4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qopc4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQopc4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qemc4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQemc4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qgmc4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQgmc4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qlmc4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQlmc4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qist4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQist4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpre4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpre4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qese4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQese4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qesr4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQesr4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qpsc4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQpsc4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qsre4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQsre4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qstb4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQstb4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint Qddt4(uint Adr, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpQddt4(Adr, ref Srlen, Srbuf);
			return ret;
		}

		public uint TaLaBit4(uint TaLaSts)
		{
			uint ret = GpTaLaBit4(TaLaSts);
			return ret;
		}

		public uint Boardsts4(uint Reg, out uint Preg)
		{
			Preg = 0;
			uint ret = GpBoardsts4(Reg, ref Preg);
			return ret;
		}

		public uint SrqEvent4(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEvent4(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqEventEx4(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSrqEventEx4(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SrqOn4()
		{
			uint ret = GpSrqOn4();
			return ret;
		}

		public uint DevFind4(uint[] Fstb)
		{
			uint ret = GpDevFind4(Fstb);
			return ret;
		}

		public byte InpB4(short Port)
		{
			byte ret = GpInpB4(Port);
			return ret;
		}

		public short InpW4(short Port)
		{
			short ret = GpInpW4(Port);
			return ret;
		}
		
		public int InpD4(short Port)
		{
			int ret = GpInpD4(Port);
			return ret;
		}

		public byte OutB4(short Port, byte Dat)
		{
			byte ret = GpOutB4(Port, Dat);
			return ret;
		}
		
		public short OutW4(short Port, short Dat)
		{
			short ret = GpOutW4(Port, Dat);
			return ret;
		}

		public int OutD4(short Port, int Dat)
		{
			int ret = OutD4(Port, Dat);
			return ret;
		}

		public uint SetEvent4(uint EventOn)
		{
			uint ret = GpSetEvent4(EventOn);
			return ret;
		}

		public uint SetEventSrq4(int hWnd, ushort wMsg, uint SrqOn)
		{
			uint ret = GpSetEventSrq4(hWnd, wMsg, SrqOn);
			return ret;
		}

		public uint SetEventDet4(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDet4(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventDec4(int hWnd, ushort wMsg, uint DetOn)
		{
			uint ret = GpSetEventDec4(hWnd, wMsg, DetOn);
			return ret;
		}

		public uint SetEventIfc4(int hWnd, ushort wMsg, uint IfcOn)
		{
			uint ret = GpSetEventIfc4(hWnd, wMsg, IfcOn);
			return ret;
		}

		public uint EnableNextEvent4()
		{
			uint ret = GpEnableNextEvent4();
			return ret;
		}

		public uint SrqEx4(uint Stb, uint SrqFlag, uint EoiFlag)
		{
			uint ret = GpSrqEx4(Stb, SrqFlag, EoiFlag);
			return ret;
		}

		public uint UpperCode4(uint UpperCode)
		{
			uint ret = GpUpperCode4(UpperCode);
			return ret;
		}

		public uint CnvSettings4(string HeaderStr, string UnitStr, string SepStr, uint SfxFlag)
		{
			uint ret = GpCnvSettings4(HeaderStr, UnitStr, SepStr, SfxFlag);
			return ret;
		}

		public uint CnvSettingsToStr4(uint PlusFlag, uint Digit, uint CutDown)
		{
			uint ret = GpCnvSettingsToStr4(PlusFlag, Digit, CutDown);
			return ret;
		}

		public uint CnvStrToDbl4(string Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvStrToDbl4(Str, ref DblData);
			return ret;
		}

		public uint CnvStrToDblArray4(string Str, double[] DblData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToDblArray4(Str, DblData, ref ArraySize);
			return ret;
		}

		public uint CnvStrToFlt4(string Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvStrToFlt4(Str, ref FltData);
			return ret;
		}

		public uint CnvStrToFltArray4(string Str, float[] FltData, ref uint ArraySize)
		{
			uint ret = GpCnvStrToFltArray4(Str, FltData, ref ArraySize);
			return ret;
		}

		public uint CnvDblToStr4(StringBuilder Str, ref uint StrSize, double DblData)
		{
			uint ret = GpCnvDblToStr4(Str, ref StrSize, DblData);
			return ret;
		}

		public uint CnvDblArrayToStr4(StringBuilder Str, ref uint StrSize, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvDblArrayToStr4(Str, ref StrSize, DblData, ArraySize);
			return ret;
		}

		public uint CnvFltToStr4(StringBuilder Str, ref uint StrSize, float FltData)
		{
			uint ret = GpCnvFltToStr4(Str, ref StrSize, FltData);
			return ret;
		}

		public uint CnvFltArrayToStr4(StringBuilder Str, ref uint StrSize, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvFltArrayToStr4(Str, ref StrSize, FltData, ArraySize);
			return ret;
		}

		public uint PollEx4(uint[] Cmd, uint[] Pstb, uint[] Psrq)
		{
			uint ret = GpPollEx4(Cmd, Pstb, Psrq);
			return ret;
		}

		public uint SlowMode4(uint SlowTime)
		{
			uint ret = GpSlowMode4(SlowTime);
			return ret;
		}

		public uint CnvCvSettings4(uint Settings)
		{
			uint ret = GpCnvCvSettings4(Settings);
			return ret;
		}

		public uint CnvCvi4(byte[] Str, out short ShtData)
		{
			ShtData = 0;
			uint ret = GpCnvCvi4(Str, ref ShtData);
			return ret;
		}

		public uint CnvCviArray4(byte[] Str, short[] ShtData, uint ArraySize)
		{
			uint ret = GpCnvCviArray4(Str, ShtData, ArraySize);
			return ret;
		}

		public uint CnvCvs4(byte[] Str, out float FltData)
		{
			FltData = 0;
			uint ret = GpCnvCvs4(Str, ref FltData);
			return ret;
		}

		public uint CnvCvsArray4(byte[] Str, float[] FltData, uint ArraySize)
		{
			uint ret = GpCnvCvsArray4(Str, FltData, ArraySize);
			return ret;
		}

		public uint CnvCvd4(byte[] Str, out double DblData)
		{
			DblData = 0;
			uint ret = GpCnvCvd4(Str, ref DblData);
			return ret;
		}

		public uint CnvCvdArray4(byte[] Str, double[] DblData, uint ArraySize)
		{
			uint ret = GpCnvCvdArray4(Str, DblData, ArraySize);
			return ret;
		}

		public uint TalkEx4(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkEx4(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkExBinary4(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkEx4(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenEx4(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenEx4(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenExBinary4(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenEx4(Cmd, ref Srlen, Srbufb);
            return ret;
        }

        public uint TalkAsync4(uint[] Cmd, ref uint Srlen, string Srbuf)
		{
			uint ret = GpTalkAsync4(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint TalkAsyncBinary4(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpTalkAsync4(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint ListenAsync4(uint[] Cmd, ref uint Srlen, StringBuilder Srbuf)
		{
			uint ret = GpListenAsync4(Cmd, ref Srlen, Srbuf);
			return ret;
		}

        public uint ListenAsyncBinary4(uint[] Cmd, ref uint Srlen, byte[] Srbufb)
        {
            uint ret = GpListenAsync4(Cmd, ref Srlen, Srbufb);
            return ret;
        }

		public uint CommandAsync4(uint[] Cmd)
		{
			uint ret = GpCommandAsync4(Cmd);
			return ret;
		}

		public uint CheckAsync4(uint WaitFlag, out uint ErrCode)
		{
			ErrCode = 0;
			uint ret = GpCheckAsync4(WaitFlag, ref ErrCode);
			return ret;
		}

		public uint StopAsync4()
		{
			uint ret = GpStopAsync4();
			return ret;
		}

		public uint DevFindEx4(short Pad, short Sad, out short Lstn)
		{
			Lstn = 0;
			uint ret = GpDevFindEx4(Pad, Sad, ref Lstn);
			return ret;
		}

		public uint BoardstsEx4(uint SetFlag, uint Reg, ref uint Preg)
		{
			uint ret = GpBoardstsEx4(SetFlag, Reg, ref Preg);
			return ret;
		}

		public uint SmoothMode4(uint Mode)
		{
			uint ret = GpSmoothMode4(Mode);
			return ret;
		}

		public short gpGetAsyncKeyState(int vKey)
		{
			short ret = GetAsyncKeyState(vKey);
			return ret;
		}

		public void Help(int hwnd, string lpHelpFile, int wCommand, uint dwData)
		{
			WinHelp(hwnd, lpHelpFile, wCommand, dwData);
		}
	}
}

