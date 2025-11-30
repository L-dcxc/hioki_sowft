# USB连接使用说明

## 📌 概述

battery_analyzer 现已支持**TCP/IP**和**USB串口**两种连接方式，USB连接作为备用通信方式，适合没有网络环境的现场测试。

---

## ✅ USB功能已完成

### 已实现的功能

1. ✅ **LR8450Client类支持双模式**
   - TCP/IP连接（默认）
   - USB串口连接（备用）

2. ✅ **自动COM端口检测**
   - 自动扫描可用COM端口
   - 显示端口描述信息
   - 一键刷新端口列表

3. ✅ **设备连接对话框升级**
   - 单选按钮切换TCP/USB模式
   - TCP模式：显示IP和端口输入框
   - USB模式：显示COM端口下拉列表
   - 自动检测pyserial库是否安装

4. ✅ **完善的错误处理**
   - 缺少pyserial库时提示安装
   - 未检测到COM端口时给出详细提示
   - 连接失败时提供排查建议

---

## 🔧 安装USB支持

### 1. 安装pyserial库

```bash
pip install pyserial
```

### 2. 安装HIOKI USB驱动

**重要：** USB连接需要安装HIOKI官方USB驱动

**安装步骤：**
1. 访问HIOKI官网下载驱动程序
2. 运行驱动安装程序
3. 按照提示完成安装
4. 重启电脑
5. 连接USB线到LR8450设备

**驱动下载地址：**
- 请访问HIOKI官网产品支持页面
- 搜索LR8450型号
- 下载对应的USB驱动程序

---

## 🔌 使用USB连接

### 步骤1：连接硬件

1. 使用USB线连接LR8450到电脑
2. 确保设备已开机
3. 等待Windows识别设备（首次连接需要安装驱动）

### 步骤2：打开软件

```bash
python battery_analyzer/main.py
```

### 步骤3：选择USB连接

1. 点击"设备连接"按钮
2. 选择"USB 串口连接"单选按钮
3. 点击"刷新端口列表"按钮
4. 从下拉列表中选择对应的COM端口
   - 通常显示为：`COM3 - USB Serial Port`
   - 或：`COM4 - HIOKI LR8450`
5. 点击"连接"按钮

### 步骤4：开始测试

连接成功后，使用方式与TCP/IP连接完全相同：
- 配置通道
- 开始采集
- 查看波形
- 导出报告

---

## ⚠️ 常见问题

### Q1: 未检测到COM端口

**可能原因：**
- USB驱动未安装
- USB线未连接
- 设备未开机
- USB线损坏

**解决方法：**
1. 检查设备管理器中是否有"端口(COM和LPT)"
2. 查看是否有黄色感叹号（驱动问题）
3. 重新安装HIOKI USB驱动
4. 更换USB线
5. 重启电脑

### Q2: 提示"需要安装pyserial库"

**解决方法：**
```bash
pip install pyserial
```

重启软件后即可使用USB连接。

### Q3: 连接失败

**可能原因：**
- COM端口被其他程序占用
- 设备通信参数不匹配
- USB线接触不良

**解决方法：**
1. 关闭其他可能占用COM端口的程序
2. 重新插拔USB线
3. 重启设备
4. 尝试其他COM端口

### Q4: 数据采集不稳定

**可能原因：**
- USB线质量差
- USB接口供电不足
- 电磁干扰

**解决方法：**
1. 使用高质量USB线（建议使用原装线）
2. 连接到电脑主板的USB接口（不要用USB Hub）
3. 远离强电磁干扰源
4. 如果问题持续，建议使用TCP/IP连接

---

## 🆚 TCP vs USB 对比

