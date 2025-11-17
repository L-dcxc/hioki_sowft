"""Manual add device dialog with comprehensive settings."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
)


class ManualAddDeviceDialog(QDialog):
    """\u624b\u52a8\u6dfb\u52a0\u8bbe\u5907\u5bf9\u8bdd\u6846 - \u5305\u542b\u5b8c\u6574\u7684\u8bbe\u7f6e\u9009\u9879"""
    
    def __init__(self, parent=None):
        """\u521d\u59cb\u5316\u624b\u52a8\u6dfb\u52a0\u8bbe\u5907\u5bf9\u8bdd\u6846"""
        super().__init__(parent)
        self.setWindowTitle("\u65b0\u589e\u52a0\u6570\u91c7")
        self.resize(400, 600)
        self.setModal(True)
        self._setup_ui()
        self._setup_defaults()
    
    def _setup_ui(self):
        """\u8bbe\u7f6e\u7528\u6237\u754c\u9762"""
        layout = QVBoxLayout(self)
        
        # \u7cfb\u7edf\u4fe1\u606f\u7ec4
        self._create_system_info_group(layout)
        
        # \u901a\u4fe1\u8bbe\u7f6e\u7ec4
        self._create_communication_group(layout)
        
        # \u6309\u94ae\u533a\u57df
        self._create_buttons(layout)
    
    def _create_system_info_group(self, layout):
        """\u521b\u5efa\u7cfb\u7edf\u4fe1\u606f\u7ec4"""
        system_group = QGroupBox("\u7cfb\u7edf")
        system_layout = QFormLayout(system_group)
        
        # No.
        self.no_edit = QLineEdit("2")
        system_layout.addRow("No.", self.no_edit)
        
        # \u673a\u578b
        self.model_combo = QComboBox()
        self.model_combo.addItems(["8423", "LR8450", "LR8450-01"])
        self.model_combo.setCurrentText("8423")
        system_layout.addRow("\u673a\u578b", self.model_combo)
        
        # \u6ce8\u91ca
        self.comment_edit = QLineEdit()
        system_layout.addRow("\u6ce8\u91ca", self.comment_edit)
        
        layout.addWidget(system_group)
    
    def _create_communication_group(self, layout):
        """\u521b\u5efa\u901a\u4fe1\u8bbe\u7f6e\u7ec4"""
        comm_group = QGroupBox("\u901a\u4fe1")
        comm_layout = QFormLayout(comm_group)
        
        # \u63a5\u53e3\u9009\u62e9
        interface_layout = QHBoxLayout()
        self.usb_radio = QRadioButton("USB")
        self.lan_radio = QRadioButton("LAN")
        self.lan_radio.setChecked(True)  # \u9ed8\u8ba4\u9009\u62e9LAN
        interface_layout.addWidget(self.usb_radio)
        interface_layout.addWidget(self.lan_radio)
        interface_layout.addStretch()
        comm_layout.addRow("\u63a5\u53e3", interface_layout)
        
        # \u5730\u5740
        self.address_edit = QLineEdit()
        comm_layout.addRow("\u5730\u5740", self.address_edit)
        
        # DHCP
        self.dhcp_combo = QComboBox()
        self.dhcp_combo.addItems(["OFF", "ON"])
        comm_layout.addRow("DHCP", self.dhcp_combo)
        
        # \u5b50\u7f51\u63a9\u7801
        subnet_layout = QHBoxLayout()
        self.subnet_1 = QSpinBox()
        self.subnet_1.setRange(0, 255)
        self.subnet_1.setValue(255)
        self.subnet_2 = QSpinBox()
        self.subnet_2.setRange(0, 255)
        self.subnet_2.setValue(255)
        self.subnet_3 = QSpinBox()
        self.subnet_3.setRange(0, 255)
        self.subnet_3.setValue(255)
        self.subnet_4 = QSpinBox()
        self.subnet_4.setRange(0, 255)
        self.subnet_4.setValue(0)
        
        subnet_layout.addWidget(self.subnet_1)
        subnet_layout.addWidget(QLabel("."))
        subnet_layout.addWidget(self.subnet_2)
        subnet_layout.addWidget(QLabel("."))
        subnet_layout.addWidget(self.subnet_3)
        subnet_layout.addWidget(QLabel("."))
        subnet_layout.addWidget(self.subnet_4)
        subnet_layout.addStretch()
        
        comm_layout.addRow("\u5b50\u7f51\u63a9\u7801", subnet_layout)
        
        # \u7aef\u53e3\u53f7
        self.port_edit = QLineEdit("8802")
        comm_layout.addRow("\u7aef\u53e3\u53f7", self.port_edit)
        
        # \u7f51\u5173 - \u7b2c\u4e00\u884c
        gateway_layout_1 = QHBoxLayout()
        self.gateway_1_1 = QSpinBox()
        self.gateway_1_1.setRange(0, 255)
        self.gateway_1_1.setValue(0)
        self.gateway_1_2 = QSpinBox()
        self.gateway_1_2.setRange(0, 255)
        self.gateway_1_2.setValue(0)
        self.gateway_1_3 = QSpinBox()
        self.gateway_1_3.setRange(0, 255)
        self.gateway_1_3.setValue(0)
        self.gateway_1_4 = QSpinBox()
        self.gateway_1_4.setRange(0, 255)
        self.gateway_1_4.setValue(0)
        
        gateway_layout_1.addWidget(self.gateway_1_1)
        gateway_layout_1.addWidget(QLabel("."))
        gateway_layout_1.addWidget(self.gateway_1_2)
        gateway_layout_1.addWidget(QLabel("."))
        gateway_layout_1.addWidget(self.gateway_1_3)
        gateway_layout_1.addWidget(QLabel("."))
        gateway_layout_1.addWidget(self.gateway_1_4)
        gateway_layout_1.addStretch()
        
        comm_layout.addRow("\u7f51\u5173", gateway_layout_1)
        
        # DNS - \u7b2c\u4e8c\u884c
        dns_layout = QHBoxLayout()
        self.dns_1 = QSpinBox()
        self.dns_1.setRange(0, 255)
        self.dns_1.setValue(0)
        self.dns_2 = QSpinBox()
        self.dns_2.setRange(0, 255)
        self.dns_2.setValue(0)
        self.dns_3 = QSpinBox()
        self.dns_3.setRange(0, 255)
        self.dns_3.setValue(0)
        self.dns_4 = QSpinBox()
        self.dns_4.setRange(0, 255)
        self.dns_4.setValue(0)
        
        dns_layout.addWidget(self.dns_1)
        dns_layout.addWidget(QLabel("."))
        dns_layout.addWidget(self.dns_2)
        dns_layout.addWidget(QLabel("."))
        dns_layout.addWidget(self.dns_3)
        dns_layout.addWidget(QLabel("."))
        dns_layout.addWidget(self.dns_4)
        dns_layout.addStretch()
        
        comm_layout.addRow("DNS", dns_layout)
        
        # \u8d85\u65f6(\u79d2)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 999)
        self.timeout_spin.setValue(10)
        comm_layout.addRow("\u8d85\u65f6(\u79d2)", self.timeout_spin)
        
        # MAC\u5730\u5740
        self.mac_edit = QLineEdit("00:00:00:00:00:00")
        self.mac_edit.setReadOnly(True)
        comm_layout.addRow("MAC\u5730\u5740", self.mac_edit)
        
        # \u5e8f\u5217\u53f7
        self.serial_edit = QLineEdit()
        self.serial_edit.setReadOnly(True)
        comm_layout.addRow("\u5e8f\u5217\u53f7", self.serial_edit)
        
        layout.addWidget(comm_group)
    
    def _create_buttons(self, layout):
        """\u521b\u5efa\u6309\u94ae\u533a\u57df"""
        button_layout = QHBoxLayout()
        
        # \u63a5\u6536\u8bbe\u7f6e\u6309\u94ae
        self.receive_settings_btn = QPushButton("\u63a5\u6536\u8bbe\u7f6e")
        self.receive_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        # \u786e\u5b9a\u548c\u53d6\u6d88\u6309\u94ae
        self.confirm_btn = QPushButton("\u786e\u5b9a")
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
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
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addWidget(self.receive_settings_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.confirm_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # \u8fde\u63a5\u4fe1\u53f7
        self.receive_settings_btn.clicked.connect(self._receive_settings)
        self.confirm_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
    
    def _setup_defaults(self):
        """\u8bbe\u7f6e\u9ed8\u8ba4\u503c"""
        # \u9ed8\u8ba4IP\u5730\u5740
        self.address_edit.setText("192.168.2.136")
        
        # \u6839\u636e\u63a5\u53e3\u9009\u62e9\u542f\u7528/\u7981\u7528\u76f8\u5173\u5b57\u6bb5
        self.usb_radio.toggled.connect(self._on_interface_changed)
        self.lan_radio.toggled.connect(self._on_interface_changed)
        self._on_interface_changed()
    
    def _on_interface_changed(self):
        """\u63a5\u53e3\u9009\u62e9\u53d8\u5316\u65f6\u7684\u5904\u7406"""
        is_lan = self.lan_radio.isChecked()
        
        # LAN\u76f8\u5173\u5b57\u6bb5\u7684\u542f\u7528/\u7981\u7528
        self.address_edit.setEnabled(is_lan)
        self.dhcp_combo.setEnabled(is_lan)
        self.subnet_1.setEnabled(is_lan)
        self.subnet_2.setEnabled(is_lan)
        self.subnet_3.setEnabled(is_lan)
        self.subnet_4.setEnabled(is_lan)
        self.port_edit.setEnabled(is_lan)
        self.gateway_1_1.setEnabled(is_lan)
        self.gateway_1_2.setEnabled(is_lan)
        self.gateway_1_3.setEnabled(is_lan)
        self.gateway_1_4.setEnabled(is_lan)
        self.dns_1.setEnabled(is_lan)
        self.dns_2.setEnabled(is_lan)
        self.dns_3.setEnabled(is_lan)
        self.dns_4.setEnabled(is_lan)
    
    def _receive_settings(self):
        """\u63a5\u6536\u8bbe\u7f6e - \u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f"""
        from PySide6.QtWidgets import QMessageBox
        from app.core.singleton_manager import DeviceManagerSingleton
        
        if not self.lan_radio.isChecked():
            QMessageBox.warning(self, "\u9519\u8bef", "\u76ee\u524d\u4ec5\u652f\u6301LAN\u63a5\u53e3\u7684\u8bbe\u5907")
            return
        
        ip_address = self.address_edit.text().strip()
        if not ip_address:
            QMessageBox.warning(self, "\u9519\u8bef", "\u8bf7\u8f93\u5165IP\u5730\u5740")
            return
        
        port = int(self.port_edit.text() or "8802")
        
        # \u663e\u793a\u8fde\u63a5\u8fdb\u5ea6
        progress = QMessageBox(self)
        progress.setWindowTitle("\u63a5\u6536\u8bbe\u7f6e")
        progress.setText(f"\u6b63\u5728\u8fde\u63a5\u5230 {ip_address}:{port} \u5e76\u8bfb\u53d6\u8bbe\u5907\u4fe1\u606f...")
        progress.setStandardButtons(QMessageBox.StandardButton.Cancel)  # \u6dfb\u52a0\u53d6\u6d88\u6309\u94ae
        progress.show()
        
        try:
            device_manager = DeviceManagerSingleton.get_instance()
            
            # \u8fde\u63a5\u8bbe\u5907
            success = device_manager.connect_device(ip_address, port)
            if not success:
                raise Exception("\u65e0\u6cd5\u8fde\u63a5\u5230\u8bbe\u5907")
            
            # \u83b7\u53d6\u8bbe\u5907\u4fe1\u606f
            devices = device_manager.get_connected_devices()
            if not devices:
                raise Exception("\u6ca1\u6709\u627e\u5230\u5df2\u8fde\u63a5\u7684\u8bbe\u5907")
            
            device = list(devices.values())[0]
            
            # \u66f4\u65b0\u754c\u9762\u5b57\u6bb5
            self.model_combo.setCurrentText(device.model)
            self.serial_edit.setText(device.serial)
            
            # \u5c1d\u8bd5\u8bfb\u53d6\u72b6\u6001\u4fe1\u606f\uff08API\u6587\u6863\u4e2d\u6ca1\u6709\u76f4\u63a5\u7684MAC\u5730\u5740\u547d\u4ee4\uff09
            try:
                # \u8bfb\u53d6\u8bbe\u5907\u72b6\u6001
                status_response = device_manager.send_command(device.device_id, ":STATus?")
                if status_response and status_response.strip():
                    print(f"Device status: {status_response.strip()}")
            except:
                pass  # \u72b6\u6001\u8bfb\u53d6\u5931\u8d25\u4e0d\u5f71\u54cd\u6574\u4f53\u6d41\u7a0b
            
            progress.close()
            
            QMessageBox.information(
                self, "\u63a5\u6536\u8bbe\u7f6e\u6210\u529f",
                f"\u5df2\u6210\u529f\u4ece\u8bbe\u5907\u8bfb\u53d6\u4fe1\u606f\uff1a\n"
                f"\u8bbe\u5907\u578b\u53f7: {device.model}\n"
                f"\u5e8f\u5217\u53f7: {device.serial}\n"
                f"\u56fa\u4ef6\u7248\u672c: {device.firmware}\n"
                f"IP\u5730\u5740: {device.ip_address}\n"
                f"\u7aef\u53e3: {device.port}"
            )
            
        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self, "\u63a5\u6536\u8bbe\u7f6e\u5931\u8d25",
                f"\u65e0\u6cd5\u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f\uff1a\n{str(e)}\n\n"
                f"\u8bf7\u68c0\u67e5\uff1a\n"
                f"1. \u8bbe\u5907\u662f\u5426\u5df2\u5f00\u673a\u5e76\u8fde\u63a5\u5230\u7f51\u7edc\n"
                f"2. IP\u5730\u5740\u548c\u7aef\u53e3\u662f\u5426\u6b63\u786e\n"
                f"3. \u9632\u706b\u5899\u8bbe\u7f6e\u662f\u5426\u5141\u8bb8\u8fde\u63a5"
            )
    
    def get_device_info(self):
        """\u83b7\u53d6\u8bbe\u5907\u4fe1\u606f"""
        return {
            'no': self.no_edit.text(),
            'model': self.model_combo.currentText(),
            'comment': self.comment_edit.text(),
            'interface': 'LAN' if self.lan_radio.isChecked() else 'USB',
            'ip_address': self.address_edit.text(),
            'port': int(self.port_edit.text() or "8802"),
            'dhcp': self.dhcp_combo.currentText(),
            'subnet_mask': f"{self.subnet_1.value()}.{self.subnet_2.value()}.{self.subnet_3.value()}.{self.subnet_4.value()}",
            'gateway': f"{self.gateway_1_1.value()}.{self.gateway_1_2.value()}.{self.gateway_1_3.value()}.{self.gateway_1_4.value()}",
            'dns': f"{self.dns_1.value()}.{self.dns_2.value()}.{self.dns_3.value()}.{self.dns_4.value()}",
            'timeout': self.timeout_spin.value(),
            'mac_address': self.mac_edit.text(),
            'serial_number': self.serial_edit.text(),
        }
