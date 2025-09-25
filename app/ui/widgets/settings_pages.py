"""Settings pages for the settings dialog."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ConnectionSettingsPage(QWidget):
    """Connection settings page."""

    def __init__(self):
        """Initialize the connection settings page."""
        super().__init__()
        self._setup_ui()

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
        conn_button_layout.addWidget(self.manual_add_btn)
        conn_button_layout.addWidget(self.detail_btn)
        conn_button_layout.addWidget(self.delete_btn)
        conn_button_layout.addStretch()
        connect_layout.addLayout(conn_button_layout)

        # Connected devices table with sample data
        self.connected_table = QTableWidget(2, 4)
        self.connected_table.setHorizontalHeaderLabels([
            "\u8bbe\u5907\u540d\u79f0", "\u63a5\u53e3", "IP\u5730\u5740", "\u72b6\u6001"
        ])

        # Add sample data
        sample_data = [
            ["LR8450-01", "LAN", "192.168.2.154", "\u5df2\u8fde\u63a5"],
            ["LR8450-02", "USB", "USB0", "\u672a\u8fde\u63a5"]
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
        self.main_unit_combo.addItems(["LR8450-01", "LR8450-02"])
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


class UnitSettingsPage(QWidget):
    """Unit settings page."""

    def __init__(self):
        """Initialize the unit settings page."""
        super().__init__()
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

        # LR8450 icon/label
        device_label = QLabel("LR8450")
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


class MeasurementSettingsPage(QWidget):
    """Measurement settings page."""

    def __init__(self):
        """Initialize the measurement settings page."""
        super().__init__()
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


class ChannelSettingsPage(QWidget):
    """Channel settings page."""

    def __init__(self):
        """Initialize the channel settings page."""
        super().__init__()
        self._setup_ui()

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
        
        # Channel list table
        self.channel_table = QTableWidget(15, 10)
        self.channel_table.setHorizontalHeaderLabels([
            "\u901a\u9053", "\u6ce8\u91ca", "\u5355\u5143", "\u540d\u79f0", "\u8f93\u5165\u7c7b\u578b", "\u5355\u4f4d", "1", "2", "3", "4"
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

        for row, data in enumerate(channels_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.channel_table.setItem(row, col, item)
                
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
