"""About dialog for the application."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app import config


class AboutDialog(QDialog):
    """About dialog showing application information."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the about dialog."""
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle(f"\u5173\u4e8e {config.APP_NAME}")
        self.setFixedSize(500, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Application title and version
        title_label = QLabel(config.APP_NAME)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(f"\u7248\u672c: {config.APP_VERSION}")
        version_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                margin-bottom: 5px;
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Company info
        company_info = QGridLayout()
        
        company_info.addWidget(QLabel("\u516c\u53f8:"), 0, 0)
        company_info.addWidget(QLabel(config.COMPANY_NAME), 0, 1)
        
        company_info.addWidget(QLabel("\u8054\u7cfb\u7535\u8bdd:"), 1, 0)
        company_info.addWidget(QLabel(config.COMPANY_PHONE), 1, 1)
        
        company_info.addWidget(QLabel("\u90ae\u7bb1:"), 2, 0)
        company_info.addWidget(QLabel(config.COMPANY_EMAIL), 2, 1)

        company_widget = QWidget()
        company_widget.setLayout(company_info)
        layout.addWidget(company_widget)

        # Description
        description = QTextEdit()
        description.setReadOnly(True)
        description.setMaximumHeight(120)
        description.setPlainText(
            f"{config.DEVICE_FULL_NAME} \u662f\u4e00\u6b3e\u4e13\u4e1a\u7684\u6570\u636e\u91c7\u96c6\u4e0e\u5206\u6790\u8f6f\u4ef6\u3002"
        )
        layout.addWidget(description)

        # Technical info
        tech_info = QGridLayout()
        
        tech_info.addWidget(QLabel("\u6280\u672f\u652f\u6301:"), 0, 0)
        tech_info.addWidget(QLabel(config.TECH_STACK), 0, 1)
        
        tech_info.addWidget(QLabel("\u652f\u6301\u8bbe\u5907:"), 1, 0)
        tech_info.addWidget(QLabel(config.DEVICE_FULL_NAME), 1, 1)

        tech_widget = QWidget()
        tech_widget.setLayout(tech_info)
        layout.addWidget(tech_widget)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("\u786e\u5b9a")
        ok_button.setMinimumWidth(80)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)

        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #2c3e50;
                font-size: 11px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                padding: 8px;
                font-size: 11px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
