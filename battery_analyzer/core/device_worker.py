#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""设备操作后台线程 - 在后台线程中执行设备配置等耗时操作，避免阻塞UI"""

from __future__ import annotations

from typing import Dict, List, Optional
import time

from PySide6.QtCore import QThread, Signal


class DeviceConfigWorker(QThread):
    """设备配置工作线程
    
    在后台线程中执行设备配置操作（如配置通道、启动/停止采集等），
    避免阻塞UI线程，保持界面流畅。
    """
    
    # 信号：配置完成 (成功标志, 消息)
    config_finished = Signal(bool, str)
    
    # 信号：进度更新 (进度百分比, 消息)
    progress_updated = Signal(int, str)
    
    def __init__(
        self,
        device_client,
        channels: List[str],
        channel_configs: List[Dict],
        parent=None
    ):
        """初始化配置工作线程
        
        Args:
            device_client: LR8450设备客户端
            channels: 要配置的通道列表
            channel_configs: 通道详细配置列表
            parent: 父对象
        """
        super().__init__(parent)
        
        self.device_client = device_client
        self.channels = channels
        self.channel_configs = channel_configs
    
    def run(self):
        """执行配置操作"""
        try:
            self.progress_updated.emit(10, "停止当前采集...")
            
            # 停止采集
            self.device_client.write(":STOP")
            time.sleep(0.3)
            
            self.progress_updated.emit(20, "禁用所有通道...")
            
            # 禁用所有通道
            self.device_client.disable_all_channels()
            
            self.progress_updated.emit(40, f"配置 {len(self.channels)} 个通道...")
            
            # 配置通道
            success_count = 0
            total = len(self.channel_configs)
            
            for i, config in enumerate(self.channel_configs):
                channel = config.get('channel')
                ch_type = config.get('type', 'VOLTAGE')
                range_val = config.get('range', 10.0)
                tc_type = config.get('thermocouple')
                int_ext = config.get('int_ext')
                
                progress = 40 + int((i + 1) / total * 40)
                self.progress_updated.emit(progress, f"配置通道 {channel}...")
                
                if self.device_client.configure_channel(
                    channel=channel,
                    enabled=True,
                    channel_type=ch_type,
                    range_value=range_val,
                    thermocouple_type=tc_type,
                    int_ext=int_ext
                ):
                    success_count += 1
            
            self.progress_updated.emit(85, "启动采集...")
            
            # 启动采集
            self.device_client.write(":STARt")
            time.sleep(0.5)
            
            self.progress_updated.emit(100, "配置完成")
            
            if success_count == len(self.channels):
                self.config_finished.emit(True, f"✓ 通道配置完成: {success_count}/{len(self.channels)} 成功")
            else:
                self.config_finished.emit(True, f"⚠️ 通道配置部分成功: {success_count}/{len(self.channels)}")
                
        except Exception as e:
            self.config_finished.emit(False, f"❌ 配置失败: {str(e)}")


class DeviceStopWorker(QThread):
    """设备停止工作线程

    在后台线程中执行停止采集操作。
    """

    # 信号：停止完成 (成功标志, 消息)
    stop_finished = Signal(bool, str)

    def __init__(self, device_client, parent=None):
        """初始化停止工作线程

        Args:
            device_client: LR8450设备客户端
            parent: 父对象
        """
        super().__init__(parent)
        self.device_client = device_client

    def run(self):
        """执行停止操作 - 使用多次重试和验证确保停止成功"""
        try:
            max_retries = 5
            success = False

            for attempt in range(max_retries):
                print(f"   尝试停止设备 (第 {attempt + 1}/{max_retries} 次)...")

                # 发送停止命令
                result = self.device_client.write(":STOP")
                time.sleep(0.3)

                # 再发送一次确保命令到达
                self.device_client.write(":STOP")
                time.sleep(0.2)

                if result:
                    success = True
                    break

                time.sleep(0.2)

            if success:
                self.stop_finished.emit(True, "✓ 设备已停止采集")
            else:
                self.stop_finished.emit(False, "⚠️ 停止命令发送失败，请手动检查设备")

        except Exception as e:
            self.stop_finished.emit(False, f"❌ 停止失败: {str(e)}")


class DeviceStartWorker(QThread):
    """设备启动工作线程
    
    在后台线程中执行快速启动采集操作（不重新配置通道）。
    """
    
    # 信号：启动完成 (成功标志, 消息)
    start_finished = Signal(bool, str)
    
    def __init__(self, device_client, parent=None):
        """初始化启动工作线程
        
        Args:
            device_client: LR8450设备客户端
            parent: 父对象
        """
        super().__init__(parent)
        self.device_client = device_client
    
    def run(self):
        """执行启动操作"""
        try:
            result = self.device_client.write(":STARt")
            if result:
                time.sleep(0.2)
                self.start_finished.emit(True, "✓ 采集已启动")
            else:
                self.start_finished.emit(False, "⚠️ 启动命令发送失败")
        except Exception as e:
            self.start_finished.emit(False, f"❌ 启动失败: {str(e)}")

