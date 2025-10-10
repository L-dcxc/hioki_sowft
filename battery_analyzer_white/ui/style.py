#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""白色主题样式（简洁现代风格）。"""

from __future__ import annotations


def get_stylesheet() -> str:
    return """
    /* 白色简洁主题 */
    QMainWindow { 
        background-color: #ffffff; 
        color: #2c3e50;
    }
    QWidget { 
        font-family: "Microsoft YaHei UI", "Segoe UI", "PingFang SC"; 
    }

    /* 顶部标题栏 */
    QWidget#titleBar {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #3498db, stop:0.5 #2980b9, stop:1 #3498db);
        border-bottom: 3px solid #2980b9;
    }
    QLabel#mainTitle {
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    QPushButton#titleBtn {
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 13px;
    }
    QPushButton#titleBtn:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }

    /* 控制面板（顶部横向） */
    QWidget#controlBar {
        background-color: #f8f9fa;
        border-bottom: 2px solid #e0e0e0;
    }
    QPushButton {
        background-color: #ffffff;
        color: #2c3e50;
        border: 2px solid #3498db;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #3498db;
        color: #ffffff;
    }
    QPushButton:pressed {
        background-color: #2980b9;
    }
    QPushButton#startButton {
        background-color: #27ae60;
        color: #ffffff;
        border: none;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 32px;
        min-width: 120px;
    }
    QPushButton#startButton:hover {
        background-color: #229954;
    }

    QLabel { color: #2c3e50; }
    QLineEdit, QSpinBox, QComboBox {
        background-color: #ffffff;
        color: #2c3e50;
        border: 2px solid #bdc3c7;
        border-radius: 4px;
        padding: 6px;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
        border-color: #3498db;
    }

    /* KPI 卡片 */
    QLabel.kpi {
        background-color: #f8f9fa;
        border: 2px solid #3498db;
        border-radius: 8px;
        padding: 12px;
        color: #2c3e50;
        font-weight: bold;
        font-size: 32px;
    }
    QLabel.kpiTitle {
        color: #7f8c8d;
        font-size: 13px;
        font-weight: 600;
    }

    QStatusBar {
        background-color: #f8f9fa;
        color: #7f8c8d;
        border-top: 1px solid #e0e0e0;
    }
    """

