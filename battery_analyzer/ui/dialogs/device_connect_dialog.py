#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""设备连接对话框"""

from __future__ import annotations

from typing import Optional, Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox,
    QRadioButton, QButtonGroup, QComboBox, QGroupBox,
)

from battery_analyzer.core.lr8450_client import LR8450Client


class DeviceConnectDialog(QDialog):
    """设备连接对话框 - 支持TCP/IP和USB两种连接方式"""

    def __init__(self, parent: Optional[QDialog] = None):
        super().__init__(parent)
        self.setWindowTitle("连接LR8450设备")
        self.setFixedSize(450, 400)

        self.connection_type: Literal["TCP", "USB"] = "TCP"
        self.device_ip = "192.168.2.136"
        self.device_port = 8802
        self.com_port = ""

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # 标题
        title = QLabel("LR8450设备连接设置")
        title.setStyleSheet("color: #6dd5ed; font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 连接方式选择
        connection_group = QGroupBox("连接方式")
        connection_layout = QVBoxLayout(connection_group)

        self.radio_tcp = QRadioButton("TCP/IP 网络连接")
        self.radio_usb = QRadioButton("USB 串口连接")
        self.radio_tcp.setChecked(True)

        self.radio_tcp.toggled.connect(self._on_connection_type_changed)

        connection_layout.addWidget(self.radio_tcp)
        connection_layout.addWidget(self.radio_usb)

        layout.addWidget(connection_group)

        # TCP/IP 参数
        self.tcp_group = QGroupBox("TCP/IP 连接参数")
        tcp_layout = QFormLayout(self.tcp_group)
        tcp_layout.setSpacing(12)

        self.ip_edit = QLineEdit(self.device_ip)
        self.ip_edit.setPlaceholderText("192.168.2.136")
        tcp_layout.addRow("设备IP地址:", self.ip_edit)

        self.port_edit = QLineEdit(str(self.device_port))
        self.port_edit.setPlaceholderText("8802")
        tcp_layout.addRow("端口号:", self.port_edit)

        tcp_hint = QLabel("提示：SCPI控制端口通常是8802")
        tcp_hint.setStyleSheet("color: #7fb6ff; font-size: 11px;")
        tcp_layout.addRow("", tcp_hint)

        layout.addWidget(self.tcp_group)

        # USB 参数
        self.usb_group = QGroupBox("USB 串口参数")
        usb_layout = QFormLayout(self.usb_group)
        usb_layout.setSpacing(12)

        self.com_combo = QComboBox()
        self.com_combo.setEditable(True)
        usb_layout.addRow("COM端口:", self.com_combo)

        btn_refresh = QPushButton("刷新端口列表")
        btn_refresh.clicked.connect(self._refresh_com_ports)
        usb_layout.addRow("", btn_refresh)

        # 检查USB是否可用
        if not LR8450Client.is_usb_available():
            usb_hint = QLabel("⚠️ 需要安装 pyserial 库\n运行: pip install pyserial")
            usb_hint.setStyleSheet("color: #ff9933; font-size: 11px;")
            usb_layout.addRow("", usb_hint)
            self.radio_usb.setEnabled(False)
        else:
            usb_hint = QLabel("提示：请先安装HIOKI USB驱动")
            usb_hint.setStyleSheet("color: #7fb6ff; font-size: 11px;")
            usb_layout.addRow("", usb_hint)

        layout.addWidget(self.usb_group)
        self.usb_group.setVisible(False)  # 默认隐藏USB设置

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

        # 初始化COM端口列表
        if LR8450Client.is_usb_available():
            self._refresh_com_ports()
    
    def _on_connection_type_changed(self, checked: bool):
        """连接方式改变时的处理"""
        if checked:  # TCP被选中
            self.tcp_group.setVisible(True)
            self.usb_group.setVisible(False)
            self.connection_type = "TCP"
        else:  # USB被选中
            self.tcp_group.setVisible(False)
            self.usb_group.setVisible(True)
            self.connection_type = "USB"

    def _refresh_com_ports(self):
        """刷新COM端口列表"""
        self.com_combo.clear()

        ports = LR8450Client.list_available_ports()

        if not ports:
            self.com_combo.addItem("未检测到COM端口")
            return

        for port_info in ports:
            port_name = port_info['port']
            description = port_info['description']
            display_text = f"{port_name} - {description}"
            self.com_combo.addItem(display_text, port_name)

    def _connect(self):
        """连接设备"""
        try:
            if self.connection_type == "TCP":
                # TCP连接验证
                self.device_ip = self.ip_edit.text().strip()
                self.device_port = int(self.port_edit.text().strip())

                if not self.device_ip:
                    QMessageBox.warning(self, "输入错误", "请输入设备IP地址")
                    return

                if self.device_port <= 0 or self.device_port > 65535:
                    QMessageBox.warning(self, "输入错误", "端口号必须在1-65535之间")
                    return

            else:  # USB连接验证
                if self.com_combo.count() == 0 or self.com_combo.currentText() == "未检测到COM端口":
                    QMessageBox.warning(self, "输入错误", "未检测到可用的COM端口\n\n请确保：\n1. 已安装HIOKI USB驱动\n2. 设备已通过USB连接到电脑")
                    return

                # 获取实际的COM端口名（从userData或文本中提取）
                port_data = self.com_combo.currentData()
                if port_data:
                    self.com_port = port_data
                else:
                    # 从文本中提取COM端口（格式：COM3 - description）
                    text = self.com_combo.currentText()
                    self.com_port = text.split(' - ')[0].strip() if ' - ' in text else text.strip()

                if not self.com_port or self.com_port == "未检测到COM端口":
                    QMessageBox.warning(self, "输入错误", "请选择有效的COM端口")
                    return

            self.accept()

        except ValueError:
            QMessageBox.warning(self, "输入错误", "端口号必须是数字")

    def get_connection_params(self) -> dict:
        """获取连接参数

        Returns:
            包含连接参数的字典：
            - connection_type: "TCP" 或 "USB"
            - ip_address: TCP IP地址（TCP模式）
            - port: TCP端口（TCP模式）
            - com_port: COM端口（USB模式）
        """
        return {
            'connection_type': self.connection_type,
            'ip_address': self.device_ip,
            'port': self.device_port,
            'com_port': self.com_port,
        }




