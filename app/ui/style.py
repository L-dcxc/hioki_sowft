"""Application styling and theming."""

from __future__ import annotations


def get_stylesheet() -> str:
    """Get the application stylesheet."""
    return """
    /* Main application styling */
    QMainWindow {
        background-color: #f5f5f5;
        color: #222222;
    }

    /* Menu bar styling */
    QMenuBar {
        background-color: #e8e8e8;
        color: #222222;
        border-bottom: 1px solid #cccccc;
        padding: 2px;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
        margin: 0px;
    }

    QMenuBar::item:selected {
        background-color: #d0d0d0;
        border: 1px solid #aaaaaa;
    }

    QMenuBar::item:pressed {
        background-color: #c0c0c0;
    }

    /* Menu dropdown styling */
    QMenu {
        background-color: #f0f0f0;
        color: #222222;
        border: 1px solid #cccccc;
        padding: 2px;
    }

    QMenu::item {
        background-color: transparent;
        padding: 4px 20px;
        margin: 1px;
    }

    QMenu::item:selected {
        background-color: #4a90e2;
        color: white;
    }

    QMenu::separator {
        height: 1px;
        background-color: #cccccc;
        margin: 2px 0px;
    }

    /* Tool bar styling */
    QToolBar {
        background-color: #e8e8e8;
        border: 1px solid #cccccc;
        spacing: 3px;
        padding: 2px;
        color: #222222;
    }

    QToolBar QAction {
        color: #222222;
    }

    QToolBar::separator {
        background-color: #cccccc;
        width: 1px;
        margin: 0px 2px;
    }

    /* Status bar styling */
    QStatusBar {
        background-color: #e8e8e8;
        color: #222222;
        border-top: 1px solid #cccccc;
    }

    /* Dock widget styling */
    QDockWidget {
        background-color: #f0f0f0;
        color: #222222;
        titlebar-close-icon: url(close.png);
        titlebar-normal-icon: url(undock.png);
    }

    QDockWidget::title {
        background-color: #e0e0e0;
        color: #222222;
        padding: 4px;
        border-bottom: 1px solid #cccccc;
    }

    /* Tab widget styling */
    QTabWidget::pane {
        background-color: #f8f8f8;
        border: 1px solid #cccccc;
    }

    QTabBar::tab {
        background-color: #e0e0e0;
        color: #222222;
        padding: 6px 12px;
        margin-right: 2px;
        border: 1px solid #cccccc;
        border-bottom: none;
    }

    QTabBar::tab:selected {
        background-color: #f8f8f8;
        color: #222222;
    }

    QTabBar::tab:hover {
        background-color: #d8d8d8;
    }

    /* Table view styling */
    QTableWidget {
        background-color: #ffffff;
        color: #222222;
        gridline-color: #e0e0e0;
        selection-background-color: #4a90e2;
        selection-color: white;
        border: 1px solid #cccccc;
    }

    QTableWidget::item {
        padding: 4px;
        border: none;
    }

    QHeaderView::section {
        background-color: #e8e8e8;
        color: #222222;
        padding: 6px;
        border: 1px solid #cccccc;
        border-left: none;
    }

    QHeaderView::section:first {
        border-left: 1px solid #cccccc;
    }

    /* Text edit styling */
    QPlainTextEdit {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #cccccc;
        font-family: "Consolas", "Monaco", "Courier New", monospace;
    }

    /* Dialog styling */
    QDialog {
        background-color: #f5f5f5;
        color: #222222;
    }

    /* List widget styling */
    QListWidget {
        background-color: #f8f8f8;
        color: #222222;
        border: 1px solid #cccccc;
        selection-background-color: #4a90e2;
        selection-color: white;
    }

    QListWidget::item {
        padding: 8px;
        border-bottom: 1px solid #e0e0e0;
        min-height: 20px;
    }

    QListWidget::item:hover {
        background-color: #e8e8e8;
    }

    QListWidget::item:selected {
        background-color: #4a90e2;
        color: white;
    }

    /* Stacked widget styling */
    QStackedWidget {
        background-color: #f8f8f8;
        border: 1px solid #cccccc;
    }

    /* Button styling */
    QPushButton {
        background-color: #e8e8e8;
        color: #222222;
        border: 1px solid #cccccc;
        padding: 6px 12px;
        min-height: 20px;
        border-radius: 3px;
    }

    QPushButton:hover {
        background-color: #d8d8d8;
    }

    QPushButton:pressed {
        background-color: #c8c8c8;
    }

    QPushButton:disabled {
        background-color: #f0f0f0;
        color: #888888;
    }

    /* Group box styling */
    QGroupBox {
        color: #222222;
        border: 1px solid #cccccc;
        border-radius: 3px;
        margin-top: 10px;
        padding-top: 10px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }

    /* Radio button styling */
    QRadioButton {
        color: #222222;
        spacing: 5px;
    }

    QRadioButton::indicator {
        width: 13px;
        height: 13px;
    }

    QRadioButton::indicator:unchecked {
        border: 2px solid #888888;
        border-radius: 7px;
        background-color: white;
    }

    QRadioButton::indicator:checked {
        border: 2px solid #4a90e2;
        border-radius: 7px;
        background-color: #4a90e2;
    }

    /* Combo box styling */
    QComboBox {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #cccccc;
        padding: 4px;
        min-height: 20px;
    }

    QComboBox::drop-down {
        border: none;
        width: 20px;
    }

    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
    }

    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #cccccc;
        selection-background-color: #4a90e2;
        selection-color: white;
    }

    /* Line edit styling */
    QLineEdit {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #cccccc;
        padding: 4px;
        min-height: 20px;
    }

    QLineEdit:focus {
        border: 2px solid #4a90e2;
    }

    /* Checkbox styling */
    QCheckBox {
        color: #222222;
        spacing: 5px;
    }

    QCheckBox::indicator {
        width: 13px;
        height: 13px;
    }

    QCheckBox::indicator:unchecked {
        border: 2px solid #888888;
        background-color: white;
    }

    QCheckBox::indicator:checked {
        border: 2px solid #4a90e2;
        background-color: #4a90e2;
    }

    /* Spin box styling */
    QSpinBox {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #cccccc;
        padding: 4px;
        min-height: 20px;
    }

    QSpinBox:focus {
        border: 2px solid #4a90e2;
    }

    /* Form layout label styling */
    QFormLayout QLabel {
        color: #222222;
        font-weight: normal;
    }

    /* Ensure all labels have dark text on light background */
    QLabel {
        color: #222222;
        background-color: transparent;
    }

    /* Scroll area styling - ensure white background for right panel */
    QScrollArea {
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }

    QScrollArea > QWidget > QWidget {
        background-color: #ffffff;
    }

    QScrollArea QWidget {
        background-color: #ffffff;
    }
    """
