Option Strict Off
Option Explicit On

Imports System.Text

Module SubFunc

    '///// Win32Api /////////////////////////////////////////////////////////////////////////
    Public Declare Function GetAsyncKeyState Lib "user32" (ByVal vKey As Integer) As Short

    '///// ｢SubFunc.bas｣で使用されるグローバル変数 //////////////////////////////////////////
    Public CmdNum As Integer                        'コマンド数
    Public Mode As Integer                          'マスタ(=0)かスレーブ(=1)の判別
    Public MyAddr As Integer                        'マイアドレス(新しいVer)
    Public YrAddr As Integer                        '相手機器アドレス(新しいVer)
    Public Cmd(30) As Integer                       'メッセージ(コマンド)
    Public Cnt As Integer                           '繰り返す回数など
    Public Delim As Integer                         'デリミタ
    Public Eoi As Integer                           'EOI
    Public Timeout As Integer                       'タイムアウト
    Public Dmamode As Integer                       'DMAモード
    Public DmaPos As Integer                        'DMAチャネル
    Public Ret As Integer                           '戻り値
    Public Srbuf As New String("", 10000)           '文字列のバッファ
    Public Srlen As Integer                         '文字列の長さ
    Public ErrText As String                        'エラー文字列
    Public RetTmp As Integer                        '一時的な戻り値
    Public pCmd As IntPtr                           'Cmd配列用IntPtr

    '///// [ CheckRet 関数 ] ////////////////////////////////////////////////////////////////
    Public Function CheckRet(ByRef FuncStr As String, ByRef RetCode As Integer, ByRef Text As String) As Integer
        Dim RetSts As Integer
        Text = FuncStr & " : 正常に終了しました｡"
        CheckRet = RetCode And &HFFS
        RetSts = 0
        If (CheckRet >= 3) Then              'CheckRetが３以上でエラー
            RetSts = 1                        'そしてコードに対するエラーを文字列にします。
            If (CheckRet = 80) Then Text = FuncStr & " : I/Oアドレスエラーです、またはGpIni未実行エラーです。" : GoTo CheckStatus
            If (CheckRet = 82) Then Text = FuncStr & " : レジストリ設定のエラーです。" : GoTo CheckStatus
            If (CheckRet = 128) Then Text = FuncStr & " : データ受信オーバー(受信)又は[SRQ]は上がっていません(ポーリング)" : GoTo CheckStatus
            If (CheckRet = 140) Then Text = FuncStr & " : 非同期関数の実行中です" : GoTo CheckStatus
            If (CheckRet = 141) Then Text = FuncStr & " : 非同期関数が強制終了されました" : GoTo CheckStatus
            If (CheckRet = 190) Then Text = FuncStr & " : イベントオブジェクトが作成できません" : GoTo CheckStatus
            If (CheckRet = 200) Then Text = FuncStr & " : スレッドが作成できません。" : GoTo CheckStatus
            If (CheckRet = 201) Then Text = FuncStr & " : 他のイベント発生関数が実行中です。" : GoTo CheckStatus
            If (CheckRet = 210) Then Text = FuncStr & " : DMAが設定できませんでした。" : GoTo CheckStatus
            If (CheckRet = 240) Then Text = FuncStr & " : [Esc]キーが押されました。" : GoTo CheckStatus
            If (CheckRet = 241) Then Text = FuncStr & " : File入出力エラーです。" : GoTo CheckStatus
            If (CheckRet = 242) Then Text = FuncStr & " : アドレス指定が間違っています。" : GoTo CheckStatus
            If (CheckRet = 243) Then Text = FuncStr & " : バッファ指定エラーです。" : GoTo CheckStatus
            If (CheckRet = 244) Then Text = FuncStr & " : 配列サイズエラーです。" : GoTo CheckStatus
            If (CheckRet = 245) Then Text = FuncStr & " : バッファが小さすぎます。" : GoTo CheckStatus
            If (CheckRet = 246) Then Text = FuncStr & " : 不正なオブジェクト名です。" : GoTo CheckStatus
            If (CheckRet = 247) Then Text = FuncStr & " : デバイス名の横のチェックが無効です。" : GoTo CheckStatus
            If (CheckRet = 248) Then Text = FuncStr & " : 不正なデータ型です。" : GoTo CheckStatus
            If (CheckRet = 249) Then Text = FuncStr & " : これ以上デバイスを追加できません。" : GoTo CheckStatus
            If (CheckRet = 250) Then Text = FuncStr & " : デバイス名が見つかりません。" : GoTo CheckStatus
            If (CheckRet = 251) Then Text = FuncStr & " : デリミタがデバイス間で違っています。" : GoTo CheckStatus
            If (CheckRet = 252) Then Text = FuncStr & " : GP-IBエラーです。確認してください。" : GoTo CheckStatus
            If (CheckRet = 253) Then Text = FuncStr & " : デリミタのみを受信しました。" : GoTo CheckStatus
            If (CheckRet = 254) Then Text = FuncStr & " : タイムアウトしました。" : GoTo CheckStatus
            If (CheckRet = 255) Then Text = FuncStr & " : パラメータエラー、または不正呼び出しです。" : GoTo CheckStatus
        End If
