#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 诊断测试脚本 - 测试各种命令变体和状态"""

import socket
import time


def send_query(sock, command, timeout=3.0):
    """发送查询命令并接收响应"""
    try:
        cmd_with_terminator = command + "\r\n"
        print(f"  >> {command}")
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
        print(f"  << {response if response else '(空)'}")
        return response
        
    except Exception as e:
        print(f"  !! 错误: {e}")
        return None


def send_write(sock, command):
    """发送写命令（不期待响应）"""
    try:
        cmd_with_terminator = command + "\r\n"
        print(f"  >> {command} (写入)")
        sock.sendall(cmd_with_terminator.encode('ascii'))
        time.sleep(0.2)
        return True
    except Exception as e:
        print(f"  !! 错误: {e}")
        return False


def main():
    ip = '192.168.2.136'
    port = 8800
    
    print('=' * 70)
    print('LR8450 诊断测试')
    print('=' * 70)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print(f'\n✓ 连接成功: {ip}:{port}\n')
        
        # ========== 初始化 ==========
        print('【阶段1】初始化设备')
        print('-' * 70)
        
        # IDN
        idn = send_query(sock, "*IDN?")
        
        # Header OFF
        send_write(sock, ":HEAD OFF")
        send_write(sock, ":HEADer OFF")  # 尝试完整形式
        
        # 清除错误
        send_write(sock, "*CLS")
        
        time.sleep(0.5)
        
        # ========== 测试状态查询 ==========
        print('\n【阶段2】测试状态查询命令')
        print('-' * 70)
        
        status_commands = [
            '*ESR?',
            '*STB?',
            ':STATus?',
            ':STAT?',
            ':ERRor?',
            ':ERR?',
            ':SYST:ERR?',
        ]
        
        for cmd in status_commands:
            send_query(sock, cmd)
            time.sleep(0.3)
        
        # ========== 测试内存查询 ==========
        print('\n【阶段3】测试内存相关命令')
        print('-' * 70)
        
        memory_commands = [
            ':MEMory:MAXPoint?',
            ':MEM:MAXP?',
            ':MEMory:UNIT?',
            ':MEM:UNIT?',
        ]
        
        for cmd in memory_commands:
            send_query(sock, cmd)
            time.sleep(0.3)
        
        # ========== 启动采集并测试实时数据 ==========
        print('\n【阶段4】启动采集并测试实时数据')
        print('-' * 70)
        
        print('  启动采集...')
        send_write(sock, ":STARt")
        time.sleep(1.0)
        
        # 查询状态
        print('  查询采集状态...')
        status = send_query(sock, ":STATus?")
        
        # 获取实时数据快照
        print('  获取实时数据快照...')
        send_write(sock, ":MEMory:GETReal")
        time.sleep(0.5)
        
        # 尝试读取不同通道
        print('  读取通道数据...')
        test_channels = ['CH1_1', 'CH1_2', 'CH1_3', 'CH2_1']
        
        for channel in test_channels:
            cmd = f":MEMory:VREAL? {channel}"
            response = send_query(sock, cmd)
            if response:
                print(f'    ✓ {channel}: {response}')
                break  # 找到一个有效通道就够了
            time.sleep(0.2)
        
        # 停止采集
        print('\n  停止采集...')
        send_write(sock, ":STOP")
        
        sock.close()
        
        print('\n' + '=' * 70)
        print('✓ 诊断测试完成')
        print('=' * 70)
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()




