#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 完整通道扫描

通过实时数据扫描发现所有有效通道
"""

import socket
import time


def send_query(sock, command, timeout=2.0):
    """发送查询命令"""
    cmd_with_terminator = command + "\r\n"
    sock.sendall(cmd_with_terminator.encode('ascii'))
    
    response_chars = []
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            sock.settimeout(0.1)
            byte = sock.recv(1)
            if not byte:
                break
            
            char = byte.decode('ascii', errors='ignore')
            if char == '\n':
                break
            elif char == '\r':
                continue
            else:
                response_chars.append(char)
                
        except socket.timeout:
            if response_chars:
                continue
            else:
                break
    
    response = ''.join(response_chars)
    return response if response else None


def send_write(sock, command):
    """发送写命令"""
    cmd_with_terminator = command + "\r\n"
    sock.sendall(cmd_with_terminator.encode('ascii'))
    time.sleep(0.1)


def main():
    ip = '192.168.2.136'
    port = 8802
    
    print('=' * 70)
    print('LR8450 完整通道扫描')
    print('=' * 70)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print(f'\n✓ 连接成功: {ip}:{port}\n')
        
        # 初始化
        print('初始化...')
        send_query(sock, "*IDN?")
        send_write(sock, ":HEAD OFF")
        send_write(sock, "*CLS")
        
        # 启动采集
        print('启动采集...')
        send_write(sock, ":STARt")
        time.sleep(1.5)
        
        # 获取实时数据快照
        print('获取实时数据快照...\n')
        send_write(sock, ":MEMory:GETReal")
        time.sleep(0.5)
        
        # 扫描所有可能的通道
        print('=' * 70)
        print('扫描通道（基于IDN: U1-A=15ch, U2-4=4ch, U3-UB=4ch*10）')
        print('=' * 70)
        
        # 定义要扫描的单元和通道数
        units_to_scan = [
            (1, 15, 'U1-A'),   # UNIT1: 15通道模拟模块
            (2, 4, 'U2-4'),    # UNIT2: 4通道模块
            (3, 4, 'U3-B'),    # UNIT3: 4通道基础模块
            (4, 4, 'U4-B'),
            (5, 4, 'U5-B'),
            (6, 4, 'U6-B'),
            (7, 4, 'U7-B'),
            (8, 4, 'U8-B'),
            (9, 4, 'U9-B'),
            (10, 4, 'UA-B'),
            (11, 4, 'UB-B'),
            (12, 4, 'UC-B'),
        ]
        
        active_channels = []
        
        for unit_num, max_ch, unit_name in units_to_scan:
            print(f'\n扫描 UNIT{unit_num} ({unit_name}) - 最多{max_ch}通道:')
            unit_has_data = False
            
            for ch_num in range(1, max_ch + 1):
                channel = f"CH{unit_num}_{ch_num}"
                
                response = send_query(sock, f":MEMory:VREAL? {channel}")
                
                if response:
                    # 检查是否是NODATA
                    if '9.99999' in response and 'E+99' in response:
                        # NODATA - 跳过
                        pass
                    else:
                        try:
                            value = float(response)
                            print(f'  ✓ {channel:10s} = {value:12.6f}')
                            active_channels.append({
                                'channel': channel,
                                'unit': unit_num,
                                'ch': ch_num,
                                'value': value
                            })
                            unit_has_data = True
                        except ValueError:
                            print(f'  ⚠ {channel:10s} = {response}')
                
                time.sleep(0.05)  # 快速扫描
            
            if not unit_has_data:
                print(f'  (无有效数据)')
        
        # 停止采集
        print('\n停止采集...')
        send_write(sock, ":STOP")
        
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('扫描结果总结')
        print('=' * 70)
        
        if active_channels:
            print(f'\n✓ 发现 {len(active_channels)} 个有效通道:\n')
            for ch_info in active_channels:
                print(f"  {ch_info['channel']:10s} (UNIT{ch_info['unit']}-CH{ch_info['ch']}) = {ch_info['value']:12.6f}")
            
            print('\n建议的通道配置:')
            print('```python')
            print('ACTIVE_CHANNELS = [')
            for ch_info in active_channels:
                print(f'    "{ch_info["channel"]}",  # UNIT{ch_info["unit"]}-CH{ch_info["ch"]}')
            print(']')
            print('```')
        else:
            print('\n⚠ 未发现有效通道')
        
        return len(active_channels) > 0
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    print(f'\n{"=" * 70}')
    print(f'{"✓ 扫描完成" if success else "✗ 扫描失败"}')
    print('=' * 70)
    exit(0 if success else 1)




