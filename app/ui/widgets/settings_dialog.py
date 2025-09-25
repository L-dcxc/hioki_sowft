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
        self.resize(950, 700)
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
        # TODO: Implement sending settings to device
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "\u63d0\u793a",
            "\u8bbe\u7f6e\u5df2\u53d1\u9001\u5230\u8bbe\u5907\uff01"
        )
        self.accept()
