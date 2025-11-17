#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""设备连接对话框"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox,
)


class DeviceConnectDialog(QDialog):
    """设备连接对话框"""
    
    def __init__(self, parent: Optional[QDialog] = None):
        super().__init__(parent)
        self.setWindowTitle("连接LR8450设备")
        self.setFixedSize(400, 250)
        
        self.device_ip = "192.168.2.136"
        self.device_port = 8802
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("LR8450设备连接设置")
        title.setStyleSheet("color: #6dd5ed; font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 连接参数
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.ip_edit = QLineEdit(self.device_ip)
        self.ip_edit.setPlaceholderText("192.168.2.136")
        form_layout.addRow("设备IP地址:", self.ip_edit)
        
        self.port_edit = QLineEdit(str(self.device_port))
        self.port_edit.setPlaceholderText("8802")
        form_layout.addRow("端口号:", self.port_edit)
        
        layout.addLayout(form_layout)
        
        # 提示
        hint = QLabel("提示：LR8450的SCPI控制端口通常是8802")
        hint.setStyleSheet("color: #7fb6ff; font-size: 11px;")
        layout.addWidget(hint)
        
        layout.addStretch()
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        btn_connect = QPushButton("连接")
        btn_connect.clicked.connect(self._connect)
        btn_connect.setStyleSheet("""
            QPushButton {
                background-color: #0080ff;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1992ff;
            }
        """)
        button_layout.addWidget(btn_connect)
        
        layout.addLayout(button_layout)
    
    def _connect(self):
        """连接设备"""
        try:
            self.device_ip = self.ip_edit.text().strip()
            self.device_port = int(self.port_edit.text().strip())
            
            if not self.device_ip:
                QMessageBox.warning(self, "输入错误", "请输入设备IP地址")
                return
            
            if self.device_port <= 0 or self.device_port > 65535:
                QMessageBox.warning(self, "输入错误", "端口号必须在1-65535之间")
                return
            
            self.accept()
            
        except ValueError:
            QMessageBox.warning(self, "输入错误", "端口号必须是数字")
    
    def get_connection_params(self) -> tuple[str, int]:
        """获取连接参数"""
        return self.device_ip, self.device_port




