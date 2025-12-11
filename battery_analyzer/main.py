#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Battery Analyzer 应用入口。"""

from __future__ import annotations

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from battery_analyzer.ui.style import get_stylesheet
from battery_analyzer.ui.main_window import MainWindow


def main() -> None:
    # 启用高DPI缩放支持，避免在125%缩放或高分屏下控件被异常放大/裁切
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setApplicationName("电池电压与温升分析软件")
    app.setStyleSheet(get_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

