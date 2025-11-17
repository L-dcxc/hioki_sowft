#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 端口测试 - 尝试8802端口

官方Sample3默认使用端口8802，而不是8800
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
        result = response if response else '(空)'
        print(f"<< {result}")
        return response if response else None
        
    except Exception as e:
        print(f"!! 错误: {e}")
        return None


def send_write(sock, command):
    """发送写命令"""
    cmd_with_terminator = command + "\r\n"
    sock.sendall(cmd_with_terminator.encode('ascii'))
    time.sleep(0.2)


def test_port(ip, port):
    """测试指定端口"""
    print(f'\n{"=" * 70}')
    print(f'测试端口 {port}')
    print(f'{"=" * 70}\n')
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((ip, port))
        print(f'✓ 端口 {port} 连接成功\n')
        
        # 测试基本命令
        idn = send_query(sock, "*IDN?")
        time.sleep(0.5)
        
        # 发送 :HEAD OFF
        print('\n发送 :HEAD OFF...')
        send_write(sock, ":HEAD OFF")
        
        # 测试配置查询
        print('\n测试配置查询命令:')
        test_commands = [
            '*ESR?',
            ':UNIT:COUNt?',
            ':CONFigure:SRATe?',
        ]
        
        success_count = 0
        for cmd in test_commands:
            response = send_query(sock, cmd)
            if response:
                success_count += 1
            time.sleep(0.3)
        
        sock.close()
        
        return {
            'port': port,
            'connected': True,
            'idn_response': bool(idn),
            'query_responses': success_count
        }
        
    except Exception as e:
        print(f'✗ 端口 {port} 连接失败: {e}')
        return {
            'port': port,
            'connected': False,
            'error': str(e)
        }


def main():
    ip = '192.168.2.136'
    
    print('=' * 70)
    print('LR8450 端口扫描测试')
    print(f'设备IP: {ip}')
    print('=' * 70)
    
    # 测试两个端口
    ports = [8800, 8802]
    results = []
    
    for port in ports:
        result = test_port(ip, port)
        results.append(result)
        time.sleep(1.0)
    
    # 总结
    print('\n' + '=' * 70)
    print('端口测试总结')
    print('=' * 70)
    
    for result in results:
        port = result['port']
        if result['connected']:
            idn_ok = '✓' if result.get('idn_response') else '✗'
            query_ok = result.get('query_responses', 0)
            print(f'\n端口 {port}:')
            print(f'  连接: ✓')
            print(f'  *IDN?: {idn_ok}')
            print(f'  配置查询响应数: {query_ok}/3')
            
            if query_ok > 0:
                print(f'  >>> 推荐使用端口 {port}')
        else:
            print(f'\n端口 {port}:')
            print(f'  连接: ✗ ({result.get("error", "未知错误")})')
    
    print('\n' + '=' * 70)


if __name__ == '__main__':
    main()





