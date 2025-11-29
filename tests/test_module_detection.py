#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试模块检测功能"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from battery_analyzer.core.lr8450_client import LR8450Client


def test_module_detection():
    """测试模块检测功能"""
    print("=" * 70)
    print("测试LR8450模块检测功能")
    print("=" * 70)
    
    # 连接参数（根据实际情况修改）
    ip_address = "192.168.1.100"
    port = 8802
    
    print(f"\n正在连接设备 {ip_address}:{port}...")
    
    try:
        # 创建客户端
        client = LR8450Client(
            connection_type="TCP",
            ip_address=ip_address,
            port=port
        )
        
        # 连接
        if client.connect():
            print("✓ 设备连接成功\n")
            
            # 检测已安装的模块
            print("正在检测已安装的模块...")
            print("-" * 70)
            installed_modules = client.detect_installed_modules()
            print("-" * 70)
            
            if installed_modules:
                print(f"\n✓ 检测到 {len(installed_modules)} 个已安装的模块:")
                for unit_num in installed_modules:
                    print(f"  • UNIT{unit_num}")
                    
                print("\n可用的通道:")
                for unit_num in installed_modules:
                    print(f"  UNIT{unit_num}: CH{unit_num}_1 到 CH{unit_num}_30")
            else:
                print("\n⚠ 未检测到任何已安装的模块")
                print("请检查设备上是否插入了模块")
            
            # 断开连接
            client.disconnect()
            print("\n✓ 测试完成")
        else:
            print("✗ 设备连接失败")
            
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_module_detection()

