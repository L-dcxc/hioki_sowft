#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通道配置对话框 - 映射4个LR8450通道到两个电池（含详细参数）"""

from __future__ import annotations

from typing import Optional, Dict, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QGroupBox, QMessageBox, QScrollArea, QWidget,
)


class ChannelConfigDialog(QDialog):
    """通道配置对话框（增强版：支持详细参数配置）"""

    # 电压量程选项（单位：V）
    VOLTAGE_RANGES = [
        ("10mV", 0.01),
        ("20mV", 0.02),
        ("100mV", 0.1),
        ("200mV", 0.2),
        ("1V", 1.0),
        ("2V", 2.0),
        ("10V", 10.0),
        ("20V", 20.0),
        ("100V", 100.0),
    ]

    # 温度量程选项（单位：°C）
    TEMP_RANGES = [
        ("100°C", 100),
        ("500°C", 500),
        ("2000°C", 2000),
    ]

    # 热电偶类型选项
    THERMOCOUPLE_TYPES = ["K", "J", "E", "T", "N", "R", "S", "C"]

    # INT/EXT选项
    INT_EXT_OPTIONS = ["INT", "EXT"]

    def __init__(self, parent: Optional[QDialog] = None, current_config: Dict = None):
        super().__init__(parent)
        self.setWindowTitle("通道配置")
        self.setMinimumSize(700, 600)

        # 当前配置（包含详细参数）
        self.config = current_config or {
            'ternary_voltage': {
                'channel': 'CH2_1',
                'type': 'VOLTAGE',
                'range': 10.0,
            },
            'ternary_temp': {
                'channel': 'CH2_3',
                'type': 'TEMPERATURE',
                'range': 500,
                'thermocouple': 'K',
                'int_ext': 'INT',
            },
            'blade_voltage': {
                'channel': 'CH2_4',
                'type': 'VOLTAGE',
                'range': 10.0,
            },
            'blade_temp': {
                'channel': 'CH2_5',
                'type': 'TEMPERATURE',
                'range': 500,
                'thermocouple': 'K',
                'int_ext': 'INT',
            },
        }

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 主容器
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("电池测试通道配置（详细参数）")
        title.setStyleSheet("color: #6dd5ed; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 说明
        desc = QLabel("请为两个电池配置电压和温度采集通道及详细参数")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #94a3b8; margin-bottom: 10px;")
        layout.addWidget(desc)

        # 三元电池配置
        ternary_group = QGroupBox("三元电池通道配置")
        ternary_group.setStyleSheet("QGroupBox { font-weight: bold; color: #6dd5ed; }")
        ternary_layout = QGridLayout(ternary_group)
        ternary_layout.setSpacing(12)

        # 三元电池 - 电压通道
        ternary_layout.addWidget(QLabel("电压通道:"), 0, 0)
        self.ternary_v_channel = self._create_channel_combo()
        self.ternary_v_channel.setCurrentText(self.config['ternary_voltage']['channel'])
        ternary_layout.addWidget(self.ternary_v_channel, 0, 1)

        ternary_layout.addWidget(QLabel("电压量程:"), 0, 2)
        self.ternary_v_range = self._create_voltage_range_combo()
        self._set_voltage_range(self.ternary_v_range, self.config['ternary_voltage']['range'])
        ternary_layout.addWidget(self.ternary_v_range, 0, 3)

        # 三元电池 - 温度通道
        ternary_layout.addWidget(QLabel("温度通道:"), 1, 0)
        self.ternary_t_channel = self._create_channel_combo()
        self.ternary_t_channel.setCurrentText(self.config['ternary_temp']['channel'])
        ternary_layout.addWidget(self.ternary_t_channel, 1, 1)

        ternary_layout.addWidget(QLabel("温度量程:"), 1, 2)
        self.ternary_t_range = self._create_temp_range_combo()
        self._set_temp_range(self.ternary_t_range, self.config['ternary_temp']['range'])
        ternary_layout.addWidget(self.ternary_t_range, 1, 3)

        ternary_layout.addWidget(QLabel("热电偶类型:"), 2, 0)
        self.ternary_t_tc = self._create_thermocouple_combo()
        self.ternary_t_tc.setCurrentText(self.config['ternary_temp']['thermocouple'])
        ternary_layout.addWidget(self.ternary_t_tc, 2, 1)

        ternary_layout.addWidget(QLabel("参考类型:"), 2, 2)
        self.ternary_t_int_ext = self._create_int_ext_combo()
        self.ternary_t_int_ext.setCurrentText(self.config['ternary_temp']['int_ext'])
        ternary_layout.addWidget(self.ternary_t_int_ext, 2, 3)

        layout.addWidget(ternary_group)

        # 刀片电池配置
        blade_group = QGroupBox("刀片电池通道配置")
        blade_group.setStyleSheet("QGroupBox { font-weight: bold; color: #6dd5ed; }")
        blade_layout = QGridLayout(blade_group)
        blade_layout.setSpacing(12)

        # 刀片电池 - 电压通道
        blade_layout.addWidget(QLabel("电压通道:"), 0, 0)
        self.blade_v_channel = self._create_channel_combo()
        self.blade_v_channel.setCurrentText(self.config['blade_voltage']['channel'])
        blade_layout.addWidget(self.blade_v_channel, 0, 1)

        blade_layout.addWidget(QLabel("电压量程:"), 0, 2)
        self.blade_v_range = self._create_voltage_range_combo()
        self._set_voltage_range(self.blade_v_range, self.config['blade_voltage']['range'])
        blade_layout.addWidget(self.blade_v_range, 0, 3)

        # 刀片电池 - 温度通道
        blade_layout.addWidget(QLabel("温度通道:"), 1, 0)
        self.blade_t_channel = self._create_channel_combo()
        self.blade_t_channel.setCurrentText(self.config['blade_temp']['channel'])
        blade_layout.addWidget(self.blade_t_channel, 1, 1)

        blade_layout.addWidget(QLabel("温度量程:"), 1, 2)
        self.blade_t_range = self._create_temp_range_combo()
        self._set_temp_range(self.blade_t_range, self.config['blade_temp']['range'])
        blade_layout.addWidget(self.blade_t_range, 1, 3)

        blade_layout.addWidget(QLabel("热电偶类型:"), 2, 0)
        self.blade_t_tc = self._create_thermocouple_combo()
        self.blade_t_tc.setCurrentText(self.config['blade_temp']['thermocouple'])
        blade_layout.addWidget(self.blade_t_tc, 2, 1)

        blade_layout.addWidget(QLabel("参考类型:"), 2, 2)
        self.blade_t_int_ext = self._create_int_ext_combo()
        self.blade_t_int_ext.setCurrentText(self.config['blade_temp']['int_ext'])
        blade_layout.addWidget(self.blade_t_int_ext, 2, 3)

        layout.addWidget(blade_group)
        
        # 参数说明
        info_group = QGroupBox("参数说明")
        info_layout = QVBoxLayout(info_group)
        info_text = QLabel(
            "• <b>电压量程</b>: 根据实际测量电压选择合适的量程\n"
            "• <b>温度量程</b>: 根据实际测量温度选择合适的量程\n"
            "• <b>热电偶类型</b>: K型最常用，适用于-200°C到1260°C\n"
            "• <b>参考类型</b>: INT=内部参考（常用），EXT=外部参考"
        )
        info_text.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        layout.addWidget(info_group)

        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #475569;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
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

        # 设置滚动区域
        scroll.setWidget(container)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_channel_combo(self) -> QComboBox:
        """创建通道选择下拉框"""
        combo = QComboBox()
        # 添加UNIT2的30个通道
        for i in range(1, 31):
            combo.addItem(f"CH2_{i}", f"CH2_{i}")
        return combo

    def _create_voltage_range_combo(self) -> QComboBox:
        """创建电压量程下拉框"""
        combo = QComboBox()
        for label, value in self.VOLTAGE_RANGES:
            combo.addItem(label, value)
        return combo

    def _create_temp_range_combo(self) -> QComboBox:
        """创建温度量程下拉框"""
        combo = QComboBox()
        for label, value in self.TEMP_RANGES:
            combo.addItem(label, value)
        return combo

    def _create_thermocouple_combo(self) -> QComboBox:
        """创建热电偶类型下拉框"""
        combo = QComboBox()
        for tc_type in self.THERMOCOUPLE_TYPES:
            combo.addItem(f"{tc_type}型", tc_type)
        return combo

    def _create_int_ext_combo(self) -> QComboBox:
        """创建INT/EXT下拉框"""
        combo = QComboBox()
        combo.addItem("内部参考 (INT)", "INT")
        combo.addItem("外部参考 (EXT)", "EXT")
        return combo

    def _set_voltage_range(self, combo: QComboBox, value: float):
        """设置电压量程"""
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                break

    def _set_temp_range(self, combo: QComboBox, value: float):
        """设置温度量程"""
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                break

    def _save_config(self):
        """保存配置"""
        # 检查是否有重复通道
        channels = [
            self.ternary_v_channel.currentText(),
            self.ternary_t_channel.currentText(),
            self.blade_v_channel.currentText(),
            self.blade_t_channel.currentText(),
        ]

        if len(set(channels)) != len(channels):
            QMessageBox.warning(self, "配置错误", "不能选择重复的通道！")
            return

        # 更新配置
        self.config = {
            'ternary_voltage': {
                'channel': self.ternary_v_channel.currentText(),
                'type': 'VOLTAGE',
                'range': self.ternary_v_range.currentData(),
            },
            'ternary_temp': {
                'channel': self.ternary_t_channel.currentText(),
                'type': 'TEMPERATURE',
                'range': self.ternary_t_range.currentData(),
                'thermocouple': self.ternary_t_tc.currentData(),
                'int_ext': self.ternary_t_int_ext.currentData(),
            },
            'blade_voltage': {
                'channel': self.blade_v_channel.currentText(),
                'type': 'VOLTAGE',
                'range': self.blade_v_range.currentData(),
            },
            'blade_temp': {
                'channel': self.blade_t_channel.currentText(),
                'type': 'TEMPERATURE',
                'range': self.blade_t_range.currentData(),
                'thermocouple': self.blade_t_tc.currentData(),
                'int_ext': self.blade_t_int_ext.currentData(),
            },
        }

        self.accept()

    def get_config(self) -> Dict:
        """获取配置"""
        return self.config.copy()




