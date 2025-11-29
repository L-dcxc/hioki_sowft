#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试各种UNIT检测命令，找出设备实际支持的命令"""

import socket
import time


def send_write(sock, command):
    """发送写命令"""
    try:
        sock.sendall((command + "\r\n").encode('utf-8'))
        time.sleep(0.1)
        return True
    except Exception as e:
        print(f"  ✗ 发送失败: {e}")
        return False


def send_query(sock, command):
    """发送查询命令并接收响应"""
    try:
        sock.sendall((command + "\r\n").encode('utf-8'))
        time.sleep(0.3)
        
        response = sock.recv(4096).decode('utf-8', errors='ignore').strip()
        
        if response:
            print(f"  ✓ {command}")
            print(f"    响应: {response}")
            return response
        else:
            print(f"  ✗ {command} (无响应)")
            return None
            
    except Exception as e:
        print(f"  ✗ {command} (错误: {e})")
        return None


def test_unit_commands():
    """测试各种UNIT相关命令"""
    ip = "192.168.2.44"
    port = 8802
    
    print("=" * 70)
    print("测试LR8450 UNIT检测命令")
    print("=" * 70)
    print(f"\n连接到 {ip}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((ip, port))
        print("✓ 连接成功\n")
        
        # 初始化
        print("【步骤1】初始化设备")
        print("-" * 70)
        send_query(sock, "*IDN?")
        send_write(sock, ":HEAD OFF")
        send_write(sock, "*CLS")
        time.sleep(0.5)
        print()
        
        # 测试UNIT相关命令（多种格式）
        print("【步骤2】测试UNIT查询命令（多种格式）")
        print("-" * 70)
        
        unit_commands = [
            # 查询模块数量
            ':UNIT:COUNt?',
            ':UNIT:COUNT?',
            
            # 查询UNIT1信息（多种格式）
            ':UNIT:CHANnel? UNIT1',
            ':UNIT:CHANNEL? UNIT1',
            ':UNIT:CHANnel? 1',
            ':UNIT:CHANNEL? 1',
            ':UNIT1:CHANnel?',
            ':UNIT1:CHANNEL?',
            ':UNIT1:CHANnel:COUNt?',
            ':UNIT1:CHANNEL:COUNT?',
            
            # 查询UNIT类型
            ':UNIT:TYPE? UNIT1',
            ':UNIT:TYPE? 1',
            ':UNIT1:TYPE?',
            ':UNIT:MODel? UNIT1',
            ':UNIT:MODEL? UNIT1',
            ':UNIT1:MODel?',
            ':UNIT1:MODEL?',
            
            # 查询UNIT名称
            ':UNIT:NAME? UNIT1',
            ':UNIT1:NAME?',
            
            # 查询UNIT功能
            ':UNIT:FUNCtion? UNIT1',
            ':UNIT:FUNCTION? UNIT1',
            ':UNIT1:FUNCtion?',
            ':UNIT1:FUNCTION?',
        ]
        
        print("\n尝试各种UNIT查询命令:\n")
        for cmd in unit_commands:
            send_query(sock, cmd)
            time.sleep(0.2)
        
        print()
        
        # 测试通道查询命令
        print("【步骤3】测试通道查询命令")
        print("-" * 70)
        
        channel_commands = [
            # 查询CH1_1的状态
            ':UNIT:STORe? CH1_1',
            ':UNIT:STORE? CH1_1',
            
            # 查询CH1_1的量程
            ':UNIT:RANGe? CH1_1',
            ':UNIT:RANGE? CH1_1',
            ':SCALing:RANGe? CH1_1',
            ':SCALING:RANGE? CH1_1',
            
            # 查询CH1_1的标签
            ':UNIT:LABel? UNIT1,CH1',
            ':UNIT:LABEL? UNIT1,CH1',
            
            # 查询CH1_1的单位
            ':UNIT:UNIT? UNIT1,CH1',
            ':SCALing:UNIT? CH1_1',
            ':SCALING:UNIT? CH1_1',
        ]
        
        print("\n尝试各种通道查询命令:\n")
        for cmd in channel_commands:
            send_query(sock, cmd)
            time.sleep(0.2)
        
        print()
        
        # 测试配置查询命令
        print("【步骤4】测试配置查询命令")
        print("-" * 70)
        
        config_commands = [
            ':CONFigure:INTerval?',
            ':CONFIGURE:INTERVAL?',
            ':CONFigure:RECTime?',
            ':CONFIGURE:RECTIME?',
            ':CONFigure:SRATe?',
            ':CONFIGURE:SRATE?',
        ]
        
        print("\n尝试各种配置查询命令:\n")
        for cmd in config_commands:
            send_query(sock, cmd)
            time.sleep(0.2)
        
        print()
        
        # 测试实际读取通道数据
        print("【步骤5】测试读取通道数据")
        print("-" * 70)
        
        print("\n启动采集...")
        send_write(sock, ":STARt")
        time.sleep(1.0)
        
        print("\n获取实时数据快照...")
        send_write(sock, ":MEMory:GETReal")
        time.sleep(0.5)
        
        print("\n尝试读取各个通道的数据:\n")
        test_channels = ['CH1_1', 'CH1_2', 'CH1_3', 'CH1_4', 'CH1_5', 'CH2_1']
        
        for channel in test_channels:
            cmd = f":MEMory:VREAL? {channel}"
            response = send_query(sock, cmd)
            time.sleep(0.2)
        
        print("\n停止采集...")
        send_write(sock, ":STOP")
        
        sock.close()
        
        print("\n" + "=" * 70)
        print("✓ 测试完成")
        print("=" * 70)
        print("\n请查看上面的输出，找出哪些命令返回了有效响应。")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_unit_commands()

