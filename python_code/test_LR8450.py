#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LR8450通信协议测试脚本
基于HIOKI官方通信手册进行系统性测试
"""

import socket
import time
import logging
from typing import Optional, Dict, Any, List
import json

class LR8450Tester:
    """LR8450设备通信测试器"""

    def __init__(self, ip_address: str, port: int = 8800):
        self.ip_address = ip_address
        self.port = port
        self.timeout = 5.0
        self.logger = logging.getLogger(__name__)

    def send_command(self, command: str, expect_response: bool = True) -> Optional[str]:
        """发送命令并获取响应"""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.ip_address, self.port))

            # 发送命令
            cmd_with_terminator = command + "\r\n"
            print(f"\n>> 发送: {command}")
            sock.sendall(cmd_with_terminator.encode("ascii"))

            if expect_response:
                # 接收响应
                response_bytes = []
                start_time = time.time()

                while time.time() - start_time < self.timeout:
                    try:
                        sock.settimeout(0.1)
                        byte = sock.recv(1)
                        if not byte:
                            break

                        char = byte.decode('ascii', errors='ignore')
                        if char == '\n':  # LF found
                            break
                        elif char == '\r':  # Skip CR
                            continue
                        else:
                            response_bytes.append(char)

                    except socket.timeout:
                        if response_bytes:
                            continue  # Keep waiting
                        else:
                            break  # No data received

                response = ''.join(response_bytes)
                print(f"<< 响应: {response}")
                return response if response else None
            else:
                return "OK"

        except Exception as e:
            print(f"命令执行错误 '{command}': {e}")
            return None
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass

    def test_basic_identification(self) -> Dict[str, Any]:
        """测试基本识别命令"""
        print("\n=== 基本识别测试 ===")

        results = {}

        # 1. 设备识别
        commands = [
            ("*IDN?", "设备识别"),
            ("*ESR?", "标准事件状态寄存器"),
            ("*STB?", "状态字节"),
        ]

        for cmd, desc in commands:
            response = self.send_command(cmd, True)
            results[cmd] = {
                "description": desc,
                "success": response is not None,
                "response": response
            }
            time.sleep(0.5)

        return results

    def test_error_handling(self) -> Dict[str, Any]:
        """测试错误处理命令"""
        print("\n=== 错误处理测试 ===")

        results = {}

        commands = [
            ("*CLS", "清除状态"),
            (":ERRor?", "查询错误"),
            (":ERRor:COUNt?", "错误计数"),
        ]

        for cmd, desc in commands:
            expect_response = not cmd.endswith("?")
            response = self.send_command(cmd, expect_response)
            results[cmd] = {
                "description": desc,
                "success": response is not None,
                "response": response
            }
            time.sleep(0.5)

        return results

    def test_memory_commands(self) -> Dict[str, Any]:
        """测试内存相关命令"""
        print("\n=== 内存命令测试 ===")

        results = {}

        commands = [
            (":MEMory:MAXPoint?", "最大记录点数"),
            (":MEMory:POINts?", "当前记录点数"),
            (":MEMory:TIME?", "记录时间"),
            (":MEMory:UNIT?", "单元信息"),
            (":MEMory:MODE?", "记录模式"),
        ]

        for cmd, desc in commands:
            response = self.send_command(cmd, True)
            results[cmd] = {
                "description": desc,
                "success": response is not None,
                "response": response
            }
            time.sleep(0.5)

        return results

    def test_configure_commands(self) -> Dict[str, Any]:
        """测试配置相关命令"""
        print("\n=== 配置命令测试 ===")

        results = {}

        commands = [
            (":CONFigure:RATE?", "采样率查询"),
            (":CONFigure:TIME?", "记录时间查询"),
            (":CONFigure:TRIGger:MODE?", "触发模式查询"),
            (":CONFigure:UNIT:COUNt?", "单元数量查询"),
        ]

        for cmd, desc in commands:
            response = self.send_command(cmd, True)
            results[cmd] = {
                "description": desc,
                "success": response is not None,
                "response": response
            }
            time.sleep(0.5)

        return results

    def test_channel_commands(self) -> Dict[str, Any]:
        """测试通道相关命令"""
        print("\n=== 通道命令测试 ===")

        results = {}

        commands = [
            (":UNIT:COUNt?", "单元数量"),
            (":UNIT:TYPE? 1", "单元1类型"),
            (":UNIT:NAME? 1", "单元1名称"),
            (":UNIT:INFO? 1", "单元1信息"),
        ]

        for cmd, desc in commands:
            response = self.send_command(cmd, True)
            results[cmd] = {
                "description": desc,
                "success": response is not None,
                "response": response
            }
            time.sleep(0.5)

        return results

    def test_real_time_data(self) -> Dict[str, Any]:
        """测试实时数据获取"""
        print("\n=== 实时数据测试 ===")

        results = {}

        # 首先尝试获取实时快照
        response = self.send_command(":MEM:GETREAL", False)
        results[":MEM:GETREAL"] = {
            "description": "获取实时快照",
            "success": response is not None,
            "response": response
        }

        if response:
            time.sleep(1)

            # 尝试查询通道数据
            channel_commands = [
                ":MEM:VREAL? CH1_1",
                ":MEM:VREAL? CH1_2",
                ":MEM:VREAL? CH1_3",
            ]

            for cmd in channel_commands:
                response = self.send_command(cmd, True)
                results[cmd] = {
                    "description": f"查询{cmd.split()[-1]}数据",
                    "success": response is not None,
                    "response": response
                }
                time.sleep(0.5)

        return results

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """运行全面测试"""
        print(f"开始对设备 {self.ip_address}:{self.port} 进行全面测试")
        print("=" * 60)

        all_results = {}

        # 运行各个测试模块
        test_modules = [
            ("基本识别", self.test_basic_identification),
            ("错误处理", self.test_error_handling),
            ("内存命令", self.test_memory_commands),
            ("配置命令", self.test_configure_commands),
            ("通道命令", self.test_channel_commands),
            ("实时数据", self.test_real_time_data),
        ]

        for module_name, test_func in test_modules:
            try:
                module_results = test_func()
                all_results[module_name] = module_results
            except Exception as e:
                print(f"测试模块 '{module_name}' 出错: {e}")
                all_results[module_name] = {"error": str(e)}

        return all_results

    def print_test_summary(self, results: Dict[str, Any]):
        """打印测试总结"""
        print("\n" + "=" * 60)
        print("测试总结:")
        print("=" * 60)

        total_commands = 0
        successful_commands = 0

        for module_name, module_results in results.items():
            if "error" not in module_results:
                print(f"\n{module_name}:")
                for cmd, result in module_results.items():
                    total_commands += 1
                    if result["success"]:
                        successful_commands += 1
                        status = "?"
                    else:
                        status = "?"

                    response = result.get("response", "")
                    if len(response) > 50:
                        response = response[:50] + "..."

                    print(f"  {status} {cmd"<20"} {response}")

        print(f"\n总体结果: {successful_commands}/{total_commands} 个命令成功")
        success_rate = (successful_commands / total_commands * 100) if total_commands > 0 else 0
        print(f"成功率: {success_rate".1f"}%")

        return success_rate


def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 设备连接信息
    devices = [
        {"ip": "192.168.2.136", "port": 8800, "name": "LR8450-01"},
        # 可以添加更多设备
    ]

    all_results = {}

    for device in devices:
        print(f"\n{'='*80}")
        print(f"测试设备: {device['name']} ({device['ip']}:{device['port']})")
        print(f"{'='*80}")

        tester = LR8450Tester(device["ip"], device["port"])

        try:
            results = tester.run_comprehensive_test()
            success_rate = tester.print_test_summary(results)

            all_results[device["name"]] = {
                "results": results,
                "success_rate": success_rate
            }

        except Exception as e:
            print(f"设备 {device['name']} 测试失败: {e}")
            all_results[device["name"]] = {"error": str(e)}

    # 保存测试结果
    with open("lr8450_test_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("\n测试结果已保存到 lr8450_test_results.json")


if __name__ == "__main__":
    main()