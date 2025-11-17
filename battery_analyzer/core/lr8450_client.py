#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450设备客户端（用于电池测试）"""

from __future__ import annotations

import socket
import time
from typing import Optional, Dict, List


class LR8450Client:
    """LR8450设备客户端 - 简化版，专门用于电池测试"""
    
    def __init__(self, ip_address: str, port: int = 8802):
        self.ip_address = ip_address
        self.port = port
        self.timeout = 10.0
        self.sock: Optional[socket.socket] = None
        self.connected = False
    
    def connect(self) -> bool:
        """连接到设备"""
        try:
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
            return True
            
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def disconnect(self) -> None:
        """断开连接"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.connected = False
    
    def query(self, command: str, timeout: float = 3.0) -> Optional[str]:
        """发送查询命令并接收响应"""
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
            print(f"查询错误 [{command}]: {e}")
            return None
    
    def write(self, command: str) -> bool:
        """发送写命令（不期待响应）"""
        if not self.sock:
            return False
        
        try:
            cmd_with_terminator = command + "\r\n"
            self.sock.sendall(cmd_with_terminator.encode('ascii'))
            time.sleep(0.1)
            return True
        except Exception as e:
            print(f"写入错误 [{command}]: {e}")
            return False
    
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




