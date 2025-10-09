"""Device configuration dialog."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class DeviceConfigDialog(QDialog):
    """\u8bbe\u5907\u914d\u7f6e\u5bf9\u8bdd\u6846 - \u53cc\u51fb\u8bbe\u5907\u65f6\u663e\u793a\u7684\u8bbe\u7f6e\u6846"""
    
    def __init__(self, device, parent=None):
        """\u521d\u59cb\u5316\u8bbe\u5907\u914d\u7f6e\u5bf9\u8bdd\u6846"""
        super().__init__(parent)
        self.device = device
        self.setWindowTitle(f"\u8bbe\u5907\u914d\u7f6e - {device.model}")
        self.resize(500, 400)
        self.setModal(True)
        self._setup_ui()
    
    def _setup_ui(self):
        """\u8bbe\u7f6e\u7528\u6237\u754c\u9762"""
        layout = QVBoxLayout(self)
        
        # \u8bbe\u5907\u4fe1\u606f\u663e\u793a
        info_group = QGroupBox("\u8bbe\u5907\u4fe1\u606f")
        info_layout = QFormLayout(info_group)
        
        info_layout.addRow("\u8bbe\u5907\u578b\u53f7:", QLabel(self.device.model))
        info_layout.addRow("\u5236\u9020\u5546:", QLabel(self.device.manufacturer))
        info_layout.addRow("\u5e8f\u5217\u53f7:", QLabel(self.device.serial))
        info_layout.addRow("\u56fa\u4ef6\u7248\u672c:", QLabel(self.device.firmware))
        info_layout.addRow("IP\u5730\u5740:", QLabel(self.device.ip_address))
        info_layout.addRow("\u7aef\u53e3:", QLabel(str(self.device.port)))
        info_layout.addRow("\u8fde\u63a5\u72b6\u6001:", QLabel(self.device.status.value))
        
        layout.addWidget(info_group)
        
        # \u914d\u7f6e\u9009\u9879
        config_group = QGroupBox("\u914d\u7f6e\u9009\u9879")
        config_layout = QVBoxLayout(config_group)
        
        # \u91cd\u8981\u8bf4\u660e
        note_label = QLabel(
            "\u8bf7\u70b9\u51fb\"\u63a5\u53d7\u8bbe\u7f6e\"\u6309\u94ae\u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f\uff0c\n"
            "\u7cfb\u7edf\u5c06\u81ea\u52a8\u83b7\u53d6\u8bbe\u5907\u7684\u578b\u53f7\u3001\u7248\u672c\u548c\u8bbe\u7f6e\u4fe1\u606f\uff0c\n"
            "\u5e76\u540c\u6b65\u5230\u540e\u7eed\u7684\u5355\u5143\u8bbe\u7f6e\u3001\u6d4b\u91cf\u8bbe\u7f6e\u548c\u901a\u9053\u8bbe\u7f6e\u4e2d\u3002"
        )
        note_label.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                color: #856404;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        config_layout.addWidget(note_label)
        
        layout.addWidget(config_group)
        
        # \u6309\u94ae\u533a\u57df
        button_layout = QHBoxLayout()
        
        self.accept_btn = QPushButton("\u63a5\u53d7\u8bbe\u7f6e")
        self.accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        self.cancel_btn = QPushButton("\u53d6\u6d88")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # \u8fde\u63a5\u4fe1\u53f7
        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
