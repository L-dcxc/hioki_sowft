# LR8450/LR8450-01 SDK 开发总结

## 1. 设备概述

HIOKI LR8450/LR8450-01 Memory HiLogger 是一款多通道数据记录仪，支持：
- 最大通道数：2035（测量）+ 60（波形运算）
- 支持模拟量、脉冲、逻辑、报警等多种数据类型
- 实时数据采集和存储功能
- 多种通信接口：LAN、USB、无线LAN（仅LR8450-01）

## 2. 通信接口规格

### 2.1 LAN 连接（推荐）
- **协议**: TCP/IP
- **标准**: IEEE802.3 Ethernet 1000BASE-T, 100BASE-TX
- **传输速度**: 1Gbps
- **默认端口**: 8802
- **连接方式**: 直连或通过网络交换机
- **IP地址建议**: 192.168.1.x 网段（设备192.168.1.2，PC 192.168.1.1）

### 2.2 USB 连接
- **标准**: USB2.0
- **接口**: mini-B type USB
- **注意事项**: 
  - 需要安装USB驱动
  - 不能与Logger Utility同时使用
  - 切换需要等待至少30秒

### 2.3 无线LAN（仅LR8450-01）
- **标准**: IEEE802.11b/g/n
- **通信距离**: 视距30m
- **加密**: WPA-PSK/WPA2-PSK、TKIP/AES
- **注意**: 与有线LAN互斥使用

## 3. 命令协议

### 3.1 命令格式
- **终止符**: CR+LF (`\r\n`)
- **查询命令**: 以 `?` 结尾
- **响应格式**: 可选择是否包含头部信息
- **数据类型**: 支持字符串、整数、浮点数等多种格式

### 3.2 通道标识符
```
模拟通道: CH1_1 到 CH4_30 (最多120通道)
脉冲通道: PLS1 到 PLS8
报警通道: ALM1 到 ALM8
逻辑通道: LOG
波形计算: W1 到 W30
远程单元: R1_1 到 R7_30
```

## 4. 核心命令分类

### 4.1 执行控制命令
```
:STARt          # 开始波形采样
:STOP           # 停止波形采样  
:ABORT          # 强制停止波形采样
:ERRor?         # 查询错误号
:HEADer ON/OFF  # 启用/禁用响应头部
```

### 4.2 数据获取命令

#### 实时数据获取
```
:MEMory:GETReal                    # 获取实时数据快照
:MEMory:AFETch? ch$               # 获取指定通道实时数据(ASCII)
:MEMory:BFETch? ch$               # 获取指定通道实时数据(二进制)
```

#### 存储数据获取
```
:MEMory:ADATa? A                  # 获取存储数据(ASCII格式)
:MEMory:BDATa? A                  # 获取存储数据(二进制格式)
:MEMory:APOINt ch$,A              # 设置数据读取起始点
:MEMory:AMAXPoint?                # 查询数据结束点
```

### 4.3 配置命令
```
:CONFigure:...                    # 基本配置
:UNIT:...                         # 通道单元配置
:SCALing:...                      # 缩放设置
:TRIGger:...                      # 触发设置
:ALARm:...                        # 报警设置
:SYSTem:...                       # 系统环境设置
```

## 5. 数据格式

### 5.1 数据值范围
```
模拟通道: -32768 到 32767
脉冲通道: 0 到 1000000000
逻辑通道: 0 到 255
报警通道: 0 到 255
波形计算: 浮点数结果
```

### 5.2 二进制数据格式
- **模拟/脉冲/逻辑/报警**: 2字节整数
- **波形计算**: 8字节双精度浮点数
- **无效数据标识**: 0x7fff (模拟), 0x7ff0000000000001 (波形计算)

## 6. 性能指标

### 6.1 数据传输性能
- **ASCII格式**: 100万点数据约12秒（每次2000点，500次传输）
- **二进制格式**: 100万点数据约2秒（每次5000点，200次传输）
- **建议**: 大量数据传输优先使用二进制格式

### 6.2 实时采集限制
- **最小采集间隔**: 1秒（通过通信命令）
- **更高频率**: 需要使用Logger Utility专用软件
- **多设备**: 支持同时连接多台设备

## 7. 开发要点

### 7.1 连接管理
```python
# TCP连接示例
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.2', 8802))
sock.settimeout(10.0)  # 设置超时
```

### 7.2 命令发送
```python
def send_command(sock, command):
    """发送命令到设备"""
    cmd_bytes = (command + '\r\n').encode('ascii')
    sock.send(cmd_bytes)

def send_query(sock, query, timeout=5.0):
    """发送查询命令并接收响应"""
    send_command(sock, query)
    response = receive_response(sock, timeout)
    return response
```

