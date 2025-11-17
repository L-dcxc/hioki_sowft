# -*- coding: utf-8 -*-
"""
Simple device client based on official LR8450 samples
This implements a connection-per-command approach to avoid connection drops
"""

import socket
import time
import logging
from typing import Optional, Dict, Any


class SimpleDeviceClient:
    """Simple device client that creates new connection for each command."""
    
    def __init__(self, ip_address: str, port: int = 8802):
        """Initialize device client.
        
        Args:
            ip_address: Device IP address
            port: Device port
        """
        self.ip_address = ip_address
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.timeout = 5.0
        
    def send_query(self, command: str) -> Optional[str]:
        """Send a query command and get response.
        
        Args:
            command: SCPI command to send
            
        Returns:
            Response string or None if failed
        """
        sock = None
        try:
            # Create new connection for each command
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.ip_address, self.port))
            
            # Send command
            cmd_with_terminator = command + "\r\n"
            print(f">> {command}")
            sock.sendall(cmd_with_terminator.encode("ascii"))
            
            # Receive response (byte by byte like official sample)
            response_bytes = []
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                try:
                    sock.settimeout(0.1)
                    byte = sock.recv(1)
                    if not byte:
                        break
                    
                    char = byte.decode('ascii', errors='ignore')
                    if char == '\n':  # LF found
                        break
                    elif char == '\r':  # Skip CR
                        continue
                    else:
                        response_bytes.append(char)
                        
                except socket.timeout:
                    if response_bytes:
                        continue  # Keep waiting
                    else:
                        break  # No data received
                        
            response = ''.join(response_bytes)
            print(f"<< {response}")
            return response if response else None
            
        except Exception as e:
            print(f"Query error for '{command}': {e}")
            return None
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass
    
    def send_command(self, command: str) -> bool:
        """Send a command without expecting response.
        
        Args:
            command: SCPI command to send
            
        Returns:
            True if successful
        """
        sock = None
        try:
            # Create new connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.ip_address, self.port))
            
            # Send command
            cmd_with_terminator = command + "\r\n"
            print(f">> {command} (write)")
            sock.sendall(cmd_with_terminator.encode("ascii"))
            
            return True
            
        except Exception as e:
            print(f"Write error for '{command}': {e}")
            return False
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass
    
    def get_device_info(self) -> Optional[Dict[str, Any]]:
        """Get basic device information.
        
        Returns:
            Device info dictionary or None if failed
        """
        idn_response = self.send_query("*IDN?")
        if not idn_response:
            return None
            
        try:
            # 判断IDN格式：标准SCPI格式 vs HIOKI扩展格式
            if ',' in idn_response:
                # 标准SCPI格式（8802端口）: "HIOKI,LR8450-01,221018368,V2.10"
                parts = idn_response.split(',')
                manufacturer = parts[0].strip()  # "HIOKI"
                model = parts[1].strip()          # "LR8450-01"
                serial = parts[2].strip()         # "221018368"
                firmware = parts[3].strip()       # "V2.10"
                
                return {
                    "manufacturer": manufacturer,
                    "model": model,
                    "serial": serial,
                    "firmware": firmware,
                    "unit_info": [],  # 标准格式不包含单元信息
                    "estimated_channels": 60,  # 默认估算
                    "raw_idn": idn_response,
                    "port_type": "8802_SCPI"
                }
            else:
                # HIOKI扩展格式（8800端口）: "HIOKI 8450 V2.10 1.01 U1-A U2-4 ..."
                parts = idn_response.split()
                if len(parts) >= 3:
                    manufacturer = parts[0]  # "HIOKI"
                    model = parts[1]         # "8450"
                    firmware = parts[2]      # "V2.10"
                    
                    # Extract unit information
                    unit_info = []
                    estimated_channels = 0
                    
                    for part in parts[4:]:
                        if part.startswith('U') and '-' in part:
                            unit_info.append(part)
                            try:
                                unit_type = part.split('-')[1]
                                if unit_type == 'A':
                                    estimated_channels += 15
                                elif unit_type.isdigit():
                                    estimated_channels += int(unit_type)
                                elif unit_type == 'B':
                                    estimated_channels += 4
                            except:
                                pass
                        elif part == "DUMMY":
                            break
                    
                    return {
                        "manufacturer": manufacturer,
                        "model": f"LR{model}",
                        "firmware": firmware,
                        "unit_info": unit_info,
                        "estimated_channels": max(estimated_channels, 30),
                        "raw_idn": idn_response,
                        "port_type": "8800_INFO"
                    }
                
        except Exception as e:
            print(f"Error parsing device info: {e}")
            
        return None
    
    def test_basic_commands(self) -> Dict[str, Any]:
        """Test basic SCPI commands to see what works.
        
        Returns:
            Dictionary of test results
        """
        results = {}
        
        # Test basic queries
        test_queries = [
            "*ESR?",
            ":STATus?", 
            ":MEMORY:MAXPOINT?",
        ]
        
        for cmd in test_queries:
            response = self.send_query(cmd)
            results[cmd] = {
                "success": response is not None,
                "response": response
            }
            time.sleep(0.5)  # Wait between commands
        
        # Test basic commands
        test_commands = [
            ":HEAD OFF",
            "*CLS",
        ]
        
        for cmd in test_commands:
            success = self.send_command(cmd)
            results[cmd] = {
                "success": success,
                "response": None
            }
            time.sleep(0.5)
            
        return results
    
    def get_real_time_data_simple(self) -> Optional[Dict[str, float]]:
        """Get real-time data using the simplest possible approach.
        
        Returns:
            Dictionary of channel data or None if failed
        """
        try:
            # Try the official Sample3 approach
            # Step 1: Get real-time snapshot
            if not self.send_command(":MEM:GETREAL"):
                print("Failed to get real-time snapshot")
                return None
            
            # Step 2: Query a single channel to test
            response = self.send_query(":MEM:VREAL? CH1_1")
            if response:
                try:
                    value = float(response.strip())
                    return {"CH1_1": value}
                except ValueError:
                    print(f"Could not parse channel data: {response}")
                    
        except Exception as e:
            print(f"Real-time data error: {e}")
            
        return None
