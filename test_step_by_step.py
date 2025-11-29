#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一步步测试连接、读取、配置、采集"""

import sys
import time
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from battery_analyzer.core.lr8450_client import LR8450Client


def test_step_by_step():
    """一步步测试"""
    
    print("=" * 80)
    print("LR8450 逐步测试工具")
    print("=" * 80)
    
    # 步骤1：连接设备
    print("\n【步骤1】连接设备")
    print("-" * 80)
    
    ip = input("请输入设备IP地址 (默认: 192.168.2.44): ").strip() or "192.168.2.44"
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

        print(f"✓ 连接成功: {ip}:{port}")
        
        # 步骤2：读取设备信息
        print("\n【步骤2】读取设备信息")
        print("-" * 80)
        
        idn = client.query("*IDN?")
        print(f"设备信息: {idn}")
        
        # 步骤3：检测已安装的模块
        print("\n【步骤3】检测已安装的模块")
        print("-" * 80)

        installed_modules = []
        for unit in range(1, 5):
            unit_name = f"UNIT{unit}"
            response = client.query(f":UNIT:IDN? {unit_name}")

            if response and ',' in response and unit_name in response:
                # 解析模块信息
                parts = response.split(',')
                model = parts[1].strip() if len(parts) > 1 else "未知"
                print(f"  UNIT{unit}: {model} (响应: {response[:60]}...)")
                installed_modules.append(unit)
            else:
                print(f"  UNIT{unit}: 无模块 (响应: {response if response else '无'})")

        if not installed_modules:
            print("\n❌ 没有检测到任何模块")
            return

        print(f"\n✓ 已安装的模块: UNIT{installed_modules}")
        
        # 步骤4：选择要使用的模块
        print("\n【步骤4】选择要使用的模块")
        print("-" * 80)
        
        unit_num = input(f"请选择要使用的模块 (1-4, 默认: {installed_modules[0]}): ").strip()
        unit_num = int(unit_num) if unit_num else installed_modules[0]
        
        if unit_num not in installed_modules:
            print(f"⚠️ UNIT{unit_num} 未安装模块，但继续测试...")
        
        # 步骤5：配置通道
        print("\n【步骤5】配置通道")
        print("-" * 80)
        
        print(f"\n请配置4个通道 (UNIT{unit_num}):")
        print("  默认配置：CH1_1(温度), CH1_2(电压), CH1_3(电压), CH1_4(温度)")

        ch1 = input(f"  通道1 (三元电池温度, 默认: CH{unit_num}_1): ").strip() or f"CH{unit_num}_1"
        ch2 = input(f"  通道2 (三元电池电压, 默认: CH{unit_num}_2): ").strip() or f"CH{unit_num}_2"
        ch3 = input(f"  通道3 (刀片电池电压, 默认: CH{unit_num}_3): ").strip() or f"CH{unit_num}_3"
        ch4 = input(f"  通道4 (刀片电池温度, 默认: CH{unit_num}_4): ").strip() or f"CH{unit_num}_4"

        channels = [ch1, ch2, ch3, ch4]

        print(f"\n配置通道: {channels}")

        # 禁用所有通道
        print(f"\n禁用UNIT{unit_num}的所有通道...")
        for ch_num in range(1, 31):
            client.write(f":UNIT:STORe CH{unit_num}_{ch_num},OFF")
        time.sleep(0.5)  # 等待禁用完成
        print("✓ 已禁用所有通道")

        # 配置通道1 (温度)
        print(f"\n配置 {ch1} (温度, K型, 100°C)...")
        client.write(f":UNIT:STORe {ch1},ON")
        time.sleep(0.1)
        # 先设置测量模式为热电偶
        client.write(f":UNIT:INMOde {ch1},TC")
        time.sleep(0.1)
        # 再设置热电偶类型
        client.write(f":SCALing:UNIT {ch1},TC_K")
        time.sleep(0.1)
        # 设置量程
        client.write(f":UNIT:RANGe {ch1},100")
        time.sleep(0.1)
        # 设置参考类型
        client.write(f":SCALing:REFerence {ch1},INT")
        time.sleep(0.1)
        print(f"✓ {ch1} 配置完成")

        # 配置通道2 (电压)
        print(f"\n配置 {ch2} (电压, 20V)...")
        client.write(f":UNIT:STORe {ch2},ON")
        time.sleep(0.1)
        # 设置测量模式为电压
        client.write(f":UNIT:INMOde {ch2},VOLTAGE")
        time.sleep(0.1)
        # 设置量程
        client.write(f":UNIT:RANGe {ch2},20.0")
        time.sleep(0.1)
        print(f"✓ {ch2} 配置完成")

        # 配置通道3 (电压)
        print(f"\n配置 {ch3} (电压, 20V)...")
        client.write(f":UNIT:STORe {ch3},ON")
        time.sleep(0.1)
        # 设置测量模式为电压
        client.write(f":UNIT:INMOde {ch3},VOLTAGE")
        time.sleep(0.1)
        # 设置量程
        client.write(f":UNIT:RANGe {ch3},20.0")
        time.sleep(0.1)
        print(f"✓ {ch3} 配置完成")

        # 配置通道4 (温度)
        print(f"\n配置 {ch4} (温度, K型, 100°C)...")
        client.write(f":UNIT:STORe {ch4},ON")
        time.sleep(0.1)
        # 先设置测量模式为热电偶
        client.write(f":UNIT:INMOde {ch4},TC")
        time.sleep(0.1)
        # 再设置热电偶类型
        client.write(f":SCALing:UNIT {ch4},TC_K")
        time.sleep(0.1)
        # 设置量程
        client.write(f":UNIT:RANGe {ch4},100")
        time.sleep(0.1)
        # 设置参考类型
        client.write(f":SCALing:REFerence {ch4},INT")
        time.sleep(0.1)
        print(f"✓ {ch4} 配置完成")
        
        # 步骤6：启动采集
        print("\n【步骤6】启动采集")
        print("-" * 80)
        
        client.write(":STARt")
        print("✓ 已发送 :STARt 命令")
        
        print("等待设备准备数据...")
        time.sleep(2.0)
        
        # 步骤7：读取数据
        print("\n【步骤7】读取数据 (连续10次)")
        print("-" * 80)
        
        for i in range(10):
            print(f"\n第 {i+1} 次读取:")
            
            client.write(":MEMory:GETReal")
            time.sleep(0.3)
            
            for ch in channels:
                response = client.query(f":MEMory:VREAL? {ch}")
                
                if response and '9.99999' not in response:
                    try:
                        value = float(response)
                        print(f"  {ch}: {value}")
                    except ValueError:
                        print(f"  {ch}: 无效数据 ({response})")
                else:
                    print(f"  {ch}: 无数据")
            
            time.sleep(0.5)
        
        # 步骤8：停止采集
        print("\n【步骤8】停止采集")
        print("-" * 80)
        
        client.write(":STOP")
        print("✓ 已发送 :STOP 命令")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.disconnect()
        print("\n✓ 已断开连接")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == '__main__':
    test_step_by_step()

