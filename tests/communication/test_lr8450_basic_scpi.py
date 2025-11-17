#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 基本SCPI命令测试

只测试最基本的标准SCPI命令，看看设备到底支持什么
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


def main():
    ip = '192.168.2.136'
    port = 8800
    
    print('=' * 70)
    print('LR8450 基本SCPI命令测试')
    print(f'设备: {ip}:{port}')
    print('=' * 70)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print('\n✓ 连接成功\n')
        
        # 只测试标准SCPI命令（不带:HEAD OFF）
        print('【测试1】标准SCPI命令（不初始化）')
        print('-' * 70)
        
        basic_commands = [
            ('*IDN?', '设备识别'),
            ('*OPC?', '操作完成查询'),
            ('*ESR?', '事件状态寄存器'),
            ('*STB?', '状态字节'),
        ]
        
        results = {}
        for cmd, desc in basic_commands:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                results[cmd] = response
            time.sleep(0.5)
        
        sock.close()
        time.sleep(1.0)
        
        # 第二次连接，先发送 :HEAD OFF
        print('\n\n【测试2】发送 :HEAD OFF 后再测试')
        print('-' * 70)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        
        # 发送 :HEAD OFF
        print('\n先发送 :HEAD OFF...')
        cmd_with_terminator = ":HEAD OFF\r\n"
        sock.sendall(cmd_with_terminator.encode('ascii'))
        time.sleep(0.5)
        
        # 再测试同样的命令
        for cmd, desc in basic_commands:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                results[f'{cmd} (after HEAD OFF)'] = response
            time.sleep(0.5)
        
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('测试总结')
        print('=' * 70)
        
        if results:
            print(f'\n✓ 成功响应的命令:\n')
            for cmd, value in results.items():
                print(f'  {cmd:30s} = {value[:60]}')
        else:
            print('\n⚠ 除了 *IDN? 外，没有其他命令有响应')
            print('\n可能的原因:')
            print('1. 设备可能只支持非常有限的SCPI命令')
            print('2. 设备可能需要特殊的初始化序列')
            print('3. 某些命令可能需要在特定状态下才响应')
            print('4. 固件版本V2.10可能命令支持与文档不一致')
        
        print('\n建议:')
        print('• 查看设备面板上的当前状态')
        print('• 查看是否有错误指示灯')
        print('• 尝试手动在设备上操作后再测试')
        print('• 检查设备是否需要特殊模式切换到远程控制')
        
        return len(results) > 1  # 至少要有2个命令响应（包括*IDN?）
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)





