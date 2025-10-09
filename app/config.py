"""Application configuration constants."""

from __future__ import annotations

# Display device information (what users see)
DEVICE_MANUFACTURER = "XUNYU"
DEVICE_MODEL = "XY2580"
DEVICE_FULL_NAME = f"{DEVICE_MANUFACTURER} {DEVICE_MODEL}"

# Internal device communication (actual hardware protocol)
INTERNAL_MANUFACTURER = "HIOKI"
INTERNAL_MODEL = "LR8450"
INTERNAL_MODEL_VARIANTS = ["LR8450", "LR8450-01"]

# Device identification mapping
DEVICE_ID_MAPPING = {
    # Map actual device responses to our display names
    "HIOKI,LR8450": {"manufacturer": DEVICE_MANUFACTURER, "model": DEVICE_MODEL},
    "HIOKI,LR8450-01": {"manufacturer": DEVICE_MANUFACTURER, "model": DEVICE_MODEL},
    # Add more mappings as needed
}

# Communication protocol settings
PROTOCOL_SETTINGS = {
    "use_internal_model_for_communication": True,  # Use HIOKI LR8450 for protocol
    "display_custom_model_in_ui": True,           # Show XUNYU XY2580 in UI
}

# Application information
APP_NAME = f"{DEVICE_MODEL} \u6570\u636e\u91c7\u96c6\u4e0e\u5206\u6790\u8f6f\u4ef6"
APP_VERSION = "1.0.0"
APP_BUILD_DATE = "2024-01-01"

# Company information
COMPANY_NAME = "\u5e7f\u5dde\u8baf\u5c7f\u79d1\u6280\u6709\u9650\u516c\u53f8"
COMPANY_PHONE = "020-31801362"
COMPANY_EMAIL = "xs@xunyutek.cn"
TECH_STACK = "jack chen"
LICENSE = "MIT License"

# File formats
SUPPORTED_EXTENSIONS = [".luw", ".lus", ".mem", ".csv"]

# Network configuration
DEFAULT_PORT = 8800
DEFAULT_IP_RANGE = "192.168.1.x"
DEFAULT_DEVICE_IP = "192.168.1.2"
DEFAULT_PC_IP = "192.168.1.1"

# UI configuration
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
MAX_TABLE_ROWS = 1000

# Data acquisition
MAX_DEVICES = 5
DEFAULT_SAMPLE_RATE = 100.0  # Hz
DEFAULT_RECORDING_DURATION = 10.0  # seconds

# File paths
TEST_DATA_DIR = "test_data"
DOCS_DIR = "docs"
CONFIG_DIR = "config"
