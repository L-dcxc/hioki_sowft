#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 完整测试 - 使用正确的8802端口

8802端口是SCPI控制端口，8800是信息服务端口
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
    print(f">> {command} (写入)")
    sock.sendall(cmd_with_terminator.encode('ascii'))
    time.sleep(0.2)


def main():
    ip = '192.168.2.136'
    port = 8802  # 使用正确的SCPI端口
    
    print('=' * 70)
    print('LR8450 完整功能测试 - 端口8802（SCPI控制端口）')
    print(f'设备: {ip}:{port}')
    print('=' * 70)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print('\n✓ 连接成功\n')
        
        # 初始化
        print('【步骤1】初始化')
        print('-' * 70)
        idn = send_query(sock, "*IDN?")
        send_write(sock, ":HEAD OFF")
        send_write(sock, "*CLS")
        time.sleep(0.5)
        print()
        
        # 测试标准SCPI状态命令
        print('【步骤2】测试标准SCPI状态命令')
        print('-' * 70)
        
        status_commands = [
            ('*ESR?', '事件状态寄存器'),
            ('*STB?', '状态字节'),
            ('*OPC?', '操作完成'),
        ]
        
        config_data = {}
        for cmd, desc in status_commands:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        print()
        
        # 测试通道配置查询
        print('【步骤3】测试通道配置查询')
        print('-' * 70)
        
        unit_commands = [
            (':UNIT:COUNt?', '模块数量'),
            (':UNIT:TYPE? UNIT1', 'UNIT1类型'),
            (':UNIT:CHANnel? UNIT1', 'UNIT1通道数'),
            (':UNIT:LABel? UNIT1,CH1', 'UNIT1-CH1标签'),
        ]
        
        for cmd, desc in unit_commands:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        print()
        
        # 测试采样配置
        print('【步骤4】测试采样配置查询')
        print('-' * 70)
        
        config_commands = [
            (':CONFigure:SRATe?', '采样率'),
            (':CONFigure:TIMEbase?', '时基'),
        ]
        
        for cmd, desc in config_commands:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        print()
        
        # 测试实时数据获取
        print('【步骤5】测试实时数据获取')
        print('-' * 70)
        
        print('\n启动采集...')
        send_write(sock, ":STARt")
        time.sleep(1.5)
        
        print('\n查询状态...')
        status = send_query(sock, ":STATus?")
        
        print('\n获取实时数据快照...')
        send_write(sock, ":MEMory:GETReal")
        time.sleep(0.5)
        
        print('\n查询通道数据:')
        for ch in ['CH1_1', 'CH1_2', 'CH2_1']:
            response = send_query(sock, f":MEMory:VREAL? {ch}")
            if response and response != '9.99999+E99':
                config_data[f'Real-time {ch}'] = response
                print(f'  ✓ {ch} = {response}')
            time.sleep(0.2)
        
        print('\n停止采集...')
        send_write(sock, ":STOP")
        
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('测试总结')
        print('=' * 70)
        
        if config_data:
            print(f'\n✓ 成功获取 {len(config_data)} 项数据:\n')
            for cmd, value in config_data.items():
                print(f'  {cmd:35s} = {value[:60] if len(value) > 60 else value}')
            
            print('\n结论:')
            print('✓ 端口8802是正确的SCPI控制端口')
            print('✓ 设备支持标准SCPI命令')
            
            if any('Real-time' in k for k in config_data.keys()):
                print('✓ 成功获取实时数据！')
        else:
            print('\n⚠ 未能获取任何数据')
        
        print('\n' + '=' * 70)
        
        return len(config_data) > 0
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    print(f'\n{"✓ 测试通过" if success else "✗ 测试失败"}')
    exit(0 if success else 1)





