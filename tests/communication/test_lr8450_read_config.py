#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR8450 读取设备配置测试

测试目标：读取设备的配置信息（通道设置、采样率、量程等）
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


def main():
    ip = '192.168.2.136'
    port = 8800
    
    print('=' * 70)
    print('LR8450 设备配置读取测试')
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
        
        # 读取通道配置
        print('【步骤2】读取通道配置（UNIT命令）')
        print('-' * 70)
        
        unit_queries = [
            (':UNIT:COUNt?', '查询模块数量'),
            (':UNIT:TYPE? UNIT1', '查询UNIT1类型'),
            (':UNIT:TYPE? UNIT2', '查询UNIT2类型'),
            (':UNIT:CHANnel? UNIT1', '查询UNIT1通道数'),
            (':UNIT:CHANnel? UNIT2', '查询UNIT2通道数'),
            (':UNIT:FUNCtion? UNIT1', '查询UNIT1功能'),
            (':UNIT:RANGe? UNIT1,CH1', '查询UNIT1-CH1量程'),
        ]
        
        config_data = {}
        for cmd, desc in unit_queries:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        print()
        
        # 读取采样配置
        print('【步骤3】读取采样配置（CONFigure命令）')
        print('-' * 70)
        
        config_queries = [
            (':CONFigure:STORe?', '查询存储模式'),
            (':CONFigure:SRATe?', '查询采样率'),
            (':CONFigure:TIMEbase?', '查询时基'),
            (':CONFigure:TRIGger?', '查询触发设置'),
            (':CONFigure:RECLength?', '查询记录长度'),
        ]
        
        for cmd, desc in config_queries:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        print()
        
        # 读取系统信息
        print('【步骤4】读取系统信息（SYSTem命令）')
        print('-' * 70)
        
        system_queries = [
            (':SYSTem:VERSion?', '查询SCPI版本'),
            (':SYSTem:DATE?', '查询系统日期'),
            (':SYSTem:TIME?', '查询系统时间'),
            (':SYSTem:ERRor?', '查询系统错误'),
        ]
        
        for cmd, desc in system_queries:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        print()
        
        # 读取通道名称和单位
        print('【步骤5】读取通道名称和单位')
        print('-' * 70)
        
        channel_queries = [
            (':UNIT:LABel? UNIT1,CH1', '查询UNIT1-CH1标签'),
            (':UNIT:UNIT? UNIT1,CH1', '查询UNIT1-CH1单位'),
            (':UNIT:SCALing? UNIT1,CH1', '查询UNIT1-CH1缩放'),
        ]
        
        for cmd, desc in channel_queries:
            print(f'\n{desc}:')
            response = send_query(sock, cmd)
            if response:
                config_data[cmd] = response
            time.sleep(0.3)
        
        sock.close()
        
        # 总结
        print('\n' + '=' * 70)
        print('配置读取总结')
        print('=' * 70)
        
        if config_data:
            print(f'\n✓ 成功读取 {len(config_data)} 项配置信息:\n')
            for cmd, value in config_data.items():
                print(f'  {cmd:35s} = {value}')
        else:
            print('\n⚠ 未能读取任何配置信息')
        
        print('\n' + '=' * 70)
        
        return len(config_data) > 0
        
    except Exception as e:
        print(f'\n✗ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    print(f'{"✓ 测试通过 - 成功读取设备配置" if success else "✗ 测试失败"}')
    exit(0 if success else 1)




