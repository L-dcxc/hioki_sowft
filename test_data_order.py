#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试数据读取顺序问题"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from battery_analyzer.core.lr8450_client import LR8450Client


def test_data_order():
    """测试数据读取顺序"""
    
    print("=" * 80)
    print("数据读取顺序测试")
    print("=" * 80)
    
    # 连接设备
    ip = "192.168.2.44"
    port = 8802
    
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
        
        # 停止采集
        print("停止采集...")
        client.write(":STOP")
        time.sleep(0.5)
        
        # 禁用所有通道
        print("禁用所有通道...")
        for ch_num in range(1, 31):
            client.write(f":UNIT:STORe CH1_{ch_num},OFF")
        time.sleep(0.5)
        print("✓ 已禁用所有通道\n")
        
        # 按顺序配置通道：CH1_1, CH1_2, CH1_3, CH1_4
        print("=" * 80)
        print("配置通道（顺序：CH1_1, CH1_2, CH1_3, CH1_4）")
        print("=" * 80)
        
        # CH1_1: 温度
        print("\n配置 CH1_1 (温度, K型, 100°C)...")
        client.write(":UNIT:STORe CH1_1,ON")
        time.sleep(0.1)
        client.write(":UNIT:INMOde CH1_1,TC")
        time.sleep(0.1)
        client.write(":SCALing:UNIT CH1_1,TC_K")
        time.sleep(0.1)
        client.write(":UNIT:RANGe CH1_1,100")
        time.sleep(0.1)
        client.write(":SCALing:REFerence CH1_1,INT")
        time.sleep(0.1)
        print("✓ CH1_1 配置完成")
        
        # CH1_2: 电压
        print("\n配置 CH1_2 (电压, 20V)...")
        client.write(":UNIT:STORe CH1_2,ON")
        time.sleep(0.1)
        client.write(":UNIT:INMOde CH1_2,VOLTAGE")
        time.sleep(0.1)
        client.write(":UNIT:RANGe CH1_2,20.0")
        time.sleep(0.1)
        print("✓ CH1_2 配置完成")
        
        # CH1_3: 电压
        print("\n配置 CH1_3 (电压, 20V)...")
        client.write(":UNIT:STORe CH1_3,ON")
        time.sleep(0.1)
        client.write(":UNIT:INMOde CH1_3,VOLTAGE")
        time.sleep(0.1)
        client.write(":UNIT:RANGe CH1_3,20.0")
        time.sleep(0.1)
        print("✓ CH1_3 配置完成")
        
        # CH1_4: 温度
        print("\n配置 CH1_4 (温度, K型, 100°C)...")
        client.write(":UNIT:STORe CH1_4,ON")
        time.sleep(0.1)
        client.write(":UNIT:INMOde CH1_4,TC")
        time.sleep(0.1)
        client.write(":SCALing:UNIT CH1_4,TC_K")
        time.sleep(0.1)
        client.write(":UNIT:RANGe CH1_4,100")
        time.sleep(0.1)
        client.write(":SCALing:REFerence CH1_4,INT")
        time.sleep(0.1)
        print("✓ CH1_4 配置完成")
        
        # 启动采集
        print("\n" + "=" * 80)
        print("启动采集")
        print("=" * 80)
        client.write(":STARt")
        time.sleep(2)
        print("✓ 采集已启动\n")
        
        # 读取数据（多次）
        print("=" * 80)
        print("读取数据（10次）")
        print("=" * 80)
        
        for i in range(10):
            print(f"\n第 {i+1} 次读取:")
            
            # 获取实时数据快照
            client.write(":MEMory:GETReal")
            time.sleep(0.3)
            
            # 按顺序读取
            data = {}
            for ch in ['CH1_1', 'CH1_2', 'CH1_3', 'CH1_4']:
                response = client.query(f":MEMory:VREAL? {ch}")
                if response and '9.99999' not in response:
                    try:
                        data[ch] = float(response)
                    except:
                        pass
                time.sleep(0.05)
            
            print(f"  数据: {data}")
            
            # 分析数据
            if len(data) == 4:
                print(f"  CH1_1 (温度): {data.get('CH1_1', 'N/A')}")
                print(f"  CH1_2 (电压): {data.get('CH1_2', 'N/A')}")
                print(f"  CH1_3 (电压): {data.get('CH1_3', 'N/A')}")
                print(f"  CH1_4 (温度): {data.get('CH1_4', 'N/A')}")
            
            time.sleep(0.5)
        
        # 停止采集
        print("\n" + "=" * 80)
        print("停止采集")
        print("=" * 80)
        client.write(":STOP")
        
    finally:
        client.disconnect()
        print("\n✓ 已断开连接")


if __name__ == "__main__":
    test_data_order()

