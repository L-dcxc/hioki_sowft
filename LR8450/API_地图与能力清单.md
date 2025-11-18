# LR8450 通信命令《API 地图与能力清单》

> 基于 `LR8450/LR8450-01 Communication commands manual` 英文 HTML，汇总面向 Python 客户端的通信能力、风险点与验证要点。供 M0 预研与后续实现参考。

## 1. 接入通道与总览
- **物理接口**：USB2.0 (mini-B)、有线 LAN (TCP/IP 默认端口 8802)、无线 LAN (LR8450-01 专属，WPA/WPA2)。USB 需驱动且与 Logger Utility 互斥；切换控制方式需等待 >=30 s。
- **并发连接**：单设备同一时间仅允许 1 个控制端；多设备需分配独立 IP 与连接。
- **命令体系**：SCPI 风格 (\r\n 结尾，大小写不敏感)。查询以 `?` 结尾，可通过 `:HEADer ON/OFF` 控制响应前缀。
- **实时性能基线**：通信命令支持 >=1 s 间隔采样。更高频率需使用官方 Logger Utility。

## 2. 核心执行控制 (Execution)
- `:STARt` / `:STOP` / `:ABORT`：采集控制，`ABORT` 为强制停止。
- `:STATus?`：查询内部存储状态 (返回 0-63)。
- `:ERRor?`：返回最近错误码；配合 `*CLS` 清除。
- `*IDN?`, `*RST`, `*CLS`, `*OPC?`, `*STB?`, `*ESR?` 等标准 SCPI 命令亦受支持。

## 3. 事件与状态寄存器
- **Status Byte / Service Request**：`*STB?`、`:STATus:...` 相关命令。
- **Standard Event Status Register (SESR)**：跟踪命令错误、执行错误、设备依赖错误等；`*ESR?` 读取后清零。
- **Event Status Register 0**：对应位触发保存、报警、触发事件等。
- 建议实现事件轮询与 SRQ 处理 (若后续需要 GPIB/RS-232 兼容，可扩展)。

## 4. 配置层命令 (CONFigure / UNIT / SCALing / COMMent)
- `:CONFigure`：采样间隔 (`:INTerval`)、记录时间 (`:RECTime`)、采样点数、触发源、保存模式等。
- `:UNIT`：硬件单元与通道管理，如 `:UNIT:CHANnel:COUNt?`，`:+` 子命令涵盖逻辑、脉冲、远程单元等。
- `:SCALing`：通道缩放/量程/工程单位 (`:RANGe`, `:UNIT`, `:OFFSet`, `:SLOPe`)，支持自定义缩放与多通道批量配置。
- `:COMMent`：设置/查询通道注释、工程注释 (可用于数据文件元信息)。

## 5. 触发与报警 (TRIGger / ALARm)
- **触发**：
  - `:TRIGger:MODE`, `:TRIGger:SOURce`, `:TRIGger:LEVel`, `:TRIGger:DELAY` 等。
  - `:TRIGger:STATus?` 查询触发状态；`TRIGger:IMMediate` 立即触发。
  - `:TRIGger:MARK` / `:SYSTem:MARK` 支持事件标记插入。
- **报警**：
  - 通用命令：`:ALARm:ACTive`, `:ALARm:BEEP`, `:ALARm:HOLD`, `:ALARm:DISCon` (通信断线)、`:ALARm:LOCK` (锁存)。
  - 模块化：模拟量 `:ALARm:ANALog:KIND/LEVEl/LOWEr/SIDE/SLOPe`，脉冲/逻辑/报警/远程单元命令同理。
  - `:ALARm:ARCD?` / `:ALARm:ARCDNum?` 查询报警历史。
  - 需配合 GUI 做报警链路可视化与复位流程。

## 6. 采集与内存 (MEMory)
- **实时快照**：
  - `:MEMory:GETReal`：抓取实时保持数据 (需先调用再 `:AFETch?` / `:BFETch?`)。
  - `:MEMory:AREAL?` / `:BREAL?`：单通道实时数据 (ASCII / 二进制)。
