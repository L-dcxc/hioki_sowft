"""Waveform display panel using pyqtgraph."""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget

# Import here to avoid circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.file_parser import WaveformData
    from app.core.data_acquisition import RealTimeData


class WaveformPanel(QWidget):
    """Main waveform display panel."""

    def __init__(self) -> None:
        """Initialize the waveform panel."""
        super().__init__()
        self.current_waveform_data: WaveformData | None = None
        self.real_time_mode = False
        self.real_time_curves = {}  # Store plot curves for real-time updates
        self.real_time_data_buffer = {}  # Buffer for real-time data
        self.buffer_size = 1000  # Maximum points to keep in buffer
        
        # Multi-scale settings
        self.active_scales = [0, 1]  # Default to 2 scales
        self.scale_configs = {}  # Scale configuration for each scale  
        self.time_scale = "1s"
        self.background_color = "black"
        
        # Multi-Y-axis support
        self.y_axes = {}  # Store different Y axes (max 8)
        self.axis_colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ]  # 8 different colors for axes
        self.channel_axis_mapping = {}  # Map channels to axis indices
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create plot widget with multi-axis support
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#2b2b2b')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('bottom', '\u65f6\u95f4 (s)')
        
        # Initialize default Y-axes
        self._setup_initial_axes()
        
        layout.addWidget(self.plot_widget)

        # Add some sample data
        self._add_sample_data()
    
    def _setup_initial_axes(self) -> None:
        """\u521d\u59cb\u5316\u591a\u4e2aY\u8f74"""
        # \u4e3b\u8f74 (axis 0) - \u9ed8\u8ba4\u7535\u538b
        main_axis = self.plot_widget.getAxis('left')
        main_axis.setLabel('\u7535\u538b (V)', color=self.axis_colors[0])
        main_axis.setPen(color=self.axis_colors[0], width=2)
        self.y_axes[0] = {
            'axis': main_axis,
            'viewbox': self.plot_widget.getViewBox(),
            'label': '\u7535\u538b (V)',
            'range': (-10, 10),
            'unit': 'V',
            'color': self.axis_colors[0],
            'channels': []
        }
        
        # \u521d\u59cb\u5316\u7b2c\u4e8c\u4e2a\u8f74 (axis 1) - \u9ed8\u8ba4\u6e29\u5ea6
        self._add_y_axis(1, '\u6e29\u5ea6 (\u00b0C)', (-50, 100), '\u00b0C')
    
    def _add_y_axis(self, axis_id: int, label: str, range_values: tuple, unit: str) -> None:
        """\u6dfb\u52a0\u65b0\u7684Y\u8f74"""
        if axis_id >= 8:  # \u6700\u591a8\u4e2a\u8f74
            return
        
        if axis_id == 0:  # \u4e3b\u8f74\u5df2\u7ecf\u5b58\u5728
            return
            
        # \u521b\u5efa\u65b0\u7684ViewBox\u548cAxis
        viewbox = pg.ViewBox()
        axis = pg.AxisItem('left')
        axis.setLabel(label, color=self.axis_colors[axis_id])
        axis.setPen(color=self.axis_colors[axis_id], width=2)
        axis.linkToView(viewbox)
        
        # \u6dfb\u52a0\u5230\u5e03\u5c40\u4e2d (\u68c0\u67e5\u662f\u5426\u5df2\u5b58\u5728\u907f\u514d\u91cd\u590d)
        layout = self.plot_widget.plotItem.layout
        
        # \u68c0\u67e5\u8be5\u4f4d\u7f6e\u662f\u5426\u5df2\u6709\u8f74
        existing_item = layout.itemAt(2, axis_id + 1)
        if existing_item is not None:
            layout.removeItem(existing_item)
            
        layout.addItem(axis, 2, axis_id + 1)  # \u653e\u7f6e\u5728\u5de6\u4fa7
        
        # \u8fde\u63a5ViewBox\u5230\u4e3b\u56fe
        viewbox.setXLink(self.plot_widget.getViewBox())
        
        # \u5b58\u50a8\u8f74\u4fe1\u606f
        self.y_axes[axis_id] = {
            'axis': axis,
            'viewbox': viewbox,
            'label': label,
            'range': range_values,
            'unit': unit,
            'color': self.axis_colors[axis_id],
            'channels': []
        }
        
        # \u8bbe\u7f6e\u8303\u56f4
        viewbox.setYRange(range_values[0], range_values[1])
    
    def assign_channel_to_axis(self, channel_id: int, axis_id: int) -> None:
        """\u5c06\u901a\u9053\u5206\u914d\u5230\u6307\u5b9a\u7684Y\u8f74"""
        if axis_id not in self.y_axes:
            return
            
        # \u4ece\u65e7\u8f74\u4e2d\u79fb\u9664
        for aid, axis_info in self.y_axes.items():
            if channel_id in axis_info['channels']:
                axis_info['channels'].remove(channel_id)
        
        # \u6dfb\u52a0\u5230\u65b0\u8f74
        self.y_axes[axis_id]['channels'].append(channel_id)
        self.channel_axis_mapping[channel_id] = axis_id
    
    def display_waveform_data(self, waveform_data: WaveformData) -> None:
        """Display waveform data from a parsed file.
        
        Args:
            waveform_data: Parsed waveform data to display
        """
        self.current_waveform_data = waveform_data
        
        # Clear existing plots
        self.plot_widget.clear()
        
        if not waveform_data.channels:
            return
        
        # Define colors for different channels
        colors = ['#ff4444', '#44ff44', '#4444ff', '#ffff44', '#ff44ff', '#44ffff']
        
        # Calculate time array based on sample rate
        sample_count = waveform_data.sample_count
        if sample_count > 0 and waveform_data.channels:
            # Use the first channel's sample rate
            sample_rate = waveform_data.channels[0].sample_rate
            time_array = np.arange(sample_count) / sample_rate
        else:
            time_array = np.array([])
        
        # \u81ea\u52a8\u5206\u914d\u901a\u9053\u5230\u4e0d\u540c\u7684Y\u8f74
        self._auto_assign_channels_to_axes(waveform_data.channels)
        
        # \u4e3a\u6bcf\u4e2a\u901a\u9053\u7ed8\u5236\u6570\u636e
        for i, channel in enumerate(waveform_data.channels):
            if len(channel.data) == 0:
                continue
            
            # \u83b7\u53d6\u901a\u9053\u5bf9\u5e94\u7684Y\u8f74
            axis_id = self.channel_axis_mapping.get(i, 0)  # \u9ed8\u8ba4\u4f7f\u7528\u8f740
            axis_info = self.y_axes[axis_id]
            
            # \u4f7f\u7528\u8f74\u7684\u989c\u8272\u4f5c\u4e3a\u901a\u9053\u989c\u8272
            color = axis_info['color']
            
            # \u5904\u7406\u903b\u8f91\u901a\u9053\u7684\u7279\u6b8a\u663e\u793a
            if channel.channel_type == "logic":
                offset = i * 1.5  # \u903b\u8f91\u901a\u9053\u504f\u79fb
                y_data = channel.data + offset
                label = f"{channel.name} (Logic)"
            else:
                y_data = channel.data
                label = f"{channel.name} ({channel.unit})" if channel.unit else channel.name
            
            # \u4f7f\u7528\u65f6\u95f4\u6570\u7ec4\u6216\u6837\u672c\u7d22\u5f15
            if len(time_array) == len(y_data):
                x_data = time_array
            else:
                x_data = np.arange(len(y_data))
            
            # \u5728\u5bf9\u5e94\u7684ViewBox\u4e2d\u7ed8\u5236\u6570\u636e
            viewbox = axis_info['viewbox']
            curve = pg.PlotDataItem(
                x_data, 
                y_data,
                pen=pg.mkPen(color=color, width=2),
                name=label
            )
            viewbox.addItem(curve)
        
        # Update labels
        self.plot_widget.setLabel('bottom', '\u65f6\u95f4 (s)')
        if len(waveform_data.channels) == 1:
            # Single channel - use its unit
            unit = waveform_data.channels[0].unit or "Value"
            self.plot_widget.setLabel('left', f'\u5e45\u5ea6 ({unit})')
        else:
            # Multiple channels - generic label
            self.plot_widget.setLabel('left', '\u5e45\u5ea6')
        
        # Add legend if multiple channels
        if len(waveform_data.channels) > 1:
            self.plot_widget.addLegend()
        
        # Set title with file info
        if waveform_data.device_info and 'file_name' in waveform_data.device_info:
            title = f"\u6ce2\u5f62\u6570\u636e: {waveform_data.device_info['file_name']}"
            self.plot_widget.setTitle(title)

    def _add_sample_data(self) -> None:
        """Add sample waveform data for demonstration."""
        # Generate sample data
        t = np.linspace(0, 10, 1000)
        y1 = np.sin(2 * np.pi * t) + 0.1 * np.random.normal(size=len(t))
        y2 = np.cos(2 * np.pi * t * 1.5) + 0.1 * np.random.normal(size=len(t))
        
        # Plot the data
        self.plot_widget.plot(t, y1, pen='#ff4444', name='\u793a\u4f8b\u901a\u9053 1')
        self.plot_widget.plot(t, y2, pen='#44ff44', name='\u793a\u4f8b\u901a\u9053 2')
        
        # Add legend
        self.plot_widget.addLegend()
    
    def update_real_time_data(self, data: RealTimeData) -> None:
        """Update waveform display with real-time data.
        
        Args:
            data: Real-time data from acquisition
        """
        # Switch to real-time mode if not already
        if not self.real_time_mode:
            self._switch_to_real_time_mode()
        
        # Update data buffer for each channel
        for channel_name, channel_data in data.channel_data.items():
            if channel_name not in self.real_time_data_buffer:
                self.real_time_data_buffer[channel_name] = {
                    'data': np.array([]),
                    'time': np.array([])
                }
            
            # Add new data to buffer
            buffer = self.real_time_data_buffer[channel_name]
            
            # Create time array for new data
            if len(buffer['time']) > 0:
                last_time = buffer['time'][-1]
                new_time = np.arange(len(channel_data)) / data.sample_rate + last_time + (1.0 / data.sample_rate)
            else:
                new_time = np.arange(len(channel_data)) / data.sample_rate
            
            # Append new data
            buffer['data'] = np.concatenate([buffer['data'], channel_data])
            buffer['time'] = np.concatenate([buffer['time'], new_time])
            
            # Limit buffer size
            if len(buffer['data']) > self.buffer_size:
                excess = len(buffer['data']) - self.buffer_size
                buffer['data'] = buffer['data'][excess:]
                buffer['time'] = buffer['time'][excess:]
            
            # Update plot curve
            if channel_name in self.real_time_curves:
                self.real_time_curves[channel_name].setData(buffer['time'], buffer['data'])
    
    def _switch_to_real_time_mode(self) -> None:
        """Switch display to real-time mode."""
        self.real_time_mode = True
        
        # Clear existing plots
        self.plot_widget.clear()
        
        # Setup for real-time display
        self.plot_widget.setLabel('bottom', '\u65f6\u95f4 (s)')
        self.plot_widget.setLabel('left', '\u5e45\u5ea6')
        self.plot_widget.setTitle('\u5b9e\u65f6\u6ce2\u5f62\u6570\u636e')
        
        # Enable auto-ranging
        self.plot_widget.enableAutoRange()
        
        # Define colors for channels
        colors = ['#ff4444', '#44ff44', '#4444ff', '#ffff44', '#ff44ff', '#44ffff']
        
        # Pre-create curves for expected channels
        expected_channels = ["CH1_1", "CH2_1", "CH3_1", "CH4_1", "LOG1"]
        
        for i, channel in enumerate(expected_channels):
            color = colors[i % len(colors)]
            curve = self.plot_widget.plot(
                [], [], 
                pen=color, 
                name=channel
            )
            self.real_time_curves[channel] = curve
        
        # Add legend
        self.plot_widget.addLegend()
    
    def switch_to_file_mode(self) -> None:
        """Switch back to file display mode."""
        self.real_time_mode = False
        self.real_time_curves.clear()
        self.real_time_data_buffer.clear()
        
        # Restore sample data or clear
        self.plot_widget.clear()
        self._add_sample_data()
    
    def update_scale_configuration(self, active_scales: list[int]) -> None:
        """Update active scales configuration.
        
        Args:
            active_scales: List of active scale indices (0-7)
        """
        self.active_scales = active_scales
        # TODO: Implement multi-scale Y-axis display
        print(f"Active scales updated: {active_scales}")
    
    def update_time_scale(self, time_scale: str) -> None:
        """Update time scale setting.
        
        Args:
            time_scale: Time scale string (e.g., "1s", "100ms")
        """
        self.time_scale = time_scale
        # TODO: Update X-axis time scale
        print(f"Time scale updated: {time_scale}")
    
    def update_background(self, background: str) -> None:
        """Update background color.
        
        Args:
            background: Background color ("black" or "white")
        """
        self.background_color = background
        
        if background == "black":
            self.plot_widget.setBackground('#2b2b2b')
        else:
            self.plot_widget.setBackground('#ffffff')
            
        print(f"Background updated: {background}")
    
    def _auto_assign_channels_to_axes(self, channels) -> None:
        """\u81ea\u52a8\u5c06\u901a\u9053\u5206\u914d\u5230\u5408\u9002\u7684Y\u8f74"""
        for i, channel in enumerate(channels):
            # \u6839\u636e\u901a\u9053\u7c7b\u578b\u81ea\u52a8\u5206\u914d\u8f74
            if '\u7535\u538b' in channel.name or 'V' in str(channel.unit):
                axis_id = 0  # \u7535\u538b\u4f7f\u7528\u8f740
            elif '\u6e29\u5ea6' in channel.name or '\u00b0C' in str(channel.unit):
                axis_id = 1  # \u6e29\u5ea6\u4f7f\u7528\u8f741
            elif '\u6e7f\u5ea6' in channel.name or '%' in str(channel.unit):
                # \u5982\u679c\u8f742\u4e0d\u5b58\u5728\uff0c\u521b\u5efa\u5b83
                if 2 not in self.y_axes:
                    self._add_y_axis(2, '\u6e7f\u5ea6 (%)', (0, 100), '%')
                axis_id = 2
            else:
                # \u5176\u4ed6\u7c7b\u578b\u4f7f\u7528\u53ef\u7528\u7684\u8f74
                axis_id = min(len(self.y_axes), 7)  # \u6700\u591a8\u4e2a\u8f74
                if axis_id not in self.y_axes:
                    # \u8ba1\u7b97\u6570\u636e\u8303\u56f4
                    data_min = min(channel.data) if len(channel.data) > 0 else 0
                    data_max = max(channel.data) if len(channel.data) > 0 else 10
                    margin = (data_max - data_min) * 0.1  # 10%\u8fb9\u8ddd
                    range_values = (data_min - margin, data_max + margin)
                    
                    self._add_y_axis(axis_id, f'{channel.name} ({channel.unit})', 
                                    range_values, str(channel.unit))
            
            self.assign_channel_to_axis(i, axis_id)
    
    def get_axis_info(self) -> dict:
        """\u83b7\u53d6\u6240\u6709Y\u8f74\u4fe1\u606f"""
        return self.y_axes.copy()
    
    def get_channel_axis_mapping(self) -> dict:
        """\u83b7\u53d6\u901a\u9053\u5230Y\u8f74\u7684\u6620\u5c04\u5173\u7cfb"""
        return self.channel_axis_mapping.copy()