### 7.3 数据接收
```python
def receive_response(sock, timeout=5.0):
    """接收设备响应"""
    sock.settimeout(timeout)
    buffer = b''
    while True:
        data = sock.recv(4096)
        buffer += data
        if b'\n' in buffer:
            response = buffer.split(b'\n')[0].decode('ascii').strip()
            return response.replace('\r', '')
```

### 7.4 错误处理
- **超时处理**: 设置合理的socket超时时间
- **连接断开**: 实现自动重连机制
- **命令错误**: 使用 `:ERRor?` 查询错误信息
- **数据校验**: 检查返回数据的有效性

## 8. 文件格式支持

### 8.1 LUW格式（测量数据文件）
- HIOKI专有的二进制数据格式
- 包含测量数据和设置信息
- 需要专门的解析库或工具

### 8.2 LUS格式（设置文件）
- 设备配置信息存储格式
- 可用于保存和恢复设备设置

### 8.3 MEM格式
- 内存数据格式
- 用于波形显示和分析

## 9. 多设备管理

### 9.1 设备发现
- 通过IP地址扫描发现设备
- 支持同时连接最多5台设备
- 每台设备需要独立的TCP连接

### 9.2 并发处理
- 使用多线程或异步IO处理多设备
- 避免设备间的数据混淆
- 实现设备状态监控和故障恢复

## 10. 开发建议

### 10.1 架构设计
1. **设备管理层**: 处理连接、断线重连、设备发现
2. **通信协议层**: 封装命令发送、响应解析
3. **数据处理层**: 实时数据缓存、格式转换
4. **应用接口层**: 提供高级API给上层应用

### 10.2 性能优化
1. **使用二进制传输**: 提高数据传输效率
2. **批量数据获取**: 减少网络往返次数
3. **异步处理**: 避免UI阻塞
4. **数据缓存**: 实现环形缓冲区

### 10.3 可靠性保证
1. **连接监控**: 定期检查连接状态
2. **自动重连**: 网络中断后自动恢复
3. **数据校验**: 确保数据完整性
4. **错误恢复**: 优雅处理各种异常情况

## 11. 实际应用示例

### 11.1 基础连接测试
```python
import socket
import time

def test_connection():
    """测试设备连接"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.1.2', 8802))
        sock.settimeout(5.0)

        # 发送标识查询
        sock.send(b'*IDN?\r\n')
        response = sock.recv(1024).decode('ascii').strip()
        print(f"设备信息: {response}")

        sock.close()
        return True
    except Exception as e:
        print(f"连接失败: {e}")
        return False
```

### 11.2 实时数据采集
```python
def start_realtime_acquisition(sock, channels):
    """开始实时数据采集"""
    # 开始测量
    sock.send(b':STARt\r\n')
    time.sleep(1)

    while True:
        # 获取实时数据快照
        sock.send(b':MEMory:GETReal\r\n')
        time.sleep(0.1)

        # 读取各通道数据
        data = {}
        for ch in channels:
            cmd = f':MEMory:AFETch? {ch}\r\n'
            sock.send(cmd.encode('ascii'))
            response = sock.recv(1024).decode('ascii').strip()
            # 解析响应数据
            if ':MEMORY:AFETCH' in response:
                value = response.split()[-1]
                data[ch] = float(value)

        yield data
        time.sleep(1)  # 1秒采集间隔
```

### 11.3 批量数据下载
```python
def download_stored_data(sock, channel, start_point=0, count=1000):
    """下载存储的历史数据"""
    # 设置读取起始点
    cmd = f':MEMory:APOINt {channel},{start_point}\r\n'
    sock.send(cmd.encode('ascii'))

    # 获取二进制数据（更快）
    cmd = f':MEMory:BDATa? {count}\r\n'
    sock.send(cmd.encode('ascii'))

    # 接收二进制响应
    response = receive_binary_data(sock)
    return parse_binary_data(response, count)

def receive_binary_data(sock):
    """接收二进制数据响应"""
    # 先接收头部信息
    header = b''
    while not header.endswith(b'\n'):
        header += sock.recv(1)

    # 解析数据长度
    if b'#' in header:
        # IEEE 488.2 格式: #<digits><length><data>
        hash_pos = header.find(b'#')
        digits = int(chr(header[hash_pos + 1]))
        length = int(header[hash_pos + 2:hash_pos + 2 + digits])

        # 接收实际数据
        data = b''
        while len(data) < length:
            chunk = sock.recv(min(4096, length - len(data)))
            data += chunk

        return data
    return b''
```

## 12. 常见问题和解决方案

### 12.1 连接问题
**问题**: 无法连接到设备
**解决方案**:
1. 检查IP地址和端口设置
2. 确认网络连通性（ping测试）
3. 检查防火墙设置
4. 确认设备LAN功能已启用

### 12.2 数据传输问题
**问题**: 数据传输缓慢或超时
**解决方案**:
1. 使用二进制格式传输（BDATa而非ADATa）
2. 增加批量传输大小
3. 调整socket超时设置
4. 检查网络带宽和延迟

