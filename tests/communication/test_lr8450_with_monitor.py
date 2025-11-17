#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 测试 - 启用监控值显示后获取实时数据

根据官方文档，:MEMory:VREAL? 需要满足以下条件之一：
1. Measurements（测量中）
2. Display Monitor Values（显示监控值）
3. Execute :MEMory:GETReal
"""

import socket
import time


def send_query(sock, command, timeout=3.0):
    """发送查询命令并接收响应"""
    try:
        cmd_with_terminator = command + "\r\n"
        print(f">> {command}")
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
        print(f"<< {response if response else '(空)'}")
        return response
        
    except Exception as e:
        print(f"!! 错误: {e}")
        return None


def send_write(sock, command):
    """发送写命令"""
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
    ip = '192.168.2.136'
    port = 8800
    
    print('=' * 70)
    print('LR8450 测试 - 启用监控值后获取实时数据')
    print(f'设备: {ip}:{port}')
    print('=' * 70)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print('\n✓ 连接成功\n')
        
        # 初始化
        print('【步骤1】初始化...')
        idn = send_query(sock, "*IDN?")
        send_write(sock, ":HEAD OFF")
        send_write(sock, "*CLS")
        time.sleep(0.5)
        print()
        
        # 尝试启用监控值显示（猜测命令）
        print('【步骤2】尝试启用监控值显示...')
        possible_commands = [
            ':DISPlay:MONItor ON',
            ':DISP:MONI ON',
            ':MONItor ON',
            ':MONI ON',
        ]
        
        for cmd in possible_commands:
            send_write(sock, cmd)
            time.sleep(0.3)
        print()
        
        # 启动采集
        print('【步骤3】启动采集...')
        send_write(sock, ":STARt")
        time.sleep(2.0)  # 等待采集启动
        
        # 查询状态
        status = send_query(sock, ":STATus?")
        print()
        
        # 获取实时数据
        print('【步骤4】获取实时数据（完整形式）...')
        send_write(sock, ":MEMory:GETReal")
        time.sleep(0.5)
        
        # 测试不同的查询命令
        print('\n尝试不同的实时数据查询命令:')
        
        test_queries = [
            (':MEMory:VREAL? CH1_1', '完整形式 - 测量值'),
            (':MEM:VREAL? CH1_1', '缩写形式 - 测量值'),
            (':MEMory:AREAL? CH1_1', '完整形式 - ASCII'),
            (':MEM:AREAL? CH1_1', '缩写形式 - ASCII'),
            (':MEMory:BREAL? CH1_1', '完整形式 - Binary'),
            (':MEM:BREAL? CH1_1', '缩写形式 - Binary'),
        ]
        
        success_data = {}
        for cmd, desc in test_queries:
            print(f'\n  {desc}:')
            response = send_query(sock, cmd)
            
            if response and response != '(空)':
                # 检查是否是NODATA
                if '9.99999+E99' in response or '9.99999E+99' in response:
                    print(f'    ⚠ NODATA - 设备未准备好')
                else:
                    try:
                        # 尝试解析为浮点数
                        value = float(response)
                        success_data[cmd] = value
                        print(f'    ✓ 成功: {value}')
                    except ValueError:
                        print(f'    ⚠ 非数值: {response}')
                        success_data[cmd] = response
            
            time.sleep(0.3)
        
        # 测试整个Unit的数据（可能更容易成功）
        print('\n【步骤5】尝试获取整个Unit的数据...')
        unit_cmd = ':MEMory:TVREAL? UNIT1'
        print(f'  {unit_cmd}:')
        response = send_query(sock, unit_cmd)
        
        if response and '9.99999' not in response:
            print(f'    ✓ 成功获取Unit数据')
            print(f'    数据: {response[:100]}...')
        
        # 停止采集
        print('\n【步骤6】停止采集...')
        send_write(sock, ":STOP")
        
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('测试总结')
        print('=' * 70)
        
        if success_data:
            print(f'✓ 成功获取 {len(success_data)} 个命令的数据:')
            for cmd, val in success_data.items():
                print(f'  {cmd}: {val}')
        else:
            print('⚠ 未能获取任何实时数据')
            print('\n可能的原因:')
            print('1. 设备未启动采集（:STARt）')
            print('2. 设备未显示监控值')
            print('3. 命令格式不正确')
            print('4. 设备固件版本不支持')
        
        return len(success_data) > 0
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    print(f'\n{"✓ 测试通过" if success else "✗ 测试失败"}')
    exit(0 if success else 1)




