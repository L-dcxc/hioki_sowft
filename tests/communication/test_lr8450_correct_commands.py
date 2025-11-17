#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 正确命令测试 - 基于官方Sample3源代码"""

import socket
import time


def send_query(sock, command, timeout=3.0):
    """发送查询命令并接收响应（按照官方Sample逐字节读取）"""
    try:
        # 发送命令
        cmd_with_terminator = command + "\r\n"
        print(f">> {command}")
        sock.sendall(cmd_with_terminator.encode('ascii'))
        
        # 逐字节接收（完全按照官方VB代码的逻辑）
        response_chars = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                sock.settimeout(0.1)
                byte = sock.recv(1)
                if not byte:
                    break
                
                char = byte.decode('ascii', errors='ignore')
                
                if char == '\n':  # LF - 响应结束
                    break
                elif char == '\r':  # CR - 跳过
                    continue
                else:
                    response_chars.append(char)
                    
            except socket.timeout:
                if response_chars:
                    continue
                else:
                    break
        
        response = ''.join(response_chars)
        print(f"<< {response if response else '(空)'}")
        return response
        
    except Exception as e:
        print(f"!! 错误: {e}")
        return None


def send_write(sock, command):
    """发送写命令（不期待响应）"""
    try:
        cmd_with_terminator = command + "\r\n"
        print(f">> {command} (写入)")
        sock.sendall(cmd_with_terminator.encode('ascii'))
        time.sleep(0.2)
        return True
    except Exception as e:
        print(f"!! 错误: {e}")
        return False


def main():
    """测试LR8450 - 使用官方Sample3的正确命令格式"""
    
    ip = '192.168.2.136'
    port = 8800
    
    print('=' * 70)
    print('LR8450 测试 - 使用官方Sample3命令格式（缩写形式）')
    print(f'设备: {ip}:{port}')
    print('=' * 70)
    
    try:
        # 连接设备
        print('\n【步骤1】连接设备...')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print('✓ 连接成功\n')
        
        # 初始化（按照Sample3）
        print('【步骤2】初始化...')
        idn = send_query(sock, "*IDN?")
        send_write(sock, ":HEAD OFF")
        print()
        
        # 测试实时数据获取（官方Sample3的核心功能）
        print('【步骤3】获取实时数据（Sample3流程）...')
        print('注意：使用缩写形式 :MEM:GETREAL 和 :MEM:VREAL?\n')
        
        # 发送 :MEM:GETREAL（缩写形式）
        send_write(sock, ":MEM:GETREAL")
        time.sleep(0.3)
        
        # 查询通道数据（缩写形式）
        print('查询前4个通道:')
        channels = ['CH1_1', 'CH1_2', 'CH1_3', 'CH1_4']
        
        channel_data = {}
        for ch in channels:
            response = send_query(sock, f":MEM:VREAL? {ch}")
            if response:
                try:
                    value = float(response)
                    channel_data[ch] = value
                    print(f'  ✓ {ch} = {value}')
                except ValueError:
                    print(f'  ⚠ {ch} = {response} (非数值)')
            time.sleep(0.2)
        
        # 测试其他常用命令（缩写形式）
        print('\n【步骤4】测试其他常用命令（缩写形式）...')
        
        other_commands = [
            ':STAT?',
            ':MEM:MAXP?',
            ':MEM:UNIT?',
        ]
        
        for cmd in other_commands:
            send_query(sock, cmd)
            time.sleep(0.3)
        
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('测试总结')
        print('=' * 70)
        
        if channel_data:
            print(f'✓ 成功获取 {len(channel_data)} 个通道的实时数据:')
            for ch, val in channel_data.items():
                print(f'  {ch}: {val}')
        else:
            print('⚠ 未能获取通道数据')
        
        print('\n关键发现：')
        print('• 正确命令格式：使用缩写形式 :MEM:GETREAL 和 :MEM:VREAL?')
        print('• 完整形式 :MEMory:GETReal 可能不被支持')
        
        return len(channel_data) > 0
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    print(f'\n{"✓ 测试通过" if success else "✗ 测试失败"}')
    exit(0 if success else 1)




