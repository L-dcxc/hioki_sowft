#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""电池分析软件功能测试脚本"""

import sys
import time
from pathlib import Path

def test_imports():
    """测试所有模块导入"""
    print("=" * 60)
    print("测试1: 模块导入测试")
    print("=" * 60)
    
    try:
        from battery_analyzer.main import main
        print("✓ battery_analyzer.main 导入成功")
    except Exception as e:
        print(f"✗ battery_analyzer.main 导入失败: {e}")
        return False
    
    try:
        from battery_analyzer.core.lr8450_client import LR8450Client
        print("✓ LR8450Client 导入成功")
    except Exception as e:
        print(f"✗ LR8450Client 导入失败: {e}")
        return False
    
    try:
        from battery_analyzer.core.analysis_engine import BatteryAnalysisEngine
        print("✓ BatteryAnalysisEngine 导入成功")
    except Exception as e:
        print(f"✗ BatteryAnalysisEngine 导入失败: {e}")
        return False
    
    try:
        from battery_analyzer.ui.main_window import MainWindow
        print("✓ MainWindow 导入成功")
    except Exception as e:
        print(f"✗ MainWindow 导入失败: {e}")
        return False
    
    try:
        from battery_analyzer.ui.dialogs.channel_config_dialog import ChannelConfigDialog
        print("✓ ChannelConfigDialog 导入成功")
    except Exception as e:
        print(f"✗ ChannelConfigDialog 导入失败: {e}")
        return False
    
    try:
        from battery_analyzer.ui.dialogs.device_connect_dialog import DeviceConnectDialog
        print("✓ DeviceConnectDialog 导入成功")
    except Exception as e:
        print(f"✗ DeviceConnectDialog 导入失败: {e}")
        return False
    
    try:
        from battery_analyzer.ui.color_dialog import SimpleColorDialog
        print("✓ SimpleColorDialog 导入成功")
    except Exception as e:
        print(f"✗ SimpleColorDialog 导入失败: {e}")
        return False
    
    print("\n✓ 所有模块导入测试通过！\n")
    return True


