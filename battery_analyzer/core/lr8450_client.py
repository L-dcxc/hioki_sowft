#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450设备客户端（用于电池测试）"""

from __future__ import annotations

import socket
import time
from typing import Optional, Dict, List, Literal

# USB串口支持
try:
    import serial
    import serial.tools.list_ports
    USB_AVAILABLE = True
except ImportError:
    USB_AVAILABLE = False


class LR8450Client:
    """LR8450设备客户端 - 支持TCP/IP和USB两种连接方式"""

    def __init__(self, connection_type: Literal["TCP", "USB"] = "TCP",
                 ip_address: str = "", port: int = 8802,
                 com_port: str = ""):
        """初始化LR8450客户端

        Args:
            connection_type: 连接类型，"TCP" 或 "USB"
            ip_address: TCP/IP地址（TCP模式使用）
            port: TCP端口（TCP模式使用，默认8802）
            com_port: COM端口（USB模式使用，如"COM3"）
        """
        self.connection_type = connection_type
        self.ip_address = ip_address
        self.port = port
        self.com_port = com_port
        self.timeout = 10.0

        # TCP连接对象
        self.sock: Optional[socket.socket] = None

        # USB串口对象
        self.serial: Optional['serial.Serial'] = None

        self.connected = False
    
    def connect(self) -> bool:
        """连接到设备（支持TCP和USB两种方式）"""
        try:
            if self.connection_type == "TCP":
                return self._connect_tcp()
            elif self.connection_type == "USB":
                return self._connect_usb()
            else:
                print(f"不支持的连接类型: {self.connection_type}")
                return False
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def _connect_tcp(self) -> bool:
        """TCP/IP连接"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.ip_address, self.port))

        # 初始化
        idn = self.query("*IDN?")
        if not idn:
            return False

        self.write(":HEAD OFF")
        self.write("*CLS")
        time.sleep(0.3)

        self.connected = True
        print(f"✓ TCP连接成功: {self.ip_address}:{self.port}")
        return True

    def _connect_usb(self) -> bool:
        """USB串口连接"""
        if not USB_AVAILABLE:
            print("❌ USB连接需要安装 pyserial 库")
            print("请运行: pip install pyserial")
            return False

        if not self.com_port:
            print("❌ 未指定COM端口")
            return False

        # 打开串口
        self.serial = serial.Serial(
            port=self.com_port,
            baudrate=9600,  # LR8450默认波特率
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self.timeout,
            write_timeout=self.timeout
        )

        time.sleep(0.5)  # 等待串口稳定

        # 初始化
        idn = self.query("*IDN?")
        if not idn:
            self.serial.close()
            return False

        self.write(":HEAD OFF")
        self.write("*CLS")
        time.sleep(0.3)

        self.connected = True
        print(f"✓ USB连接成功: {self.com_port}")
        return True
    
    def disconnect(self) -> None:
        """断开连接（支持TCP和USB）"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

        if self.serial:
            try:
                self.serial.close()
            except:
                pass
            self.serial = None

        self.connected = False
    
    def query(self, command: str, timeout: float = 3.0) -> Optional[str]:
        """发送查询命令并接收响应（支持TCP和USB）"""
        if self.connection_type == "TCP":
            return self._query_tcp(command, timeout)
        elif self.connection_type == "USB":
            return self._query_usb(command, timeout)
        return None

    def _query_tcp(self, command: str, timeout: float = 3.0) -> Optional[str]:
        """TCP方式查询"""
        if not self.sock:
            return None

        try:
            # 发送命令
            cmd_with_terminator = command + "\r\n"
            self.sock.sendall(cmd_with_terminator.encode('ascii'))

            # 逐字节接收
            response_chars = []
            start_time = time.time()

            while time.time() - start_time < timeout:
                try:
                    self.sock.settimeout(0.1)
                    byte = self.sock.recv(1)
                    if not byte:
                        break

                    char = byte.decode('ascii', errors='ignore')
                    if char == '\n':
                        break
                    elif char == '\r':
                        continue
                    else:
                        response_chars.append(char)

                except socket.timeout:
                    if response_chars:
                        continue
                    else:
                        break

            response = ''.join(response_chars)
            return response if response else None

        except Exception as e:
            print(f"TCP查询错误 [{command}]: {e}")
            return None

    def _query_usb(self, command: str, timeout: float = 3.0) -> Optional[str]:
        """USB串口方式查询"""
        if not self.serial or not self.serial.is_open:
            return None

        try:
            # 清空缓冲区
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()

            # 发送命令
            cmd_with_terminator = command + "\r\n"
            self.serial.write(cmd_with_terminator.encode('ascii'))
            self.serial.flush()

            # 读取响应（逐字节读取直到遇到换行符）
            response_chars = []
            start_time = time.time()

            while time.time() - start_time < timeout:
                if self.serial.in_waiting > 0:
                    byte = self.serial.read(1)
                    char = byte.decode('ascii', errors='ignore')

                    if char == '\n':
                        break
                    elif char == '\r':
                        continue
                    else:
                        response_chars.append(char)
                else:
                    time.sleep(0.01)  # 短暂等待
                    if response_chars and time.time() - start_time > 0.5:
                        # 如果已有数据且等待超过0.5秒，认为接收完成
                        break

            response = ''.join(response_chars)
            return response if response else None

        except Exception as e:
            print(f"USB查询错误 [{command}]: {e}")
            return None
    
    def write(self, command: str) -> bool:
        """发送写命令（不期待响应，支持TCP和USB）"""
        if self.connection_type == "TCP":
            return self._write_tcp(command)
        elif self.connection_type == "USB":
            return self._write_usb(command)
        return False

    def _write_tcp(self, command: str) -> bool:
        """TCP方式写入"""
        if not self.sock:
            return False

        try:
            cmd_with_terminator = command + "\r\n"
            self.sock.sendall(cmd_with_terminator.encode('ascii'))
            time.sleep(0.1)
            return True
        except Exception as e:
            print(f"TCP写入错误 [{command}]: {e}")
            return False

    def _write_usb(self, command: str) -> bool:
        """USB串口方式写入"""
        if not self.serial or not self.serial.is_open:
            return False

        try:
            cmd_with_terminator = command + "\r\n"
            self.serial.write(cmd_with_terminator.encode('ascii'))
            self.serial.flush()
            time.sleep(0.1)
            return True
        except Exception as e:
            print(f"USB写入错误 [{command}]: {e}")
            return False
    
    def disable_all_channels(self, modules: List[int] = None) -> bool:
        """禁用指定模块的所有通道（防止数据错乱）

        Args:
            modules: 要禁用的模块列表，如 [2] 表示只禁用模块2的通道
                    如果为None，则禁用所有模块（1-4）

        Returns:
            是否成功
        """
        try:
            if modules is None:
                modules = [1, 2, 3, 4]  # 默认禁用所有模块

            print(f"\n🔧 禁用模块 {modules} 的所有通道...")

            disabled_count = 0
            for module in modules:
                for ch in range(1, 31):  # 每个模块30个通道
                    channel = f"CH{module}_{ch}"
                    store_cmd = f":UNIT:STORe {channel},OFF"
                    if self.write(store_cmd):
                        disabled_count += 1
                    time.sleep(0.005)  # 减少延迟，提高速度

            print(f"✓ 已禁用 {disabled_count} 个通道\n")
            return True

        except Exception as e:
            print(f"❌ 禁用通道失败: {e}")
            return False

    def configure_channel(self, channel: str, enabled: bool = True,
                         channel_type: str = "VOLTAGE",
                         range_value: float = None,
                         thermocouple_type: str = None,
                         int_ext: str = None) -> bool:
        """配置单个通道（启用/禁用 + 详细参数设置）

        Args:
            channel: 通道名称，如 "CH2_1"
            enabled: 是否启用通道数据记录
            channel_type: 通道类型，"VOLTAGE"（电压）或 "TEMPERATURE"（温度）
            range_value: 量程值
                - 电压: 0.01, 0.02, 0.1, 0.2, 1, 2, 10, 20, 100 (单位: V)
                - 温度: 100, 500, 2000 (单位: °C)
            thermocouple_type: 热电偶类型（仅温度通道）: "K", "J", "E", "T", "N", "R", "S", "C"
            int_ext: 内部/外部参考（仅温度通道）: "INT" 或 "EXT"

        Returns:
            是否配置成功
        """
        try:
            # 1. 设置通道存储（启用/禁用）
            store_cmd = f":UNIT:STORe {channel},{'ON' if enabled else 'OFF'}"
            if not self.write(store_cmd):
                print(f"⚠️ 设置通道 {channel} 存储失败")
                return False

            print(f"✓ 通道 {channel} 存储已{'启用' if enabled else '禁用'}")

            # 如果禁用，直接返回
            if not enabled:
                return True

            # 2. 设置量程
            if range_value is not None:
                range_cmd = f":UNIT:RANGe {channel},{range_value}"
                if not self.write(range_cmd):
                    print(f"⚠️ 设置通道 {channel} 量程失败")
                    return False

                if channel_type == "VOLTAGE":
                    print(f"✓ 通道 {channel} 电压量程设置为 {range_value}V")
                else:
                    print(f"✓ 通道 {channel} 温度量程设置为 {range_value}°C")

            # 3. 如果是温度通道，设置热电偶类型
            if channel_type == "TEMPERATURE" and thermocouple_type:
                tc_cmd = f":SCALing:UNIT {channel},TC_{thermocouple_type}"
                if not self.write(tc_cmd):
                    print(f"⚠️ 设置通道 {channel} 热电偶类型失败")
                    return False
                print(f"✓ 通道 {channel} 热电偶类型设置为 {thermocouple_type}")

            # 4. 如果是温度通道，设置INT/EXT（内部/外部参考）
            if channel_type == "TEMPERATURE" and int_ext:
                # INT/EXT 通常用于设置参考端温度补偿方式
                # 具体命令可能因设备而异，这里使用常见的SCPI命令
                ref_cmd = f":SCALing:REFerence {channel},{int_ext}"
                if self.write(ref_cmd):
                    print(f"✓ 通道 {channel} 参考设置为 {int_ext}")
                # 如果命令不支持，不影响主要功能

            return True

        except Exception as e:
            print(f"❌ 配置通道 {channel} 失败: {e}")
            return False

    def configure_channels(self, channels: List[str],
                          disable_others: bool = True,
                          channel_configs: List[Dict] = None) -> bool:
        """批量配置多个通道（支持详细参数）

        Args:
            channels: 通道列表，如 ["CH2_1", "CH2_3", "CH2_5", "CH2_7"]
            disable_others: 是否先禁用其他所有通道（防止数据错乱）
            channel_configs: 通道详细配置列表，每个元素为字典：
                {
                    'channel': 'CH2_1',
                    'type': 'VOLTAGE',  # 或 'TEMPERATURE'
                    'range': 10.0,
                    'thermocouple': 'K',  # 仅温度通道
                    'int_ext': 'INT'      # 仅温度通道
                }
                如果为None，则使用默认配置（电压，10V量程）

        Returns:
            是否全部配置成功
        """
        print(f"\n🔧 开始配置 {len(channels)} 个通道...")

        # 1. 先禁用所有通道（防止数据错乱）
        if disable_others:
            if not self.disable_all_channels():
                print("⚠️ 禁用通道失败，继续配置...")

        # 2. 配置指定的通道
        success_count = 0

        if channel_configs:
            # 使用详细配置
            for config in channel_configs:
                channel = config.get('channel')
                ch_type = config.get('type', 'VOLTAGE')
                range_val = config.get('range', 10.0)
                tc_type = config.get('thermocouple')
                int_ext = config.get('int_ext')

                if self.configure_channel(
                    channel=channel,
                    enabled=True,
                    channel_type=ch_type,
                    range_value=range_val,
                    thermocouple_type=tc_type,
                    int_ext=int_ext
                ):
                    success_count += 1
        else:
            # 使用默认配置（电压，10V量程）
            for channel in channels:
                if self.configure_channel(
                    channel=channel,
                    enabled=True,
                    channel_type='VOLTAGE',
                    range_value=10.0
                ):
                    success_count += 1

        print(f"\n✅ 通道配置完成: {success_count}/{len(channels)} 成功\n")
        return success_count == len(channels)

    def start_acquisition(self) -> bool:
        """启动数据采集"""
        return self.write(":STARt")

    def stop_acquisition(self) -> bool:
        """停止数据采集"""
        return self.write(":STOP")
    
    def get_channel_data(self, channels: List[str]) -> Dict[str, float]:
        """获取指定通道的实时数据

        Args:
            channels: 通道列表，如 ["CH2_1", "CH2_3"]

        Returns:
            字典 {通道名: 测量值}
        """
        # 获取实时数据快照
        self.write(":MEMory:GETReal")
        time.sleep(0.3)

        data = {}
        for channel in channels:
            response = self.query(f":MEMory:VREAL? {channel}")

            if response and '9.99999' not in response:
                try:
                    value = float(response)
                    data[channel] = value
                except ValueError:
                    pass

            time.sleep(0.01)

        return data

    @staticmethod
    def list_available_ports() -> List[Dict[str, str]]:
        """列出所有可用的COM端口

        Returns:
            端口信息列表，每个元素包含 {'port': 'COM3', 'description': '...', 'hwid': '...'}
        """
        if not USB_AVAILABLE:
            return []

        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'port': port.device,
                'description': port.description,
                'hwid': port.hwid,
                'manufacturer': getattr(port, 'manufacturer', 'Unknown')
            })

        return ports

    @staticmethod
    def is_usb_available() -> bool:
        """检查USB串口功能是否可用"""
        return USB_AVAILABLE




