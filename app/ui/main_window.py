"""Main window implementation."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QToolBar,
)

from app.ui.widgets.control_toolbar import ControlToolbar
from app.ui.widgets.data_table import DataTable
from app.ui.widgets.settings_dialog import SettingsDialog
from app.ui.widgets.waveform_panel import WaveformPanel


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("LR8450 \u6570\u636e\u91c7\u96c6\u4e0e\u5206\u6790\u8f6f\u4ef6")
        self.setGeometry(100, 100, 1200, 800)

        # Create menu bar
        self._create_menu_bar()

        # Create toolbar
        self._create_toolbar()

        # Create central widget (waveform panel)
        self.waveform_panel = WaveformPanel()
        self.setCentralWidget(self.waveform_panel)

        # Create bottom dock (data table)
        self._create_bottom_dock()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("\u5c31\u7eea")

    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("\u6587\u4ef6(&F)")
        
        file_menu.addAction("\u65b0\u5efa(&N)", self._show_placeholder)
        file_menu.addAction("\u6253\u5f00(&O)", self._show_placeholder)
        file_menu.addSeparator()
        file_menu.addAction("\u4fdd\u5b58(&S)", self._show_placeholder)
        file_menu.addAction("\u53e6\u5b58\u4e3a(&A)", self._show_placeholder)
        file_menu.addSeparator()
        file_menu.addAction("\u5bfc\u5165\u6570\u636e", self._show_placeholder)
        file_menu.addAction("\u5bfc\u51fa\u6570\u636e", self._show_placeholder)
        file_menu.addSeparator()
        file_menu.addAction("\u6253\u5370\u8bbe\u7f6e", self._show_placeholder)
        file_menu.addAction("\u6253\u5370\u9884\u89c8", self._show_placeholder)
        file_menu.addAction("\u6253\u5370", self._show_placeholder)
        file_menu.addSeparator()
        file_menu.addAction("\u6700\u8fd1\u6587\u4ef6", self._show_placeholder)
        file_menu.addSeparator()
        file_menu.addAction("\u9000\u51fa(&X)", QApplication.quit)

        # Edit menu
        edit_menu = menubar.addMenu("\u7f16\u8f91(&E)")
        edit_menu.addAction("\u64a4\u9500(&U)", self._show_placeholder)
        edit_menu.addAction("\u91cd\u505a(&R)", self._show_placeholder)
        edit_menu.addSeparator()
        edit_menu.addAction("\u526a\u5207(&T)", self._show_placeholder)
        edit_menu.addAction("\u590d\u5236(&C)", self._show_placeholder)
        edit_menu.addAction("\u7c98\u8d34(&P)", self._show_placeholder)

        # View menu
        view_menu = menubar.addMenu("\u67e5\u770b(&V)")
        view_menu.addAction("\u5de5\u5177\u680f", self._show_placeholder)
        view_menu.addAction("\u72b6\u6001\u680f", self._show_placeholder)
        view_menu.addSeparator()
        view_menu.addAction("\u653e\u5927", self._show_placeholder)
        view_menu.addAction("\u7f29\u5c0f", self._show_placeholder)
        view_menu.addAction("\u9002\u5408\u7a97\u53e3", self._show_placeholder)

        # Tools menu
        tools_menu = menubar.addMenu("\u5de5\u5177(&T)")
        tools_menu.addAction("\u8bbe\u7f6e(&S)", self._open_settings)
        tools_menu.addAction("\u9009\u9879(&O)", self._show_placeholder)

        # Help menu
        help_menu = menubar.addMenu("\u5e2e\u52a9(&H)")
        help_menu.addAction("\u67e5\u770b\u5e2e\u52a9", self._show_placeholder)
        help_menu.addAction("\u5173\u4e8e", self._show_placeholder)

    def _create_toolbar(self) -> None:
        """Create the toolbar."""
        self.control_toolbar = ControlToolbar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.control_toolbar)
        
        # Connect signals
        self.control_toolbar.settings_requested.connect(self._open_settings)

    def _create_bottom_dock(self) -> None:
        """Create the bottom dock widget."""
        self.data_dock = QDockWidget("\u6570\u636e\u4e0e\u65e5\u5fd7", self)
        self.data_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        
        self.data_table = DataTable()
        self.data_dock.setWidget(self.data_table)
        
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.data_dock)

    def _show_placeholder(self) -> None:
        """Show placeholder message for unimplemented features."""
        QMessageBox.information(
            self,
            "\u63d0\u793a",
            "\u8be5\u529f\u80fd\u5c1a\u672a\u5b9e\u73b0"
        )

    def _open_settings(self) -> None:
        """Open the settings dialog."""
        dialog = SettingsDialog(self)
        dialog.exec()