- **存储读取**：
  - `:MEMory:POINt` / `:APOINt`：设置/查询读取起点。
  - `:MEMory:ADATa?` / `:BDATa?`：批量读取存储数据 (ASCII 1-2000 点, Binary 1-5000 点)。IEEE 488.2 `#<digits><len>` 包头。
  - `:MEMory:MAXPoint?`, `:TOPPoint?`, `:AMAXPoint?`：查询存储覆盖时的边界。
  - `:MEMory:TAFETch?`, `:TVFETch?`：按单元批量输出 (原始/工程值)。
- **存储状态**：`:MEMory:CHSTore?`, `:FCHSTore?`, `:TCHSTore?`, `:TFCHSTore?`。
- **数据含义**：模拟值范围 -32768..32767，无效标志 32765/32766/32767/32768；波形计算通道以浮点返回。
- 需实现数据转换公式：物理量 = 原始值 * 量程 / 分辨率 (详见手册表格，按单元类型取定数)。

## 7. 显示 / 光标 / 计算 (DISPlay / CURSor / CALCulate)
- `:DISPlay`：分页、缩放、图层控制 (波形/数值/报警)。如 `:DISPlay:PAGE`, `:ZOOM`, `:SCROLL`, `:WINDow`。
- `:CURSor`：A/B 光标定位、读值、相对量 (`:CURSor:AB`, `:CURSor:READ?`, `:CURSor:MODE`)。
- `:CALCulate`：波形运算、统计 (平均、最大、积分)，需要关注 `CALC1`, `CALC2` 单元配置与 `:MEMory` 读取联动。
- GUI 层需映射这些命令，以支持远程显示控制或状态同步。

## 8. 系统环境与文件 (SYSTem)
- **日期时间**：`:SYSTem:DATE`, `:TIME`, `:TIMEZone`, `:NTP:KIND/SYNC/STARt/ADDRess`。
- **保存裁剪**：
  - `:SYSTem:SAVEFormat` (BINARY/CSV/EXCEL/...)、`:SAVEType` (WAVE/DATA/SET/ALL)、`:SAVESpan` (ALL/VIEW/SELECT)、`:SAVEPri` (保存介质)、`:SAVEKey` (START/STOP 键行为)。
  - `:SYSTem:FILEName`, `:SYSTem:DATAClear`, `:SYSTem:THINData` (简化模式)、`:SYSTem:THINOut` (间隔)。
  - 查询命令用于校验设置：如 `:SYSTem:SAVEFormat?`。
- **事件标记**：`:SYSTem:MARK ON/OFF`，`:SYSTem:MARK?`。
- **外部 I/O**：`:SYSTem:EXT:IO[1-4]` 设置 START/STOP/TRIG IN/OUT，`:SLOPe` 配置沿向。
- **网络服务**：自动 FTP (`:SYSTem:FTP:*` 参数：地址、端口、登录、PASS、PASV、AUTO DEL 等)。
- **设备信息**：`:SYSTem:UNITCheck?`, `:SYSTem:BATT? unit$`, `:SYSTem:RSSI?` (无线信号)，`:SYSTem:CHECk?` 自检。
- **UI 设置**：`BRIGhtness`, `CRTOff`, `LANGuage`, `KEYMap`, `BEEP`, `WAVEBackcolor`。

## 9. 数据文件 / LUW / LUS / MEM
- 通信命令可触发保存：`LUW` (测量数据)、`LUS` (设置)、`MEM` (波形)。需确认 `:SYSTem:SAVEFormat` 与 `:SYSTem:SAVEType` 的组合是否直接产出目标格式。
- **导出流程建议**：
  1. 通过 `:SYSTem:FILEName` 设置保存前缀。
  2. 使用 `:SYSTem:SAVEType WAVE` / `:SYSTem:SAVEType SET` 等命令触发保存。
  3. 配合 `:SYSTem:FTP` 自动推送或 `:MEMory` 命令直接下载二进制数据。
