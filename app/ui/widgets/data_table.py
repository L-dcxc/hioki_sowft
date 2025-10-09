"""Data table and log display widget."""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QPlainTextEdit,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app import config

# Import here to avoid circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.file_parser import WaveformData


class DataTable(QWidget):
    """Combined data table and log display widget."""

    def __init__(self) -> None:
        """Initialize the data table widget."""
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Data table tab
        self.data_table = QTableWidget()
        self._setup_data_table()
        self.tab_widget.addTab(self.data_table, "\u6570\u636e")

        # Log tab
        self.log_text = QPlainTextEdit()
        self.log_text.setMaximumBlockCount(1000)  # Limit log entries
        self._setup_log()
        self.tab_widget.addTab(self.log_text, "\u65e5\u5fd7")

        layout.addWidget(self.tab_widget)

    def _setup_data_table(self) -> None:
        """Set up the data table."""
        # Set up columns
        headers = ["\u65f6\u95f4", "\u901a\u9053 1", "\u901a\u9053 2", "\u901a\u9053 3", "\u5355\u4f4d"]
        self.data_table.setColumnCount(len(headers))
        self.data_table.setHorizontalHeaderLabels(headers)

        # Add sample data
        sample_data = [
            ["00:00:01", "1.234", "2.345", "3.456", "V"],
            ["00:00:02", "1.235", "2.346", "3.457", "V"],
            ["00:00:03", "1.236", "2.347", "3.458", "V"],
            ["00:00:04", "1.237", "2.348", "3.459", "V"],
            ["00:00:05", "1.238", "2.349", "3.460", "V"],
        ]

        self.data_table.setRowCount(len(sample_data))
        for row, row_data in enumerate(sample_data):
            for col, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.data_table.setItem(row, col, item)

        # Adjust column widths
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _setup_log(self) -> None:
        """Set up the log display."""
        self.log_text.setReadOnly(True)
        self.log_text.appendPlainText("\u7cfb\u7edf\u521d\u59cb\u5316\u5b8c\u6210")
        self.log_text.appendPlainText("\u6b63\u5728\u7b49\u5f85\u8bbe\u5907\u8fde\u63a5...")
        self.log_text.appendPlainText("\u51c6\u5907\u5c31\u7eea\uff0c\u53ef\u4ee5\u5f00\u59cb\u6570\u636e\u91c7\u96c6")

    def add_log_entry(self, message: str) -> None:
        """Add a new log entry."""
        self.log_text.appendPlainText(message)
    
    def update_data(self, waveform_data: WaveformData) -> None:
        """Update the data table with waveform data.
        
        Args:
            waveform_data: Waveform data to display in table
        """
        if not waveform_data.channels:
            self.add_log_entry("\u65e0\u6570\u636e\u53ef\u663e\u793a")
            return
        
        # Clear existing table
        self.data_table.clear()
        
        # Prepare headers
        headers = ["\u65f6\u95f4 (s)"]
        for channel in waveform_data.channels:
            if channel.unit:
                header = f"{channel.name} ({channel.unit})"
            else:
                header = channel.name
            headers.append(header)
        
        self.data_table.setColumnCount(len(headers))
        self.data_table.setHorizontalHeaderLabels(headers)
        
        # Determine number of rows to display (limit to avoid performance issues)
        max_rows = config.MAX_TABLE_ROWS
        sample_count = waveform_data.sample_count
        
        if sample_count > max_rows:
            # Sample data points evenly
            indices = np.linspace(0, sample_count - 1, max_rows, dtype=int)
            display_count = max_rows
            self.add_log_entry(f"\u6570\u636e\u91cf\u8f83\u5927\uff0c\u4ec5\u663e\u793a {max_rows} \u4e2a\u91c7\u6837\u70b9")
        else:
            indices = np.arange(sample_count)
            display_count = sample_count
        
        self.data_table.setRowCount(display_count)
        
        # Calculate time array
        if waveform_data.channels and waveform_data.channels[0].sample_rate > 0:
            sample_rate = waveform_data.channels[0].sample_rate
            time_values = indices / sample_rate
        else:
            time_values = indices
        
        # Fill table data
        for row in range(display_count):
            # Time column
            time_item = QTableWidgetItem(f"{time_values[row]:.3f}")
            self.data_table.setItem(row, 0, time_item)
            
            # Channel data columns
            for col, channel in enumerate(waveform_data.channels, 1):
                if indices[row] < len(channel.data):
                    value = channel.data[indices[row]]
                    
                    # Format value based on channel type
                    if channel.channel_type == "logic":
                        value_str = "1" if value > 0.5 else "0"
                    elif channel.channel_type in ["analog", "wave_calc"]:
                        value_str = f"{value:.6f}"
                    else:
                        value_str = str(value)
                    
                    item = QTableWidgetItem(value_str)
                    self.data_table.setItem(row, col, item)
        
        # Adjust column widths
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Add log entry
        self.add_log_entry(f"\u6570\u636e\u8868\u5df2\u66f4\u65b0: {len(waveform_data.channels)}\u4e2a\u901a\u9053, {display_count}\u884c\u6570\u636e")