CheckStatus:
        '----- IFC & SRQ 受信テータスのメッセージ ------
        CheckRet = RetCode And &HFF00S
        If (CheckRet = &H100S) Then Text = Text & " -SRQを受信[ステータス]" : GoTo CheckEnd
        If (CheckRet = &H200S) Then Text = Text & " -IFCを受信[ステータス]" : GoTo CheckEnd
        If (CheckRet = &H300S) Then Text = Text & " -SRQとIFCを受信[ステータス]"
CheckEnd:
        CheckRet = RetSts

    End Function

    '///// [ AddCommand 関数 ] //////////////////////////////////////////////////////////////
    Public Function AddCommand(ByRef CommandType As Integer, ByRef CommandNum As Short) As Boolean
        Dim ErrMsg As String                            'エラーメッセージ用

        If (CmdNum > 30) Then                           'メッセージが30以上の時
            ErrMsg = "これ以上設定できません。"
            MsgBox(ErrMsg)
            AddCommand = False
            Exit Function
        End If
        If (CommandNum = 2) Then                        'メッセージに相手機器アドレス
            Cmd(CmdNum) = (YrAddr Or &H20S)
            CmdNum = CmdNum + 1
        End If
        Cmd(CmdNum) = CommandType                       'どのメッセージか値で渡される。
        CmdNum = CmdNum + 1
        AddCommand = True

    End Function

    '///// [ DispCommandList 関数 ] /////////////////////////////////////////////////////////
    Public Function DispCommandList() As String
        Dim TxtRet As Integer                           '16進メッセージ用
        Dim TmpString, Txt As String                    'TmpString = 作成したMSG､Text = 全てのMSG

        Txt = ""
        For Cnt = 1 To CmdNum - 1                       '全てのMSGの最後に作成したMSGを追加
            TxtRet = Cmd(Cnt)                           '何番目のCmd配列か
            TmpString = "[" & Hex(TxtRet) & "h] "       '表示用
            Txt = Txt & TmpString                       '新規MSGを追加
        Next

        DispCommandList = Txt

    End Function

    '///// [ GpinInit 関数 ] ////////////////////////////////////////////////////////////////
    Public Function GpibInit(ByRef TextInit As String) As Integer

        'Delim = 1: Eoi = 1								'Delim = 0:使用しない/1:CR+LF/2:CR/3:LF Eoi = 0:使用しない/1:使用する
        Timeout = 10000                                 'Timeout = ms(1000ms -> 1s)
        GpibInit = 0                                        '初期設定

        Ret = GpExit()                                  '再初期化によるエラーを防ぎます｡
        Ret = GpIni()                                   'GP-IBボードの初期化,関数使用の開始宣言を行います｡
        If CheckRet("GpIni", Ret, TextInit) = 1 Then GoTo Err_Renamed 'GpIniでのエラーチェックをします｡
        '次のGpBoardsts()ではレジストリから情報を取得することができます｡
        '１番目の引数はヘルプに対照表があります｡2番目は代入する変数名です｡
        Ret = GpBoardsts(&HAS, Mode)                    'Master(=0)かSlave(=1)かを取得します｡
        Ret = GpBoardsts(&H8S, MyAddr)                  'マイアドレスを取得します｡
        Ret = GpBoardsts(&HCS, Dmamode)                 'DMA モード
        Ret = GpBoardsts(&HDS, DmaPos)                  'DMA チャネル

        If Mode = 0 Then                                'マスタの時はGpIni()、GpRen()を使用します。
            Ret = GpIfc(1)                              'マスタであることを伝えます。(1の場合は100usになります｡)
            If CheckRet("GpIfc", Ret, TextInit) = 1 Then GoTo Err_Renamed 'GpRetでのエラーチェックをします｡

            Ret = GpRen()                               '相手機器をリモート状態にします。
            If CheckRet("GpRen", Ret, TextInit) = 1 Then GoTo Err_Renamed 'GpRenでのエラーチェックをします｡
        End If
        '実行しない場合の初期値はCR+LF+EOIになっています。
        'Ret = GpDelim(Delim, Eoi)						'デリミタコード(EOI)送出の指定をします。(指定しなくてもいいです｡)
        'If CheckRet("GpDelim", Ret, TextInit) = 1 Then GoTo Err	'GpDelimでのエラーチェックをします｡

        '実行しない場合の初期値は10000ms -> 10sになっています。
        Ret = GpTimeout(Timeout)                        'タイムアウト時間を指定します。(指定しなくてもいいです｡)
        If CheckRet("GpTimeout", Ret, TextInit) = 1 Then GoTo Err_Renamed 'Timeoutでのエラーチェックをします｡

        TextInit = "初期化を終了しました。"                'Checkが全て０(正常終了)の場合｡
        Exit Function
