#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试配置文件和通道映射"""

import json
import os

def main():
    config_file = os.path.expanduser('~/.battery_analyzer/app_config.json')
    
    print("=" * 80)
    print("配置文件诊断工具")
    print("=" * 80)
    
    if not os.path.exists(config_file):
        print(f"\n❌ 配置文件不存在: {config_file}")
        print("\n建议：")
        print("  1. 启动程序")
        print("  2. 点击'配置通道'按钮")
        print("  3. 配置正确的通道参数")
        print("  4. 保存配置")
        print("  5. 重新运行此脚本")
        return
    
    print(f"\n✓ 配置文件存在: {config_file}\n")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("📋 完整配置内容:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("\n" + "=" * 80)
    
    # 检查通道配置
    if 'channel_config' in config:
        channel_config = config['channel_config']
        
        print("\n🔍 通道配置详细分析:")
        print("-" * 80)
        
        for battery_name, battery_type in [
            ('ternary_voltage', '三元电池电压'),
            ('ternary_temp', '三元电池温度'),
            ('blade_voltage', '刀片电池电压'),
            ('blade_temp', '刀片电池温度')
        ]:
            if battery_name in channel_config:
                cfg = channel_config[battery_name]
                print(f"\n{battery_type}:")
                print(f"  通道: {cfg.get('channel', '未设置')}")
                print(f"  类型: {cfg.get('type', '❌ 缺失')}")
                print(f"  量程: {cfg.get('range', '未设置')}")
                
                if 'temp' in battery_name:
                    print(f"  热电偶: {cfg.get('thermocouple', '未设置')}")
                    print(f"  参考: {cfg.get('int_ext', '未设置')}")
                
                # 检查问题
                if 'type' not in cfg:
                    print(f"  ⚠️ 警告: 缺少 'type' 字段！")
                elif cfg['type'] not in ['VOLTAGE', 'TEMPERATURE']:
                    print(f"  ⚠️ 警告: 'type' 字段值错误: {cfg['type']}")
                elif 'temp' in battery_name and cfg['type'] != 'TEMPERATURE':
                    print(f"  ❌ 错误: 温度通道的 'type' 应该是 'TEMPERATURE'，但实际是 '{cfg['type']}'")
                elif 'voltage' in battery_name and cfg['type'] != 'VOLTAGE':
                    print(f"  ❌ 错误: 电压通道的 'type' 应该是 'VOLTAGE'，但实际是 '{cfg['type']}'")
                else:
                    print(f"  ✓ 类型配置正确")
        
        print("\n" + "-" * 80)
        
        # 检查通道重复
        channels = [
            channel_config.get('ternary_voltage', {}).get('channel'),
            channel_config.get('ternary_temp', {}).get('channel'),
            channel_config.get('blade_voltage', {}).get('channel'),
            channel_config.get('blade_temp', {}).get('channel'),
        ]
        
        print("\n🔍 通道重复检查:")
        if len(set(channels)) != len(channels):
            print("  ❌ 发现重复通道:")
            for ch in channels:
                if channels.count(ch) > 1:
                    print(f"    • {ch} 被使用了 {channels.count(ch)} 次")
        else:
            print("  ✓ 没有重复通道")
        
        # 显示通道映射
        print("\n📊 通道映射关系:")
        print("  三元电池电压 ← " + channel_config.get('ternary_voltage', {}).get('channel', '未设置'))
        print("  三元电池温度 ← " + channel_config.get('ternary_temp', {}).get('channel', '未设置'))
        print("  刀片电池电压 ← " + channel_config.get('blade_voltage', {}).get('channel', '未设置'))
        print("  刀片电池温度 ← " + channel_config.get('blade_temp', {}).get('channel', '未设置'))
    
    else:
        print("\n❌ 配置文件中没有 'channel_config' 字段")
    
    # 检查连接配置
    if 'connection' in config:
        conn = config['connection']
        print("\n🔌 连接配置:")
        print(f"  IP地址: {conn.get('ip_address', '未设置')}")
        print(f"  端口: {conn.get('port', '未设置')}")
        print(f"  COM端口: {conn.get('com_port', '未设置')}")
    
    # 检查产品信息
    if 'product_info' in config:
        info = config['product_info']
        print("\n📦 产品信息:")
        print(f"  产品型号: {info.get('model', '未设置')}")
        print(f"  流水号: {info.get('serial_number', '未设置')}")
        print(f"  测试员: {info.get('tester', '未设置')}")
    
    print("\n" + "=" * 80)
    print("诊断完成")
    print("=" * 80)

if __name__ == '__main__':
    main()

