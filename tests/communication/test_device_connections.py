#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备连接测试脚本
测试TCP和USB连接的建立、断开和基本功能
"""

import socket
import time
import json
import argparse
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ConnectionTestResult:
    """连接测试结果"""
    connection_type: str
    ip_address: str
    port: int
    success: bool
    response_time: float
    error_message: str = ""
    device_info: Dict[str, Any] = None


def load_device_config(config_file: str = "tests/config/devices.json") -> Dict[str, Any]:
    """加载设备配置文件"""
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"配置文件不存在: {config_file}，使用默认配置")
            return {
                "devices": [{"name": "LR8450-01", "ip": "192.168.1.14", "port": 8800}],
                "test_settings": {"timeout": 5.0, "retry_count": 3, "delay_between_commands": 0.5}
            }
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return {
            "devices": [{"name": "LR8450-01", "ip": "192.168.1.14", "port": 8800}],
            "test_settings": {"timeout": 5.0, "retry_count": 3, "delay_between_commands": 0.5}
        }


class DeviceConnectionTester:
    """设备连接测试器"""

    def __init__(self):
        self.timeout = 5.0

    def test_tcp_connection(self, ip_address: str, port: int = 8800) -> ConnectionTestResult:
        """测试TCP连接"""
        start_time = time.time()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            # 尝试连接
            sock.connect((ip_address, port))

            # 测试基本命令
            cmd = "*IDN?\r\n"
            sock.sendall(cmd.encode('ascii'))

            # 读取响应
            response = sock.recv(1024).decode('ascii', errors='ignore').strip()
            device_info = self._parse_device_info(response)

            response_time = time.time() - start_time

            return ConnectionTestResult(
                connection_type="TCP",
                ip_address=ip_address,
                port=port,
                success=True,
                response_time=response_time,
                device_info=device_info
            )

        except Exception as e:
            response_time = time.time() - start_time
            return ConnectionTestResult(
                connection_type="TCP",
                ip_address=ip_address,
                port=port,
                success=False,
                response_time=response_time,
                error_message=str(e)
            )
        finally:
            try:
                sock.close()
            except:
                pass

    def _parse_device_info(self, response: str) -> Dict[str, Any]:
        """解析设备信息"""
        try:
            parts = response.split(',')
            if len(parts) >= 3:
                return {
                    "manufacturer": parts[0].strip(),
                    "model": parts[1].strip(),
                    "serial": parts[2].strip(),
                    "firmware": parts[3].strip() if len(parts) > 3 else ""
                }
        except:
            pass
        return {"raw_response": response}

    def test_multiple_connections(self, devices: list) -> Dict[str, ConnectionTestResult]:
        """测试多个设备的连接"""
        results = {}

        for device in devices:
            print(f"\n测试设备: {device['name']} ({device['ip']}:{device['port']})")

            result = self.test_tcp_connection(device['ip'], device['port'])

            if result.success:
                print(f"  ? 连接成功，响应时间: {result.response_time".2f"}s")
                if result.device_info:
                    print(f"  设备信息: {result.device_info}")
            else:
                print(f"  ? 连接失败: {result.error_message}")

            results[device['name']] = result

        return results

    def generate_connection_report(self, results: Dict[str, ConnectionTestResult]) -> str:
        """生成连接测试报告"""
        report = []
        report.append("设备连接测试报告")
        report.append("=" * 50)

        total_devices = len(results)
        successful_connections = sum(1 for r in results.values() if r.success)

        report.append(f"总设备数: {total_devices}")
        report.append(f"成功连接: {successful_connections}")
        report.append(f"失败连接: {total_devices - successful_connections}")
        report.append(f"成功率: {(successful_connections/total_devices*100)".1f"}%")

        report.append("\n详细结果:")
        report.append("-" * 30)

        for device_name, result in results.items():
            status = "?" if result.success else "?"
            report.append(f"{status} {device_name}: {result.response_time".2f"}s")

            if not result.success:
                report.append(f"    错误: {result.error_message}")

            if result.device_info:
                report.append(f"    设备: {result.device_info}")

        return "\n".join(report)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="LR8450设备连接测试")
    parser.add_argument("--config", default="tests/config/devices.json",
                       help="设备配置文件路径 (默认: tests/config/devices.json)")
    parser.add_argument("--device", default=None,
                       help="指定要测试的设备名称 (默认: 测试所有设备)")

    args = parser.parse_args()

    # 加载设备配置
    config = load_device_config(args.config)
    devices = config["devices"]

    # 如果指定了特定设备，只测试该设备
    if args.device:
        devices = [d for d in devices if d["name"] == args.device]
        if not devices:
            print(f"未找到设备: {args.device}")
            return

    print(f"加载了 {len(devices)} 个设备配置")

    tester = DeviceConnectionTester()

    print("开始设备连接测试...")
    print("=" * 60)

    # 运行测试
    results = tester.test_multiple_connections(test_devices)

    # 生成并显示报告
    report = tester.generate_connection_report(results)
    print(f"\n{report}")

    # 保存结果到文件
    with open("tests/communication/connection_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            device_name: {
                "connection_type": result.connection_type,
                "success": result.success,
                "response_time": result.response_time,
                "error_message": result.error_message,
                "device_info": result.device_info
            }
            for device_name, result in results.items()
        }, f, indent=2, ensure_ascii=False)

    print("\n测试结果已保存到 tests/communication/connection_test_results.json")


if __name__ == "__main__":
    main()