Err_Renamed:
        GpibInit = 1

    End Function

    '///// [ GpibExit 関数 ] ////////////////////////////////////////////////////////////////
    Public Function GpibExit() As Integer

        Ret = GpBoardsts(&HAS, Mode)                    'Master(=0)かSlave(=1)かを取得します｡
        If Mode = 0 Then
            Cmd(0) = 2                                  'コマンド数
            Cmd(1) = &H3FS                              'アンリスン／UNL
            Cmd(2) = &H5FS                              'アントークン／UNT
            Ret = GpComand(pCmd)
            Ret = GpResetren()                          '相手機器のリモート状態を解除します。
        End If
        Ret = GpExit()                                  'GP-IBボードのリセット､関数使用の終了宣言をします。

    End Function

    '///// [ GpibPrint 関数 ] ///////////////////////////////////////////////////////////////
    Public Function GpibPrint(ByRef DeviceAddr As Integer, ByRef Str_Renamed As String) As Integer

        Ret = GpBoardsts(&H8S, MyAddr)
        Cmd(0) = 2                                      '最大受信数
        Cmd(1) = MyAddr                                 'マイアドレス(PC)
        Cmd(2) = DeviceAddr                             'PIA3200

        'Srbuf = Str_Renamed                             '送信データ
        Srlen = Len(Str_Renamed)                        'データ長
        'Ret = GpTalk(pCmd, Srlen, Srbuf)                '実際の送信
        Ret = GpTalk(pCmd, Srlen, Str_Renamed)          '実際の送信
        If Ret <> 0 Then                                'エラーチェック
            GpibPrint = 1                               'エラーあり
            RetTmp = CheckRet("GpTalk", Ret, ErrText)
            Ret = MsgBox("アドレス [ " & DeviceAddr & " ] <- [ " & Str_Renamed & " ] の送信に失敗しました。", MsgBoxStyle.YesNo, "継続しますか？")
            If Ret = MsgBoxResult.No Then GpibPrint = 1 '[いいえ]の場合は終了
            If Ret = MsgBoxResult.Yes Then GpibPrint = 0 'エラーなし
        End If

    End Function

    '///// [ GpibInput 関数 ] ///////////////////////////////////////////////////////////////
    Public Function GpibInput(ByRef DeviceAddr As Integer, ByRef Str_Renamed As String) As Integer

        Str_Renamed = Space(10000)                      'スペースで初期化します。
        Ret = GpBoardsts(&H8S, MyAddr)
        Srlen = 10000                                   '最大受信数
        Cmd(0) = 2                                      '配列(コマンド)総数
        Cmd(1) = DeviceAddr                             'PIA3200のアドレス
        Cmd(2) = MyAddr                                 'マイアドレス(PC)

        Ret = GpListen(pCmd, Srlen, Srbuf)

        If Ret > 3 Then                                 'エラーチェック
            RetTmp = CheckRet("GpListen", Ret, ErrText)
            Ret = MsgBox("アドレス [ " & DeviceAddr & " ] からの受信に失敗しました。", MsgBoxStyle.YesNo, "継続しますか？")
            If Ret = MsgBoxResult.No Then GpibInput = 1
            If Ret = MsgBoxResult.Yes Then
                GpibInput = 0                           'エラーなし
            End If
        End If
        Str_Renamed = Mid(Srbuf, 1, Srlen)

    End Function

    'HIOKI追加
    '///// [ GpibInputHioki 関数 ] //////////////////////////////////////////////////////////
    Public Function GpibInputHioki(ByRef DeviceAddr As Integer, ByRef Str As StringBuilder) As Integer

        Ret = GpBoardsts(&H8S, MyAddr)
        Cmd(0) = 2                                      '配列(コマンド)総数
        Cmd(1) = DeviceAddr                             'スレーブ機器
        Cmd(2) = MyAddr                                 'マイアドレス(PC)

        Str.Clear()                                     '初期化
        While True
            Srlen = 10000                               '最大受信数
            Ret = GpListen(pCmd, Srlen, Srbuf)
            If Ret <= 2 Then                            '受信終了
                Str.Append(Mid(Srbuf, 1, Srlen))
                Exit While
            ElseIf Ret = 128 Then                       '受信データ域オーバー
                Str.Append(Mid(Srbuf, 1, Srlen))
                Cmd(0) = 0                              'コマンドを出さずにGpListenします。
            Else                                        'エラーチェック
                CheckRet("GpListen", Ret, ErrText)
                MsgBox("アドレス [ " & DeviceAddr & " ] からの受信に失敗しました。", MsgBoxStyle.OkOnly)
                Return 1                                '異常 = 1を返す
            End If
        End While
        Return 0                                        '正常 = 0を返す

    End Function

    'Tektronix/TDS3000バイナリデータ受信専用 ////////////////////////////////////////////////
    Public Function GpibListenB(ByRef Dev As Integer, ByVal pByteData As IntPtr, ByRef Srlen As Integer) As Integer
        Dim DataLen As New String("", 10)

        Ret = GpBoardsts(&H8S, MyAddr)                  'マイアドレス取得
        Srlen = 2                                       '最大受信数
        Cmd(0) = 2                                      '配列(コマンド)総数
        Cmd(1) = Dev                                    'PIA3200のアドレス
        Cmd(2) = MyAddr                                 'マイアドレス(Board)
        Ret = GpDelim(0, 1)                             'TDS3000のデリミタが初期設定では｢LF｣のみなのでデリミタの変更が必要
        Ret = GpListen(pCmd, Srlen, DataLen)
        If (Ret >= 3) Then
            If (Ret <> 128) Then                        'わざとデータを切っているために Ret=128 となります。
                RetTmp = CheckRet("GpListen", Ret, ErrText)
                Ret = MsgBox("アドレス [ " & Dev & " ] からの受信に失敗しました。", MsgBoxStyle.YesNo, "継続しますか？")
                If Ret = MsgBoxResult.No Then
                    GpibListenB = 1                     '[いいえ]の場合は終了
                    Exit Function
                End If
            End If
            If Ret = MsgBoxResult.Yes Then GpibListenB = 0 'エラーなし
        End If
        Cmd(0) = 0                                      'コマンドを出さずにGpListenします。
        Srlen = Val(Mid(DataLen, 2, 1))
        Ret = GpListen(pCmd, Srlen, DataLen)

        Srlen = Val(Mid(DataLen, 1, Srlen))
        Ret = GpListenBinary(pCmd, Srlen, pByteData)
        Ret = GpDelim(3, 1)                             'デリミタを戻します。

    End Function

    '///// [ GpibInputB 関数 ] //////////////////////////////////////////////////////////////
    Public Function GpibInputB(ByRef Dev As Integer, ByVal pByteData As IntPtr) As Integer

        Ret = GpBoardsts(&H8S, MyAddr)
        Srlen = 10000                                   '最大受信数
        Cmd(0) = 2                                      '配列(コマンド)総数
        Cmd(1) = Dev                                    'PIA3200のアドレス
        Cmd(2) = MyAddr                                 'マイアドレス(PC)

        Ret = GpListenBinary(pCmd, Srlen, pByteData)
        If Ret > 3 Then                                 'エラーチェック
            RetTmp = CheckRet("GpListenBinary", Ret, ErrText)
            Ret = MsgBox(ErrText & " 継続しますか？", MsgBoxStyle.YesNo, "エラー")
            If Ret = MsgBoxResult.No Then
                GpibInputB = 1
                Exit Function
            End If
        Else
            GpibInputB = 0                              'エラーなし
        End If

    End Function

    '///// [ GpibCmd 関数 ] /////////////////////////////////////////////////////////////////
    Public Function GpibCmd() As Integer

        Cmd(0) = 2                                      'コマンド数
        Cmd(1) = &H3FS                                  'アンリスン  ／UNL
        Cmd(2) = &H5FS                                  'アントークン／UNT

        Ret = GpComand(pCmd)                            'コマンド送信
        If Ret <> 0 Then                                'エラーチェック
            GpibCmd = 1                                 'エラーあり
            RetTmp = CheckRet("GpComand", Ret, ErrText)
            Ret = MsgBox(ErrText, MsgBoxStyle.OkOnly, "エラー")
            End                                         'プログラム終了(エラーで終わらない場合は消去して下さい。)
        End If
        GpibCmd = 0                                     '正常終了

    End Function

    ' ///// [ OPCのチェック ] ///////////////////////////////////////////////////////////////
    Public Sub WaitOPC(ByRef Dev As Integer)
        Dim RdData As String = ""

        Ret = GpibPrint(Dev, "*OPC?")                   '工程作業が完了しているか
        Ret = GpibInput(Dev, RdData)

    End Sub

    '///// [ESC]キーの制御 //////////////////////////////////////////////////////////////////
    Public Function EscCheck() As Integer
        Dim vKey As Integer

        vKey = &H1BS         'ESCのアスキーコード
        If (GetAsyncKeyState(vKey) <> 0) Then
            EscCheck = 1        'ESCキー検出(戻り値)
        Else
            EscCheck = 0        'ESCキーなし(戻り値)
        End If

    End Function
End Module