#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据采集线程 - 在后台线程中采集数据，避免阻塞UI"""

from __future__ import annotations

from typing import Dict, List, Optional
import time

from PySide6.QtCore import QThread, Signal

from battery_analyzer.core.lr8450_client import LR8450Client


class DataAcquisitionThread(QThread):
    """数据采集线程
    
    在后台线程中定期从LR8450设备读取数据，通过信号发送到主线程更新UI。
    这样可以避免数据采集阻塞UI线程，保持界面流畅。
    """
    
    # 信号：数据采集成功 (时间戳, 通道数据字典)
    data_acquired = Signal(float, dict)
    
    # 信号：采集错误 (错误消息)
    error_occurred = Signal(str)
    
    # 信号：采集状态 (状态消息)
    status_changed = Signal(str)
    
    def __init__(
        self,
        device_client: LR8450Client,
        channels: List[str],
        interval_ms: int = 100,
        parent=None
    ):
        """初始化数据采集线程
        
        Args:
            device_client: LR8450设备客户端
            channels: 要采集的通道列表，如 ["CH2_1", "CH2_3", "CH2_5", "CH2_7"]
            interval_ms: 采集间隔（毫秒），默认100ms
            parent: 父对象
        """
        super().__init__(parent)
        
        self.device_client = device_client
        self.channels = channels
        self.interval_ms = interval_ms
        self.interval_sec = interval_ms / 1000.0
        
        self._running = False
        self._paused = False
        self.data_index = 0
    
    def run(self):
        """线程主循环 - 定期采集数据"""
        self._running = True
        self.data_index = 0
        
        self.status_changed.emit("数据采集线程已启动")
        
        while self._running:
            try:
                # 如果暂停，跳过采集
                if self._paused:
                    time.sleep(0.1)
                    continue
                
                # 计算时间戳
                timestamp = self.data_index * self.interval_sec
                
                # 从设备读取数据
                data = self.device_client.get_channel_data(self.channels)
                
                if data:
                    # 发送数据到主线程
                    self.data_acquired.emit(timestamp, data)
                    self.data_index += 1
                else:
                    # 数据读取失败
                    self.error_occurred.emit("设备无响应，未能读取数据")
                
                # 等待下一个采集周期
                time.sleep(self.interval_sec)
                
            except Exception as e:
                self.error_occurred.emit(f"数据采集错误: {str(e)}")
                time.sleep(self.interval_sec)
        
        self.status_changed.emit("数据采集线程已停止")
    
    def stop(self):
        """停止采集线程"""
        self._running = False
        self.wait()  # 等待线程结束
    
    def pause(self):
        """暂停采集"""
        self._paused = True
        self.status_changed.emit("数据采集已暂停")
    
    def resume(self):
        """恢复采集"""
        self._paused = False
        self.status_changed.emit("数据采集已恢复")
    
    def is_running(self) -> bool:
        """是否正在运行"""
        return self._running
    
    def is_paused(self) -> bool:
        """是否已暂停"""
        return self._paused

