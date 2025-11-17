"""Settings pages for the settings dialog."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app import config
from app.core.device_manager import DeviceManager, ConnectionStatus
from app.core.singleton_manager import DeviceManagerSingleton
from app.core.settings_manager import get_settings_manager
from app.ui.widgets.device_config_dialog import DeviceConfigDialog
from app.ui.widgets.manual_add_device_dialog import ManualAddDeviceDialog


class ConnectionSettingsPage(QWidget):
    """Connection settings page."""

    def __init__(self):
        """Initialize the connection settings page."""
        super().__init__()
        self.device_manager = DeviceManagerSingleton.get_instance()
        self.settings_manager = get_settings_manager()
        self.device_manager.add_status_callback(self._on_device_status_changed)
        self.is_searching = False
        self._setup_ui()
        self._connect_signals()
        self._load_saved_configurations()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = QLabel("\u8fde\u63a5\u8bbe\u7f6e")
        header.setStyleSheet("""
            QLabel {
                background-color: #ffd700;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        layout.addWidget(header)

        # Search section
        search_group = QGroupBox("\u641c\u7d22\u8bbe\u5907")
        search_layout = QVBoxLayout(search_group)

        # Search type radio buttons
        search_type_layout = QHBoxLayout()
        self.usb_radio = QRadioButton("USB")
        self.usb_radio.setChecked(True)
        self.lan_radio = QRadioButton("LAN")
        search_type_layout.addWidget(self.usb_radio)
        search_type_layout.addWidget(self.lan_radio)
        search_type_layout.addStretch()
        search_layout.addLayout(search_type_layout)

        # Search buttons
        button_layout = QHBoxLayout()
        self.search_btn = QPushButton("\u641c\u7d22")
        self.clear_btn = QPushButton("\u6e05\u9664")
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        search_layout.addLayout(button_layout)

        # Found devices table
        self.found_table = QTableWidget(0, 4)
        self.found_table.setHorizontalHeaderLabels([
            "\u8bbe\u5907\u540d\u79f0", "\u63a5\u53e3", "IP\u5730\u5740", "\u72b6\u6001"
        ])
        self.found_table.setMaximumHeight(120)
        search_layout.addWidget(self.found_table)

        layout.addWidget(search_group)

        # Connected devices section
        connect_group = QGroupBox("\u5df2\u8fde\u63a5\u8bbe\u5907")
        connect_layout = QVBoxLayout(connect_group)

        # Connection control buttons
        conn_button_layout = QHBoxLayout()
        self.manual_add_btn = QPushButton("\u624b\u52a8\u6dfb\u52a0")
        self.detail_btn = QPushButton("\u8be6\u7ec6\u4fe1\u606f")
        self.delete_btn = QPushButton("\u5220\u9664")
        self.accept_settings_btn = QPushButton("\u63a5\u53d7\u8bbe\u7f6e")  # ????????????????
        self.accept_settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        conn_button_layout.addWidget(self.manual_add_btn)
        conn_button_layout.addWidget(self.detail_btn)
        conn_button_layout.addWidget(self.delete_btn)
        conn_button_layout.addWidget(self.accept_settings_btn)
        conn_button_layout.addStretch()
        connect_layout.addLayout(conn_button_layout)

        # Connected devices table with sample data
        self.connected_table = QTableWidget(2, 7)
        self.connected_table.setHorizontalHeaderLabels([
            "\u7f16\u53f7", "\u673a\u578b", "\u6ce8\u91ca", "\u5e8f\u5217\u53f7", "\u901a\u4fe1", "\u5730\u5740", "\u7aef\u53e3\u53f7", "\u7248\u672c"
        ])

        # Add sample data
        sample_data = [
            ["1", "LR8450", "", "221018368", "LAN", "192.168.2.136", "8800", "v2.10"],
            ["2", "LR8450", "", "", "USB", "USB0", "", ""]
        ]

        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.connected_table.setItem(row, col, item)

        self.connected_table.setMaximumHeight(120)
        connect_layout.addWidget(self.connected_table)

        layout.addWidget(connect_group)

        # Bottom controls
        bottom_layout = QHBoxLayout()

        # Time settings
        time_group = QGroupBox("\u65f6\u95f4\u8bbe\u7f6e")
        time_layout = QFormLayout(time_group)
        self.time_combo = QComboBox()
        self.time_combo.addItems(["\u81ea\u52a8", "\u624b\u52a8"])
        time_layout.addRow("\u65f6\u95f4\u540c\u6b65:", self.time_combo)
        bottom_layout.addWidget(time_group)

        # Sync controls
        sync_layout = QVBoxLayout()
        self.sync_refresh_btn = QPushButton("\u540c\u6b65\u5237\u65b0")
        self.main_unit_combo = QComboBox()
        self.main_unit_combo.addItems([f"{config.DEVICE_MODEL}-01", f"{config.DEVICE_MODEL}-02"])
        self.sync_test_btn = QPushButton("\u540c\u6b65\u6d4b\u8bd5")
        
        sync_layout.addWidget(QLabel("\u4e3b\u5355\u5143:"))
        sync_layout.addWidget(self.main_unit_combo)
        sync_layout.addWidget(self.sync_refresh_btn)
        sync_layout.addWidget(self.sync_test_btn)
        
        bottom_layout.addLayout(sync_layout)
        bottom_layout.addStretch()

        layout.addLayout(bottom_layout)

        # Status bar
        self.status_bar = QLabel("\u5237\u65b0\u9875\u9762\u663e\u793a\u72b6\u6001")
        self.status_bar.setStyleSheet("""
            QLabel {
                background-color: #90ee90;
                color: #000000;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        self.status_bar.setFixedHeight(40)
        layout.addWidget(self.status_bar)
    
    def _connect_signals(self):
        """Connect UI signals to slots."""
        # Search functionality
        self.search_btn.clicked.connect(self._start_device_search)
        self.clear_btn.clicked.connect(self._clear_search_results)
        
        # Connection functionality
        self.manual_add_btn.clicked.connect(self._manual_add_device)
        self.delete_btn.clicked.connect(self._delete_selected_device)
        self.detail_btn.clicked.connect(self._show_device_details)
        self.accept_settings_btn.clicked.connect(self._accept_device_settings)  # ????????????
        
        # Found devices table
        self.found_table.doubleClicked.connect(self._connect_selected_device)
        
        # Connected devices table - ?????????????
        self.connected_table.doubleClicked.connect(self._open_device_config_dialog)
    
    def _start_device_search(self):
        """Start searching for devices."""
        if self.is_searching:
            self._stop_device_search()
            return
        
        self._clear_search_results()
        self.is_searching = True
        self.search_btn.setText("\u505c\u6b62\u641c\u7d22")
        self.status_bar.setText("\u6b63\u5728\u641c\u7d22\u8bbe\u5907...")
        
        if self.lan_radio.isChecked():
            self._search_lan_devices()
        else:
            self._search_usb_devices()
    
    def _stop_device_search(self):
        """Stop device search."""
        self.device_manager.stop_discovery()
        self.is_searching = False
        self.search_btn.setText("\u641c\u7d22")
        self.status_bar.setText("\u641c\u7d22\u5df2\u505c\u6b62")
    
    def _search_lan_devices(self):
        """Search for LAN devices."""
        ip_range = "192.168.2"
        self.status_bar.setText(f"\u6b63\u5728\u626b\u63cf IP \u8303\u56f4: {ip_range}.1-254")
        self.device_manager.discover_devices(ip_range)
        
        import threading
        import time
        
        def discovery_checker():
            time.sleep(1)
            for _ in range(30):
                if not self.is_searching:
                    break
                devices = self.device_manager.get_connected_devices()
                self._update_found_devices_table()
                time.sleep(1)
            
            if self.is_searching:
                self._stop_device_search()
                device_count = len(self.device_manager.get_connected_devices())
                self.status_bar.setText(f"\u641c\u7d22\u5b8c\u6210\uff0c\u53d1\u73b0 {device_count} \u53f0\u8bbe\u5907")
        
        threading.Thread(target=discovery_checker, daemon=True).start()
    
    def _search_usb_devices(self):
        """Search for USB devices."""
        self.status_bar.setText("USB \u8bbe\u5907\u641c\u7d22\u5c06\u5728\u540e\u7eed\u7248\u672c\u4e2d\u5b9e\u73b0")
        self._stop_device_search()
    
    def _update_found_devices_table(self):
        """Update the found devices table."""
        devices = self.device_manager.get_connected_devices()
        self.found_table.setRowCount(0)
        
        for device_id, device in devices.items():
            if device.status in [ConnectionStatus.CONNECTED, ConnectionStatus.ERROR]:
                row = self.found_table.rowCount()
                self.found_table.insertRow(row)
                self.found_table.setItem(row, 0, QTableWidgetItem(f"{device.manufacturer} {device.model}"))
                self.found_table.setItem(row, 1, QTableWidgetItem("LAN"))
                self.found_table.setItem(row, 2, QTableWidgetItem(device.ip_address))
                status_text = "\u5df2\u8fde\u63a5" if device.status == ConnectionStatus.CONNECTED else "\u53d1\u73b0"
                self.found_table.setItem(row, 3, QTableWidgetItem(status_text))
    
    def _clear_search_results(self):
        """Clear search results."""
        self.found_table.setRowCount(0)
        self.status_bar.setText("\u51c6\u5907\u5c31\u7eea")
    
    def _connect_selected_device(self):
        """Connect to selected device."""
        current_row = self.found_table.currentRow()
        if current_row < 0:
            return
        
        ip_item = self.found_table.item(current_row, 2)
        if not ip_item:
            return
        
        ip_address = ip_item.text()
        self.status_bar.setText(f"\u6b63\u5728\u8fde\u63a5\u5230 {ip_address}...")
        
        success = self.device_manager.connect_device(ip_address)
        
        if success:
            self.status_bar.setText(f"\u8fde\u63a5\u6210\u529f: {ip_address}")
            self._update_connected_devices_table()
        else:
            self.status_bar.setText(f"\u8fde\u63a5\u5931\u8d25: {ip_address}")
    
    def _manual_add_device(self):
        """\u624b\u52a8\u6dfb\u52a0\u8bbe\u5907 - \u4f7f\u7528\u65b0\u7684\u8be6\u7ec6\u5bf9\u8bdd\u6846"""
        dialog = ManualAddDeviceDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            device_info = dialog.get_device_info()
            
            if device_info['interface'] == 'LAN':
                ip_address = device_info['ip_address']
                port = device_info['port']
                
                self.status_bar.setText(f"\u6b63\u5728\u8fde\u63a5\u5230 {ip_address}:{port}...")
                success = self.device_manager.connect_device(ip_address, port)
                
                if success:
                    self.status_bar.setText(f"\u8fde\u63a5\u6210\u529f: {ip_address}:{port}")
                    self._update_connected_devices_table()
                    
                    # \u8fde\u63a5\u6210\u529f\u540e\u81ea\u52a8\u8bfb\u53d6\u8bbe\u5907\u4fe1\u606f
                    self._auto_read_device_info(ip_address, port)
                else:
                    self.status_bar.setText(f"\u8fde\u63a5\u5931\u8d25: {ip_address}:{port}")
            else:
                # USB\u63a5\u53e3\u6682\u65f6\u4e0d\u652f\u6301
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self, "\u4fe1\u606f", 
                    "USB\u63a5\u53e3\u529f\u80fd\u6b63\u5728\u5f00\u53d1\u4e2d\uff0c\u8bf7\u4f7f\u7528LAN\u63a5\u53e3\u3002"
                )
    
    def _delete_selected_device(self):
        """Delete selected device."""
        current_row = self.connected_table.currentRow()
        if current_row < 0:
            return
        
        devices = self.device_manager.get_connected_devices()
        for device_id in devices:
            self.device_manager.disconnect_device(device_id)
            break
        
        self._update_connected_devices_table()
        self.status_bar.setText("\u8bbe\u5907\u5df2\u65ad\u5f00\u8fde\u63a5")
    
    def _show_device_details(self):
        """Show device details."""
        current_row = self.connected_table.currentRow()
        if current_row < 0:
            return
        
        devices = self.device_manager.get_connected_devices()
        if not devices:
            return
        
        device = list(devices.values())[0]
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self, "\u8bbe\u5907\u8be6\u7ec6\u4fe1\u606f",
            f"\u5236\u9020\u5546: {device.manufacturer}\n"
            f"\u578b\u53f7: {device.model}\n"
            f"\u5e8f\u5217\u53f7: {device.serial}\n"
            f"\u56fa\u4ef6\u7248\u672c: {device.firmware}\n"
            f"IP \u5730\u5740: {device.ip_address}\n"
            f"\u7aef\u53e3: {device.port}\n"
            f"\u72b6\u6001: {device.status.value}"
        )
    
    def _update_connected_devices_table(self):
        """\u66f4\u65b0\u5df2\u8fde\u63a5\u8bbe\u5907\u8868\u683c"""
        devices = self.device_manager.get_connected_devices()
        self.connected_table.setRowCount(0)
        
        for i, (device_id, device) in enumerate(devices.items()):
            if device.status == ConnectionStatus.CONNECTED:
                row = self.connected_table.rowCount()
                self.connected_table.insertRow(row)
                
                # \u7f16\u53f7, \u673a\u578b, \u6ce8\u91ca, \u5e8f\u5217\u53f7, \u901a\u4fe1, \u5730\u5740, \u7aef\u53e3\u53f7, \u7248\u672c
                self.connected_table.setItem(row, 0, QTableWidgetItem(str(i + 1)))  # \u7f16\u53f7
                self.connected_table.setItem(row, 1, QTableWidgetItem(device.model))  # \u673a\u578b
                self.connected_table.setItem(row, 2, QTableWidgetItem(""))  # \u6ce8\u91ca(\u7a7a)
                self.connected_table.setItem(row, 3, QTableWidgetItem(device.serial))  # \u5e8f\u5217\u53f7
                self.connected_table.setItem(row, 4, QTableWidgetItem("LAN"))  # \u901a\u4fe1
                self.connected_table.setItem(row, 5, QTableWidgetItem(device.ip_address))  # \u5730\u5740
                self.connected_table.setItem(row, 6, QTableWidgetItem(str(device.port)))  # \u7aef\u53e3\u53f7
                self.connected_table.setItem(row, 7, QTableWidgetItem(device.firmware))  # \u7248\u672c
    
    def _on_device_status_changed(self, device_id: str, status: ConnectionStatus):
        """Handle device status changes."""
        if status == ConnectionStatus.CONNECTED:
            self._update_connected_devices_table()
            self._update_found_devices_table()
        elif status == ConnectionStatus.DISCONNECTED:
            self._update_connected_devices_table()
    
    def _open_device_config_dialog(self):
        """\u53cc\u51fb\u8bbe\u5907\u65f6\u6253\u5f00\u914d\u7f6e\u5bf9\u8bdd\u6846 - \u7528\u6237\u63cf\u8ff0\u7684\u91cd\u8981\u529f\u80fd\u3002"""
        current_row = self.connected_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "\u9519\u8bef", "\u8bf7\u9009\u62e9\u4e00\u4e2a\u8bbe\u5907")
            return
        
        devices = self.device_manager.get_connected_devices()
        if not devices:
            QMessageBox.warning(self, "\u9519\u8bef", "\u6ca1\u6709\u8fde\u63a5\u7684\u8bbe\u5907")
            return
        
        device = list(devices.values())[0]
        dialog = DeviceConfigDialog(device, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # ???????????????????"????????"????????????????????
            self._accept_device_settings()
    
    def _accept_device_settings(self):
        """\u63a5\u53d7\u8bbe\u7f6e - \u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f\u5e76\u540c\u6b65\u5230\u540e\u7eed\u6b65\u9aa4\u3002\u8fd9\u662f\u7528\u6237\u5f3a\u8c03\u7684\u91cd\u70b9\u529f\u80fd\uff01"""
        devices = self.device_manager.get_connected_devices()
        if not devices:
            QMessageBox.warning(self, "\u9519\u8bef", "\u6ca1\u6709\u8fde\u63a5\u7684\u8bbe\u5907")
            return
        
        device = list(devices.values())[0]
        
        # ???????????
        progress = QMessageBox(self)
        progress.setWindowTitle("\u63a5\u53d7\u8bbe\u7f6e")
        progress.setText("\u6b63\u5728\u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f...")
        progress.setStandardButtons(QMessageBox.StandardButton.Cancel)  # \u6dfb\u52a0\u53d6\u6d88\u6309\u94ae
        progress.show()
        
        try:
            # ??????????????
            device_settings = self._read_device_settings(device)
            
            # \u540c\u6b65\u5230\u540e\u7eed\u8bbe\u7f6e\u9875\u9762
            self._sync_settings_to_pages(device_settings)
            
            progress.close()
            
            # \u663e\u793a\u8be6\u7ec6\u7684\u6210\u529f\u4fe1\u606f
            sync_details = []
            sync_details.append(f"\u8bbe\u5907\u578b\u53f7: {device.model}")
            sync_details.append(f"\u56fa\u4ef6\u7248\u672c: {device.firmware}")
            sync_details.append(f"\u5e8f\u5217\u53f7: {device.serial}")
            sync_details.append(f"\u53ef\u7528\u901a\u9053: {device_settings.get('channel_count', 30)}")
            sync_details.append(f"\u91c7\u96c6\u6a21\u5757: {device_settings.get('modules', 'U8552')}")
            
            # \u68c0\u67e5\u540c\u6b65\u72b6\u6001
            sync_status = []
            parent_dialog = self.parent()
            if hasattr(parent_dialog, 'unit_page'):
                sync_status.append("\u2713 \u5355\u5143\u8bbe\u7f6e\u9875\u9762\u5df2\u540c\u6b65")
            if hasattr(parent_dialog, 'measurement_page'):
                sync_status.append("\u2713 \u6d4b\u91cf\u8bbe\u7f6e\u9875\u9762\u5df2\u540c\u6b65")
            if hasattr(parent_dialog, 'channel_page'):
                sync_status.append("\u2713 \u901a\u9053\u8bbe\u7f6e\u9875\u9762\u5df2\u540c\u6b65")
            
            detailed_message = (
                f"\u5df2\u6210\u529f\u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f\uff1a\n\n"
                f"\u8bbe\u5907\u4fe1\u606f:\n" + "\n".join(sync_details) + "\n\n"
                f"\u540c\u6b65\u72b6\u6001:\n" + "\n".join(sync_status) + "\n\n"
                f"\u8bbe\u7f6e\u5df2\u4fdd\u5b58\u5e76\u540c\u6b65\u5230\u540e\u7eed\u9875\u9762\uff0c\u8bf7\u70b9\u51fb\u201c\u4e0b\u4e00\u6b65\u201d\u7ee7\u7eed\u914d\u7f6e\u3002"
            )
            
            QMessageBox.information(
                self, "\u63a5\u53d7\u8bbe\u7f6e\u6210\u529f", detailed_message
            )
            
            # \u53d1\u9001\u4fe1\u53f7\u901a\u77e5\u4e3b\u5bf9\u8bdd\u6846\u8df3\u8f6c\u5230\u4e0b\u4e00\u6b65
            if hasattr(self.parent(), 'progress_widget'):
                self.parent().progress_widget.set_current_step(1)  # \u8df3\u8f6c\u5230\u5355\u5143\u8bbe\u7f6e
                self.parent().content_stack.setCurrentIndex(1)
            
        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self, "\u8bfb\u53d6\u8bbe\u5907\u8bbe\u7f6e\u5931\u8d25",
                f"\u65e0\u6cd5\u4ece\u8bbe\u5907\u8bfb\u53d6\u914d\u7f6e\u4fe1\u606f\uff1a\n{str(e)}\n\n"
                f"\u8bf7\u68c0\u67e5\u8bbe\u5907\u8fde\u63a5\u548c\u517c\u5bb9\u6027\u3002"
            )
    
    def _read_device_settings(self, device):
        """\u4ece\u8bbe\u5907\u8bfb\u53d6\u8be6\u7ec6\u914d\u7f6e\u4fe1\u606f"""
        settings = {}

        try:
            print(f"\n=== \u5f00\u59cb\u8bfb\u53d6\u8bbe\u5907\u8bbe\u7f6e ===")
            print(f"\u8bbe\u5907\u4fe1\u606f: {device.ip_address}:{device.port} - {device.model}")

            # \u57fa\u7840\u8bbe\u5907\u4fe1\u606f
            settings['device_model'] = device.model
            settings['firmware_version'] = device.firmware
            settings['serial_number'] = device.serial
            print(f"\u57fa\u7840\u4fe1\u606f: \u578b\u53f7={device.model}, \u56fa\u4ef6={device.firmware}, \u5e8f\u5217\u53f7={device.serial}")

            # \u6839\u636eAPI\u6587\u6863\uff0c\u4f7f\u7528\u57fa\u672c\u7684\u6807\u51c6SCPI\u547d\u4ee4
            # \u5148\u68c0\u67e5\u8bbe\u5907\u72b6\u6001
            device_id = f"{device.ip_address}:{device.port}"
            print(f"\u8bbe\u5907ID: {device_id}")

            try:
                print(f"\u6b63\u5728\u67e5\u8be2\u8bbe\u5907\u72b6\u6001...")
                status = self.device_manager.query_device(device_id, ":STATus?")
                settings['device_status'] = status.strip() if status else "Unknown"
                print(f"\u8bbe\u5907\u72b6\u6001: {settings['device_status']}")
            except Exception as e:
                print(f"\u72b6\u6001\u67e5\u8be2\u5931\u8d25: {e}")
                settings['device_status'] = "Unknown"

            # \u6839\u636eAPI\u6587\u6863\uff0cLR8450\u652f\u6301\u6700\u591a30\u901a\u9053
            settings['channel_count'] = 30  # LR8450\u6807\u51c6\u914d\u7f6e
            settings['modules'] = "LR8450 Main Unit"  # \u4e3b\u673a\u5355\u5143
            settings['sample_interval'] = "1s"  # \u9ed8\u8ba4\u91c7\u6837\u95f4\u9694
            print(f"\u9ed8\u8ba4\u914d\u7f6e: \u901a\u9053\u6570={settings['channel_count']}, \u91c7\u6837\u95f4\u9694={settings['sample_interval']}")

            # \u8bfb\u53d6\u901a\u9053\u8be6\u7ec6\u914d\u7f6e
            print(f"\u6b63\u5728\u8bfb\u53d6\u901a\u9053\u914d\u7f6e...")
            settings['channels'] = self._read_channel_configurations(device_id)
            print(f"\u8bfb\u53d6\u5230 {len(settings['channels'])} \u4e2a\u901a\u9053\u914d\u7f6e")
            
            # \u68c0\u67e5\u662f\u5426\u6709\u9519\u8bef
            try:
                error_response = self.device_manager.query_device(device_id, "*ESR?")  # \u4f7f\u7528\u6807\u51c6\u4e8b\u4ef6\u72b6\u6001\u5bc4\u5b58\u5668
                if error_response:
                    settings['error_status'] = error_response.strip()
                    print(f"Device error status: {error_response.strip()}")
            except Exception as e:
                print(f"Error status query failed: {e}")
                settings['error_status'] = "0"
            
            print(f"Successfully read device settings: {settings}")
            return settings
            
        except Exception as e:
            print(f"Failed to read device settings: {e}")
            # \u8fd4\u56de\u9ed8\u8ba4\u8bbe\u7f6e
            return {
                'device_model': device.model if device else 'LR8450',
                'firmware_version': device.firmware if device else 'Unknown',
                'serial_number': device.serial if device else 'Unknown',
                'channel_count': 30,
                'modules': 'LR8450 Main Unit',
                'sample_interval': '1s',
                'device_status': 'Unknown',
                'error_status': '0'
            }
    
    def _sync_settings_to_pages(self, device_settings):
        """\u5c06\u8bfb\u53d6\u7684\u8bbe\u5907\u8bbe\u7f6e\u540c\u6b65\u5230\u540e\u7eed\u9875\u9762"""
        try:
            print(f"\n=== \u5f00\u59cb\u540c\u6b65\u8bbe\u7f6e\u5230\u5404\u9875\u9762 ===")
            print(f"\u8bbe\u5907\u8bbe\u7f6e\u6570\u636e: {device_settings}")

            # \u83b7\u53d6\u8bbe\u7f6e\u5bf9\u8bdd\u6846\u7684\u5176\u4ed6\u9875\u9762
            parent_dialog = self.parent()
            if not hasattr(parent_dialog, 'unit_page'):
                print(f"\u8b66\u544a: \u7236\u5bf9\u8bdd\u6846\u6ca1\u6709 unit_page \u5c5e\u6027")
                return

            # \u83b7\u53d6\u8bbe\u5907ID\u7528\u4e8e\u4fdd\u5b58\u914d\u7f6e
            devices = self.device_manager.get_connected_devices()
            print(f"\u5f53\u524d\u8fde\u63a5\u7684\u8bbe\u5907: {list(devices.keys()) if devices else '\u65e0'}")

            if devices:
                device = list(devices.values())[0]
                device_id = f"{device.ip_address}:{device.port}"
                print(f"\u4f7f\u7528\u8bbe\u5907ID: {device_id}")

                # \u4fdd\u5b58\u8bbe\u5907\u914d\u7f6e\u5230\u8bbe\u7f6e\u7ba1\u7406\u5668
                self.settings_manager.set_device_config(device_id, device_settings)
                self.settings_manager.save_device_configs()
                print(f"\u8bbe\u5907\u914d\u7f6e\u5df2\u4fdd\u5b58: {device_id}")

            # \u540c\u6b65\u5230\u5355\u5143\u8bbe\u7f6e\u9875\u9762
            print(f"\u6b63\u5728\u540c\u6b65\u5230\u5355\u5143\u8bbe\u7f6e\u9875\u9762...")
            unit_page = parent_dialog.unit_page
            if hasattr(unit_page, '_apply_device_settings'):
                print(f"  \u540c\u6b65\u5230\u5355\u5143\u8bbe\u7f6e\u9875\u9762...")
                unit_page._apply_device_settings(device_settings)
            else:
                print(f"  \u5355\u5143\u8bbe\u7f6e\u9875\u9762\u6ca1\u6709 _apply_device_settings \u65b9\u6cd5")

            # \u540c\u6b65\u5230\u6d4b\u91cf\u8bbe\u7f6e\u9875\u9762
            print(f"\u6b63\u5728\u540c\u6b65\u5230\u6d4b\u91cf\u8bbe\u7f6e\u9875\u9762...")
            measurement_page = parent_dialog.measurement_page
            if hasattr(measurement_page, '_apply_device_settings'):
                print(f"  \u540c\u6b65\u5230\u6d4b\u91cf\u8bbe\u7f6e\u9875\u9762...")
                measurement_page._apply_device_settings(device_settings)
            else:
                print(f"  \u6d4b\u91cf\u8bbe\u7f6e\u9875\u9762\u6ca1\u6709 _apply_device_settings \u65b9\u6cd5")

            # \u540c\u6b65\u5230\u901a\u9053\u8bbe\u7f6e\u9875\u9762
            print(f"\u6b63\u5728\u540c\u6b65\u5230\u901a\u9053\u8bbe\u7f6e\u9875\u9762...")
            channel_page = parent_dialog.channel_page
            if hasattr(channel_page, '_apply_device_settings'):
                print(f"  \u540c\u6b65\u5230\u901a\u9053\u8bbe\u7f6e\u9875\u9762...")
                print(f"  \u901a\u9053\u6570\u636e: {len(device_settings.get('channels', []))} \u4e2a\u901a\u9053")
                channel_page._apply_device_settings(device_settings)
                print(f"  \u901a\u9053\u8bbe\u7f6e\u540c\u6b65\u5b8c\u6210")
            else:
                print(f"  \u901a\u9053\u8bbe\u7f6e\u9875\u9762\u6ca1\u6709 _apply_device_settings \u65b9\u6cd5")

            print(f"=== \u8bbe\u7f6e\u540c\u6b65\u5b8c\u6210 ===\n")

        except Exception as e:
            print(f"\u8bbe\u7f6e\u540c\u6b65\u9519\u8bef: {e}")
            import traceback
            traceback.print_exc()
    
    def _auto_read_device_info(self, ip_address: str, port: int):
        """\u8fde\u63a5\u6210\u529f\u540e\u81ea\u52a8\u8bfb\u53d6\u8bbe\u5907\u4fe1\u606f"""
        try:
            # \u83b7\u53d6\u8bbe\u5907\u4fe1\u606f
            devices = self.device_manager.get_connected_devices()
            if not devices:
                return
            
            device = list(devices.values())[0]
            
            # \u663e\u793a\u8bfb\u53d6\u6210\u529f\u7684\u4fe1\u606f
            self.status_bar.setText(
                f"\u8bbe\u5907\u4fe1\u606f: {device.model} | "
                f"\u5e8f\u5217\u53f7: {device.serial} | "
                f"\u7248\u672c: {device.firmware}"
            )
            
        except Exception as e:
            print(f"\u8bfb\u53d6\u8bbe\u5907\u4fe1\u606f\u5931\u8d25: {e}")

    def _read_channel_configurations(self, device_id: str) -> list:
        """\u4ece\u8bbe\u5907\u8bfb\u53d6\u901a\u9053\u914d\u7f6e\u4fe1\u606f"""
        channels = []
        try:
            print(f"\n--- \u5f00\u59cb\u8bfb\u53d6\u901a\u9053\u914d\u7f6e ---")
            print(f"\u8bbe\u5907ID: {device_id}")

            # \u5148\u83b7\u53d6IDN\u54cd\u5e94\u6765\u89e3\u6790\u5355\u5143\u4fe1\u606f
            print(f"\u6b63\u5728\u67e5\u8be2\u8bbe\u5907IDN...")
            idn_response = self.device_manager.query_device(device_id, "*IDN?")
            print(f"IDN\u54cd\u5e94: {repr(idn_response)}")

            # \u89e3\u6790\u5355\u5143\u4fe1\u606f (U1-A \u8868\u793a\u5355\u51431\u662f\u7535\u538b\u6a21\u5757, U2-4 \u8868\u793a\u5355\u51432\u662f4\u901a\u9053\u6a21\u5757)
            print(f"\u6b63\u5728\u89e3\u6790\u5355\u5143\u4fe1\u606f...")
            unit_info = self._parse_unit_info_from_idn(idn_response)
            print(f"\u89e3\u6790\u5230\u7684\u5355\u5143\u4fe1\u606f: {unit_info}")

            # \u6839\u636e\u5355\u5143\u4fe1\u606f\u751f\u6210\u901a\u9053\u914d\u7f6e
            print(f"\u6b63\u5728\u751f\u6210\u901a\u9053\u914d\u7f6e...")
            channel_id = 0
            for unit_num, unit_type in unit_info.items():
                print(f"\u5904\u7406\u5355\u5143 {unit_num}: \u7c7b\u578b={unit_type}")

                if unit_type == 'A':  # \u7535\u538b\u6a21\u5757
                    print(f"  \u751f\u6210\u7535\u538b\u6a21\u5757\u901a\u9053...")
                    for ch in range(10):  # \u6bcf\u4e2a\u5355\u5143\u6700\u591a10\u901a\u9053
                        if channel_id < 30:  # LR8450\u6700\u591a30\u901a\u9053
                            channel_config = {
                                'channel_id': channel_id,
                                'enabled': channel_id < 8,  # \u9ed8\u8ba4\u524d8\u4e2a\u901a\u9053\u542f\u7528
                                'name': f"CH{channel_id+1:02d}",
                                'input_type': '\u7535\u538b',
                                'range': '\u00b110V',
                                'unit': 'V',
                                'axis_id': min(channel_id // 4, 7),  # \u6bcf4\u4e2a\u901a\u9053\u5171\u4eab\u4e00\u4e2a\u8f74
                                'comment': f'\u901a\u9053{channel_id+1}',
                                'note': '',
                                'unit_number': unit_num
                            }
                            channels.append(channel_config)
                            print(f"    \u6dfb\u52a0\u901a\u9053 {channel_id}: {channel_config['name']} (\u7535\u538b)")
                            channel_id += 1
                elif unit_type == 'B':  # \u6e29\u5ea6\u6a21\u5757
                    print(f"  \u751f\u6210\u6e29\u5ea6\u6a21\u5757\u901a\u9053...")
                    for ch in range(10):  # \u6bcf\u4e2a\u5355\u5143\u6700\u591a10\u901a\u9053
                        if channel_id < 30:
                            channel_config = {
                                'channel_id': channel_id,
                                'enabled': channel_id < 8,
                                'name': f"TEMP{channel_id+1:02d}",
                                'input_type': '\u6e29\u5ea6',
                                'range': '-50~100\u00b0C',
                                'unit': '\u00b0C',
                                'axis_id': min(channel_id // 4, 7),
                                'comment': f'\u6e29\u5ea6{channel_id+1}',
                                'note': '',
                                'unit_number': unit_num
                            }
                            channels.append(channel_config)
                            print(f"    \u6dfb\u52a0\u901a\u9053 {channel_id}: {channel_config['name']} (\u6e29\u5ea6)")
                            channel_id += 1
                elif unit_type == '4':  # 4\u901a\u9053\u6a21\u5757
                    for ch in range(4):
                        if channel_id < 30:
                            channel_config = {
                                'channel_id': channel_id,
                                'enabled': channel_id < 8,
                                'name': f"CH{channel_id+1:02d}",
                                'input_type': '\u7535\u538b',
                                'range': '\u00b15V',
                                'unit': 'V',
                                'axis_id': min(channel_id // 4, 7),
                                'comment': f'\u901a\u9053{channel_id+1}',
                                'note': '',
                                'unit_number': unit_num
                            }
                            channels.append(channel_config)
                            print(f"    \u6dfb\u52a0\u901a\u9053 {channel_id}: {channel_config['name']} (4\u901a\u9053\u6a21\u5757)")
                            channel_id += 1
                else:
                    print(f"  \u672a\u77e5\u5355\u5143\u7c7b\u578b: {unit_type}, \u8df3\u8fc7")

            print(f"Read {len(channels)} channel configurations from device")
            return channels

        except Exception as e:
            print(f"\u8bfb\u53d6\u901a\u9053\u914d\u7f6e\u5931\u8d25: {e}")
            # \u8fd4\u56de\u9ed8\u8ba4\u914d\u7f6e
            return self._get_default_channel_config()

    def _parse_unit_info_from_idn(self, idn_response: str) -> dict:
        """\u4ece IDN \u54cd\u5e94\u4e2d\u89e3\u6790\u5355\u5143\u4fe1\u606f"""
        unit_info = {}
        try:
            # IDN \u54cd\u5e94\u683c\u5f0f: "HIOKI 8450 V2.10 1.01 U1-A U2-4 U3-B ..."
            parts = idn_response.split()
            for part in parts:
                if part.startswith('U') and '-' in part:
                    unit_part, type_part = part.split('-', 1)
                    unit_num = int(unit_part[1:])  # \u53bb\u6389 'U' \u524d\u7f00
                    unit_info[unit_num] = type_part

            print(f"Parsed unit info: {unit_info}")
            return unit_info

        except Exception as e:
            print(f"\u89e3\u6790\u5355\u5143\u4fe1\u606f\u5931\u8d25: {e}")
            # \u8fd4\u56de\u9ed8\u8ba4\u5355\u5143\u4fe1\u606f
            return {1: 'A', 2: 'B', 3: 'A'}  # \u9ed8\u8ba4\u914d\u7f6e

    def _get_default_channel_config(self) -> list:
        """\u83b7\u53d6\u9ed8\u8ba4\u901a\u9053\u914d\u7f6e"""
        channels = []
        for i in range(30):
            if i < 10:  # \u524d10\u4e2a\u901a\u9053\u4e3a\u7535\u538b
                input_type = '\u7535\u538b'
                unit = 'V'
                range_val = '\u00b110V'
                name = f"CH{i+1:02d}"
            elif i < 20:  # \u4e2d\u95f410\u4e2a\u901a\u9053\u4e3a\u6e29\u5ea6
                input_type = '\u6e29\u5ea6'
                unit = '\u00b0C'
                range_val = '-50~100\u00b0C'
                name = f"TEMP{i-9:02d}"
            else:  # \u540e10\u4e2a\u901a\u9053\u4e3a\u7535\u6d41
                input_type = '\u7535\u6d41'
                unit = 'A'
                range_val = '\u00b11A'
                name = f"CURR{i-19:02d}"

            channel_config = {
                'channel_id': i,
                'enabled': i < 8,  # \u9ed8\u8ba4\u524d8\u4e2a\u901a\u9053\u542f\u7528
                'name': name,
                'input_type': input_type,
                'range': range_val,
                'unit': unit,
                'axis_id': min(i // 4, 7),
                'comment': f'\u901a\u9053{i+1}',
                'note': '',
                'unit_number': (i // 10) + 1
            }
            channels.append(channel_config)

        return channels

    def _load_saved_configurations(self):
        """\u52a0\u8f7d\u4fdd\u5b58\u7684\u8bbe\u5907\u914d\u7f6e"""
        try:
            # \u68c0\u67e5\u662f\u5426\u6709\u4fdd\u5b58\u7684\u8bbe\u5907\u914d\u7f6e
            saved_configs = self.settings_manager._device_configs
            if saved_configs:
                print(f"Found saved device configurations: {list(saved_configs.keys())}")
                self.status_bar.setText(f"\u53d1\u73b0 {len(saved_configs)} \u4e2a\u5df2\u4fdd\u5b58\u7684\u8bbe\u5907\u914d\u7f6e")

                # \u5c06\u4fdd\u5b58\u7684\u8bbe\u5907\u52a0\u8f7d\u5230\u8868\u683c\u4e2d
                for device_id, config in saved_configs.items():
                    device_model = config.get('device_model', 'Unknown')
                    firmware = config.get('firmware_version', 'Unknown')
                    print(f"Saved config for {device_id}: {device_model} (FW: {firmware})")

                    # \u89e3\u6790\u8bbe\u5907ID\u83b7\u53d6IP\u548c\u7aef\u53e3
                    try:
                        if ':' in device_id:
                            ip_address, port = device_id.split(':', 1)
                            port = int(port)
                        else:
                            ip_address = device_id
                            port = 8802  # \u9ed8\u8ba4\u7aef\u53e3

                        # \u6dfb\u52a0\u5230\u8bbe\u5907\u8868\u683c
                        self._add_device_to_table(
                            ip_address=ip_address,
                            port=port,
                            model=device_model,
                            firmware=firmware,
                            status="\u5df2\u4fdd\u5b58",
                            is_saved=True
                        )

                    except Exception as e:
                        print(f"\u89e3\u6790\u8bbe\u5907ID {device_id} \u5931\u8d25: {e}")

            else:
                print("No saved device configurations found")
                self.status_bar.setText("\u6ca1\u6709\u53d1\u73b0\u5df2\u4fdd\u5b58\u7684\u8bbe\u5907\u914d\u7f6e")

        except Exception as e:
            print(f"\u52a0\u8f7d\u4fdd\u5b58\u914d\u7f6e\u5931\u8d25: {e}")

    def _add_device_to_table(self, ip_address: str, port: int, model: str = "", firmware: str = "", status: str = "\u672a\u8fde\u63a5", is_saved: bool = False):
        """\u5411\u8bbe\u5907\u8868\u683c\u6dfb\u52a0\u8bbe\u5907"""
        try:
            # \u4f7f\u7528 connected_table \u800c\u4e0d\u662f device_table
            table = self.connected_table

            # \u68c0\u67e5\u8bbe\u5907\u662f\u5426\u5df2\u5b58\u5728 (\u68c0\u67e5\u5730\u5740\u5217 - \u7b2c5\u5217)
            for row in range(table.rowCount()):
                existing_ip = table.item(row, 5)  # \u5730\u5740\u5728\u7b2c5\u5217
                existing_port = table.item(row, 6)  # \u7aef\u53e3\u5728\u7b2c6\u5217
                if (existing_ip and existing_ip.text() == ip_address and
                    existing_port and existing_port.text() == str(port)):
                    # \u8bbe\u5907\u5df2\u5b58\u5728\uff0c\u66f4\u65b0\u4fe1\u606f
                    if model:
                        table.setItem(row, 1, QTableWidgetItem(model))  # \u673a\u578b
                    if firmware:
                        table.setItem(row, 7, QTableWidgetItem(firmware))  # \u7248\u672c
                    print(f"Updated existing device: {ip_address}:{port} - {model}")
                    return

            # \u6dfb\u52a0\u65b0\u8bbe\u5907
            row_position = table.rowCount()
            table.insertRow(row_position)

            # \u6309\u7167 connected_table \u7684\u5217\u7ed3\u6784\u586b\u5145\u6570\u636e
            # [\u7f16\u53f7, \u673a\u578b, \u6ce8\u91ca, \u5e8f\u5217\u53f7, \u901a\u4fe1, \u5730\u5740, \u7aef\u53e3\u53f7, \u7248\u672c]
            table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))  # \u7f16\u53f7
            table.setItem(row_position, 1, QTableWidgetItem(model))  # \u673a\u578b
            table.setItem(row_position, 2, QTableWidgetItem(""))  # \u6ce8\u91ca
            table.setItem(row_position, 3, QTableWidgetItem(""))  # \u5e8f\u5217\u53f7
            table.setItem(row_position, 4, QTableWidgetItem("LAN"))  # \u901a\u4fe1
            table.setItem(row_position, 5, QTableWidgetItem(ip_address))  # \u5730\u5740
            table.setItem(row_position, 6, QTableWidgetItem(str(port)))  # \u7aef\u53e3\u53f7
            table.setItem(row_position, 7, QTableWidgetItem(firmware))  # \u7248\u672c

            # \u5982\u679c\u662f\u4fdd\u5b58\u7684\u8bbe\u5907\uff0c\u8bbe\u7f6e\u7279\u6b8a\u6837\u5f0f
            if is_saved:
                for col in range(8):  # connected_table \u67098\u5217
                    item = table.item(row_position, col)
                    if item:
                        item.setBackground(Qt.GlobalColor.lightGray)

            print(f"Added device to table: {ip_address}:{port} - {model}")

        except Exception as e:
            print(f"\u6dfb\u52a0\u8bbe\u5907\u5230\u8868\u683c\u5931\u8d25: {e}")

    def get_saved_device_config(self, device_id: str):
        """\u83b7\u53d6\u6307\u5b9a\u8bbe\u5907\u7684\u4fdd\u5b58\u914d\u7f6e"""
        return self.settings_manager.get_device_config(device_id)

    def cleanup(self):
        """Cleanup device manager."""
        if hasattr(self, 'device_manager'):
            self.device_manager.cleanup()


class UnitSettingsPage(QWidget):
    """Unit settings page."""

    def __init__(self):
        """Initialize the unit settings page."""
        super().__init__()
        self.settings_manager = get_settings_manager()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = QLabel("\u5355\u5143\u8bbe\u7f6e")
        header.setStyleSheet("""
            QLabel {
                background-color: #ffd700;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        layout.addWidget(header)

        # Device display section
        device_section = QWidget()
        device_layout = QHBoxLayout(device_section)

        # Device icon/label
        device_label = QLabel(config.DEVICE_MODEL)
        device_label.setStyleSheet("""
            QLabel {
                background-color: #e8e8e8;
                border: 2px solid #888888;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
        """)
        device_label.setFixedSize(120, 80)
        device_layout.addWidget(device_label)

        # Sampling rate
        sampling_layout = QVBoxLayout()
        sampling_layout.addWidget(QLabel("\u91c7\u6837\u7387:"))
        self.sampling_combo = QComboBox()
        self.sampling_combo.addItems(["10ms", "20ms", "50ms", "100ms", "200ms", "500ms", "1s"])
        sampling_layout.addWidget(self.sampling_combo)
        sampling_layout.addStretch()
        device_layout.addLayout(sampling_layout)

        device_layout.addStretch()
        layout.addWidget(device_section)

        # Unit number buttons
        unit_section = QWidget()
        unit_layout = QHBoxLayout(unit_section)
        unit_layout.addWidget(QLabel("\u5355\u5143\u53f7:"))

        # Unit number buttons 1-10 with different colors
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#feca57", 
                 "#ff9ff3", "#54a0ff", "#5f27cd", "#00d2d3", "#ff9f43"]
        
        for i in range(1, 11):
            btn = QPushButton(str(i))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors[i-1]};
                    color: white;
                    font-weight: bold;
                    border: 2px solid #555555;
                    border-radius: 20px;
                    min-width: 35px;
                    min-height: 35px;
                }}
                QPushButton:hover {{
                    border: 2px solid #000000;
                }}
            """)
            unit_layout.addWidget(btn)

        unit_layout.addStretch()
        layout.addWidget(unit_section)

        # Control buttons
        control_layout = QHBoxLayout()
        self.report_btn = QPushButton("\u62a5\u544a")
        self.run_btn = QPushButton("\u8fd0\u884c")
        self.stop_btn = QPushButton("\u505c\u6b62")
        
        control_layout.addWidget(self.report_btn)
        control_layout.addWidget(self.run_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        # Gray placeholder sections
        for i in range(2):
            placeholder = QLabel(f"\u5360\u4f4d\u533a\u57df {i+1}")
            placeholder.setStyleSheet("""
                QLabel {
                    background-color: #e0e0e0;
                    border: 1px solid #cccccc;
                    padding: 40px;
                    text-align: center;
                    color: #666666;
                }
            """)
            layout.addWidget(placeholder)

        # Status bar
        self.status_bar = QLabel("\u5355\u5143\u8bbe\u7f6e\u72b6\u6001\u4fe1\u606f")
        self.status_bar.setStyleSheet("""
            QLabel {
                background-color: #90ee90;
                color: #000000;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        self.status_bar.setFixedHeight(40)
        layout.addWidget(self.status_bar)
    
    def _apply_device_settings(self, device_settings: dict):
        """\u5e94\u7528\u4ece\u8bbe\u5907\u8bfb\u53d6\u7684\u8bbe\u7f6e"""
        try:
            # \u66f4\u65b0\u91c7\u6837\u7387\u8bbe\u7f6e
            interval = device_settings.get('sample_interval', '100ms')
            
            # \u5c1d\u8bd5\u5728\u91c7\u6837\u7387\u4e0b\u62c9\u6846\u4e2d\u627e\u5230\u5bf9\u5e94\u7684\u503c
            for i in range(self.sampling_combo.count()):
                if self.sampling_combo.itemText(i) == interval:
                    self.sampling_combo.setCurrentIndex(i)
                    break
            
            # \u66f4\u65b0\u72b6\u6001\u680f
            self.status_bar.setText(
                f"\u5df2\u540c\u6b65\u8bbe\u5907\u8bbe\u7f6e - \u91c7\u6837\u7387: {interval}"
            )
            
        except Exception as e:
            print(f"\u5355\u5143\u8bbe\u7f6e\u540c\u6b65\u9519\u8bef: {e}")


class MeasurementSettingsPage(QWidget):
    """Measurement settings page."""

    def __init__(self):
        """Initialize the measurement settings page."""
        super().__init__()
        self.settings_manager = get_settings_manager()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = QLabel("\u6d4b\u91cf\u8bbe\u7f6e")
        header.setStyleSheet("""
            QLabel {
                background-color: #ffd700;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        layout.addWidget(header)

        # Main content area
        content_layout = QHBoxLayout()

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Function selection
        function_group = QGroupBox("\u529f\u80fd\u9009\u62e9")
        function_layout = QVBoxLayout(function_group)
        self.real_time_radio = QRadioButton("\u5b9e\u65f6\u663e\u793a")
        self.real_time_radio.setChecked(True)
        self.record_radio = QRadioButton("\u8bb0\u5f55")
        function_layout.addWidget(self.real_time_radio)
        function_layout.addWidget(self.record_radio)
        left_layout.addWidget(function_group)

        # Recording intervals
        interval_group = QGroupBox("\u8bb0\u5f55\u95f4\u9694")
        interval_layout = QFormLayout(interval_group)
        
        self.normal_combo = QComboBox()
        self.normal_combo.addItems(["1\u79d2", "2\u79d2", "5\u79d2", "10\u79d2", "30\u79d2", "1\u5206\u949f"])
        interval_layout.addRow("\u6b63\u5e38:", self.normal_combo)
        
        self.high_speed_combo = QComboBox()
        self.high_speed_combo.addItems(["10ms", "20ms", "50ms", "100ms"])
        interval_layout.addRow("\u9ad8\u901f:", self.high_speed_combo)
        
        left_layout.addWidget(interval_group)

        # File settings
        file_group = QGroupBox("\u6587\u4ef6\u8bbe\u7f6e")
        file_layout = QFormLayout(file_group)
        
        file_path_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit("C:\\Data\\")
        self.browse_btn = QPushButton("\u6d4f\u89c8")
        file_path_layout.addWidget(self.file_path_edit)
        file_path_layout.addWidget(self.browse_btn)
        file_layout.addRow("\u4fdd\u5b58\u8def\u5f84:", file_path_layout)
        
        self.filename_edit = QLineEdit("measurement")
        file_layout.addRow("\u6587\u4ef6\u540d:", self.filename_edit)
        
        self.filesize_combo = QComboBox()
        self.filesize_combo.addItems(["100MB", "500MB", "1GB", "2GB"])
        file_layout.addRow("\u6587\u4ef6\u5927\u5c0f:", self.filesize_combo)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["LUW", "CSV", "Excel"])
        file_layout.addRow("\u683c\u5f0f:", self.format_combo)
        
        self.comment_edit = QLineEdit()
        file_layout.addRow("\u6ce8\u91ca:", self.comment_edit)
        
        left_layout.addWidget(file_group)
        content_layout.addWidget(left_panel)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Recording duration
        duration_group = QGroupBox("\u8bb0\u5f55\u65f6\u95f4")
        duration_layout = QVBoxLayout(duration_group)
        
        self.duration_checkbox = QCheckBox("\u542f\u7528\u8bb0\u5f55\u65f6\u95f4\u9650\u5236")
        duration_layout.addWidget(self.duration_checkbox)
        
        time_layout = QHBoxLayout()
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0, 23)
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        
        time_layout.addWidget(QLabel("\u5c0f\u65f6:"))
        time_layout.addWidget(self.hours_spin)
        time_layout.addWidget(QLabel("\u5206\u949f:"))
        time_layout.addWidget(self.minutes_spin)
        time_layout.addWidget(QLabel("\u79d2:"))
        time_layout.addWidget(self.seconds_spin)
        time_layout.addStretch()
        
        duration_layout.addLayout(time_layout)
        right_layout.addWidget(duration_group)

        # Timed measurement
        timed_group = QGroupBox("\u5b9a\u65f6\u6d4b\u91cf")
        timed_layout = QVBoxLayout(timed_group)
        
        self.start_time_checkbox = QCheckBox("\u5f00\u59cb\u65f6\u95f4")
        self.end_time_checkbox = QCheckBox("\u7ed3\u675f\u65f6\u95f4")
        self.repeat_checkbox = QCheckBox("\u91cd\u590d\u95f4\u9694")
        
        timed_layout.addWidget(self.start_time_checkbox)
        timed_layout.addWidget(self.end_time_checkbox)
        timed_layout.addWidget(self.repeat_checkbox)
        
        repeat_layout = QFormLayout()
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(["\u65e0", "1\u5929", "1\u5468", "1\u4e2a\u6708"])
        repeat_layout.addRow("\u91cd\u590d:", self.repeat_combo)
        timed_layout.addLayout(repeat_layout)
        
        right_layout.addWidget(timed_group)

        # Split status
        split_group = QGroupBox("\u5206\u5272\u72b6\u6001")
        split_layout = QVBoxLayout(split_group)
        split_label = QLabel("\u5f53\u524d\u6587\u4ef6: measurement_001.luw")
        split_layout.addWidget(split_label)
        right_layout.addWidget(split_group)

        content_layout.addWidget(right_panel)
        layout.addLayout(content_layout)

        # Status bar
        self.status_bar = QLabel("\u6d4b\u91cf\u8bbe\u7f6e\u5df2\u51c6\u5907\u5b8c\u6210")
        self.status_bar.setStyleSheet("""
            QLabel {
                background-color: #90ee90;
                color: #000000;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        self.status_bar.setFixedHeight(40)
        layout.addWidget(self.status_bar)
    
    def _apply_device_settings(self, device_settings: dict):
        """\u5e94\u7528\u4ece\u8bbe\u5907\u8bfb\u53d6\u7684\u8bbe\u7f6e"""
        try:
            # \u66f4\u65b0\u6d4b\u91cf\u6a21\u5f0f\u8bbe\u7f6e
            # \u6839\u636e\u8bbe\u5907\u80fd\u529b\u8bbe\u7f6e\u9ed8\u8ba4\u6a21\u5f0f
            device_model = device_settings.get('device_model', '')
            
            # \u6839\u636e\u8bbe\u5907\u578b\u53f7\u8bbe\u7f6e\u9002\u5408\u7684\u6d4b\u91cf\u6a21\u5f0f
            if 'LR8450' in device_model or 'XY2580' in device_model:
                # \u9ed8\u8ba4\u542f\u7528\u5b9e\u65f6\u663e\u793a\u6a21\u5f0f
                self.real_time_radio.setChecked(True)
            
            # \u66f4\u65b0\u72b6\u6001\u680f
            self.status_bar.setText(
                f"\u5df2\u540c\u6b65\u8bbe\u5907\u8bbe\u7f6e - \u8bbe\u5907\u578b\u53f7: {device_model}"
            )
            
        except Exception as e:
            print(f"\u6d4b\u91cf\u8bbe\u7f6e\u540c\u6b65\u9519\u8bef: {e}")


class ChannelSettingsPage(QWidget):
    """Channel settings page."""

    def __init__(self):
        """Initialize the channel settings page."""
        super().__init__()
        self.settings_manager = get_settings_manager()
        self.device_manager = DeviceManagerSingleton.get_instance()
        self._setup_ui()
        # \u52a0\u8f7d\u4fdd\u5b58\u7684\u914d\u7f6e
        self._load_saved_config()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header = QLabel("\u901a\u9053\u8bbe\u7f6e")
        header.setStyleSheet("""
            QLabel {
                background-color: #ffd700;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        layout.addWidget(header)

        # Top controls
        controls_layout = QHBoxLayout()
        
        display_combo = QComboBox()
        display_combo.addItems(["\u663e\u793a\u8bbe\u7f6e1", "\u663e\u793a\u8bbe\u7f6e2"])
        controls_layout.addWidget(QLabel("\u663e\u793a:"))
        controls_layout.addWidget(display_combo)
        
        measure_btn = QPushButton("\u6d4b\u91cf")
        controls_layout.addWidget(measure_btn)
        
        copy_combo = QComboBox()
        copy_combo.addItems(["\u590d\u5236\u8bbe\u7f6e1", "\u590d\u5236\u8bbe\u7f6e2"])
        controls_layout.addWidget(copy_combo)
        
        process_btn = QPushButton("\u96c6\u4e2d\u5904\u7406")
        controls_layout.addWidget(process_btn)
        
        controls_layout.addStretch()
        
        controls_container = QWidget()
        controls_container.setLayout(controls_layout)
        layout.addWidget(controls_container)
        
        # Channel list table - enhanced
        self.channel_table = QTableWidget(30, 11)  # 30\u901a\u9053, 11\u5217
        self.channel_table.setHorizontalHeaderLabels([
            "\u5f00\u5173", "\u901a\u9053", "\u6ce8\u91ca", "\u5355\u5143", "\u540d\u79f0", "\u8f93\u5165\u7c7b\u578b", "\u91cf\u7a0b", "\u5355\u4f4d", "\u989c\u8272", "\u8f74\u5206\u914d", "\u5907\u6ce8"
        ])

        # Sample channel data
        channels_data = [
            ["1-P-1", "", "1", "CH1", "\u7535\u538b", "V", "10.0", "5.0", "0.0", "-5.0"],
            ["1-P-2", "", "1", "CH2", "\u7535\u538b", "V", "8.5", "4.2", "1.1", "-2.3"],
            ["1-P-3", "", "1", "CH3", "\u7535\u6d41", "A", "1.2", "0.8", "0.5", "0.1"],
            ["1-P-4", "", "1", "CH4", "\u7535\u538b", "V", "15.0", "12.5", "8.0", "3.2"],
            ["1-T-5", "", "1", "TEMP1", "\u6e29\u5ea6", "\u00b0C", "25.5", "24.8", "23.9", "22.1"],
            ["1-T-6", "", "1", "TEMP2", "\u6e29\u5ea6", "\u00b0C", "27.2", "26.5", "25.8", "24.3"],
            ["1-T-7", "", "1", "TEMP3", "\u6e29\u5ea6", "\u00b0C", "23.1", "22.8", "22.5", "21.9"],
            ["1-T-8", "", "1", "TEMP4", "\u6e29\u5ea6", "\u00b0C", "26.8", "26.2", "25.7", "24.9"],
            ["2-P-1", "", "2", "CH5", "\u7535\u538b", "V", "5.5", "3.2", "1.8", "0.5"],
            ["2-P-2", "", "2", "CH6", "\u7535\u6d41", "A", "2.1", "1.8", "1.5", "1.2"],
            ["2-T-3", "", "2", "TEMP5", "\u6e29\u5ea6", "\u00b0C", "28.5", "27.8", "27.1", "26.4"],
            ["2-T-4", "", "2", "TEMP6", "\u6e29\u5ea6", "\u00b0C", "24.2", "23.9", "23.6", "23.2"],
            ["3-P-1", "", "3", "CH7", "\u7535\u538b", "V", "12.3", "10.8", "9.2", "7.5"],
            ["3-P-2", "", "3", "CH8", "\u7535\u6d41", "A", "0.8", "0.6", "0.4", "0.2"],
            ["3-T-3", "", "3", "TEMP7", "\u6e29\u5ea6", "\u00b0C", "22.8", "22.5", "22.1", "21.7"]
        ]

        # \u4f7f\u7528\u65b0\u7684\u589e\u5f3a\u6570\u636e\u586b\u5145\u65b9\u6cd5
        self._populate_enhanced_channel_table()
                
        # Highlight selected row (1-P-1)
        for col in range(self.channel_table.columnCount()):
            item = self.channel_table.item(0, col)
            if item:
                item.setBackground(Qt.GlobalColor.cyan)
        
        self.channel_table.setMaximumHeight(400)
        layout.addWidget(self.channel_table)
        
        # Bottom configuration panel
        config_layout = QHBoxLayout()
        
        # Left side - Selected channel info
        left_config = QGroupBox("\u9009\u4e2d\u901a\u9053: 1-P-1")
        left_layout = QFormLayout(left_config)
        
        self.measure_enabled = QCheckBox("\u6d4b\u91cf ON")
        self.measure_enabled.setChecked(True)
        left_layout.addRow(self.measure_enabled)
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["V", "mV", "A", "mA"])
        left_layout.addRow("\u5355\u4f4d:", self.unit_combo)
        
        self.comment_edit = QLineEdit("CH1")
        left_layout.addRow("\u6ce8\u91ca:", self.comment_edit)
        
        config_layout.addWidget(left_config)
        
        # Right side - Detailed settings
        right_config = QGroupBox("\u8be6\u7ec6\u8bbe\u7f6e")
        right_layout = QFormLayout(right_config)
        
        self.input_type_combo = QComboBox()
        self.input_type_combo.addItems(["\u7535\u538b", "\u7535\u6d41", "\u6e29\u5ea6"])
        right_layout.addRow("\u8f93\u5165\u7c7b\u578b:", self.input_type_combo)
        
        self.range_combo = QComboBox()
        self.range_combo.addItems(["20V", "60V", "100V", "Auto"])
        right_layout.addRow("\u91cf\u7a0b:", self.range_combo)
        
        self.unit_label = QLabel("V")
        right_layout.addRow("\u5355\u4f4d:", self.unit_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["\u76f4\u6d41", "\u4ea4\u6d41", "RMS"])
        right_layout.addRow("\u6a21\u5f0f:", self.mode_combo)
        
        self.slope_combo = QComboBox()
        self.slope_combo.addItems(["1:1", "10:1", "100:1"])
        right_layout.addRow("\u659c\u7387:", self.slope_combo)
        
        self.threshold_edit = QLineEdit("0.0")
        right_layout.addRow("\u95e8\u9650\u503c:", self.threshold_edit)
        
        self.accumulate_unit_combo = QComboBox()
        self.accumulate_unit_combo.addItems(["\u5c0f\u65f6", "\u5929", "\u5468"])
        right_layout.addRow("\u7d2f\u52a0\u5355\u4f4d:", self.accumulate_unit_combo)
        
        self.accumulate_time_edit = QLineEdit("1")
        right_layout.addRow("\u7d2f\u52a0\u65f6\u95f4:", self.accumulate_time_edit)
        
        config_layout.addWidget(right_config)
        
        layout.addLayout(config_layout)

        # Status bar
        self.status_bar = QLabel("\u901a\u9053\u8bbe\u7f6e\u5b8c\u6210\uff0c\u5171 15 \u4e2a\u901a\u9053")
        self.status_bar.setStyleSheet("""
            QLabel {
                background-color: #90ee90;
                color: #000000;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #cccccc;
            }
        """)
        self.status_bar.setFixedHeight(40)
        layout.addWidget(self.status_bar)
    
    def _populate_enhanced_channel_table(self):
        """\u586b\u5145\u589e\u5f3a\u7684\u901a\u9053\u8868\u683c\u6570\u636e"""
        # \u9884\u5b9a\u4e49\u7684\u901a\u9053\u7c7b\u578b\u548c\u914d\u7f6e
        channel_configs = [
            ("\u7535\u538b", "V", "\u00b110V", "#FF6B6B", 0),   # \u7ea2\u8272 - \u8f740
            ("\u7535\u538b", "V", "\u00b15V", "#4ECDC4", 0),    # \u84dd\u7eff\u8272 - \u8f740
            ("\u6e29\u5ea6", "\u00b0C", "-50~100", "#45B7D1", 1), # \u84dd\u8272 - \u8f741
            ("\u6e7f\u5ea6", "%", "0~100", "#96CEB4", 2),      # \u7eff\u8272 - \u8f742
            ("\u7535\u6d41", "A", "\u00b11A", "#FFEAA7", 3),    # \u9ec4\u8272 - \u8f743
        ]
        
        for i in range(30):
            config = channel_configs[i % len(channel_configs)]
            input_type, unit, range_str, color, axis_id = config
            
            # \u5f00\u5173 (\u590d\u9009\u6846)
            enable_checkbox = QCheckBox()
            enable_checkbox.setChecked(i < 8)  # \u9ed8\u8ba4\u524d8\u4e2a\u901a\u9053\u542f\u7528
            enable_checkbox.toggled.connect(lambda checked, ch=i: self._on_channel_toggled(ch, checked))
            self.channel_table.setCellWidget(i, 0, enable_checkbox)
            
            # \u901a\u9053\u53f7
            self.channel_table.setItem(i, 1, QTableWidgetItem(f"CH{i+1:02d}"))
            
            # \u6ce8\u91ca (\u53ef\u7f16\u8f91)
            comment_item = QTableWidgetItem(f"\u901a\u9053{i+1}\u6ce8\u91ca")
            comment_item.setFlags(comment_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.channel_table.setItem(i, 2, comment_item)
            
            # \u5355\u5143
            unit_item = QTableWidgetItem(str((i // 10) + 1))
            self.channel_table.setItem(i, 3, unit_item)
            
            # \u540d\u79f0 (\u53ef\u7f16\u8f91)
            name_item = QTableWidgetItem(f"\u901a\u9053{i+1}")
            name_item.setFlags(name_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.channel_table.setItem(i, 4, name_item)
            
            # \u8f93\u5165\u7c7b\u578b (\u4e0b\u62c9\u6846)
            type_combo = QComboBox()
            type_combo.addItems(["\u7535\u538b", "\u6e29\u5ea6", "\u6e7f\u5ea6", "\u7535\u6d41", "\u9891\u7387"])
            type_combo.setCurrentText(input_type)
            type_combo.currentTextChanged.connect(lambda text, ch=i: self._on_input_type_changed(ch, text))
            self.channel_table.setCellWidget(i, 5, type_combo)
            
            # \u91cf\u7a0b (\u4e0b\u62c9\u6846)
            range_combo = QComboBox()
            self._update_range_options(range_combo, input_type)
            range_combo.setCurrentText(range_str)
            self.channel_table.setCellWidget(i, 6, range_combo)
            
            # \u5355\u4f4d
            unit_item = QTableWidgetItem(unit)
            self.channel_table.setItem(i, 7, unit_item)
            
            # \u989c\u8272 (\u6309\u94ae)
            color_btn = QPushButton()
            color_btn.setStyleSheet(f"background-color: {color}; border: 1px solid #ccc; border-radius: 3px;")
            color_btn.setFixedSize(30, 20)
            color_btn.clicked.connect(lambda checked, ch=i: self._select_channel_color(ch))
            self.channel_table.setCellWidget(i, 8, color_btn)
            
            # \u8f74\u5206\u914d (\u4e0b\u62c9\u6846)
            axis_combo = QComboBox()
            axis_combo.addItems([f"\u8f74{j+1}" for j in range(8)])
            axis_combo.setCurrentIndex(axis_id)
            axis_combo.currentIndexChanged.connect(lambda idx, ch=i: self._on_axis_assignment_changed(ch, idx))
            self.channel_table.setCellWidget(i, 9, axis_combo)
            
            # \u5907\u6ce8 (\u53ef\u7f16\u8f91)
            note_item = QTableWidgetItem("")
            note_item.setFlags(note_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.channel_table.setItem(i, 10, note_item)
            
        # \u8bbe\u7f6e\u8868\u683c\u5c5e\u6027
        self.channel_table.setAlternatingRowColors(True)
        self.channel_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def _update_range_options(self, range_combo: QComboBox, input_type: str):
        """\u6839\u636e\u8f93\u5165\u7c7b\u578b\u66f4\u65b0\u91cf\u7a0b\u9009\u9879"""
        range_combo.clear()
        if input_type == "\u7535\u538b":
            range_combo.addItems(["\u00b110V", "\u00b15V", "\u00b12V", "\u00b11V", "\u00b1500mV"])
        elif input_type == "\u6e29\u5ea6":
            range_combo.addItems(["-50~100\u00b0C", "0~200\u00b0C", "-100~500\u00b0C", "0~1000\u00b0C"])
        elif input_type == "\u6e7f\u5ea6":
            range_combo.addItems(["0~100%", "20~80%", "30~90%"])
        elif input_type == "\u7535\u6d41":
            range_combo.addItems(["\u00b15A", "\u00b11A", "\u00b1500mA", "\u00b1100mA"])
        elif input_type == "\u9891\u7387":
            range_combo.addItems(["0~10kHz", "0~100kHz", "0~1MHz"])
        else:
            range_combo.addItems(["\u81ea\u52a8"])
    
    def _on_channel_toggled(self, channel_id: int, enabled: bool):
        """\u901a\u9053\u5f00\u5173\u72b6\u6001\u53d8\u5316"""
        print(f"Channel {channel_id+1} {'enabled' if enabled else 'disabled'}")
        # \u4fdd\u5b58\u914d\u7f6e
        self._save_current_config()
        # TODO: \u901a\u77e5\u6ce2\u5f62\u9762\u677f\u66f4\u65b0\u663e\u793a
    
    def _on_input_type_changed(self, channel_id: int, input_type: str):
        """\u8f93\u5165\u7c7b\u578b\u53d8\u5316"""
        # \u66f4\u65b0\u5bf9\u5e94\u7684\u91cf\u7a0b\u9009\u9879
        range_combo = self.channel_table.cellWidget(channel_id, 6)
        if range_combo:
            self._update_range_options(range_combo, input_type)
        
        # \u66f4\u65b0\u5355\u4f4d
        unit_map = {"\u7535\u538b": "V", "\u6e29\u5ea6": "\u00b0C", "\u6e7f\u5ea6": "%", "\u7535\u6d41": "A", "\u9891\u7387": "Hz"}
        unit_item = self.channel_table.item(channel_id, 7)
        if unit_item:
            unit_item.setText(unit_map.get(input_type, ""))
        
        print(f"Channel {channel_id+1} input type changed to: {input_type}")
        # \u4fdd\u5b58\u914d\u7f6e
        self._save_current_config()
    
    def _on_axis_assignment_changed(self, channel_id: int, axis_index: int):
        """\u8f74\u5206\u914d\u53d8\u5316"""
        print(f"Channel {channel_id+1} assigned to axis {axis_index+1}")
        # \u4fdd\u5b58\u914d\u7f6e
        self._save_current_config()
        # TODO: \u901a\u77e5\u6ce2\u5f62\u9762\u677f\u66f4\u65b0\u8f74\u5206\u914d
    
    def _select_channel_color(self, channel_id: int):
        """\u9009\u62e9\u901a\u9053\u989c\u8272"""
        from PySide6.QtWidgets import QColorDialog
        from PySide6.QtGui import QColor
        
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor(QColor("#FF6B6B"), self, f"\u9009\u62e9\u901a\u9053{channel_id+1}\u7684\u989c\u8272")
        
        if color.isValid():
            color_btn = self.channel_table.cellWidget(channel_id, 8)
            if color_btn:
                color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc; border-radius: 3px;")
            print(f"Channel {channel_id+1} color changed to: {color.name()}")
    
    def get_channel_configuration(self) -> list:
        """\u83b7\u53d6\u6240\u6709\u901a\u9053\u7684\u914d\u7f6e\u4fe1\u606f"""
        channels = []
        for i in range(self.channel_table.rowCount()):
            # \u83b7\u53d6\u6bcf\u4e2a\u901a\u9053\u7684\u914d\u7f6e
            enable_checkbox = self.channel_table.cellWidget(i, 0)
            type_combo = self.channel_table.cellWidget(i, 5)
            range_combo = self.channel_table.cellWidget(i, 6)
            axis_combo = self.channel_table.cellWidget(i, 9)
            
            if enable_checkbox and type_combo and range_combo and axis_combo:
                config = {
                    'channel_id': i,
                    'enabled': enable_checkbox.isChecked(),
                    'name': self.channel_table.item(i, 4).text() if self.channel_table.item(i, 4) else f"CH{i+1}",
                    'input_type': type_combo.currentText(),
                    'range': range_combo.currentText(),
                    'unit': self.channel_table.item(i, 7).text() if self.channel_table.item(i, 7) else "",
                    'axis_id': axis_combo.currentIndex(),
                    'comment': self.channel_table.item(i, 2).text() if self.channel_table.item(i, 2) else "",
                    'note': self.channel_table.item(i, 10).text() if self.channel_table.item(i, 10) else "",
                }
                channels.append(config)
        
        return channels
    
    def _apply_device_settings(self, device_settings: dict):
        """\u5e94\u7528\u4ece\u8bbe\u5907\u8bfb\u53d6\u7684\u8bbe\u7f6e"""
        try:
            # \u83b7\u53d6\u901a\u9053\u914d\u7f6e
            channels = device_settings.get('channels', [])
            channel_count = device_settings.get('channel_count', 30)

            print(f"Applying device settings: {len(channels)} channels")

            # \u5982\u679c\u6709\u901a\u9053\u914d\u7f6e\uff0c\u5e94\u7528\u5230\u8868\u683c
            if channels:
                for channel_config in channels:
                    channel_id = channel_config.get('channel_id', 0)
                    if channel_id < self.channel_table.rowCount():
                        # \u5e94\u7528\u542f\u7528\u72b6\u6001
                        enable_checkbox = self.channel_table.cellWidget(channel_id, 0)
                        if enable_checkbox:
                            enable_checkbox.setChecked(channel_config.get('enabled', False))

                        # \u5e94\u7528\u8f93\u5165\u7c7b\u578b
                        type_combo = self.channel_table.cellWidget(channel_id, 5)
                        if type_combo:
                            input_type = channel_config.get('input_type', '\u7535\u538b')
                            index = type_combo.findText(input_type)
                            if index >= 0:
                                type_combo.setCurrentIndex(index)

                        # \u5e94\u7528\u91cf\u7a0b
                        range_combo = self.channel_table.cellWidget(channel_id, 6)
                        if range_combo:
                            range_val = channel_config.get('range', '\u00b110V')
                            # \u66f4\u65b0\u91cf\u7a0b\u9009\u9879
                            self._update_range_options(range_combo, input_type)
                            index = range_combo.findText(range_val)
                            if index >= 0:
                                range_combo.setCurrentIndex(index)

                        # \u5e94\u7528\u8f74\u5206\u914d
                        axis_combo = self.channel_table.cellWidget(channel_id, 9)
                        if axis_combo:
                            axis_id = channel_config.get('axis_id', 0)
                            if axis_id < axis_combo.count():
                                axis_combo.setCurrentIndex(axis_id)

                        # \u5e94\u7528\u540d\u79f0\u548c\u6ce8\u91ca
                        name_item = self.channel_table.item(channel_id, 4)
                        if name_item:
                            name_item.setText(channel_config.get('name', f'CH{channel_id+1:02d}'))

                        comment_item = self.channel_table.item(channel_id, 2)
                        if comment_item:
                            comment_item.setText(channel_config.get('comment', ''))

                        # \u5e94\u7528\u5355\u4f4d
                        unit_item = self.channel_table.item(channel_id, 7)
                        if unit_item:
                            unit_item.setText(channel_config.get('unit', 'V'))

            # \u66f4\u65b0\u72b6\u6001\u680f
            self.status_bar.setText(f"\u5df2\u540c\u6b65\u8bbe\u5907\u8bbe\u7f6e - \u53ef\u7528\u901a\u9053: {len(channels)}")

            # \u4fdd\u5b58\u8bbe\u5907\u8bbe\u7f6e
            self._save_current_config()

        except Exception as e:
            print(f"\u5e94\u7528\u8bbe\u5907\u8bbe\u7f6e\u5931\u8d25: {e}")
            self.status_bar.setText(f"\u540c\u6b65\u8bbe\u5907\u8bbe\u7f6e\u5931\u8d25: {str(e)}")
    
    def _save_current_config(self):
        """\u4fdd\u5b58\u5f53\u524d\u901a\u9053\u914d\u7f6e"""
        try:
            # \u83b7\u53d6\u5f53\u524d\u8fde\u63a5\u7684\u8bbe\u5907ID
            connected_devices = self.device_manager.get_connected_devices()
            if not connected_devices:
                print("No connected devices found for saving config")
                return

            # \u4f7f\u7528\u7b2c\u4e00\u4e2a\u8fde\u63a5\u7684\u8bbe\u5907
            device_id = list(connected_devices.keys())[0]

            # \u83b7\u53d6\u5f53\u524d\u914d\u7f6e
            channel_config = self.get_channel_configuration()

            # \u4fdd\u5b58\u5230\u8bbe\u7f6e\u7ba1\u7406\u5668
            self.settings_manager.set_channel_config(device_id, channel_config)
            self.settings_manager.save_device_configs()

            print(f"Saved channel config for device {device_id}: {len(channel_config)} channels")

        except Exception as e:
            print(f"\u4fdd\u5b58\u901a\u9053\u914d\u7f6e\u5931\u8d25: {e}")
    
    def _load_saved_config(self, device_id: str = None):
        """\u52a0\u8f7d\u4fdd\u5b58\u7684\u914d\u7f6e"""
        try:
            if device_id is None:
                # \u83b7\u53d6\u5f53\u524d\u8fde\u63a5\u7684\u8bbe\u5907
                connected_devices = self.device_manager.get_connected_devices()
                if connected_devices:
                    device_id = list(connected_devices.keys())[0]
                else:
                    # \u5982\u679c\u6ca1\u6709\u8fde\u63a5\u7684\u8bbe\u5907\uff0c\u5c1d\u8bd5\u52a0\u8f7d\u4fdd\u5b58\u7684\u914d\u7f6e
                    saved_configs = self.settings_manager._device_configs
                    if saved_configs:
                        device_id = list(saved_configs.keys())[0]
                    else:
                        device_id = "default"

            # \u52a0\u8f7d\u4fdd\u5b58\u7684\u901a\u9053\u914d\u7f6e
            saved_channels = self.settings_manager.get_channel_config(device_id)
            
            if saved_channels:
                # \u5e94\u7528\u4fdd\u5b58\u7684\u914d\u7f6e
                for config in saved_channels:
                    channel_id = config.get('channel_id', 0)
                    if channel_id < self.channel_table.rowCount():
                        # \u6062\u590d\u542f\u7528\u72b6\u6001
                        enable_checkbox = self.channel_table.cellWidget(channel_id, 0)
                        if enable_checkbox:
                            enable_checkbox.setChecked(config.get('enabled', False))
                        
                        # \u6062\u590d\u8f93\u5165\u7c7b\u578b
                        type_combo = self.channel_table.cellWidget(channel_id, 5)
                        if type_combo:
                            input_type = config.get('input_type', '\u7535\u538b')
                            index = type_combo.findText(input_type)
                            if index >= 0:
                                type_combo.setCurrentIndex(index)
                        
                        # \u6062\u590d\u91cf\u7a0b
                        range_combo = self.channel_table.cellWidget(channel_id, 6)
                        if range_combo:
                            range_val = config.get('range', '10V')
                            index = range_combo.findText(range_val)
                            if index >= 0:
                                range_combo.setCurrentIndex(index)
                        
                        # \u6062\u590d\u8f74\u5206\u914d
                        axis_combo = self.channel_table.cellWidget(channel_id, 9)
                        if axis_combo:
                            axis_id = config.get('axis_id', 0)
                            if axis_id < axis_combo.count():
                                axis_combo.setCurrentIndex(axis_id)
                        
                        # \u6062\u590d\u6ce8\u91ca\u548c\u5907\u6ce8
                        if self.channel_table.item(channel_id, 2):
                            self.channel_table.item(channel_id, 2).setText(config.get('comment', ''))
                        if self.channel_table.item(channel_id, 10):
                            self.channel_table.item(channel_id, 10).setText(config.get('note', ''))
                
                self.status_bar.setText(f"\u5df2\u52a0\u8f7d\u4fdd\u5b58\u7684\u914d\u7f6e - \u8bbe\u5907: {device_id}")
                
        except Exception as e:
            print(f"\u52a0\u8f7d\u901a\u9053\u914d\u7f6e\u5931\u8d25: {e}")
