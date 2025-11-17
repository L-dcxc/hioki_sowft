#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通道配置对话框 - 映射4个LR8450通道到两个电池"""

from __future__ import annotations

from typing import Optional, Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QGroupBox, QMessageBox,
)


class ChannelConfigDialog(QDialog):
    """通道配置对话框"""
    
    def __init__(self, parent: Optional[QDialog] = None):
        super().__init__(parent)
        self.setWindowTitle("通道配置")
        self.setFixedSize(500, 400)
        
        # 当前配置
        self.config = {
            'ternary_voltage': 'CH2_1',
            'ternary_temp': 'CH2_3',
            'blade_voltage': 'CH2_4',
            'blade_temp': 'CH2_5',
        }
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("电池测试通道配置")
        title.setStyleSheet("color: #6dd5ed; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 说明
        desc = QLabel("请为两个电池配置电压和温度采集通道")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # 三元电池配置
        ternary_group = QGroupBox("三元电池通道配置")
        ternary_layout = QGridLayout(ternary_group)
        ternary_layout.setSpacing(12)
        
        ternary_layout.addWidget(QLabel("电压通道:"), 0, 0)
        self.ternary_v_combo = self._create_channel_combo()
        self.ternary_v_combo.setCurrentText(self.config['ternary_voltage'])
        ternary_layout.addWidget(self.ternary_v_combo, 0, 1)
        
        ternary_layout.addWidget(QLabel("温度通道:"), 1, 0)
        self.ternary_t_combo = self._create_channel_combo()
        self.ternary_t_combo.setCurrentText(self.config['ternary_temp'])
        ternary_layout.addWidget(self.ternary_t_combo, 1, 1)
        
        layout.addWidget(ternary_group)
        
        # 刀片电池配置
        blade_group = QGroupBox("刀片电池通道配置")
        blade_layout = QGridLayout(blade_group)
        blade_layout.setSpacing(12)
        
        blade_layout.addWidget(QLabel("电压通道:"), 0, 0)
        self.blade_v_combo = self._create_channel_combo()
        self.blade_v_combo.setCurrentText(self.config['blade_voltage'])
        blade_layout.addWidget(self.blade_v_combo, 0, 1)
        
        blade_layout.addWidget(QLabel("温度通道:"), 1, 0)
        self.blade_t_combo = self._create_channel_combo()
        self.blade_t_combo.setCurrentText(self.config['blade_temp'])
        blade_layout.addWidget(self.blade_t_combo, 1, 1)
        
        layout.addWidget(blade_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        btn_save = QPushButton("保存配置")
        btn_save.clicked.connect(self._save_config)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        button_layout.addWidget(btn_save)
        
        layout.addLayout(button_layout)
    
    def _create_channel_combo(self) -> QComboBox:
        """创建通道选择下拉框"""
        combo = QComboBox()
        
        # 添加UNIT2的30个通道
        for i in range(1, 31):
            combo.addItem(f"CH2_{i}", f"CH2_{i}")
        
        return combo
    
    def _save_config(self):
        """保存配置"""
        # 检查是否有重复通道
        channels = [
            self.ternary_v_combo.currentText(),
            self.ternary_t_combo.currentText(),
            self.blade_v_combo.currentText(),
            self.blade_t_combo.currentText(),
        ]
        
        if len(set(channels)) != len(channels):
            QMessageBox.warning(self, "配置错误", "不能选择重复的通道！")
            return
        
        # 更新配置
        self.config = {
            'ternary_voltage': self.ternary_v_combo.currentText(),
            'ternary_temp': self.ternary_t_combo.currentText(),
            'blade_voltage': self.blade_v_combo.currentText(),
            'blade_temp': self.blade_t_combo.currentText(),
        }
        
        self.accept()
    
    def get_config(self) -> Dict[str, str]:
        """获取配置"""
        return self.config.copy()




