# -*- coding: utf-8 -*-
"""XUNYU XY2580 file format parser."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO

import numpy as np

from app import config


@dataclass
class ChannelData:
    """Channel data container."""
    
    name: str
    channel_type: str  # "analog", "logic", "alarm", "pulse", "wave_calc"
    unit: str
    data: np.ndarray
    sample_rate: float
    range_info: dict[str, Any] | None = None


@dataclass
class WaveformData:
    """Complete waveform data container."""
    
    channels: list[ChannelData]
    start_time: str
    recording_duration: float
    sample_count: int
    device_info: dict[str, Any] | None = None
    comments: str = ""


class HIOKIFileParser:
    """Parser for XUNYU XY2580 file formats (compatible with HIOKI LR8450)."""
    
    # Data type sizes in bytes
    DATA_SIZES = {
        "analog": 2,
        "logic": 2, 
        "alarm": 2,
        "pulse": 4,
        "wave_calc": 8,
    }
    
    def __init__(self) -> None:
        """Initialize the parser."""
        pass
    
    def parse_file(self, file_path: str | Path) -> WaveformData:
        """Parse a device file and return waveform data.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            WaveformData object containing parsed data
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == ".luw":
            return self._parse_luw_file(file_path)
        elif suffix == ".lus":
            return self._parse_lus_file(file_path)
        elif suffix == ".mem":
            return self._parse_mem_file(file_path)
        elif suffix == ".csv":
            return self._parse_csv_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def _parse_luw_file(self, file_path: Path) -> WaveformData:
        """Parse LUW binary file format.
        
        Note: This is a simplified parser. The actual LUW format
        would require detailed reverse engineering of the binary structure.
        """
        # For now, create a mock implementation
        # TODO: Implement actual LUW binary parsing
        return self._create_mock_waveform_data(file_path.name)
    
    def _parse_lus_file(self, file_path: Path) -> WaveformData:
        """Parse LUS settings file format."""
        # LUS files typically contain device configuration
        # For now, return empty waveform data
        return WaveformData(
            channels=[],
            start_time="",
            recording_duration=0.0,
            sample_count=0,
            device_info={"file_type": "LUS", "file_name": file_path.name},
            comments=f"Settings file: {file_path.name}"
        )
    
    def _parse_mem_file(self, file_path: Path) -> WaveformData:
        """Parse MEM memory file format."""
        # For now, create a mock implementation
        return self._create_mock_waveform_data(file_path.name)
    
    def _parse_csv_file(self, file_path: Path) -> WaveformData:
        """Parse CSV text file format."""
        try:
            import pandas as pd
            
            # Read CSV file
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # Extract channel data
            channels = []
            for col in df.columns:
                # Check for time columns using ASCII keywords only
                if col.lower() in ['time', 'timestamp', 'times']:
                    continue
                    
                # Create channel data
                channel_data = ChannelData(
                    name=col,
                    channel_type="analog",  # Assume analog for CSV
                    unit="V",  # Default unit
                    data=df[col].values,
                    sample_rate=1.0,  # Default sample rate
                )
                channels.append(channel_data)
            
            return WaveformData(
                channels=channels,
                start_time="2024-01-01 00:00:00",
                recording_duration=len(df) * 1.0,  # Assume 1 second per sample
                sample_count=len(df),
                device_info={"file_type": "CSV", "file_name": file_path.name},
                comments=f"CSV file imported: {file_path.name}"
            )
            
        except ImportError:
            # Fallback if pandas not available
            return self._parse_csv_simple(file_path)
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {e}")
    
    def _parse_csv_simple(self, file_path: Path) -> WaveformData:
        """Simple CSV parser without pandas."""
        channels = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if not lines:
            raise ValueError("Empty CSV file")
        
        # Parse header
        headers = [h.strip() for h in lines[0].split(',')]
        
        # Parse data
        data_rows = []
        for line in lines[1:]:
            try:
                row = [float(x.strip()) for x in line.split(',')]
                data_rows.append(row)
            except ValueError:
                continue  # Skip invalid rows
        
        if not data_rows:
            raise ValueError("No valid data found in CSV file")
        
        data_array = np.array(data_rows)
        
        # Create channels
        for i, header in enumerate(headers):
            # Check for time columns using ASCII keywords only
            if header.lower() in ['time', 'timestamp', 'times']:
                continue
                
            if i < data_array.shape[1]:
                channel_data = ChannelData(
                    name=header,
                    channel_type="analog",
                    unit="V",
                    data=data_array[:, i],
                    sample_rate=1.0,
                )
                channels.append(channel_data)
        
        return WaveformData(
            channels=channels,
            start_time="2024-01-01 00:00:00",
            recording_duration=len(data_rows) * 1.0,
            sample_count=len(data_rows),
            device_info={"file_type": "CSV", "file_name": file_path.name},
            comments=f"CSV file imported: {file_path.name}"
        )
    
    def _create_mock_waveform_data(self, filename: str) -> WaveformData:
        """Create mock waveform data for testing purposes."""
        # Generate sample data
        sample_count = 1000
        time_array = np.linspace(0, 10, sample_count)  # 10 seconds
        
        channels = []
        
        # Create 4 analog channels with different waveforms
        for i in range(4):
            frequency = 1.0 + i * 0.5  # Different frequencies
            amplitude = 1.0 + i * 0.5   # Different amplitudes
            
            # Generate sinusoidal data with some noise
            data = amplitude * np.sin(2 * np.pi * frequency * time_array)
            data += 0.1 * np.random.normal(0, 1, sample_count)  # Add noise
            
            channel = ChannelData(
                name=f"CH{i+1}_1",
                channel_type="analog",
                unit="V",
                data=data,
                sample_rate=100.0,  # 100 Hz
                range_info={"min": -5.0, "max": 5.0}
            )
            channels.append(channel)
        
        # Add a logic channel
        logic_data = np.random.choice([0, 1], sample_count)
        logic_channel = ChannelData(
            name="LOG1",
            channel_type="logic",
            unit="",
            data=logic_data,
            sample_rate=100.0
        )
        channels.append(logic_channel)
        
        return WaveformData(
            channels=channels,
            start_time="2024-01-01 12:00:00",
            recording_duration=10.0,
            sample_count=sample_count,
            device_info={
                "model": config.DEVICE_MODEL,
                "manufacturer": config.DEVICE_MANUFACTURER,
                "serial": "12345678",
                "firmware": "1.0.0",
                "file_type": "LUW",
                "file_name": filename,
                "compatible_with": f"{config.INTERNAL_MANUFACTURER} {config.INTERNAL_MODEL}"
            },
            comments="Mock waveform data for testing"
        )
    
    def parse_binary_data(self, data: bytes, channel_type: str, count: int) -> np.ndarray:
        """Parse binary data based on channel type.
        
        Args:
            data: Raw binary data
            channel_type: Type of channel ("analog", "logic", "alarm", "pulse", "wave_calc")
            count: Number of data points
            
        Returns:
            numpy array of parsed data
        """
        size = self.DATA_SIZES.get(channel_type, 2)
        expected_size = count * size
        
        if len(data) < expected_size:
            raise ValueError(f"Insufficient data: expected {expected_size}, got {len(data)}")
        
        if channel_type in ["analog", "logic", "alarm"]:
            # 2-byte signed integers, big-endian
            values = struct.unpack(f">{count}h", data[:expected_size])
        elif channel_type == "pulse":
            # 4-byte unsigned integers, big-endian  
            values = struct.unpack(f">{count}I", data[:expected_size])
        elif channel_type == "wave_calc":
            # 8-byte double precision floats, big-endian
            values = struct.unpack(f">{count}d", data[:expected_size])
        else:
            raise ValueError(f"Unknown channel type: {channel_type}")
        
        return np.array(values)
