#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""灰色主题样式（专业商务风格）。"""

from __future__ import annotations


def get_stylesheet() -> str:
    return """
    /* 灰色专业主题 */
    QMainWindow { 
        background-color: #2b2b2b; 
        color: #e0e0e0;
    }
    QWidget { 
        font-family: "Microsoft YaHei UI", "Segoe UI", "PingFang SC"; 
    }

    /* 顶部工具栏 */
    QWidget#toolbar {
        background-color: #3a3a3a;
        border-bottom: 2px solid #555555;
    }
    QLabel#appTitle {
        color: #ffa500;
        font-size: 20px;
        font-weight: bold;
    }

    /* 卡片容器 */
    QWidget#card {
        background-color: #353535;
        border: 1px solid #555555;
        border-radius: 8px;
    }
    QLabel#cardTitle {
        color: #ffa500;
        font-size: 14px;
        font-weight: bold;
        border-bottom: 2px solid #555555;
        padding-bottom: 6px;
    }

    QPushButton {
        background-color: #454545;
        color: #e0e0e0;
        border: 1px solid #666666;
        border-radius: 5px;
        padding: 8px 14px;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #555555;
        border-color: #ffa500;
    }
    QPushButton:pressed {
        background-color: #3a3a3a;
    }
    QPushButton#actionBtn {
        background-color: #e67e22;
        color: #ffffff;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 24px;
    }
    QPushButton#actionBtn:hover {
        background-color: #d35400;
    }

    QLabel { color: #e0e0e0; }
    QLineEdit, QSpinBox, QComboBox {
        background-color: #404040;
        color: #e0e0e0;
        border: 1px solid #666666;
        border-radius: 4px;
        padding: 6px;
    }
    QLineEdit:focus, QSpinBox:focus {
        border-color: #ffa500;
    }

    /* KPI 显示 */
    QLabel.kpiValue {
        background-color: #404040;
        border: 2px solid #ffa500;
        border-radius: 6px;
        padding: 10px;
        color: #ffa500;
        font-weight: bold;
        font-size: 28px;
    }
    QLabel.kpiLabel {
        color: #b0b0b0;
        font-size: 12px;
    }

    QStatusBar {
        background-color: #3a3a3a;
        color: #b0b0b0;
        border-top: 1px solid #555555;
    }
    """

