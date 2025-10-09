# -*- coding: utf-8 -*-
"""Right sidebar panel for waveform display settings."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app import config


class WaveformSettingsPanel(QWidget):
    """Right sidebar for waveform display settings."""
    
    # Signals for settings changes
    scale_settings_changed = Signal(dict)  # Scale configuration changes
    time_scale_changed = Signal(str)       # Time scale changes
    background_changed = Signal(str)       # Background color changes
    
    def __init__(self, parent=None):
        """Initialize the waveform settings panel."""
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { background-color: #ffffff; border: none; }")
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #ffffff;")  # Ensure white background
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(10)
        
        # Add all settings groups to content
        self._create_display_settings_group(content_layout)
        self._create_scale_settings_group(content_layout)
        self._create_time_settings_group(content_layout)
        self._create_background_settings_group(content_layout)
        
        content_layout.addStretch()
        
        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def _create_display_settings_group(self, layout):
        """Create waveform display settings group."""
        group = QGroupBox("\u6ce2\u5f62\u663e\u793a\u8bbe\u7f6e")
        group_layout = QFormLayout(group)
        
        # Screen split
        self.screen_split_combo = QComboBox()
        self.screen_split_combo.addItems(["OFF", "2\u5206\u5272", "4\u5206\u5272", "8\u5206\u5272"])
        group_layout.addRow("\u753b\u9762\u5206\u5272:", self.screen_split_combo)
        
        # Time grid
        self.time_grid_combo = QComboBox()
        time_options = ["1s", "10ms", "50ms", "100ms", "200ms", "500ms", "1s", "2s", "5s", "10s", "20s", "30s", "1min", "2min", "5min", "10min", "20min", "30min", "1hour", "2hour", "5hour", "10hour", "12hour", "1day", "2day"]
        self.time_grid_combo.addItems(time_options)
        self.time_grid_combo.setCurrentText("1s")
        group_layout.addRow("\u65f6\u95f4/1\u683c:", self.time_grid_combo)
        
        # Grid display
        self.grid_display_combo = QComboBox()
        self.grid_display_combo.addItems(["\u7ec6\u7f51\u7ebf", "\u7c97\u7f51\u7ebf", "\u65e0\u7f51\u7ebf"])
        group_layout.addRow("\u7f51\u683c\u663e\u793a:", self.grid_display_combo)
        
        # CH record
        self.ch_record_combo = QComboBox()
        self.ch_record_combo.addItems(["\u901a\u9053\u53f7\u7801", "\u5355\u5143\u540d\u79f0", "\u6ce8\u91ca"])
        group_layout.addRow("CH\u8bb0\u5f55:", self.ch_record_combo)
        
        # Waveform background color
        self.bg_color_combo = QComboBox()
        self.bg_color_combo.addItems(["\u767d", "\u9ed1"])
        self.bg_color_combo.setCurrentText("\u9ed1")
        group_layout.addRow("\u6ce2\u5f62\u80cc\u666f\u989c\u8272:", self.bg_color_combo)
        
        # Scale display and configuration
        self.scale_display_combo = QComboBox()
        self.scale_display_combo.addItems(["ON", "OFF"])
        group_layout.addRow("\u91cf\u89c4\u663e\u793a:", self.scale_display_combo)
        
        self.scale_count_spin = QSpinBox()
        self.scale_count_spin.setRange(1, 8)
        self.scale_count_spin.setValue(2)
        group_layout.addRow("\u91cf\u89c4\u6570\u91cf:", self.scale_count_spin)
        
        # Add axis configuration button
        self.axis_config_btn = QPushButton("\u8f74\u914d\u7f6e...")
        self.axis_config_btn.setToolTip("\u914d\u7f6e\u6bcf\u4e2a\u8f74\u7684\u91cf\u7a0b\u548c\u901a\u9053\u5206\u914d")
        group_layout.addRow("", self.axis_config_btn)
        
        layout.addWidget(group)
    
    def _create_scale_settings_group(self, layout):
        """Create scale settings group."""
        group = QGroupBox("\u91cf\u89c4\u8bbe\u7f6e")
        group_layout = QVBoxLayout(group)
        
        # Scale selection buttons
        self.scale_buttons = []
        for i in range(8):
            btn = QPushButton(f"\u91cf\u89c4 {i+1}")
            btn.setCheckable(True)
            if i < 2:  # Enable first 2 scales by default
                btn.setChecked(True)
                btn.setStyleSheet("QPushButton:checked { background-color: #4a90e2; color: white; }")
            self.scale_buttons.append(btn)
            group_layout.addWidget(btn)
        
        layout.addWidget(group)
    
    def _create_time_settings_group(self, layout):
        """Create time settings group."""
        group = QGroupBox("\u65f6\u95f4\u8bbe\u7f6e")
        group_layout = QFormLayout(group)
        
        # Real-time display
        self.realtime_display_combo = QComboBox()
        self.realtime_display_combo.addItems(["ON", "OFF"])
        group_layout.addRow("\u5b9e\u65f6\u663e\u793a:", self.realtime_display_combo)
        
        # Display range  
        self.display_range_combo = QComboBox()
        self.display_range_combo.addItems(["\u663e\u793a\u8303\u56f4", "\u5168\u90e8", "\u6700\u8fd110\u5206\u949f"])
        group_layout.addRow("\u663e\u793a\u8303\u56f4:", self.display_range_combo)
        
        # Public settings button
        self.public_settings_btn = QPushButton("\u516c\u7528\u8bbe\u7f6e")
        group_layout.addRow("", self.public_settings_btn)
        
        # Time record
        self.time_record_combo = QComboBox()
        self.time_record_combo.addItems(["\u65f6\u95f4\u8bb0\u5f55", "\u76f8\u5bf9\u65f6\u95f4"])
        group_layout.addRow("\u65f6\u95f4\u8bb0\u5f55:", self.time_record_combo)
        
        # Display interval
        self.display_interval_combo = QComboBox()
        self.display_interval_combo.addItems(["\u663e\u793a\u95f4\u9694", "\u5b9e\u65f6", "1\u79d2", "10\u79d2"])
        group_layout.addRow("\u663e\u793a\u95f4\u9694:", self.display_interval_combo)
        
        layout.addWidget(group)
    
    def _create_background_settings_group(self, layout):
        """Create background settings group."""
        group = QGroupBox("\u663e\u793a\u8bbe\u7f6e")
        group_layout = QFormLayout(group)
        
        # Background color
        self.background_color_combo = QComboBox()
        self.background_color_combo.addItems(["\u9ed1\u8272", "\u767d\u8272"])
        group_layout.addRow("\u80cc\u666f\u989c\u8272:", self.background_color_combo)
        
        # Grid style
        self.grid_style_combo = QComboBox()
        self.grid_style_combo.addItems(["\u7ec6\u7ebf", "\u7c97\u7ebf", "\u65e0\u7f51\u683c"])
        group_layout.addRow("\u7f51\u683c\u98ce\u683c:", self.grid_style_combo)
        
        layout.addWidget(group)
    
    def _connect_signals(self):
        """Connect widget signals."""
        # Time scale changes
        self.time_grid_combo.currentTextChanged.connect(self._on_time_scale_changed)
        
        # Background changes
        self.bg_color_combo.currentTextChanged.connect(self._on_background_changed)
        self.background_color_combo.currentTextChanged.connect(self._on_background_changed)
        
        # Scale changes
        for i, btn in enumerate(self.scale_buttons):
            btn.toggled.connect(lambda checked, scale_id=i: self._on_scale_toggled(scale_id, checked))
        
        # Scale count changes
        self.scale_count_spin.valueChanged.connect(self._on_scale_count_changed)
        
        # Axis configuration
        self.axis_config_btn.clicked.connect(self._open_axis_config_dialog)
    
    def _on_time_scale_changed(self, time_scale: str):
        """Handle time scale changes."""
        self.time_scale_changed.emit(time_scale)
    
    def _on_background_changed(self, background: str):
        """Handle background changes."""
        # Convert Chinese to English for internal use
        bg_map = {"\u9ed1": "black", "\u767d": "white", "\u9ed1\u8272": "black", "\u767d\u8272": "white"}
        internal_bg = bg_map.get(background, "black")
        self.background_changed.emit(internal_bg)
    
    def _on_scale_toggled(self, scale_id: int, checked: bool):
        """Handle scale button toggle."""
        # Update button style
        btn = self.scale_buttons[scale_id]
        if checked:
            btn.setStyleSheet("QPushButton:checked { background-color: #4a90e2; color: white; }")
        else:
            btn.setStyleSheet("")
        
        # Emit scale settings change
        scale_settings = {
            "scale_id": scale_id,
            "enabled": checked,
            "active_scales": [i for i, b in enumerate(self.scale_buttons) if b.isChecked()]
        }
        self.scale_settings_changed.emit(scale_settings)
    
    def _on_scale_count_changed(self, count: int):
        """Handle scale count changes."""
        # Enable/disable scale buttons based on count
        for i, btn in enumerate(self.scale_buttons):
            if i < count:
                btn.setEnabled(True)
                if i < 2:  # Auto-enable first 2 scales
                    btn.setChecked(True)
            else:
                btn.setEnabled(False)
                btn.setChecked(False)
    
    def get_active_scales(self) -> list[int]:
        """Get list of active scale indices."""
        return [i for i, btn in enumerate(self.scale_buttons) if btn.isChecked()]
    
    def set_scale_config(self, scale_configs: dict):
        """Set scale configuration from external source."""
        # This will be called when settings are loaded from device
        for scale_id, config in scale_configs.items():
            if 0 <= scale_id < len(self.scale_buttons):
                self.scale_buttons[scale_id].setChecked(config.get("enabled", False))
                # TODO: Set scale range, units, etc.
    
    def _open_axis_config_dialog(self):
        """\u6253\u5f00\u8f74\u914d\u7f6e\u5bf9\u8bdd\u6846"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self, "\u8f74\u914d\u7f6e", 
            "\u8f74\u914d\u7f6e\u529f\u80fd\u6b63\u5728\u5f00\u53d1\u4e2d\uff0c\u656c\u8bf7\u671f\u5f85\uff01\n\n"
            "\u5c06\u652f\u6301\uff1a\n"
            "- \u4e3a\u6bcf\u4e2a\u8f74\u8bbe\u7f6e\u4e0d\u540c\u7684\u91cf\u7a0b\n"
            "- \u5c06\u901a\u9053\u5206\u914d\u5230\u4e0d\u540c\u7684\u8f74\n"
            "- \u8bbe\u7f6e\u8f74\u7684\u989c\u8272\u548c\u6807\u7b7e"
        )
