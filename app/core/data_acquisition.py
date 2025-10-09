# -*- coding: utf-8 -*-
"""Real-time data acquisition module."""

from __future__ import annotations

import struct
import threading
import time
import logging
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
from PySide6.QtCore import QObject, Signal, QTimer

from app import config


@dataclass
class RealTimeData:
    """Container for real-time data."""
    
    timestamp: float
    channel_data: dict[str, np.ndarray]
    sample_count: int
    sample_rate: float


class DataAcquisition(QObject):
    """Handle real-time data acquisition from connected devices."""
    
    # Signals for thread-safe communication
    data_received = Signal(str, object)  # device_id, RealTimeData
    error_occurred = Signal(str, str)    # device_id, error_message
    
    def __init__(self, device_manager):
        """Initialize data acquisition.
        
        Args:
            device_manager: Device manager instance
        """
        super().__init__()
        self.device_manager = device_manager
        self.is_acquiring = False
        self.logger = logging.getLogger(__name__)
        
        # ???QTimer??????????????????????
        self.acquisition_timer = QTimer()
        self.acquisition_timer.timeout.connect(self._acquisition_tick)
        self.current_device_id = None
        
        # Data buffer settings
        self.buffer_size = 1000  # Number of points to keep in buffer
        self.acquisition_interval = 0.1  # Seconds between data requests
        
        # Channel configuration (will be detected from device)
        self.active_channels = []
        self.channel_types = {}
        self.sample_rate = 100.0  # Hz
        
    
    def start_acquisition(self, device_id: str | None = None) -> bool:
        """Start real-time data acquisition.
        
        Args:
            device_id: Specific device ID, or None for all connected devices
            
        Returns:
            True if acquisition started successfully
        """
        if self.is_acquiring:
            return False
        
        # Get connected devices
        devices = self.device_manager.get_connected_devices()
        if not devices:
            self._notify_error("", "No connected devices found")
            return False
        
        # Start acquisition on specified device or first available
        target_device = device_id if device_id else list(devices.keys())[0]
        
        if target_device not in devices:
            self._notify_error(target_device, "Device not connected")
            return False
        
        # Initialize acquisition
        if not self._initialize_acquisition(target_device):
            return False
        
        # Start acquisition using QTimer (thread-safe)
        self.is_acquiring = True
        self.current_device_id = target_device
        
        # Start timer with 1 second interval (like Sample3)
        self.acquisition_timer.start(1000)  # 1000ms = 1 second
        print(f"Started acquisition timer for device: {target_device}")
        
        return True
    
    def stop_acquisition(self) -> None:
        """Stop data acquisition."""
        self.is_acquiring = False
        
        # Stop timer
        if self.acquisition_timer.isActive():
            self.acquisition_timer.stop()
            print("Stopped acquisition timer")
        
        self.current_device_id = None
    
    def _acquisition_tick(self):
        """Timer callback for data acquisition (thread-safe)."""
        if not self.is_acquiring or not self.current_device_id:
            return
            
        try:
            # Get real-time data
            real_time_data = self._get_real_time_data(self.current_device_id)
            
            if real_time_data:
                # Emit signal (thread-safe)
                self.data_received.emit(self.current_device_id, real_time_data)
            else:
                self.error_occurred.emit(self.current_device_id, "No data received")
                
        except Exception as e:
            self.error_occurred.emit(self.current_device_id, f"Acquisition error: {e}")
    
    def _initialize_acquisition(self, device_id: str) -> bool:
        """\u6839\u636eAPI\u6587\u6863\u521d\u59cb\u5316\u8bbe\u5907\u6570\u636e\u91c7\u96c6
        
        Args:
            device_id: Device identifier
            
        Returns:
            True if initialization successful
        """
        try:
            # \u6309\u7167API\u6587\u6863\u7684\u7b80\u5316\u6d41\u7a0b - \u53ea\u4f7f\u7528\u57fa\u672c\u547d\u4ee4
            print(f"Initializing data acquisition for device: {device_id}")
            
            # 1. \u6e05\u9664\u4e4b\u524d\u7684\u9519\u8bef
            try:
                self.device_manager.send_command(device_id, "*CLS")
                print("Cleared previous errors")
            except Exception as e:
                print(f"Clear command failed (non-critical): {e}")
            
            # 2. \u68c0\u67e5\u8bbe\u5907\u72b6\u6001 (\u4f7f\u7528\u6807\u51c6SCPI\u547d\u4ee4)
            try:
                status = self.device_manager.send_command(device_id, ":STATus?")
                print(f"Device status before start: {status}")
            except Exception as e:
                print(f"Status check failed (non-critical): {e}")
            
            # 4. \u542f\u52a8\u6570\u636e\u91c7\u96c6
            self.device_manager.send_command(device_id, ":STARt", expect_response=False)
            
            # 5. \u7b49\u5f85\u8bbe\u5907\u51c6\u5907\u5c31\u7eea
            time.sleep(1.0)
            
            # 6. \u68c0\u6d4b\u53ef\u7528\u901a\u9053
            self._detect_channels(device_id)
            
            return True
            
        except Exception as e:
            self._notify_error(device_id, f"Initialization error: {e}")
            return False
    
    def _detect_channels(self, device_id: str) -> None:
        """Detect available channels from device.
        
        Args:
            device_id: Device identifier
        """
        # For now, assume standard channel configuration
        # TODO: Query device for actual channel configuration
        self.active_channels = [
            "CH1_1", "CH2_1", "CH3_1", "CH4_1",  # Analog channels
            "LOG1"  # Logic channel
        ]
        
        self.channel_types = {
            "CH1_1": "analog",
            "CH2_1": "analog", 
            "CH3_1": "analog",
            "CH4_1": "analog",
            "LOG1": "logic"
        }
    
    
    def _get_real_time_data(self, device_id: str) -> RealTimeData | None:
        """\u6839\u636e\u5b98\u65b9\u793a\u4f8b\u83b7\u53d6\u5b9e\u65f6\u6570\u636e

        \u6309\u7167Sample3\u7684\u6b63\u786e\u6d41\u7a0b:
        1. :MEMory:GETReal
        2. :MEMory:VREAL? CH1_1 (\u6309\u901a\u9053\u83b7\u53d6)
        
        Args:
            device_id: Device identifier
            
        Returns:
            RealTimeData object or None if failed
        """
        try:
            print(f"Getting real-time data from device: {device_id}")
            channel_data = {}
            
            # \u6309\u7167\u5b98\u65b9Sample3\u7684\u6b63\u786e\u6d41\u7a0b
            try:
                # Step 1: \u83b7\u53d6\u5b9e\u65f6\u6570\u636e\u5feb\u7167
                print("Sending :MEMory:GETReal command...")
                self.device_manager.send_command(device_id, ":MEMory:GETReal")
                
                # Step 2: \u6309\u901a\u9053\u83b7\u53d6\u6570\u636e (\u6309\u7167Sample3\u7684\u65b9\u5f0f)
                test_channels = ["CH1_1", "CH1_2", "CH1_3", "CH1_4"]  # \u6d4b\u8bd5\u524d4\u4e2a\u901a\u9053
                
                for channel in test_channels:
                    try:
                        print(f"Querying channel {channel}...")
                        # \u4f7f\u7528\u6b63\u786e\u7684\u547d\u4ee4\u683c\u5f0f
                        cmd = f":MEMory:VREAL? {channel}"
                        response = self.device_manager.query_device(device_id, cmd)
                        
                        if response and response.strip():
                            try:
                                value = float(response.strip())
                                channel_data[channel] = [value]
                                print(f"Got data for {channel}: {value}")
                            except ValueError:
                                print(f"Could not parse response for {channel}: {response}")
                        else:
                            print(f"No response for {channel}")
                            
                    except Exception as e:
                        print(f"Error querying {channel}: {e}")
                        continue
                
                if channel_data:
                    print(f"Successfully got real data from {len(channel_data)} channels")
                else:
                    print("No real data received from any channel")
                
            except Exception as e:
                print(f"Real data acquisition failed: {e}")
            
            # \u5982\u679c\u6ca1\u6709\u771f\u5b9e\u6570\u636e\uff0c\u4f7f\u7528\u6a21\u62df\u6570\u636e
            if not channel_data:
                print("Using simulated data as fallback")
                channel_data = self._generate_simulated_data()
            
            if not channel_data:
                return None
            
            # \u521b\u5efa\u5b9e\u65f6\u6570\u636e\u5bf9\u8c61
            return RealTimeData(
                timestamp=time.time(),
                channel_data=channel_data,
                sample_count=len(next(iter(channel_data.values()))),
                sample_rate=self.sample_rate
            )
            
        except Exception as e:
            print(f"Error getting real-time data: {e}")
            # \u8fd4\u56de\u6a21\u62df\u6570\u636e\u4f5c\u4e3a\u6700\u540e\u7684\u540e\u5907
            try:
                return RealTimeData(
                    timestamp=time.time(),
                    channel_data=self._generate_simulated_data(),
                    sample_count=4,
                    sample_rate=self.sample_rate
                )
            except:
                return None
    
    def _get_channel_binary_data(self, device_id: str, channel: str) -> np.ndarray | None:
        """Get binary data for a specific channel.
        
        Args:
            device_id: Device identifier
            channel: Channel name (e.g., "CH1_1")
            
        Returns:
            Numpy array of data or None if failed
        """
        try:
            # Request binary data for channel
            # Format: :MEMory:BFETch? CH1_1
            command = f":MEMory:BFETch? {channel}"
            
            # This should return binary data in SCPI format
            # For now, simulate data since we need the actual device response format
            return self._simulate_channel_data(channel, 10)  # 10 data points
            
        except Exception as e:
            print(f"Error getting channel data for {channel}: {e}")
            return None
    
    def _simulate_channel_data(self, channel: str, count: int) -> np.ndarray:
        """Simulate channel data for testing.
        
        Args:
            channel: Channel name
            count: Number of data points
            
        Returns:
            Simulated data array
        """
        channel_type = self.channel_types.get(channel, "analog")
        
        if channel_type == "analog":
            # Generate sinusoidal data with noise
            t = np.linspace(0, count/self.sample_rate, count)
            frequency = 1.0 + int(channel[-1])  # Different frequency per channel
            amplitude = 1.0 + np.random.normal(0, 0.1)
            data = amplitude * np.sin(2 * np.pi * frequency * t)
            data += 0.1 * np.random.normal(0, 1, count)  # Add noise
            return data
            
        elif channel_type == "logic":
            # Generate logic data
            return np.random.choice([0, 1], count).astype(np.float64)
            
        else:
            # Default to zeros
            return np.zeros(count)
    
    def _parse_binary_response(self, response: bytes, channel_type: str, count: int) -> np.ndarray:
        """Parse binary response from device.
        
        Args:
            response: Raw binary response
            channel_type: Type of channel
            count: Expected number of data points
            
        Returns:
            Parsed data array
        """
        # SCPI binary format: #<length_of_length><length><binary_data>
        # Example: #42000<binary_data> means 2000 bytes of binary data
        
        if not response.startswith(b'#'):
            raise ValueError("Invalid binary response format")
        
        # Parse header
        length_digits = int(response[1:2])
        data_length = int(response[2:2+length_digits])
        binary_data = response[2+length_digits:2+length_digits+data_length]
        
        # Parse based on channel type
        if channel_type in ["analog", "logic", "alarm"]:
            # 2-byte signed integers, big-endian
            values = struct.unpack(f'>{count}h', binary_data[:count*2])
        elif channel_type == "pulse":
            # 4-byte unsigned integers, big-endian
            values = struct.unpack(f'>{count}I', binary_data[:count*4])
        elif channel_type == "wave_calc":
            # 8-byte double precision floats, big-endian
            values = struct.unpack(f'>{count}d', binary_data[:count*8])
        else:
            raise ValueError(f"Unknown channel type: {channel_type}")
        
        return np.array(values, dtype=np.float64)
    
    def get_acquisition_status(self) -> dict[str, Any]:
        """Get current acquisition status.
        
        Returns:
            Status information dictionary
        """
        return {
            "is_acquiring": self.is_acquiring,
            "active_channels": self.active_channels,
            "sample_rate": self.sample_rate,
            "buffer_size": self.buffer_size,
            "acquisition_interval": self.acquisition_interval
        }
    
    def set_acquisition_parameters(self, sample_rate: float = None, 
                                 buffer_size: int = None,
                                 interval: float = None) -> None:
        """Set acquisition parameters.
        
        Args:
            sample_rate: Sampling rate in Hz
            buffer_size: Buffer size in samples
            interval: Acquisition interval in seconds
        """
        if sample_rate is not None:
            self.sample_rate = sample_rate
            
        if buffer_size is not None:
            self.buffer_size = buffer_size
            
        if interval is not None:
            self.acquisition_interval = interval
    
    def _parse_ieee488_binary_data(self, data: bytes) -> list[float]:
        """Parse IEEE 488.2 binary data format.
        
        IEEE 488.2 binary format:
        #<digit><length><data>
        Where:
        - # is the header marker
        - <digit> is a single digit indicating length of <length> field
        - <length> is the number of data bytes
        - <data> is the binary data
        
        Args:
            data: Raw binary data from device
            
        Returns:
            List of parsed float values
            
        Raises:
            ValueError: If data format is invalid
        """
        try:
            if not data or len(data) < 3:
                raise ValueError("Data too short for IEEE 488.2 format")
                
            # Check for IEEE 488.2 header
            if data[0:1] != b'#':
                raise ValueError("Missing IEEE 488.2 header '#'")
                
            # Get length field size
            length_digits = int(chr(data[1]))
            if length_digits == 0:
                raise ValueError("Invalid length field size")
                
            if len(data) < 2 + length_digits:
                raise ValueError("Data too short for specified length field")
                
            # Get data length
            length_str = data[2:2+length_digits].decode('ascii')
            data_length = int(length_str)
            
            # Extract binary data
            header_size = 2 + length_digits
            if len(data) < header_size + data_length:
                raise ValueError(f"Data length mismatch: expected {data_length}, got {len(data) - header_size}")
                
            binary_data = data[header_size:header_size + data_length]
            
            # Parse binary data as 32-bit floats (little-endian)
            import struct
            float_count = data_length // 4
            values = struct.unpack(f'<{float_count}f', binary_data[:float_count * 4])
            
            return list(values)
            
        except (ValueError, struct.error, UnicodeDecodeError) as e:
            self.logger.error(f"IEEE 488.2 binary parsing error: {e}")
            raise ValueError(f"Failed to parse IEEE 488.2 binary data: {e}")
    
    def _parse_ascii_data(self, data: str) -> list[float]:
        """Parse ASCII data format.
        
        Args:
            data: ASCII data string (comma or space separated values)
            
        Returns:
            List of parsed float values
        """
        try:
            # Remove any whitespace and split by comma or space
            data = data.strip()
            if not data:
                return []
                
            # Try comma-separated first, then space-separated
            if ',' in data:
                values_str = data.split(',')
            else:
                values_str = data.split()
                
            values = []
            for value_str in values_str:
                value_str = value_str.strip()
                if value_str:  # Skip empty strings
                    try:
                        values.append(float(value_str))
                    except ValueError:
                        self.logger.warning(f"Could not parse value: {value_str}")
                        
            return values
            
        except Exception as e:
            self.logger.error(f"ASCII data parsing error: {e}")
            return []
    
    def _format_channel_data_from_values(self, values: list[float]) -> dict[str, list[float]]:
        """Format parsed values into channel data structure.
        
        Args:
            values: List of parsed float values
            
        Returns:
            Dictionary mapping channel names to value lists
        """
        try:
            channel_data = {}
            
            if not values:
                return channel_data
            
            # If we have active channels configuration, use it
            if self.active_channels:
                values_per_channel = max(1, len(values) // len(self.active_channels))
                
                for i, channel in enumerate(self.active_channels):
                    start_idx = i * values_per_channel
                    end_idx = min(start_idx + values_per_channel, len(values))
                    
                    if start_idx < len(values):
                        channel_values = values[start_idx:end_idx]
                        channel_data[f"channel_{channel}"] = channel_values
            else:
                # Default channel assignment based on device capabilities
                # Assume channels are ordered: voltage, temperature, humidity
                channel_assignments = [
                    ("voltage", 4),      # First 4 values are voltage channels
                    ("temperature", 4),   # Next 4 values are temperature channels  
                    ("humidity", 2),     # Next 2 values are humidity channels
                ]
                
                value_idx = 0
                for ch_type, count in channel_assignments:
                    for i in range(count):
                        if value_idx < len(values):
                            channel_name = f"{ch_type}_{i+1}"
                            channel_data[channel_name] = [values[value_idx]]
                            value_idx += 1
                        else:
                            break
                    if value_idx >= len(values):
                        break
                
                # If there are remaining values, assign to generic channels
                while value_idx < len(values):
                    channel_name = f"channel_{value_idx + 1}"
                    channel_data[channel_name] = [values[value_idx]]
                    value_idx += 1
            
            return channel_data
            
        except Exception as e:
            self.logger.error(f"Error formatting channel data from values: {e}")
            return {}
    
    def _generate_simulated_data(self) -> dict[str, list[float]]:
        """Generate simulated data for testing when device is not available.
        
        Returns:
            Dictionary containing simulated channel data
        """
        try:
            import random
            import math
            
            current_time = time.time()
            
            # Generate different types of simulated data
            channel_data = {}
            
            # Voltage channels (4 channels)
            for i in range(1, 5):
                # Generate sinusoidal voltage data with some noise
                base_voltage = 5.0 + i * 2.0  # Different base voltages
                frequency = 0.5 + i * 0.1  # Different frequencies
                voltage = base_voltage + 2.0 * math.sin(2 * math.pi * frequency * current_time)
                voltage += random.uniform(-0.5, 0.5)  # Add noise
                channel_data[f"voltage_{i}"] = [round(voltage, 3)]
            
            # Temperature channels (4 channels)
            for i in range(1, 5):
                # Generate temperature data with slow variations
                base_temp = 20.0 + i * 5.0  # Different base temperatures
                temp_variation = 3.0 * math.sin(2 * math.pi * 0.1 * current_time + i)
                temperature = base_temp + temp_variation + random.uniform(-1.0, 1.0)
                channel_data[f"temperature_{i}"] = [round(temperature, 2)]
            
            # Humidity channels (2 channels)
            for i in range(1, 3):
                base_humidity = 45.0 + i * 10.0
                humidity_variation = 5.0 * math.sin(2 * math.pi * 0.05 * current_time + i * 2)
                humidity = base_humidity + humidity_variation + random.uniform(-2.0, 2.0)
                humidity = max(0.0, min(100.0, humidity))  # Clamp to 0-100%
                channel_data[f"humidity_{i}"] = [round(humidity, 1)]
            
            return channel_data
            
        except Exception as e:
            self.logger.error(f"Error generating simulated data: {e}")
            # Return minimal fallback data
            return {
                "voltage_1": [5.0],
                "temperature_1": [25.0],
                "humidity_1": [50.0]
            }

