#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备客户端单元测试
测试SimpleDeviceClient类的各个功能
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import socket
import time

# 导入被测试的模块
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.core.simple_device_client import SimpleDeviceClient


class TestSimpleDeviceClient(unittest.TestCase):
    """SimpleDeviceClient单元测试"""

    def setUp(self):
        """测试前准备"""
        self.client = SimpleDeviceClient("192.168.1.14", 8800)
        self.test_responses = {
            "*IDN?": "HIOKI,LR8450,V1.00,123456",
            "*ESR?": "0",
            ":ERRor?": "0,\"No error\"",
            ":MEMory:MAXPoint?": "1000000"
        }

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.client.ip_address, "192.168.1.14")
        self.assertEqual(self.client.port, 8800)
        self.assertEqual(self.client.timeout, 5.0)

    @patch('socket.socket')
    def test_send_query_success(self, mock_socket):
        """测试查询命令成功发送"""
        # 设置模拟socket
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # 模拟连接和响应
        mock_sock_instance.recv.side_effect = [
            b"HIOKI,LR8450,V1.00,123456\n"  # 响应数据
        ]

        # 执行查询
        response = self.client.send_query("*IDN?")

        # 验证结果
        self.assertEqual(response, "HIOKI,LR8450,V1.00,123456")
        mock_sock_instance.connect.assert_called_once_with(("192.168.1.14", 8800))
        mock_sock_instance.sendall.assert_called_once()

    @patch('socket.socket')
    def test_send_query_timeout(self, mock_socket):
        """测试查询命令超时"""
        # 设置模拟socket
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # 模拟超时
        mock_sock_instance.recv.side_effect = socket.timeout()

        # 执行查询
        response = self.client.send_query("*IDN?")

        # 验证结果
        self.assertIsNone(response)

    @patch('socket.socket')
    def test_send_command_success(self, mock_socket):
        """测试命令发送成功"""
        # 设置模拟socket
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # 执行命令
        result = self.client.send_command("*CLS")

        # 验证结果
        self.assertTrue(result)
        mock_sock_instance.connect.assert_called_once_with(("192.168.1.14", 8800))
        mock_sock_instance.sendall.assert_called_once()

    @patch('socket.socket')
    def test_get_device_info_success(self, mock_socket):
        """测试设备信息获取成功"""
        # 设置模拟socket
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # 模拟IDN响应
        mock_sock_instance.recv.side_effect = [
            b"HIOKI,LR8450,V1.00,123456,U8552-15,U8552-15\n"
        ]

        # 执行获取设备信息
        device_info = self.client.get_device_info()

        # 验证结果
        self.assertIsNotNone(device_info)
        self.assertEqual(device_info["manufacturer"], "HIOKI")
        self.assertEqual(device_info["model"], "LR8450")
        self.assertEqual(device_info["firmware"], "V1.00")
        self.assertEqual(device_info["estimated_channels"], 30)

    @patch('socket.socket')
    def test_get_device_info_failure(self, mock_socket):
        """测试设备信息获取失败"""
        # 设置模拟socket
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # 模拟连接失败
        mock_sock_instance.connect.side_effect = ConnectionError("Connection failed")

        # 执行获取设备信息
        device_info = self.client.get_device_info()

        # 验证结果
        self.assertIsNone(device_info)

    def test_parse_device_info_complex(self):
        """测试复杂设备信息的解析"""
        # 测试包含多个单元模块的响应
        idn_response = "HIOKI,LR8450,V1.00,123456,U8552-15,U8552-15,U8551-4,DUMMY"
        device_info = self.client.get_device_info()

        # 这里我们需要模拟send_query方法
        with patch.object(self.client, 'send_query', return_value=idn_response):
            device_info = self.client.get_device_info()

        self.assertIsNotNone(device_info)
        self.assertEqual(device_info["manufacturer"], "HIOKI")
        self.assertEqual(device_info["model"], "LR8450")
        self.assertEqual(device_info["estimated_channels"], 30)  # 15+15+4 = 34，但限制为30

    def test_connection_per_command_pattern(self):
        """测试每个命令创建新连接的模式"""
        with patch('socket.socket') as mock_socket_class:
            mock_sock_instance = Mock()
            mock_socket_class.return_value = mock_sock_instance

            # 模拟成功响应
            mock_sock_instance.recv.side_effect = [b"OK\n"]

            # 发送两个命令
            self.client.send_query("*IDN?")
            self.client.send_command("*CLS")

            # 验证创建了两个连接
            self.assertEqual(mock_socket_class.call_count, 2)
            self.assertEqual(mock_sock_instance.connect.call_count, 2)
            self.assertEqual(mock_sock_instance.close.call_count, 2)

    def test_error_handling_in_send_query(self):
        """测试查询命令中的错误处理"""
        with patch('socket.socket') as mock_socket_class:
            mock_sock_instance = Mock()
            mock_socket_class.return_value = mock_sock_instance

            # 模拟各种错误情况
            mock_sock_instance.connect.side_effect = Exception("Connection failed")

            response = self.client.send_query("*IDN?")

            # 验证错误处理
            self.assertIsNone(response)

    def test_command_with_terminator(self):
        """测试命令是否正确添加终止符"""
        with patch('socket.socket') as mock_socket_class:
            mock_sock_instance = Mock()
            mock_socket_class.return_value = mock_sock_instance

            # 模拟成功响应
            mock_sock_instance.recv.side_effect = [b"OK\n"]

            self.client.send_command("*CLS")

            # 验证命令是否添加了\r\n
            sent_data = mock_sock_instance.sendall.call_args[0][0]
            self.assertEqual(sent_data, b"*CLS\r\n")


class TestDeviceInfoParsing(unittest.TestCase):
    """设备信息解析测试"""

    def setUp(self):
        self.client = SimpleDeviceClient("192.168.1.14", 8800)

    def test_parse_minimal_idn(self):
        """测试解析最小IDN响应"""
        response = "HIOKI,LR8450,V1.00"
        device_info = self.client.get_device_info()

        with patch.object(self.client, 'send_query', return_value=response):
            device_info = self.client.get_device_info()

        self.assertEqual(device_info["manufacturer"], "HIOKI")
        self.assertEqual(device_info["model"], "LR8450")
        self.assertEqual(device_info["firmware"], "V1.00")

    def test_parse_full_idn(self):
        """测试解析完整IDN响应"""
        response = "HIOKI,LR8450,V1.00,123456,U8552-15,U8551-4"
        device_info = self.client.get_device_info()

        with patch.object(self.client, 'send_query', return_value=response):
            device_info = self.client.get_device_info()

        self.assertEqual(device_info["manufacturer"], "HIOKI")
        self.assertEqual(device_info["model"], "LR8450")
        self.assertEqual(device_info["firmware"], "V1.00")
        self.assertEqual(device_info["estimated_channels"], 19)  # 15+4

    def test_parse_malformed_response(self):
        """测试解析格式错误的响应"""
        response = "INVALID_RESPONSE"
        device_info = self.client.get_device_info()

        with patch.object(self.client, 'send_query', return_value=response):
            device_info = self.client.get_device_info()

        self.assertIsNotNone(device_info)
        self.assertEqual(device_info["raw_idn"], "INVALID_RESPONSE")


if __name__ == '__main__':
    # 创建测试套件
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSimpleDeviceClient)
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDeviceInfoParsing))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 退出码
    exit(0 if result.wasSuccessful() else 1)