### 12.3 多设备冲突
**问题**: 多设备同时连接时出现冲突
**解决方案**:
1. 为每台设备分配不同IP地址
2. 使用独立的socket连接
3. 实现设备连接状态监控
4. 添加设备标识和路由机制

## 13. 开发路线图

### 13.1 M0 预研阶段（1-2天）
- [ ] 基础TCP通信模块
- [ ] 命令发送/接收封装
- [ ] 设备连接测试
- [ ] 基本数据获取验证

### 13.2 M1 MVP单机采集（3-5天）
- [ ] 实时数据采集循环
- [ ] 数据格式解析
- [ ] 基础GUI界面
- [ ] CSV数据导出

### 13.3 M2 多机与稳定性（5-7天）
- [ ] 多设备管理
- [ ] 断线重连机制
- [ ] 错误处理和恢复
- [ ] 设备状态监控

### 13.4 M3 显示与转换（5-7天）
- [ ] 实时波形显示
- [ ] 历史数据查看
- [ ] 多格式数据导出
- [ ] Excel模板支持

### 13.5 M4 电池分析（5-7天）
- [ ] 温升比对算法
- [ ] 压降分析功能
- [ ] mX+b线性拟合
- [ ] mAh容量计算

## 附录A: 常用命令快速参考

### A.1 系统控制命令
```
*IDN?                    # 查询设备标识信息
*RST                     # 复位设备到默认状态
*OPC?                    # 查询操作完成状态
:STARt                   # 开始测量
:STOP                    # 停止测量
:ABORT                   # 强制停止测量
:ERRor?                  # 查询错误信息
```

### A.2 数据获取命令
```
:MEMory:GETReal                    # 获取实时数据快照
:MEMory:AFETch? CH1_1             # 获取CH1_1实时数据(ASCII)
:MEMory:BFETch? CH1_1             # 获取CH1_1实时数据(二进制)
:MEMory:ADATa? 100                # 获取100个数据点(ASCII)
:MEMory:BDATa? 100                # 获取100个数据点(二进制)
:MEMory:APOINt CH1_1,0            # 设置CH1_1读取起始点为0
:MEMory:AMAXPoint?                # 查询最大数据点数
```

### A.3 配置查询命令
```
:CONFigure:INTerval?              # 查询采样间隔
:CONFigure:RECTime?               # 查询记录时间
:UNIT1:CHANnel:COUNt?             # 查询UNIT1通道数
:SCALing:CH1_1:RANGe?             # 查询CH1_1量程
:TRIGger:MODE?                    # 查询触发模式
:ALARm:CH1_1:UPPer?               # 查询CH1_1上限报警值
```

### A.4 状态查询命令
```
:STATus:MEASure?                  # 查询测量状态
:STATus:TRIGger?                  # 查询触发状态
:STATus:ALARm?                    # 查询报警状态
:STATus:MEMory?                   # 查询内存状态
:STATus:BATTery?                  # 查询电池状态
```

## 附录B: 错误代码参考

### B.1 常见错误代码
```
0     # 无错误
-100  # 命令错误
-101  # 无效字符
-102  # 语法错误
-103  # 无效分隔符
-104  # 数据类型错误
-108  # 参数不允许
-109  # 缺少参数
-110  # 命令头错误
-111  # 头分隔符错误
-112  # 程序助记符太长
-113  # 未定义头
-200  # 执行错误
-201  # 无效的测量状态
-202  # 设置冲突
-203  # 命令保护
```

## 附录C: 数据类型转换

### C.1 模拟通道数据转换
```python
def convert_analog_data(raw_value, range_setting, unit_setting):
    """转换模拟通道原始数据为实际值"""
    # raw_value: -32768 到 32767
    # range_setting: 量程设置 (如 "10V", "1V", "100mV")
    # unit_setting: 单位设置 (如 "V", "A", "°C")

    if raw_value == 0x7fff:  # 无效数据
        return float('nan')

    # 根据量程计算实际值
    range_map = {
        "100V": 100.0,
        "10V": 10.0,
        "1V": 1.0,
        "100mV": 0.1
    }

    full_scale = range_map.get(range_setting, 10.0)
    actual_value = (raw_value / 32767.0) * full_scale

    return actual_value
```

### C.2 脉冲通道数据处理
```python
def convert_pulse_data(raw_value, pulse_setting):
    """转换脉冲通道数据"""
    # raw_value: 0 到 1000000000
    # pulse_setting: 脉冲设置信息

    if raw_value == 0x7fffffff:  # 无效数据
        return float('nan')

    return float(raw_value)
```

---

*本文档基于 HIOKI LR8450/LR8450-01 Communication commands manual 整理*
*版本: v1.0*
*最后更新: 2024年12月*
