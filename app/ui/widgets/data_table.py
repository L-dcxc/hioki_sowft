"""Data table and log display widget."""

from __future__ import annotations

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
