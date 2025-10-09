"""Settings dialog implementation."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.widgets.settings_pages import (
    ChannelSettingsPage,
    ConnectionSettingsPage,
    MeasurementSettingsPage,
    UnitSettingsPage,
)


class ClickableLabel(QLabel):
    """A clickable label widget."""
    
    clicked = Signal()
    
    def mousePressEvent(self, event):
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class SettingsProgressWidget(QWidget):
    """Progress indicator for settings steps."""
    
    step_clicked = Signal(int)
    
    def __init__(self):
        """Initialize the progress widget."""
        super().__init__()
        self._setup_ui()
        self.current_step = 0
        
    def _setup_ui(self):
        """Set up the UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(30)
        
        self.steps = [
            "1. \u8fde\u63a5\u8bbe\u7f6e",
            "2. \u5355\u5143\u8bbe\u7f6e", 
            "3. \u6d4b\u91cf\u8bbe\u7f6e",
            "4. \u901a\u9053\u8bbe\u7f6e"
        ]
        
        self.step_labels = []
        for i, step in enumerate(self.steps):
            label = ClickableLabel(step)
            label.setStyleSheet("""
                QLabel {
                    color: #222222;
                    font-weight: normal;
                    padding: 8px 16px;
                    border: 2px solid #cccccc;
                    border-radius: 20px;
                    background-color: #f8f8f8;
                }
                QLabel:hover {
                    background-color: #e8e8e8;
                }
            """)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.clicked.connect(lambda step=i: self.step_clicked.emit(step))
            
            self.step_labels.append(label)
            layout.addWidget(label)
            
            # Add arrow between steps (except after last step)
            if i < len(self.steps) - 1:
                arrow = QLabel("\u2192")
                arrow.setStyleSheet("color: #cccccc; font-size: 16px; font-weight: bold;")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(arrow)
        
        layout.addStretch()
        
    def set_current_step(self, step: int):
        """Set the current active step."""
        self.current_step = step
        
        for i, label in enumerate(self.step_labels):
            if i == step:
                # Current step - blue (always clickable)
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-weight: bold;
                        padding: 8px 16px;
                        border: 2px solid #4a90e2;
                        border-radius: 20px;
                        background-color: #4a90e2;
                    }
                    QLabel:hover {
                        background-color: #357abd;
                    }
                """)
            elif i < step:
                # Completed step - green (always clickable)
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-weight: bold;
                        padding: 8px 16px;
                        border: 2px solid #28a745;
                        border-radius: 20px;
                        background-color: #28a745;
                    }
                    QLabel:hover {
                        background-color: #218838;
                    }
                """)
            else:
                # Future step - gray but still clickable
                label.setStyleSheet("""
                    QLabel {
                        color: #222222;
                        font-weight: normal;
                        padding: 8px 16px;
                        border: 2px solid #cccccc;
                        border-radius: 20px;
                        background-color: #f8f8f8;
                    }
                    QLabel:hover {
                        background-color: #d8d8d8;
                        border: 2px solid #4a90e2;
                    }
                """)


