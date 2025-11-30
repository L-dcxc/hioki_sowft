#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""电池测试分析引擎"""

from __future__ import annotations

import time
from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class BatteryTestData:
    """电池测试数据"""
    voltage_data: List[float]  # 电压数据
    temp_data: List[float]     # 温度数据
    timestamps: List[float]    # 时间戳
    
    def get_temp_rise(self) -> Dict[str, float]:
        """计算温升数据"""
        if not self.temp_data:
            return {}
        
        return {
            '初始温度': self.temp_data[0],
            '当前温度': self.temp_data[-1],
            '峰值温度': max(self.temp_data),
            '最低温度': min(self.temp_data),
            '温升': max(self.temp_data) - self.temp_data[0],
            '平均温度': np.mean(self.temp_data),
        }
    
    def get_voltage_drop(self) -> Dict[str, float]:
        """计算电压压降数据"""
        if not self.voltage_data:
            return {}
        
        v_start = self.voltage_data[0]
        v_current = self.voltage_data[-1]
        v_drop = v_start - v_current
        
        return {
            '初始电压': v_start,
            '当前电压': v_current,
            '最高电压': max(self.voltage_data),
            '最低电压': min(self.voltage_data),
            '电压降': v_drop,
            '压降率': (v_drop / v_start * 100) if v_start != 0 else 0,
            '平均电压': np.mean(self.voltage_data),
        }


