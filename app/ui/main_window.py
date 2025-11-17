"""Main window implementation."""

from __future__ import annotations

import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QToolBar,
)

from app import config
from app.core.data_acquisition import DataAcquisition, RealTimeData
from app.core.device_manager import DeviceManager, ConnectionStatus
from app.core.file_parser import HIOKIFileParser, WaveformData
from app.core.singleton_manager import DeviceManagerSingleton
from app.ui.widgets.about_dialog import AboutDialog
from app.ui.widgets.control_toolbar import ControlToolbar
from app.ui.widgets.data_table import DataTable
from app.ui.widgets.settings_dialog import SettingsDialog
from app.ui.widgets.waveform_panel import WaveformPanel
from app.ui.widgets.waveform_settings_panel import WaveformSettingsPanel


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.file_parser = HIOKIFileParser()
        self.device_manager = DeviceManagerSingleton.get_instance()
        self.data_acquisition = DataAcquisition(self.device_manager)
        self.current_waveform_data: WaveformData | None = None
        self.is_acquiring = False
        
        # Setup device manager callbacks
        self.device_manager.add_status_callback(self._on_device_status_changed)
        self.device_manager.add_data_callback(self._on_device_data_received)
        
        # Connect data acquisition signals (thread-safe)
        self.data_acquisition.data_received.connect(self._on_real_time_data)
        self.data_acquisition.error_occurred.connect(self._on_acquisition_error)
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle(config.APP_NAME)
        self.setGeometry(100, 100, config.DEFAULT_WINDOW_WIDTH, config.DEFAULT_WINDOW_HEIGHT)

        # Create menu bar
        self._create_menu_bar()

        # Create toolbar
        self._create_toolbar()

        # Create central widget (waveform panel)
        self.waveform_panel = WaveformPanel()
        self.setCentralWidget(self.waveform_panel)

        # Create right dock (waveform settings)
        self._create_right_dock()
        
        # Create bottom dock (data table)
        self._create_bottom_dock()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("\u5c31\u7eea - \u7b49\u5f85\u8bbe\u5907\u8fde\u63a5")

    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("\u6587\u4ef6(F)")
        
        # �򿪲����ļ�(O)... Ctrl+O
        open_waveform_action = file_menu.addAction("\u6253\u5f00\u6ce2\u5f62\u6587\u4ef6(O)...")
        open_waveform_action.setShortcut("Ctrl+O")
        open_waveform_action.triggered.connect(self._open_waveform_file)
        
        # �������ļ�(O)... Ctrl+Shift+O
        open_settings_action = file_menu.addAction("\u6253\u5f00\u8bbe\u7f6e\u6587\u4ef6(O)...")
        open_settings_action.setShortcut("Ctrl+Shift+O")
        open_settings_action.triggered.connect(self._show_placeholder)
        
        # ���������ļ�(S)... Ctrl+Shift+S
        save_settings_action = file_menu.addAction("\u4fdd\u5b58\u8bbe\u7f6e\u6587\u4ef6(S)...")
        save_settings_action.setShortcut("Ctrl+Shift+S")
        save_settings_action.triggered.connect(self._show_placeholder)
        
        file_menu.addSeparator()
        
        # ��ר�ø�ʽ�����ļ�...
        file_menu.addAction("\u4ee5\u4e13\u7528\u683c\u5f0f\u4fdd\u5b58\u6587\u4ef6...", self._show_placeholder)
        
        # ��ͨ�ø�ʽ����ת���ļ�...
        file_menu.addAction("\u4ee5\u901a\u7528\u683c\u5f0f\u4fdd\u5b58\u8f6c\u6362\u6587\u4ef6...", self._show_placeholder)
        
        # �ϲ��ļ�����...
        file_menu.addAction("\u5408\u5e76\u6587\u4ef6\u5bfc\u51fa...", self._show_placeholder)
        
        file_menu.addSeparator()
        
        # ����������Excel...
        file_menu.addAction("\u5bfc\u51fa\u6570\u636e\u81f3Excel...", self._show_placeholder)
        
        # ������������...
        file_menu.addAction("\u4fdd\u6301\u6570\u636e\u94fe\u63a5...", self._show_placeholder)
        
        file_menu.addSeparator()
        
        # ���ⲿ��������Ĳ����ļ�...
        file_menu.addAction("\u6253\u5f00\u5916\u90e8\u6570\u636e\u8f7d\u5165\u7684\u6ce2\u5f62\u6587\u4ef6...", self._show_placeholder)
        
        # �����ⲿ��������Ĳ����ļ�
        file_menu.addAction("\u4fdd\u5b58\u5916\u90e8\u6570\u636e\u8f7d\u5165\u7684\u6ce2\u5f62\u6587\u4ef6", self._show_placeholder)
        
        file_menu.addSeparator()
        
        # ��ӡ(P)... Ctrl+P
        print_action = file_menu.addAction("\u6253\u5370(P)...")
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self._show_placeholder)
        
        file_menu.addSeparator()
        
        # ���ʹ�õĴ���
        file_menu.addAction("\u6700\u8fd1\u4f7f\u7528\u7684\u50a8\u5b58", self._show_placeholder)
        
        file_menu.addSeparator()
        
        # ���������ݳ�ʼ�� Ctrl+I with red exclamation icon
        initialize_action = file_menu.addAction("\u5c06\u6240\u6709\u6570\u636e\u521d\u59cb\u5316")
        initialize_action.setShortcut("Ctrl+I")
        initialize_action.triggered.connect(self._show_placeholder)
        
        file_menu.addSeparator()
        
        # �˳�(X) Alt+F4
        exit_action = file_menu.addAction("\u9000\u51fa(X)")
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(QApplication.quit)

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
        tools_menu.addSeparator()
        tools_menu.addAction("\u5feb\u901f\u8fde\u63a5\u8bbe\u5907", self._quick_connect_device)
        tools_menu.addAction("\u9009\u9879(&O)", self._show_placeholder)

        # Help menu
        help_menu = menubar.addMenu("\u5e2e\u52a9(&H)")
        help_menu.addAction("\u67e5\u770b\u5e2e\u52a9", self._show_placeholder)
        help_menu.addAction("\u5173\u4e8e", self._show_about)

    def _create_toolbar(self) -> None:
        """Create the toolbar."""
        self.control_toolbar = ControlToolbar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.control_toolbar)
        
        # Connect signals
        self.control_toolbar.settings_requested.connect(self._open_settings)
        self.control_toolbar.start_requested.connect(self._start_acquisition)
        self.control_toolbar.stop_requested.connect(self._stop_acquisition)
        self.control_toolbar.pause_requested.connect(self._pause_acquisition)

    def _create_bottom_dock(self) -> None:
        """Create the bottom dock widget."""
        self.data_dock = QDockWidget("\u6570\u636e\u4e0e\u65e5\u5fd7", self)
        self.data_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        
        # Set minimum height for data table to show more rows
        self.data_table = DataTable()
        self.data_table.setMinimumHeight(200)  # Ensure at least 200px height
        self.data_dock.setWidget(self.data_table)
        
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.data_dock)
        
        # Set initial dock size - allocate more space to data table
        self.resizeDocks([self.data_dock], [250], Qt.Orientation.Vertical)
    
    def _create_right_dock(self) -> None:
        """Create the right dock widget for waveform settings."""
        self.settings_dock = QDockWidget("\u6ce2\u5f62\u8bbe\u7f6e", self)
        self.settings_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | 
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        
        self.waveform_settings = WaveformSettingsPanel()
        self.settings_dock.setWidget(self.waveform_settings)
        
        # Connect waveform settings signals
        self.waveform_settings.scale_settings_changed.connect(self._on_scale_settings_changed)
        self.waveform_settings.time_scale_changed.connect(self._on_time_scale_changed)
        self.waveform_settings.background_changed.connect(self._on_background_changed)
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.settings_dock)
        
        # Set initial dock sizes for better proportion
        # Give more space to waveform (central) and data table (bottom)
        self.resizeDocks([self.settings_dock], [280], Qt.Orientation.Horizontal)

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
        # The settings dialog will automatically use the singleton device manager
        dialog.exec()
    
    def _open_waveform_file(self) -> None:
        """Open a waveform file."""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("\u6253\u5f00\u6ce2\u5f62\u6587\u4ef6")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        # Set file filters for device formats
        filters = [
            f"{config.DEVICE_MANUFACTURER} \u6587\u4ef6 (*.luw *.lus *.mem)",
            "LUW \u6ce2\u5f62\u6587\u4ef6 (*.luw)",
            "LUS \u8bbe\u7f6e\u6587\u4ef6 (*.lus)", 
            "MEM \u5185\u5b58\u6587\u4ef6 (*.mem)",
            "CSV \u6587\u672c\u6587\u4ef6 (*.csv)",
            "\u6240\u6709\u6587\u4ef6 (*.*)"
        ]
        file_dialog.setNameFilters(filters)
        
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self._load_waveform_file(file_paths[0])
    
    def _load_waveform_file(self, file_path: str) -> None:
        """Load and display a waveform file.
        
        Args:
            file_path: Path to the file to load
        """
        try:
            # Show loading message
            self.status_bar.showMessage(f"\u6b63\u5728\u52a0\u8f7d\u6587\u4ef6: {file_path}")
            
            # Parse the file
            waveform_data = self.file_parser.parse_file(file_path)
            self.current_waveform_data = waveform_data
            
            # Update waveform panel
            self.waveform_panel.display_waveform_data(waveform_data)
            
            # Update data table
            self.data_table.update_data(waveform_data)
            
            # Update status bar
            channel_count = len(waveform_data.channels)
            sample_count = waveform_data.sample_count
            duration = waveform_data.recording_duration
            
            status_msg = (f"\u6587\u4ef6\u5df2\u52a0\u8f7d: {channel_count}\u4e2a\u901a\u9053, "
                         f"{sample_count}\u4e2a\u91c7\u6837\u70b9, "
                         f"\u65f6\u957f: {duration:.1f}\u79d2")
            self.status_bar.showMessage(status_msg)
            
            # Update window title
            file_name = file_path.split('/')[-1].split('\\')[-1]  # Get filename only
            self.setWindowTitle(f"{config.APP_NAME} - {file_name}")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "\u9519\u8bef",
                f"\u65e0\u6cd5\u52a0\u8f7d\u6587\u4ef6\uff1a\n{str(e)}"
            )
            self.status_bar.showMessage("\u6587\u4ef6\u52a0\u8f7d\u5931\u8d25")
    
    def _show_about(self) -> None:
        """Show the about dialog."""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def _on_device_status_changed(self, device_id: str, status: ConnectionStatus) -> None:
        """Handle device status changes.
        
        Args:
            device_id: Device identifier
            status: New connection status
        """
        try:
            if status == ConnectionStatus.CONNECTED:
                self.status_bar.showMessage(f"\u8bbe\u5907\u5df2\u8fde\u63a5: {device_id}")
                self.data_table.add_log_entry(f"\u8bbe\u5907\u8fde\u63a5\u6210\u529f: {device_id}")
            elif status == ConnectionStatus.CONNECTING:
                self.status_bar.showMessage(f"\u6b63\u5728\u8fde\u63a5: {device_id}")
                self.data_table.add_log_entry(f"\u6b63\u5728\u8fde\u63a5\u8bbe\u5907: {device_id}")
            elif status == ConnectionStatus.DISCONNECTED:
                self.status_bar.showMessage(f"\u8bbe\u5907\u5df2\u65ad\u5f00: {device_id}")
                self.data_table.add_log_entry(f"\u8bbe\u5907\u65ad\u5f00\u8fde\u63a5: {device_id}")
            elif status == ConnectionStatus.ERROR:
                self.status_bar.showMessage(f"\u8fde\u63a5\u9519\u8bef: {device_id}")
                self.data_table.add_log_entry(f"\u8bbe\u5907\u8fde\u63a5\u9519\u8bef: {device_id}")
        except RuntimeError:
            # Qt对象已删除，忽略
            pass
    
    def _on_device_data_received(self, device_id: str, data: dict) -> None:
        """Handle received device data.
        
        Args:
            device_id: Device identifier
            data: Received data
        """
        # TODO: Process real-time data and update waveform display
        self.data_table.add_log_entry(f"\u6536\u5230\u6570\u636e: {device_id}")
    
    def _start_acquisition(self) -> None:
        """Start real-time data acquisition."""
        if self.is_acquiring:
            return
        
        devices = self.device_manager.get_connected_devices()
        if not devices:
            QMessageBox.warning(
                self,
                "\u8b66\u544a",
                "\u6ca1\u6709\u8fde\u63a5\u7684\u8bbe\u5907\u3002\u8bf7\u5148\u8fde\u63a5\u8bbe\u5907\u3002"
            )
            return
        
        # Start real-time acquisition
        success = self.data_acquisition.start_acquisition()
        
        if success:
            self.is_acquiring = True
            self.data_table.add_log_entry("\u5df2\u5f00\u59cb\u5b9e\u65f6\u6570\u636e\u91c7\u96c6")
            self.status_bar.showMessage("\u5b9e\u65f6\u6570\u636e\u91c7\u96c6\u8fdb\u884c\u4e2d")
            
            # Update toolbar button states
            self.control_toolbar.start_action.setEnabled(False)
            self.control_toolbar.stop_action.setEnabled(True)
        else:
            QMessageBox.critical(
                self,
                "\u9519\u8bef",
                "\u65e0\u6cd5\u5f00\u59cb\u6570\u636e\u91c7\u96c6\u3002\u8bf7\u68c0\u67e5\u8bbe\u5907\u8fde\u63a5\u3002"
            )
    
    def _stop_acquisition(self) -> None:
        """Stop real-time data acquisition."""
        if not self.is_acquiring:
            return
        
        # Stop real-time acquisition
        self.data_acquisition.stop_acquisition()
        self.is_acquiring = False
        
        self.data_table.add_log_entry("\u5df2\u505c\u6b62\u5b9e\u65f6\u6570\u636e\u91c7\u96c6")
        self.status_bar.showMessage("\u6570\u636e\u91c7\u96c6\u5df2\u505c\u6b62")
        
        # Update toolbar button states
        self.control_toolbar.start_action.setEnabled(True)
        self.control_toolbar.stop_action.setEnabled(False)
    
    def _pause_acquisition(self) -> None:
        """Pause data acquisition (placeholder for future implementation)."""
        QMessageBox.information(
            self,
            "\u63d0\u793a",
            "\u6682\u505c\u529f\u80fd\u5c06\u5728\u540e\u7eed\u7248\u672c\u4e2d\u5b9e\u73b0"
        )
    
    def _on_real_time_data(self, device_id: str, data: RealTimeData) -> None:
        """Handle real-time data from acquisition.
        
        Args:
            device_id: Device identifier
            data: Real-time data
        """
        try:
            # Update waveform panel with real-time data
            self.waveform_panel.update_real_time_data(data)
            
            # Update data table with latest values
            self._update_data_table_with_real_time(data)
            
            # Log data reception (less frequently to avoid spam)
            if hasattr(self, '_last_data_log_time'):
                if time.time() - self._last_data_log_time > 5.0:  # Log every 5 seconds
                    self.data_table.add_log_entry(f"\u6536\u5230\u5b9e\u65f6\u6570\u636e: {len(data.channel_data)} \u901a\u9053")
                    self._last_data_log_time = time.time()
            else:
                self._last_data_log_time = time.time()
                self.data_table.add_log_entry(f"\u5f00\u59cb\u63a5\u6536\u5b9e\u65f6\u6570\u636e: {len(data.channel_data)} \u901a\u9053")
            
        except Exception as e:
            print(f"Error processing real-time data: {e}")
    
    def _on_acquisition_error(self, device_id: str, error: str) -> None:
        """Handle acquisition errors.
        
        Args:
            device_id: Device identifier
            error: Error message
        """
        self.data_table.add_log_entry(f"\u91c7\u96c6\u9519\u8bef ({device_id}): {error}")
        self.status_bar.showMessage(f"\u91c7\u96c6\u9519\u8bef: {error}")
    
    def _update_data_table_with_real_time(self, data: RealTimeData) -> None:
        """Update data table with real-time values.
        
        Args:
            data: Real-time data
        """
        # For now, just log the latest values
        # TODO: Implement actual data table update with real-time values
        pass
    
    def closeEvent(self, event) -> None:
        """Handle application close event."""
        # Stop acquisition if running
        if self.is_acquiring:
            self.data_acquisition.stop_acquisition()
        
        # Cleanup device connections
        self.device_manager.cleanup()
        event.accept()
    
    def _quick_connect_device(self) -> None:
        """Quick connect to device using known IP."""
        device_ip = "192.168.2.136"  # Your device IP
        device_port = 8802  # 使用SCPI控制端口
        
        self.status_bar.showMessage(f"\u6b63\u5728\u8fde\u63a5\u8bbe\u5907: {device_ip}:{device_port}...")
        self.data_table.add_log_entry(f"\u5c1d\u8bd5\u8fde\u63a5\u8bbe\u5907: {device_ip}:{device_port}")
        
        success = self.device_manager.connect_device(device_ip, device_port)
        
        if success:
            self.status_bar.showMessage(f"\u8bbe\u5907\u8fde\u63a5\u6210\u529f: {device_ip}")
            self.data_table.add_log_entry(f"\u8bbe\u5907\u8fde\u63a5\u6210\u529f: {device_ip}")
            
            # Show device info
            devices = self.device_manager.get_connected_devices()
            device_id = f"{device_ip}:8802"
            if device_id in devices:
                device = devices[device_id]
                self.data_table.add_log_entry(
                    f"\u8bbe\u5907\u4fe1\u606f: {device.manufacturer} {device.model} "
                    f"(S/N: {device.serial}, FW: {device.firmware})"
                )
        else:
            self.status_bar.showMessage(f"\u8bbe\u5907\u8fde\u63a5\u5931\u8d25: {device_ip}")
            self.data_table.add_log_entry(f"\u8bbe\u5907\u8fde\u63a5\u5931\u8d25: {device_ip}")
            
            QMessageBox.warning(
                self,
                "\u8fde\u63a5\u5931\u8d25",
                f"\u65e0\u6cd5\u8fde\u63a5\u5230\u8bbe\u5907 {device_ip}\n\n"
                "\u8bf7\u68c0\u67e5\uff1a\n"
                "1. \u8bbe\u5907\u7535\u6e90\u662f\u5426\u5f00\u542f\n"
                "2. \u7f51\u7edc\u8fde\u63a5\u662f\u5426\u6b63\u5e38\n"
                "3. IP\u5730\u5740\u662f\u5426\u6b63\u786e\n"
                "4. \u9632\u706b\u5899\u8bbe\u7f6e"
            )
    
    def _on_scale_settings_changed(self, settings: dict) -> None:
        """Handle scale settings changes."""
        # Update waveform panel with new scale settings
        active_scales = settings.get("active_scales", [])
        self.waveform_panel.update_scale_configuration(active_scales)
        self.data_table.add_log_entry(f"\u91cf\u89c4\u8bbe\u7f6e\u5df2\u66f4\u65b0: {len(active_scales)} \u4e2a\u6d3b\u8dc3\u91cf\u89c4")
    
    def _on_time_scale_changed(self, time_scale: str) -> None:
        """Handle time scale changes."""
        # Update waveform panel time scale
        self.waveform_panel.update_time_scale(time_scale)
        self.data_table.add_log_entry(f"\u65f6\u95f4\u523b\u5ea6\u5df2\u66f4\u65b0: {time_scale}")
    
    def _on_background_changed(self, background: str) -> None:
        """Handle background color changes."""
        # Update waveform panel background
        self.waveform_panel.update_background(background)
        self.data_table.add_log_entry(f"\u6ce2\u5f62\u80cc\u666f\u5df2\u66f4\u65b0: {background}")
