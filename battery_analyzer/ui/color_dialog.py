#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单的中文颜色选择对话框。"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QLabel,
    QWidget,
)
from PySide6.QtGui import QColor


class SimpleColorDialog(QDialog):
    """简单的中文颜色选择对话框（预设颜色）。"""
    
    # 预设常用颜色
    PRESET_COLORS = [
        # 第一行：红橙黄绿青蓝紫
        "#ff0000", "#ff6600", "#ffcc00", "#00ff00", "#00ffff", "#0066ff", "#9900ff",
        # 第二行：亮色系
        "#ff3366", "#ff9933", "#ffff33", "#66ff66", "#66ffff", "#6699ff", "#cc66ff",
        # 第三行：深色系
        "#990000", "#cc6600", "#999900", "#009900", "#009999", "#003399", "#660099",
        # 第四行：灰度
        "#ffffff", "#cccccc", "#999999", "#666666", "#333333", "#000000", "#ff9933",
        # 第五行：特殊（原图默认色）
        "#ff9933", "#66ccff", "#33c1ff", "#ffb347", "#4a90e2", "#6dd5ed", "#98d2ff",
    ]
    
    def __init__(self, current_color: QColor, title: str = "选择颜色", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.selected_color = current_color
        
        self.setFixedSize(420, 320)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #6dd5ed;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 颜色网格
        grid = QGridLayout()
        grid.setSpacing(6)
        
        row = 0
        col = 0
        for color_hex in self.PRESET_COLORS:
            btn = QPushButton()
            btn.setFixedSize(50, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_hex};
                    border: 2px solid #2b4b7d;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    border: 2px solid #6dd5ed;
                }}
            """)
            btn.clicked.connect(lambda checked, c=color_hex: self._select_color(c))
            grid.addWidget(btn, row, col)
            
            col += 1
            if col >= 7:
                col = 0
                row += 1
        
        layout.addLayout(grid)
        
        # 当前选择预览
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("当前颜色："))
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(100, 40)
        self.preview_label.setStyleSheet(f"""
            background-color: {current_color.name()};
            border: 2px solid #2b4b7d;
            border-radius: 4px;
        """)
        preview_layout.addWidget(self.preview_label)
        preview_layout.addStretch()
        layout.addLayout(preview_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("确定")
        ok_btn.setFixedWidth(80)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedWidth(80)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _select_color(self, color_hex: str) -> None:
        """选择颜色并更新预览。"""
        self.selected_color = QColor(color_hex)
        self.preview_label.setStyleSheet(f"""
            background-color: {color_hex};
            border: 2px solid #2b4b7d;
            border-radius: 4px;
        """)
    
    def get_color(self) -> QColor:
        """获取选择的颜色。"""
        return self.selected_color
    
    @staticmethod
    def get_color_from_dialog(current_color: QColor, title: str, parent: Optional[QWidget] = None) -> Optional[QColor]:
        """静态方法：打开对话框并返回选择的颜色。"""
        dialog = SimpleColorDialog(current_color, title, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_color()
        return None

