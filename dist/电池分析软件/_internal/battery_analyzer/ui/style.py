#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""应用样式（深色主题，简体中文）。"""

from __future__ import annotations


def get_stylesheet() -> str:
    return """
    QMainWindow { background-color: #0c1830; color: #cfe6ff; }
    QWidget { font-family: "Microsoft YaHei", "PingFang SC", "Source Han Sans CN"; }

    /* 左侧控制面板 */
    QGroupBox { border: 1px solid #2b4b7d; border-radius: 6px; margin-top: 10px; }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; color: #86b7ff; }

    QPushButton { background-color: #12325f; color: #cfe6ff; border: 1px solid #2b4b7d; border-radius: 4px; padding: 8px 12px; }
    QPushButton:hover { background-color: #1a417a; }
    QPushButton:pressed { background-color: #0d284e; }
    QPushButton#startButton { background-color: #0080ff; border: 1px solid #66b3ff; color: #eaf5ff; font-size: 24px; font-weight: bold; padding: 12px; }
    QPushButton#startButton:hover { background-color: #1992ff; }

    QLabel { color: #cfe6ff; }
    QLineEdit, QSpinBox, QComboBox { background-color: #0f223f; color: #e2f1ff; border: 1px solid #2b4b7d; border-radius: 4px; padding: 4px 6px; }

    /* KPI 数字显示 */
    QLabel.kpi { background-color: #0b213f; border: 1px solid #2b4b7d; border-radius: 6px; padding: 8px 12px; color: #98d2ff; font-weight: bold; font-size: 28px; }
    QLabel.kpiTitle { color: #7fb6ff; font-size: 12px; }
    QStatusBar { background-color: #0b213f; color: #98d2ff; }
    """