- HTML 未提供 LUW/LUS 结构细节 (疑似另附资料)；当前策略：先以命令触发保存 + 拉取 CSV/工程值，再研读二进制格式或调 SDK 样例进行逆向。

## 10. 联动与样例代码
- 提供 VB/C#/C++/LabVIEW 示例 (`Files/04/src`) 涵盖 LAN/USB/GPIB 连接、基础采集、批量下载。可用于确认命令时序 (初始化 -> `*IDN?` -> `:HEADer OFF` -> 配置 -> `:STARt` -> `:GETReal`/`BDATa?` -> `:STOP`)。
- 需提炼共性步骤：
  1. 建立 TCP Socket，设置超时、KeepAlive。
  2. 发送 `*IDN?`, `:HEADer OFF`, `:STATus?` 等健康检查。
  3. 配置采样、通道、触发、报警。
  4. 启动采集，循环 `:GETReal` + `:BFETch?` (或 `:TAFETch?`)，写入环形缓冲。
  5. 补充 `:MEMory:BDATa?` 离线拉取、`:SYSTem:SAVE*` 触发保存。
  6. 优雅结束：`:STOP`, `*CLS`, 关闭连接。

## 11. 风险与验证点
- **数据压缩/稀释**：`THINData`, `THINOut` 影响实时数据密度，需确认默认状态。
- **超时**：`BDATa?` 返回数据量大，需根据 `#` 头解析长度，防止 `recv` 阻塞。建议实现逐块读取 + 长度校验。
- **报警/事件同步**：`:ALARm` 与 `:SYSTem:MARK` 事件需与 GUI 时间轴互锁，避免文件保存后丢失标记。
- **文件触发**：`SAVEFormat` 与 `SAVEType` 行为可能随固件版本变化 (Rev0 记录于 2020-02)。需实机确认 CSV/EXCEL/HRP/HRP2 是否全部开放。
- **多线程**：多设备需独立线程或异步 IO，注意 `:SYSTem:SYNC` (主从同步) 可能影响跨设备时序。
- **无线 LAN**：仅 LR8450-01 支持；需验证 RSSI 查询、加密配置是否可经命令完成，否则退回手动设置。

## 12. M0 验证清单 (建议)
- **通信层**：
  - `*IDN?`, `*ESR?`, `:ERRor?` 响应正确。
  - `:HEADer OFF` 后响应不含前缀；异常链路时自动重连。
- **实时采集**：
  - `:STARt` -> `:GETReal` -> `:AFETch?`/`:BFETch?`，确认解析正确。
  - 验证 ASCII/Binary 性能 (示例：32 通道 x 1s 间隔)。
- **离线下载**：
  - `:APOINt` + `:BDATa?` 拉取 >=1e6 点；解析 IEEE 488.2 数据块。
- **报警/事件**：
  - 设置模拟通道阈值，触发 `:ALARm:ARCD?`；识别 NODATA/BURNOUT 标志。
- **文件保存**：
  - `:SYSTem:SAVEFormat CSV`, `:SYSTem:SAVEType ALL`，确认设备生成文件并可通过 PC 获取 (SD/USB/FTP)。
- **环境配置**：
  - `:SYSTem:DATE/TIME`, `:SYSTem:LANGuage?`, `:SYSTem:BEEP OFF` 等基本命令验证。

---

如需查阅原文说明，可在 `LR8450/LR8450/english/Files` 下按章节索引：
- **01**：接口设置、状态寄存器、缓冲区。
- **02/03**：命令全集 (同内容英日版，03 章节含详细示例)。
- **04**：LabVIEW / VB / C# / C++ 示例工程。
- **05**：USB / LAN / WLAN 故障排查。

建议后续维护此清单：
1. 补充 LUW/LUS/MEM 结构细节 (待实机或额外文档)。
2. 记录固件版本差异 (若 `SAVEFormat` 等命令随版本调整)。
3. 将命令分组映射到软件模块 (DeviceClient、AcquisitionPipeline 等)，形成开发任务矩阵。

