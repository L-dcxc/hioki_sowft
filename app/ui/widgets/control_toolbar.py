"""Toolbar providing primary acquisition controls."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar


class ControlToolbar(QToolBar):
    """Top toolbar with file and acquisition controls."""

    start_requested = Signal()
    stop_requested = Signal()
    pause_requested = Signal()
    settings_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__("\u63a7\u5236", parent)
        self.setMovable(False)
        self.setFloatable(False)
        
        # Set toolbar style for button text
        self.setStyleSheet("""
            QToolBar {
                background-color: #e8e8e8;
                border: 1px solid #cccccc;
                color: #222222;
            }
            QToolBar QToolButton {
                color: #222222;
                background-color: transparent;
                border: none;
                padding: 6px;
                margin: 2px;
            }
            QToolBar QToolButton:hover {
                background-color: #d8d8d8;
                border: 1px solid #aaaaaa;
            }
            QToolBar QToolButton:pressed {
                background-color: #c8c8c8;
            }
        """)
        
        self._create_actions()

    def _create_actions(self) -> None:
        self.settings_action = QAction("\u8fde\u63a5\u8bbe\u7f6e", self)
        self.settings_action.triggered.connect(self.settings_requested.emit)
        self.addAction(self.settings_action)
        self.addSeparator()

        self.start_action = QAction("\u5f00\u59cb", self)
        self.start_action.triggered.connect(self.start_requested.emit)
        self.addAction(self.start_action)

        self.stop_action = QAction("\u505c\u6b62", self)
        self.stop_action.triggered.connect(self.stop_requested.emit)
        self.addAction(self.stop_action)

        self.pause_action = QAction("\u6682\u505c", self)
        self.pause_action.triggered.connect(self.pause_requested.emit)
        self.addAction(self.pause_action)

