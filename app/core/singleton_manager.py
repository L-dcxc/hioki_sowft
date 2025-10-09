# -*- coding: utf-8 -*-
"""Singleton pattern for shared device manager."""

from __future__ import annotations

from app.core.device_manager import DeviceManager


class DeviceManagerSingleton:
    """Singleton pattern for device manager to ensure single instance."""
    
    _instance: DeviceManager | None = None
    
    @classmethod
    def get_instance(cls) -> DeviceManager:
        """Get the singleton device manager instance."""
        if cls._instance is None:
            cls._instance = DeviceManager()
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        if cls._instance:
            cls._instance.cleanup()
        cls._instance = None

