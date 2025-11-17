#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 UNIT2完整扫描 - 扫描30个通道"""

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
    print('LR8450 UNIT2 完整扫描（30通道）')
    print('=' * 70)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print(f'\n✓ 连接成功\n')
        
        # 初始化
        send_query(sock, "*IDN?")
        send_write(sock, ":HEAD OFF")
        send_write(sock, "*CLS")
        
        # 启动采集
        send_write(sock, ":STARt")
        time.sleep(1.5)
        
        # 获取实时数据快照
        send_write(sock, ":MEMory:GETReal")
        time.sleep(0.5)
        
        # 扫描UNIT2的30个通道
        print('扫描 UNIT2 的 1-30 通道:')
        print('-' * 70)
        
        active_channels = []
        nodata_channels = []
        
        for ch_num in range(1, 31):  # 1到30
            channel = f"CH2_{ch_num}"
            
            response = send_query(sock, f":MEMory:VREAL? {channel}")
            
            if response:
                # 检查是否是NODATA
                if '9.99999' in response and 'E+99' in response:
                    nodata_channels.append(channel)
                else:
                    try:
                        value = float(response)
                        print(f'  ✓ {channel:10s} = {value:15.6f}')
                        active_channels.append({
                            'channel': channel,
                            'ch_num': ch_num,
                            'value': value
                        })
                    except ValueError:
                        print(f'  ⚠ {channel:10s} = {response}')
            
            time.sleep(0.05)  # 快速扫描
        
        # 停止采集
        send_write(sock, ":STOP")
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('UNIT2 扫描结果')
        print('=' * 70)
        
        print(f'\n有效通道数: {len(active_channels)}/30')
        print(f'NODATA通道数: {len(nodata_channels)}/30')
        
        if active_channels:
            print(f'\n✓ 有效通道列表:\n')
            for ch_info in active_channels:
                print(f"  {ch_info['channel']:10s} (第{ch_info['ch_num']:2d}通道) = {ch_info['value']:15.6f}")
            
            print('\n建议的通道配置（Python代码）:')
            print('```python')
            print('# UNIT2 有效通道')
            print('UNIT2_ACTIVE_CHANNELS = [')
            for ch_info in active_channels:
                print(f'    "{ch_info["channel"]}",  # 第{ch_info["ch_num"]}通道')
            print(']')
            print('```')
            
            print('\n通道统计:')
            for ch_info in active_channels:
                if abs(ch_info['value']) > 10:
                    print(f"  {ch_info['channel']}: 可能是温度传感器（{ch_info['value']:.2f}°C）")
                elif abs(ch_info['value']) < 0.1:
                    print(f"  {ch_info['channel']}: 可能是电压或微小信号（{ch_info['value']*1000:.2f}mV）")
                else:
                    print(f"  {ch_info['channel']}: {ch_info['value']:.6f}")
        
        print('\n' + '=' * 70)
        
        return len(active_channels) > 0
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)