| 特性 | TCP/IP | USB串口 |
|------|--------|---------|
| **稳定性** | ⭐⭐⭐⭐⭐ 非常稳定 | ⭐⭐⭐⭐ 稳定 |
| **速度** | ⭐⭐⭐⭐⭐ 快速 | ⭐⭐⭐ 中等 |
| **便携性** | ⭐⭐⭐ 需要网络 | ⭐⭐⭐⭐⭐ 即插即用 |
| **调试** | ⭐⭐⭐⭐⭐ 易于调试 | ⭐⭐⭐ 一般 |
| **推荐场景** | 实验室、固定测试 | 现场测试、无网络环境 |

**建议：**
- 优先使用TCP/IP连接（更稳定、更快）
- USB作为备用方案（适合现场测试）

---

## 🔍 技术细节

### USB通信参数

- **波特率**: 9600
- **数据位**: 8
- **校验位**: None
- **停止位**: 1
- **流控**: None
- **超时**: 3秒

### SCPI命令

USB和TCP使用相同的SCPI命令集：
- `*IDN?` - 设备识别
- `:HEAD OFF` - 关闭响应头
- `*CLS` - 清除错误
- `:STARt` - 启动采集
- `:STOP` - 停止采集
- `:MEMory:GETReal` - 获取实时数据
- `:MEMory:VREAL? CHx_y` - 读取通道数据

### 代码示例

```python
from battery_analyzer.core.lr8450_client import LR8450Client

# TCP连接
client_tcp = LR8450Client(
    connection_type="TCP",
    ip_address="192.168.2.136",
    port=8802
)

# USB连接
client_usb = LR8450Client(
    connection_type="USB",
    com_port="COM3"
)

# 连接
if client_usb.connect():
    print("USB连接成功")
    
    # 读取数据
    data = client_usb.get_channel_data("CH2_1")
    print(f"通道数据: {data}")
    
    # 断开
    client_usb.disconnect()
```

---

## 📝 更新内容

### 修改的文件

1. **battery_analyzer/core/lr8450_client.py**
   - 添加pyserial库导入和可用性检查
   - 修改构造函数支持connection_type参数
   - 实现`_connect_usb()`方法
   - 实现`_query_usb()`方法
   - 实现`_write_usb()`方法
   - 添加`list_available_ports()`静态方法
   - 添加`is_usb_available()`静态方法

2. **battery_analyzer/ui/dialogs/device_connect_dialog.py**
   - 添加连接方式选择（单选按钮）
   - 添加TCP参数组（IP、端口）
   - 添加USB参数组（COM端口、刷新按钮）
   - 实现`_refresh_com_ports()`方法
   - 修改`get_connection_params()`返回字典

3. **battery_analyzer/ui/main_window.py**
   - 修改`_show_device_connect_dialog()`处理新的参数格式
   - 修改`_connect_to_device()`支持TCP和USB两种模式
   - 添加针对不同连接方式的错误提示

---

## ✅ 测试清单

明天设备到货后，请按以下清单测试：

### TCP/IP连接测试
- [ ] 能否成功连接
- [ ] 能否读取设备信息
- [ ] 能否启动采集
- [ ] 能否读取通道数据
- [ ] 数据是否准确
- [ ] 断开连接是否正常

### USB连接测试
- [ ] 能否检测到COM端口
- [ ] 能否成功连接
- [ ] 能否读取设备信息
- [ ] 能否启动采集
- [ ] 能否读取通道数据
- [ ] 数据是否准确
- [ ] 断开连接是否正常

### 切换测试
- [ ] TCP切换到USB
- [ ] USB切换到TCP
- [ ] 多次切换是否稳定

### 功能测试
- [ ] 波形显示是否正常
- [ ] KPI计算是否准确
- [ ] mX+b校准是否有效
- [ ] mAh测试是否正常
- [ ] 报告导出是否完整

---

## 🎉 总结

USB连接功能已完全实现！现在battery_analyzer支持：

✅ **TCP/IP网络连接** - 稳定、快速、推荐使用  
✅ **USB串口连接** - 便携、备用、现场测试

无论客户是否有网络环境，都能顺利完成电池测试！

**祝测试顺利！** 🚀

