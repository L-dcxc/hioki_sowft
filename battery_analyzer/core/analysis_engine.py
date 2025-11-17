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
        self.mah_test_current = 1000.0  # mA
        self.mah_test_start_time = None
        self.mah_accumulated = 0.0
        
        # mX+b校准参数
        self.ternary_m = 1.0
        self.ternary_b = 0.0
        self.blade_m = 1.0
        self.blade_b = 0.0
    
    def add_data_point(self, ternary_voltage: float, ternary_temp: float,
                       blade_voltage: float, blade_temp: float,
                       timestamp: float = None):
        """添加一个数据点"""
        if timestamp is None:
            timestamp = time.time()
        
        # 应用mX+b校准
        ternary_voltage = ternary_voltage * self.ternary_m + self.ternary_b
        blade_voltage = blade_voltage * self.blade_m + self.blade_b
        
        self.ternary_data.voltage_data.append(ternary_voltage)
        self.ternary_data.temp_data.append(ternary_temp)
        self.ternary_data.timestamps.append(timestamp)
        
        self.blade_data.voltage_data.append(blade_voltage)
        self.blade_data.temp_data.append(blade_temp)
        self.blade_data.timestamps.append(timestamp)
    
    def clear_data(self):
        """清除所有数据"""
        self.ternary_data = BatteryTestData([], [], [])
        self.blade_data = BatteryTestData([], [], [])
        self.mah_test_start_time = None
        self.mah_accumulated = 0.0
    
    def set_mx_plus_b(self, battery_type: str, m: float, b: float):
        """设置mX+b校准参数
        
        Args:
            battery_type: "ternary" 或 "blade"
            m: 斜率
            b: 截距
        """
        if battery_type == "ternary":
            self.ternary_m = m
            self.ternary_b = b
        else:
            self.blade_m = m
            self.blade_b = b
    
    def start_mah_test(self, current_ma: float):
        """开始mAh容量测试
        
        Args:
            current_ma: 额定电流（mA）
        """
        self.mah_test_current = current_ma
        self.mah_test_start_time = time.time()
        self.mah_accumulated = 0.0
    
    def update_mah_capacity(self) -> float:
        """更新并返回当前容量（mAh）"""
        if self.mah_test_start_time is None:
            return 0.0
        
        elapsed_hours = (time.time() - self.mah_test_start_time) / 3600.0
        self.mah_accumulated = self.mah_test_current * elapsed_hours
        return self.mah_accumulated
    
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
            '测试时长': (time.time() - self.ternary_data.timestamps[0]) if self.ternary_data.timestamps else 0,
        }




