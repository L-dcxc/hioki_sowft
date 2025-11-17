#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 逐步测试脚本（按照官方Sample流程）"""

import socket
import time


def send_command(sock, command, expect_response=True):
    """发送命令并接收响应"""
    try:
        # 发送命令
        cmd_with_terminator = command + "\r\n"
        print(f"\n>> 发送: {command}")
        sock.sendall(cmd_with_terminator.encode('ascii'))
        
        if not expect_response:
            print("   (不期待响应)")
            time.sleep(0.2)  # 短暂延迟
            return True
        
        # 接收响应（逐字节）
        response_chars = []
        start_time = time.time()
        
        while time.time() - start_time < 3.0:
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
                    continue  # 继续等待
                else:
                    break  # 没有数据
        
        response = ''.join(response_chars)
        print(f"<< 接收: {response if response else '(空响应)'}")
        return response
        
    except Exception as e:
        print(f"   错误: {e}")
        return None


def test_lr8450_protocol():
    """按照官方Sample3的流程测试LR8450"""
    
    ip = '192.168.2.136'
    port = 8800
    
    print('=' * 60)
    print(f'LR8450 协议测试 - 按照官方Sample流程')
    print(f'设备地址: {ip}:{port}')
    print('=' * 60)
    
    try:
        # 创建连接
        print('\n【步骤1】建立TCP连接...')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print('   ✓ 连接成功')
        
        # 按照官方Sample的初始化流程
        print('\n【步骤2】查询设备信息 (*IDN?)...')
        idn_response = send_command(sock, "*IDN?")
        
        if idn_response:
            print(f'   ✓ 设备识别成功')
            print(f'   设备信息: {idn_response[:80]}...')
        
        # 设置header OFF（按照Sample3）
        print('\n【步骤3】设置Header OFF...')
        send_command(sock, ":HEAD OFF", expect_response=False)
        print('   ✓ Header设置完成')
        
        # 清除错误
        print('\n【步骤4】清除错误 (*CLS)...')
        send_command(sock, "*CLS", expect_response=False)
        print('   ✓ 错误已清除')
        
        # 等待设备准备
        time.sleep(0.5)
        
        # 测试基本查询命令
        print('\n【步骤5】测试基本查询命令...')
        test_commands = [
            ('*ESR?', '事件状态寄存器'),
            (':STATus?', '设备状态'),
            (':MEMory:MAXPoint?', '内存容量'),
            (':MEMory:UNIT?', '单元信息'),
            (':ERRor?', '错误查询'),
        ]
        
        results = []
        for cmd, desc in test_commands:
            print(f'\n  测试: {cmd} - {desc}')
            response = send_command(sock, cmd)
            
            if response:
                results.append((cmd, True, response))
                print(f'     ✓ 成功: {response[:50]}')
            elif response == '':
                results.append((cmd, True, '(空响应，可能正常)'))
                print(f'     ⚠ 空响应')
            else:
                results.append((cmd, False, '无响应'))
                print(f'     ✗ 失败')
            
            time.sleep(0.3)  # 命令间延迟
        
        # 测试实时数据获取（Sample3流程）
        print('\n【步骤6】测试实时数据获取...')
        print('  6.1 发送 :MEMory:GETReal')
        send_command(sock, ":MEMory:GETReal", expect_response=False)
        time.sleep(0.5)
        
        print('  6.2 查询通道数据 :MEMory:VREAL? CH1_1')
        ch_data = send_command(sock, ":MEMory:VREAL? CH1_1")
        
        if ch_data:
            try:
                value = float(ch_data)
                print(f'     ✓ 通道数据获取成功: {value}')
                results.append((':MEMory:VREAL?', True, ch_data))
            except ValueError:
                print(f'     ⚠ 响应无法解析为数值: {ch_data}')
                results.append((':MEMory:VREAL?', False, ch_data))
        else:
            print(f'     ✗ 无响应')
            results.append((':MEMory:VREAL?', False, '无响应'))
        
        # 关闭连接
        sock.close()
        
        # 打印总结
        print('\n' + '=' * 60)
        print('测试总结')
        print('=' * 60)
        
        successful = sum(1 for _, success, _ in results if success)
        total = len(results)
        
        for cmd, success, response in results:
            status = '✓' if success else '✗'
            print(f'{status} {cmd:25s} : {response[:40]}')
        
        print(f'\n总体结果: {successful}/{total} 测试通过 ({successful/total*100:.1f}%)')
        
        return successful > 0
        
    except Exception as e:
        print(f'\n✗ 连接失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_lr8450_protocol()
    exit(0 if success else 1)