class BatteryAnalysisEngine:
    """电池分析引擎"""

    def __init__(self):
        self.ternary_data = BatteryTestData([], [], [])
        self.blade_data = BatteryTestData([], [], [])

        # mAh测试参数
        self.mah_test_current = 1000.0  # mA（恒流测试电流）
        self.mah_test_active = False    # 是否正在进行mAh测试
        self.mah_test_start_index = 0   # 测试开始时的数据点索引
        self.mah_test_channel = "ternary"  # 测试通道
        self.mah_accumulated = 0.0      # 累计容量
        self.mah_last_update_index = 0  # 上次更新时的数据点索引

        # mX+b校准参数 - 电压校准
        self.ternary_voltage_m = 1.0
        self.ternary_voltage_b = 0.0
        self.blade_voltage_m = 1.0
        self.blade_voltage_b = 0.0

        # mX+b校准参数 - 温度校准
        self.ternary_temp_m = 1.0
        self.ternary_temp_b = 0.0
        self.blade_temp_m = 1.0
        self.blade_temp_b = 0.0

    def apply_calibration(self, battery_type: str, data_type: str, value: float) -> float:
        """应用mX+b校准

        Args:
            battery_type: "ternary" 或 "blade"
            data_type: "voltage" 或 "temp"
            value: 原始值

        Returns:
            校准后的值
        """
        if battery_type == "ternary":
            if data_type == "voltage":
                return value * self.ternary_voltage_m + self.ternary_voltage_b
            else:
                return value * self.ternary_temp_m + self.ternary_temp_b
        else:
            if data_type == "voltage":
                return value * self.blade_voltage_m + self.blade_voltage_b
            else:
                return value * self.blade_temp_m + self.blade_temp_b

    def add_data_point(self, ternary_voltage: float, ternary_temp: float,
                       blade_voltage: float, blade_temp: float,
                       timestamp: float = None):
        """添加一个数据点（数据已经过校准）"""
        if timestamp is None:
            timestamp = time.time()

        self.ternary_data.voltage_data.append(ternary_voltage)
        self.ternary_data.temp_data.append(ternary_temp)
        self.ternary_data.timestamps.append(timestamp)

        self.blade_data.voltage_data.append(blade_voltage)
        self.blade_data.temp_data.append(blade_temp)
        self.blade_data.timestamps.append(timestamp)

        # 如果mAh测试正在进行，自动更新容量
        if self.mah_test_active:
            self._update_capacity_from_data()

    def _update_capacity_from_data(self):
        """根据实际采集的数据更新容量（使用恒流假设）"""
        data = self.ternary_data if self.mah_test_channel == "ternary" else self.blade_data
        current_index = len(data.timestamps)

        if current_index <= self.mah_last_update_index:
            return

        # 计算从上次更新到现在的时间间隔（秒）
        if current_index >= 2 and self.mah_last_update_index >= 1:
            # 使用最近两个数据点的时间差
            dt = data.timestamps[-1] - data.timestamps[-2]
        elif len(data.timestamps) >= 2:
            # 使用平均间隔
            dt = (data.timestamps[-1] - data.timestamps[0]) / (len(data.timestamps) - 1)
        else:
            dt = 0.1  # 默认100ms

        # 容量 = 电流(mA) × 时间(小时)
        # 累加增量
        delta_capacity = self.mah_test_current * (dt / 3600.0)
        self.mah_accumulated += delta_capacity
        self.mah_last_update_index = current_index

    def clear_data(self):
        """清除所有数据"""
        self.ternary_data = BatteryTestData([], [], [])
        self.blade_data = BatteryTestData([], [], [])
        self.mah_test_active = False
        self.mah_accumulated = 0.0
        self.mah_last_update_index = 0

    def set_mx_plus_b(self, battery_type: str, data_type: str, m: float, b: float):
        """设置mX+b校准参数

        Args:
            battery_type: "ternary" 或 "blade"
            data_type: "voltage" 或 "temp"
            m: 斜率
            b: 截距
        """
        if battery_type == "ternary":
            if data_type == "voltage":
                self.ternary_voltage_m = m
                self.ternary_voltage_b = b
            else:
                self.ternary_temp_m = m
                self.ternary_temp_b = b
        else:
            if data_type == "voltage":
                self.blade_voltage_m = m
                self.blade_voltage_b = b
            else:
                self.blade_temp_m = m
                self.blade_temp_b = b

    def get_calibration_params(self) -> Dict:
        """获取所有校准参数"""
        return {
            'ternary_voltage': {'m': self.ternary_voltage_m, 'b': self.ternary_voltage_b},
            'ternary_temp': {'m': self.ternary_temp_m, 'b': self.ternary_temp_b},
            'blade_voltage': {'m': self.blade_voltage_m, 'b': self.blade_voltage_b},
            'blade_temp': {'m': self.blade_temp_m, 'b': self.blade_temp_b},
        }

    def set_calibration_params(self, params: Dict):
        """设置所有校准参数"""
        if 'ternary_voltage' in params:
            self.ternary_voltage_m = params['ternary_voltage'].get('m', 1.0)
            self.ternary_voltage_b = params['ternary_voltage'].get('b', 0.0)
        if 'ternary_temp' in params:
            self.ternary_temp_m = params['ternary_temp'].get('m', 1.0)
            self.ternary_temp_b = params['ternary_temp'].get('b', 0.0)
        if 'blade_voltage' in params:
            self.blade_voltage_m = params['blade_voltage'].get('m', 1.0)
            self.blade_voltage_b = params['blade_voltage'].get('b', 0.0)
        if 'blade_temp' in params:
            self.blade_temp_m = params['blade_temp'].get('m', 1.0)
            self.blade_temp_b = params['blade_temp'].get('b', 0.0)

    def start_mah_test(self, current_ma: float, channel: str = "ternary"):
        """开始mAh容量测试（基于实际采集数据的恒流测试）

        Args:
            current_ma: 恒流测试电流（mA）
            channel: 测试通道 "ternary" 或 "blade"
        """
        self.mah_test_current = current_ma
        self.mah_test_active = True
        self.mah_test_channel = channel
        self.mah_accumulated = 0.0

        # 记录开始时的数据点索引
        data = self.ternary_data if channel == "ternary" else self.blade_data
        self.mah_test_start_index = len(data.timestamps)
        self.mah_last_update_index = self.mah_test_start_index

    def stop_mah_test(self) -> float:
        """停止mAh容量测试

        Returns:
            最终累计容量 (mAh)
        """
        self.mah_test_active = False
        return self.mah_accumulated

    def get_mah_capacity(self) -> float:
        """获取当前累计容量（mAh）"""
        return self.mah_accumulated

    def get_mah_test_info(self) -> Dict:
        """获取mAh测试信息"""
        data = self.ternary_data if self.mah_test_channel == "ternary" else self.blade_data

        if not data.timestamps:
            elapsed_time = 0.0
            current_voltage = 0.0
        else:
            if self.mah_test_start_index < len(data.timestamps):
                elapsed_time = data.timestamps[-1] - data.timestamps[self.mah_test_start_index]
            else:
                elapsed_time = 0.0
            current_voltage = data.voltage_data[-1] if data.voltage_data else 0.0

        return {
            'active': self.mah_test_active,
            'current_ma': self.mah_test_current,
            'capacity_mah': self.mah_accumulated,
            'elapsed_time': elapsed_time,
            'current_voltage': current_voltage,
            'channel': self.mah_test_channel,
            'data_points': len(data.timestamps) - self.mah_test_start_index,
        }
    
    def compare_temp_rise(self) -> Dict[str, any]:
        """对比温升"""
        ternary_rise = self.ternary_data.get_temp_rise()
        blade_rise = self.blade_data.get_temp_rise()
        
        if not ternary_rise or not blade_rise:
            return {}
        
        return {
            '三元电池': ternary_rise,
            '刀片电池': blade_rise,
            '对比': {
                '温升差异': ternary_rise['温升'] - blade_rise['温升'],
                '三元温升': ternary_rise['温升'],
                '刀片温升': blade_rise['温升'],
                '优势电池': '刀片电池' if blade_rise['温升'] < ternary_rise['温升'] else '三元电池',
            }
        }
    
    def analyze_voltage_drop(self, battery_type: str) -> Dict[str, float]:
        """分析电压压降
        
        Args:
            battery_type: "ternary" 或 "blade"
        """
        data = self.ternary_data if battery_type == "ternary" else self.blade_data
        return data.get_voltage_drop()
    
    def generate_report_data(self) -> Dict[str, any]:
        """生成报告数据"""
        # 计算测试时长（使用相对时间戳：最后一个 - 第一个）
        if len(self.ternary_data.timestamps) >= 2:
            test_duration = self.ternary_data.timestamps[-1] - self.ternary_data.timestamps[0]
        elif len(self.ternary_data.timestamps) == 1:
            test_duration = 0.0
        else:
            test_duration = 0.0

        return {
            '三元电池': {
                '温升分析': self.ternary_data.get_temp_rise(),
                '压降分析': self.ternary_data.get_voltage_drop(),
            },
            '刀片电池': {
                '温升分析': self.blade_data.get_temp_rise(),
                '压降分析': self.blade_data.get_voltage_drop(),
            },
            '对比分析': self.compare_temp_rise(),
            'mAh容量': self.mah_accumulated,
            '测试时长': test_duration,
            '数据点数': len(self.ternary_data.timestamps),
        }




