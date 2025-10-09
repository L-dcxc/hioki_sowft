#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本
提供统一的测试执行接口
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path


def run_communication_tests():
    """运行通信测试"""
    print("运行通信测试...")
    print("=" * 50)

    test_file = "tests/communication/test_lr8450_protocol.py"
    if os.path.exists(test_file):
        try:
            result = subprocess.run([sys.executable, test_file],
                                  capture_output=False, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"运行通信测试失败: {e}")
            return False
    else:
        print(f"测试文件不存在: {test_file}")
        return False


def run_connection_tests():
    """运行连接测试"""
    print("运行连接测试...")
    print("=" * 50)

    test_file = "tests/communication/test_device_connections.py"
    if os.path.exists(test_file):
        try:
            result = subprocess.run([sys.executable, test_file],
                                  capture_output=False, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"运行连接测试失败: {e}")
            return False
    else:
        print(f"测试文件不存在: {test_file}")
        return False


def run_unit_tests():
    """运行单元测试"""
    print("运行单元测试...")
    print("=" * 50)

    try:
        # 使用unittest模块运行测试
        result = subprocess.run([
            sys.executable, "-m", "unittest",
            "tests.unit.test_device_client", "-v"
        ], capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"运行单元测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("运行所有测试...")
    print("=" * 60)

    tests = [
        ("通信协议测试", run_communication_tests),
        ("设备连接测试", run_connection_tests),
        ("单元测试", run_unit_tests),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n执行: {test_name}")
        success = test_func()
        results.append((test_name, success))

    # 总结
    print("\n" + "=" * 60)
    print("测试总结:")
    print("=" * 60)

    successful = 0
    total = len(results)

    for test_name, success in results:
        status = "?" if success else "?"
        print(f"{status} {test_name}")
        if success:
            successful += 1

    print(f"\n总计: {successful}/{total} 通过")
    return successful == total


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="LR8450测试运行器")
    parser.add_argument(
        "test_type",
        choices=["communication", "connection", "unit", "all"],
        help="要运行的测试类型"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )

    args = parser.parse_args()

    print("LR8450数据采集软件测试套件")
    print("=" * 60)

    if args.test_type == "communication":
        success = run_communication_tests()
    elif args.test_type == "connection":
        success = run_connection_tests()
    elif args.test_type == "unit":
        success = run_unit_tests()
    elif args.test_type == "all":
        success = run_all_tests()

    exit(0 if success else 1)


if __name__ == "__main__":
    main()
