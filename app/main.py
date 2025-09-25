#!/usr/bin/env python3
"""Main application entry point."""

from __future__ import annotations

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from app.ui import style
from app.ui.main_window import MainWindow


def main() -> None:
    """Main application function."""
    app = QApplication(sys.argv)
    
    # Apply global stylesheet
    app.setStyleSheet(style.get_stylesheet())
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
