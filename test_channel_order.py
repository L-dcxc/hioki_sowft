#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试通道数据读取顺序"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from battery_analyzer.core.lr8450_client import LR8450Client


def test_channel_order():
    """测试通道数据读取顺序"""
    
    print("=" * 80)
    print("通道数据读取顺序测试")
    print("=" * 80)
    
    # 连接设备
    ip = input("\n请输入设备IP地址 (默认: 192.168.2.44): ").strip() or "192.168.2.44"
    port = input("请输入端口 (默认: 8802): ").strip() or "8802"
    port = int(port)
    
    client = LR8450Client(
        connection_type="TCP",
        ip_address=ip,
        port=port
    )
    
    try:
        if not client.connect():
            print("❌ 连接失败")
            return
        
        print(f"✓ 连接成功: {ip}:{port}\n")
        
        # 启动采集
        print("启动采集...")
        client.write(":STARt")
        time.sleep(2)
        print("✓ 采集已启动\n")
        
        # 获取实时数据快照
        print("获取实时数据快照...")
        client.write(":MEMory:GETReal")
        time.sleep(0.5)
        print("✓ 快照已获取\n")
        
        # 逐个查询通道
        channels = ['CH1_1', 'CH1_2', 'CH1_3', 'CH1_4']
        
        print("=" * 80)
        print("逐个查询通道数据:")
        print("=" * 80)
        
        for ch in channels:
            response = client.query(f":MEMory:VREAL? {ch}")
            print(f"  查询 {ch} → 响应: {response}")
            time.sleep(0.1)
        
        print("\n" + "=" * 80)
        print("批量查询（不同顺序）:")
        print("=" * 80)
        
        # 测试1: 顺序 1,2,3,4
        print("\n【测试1】顺序: CH1_1, CH1_2, CH1_3, CH1_4")
        client.write(":MEMory:GETReal")
        time.sleep(0.5)
        data1 = {}
        for ch in ['CH1_1', 'CH1_2', 'CH1_3', 'CH1_4']:
            response = client.query(f":MEMory:VREAL? {ch}")
            if response and '9.99999' not in response:
                try:
                    data1[ch] = float(response)
                except:
                    pass
            time.sleep(0.05)
        print(f"  结果: {data1}")
        
        # 测试2: 顺序 2,1,3,4
        print("\n【测试2】顺序: CH1_2, CH1_1, CH1_3, CH1_4")
        client.write(":MEMory:GETReal")
        time.sleep(0.5)
        data2 = {}
        for ch in ['CH1_2', 'CH1_1', 'CH1_3', 'CH1_4']:
            response = client.query(f":MEMory:VREAL? {ch}")
            if response and '9.99999' not in response:
                try:
                    data2[ch] = float(response)
                except:
                    pass
            time.sleep(0.05)
        print(f"  结果: {data2}")
        
        # 测试3: 顺序 4,3,2,1
        print("\n【测试3】顺序: CH1_4, CH1_3, CH1_2, CH1_1")
        client.write(":MEMory:GETReal")
        time.sleep(0.5)
        data3 = {}
        for ch in ['CH1_4', 'CH1_3', 'CH1_2', 'CH1_1']:
            response = client.query(f":MEMory:VREAL? {ch}")
            if response and '9.99999' not in response:
                try:
                    data3[ch] = float(response)
                except:
                    pass
            time.sleep(0.05)
        print(f"  结果: {data3}")
        
        print("\n" + "=" * 80)
        print("对比分析:")
        print("=" * 80)
        print(f"  测试1: {data1}")
        print(f"  测试2: {data2}")
        print(f"  测试3: {data3}")
        
        # 停止采集
        print("\n停止采集...")
        client.write(":STOP")
        
    finally:
        client.disconnect()
        print("\n✓ 已断开连接")


if __name__ == "__main__":
    test_channel_order()