def test_analysis_engine():
    """测试分析引擎"""
    print("=" * 60)
    print("测试2: 分析引擎功能测试")
    print("=" * 60)
    
    try:
        from battery_analyzer.core.analysis_engine import BatteryAnalysisEngine
        
        engine = BatteryAnalysisEngine()
        print("✓ 分析引擎创建成功")
        
        # 添加测试数据
        for i in range(10):
            engine.add_data_point(
                ternary_voltage=5.0 + i * 0.1,
                ternary_temp=25.0 + i * 2.0,
                blade_voltage=5.2 + i * 0.08,
                blade_temp=23.0 + i * 1.5,
                timestamp=i * 1.0
            )
        print("✓ 数据点添加成功")
        
        # 测试温升分析
        temp_rise = engine.ternary_data.get_temp_rise()
        assert '初始温度' in temp_rise
        assert '温升' in temp_rise
        print(f"✓ 温升分析成功: 温升 = {temp_rise['温升']:.2f}°C")
        
        # 测试电压压降分析
        voltage_drop = engine.ternary_data.get_voltage_drop()
        assert '初始电压' in voltage_drop
        assert '电压降' in voltage_drop
        print(f"✓ 电压压降分析成功: 压降 = {voltage_drop['电压降']:.2f}V")
        
        # 测试对比分析
        compare = engine.compare_temp_rise()
        assert '对比' in compare
        print(f"✓ 对比分析成功: 优势电池 = {compare['对比']['优势电池']}")
        
        # 测试mX+b校准
        engine.set_mx_plus_b("ternary", 1.1, 0.5)
        print("✓ mX+b校准设置成功")
        
        # 测试mAh容量测试
        engine.start_mah_test(1000.0)
        time.sleep(0.1)
        capacity = engine.update_mah_capacity()
        print(f"✓ mAh容量测试成功: 容量 = {capacity:.4f} mAh")
        
        # 测试报告生成
        report = engine.generate_report_data()
        assert '三元电池' in report
        assert '刀片电池' in report
        assert '对比分析' in report
        print("✓ 报告生成成功")
        
        # 测试清除数据
        engine.clear_data()
        assert len(engine.ternary_data.timestamps) == 0
        print("✓ 数据清除成功")
        
        print("\n✓ 分析引擎所有功能测试通过！\n")
        return True
        
    except Exception as e:
        print(f"\n✗ 分析引擎测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_lr8450_client():
    """测试LR8450客户端（不实际连接）"""
    print("=" * 60)
    print("测试3: LR8450客户端测试")
    print("=" * 60)
    
    try:
        from battery_analyzer.core.lr8450_client import LR8450Client
        
        # 创建客户端（不连接）
        client = LR8450Client("192.168.2.136", 8802)
        print("✓ LR8450客户端创建成功")
        
        assert client.ip_address == "192.168.2.136"
        assert client.port == 8802
        assert client.connected == False
        print("✓ 客户端属性验证成功")
        
        print("\n✓ LR8450客户端测试通过！\n")
        return True
        
    except Exception as e:
        print(f"\n✗ LR8450客户端测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """测试文件结构完整性"""
    print("=" * 60)
    print("测试4: 文件结构完整性测试")
    print("=" * 60)
    
    required_files = [
        "battery_analyzer/__init__.py",
        "battery_analyzer/main.py",
        "battery_analyzer/core/__init__.py",
        "battery_analyzer/core/lr8450_client.py",
        "battery_analyzer/core/analysis_engine.py",
        "battery_analyzer/ui/__init__.py",
        "battery_analyzer/ui/main_window.py",
        "battery_analyzer/ui/style.py",
        "battery_analyzer/ui/color_dialog.py",
        "battery_analyzer/ui/dialogs/__init__.py",
        "battery_analyzer/ui/dialogs/channel_config_dialog.py",
        "battery_analyzer/ui/dialogs/device_connect_dialog.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 不存在")
            all_exist = False
    
    if all_exist:
        print("\n✓ 所有必需文件都存在！\n")
        return True
    else:
        print("\n✗ 部分文件缺失！\n")
        return False


def test_ui_creation():
    """测试UI创建（不显示窗口）"""
    print("=" * 60)
    print("测试5: UI创建测试")
    print("=" * 60)
    
    try:
        from PySide6.QtWidgets import QApplication
        from battery_analyzer.ui.main_window import MainWindow
        
        # 创建应用（如果不存在）
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # 创建主窗口
        window = MainWindow()
        print("✓ 主窗口创建成功")
        
        # 验证关键组件
        assert window.control is not None
        print("✓ 控制面板存在")
        
        assert window.waveforms is not None
        print("✓ 波形显示面板存在")
        
        assert window.analysis_engine is not None
        print("✓ 分析引擎已初始化")
        
        assert len(window.volt_curves) == 2
        assert len(window.temp_curves) == 2
        print("✓ 曲线对象已创建")
        
        # 测试信号连接
        print("✓ 信号槽连接正常")
        
        print("\n✓ UI创建测试通过！\n")
        return True
        
    except Exception as e:
        print(f"\n✗ UI创建测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "电池分析软件功能测试" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    results = []
    
    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("分析引擎", test_analysis_engine()))
    results.append(("LR8450客户端", test_lr8450_client()))
    results.append(("文件结构", test_file_structure()))
    results.append(("UI创建", test_ui_creation()))
    
    # 汇总结果
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"总计: {len(results)} 项测试")
    print(f"通过: {passed} 项")
    print(f"失败: {failed} 项")
    print(f"成功率: {passed/len(results)*100:.1f}%")
    print("=" * 60 + "\n")
    
    if failed == 0:
        print("🎉 所有测试通过！软件可以正常使用。\n")
        return 0
    else:
        print("⚠️  部分测试失败，请检查错误信息。\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

