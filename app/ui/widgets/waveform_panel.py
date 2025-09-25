"""Waveform display panel using pyqtgraph."""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class WaveformPanel(QWidget):
    """Main waveform display panel."""

    def __init__(self) -> None:
        """Initialize the waveform panel."""
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#2b2b2b')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', '\u7535\u538b (V)')
        self.plot_widget.setLabel('bottom', '\u65f6\u95f4 (s)')
        
        layout.addWidget(self.plot_widget)

        # Add some sample data
        self._add_sample_data()

    def _add_sample_data(self) -> None:
        """Add sample waveform data for demonstration."""
        # Generate sample data
        t = np.linspace(0, 10, 1000)
        y1 = np.sin(2 * np.pi * t) + 0.1 * np.random.normal(size=len(t))
        y2 = np.cos(2 * np.pi * t * 1.5) + 0.1 * np.random.normal(size=len(t))
        
        # Plot the data
        self.plot_widget.plot(t, y1, pen='r', name='\u901a\u9053 1')
        self.plot_widget.plot(t, y2, pen='g', name='\u901a\u9053 2')
        
        # Add legend
        self.plot_widget.addLegend()
