#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Battery Analyzer - Gray Theme 应用入口。"""

from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication

from battery_analyzer_gray.ui.style import get_stylesheet
from battery_analyzer_gray.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("电池分析软件 - 专业版")
    app.setStyleSheet(get_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

