# -*- coding: utf-8 -*-
"""Settings management for persistent configuration storage."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import logging


class SettingsManager:
    """Manages application settings persistence."""
    
    def __init__(self, config_dir: str = None):
        """Initialize settings manager.
        
        Args:
            config_dir: Directory to store configuration files
        """
        self.logger = logging.getLogger(__name__)
        
        if config_dir is None:
            # Use user's home directory for config
            config_dir = os.path.join(os.path.expanduser("~"), ".xunyu_xy2580")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.settings_file = self.config_dir / "settings.json"
        self.device_configs_file = self.config_dir / "device_configs.json"
        
        self._settings = self._load_settings()
        self._device_configs = self._load_device_configs()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load settings: {e}")
        
        # Return default settings
        return {
            "window": {
                "width": 1200,
                "height": 800,
                "maximized": False
            },
            "waveform": {
                "background_color": "#ffffff",
                "grid_enabled": True,
                "time_scale": "1s",
                "scale_count": 4
            },
            "acquisition": {
                "sample_rate": 1.0,
                "buffer_size": 1000,
                "auto_start": False
            }
        }
    
    def _load_device_configs(self) -> Dict[str, Any]:
        """Load device configurations from file."""
        try:
            if self.device_configs_file.exists():
                with open(self.device_configs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load device configs: {e}")
        
        return {}
    
    def save_settings(self) -> None:
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
    
    def save_device_configs(self) -> None:
        """Save device configurations to file."""
        try:
            with open(self.device_configs_file, 'w', encoding='utf-8') as f:
                json.dump(self._device_configs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save device configs: {e}")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value using dot notation.
        
        Args:
            key: Setting key (e.g., "window.width")
            default: Default value if key not found
            
        Returns:
            Setting value
        """
        keys = key.split('.')
        value = self._settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value using dot notation.
        
        Args:
            key: Setting key (e.g., "window.width")
            value: Value to set
        """
        keys = key.split('.')
        setting = self._settings
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
        
        # Set the final value
        setting[keys[-1]] = value
    
    def get_device_config(self, device_id: str) -> Dict[str, Any]:
        """Get configuration for a specific device.
        
        Args:
            device_id: Device identifier (e.g., IP address)
            
        Returns:
            Device configuration dictionary
        """
        return self._device_configs.get(device_id, {})
    
    def set_device_config(self, device_id: str, config: Dict[str, Any]) -> None:
        """Set configuration for a specific device.
        
        Args:
            device_id: Device identifier
            config: Configuration dictionary
        """
        self._device_configs[device_id] = config
    
    def get_channel_config(self, device_id: str) -> list:
        """Get channel configuration for a device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            List of channel configurations
        """
        device_config = self.get_device_config(device_id)
        return device_config.get('channels', [])
    
    def set_channel_config(self, device_id: str, channels: list) -> None:
        """Set channel configuration for a device.
        
        Args:
            device_id: Device identifier
            channels: List of channel configurations
        """
        if device_id not in self._device_configs:
            self._device_configs[device_id] = {}
        
        self._device_configs[device_id]['channels'] = channels
    
    def get_unit_config(self, device_id: str) -> Dict[str, Any]:
        """Get unit configuration for a device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            Unit configuration dictionary
        """
        device_config = self.get_device_config(device_id)
        return device_config.get('unit', {})
    
    def set_unit_config(self, device_id: str, unit_config: Dict[str, Any]) -> None:
        """Set unit configuration for a device.
        
        Args:
            device_id: Device identifier
            unit_config: Unit configuration dictionary
        """
        if device_id not in self._device_configs:
            self._device_configs[device_id] = {}
        
        self._device_configs[device_id]['unit'] = unit_config
    
    def get_measurement_config(self, device_id: str) -> Dict[str, Any]:
        """Get measurement configuration for a device.
        
        Args:
            device_id: Device identifier
            
        Returns:
            Measurement configuration dictionary
        """
        device_config = self.get_device_config(device_id)
        return device_config.get('measurement', {})
    
    def set_measurement_config(self, device_id: str, measurement_config: Dict[str, Any]) -> None:
        """Set measurement configuration for a device.
        
        Args:
            device_id: Device identifier
            measurement_config: Measurement configuration dictionary
        """
        if device_id not in self._device_configs:
            self._device_configs[device_id] = {}
        
        self._device_configs[device_id]['measurement'] = measurement_config


# Global settings manager instance
_settings_manager = None


def get_settings_manager() -> SettingsManager:
    """Get the global settings manager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