class SettingsDialog(QDialog):
    """Main settings dialog."""

    def __init__(self, parent=None):
        """Initialize the settings dialog."""
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("\u8bbe\u7f6e")
        self.resize(1100, 800)  # Increased size for better content visibility
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Progress indicator
        self.progress_widget = SettingsProgressWidget()
        self.progress_widget.step_clicked.connect(self._on_step_clicked)
        layout.addWidget(self.progress_widget)

        # Content area
        self.content_stack = QStackedWidget()
        
        # Create pages
        self.connection_page = ConnectionSettingsPage()
        self.unit_page = UnitSettingsPage()
        self.measurement_page = MeasurementSettingsPage()
        self.channel_page = ChannelSettingsPage()
        
        # Add pages to stack
        self.content_stack.addWidget(self.connection_page)
        self.content_stack.addWidget(self.unit_page)
        self.content_stack.addWidget(self.measurement_page)
        self.content_stack.addWidget(self.channel_page)
        
        layout.addWidget(self.content_stack)

        # Bottom buttons
        self._create_bottom_buttons(layout)

        # Set initial page
        self._on_step_clicked(0)

    def _create_bottom_buttons(self, layout):
        """Create bottom action buttons."""
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 10, 20, 20)
        
        button_layout.addStretch()
        
        self.prev_btn = QPushButton("\u4e0a\u4e00\u6b65")
        self.prev_btn.clicked.connect(self._prev_step)
        button_layout.addWidget(self.prev_btn)
        
        self.next_btn = QPushButton("\u4e0b\u4e00\u6b65")
        self.next_btn.clicked.connect(self._next_step)
        button_layout.addWidget(self.next_btn)
        
        self.send_btn = QPushButton("\u53d1\u9001\u8bbe\u7f6e\u5230\u8bbe\u5907")
        self.send_btn.clicked.connect(self._send_to_device)
        button_layout.addWidget(self.send_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("\u53d6\u6d88")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)

    def _on_step_clicked(self, step: int):
        """Handle step button click."""
        # Allow jumping to any step directly
        if 0 <= step <= 3:
            self.content_stack.setCurrentIndex(step)
            self.progress_widget.set_current_step(step)
            
            # Update button states
            self.prev_btn.setEnabled(step > 0)
            self.next_btn.setEnabled(step < 3)
            self.send_btn.setEnabled(step == 3)

    def _prev_step(self):
        """Go to previous step."""
        current = self.content_stack.currentIndex()
        if current > 0:
            self._on_step_clicked(current - 1)

    def _next_step(self):
        """Go to next step."""
        current = self.content_stack.currentIndex()
        if current < 3:
            self._on_step_clicked(current + 1)

    def _send_to_device(self):
        """Send settings to device."""
        from PySide6.QtWidgets import QMessageBox, QProgressDialog
        from app.core.singleton_manager import DeviceManagerSingleton

        try:
            device_manager = DeviceManagerSingleton.get_instance()
            connected_devices = device_manager.get_connected_devices()

            if not connected_devices:
                QMessageBox.warning(
                    self,
                    "\u9519\u8bef",
                    "\u6ca1\u6709\u8fde\u63a5\u7684\u8bbe\u5907\u3002\u8bf7\u5148\u8fde\u63a5\u8bbe\u5907\u3002"
                )
                return

            # \u663e\u793a\u8fdb\u5ea6\u5bf9\u8bdd\u6846
            progress = QProgressDialog("\u6b63\u5728\u53d1\u9001\u8bbe\u7f6e\u5230\u8bbe\u5907...", "\u53d6\u6d88", 0, 100, self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.show()

            device_id = list(connected_devices.keys())[0]
            success_count = 0
            total_commands = 0

            # \u83b7\u53d6\u901a\u9053\u914d\u7f6e
            channel_config = self.channel_page.get_channel_configuration()
            enabled_channels = [ch for ch in channel_config if ch.get('enabled', False)]

            progress.setValue(10)
            progress.setLabelText("\u6b63\u5728\u53d1\u9001\u901a\u9053\u914d\u7f6e...")

            # \u53d1\u9001\u901a\u9053\u914d\u7f6e\u547d\u4ee4
            for i, channel in enumerate(enabled_channels):
                if progress.wasCanceled():
                    break

                channel_id = channel.get('channel_id', 0)
                input_type = channel.get('input_type', '\u7535\u538b')
                range_val = channel.get('range', '\u00b110V')

                # \u6839\u636eLR8450 SCPI\u534f\u8bae\u53d1\u9001\u547d\u4ee4
                comment = channel.get('comment', '')
                enabled = channel.get('enabled', False)

                try:
                    # \u901a\u9053\u6807\u8bc6\u7b26\u683c\u5f0f: CH1_1, CH1_2, CH2_1, etc.
                    unit_num = (channel_id // 10) + 1  # \u5355\u5143\u53f7 (1-3)
                    ch_num = (channel_id % 10) + 1      # \u901a\u9053\u53f7 (1-10)
                    ch_identifier = f"CH{unit_num}_{ch_num}"

                    # 1. \u8bbe\u7f6e\u901a\u9053\u5b58\u50a8\u542f\u7528/\u7981\u7528
                    store_cmd = f":UNIT:STORe {ch_identifier},{'ON' if enabled else 'OFF'}"
                    response = device_manager.send_command(device_id, store_cmd, expect_response=False)
                    if response is not False:  # \u6210\u529f\u6216\u65e0\u54cd\u5e94\u90fd\u7b97\u6210\u529f
                        success_count += 1
                    total_commands += 1

                    # 2. \u8bbe\u7f6e\u901a\u9053\u91cf\u7a0b (\u4ec5\u5bf9\u542f\u7528\u7684\u901a\u9053)
                    if enabled:
                        # \u5c06\u91cf\u7a0b\u503c\u8f6c\u6362\u4e3aLR8450\u53ef\u8bc6\u522b\u7684\u683c\u5f0f
                        range_value = self._convert_range_to_lr8450_format(range_val, input_type)
                        if range_value:
                            range_cmd = f":UNIT:RANGe {ch_identifier},{range_value}"
                            response = device_manager.send_command(device_id, range_cmd, expect_response=False)
                            if response is not False:
                                success_count += 1
                            total_commands += 1

                    # 3. \u8bbe\u7f6e\u901a\u9053\u6ce8\u91ca (\u5982\u679c\u6709)
                    if comment and enabled:
                        comment_cmd = f":COMMent:CH {ch_identifier},\"{comment}\""
                        response = device_manager.send_command(device_id, comment_cmd, expect_response=False)
                        if response is not False:
                            success_count += 1
                        total_commands += 1

                except Exception as e:
                    print(f"\u53d1\u9001\u901a\u9053{channel_id+1}\u914d\u7f6e\u5931\u8d25: {e}")

                # \u66f4\u65b0\u8fdb\u5ea6
                progress.setValue(10 + int(80 * (i + 1) / len(enabled_channels)))

            progress.setValue(90)
            progress.setLabelText("\u6b63\u5728\u5b8c\u6210\u914d\u7f6e...")

            # LR8450\u4e0d\u9700\u8981\u7279\u6b8a\u7684\u4fdd\u5b58\u547d\u4ee4\uff0c\u8bbe\u7f6e\u547d\u4ee4\u6267\u884c\u540e\u4f1a\u81ea\u52a8\u4fdd\u5b58
            # \u4f7f\u7528\u9519\u8bef\u67e5\u8be2\u6765\u9a8c\u8bc1\u8bbe\u5907\u72b6\u6001
            try:
                # \u7b49\u5f85\u4e00\u4e0b\u8ba9\u8bbe\u5907\u5904\u7406\u5b8c\u6210
                import time
                time.sleep(0.5)

                # \u67e5\u8be2\u8bbe\u5907\u9519\u8bef\u72b6\u6001
                error_response = device_manager.send_command(device_id, ":ERRor?", expect_response=True)
                if error_response is not False:  # \u6709\u54cd\u5e94\u5c31\u7b97\u6210\u529f
                    success_count += 1
                    if error_response and error_response.strip() != "0":
                        print(f"\u8bbe\u5907\u62a5\u544a\u9519\u8bef: {error_response}")
                    else:
                        print(f"\u8bbe\u5907\u72b6\u6001\u6b63\u5e38: {error_response}")
                total_commands += 1
            except Exception as e:
                print(f"\u9519\u8bef\u67e5\u8be2\u5931\u8d25: {e}")

            progress.setValue(100)
            progress.close()

            # \u663e\u793a\u7ed3\u679c
            if success_count == total_commands and total_commands > 0:
                QMessageBox.information(
                    self,
                    "\u6210\u529f",
                    f"\u8bbe\u7f6e\u5df2\u6210\u529f\u53d1\u9001\u5230\u8bbe\u5907\uff01\n\n"
                    f"\u5df2\u914d\u7f6e\u901a\u9053: {len(enabled_channels)}\n"
                    f"\u6210\u529f\u547d\u4ee4: {success_count}/{total_commands}"
                )
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "\u90e8\u5206\u6210\u529f",
                    f"\u8bbe\u7f6e\u90e8\u5206\u53d1\u9001\u6210\u529f\u3002\n\n"
                    f"\u6210\u529f\u547d\u4ee4: {success_count}/{total_commands}\n"
                    f"\u8bf7\u68c0\u67e5\u8bbe\u5907\u8fde\u63a5\u548c\u517c\u5bb9\u6027\u3002"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "\u9519\u8bef",
                f"\u53d1\u9001\u8bbe\u7f6e\u5931\u8d25\uff1a\n{str(e)}"
            )

    def _convert_range_to_lr8450_format(self, range_val: str, input_type: str) -> str:
        """\u5c06\u91cf\u7a0b\u503c\u8f6c\u6362\u4e3aLR8450\u53ef\u8bc6\u522b\u7684\u683c\u5f0f"""
        try:
            # \u6839\u636e\u8f93\u5165\u7c7b\u578b\u548c\u91cf\u7a0b\u8fdb\u884c\u8f6c\u6362
            if input_type == '\u7535\u538b':  # \u7535\u538b
                # \u7535\u538b\u91cf\u7a0b\u6620\u5c04
                voltage_ranges = {
                    '\u00b110V': '10',
                    '\u00b15V': '5',
                    '\u00b12V': '2',
                    '\u00b11V': '1',
                    '\u00b1500mV': '0.5'
                }
                return voltage_ranges.get(range_val, '10')  # \u9ed8\u8ba4\u4e3a10V

            elif input_type == '\u6e29\u5ea6':  # \u6e29\u5ea6
                # \u6e29\u5ea6\u91cf\u7a0b\u6620\u5c04 (\u53ef\u80fd\u9700\u8981\u6839\u636e\u5b9e\u9645\u60c5\u51b5\u8c03\u6574)
                temp_ranges = {
                    '-50~100\u00b0C': '1',
                    '0~200\u00b0C': '2',
                    '-100~500\u00b0C': '3',
                    '0~1000\u00b0C': '4'
                }
                return temp_ranges.get(range_val, '1')  # \u9ed8\u8ba4\u4e3a\u91cf\u7a0b1

            elif input_type == '\u7535\u6d41':  # \u7535\u6d41
                # \u7535\u6d41\u91cf\u7a0b\u6620\u5c04
                current_ranges = {
                    '\u00b15A': '5',
                    '\u00b11A': '1',
                    '\u00b1500mA': '0.5',
                    '\u00b1100mA': '0.1'
                }
                return current_ranges.get(range_val, '1')  # \u9ed8\u8ba4\u4e3a1A

            elif input_type == '\u6e7f\u5ea6':  # \u6e7f\u5ea6
                # \u6e7f\u5ea6\u91cf\u7a0b\u6620\u5c04
                humidity_ranges = {
                    '0~100%': '1',
                    '20~80%': '2',
                    '30~90%': '3'
                }
                return humidity_ranges.get(range_val, '1')  # \u9ed8\u8ba4\u4e3a\u91cf\u7a0b1

            else:
                return '1'  # \u9ed8\u8ba4\u91cf\u7a0b

        except Exception as e:
            print(f"\u91cf\u7a0b\u8f6c\u6362\u5931\u8d25: {e}")
            return '1'  # \u9ed8\u8ba4\u91cf\u7a0b
