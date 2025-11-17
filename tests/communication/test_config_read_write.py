#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 配置读写测试

测试哪些配置命令真正可用
"""

import socket
import time


def send_query(sock, command, timeout=3.0):
    """发送查询命令"""
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


def send_write(sock, command):
    """发送写命令"""
    cmd_with_terminator = command + "\r\n"
    print(f">> {command} (写入)")
    sock.sendall(cmd_with_terminator.encode('ascii'))
    time.sleep(0.2)


def main():
    ip = '192.168.2.136'
    port = 8802
    
    print('=' * 70)
    print('LR8450 配置读写测试')
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
        time.sleep(0.5)
        
        # 测试可能有效的配置查询命令
        print('\n【测试1】基础查询命令')
        print('-' * 70)
        
        basic_queries = [
            '*ESR?',
            '*STB?',
            '*OPC?',
            ':STATus?',
        ]
        
        for cmd in basic_queries:
            send_query(sock, cmd)
            time.sleep(0.3)
        
        # 测试通道相关查询（尝试不同格式）
        print('\n【测试2】通道信息查询（多种格式）')
        print('-' * 70)
        
        channel_queries = [
            # 尝试查询UNIT2（你插着模块的单元）
            ':UNIT:TYPE? UNIT2',
            ':UNIT:CHANnel? UNIT2',
            ':UNIT:MODel? UNIT2',
            ':UNIT:NAME? UNIT2',
            
            # 尝试查询CH2_3（你的热电偶通道）
            ':UNIT:LABel? UNIT2,CH3',
            ':UNIT:UNIT? UNIT2,CH3',
            ':UNIT:RANGe? UNIT2,CH3',
            ':UNIT:TYPE? UNIT2,CH3',
        ]
        
        for cmd in channel_queries:
            send_query(sock, cmd)
            time.sleep(0.3)
        
        # 测试采样率查询
        print('\n【测试3】采样和记录设置查询')
        print('-' * 70)
        
        sampling_queries = [
            ':CONFigure:SRATe?',
            ':CONF:SRAT?',
            ':SRATe?',
            ':INTerval?',
            ':TIMEbase?',
        ]
        
        for cmd in sampling_queries:
            send_query(sock, cmd)
            time.sleep(0.3)
        
        # 测试写入命令（设置通道标签）
        print('\n【测试4】尝试写入配置')
        print('-' * 70)
        
        print('\n尝试设置CH2_3的标签为"热电偶"...')
        send_write(sock, ':UNIT:LABel UNIT2,CH3,"热电偶"')
        time.sleep(0.5)
        
        print('读回标签验证...')
        label = send_query(sock, ':UNIT:LABel? UNIT2,CH3')
        
        if label:
            print(f'  ✓ 标签设置成功: {label}')
        else:
            print('  ⚠ 无法读回标签')
        
        sock.close()
        
        print('\n' + '=' * 70)
        print('测试完成')
        print('=' * 70)
        print('\n如果大部分命令仍返回空，可能原因:')
        print('1. 设备固件V2.10可能不支持某些查询命令')
        print('2. 某些命令需要设备处于特定状态')
        print('3. 配置信息可能只能通过其他方式获取')
        print('\n建议:')
        print('• 主要使用 *IDN? 获取基本信息')
        print('• 使用 :STATus? 查询设备状态')
        print('• 通过实时数据判断哪些通道有效（过滤NODATA）')
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()




