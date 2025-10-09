# -*- coding: utf-8 -*-
"""Device connection and management module."""

from __future__ import annotations

import socket
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from app import config
from app.core.device_identifier import DeviceIdentifier


class ConnectionStatus(Enum):
    """Device connection status."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class DeviceInfo:
    """Device information container."""
    ip_address: str
    port: int
    device_id: str
    manufacturer: str
    model: str
    serial: str
    firmware: str
    connection_type: str = "LAN"
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    last_error: str = ""


class DeviceManager:
    """Manage device connections and communication."""
    
    def __init__(self):
        """Initialize the device manager."""
        self.identifier = DeviceIdentifier()
        self.connected_devices: dict[str, DeviceInfo] = {}
        self.sockets: dict[str, socket.socket] = {}
        self.status_callbacks: list[Callable[[str, ConnectionStatus], None]] = []
        self.data_callbacks: list[Callable[[str, dict], None]] = []
        self._discovery_thread: threading.Thread | None = None
        self._stop_discovery = False
        
    def add_status_callback(self, callback: Callable[[str, ConnectionStatus], None]) -> None:
        """Add a callback for device status changes."""
        self.status_callbacks.append(callback)
    
    def add_data_callback(self, callback: Callable[[str, dict], None]) -> None:
        """Add a callback for received data."""
        self.data_callbacks.append(callback)
    
    def _notify_status_change(self, device_id: str, status: ConnectionStatus) -> None:
        """Notify all callbacks of status change."""
        for callback in self.status_callbacks:
            try:
                callback(device_id, status)
            except Exception as e:
                print(f"Error in status callback: {e}")
    
    def _notify_data_received(self, device_id: str, data: dict) -> None:
        """Notify all callbacks of received data."""
        for callback in self.data_callbacks:
            try:
                callback(device_id, data)
            except Exception as e:
                print(f"Error in data callback: {e}")
    
    def connect_device(self, ip_address: str, port: int = None) -> bool:
        """Connect to a device.
        
        Args:
            ip_address: Device IP address
            port: Device port (default from config)
            
        Returns:
            True if connection successful, False otherwise
        """
        if port is None:
            port = config.DEFAULT_PORT
            
        device_id = f"{ip_address}:{port}"
        
        # Check if already connected
        if device_id in self.connected_devices:
            if self.connected_devices[device_id].status == ConnectionStatus.CONNECTED:
                return True
        
        try:
            # Update status to connecting
            if device_id in self.connected_devices:
                self.connected_devices[device_id].status = ConnectionStatus.CONNECTING
            else:
                self.connected_devices[device_id] = DeviceInfo(
                    ip_address=ip_address,
                    port=port,
                    device_id=device_id,
                    manufacturer="Unknown",
                    model="Unknown",
                    serial="Unknown",
                    firmware="Unknown",
                    status=ConnectionStatus.CONNECTING
                )
            
            self._notify_status_change(device_id, ConnectionStatus.CONNECTING)
            
            # Create socket and connect (increase timeout for LR8450)
            sock = socket.create_connection((ip_address, port), timeout=10.0)
            sock.settimeout(10.0)  # Longer timeout for SCPI commands
            
            # Query device identification
            idn_response = self._query_device(sock, "*IDN?")
            if not idn_response:
                raise ValueError("No response to *IDN? query")
            
            # \u6309\u7167\u5b98\u65b9Sample\u793a\u4f8b\u7684\u521d\u59cb\u5316\u6d41\u7a0b
            # 1. \u53d1\u9001 *IDN? \u5df2\u5b8c\u6210
            # 2. \u8bbe\u7f6e header OFF (\u6309\u7167Sample3\u4f7f\u7528:HEAD OFF)
            print("Setting header OFF...")
            self._write_device(sock, ":HEAD OFF")
            
            # 3. \u6e05\u9664\u9519\u8bef
            print("Clearing errors...")
            self._write_device(sock, "*CLS")
            
            # Parse device information
            device_info = self.identifier.parse_idn_response(idn_response)
            
            # Check if device is supported
            if not device_info["protocol_compatible"]:
                raise ValueError(f"Unsupported device: {idn_response}")
            
            # Update device information
            self.connected_devices[device_id].manufacturer = device_info["display_manufacturer"]
            self.connected_devices[device_id].model = device_info["display_model"]
            self.connected_devices[device_id].serial = device_info["serial"]
            self.connected_devices[device_id].firmware = device_info["firmware"]
            self.connected_devices[device_id].status = ConnectionStatus.CONNECTED
            self.connected_devices[device_id].last_error = ""
            
            # Store socket
            self.sockets[device_id] = sock
            
            # Setup communication
            self._setup_device_communication(sock)
            
            self._notify_status_change(device_id, ConnectionStatus.CONNECTED)
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"Failed to connect to {ip_address}:{port} - {error_msg}")
            
            if device_id in self.connected_devices:
                self.connected_devices[device_id].status = ConnectionStatus.ERROR
                self.connected_devices[device_id].last_error = error_msg
            
            self._notify_status_change(device_id, ConnectionStatus.ERROR)
            return False
    
    def disconnect_device(self, device_id: str) -> bool:
        """Disconnect from a device.
        
        Args:
            device_id: Device identifier (ip:port)
            
        Returns:
            True if disconnection successful
        """
        try:
            if device_id in self.sockets:
                self.sockets[device_id].close()
                del self.sockets[device_id]
            
            if device_id in self.connected_devices:
                self.connected_devices[device_id].status = ConnectionStatus.DISCONNECTED
                self._notify_status_change(device_id, ConnectionStatus.DISCONNECTED)
            
            return True
            
        except Exception as e:
            print(f"Error disconnecting from {device_id}: {e}")
            return False
    
    def _query_device(self, sock: socket.socket, command: str) -> str:
        """Send a query command and receive response.
        
        Args:
            sock: Socket connection
            command: SCPI command to send
            
        Returns:
            Device response string
        """
        try:
            # Send command with debug output
            cmd_with_terminator = command + "\r\n"
            print(f">> Sending: {repr(command)}")

            # Try ASCII first, fall back to UTF-8 for Chinese characters
            try:
                sock.sendall(cmd_with_terminator.encode("ascii"))
            except UnicodeEncodeError:
                # For commands with Chinese characters, use UTF-8
                print(f"   Using UTF-8 encoding for non-ASCII characters")
                sock.sendall(cmd_with_terminator.encode("utf-8"))
            
            # Receive response byte by byte (like official VB.NET sample)
            response_bytes = []
            start_time = time.time()
            
            while time.time() - start_time < 10.0:  # 10 second timeout
                try:
                    # Check if data is available
                    sock.settimeout(0.1)  # Short timeout for individual reads
                    byte = sock.recv(1)
                    if not byte:
                        break
                    
                    char = byte.decode('ascii', errors='ignore')
                    if char == '\n':  # LF found, end of response
                        break
                    elif char == '\r':  # Skip CR
                        continue
                    else:
                        response_bytes.append(char)
                        
                except socket.timeout:
                    # Check if we have any data yet
                    if response_bytes:
                        continue  # Keep waiting for more data
                    else:
                        # No data received at all
                        break
                        
            response = ''.join(response_bytes)
            print(f"<< Received: {repr(response)}")
            return response
            
        except Exception as e:
            print(f"Query error for '{command}': {e}")
            return ""
    
    def _write_device(self, sock: socket.socket, command: str) -> bool:
        """Send a write command (no response expected).

        Args:
            sock: Socket connection
            command: SCPI command to send

        Returns:
            True if successful
        """
        try:
            cmd_with_terminator = command + "\r\n"
            print(f">> Sending (write): {repr(command)}")

            # Try ASCII first, fall back to UTF-8 for Chinese characters
            try:
                sock.sendall(cmd_with_terminator.encode("ascii"))
            except UnicodeEncodeError:
                # For commands with Chinese characters, use UTF-8
                print(f"   Using UTF-8 encoding for non-ASCII characters")
                sock.sendall(cmd_with_terminator.encode("utf-8"))

            return True
        except Exception as e:
            print(f"Write error for '{command}': {e}")
            return False
    
    def _setup_device_communication(self, sock: socket.socket) -> None:
        """Setup device communication parameters.
        
        Args:
            sock: Socket connection
        """
        try:
            # \u6839\u636eAPI\u6587\u6863\uff0c\u53ea\u9700\u8981\u5728\u8fde\u63a5\u65f6\u8bbe\u7f6e\u4e00\u6b21 header OFF
            # \u5df2\u7ecf\u5728 connect_device \u4e2d\u8bbe\u7f6e\u8fc7\u4e86\uff0c\u4e0d\u9700\u8981\u91cd\u590d
            pass
                
        except Exception as e:
            print(f"Device setup error: {e}")
    
    def send_command(self, device_id: str, command: str, expect_response: bool = True) -> str | bool:
        """Send a command to a connected device.
        
        Args:
            device_id: Device identifier
            command: SCPI command to send
            expect_response: Whether to expect a response
            
        Returns:
            Response string if expect_response=True, bool if expect_response=False
        """
        if device_id not in self.sockets:
            return "" if expect_response else False
        
        sock = self.sockets[device_id]
        
        if expect_response:
            return self._query_device(sock, command)
        else:
            return self._write_device(sock, command)
    
    def start_data_acquisition(self, device_id: str) -> bool:
        """Start data acquisition on a device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            True if successful
        """
        return bool(self.send_command(device_id, ":STARt", expect_response=False))
    
    def stop_data_acquisition(self, device_id: str) -> bool:
        """Stop data acquisition on a device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            True if successful
        """
        return bool(self.send_command(device_id, ":STOP", expect_response=False))
    
    def get_device_status(self, device_id: str) -> str:
        """Get device status.

        Args:
            device_id: Device identifier

        Returns:
            Status string
        """
        return self.send_command(device_id, ":STATus?", expect_response=True)

    def query_device(self, device_id: str, command: str) -> str:
        """Query a device with a command (convenience method).

        Args:
            device_id: Device identifier
            command: SCPI command to send

        Returns:
            Device response string
        """
        return self.send_command(device_id, command, expect_response=True)
    
    def discover_devices(self, ip_range: str = "192.168.1") -> None:
        """Start device discovery in background.
        
        Args:
            ip_range: IP range to scan (e.g., "192.168.1")
        """
        if self._discovery_thread and self._discovery_thread.is_alive():
            return
        
        self._stop_discovery = False
        self._discovery_thread = threading.Thread(
            target=self._discovery_worker,
            args=(ip_range,),
            daemon=True
        )
        self._discovery_thread.start()
    
    def stop_discovery(self) -> None:
        """Stop device discovery."""
        self._stop_discovery = True
        if self._discovery_thread:
            self._discovery_thread.join(timeout=1.0)
    
    def _discovery_worker(self, ip_range: str) -> None:
        """Worker function for device discovery.
        
        Args:
            ip_range: IP range to scan
        """
        for i in range(1, 255):
            if self._stop_discovery:
                break
                
            ip = f"{ip_range}.{i}"
            
            # Skip if already connected
            device_id = f"{ip}:{config.DEFAULT_PORT}"
            if device_id in self.connected_devices:
                if self.connected_devices[device_id].status == ConnectionStatus.CONNECTED:
                    continue
            
            # Quick connection test
            try:
                with socket.create_connection((ip, config.DEFAULT_PORT), timeout=0.5):
                    # Found a device - try full connection
                    print(f"Found device at {ip}")
                    # Note: Don't auto-connect here, just notify
                    
            except (socket.timeout, socket.error, ConnectionRefusedError):
                # No device at this IP
                pass
            
            # Small delay to avoid overwhelming the network
            time.sleep(0.01)
    
    def get_connected_devices(self) -> dict[str, DeviceInfo]:
        """Get all connected devices.
        
        Returns:
            Dictionary of device information
        """
        return self.connected_devices.copy()
    
    def cleanup(self) -> None:
        """Cleanup all connections and threads."""
        self.stop_discovery()
        
        # Close all connections
        for device_id in list(self.connected_devices.keys()):
            self.disconnect_device(device_id)
