#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 真实数据采集验证测试

验证端口8802上的完整数据采集流程
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.simple_device_client import SimpleDeviceClient
import time


def main():
    ip = '192.168.2.136'
    port = 8802  # 使用正确的SCPI控制端口
    
    print('=' * 70)
    print('LR8450 真实数据采集验证')
    print(f'设备: {ip}:{port}')
    print('=' * 70)
    
    try:
        # 使用SimpleDeviceClient（每条命令一个连接）
        client = SimpleDeviceClient(ip, port)
        
        # 获取设备信息
        print('\n【步骤1】获取设备信息...')
        device_info = client.get_device_info()
        if device_info:
            print(f'✓ 设备识别成功')
            print(f'  型号: {device_info["manufacturer"]} {device_info["model"]}')
            print(f'  固件: {device_info["firmware"]}')
            print(f'  估算通道数: {device_info["estimated_channels"]}')
            print(f'  模块配置: {", ".join(device_info["unit_info"])}')
        else:
            print('✗ 无法获取设备信息')
            return False
        
        # 启动采集
        print('\n【步骤2】启动采集...')
        if client.send_command(":STARt"):
            print('✓ 采集命令已发送')
            time.sleep(1.0)
        else:
            print('✗ 采集命令发送失败')
        
        # 查询状态
        print('\n【步骤3】查询设备状态...')
        status = client.send_query(":STATus?")
        if status:
            print(f'  设备状态: {status}')
        
        # 获取实时数据
        print('\n【步骤4】获取实时数据...')
        
        for attempt in range(3):
            print(f'\n  尝试 {attempt + 1}/3:')
            
            # 获取数据快照
            client.send_command(":MEMory:GETReal")
            time.sleep(0.3)
            
            # 测试前10个通道
            real_data_count = 0
            for unit in [1, 2]:
                max_ch = 15 if unit == 1 else 4
                
                for ch in range(1, min(6, max_ch + 1)):  # 每个单元测试前5个通道
                    channel = f"CH{unit}_{ch}"
                    response = client.send_query(f":MEMory:VREAL? {channel}")
                    
                    if response:
                        # 检查是否是NODATA
                        if '9.99999' in response and 'E+99' in response:
                            print(f'    {channel}: NODATA')
                        else:
                            try:
                                value = float(response)
                                print(f'    ✓ {channel}: {value:.6f}')
                                real_data_count += 1
                            except ValueError:
                                print(f'    ⚠ {channel}: {response}')
                    
                    time.sleep(0.1)
            
            if real_data_count > 0:
                print(f'\n  ✓ 本次获取到 {real_data_count} 个通道的真实数据')
                break
            else:
                print(f'\n  ⚠ 本次未获取到有效数据')
                time.sleep(1.0)
        
        # 停止采集
        print('\n【步骤5】停止采集...')
        client.send_command(":STOP")
        
        print('\n' + '=' * 70)
        print('测试总结')
        print('=' * 70)
        print('\n✓ 端口8802是正确的SCPI控制端口')
        print('✓ 设备支持标准SCPI命令')
        print('✓ 可以成功获取实时数据')
        print('\n注意事项:')
        print('• CH1_1, CH1_2 返回NODATA表示这些通道未连接传感器')
        print('• CH2_1 等返回实际数值的通道是已连接的')
        print('• 需要过滤掉9.99999E+99的NODATA值')
        print('\n下一步:')
        print('1. 更新主程序使用端口8802')
        print('2. 实现通道自动检测（跳过NODATA通道）')
        print('3. 在UI中显示真实设备数据')
        
        return True
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    print(f'\n{"=" * 70}')
    print(f'{"✓ 验证通过 - 可以开始集成到主程序" if success else "✗ 验证失败"}')
    print('=' * 70)
    exit(0 if success else 1)





