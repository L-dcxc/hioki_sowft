"""Device identification and model mapping utilities."""

from __future__ import annotations

import re
from typing import Any

from app import config


class DeviceIdentifier:
    """Handle device identification and model mapping."""
    
    def __init__(self) -> None:
        """Initialize the device identifier."""
        self.mapping = config.DEVICE_ID_MAPPING
        self.protocol_settings = config.PROTOCOL_SETTINGS
    
    def parse_idn_response(self, idn_response: str) -> dict[str, Any]:
        """Parse *IDN? response and map to display model.
        
        Args:
            idn_response: Response from *IDN? command
            
        Returns:
            Dictionary with device information for display
            
        Example:
            Input: "HIOKI,LR8450,123456,1.00"
            Output: {
                "display_manufacturer": "XUNYU",
                "display_model": "XY2580", 
                "internal_manufacturer": "HIOKI",
                "internal_model": "LR8450",
                "serial": "123456",
                "firmware": "1.00",
                "protocol_compatible": True
            }
        """
        # Parse IDN format - support both standard SCPI and HIOKI custom format
        if ',' in idn_response:
            # Standard SCPI format: "manufacturer,model,serial,firmware"
            parts = [part.strip() for part in idn_response.split(',')]
            internal_manufacturer = parts[0]
            internal_model = parts[1] 
            serial = parts[2] if len(parts) > 2 else "Unknown"
            firmware = parts[3] if len(parts) > 3 else "Unknown"
        else:
            # HIOKI custom format: "HIOKI 8450    V2.10    1.01 ..."
            parts = idn_response.split()
            if len(parts) < 3:
                raise ValueError(f"Invalid IDN response format: {idn_response}")
            
            internal_manufacturer = parts[0]  # "HIOKI"
            internal_model = f"LR{parts[1]}"  # "LR8450" from "8450"
            firmware = parts[2] if len(parts) > 2 else "Unknown"  # "V2.10"
            # Extract detailed information from HIOKI response
            # Parse unit configuration: U1-A, U2-4, etc.
            unit_info = []
            status_info = {}
            estimated_channels = 0
            
            for part in parts[4:]:  # Skip manufacturer, model, firmware, version
                if part.startswith('U') and '-' in part:
                    unit_info.append(part)
                    # Calculate channels: U1-A (analog=15ch), U2-4 (4ch), etc.
                    try:
                        unit_type = part.split('-')[1]
                        if unit_type == 'A':
                            estimated_channels += 15  # Analog module
                        elif unit_type.isdigit():
                            estimated_channels += int(unit_type)
                        elif unit_type == 'B':
                            estimated_channels += 4  # Base module
                    except:
                        pass
                elif '-' in part and any(part.startswith(prefix) for prefix in ['STT', 'PCC', 'PCK', 'PCS']):
                    try:
                        key, value = part.split('-', 1)
                        status_info[key] = value
                    except:
                        pass
                elif part == "DUMMY":
                    break
            
            # Use status info for serial number
            serial = status_info.get('STT', f"LR8450_{parts[1]}_{firmware}")
            
            # Store additional info for later use
            additional_info = {
                "unit_info": unit_info,
                "status_info": status_info,
                "estimated_channels": max(estimated_channels, 30),
                "raw_response": idn_response
            }
        
        # Create mapping key
        mapping_key = f"{internal_manufacturer},{internal_model}"
        
        # Check if we have a mapping for this device
        if mapping_key in self.mapping:
            mapped_info = self.mapping[mapping_key]
            display_manufacturer = mapped_info["manufacturer"]
            display_model = mapped_info["model"]
            protocol_compatible = True
        else:
            # Unknown device - use actual values
            display_manufacturer = internal_manufacturer
            display_model = internal_model
            protocol_compatible = False
        
        result = {
            "display_manufacturer": display_manufacturer,
            "display_model": display_model,
            "display_full_name": f"{display_manufacturer} {display_model}",
            "internal_manufacturer": internal_manufacturer,
            "internal_model": internal_model,
            "internal_full_name": f"{internal_manufacturer} {internal_model}",
            "serial": serial,
            "firmware": firmware,
            "protocol_compatible": protocol_compatible,
            "raw_idn": idn_response
        }
        
        # Add additional info if available (from HIOKI format)
        if 'additional_info' in locals():
            result.update(additional_info)
            
        return result
    
    def is_supported_device(self, idn_response: str) -> bool:
        """Check if the device is supported by this software.
        
        Args:
            idn_response: Response from *IDN? command
            
        Returns:
            True if device is supported, False otherwise
        """
        try:
            device_info = self.parse_idn_response(idn_response)
            return device_info["protocol_compatible"]
        except (ValueError, KeyError):
            return False
    
    def get_protocol_model(self) -> str:
        """Get the model name to use for protocol communication.
        
        Returns:
            Model name for internal communication
        """
        if self.protocol_settings["use_internal_model_for_communication"]:
            return config.INTERNAL_MODEL
        else:
            return config.DEVICE_MODEL
    
    def get_display_model(self) -> str:
        """Get the model name to display in UI.
        
        Returns:
            Model name for UI display
        """
        if self.protocol_settings["display_custom_model_in_ui"]:
            return config.DEVICE_MODEL
        else:
            return config.INTERNAL_MODEL
    
    def should_use_internal_protocol(self, device_info: dict[str, Any]) -> bool:
        """Determine if we should use internal protocol for this device.
        
        Args:
            device_info: Device information from parse_idn_response
            
        Returns:
            True if should use internal protocol, False otherwise
        """
        return device_info.get("protocol_compatible", False)
    
    def format_device_display_name(self, device_info: dict[str, Any]) -> str:
        """Format device name for display in UI.
        
        Args:
            device_info: Device information from parse_idn_response
            
        Returns:
            Formatted device name for display
        """
        if self.protocol_settings["display_custom_model_in_ui"] and device_info["protocol_compatible"]:
            return f"{device_info['display_manufacturer']} {device_info['display_model']}"
        else:
            return f"{device_info['internal_manufacturer']} {device_info['internal_model']}"
    
    def get_communication_commands(self, device_info: dict[str, Any]) -> dict[str, str]:
        """Get appropriate commands for device communication.
        
        Args:
            device_info: Device information from parse_idn_response
            
        Returns:
            Dictionary of commands to use for this device
        """
        # For now, all supported devices use the same SCPI commands
        # This could be extended to support different command sets
        return {
            "start": ":STARt",
            "stop": ":STOP",
            "get_real": ":MEMory:GETReal",
            "fetch_binary": ":MEMory:BFETch?",
            "fetch_ascii": ":MEMory:AFETch?",
            "error_query": ":ERRor?",
            "status_query": ":STATus?",
        }
