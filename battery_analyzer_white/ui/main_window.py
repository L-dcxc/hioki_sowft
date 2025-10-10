#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Battery Analyzer White Theme - 主窗口（顶部控制+横向波形布局）。"""

from __future__ import annotations

from typing import Optional
import numpy as np

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QStatusBar, QSplitter,
)

import pyqtgraph as pg


class KPICard(QWidget):
    """KPI 卡片（白色简洁风格）。"""

    def __init__(self, title: str, unit: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        
        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "kpiTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.value_label = QLabel(f"0.00{unit}")
        self.value_label.setProperty("class", "kpi")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setMinimumHeight(50)  # 确保有足够高度
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
    
    def set_value(self, value: str) -> None:
        self.value_label.setText(f"{value}{self.unit}")


class MainWindow(QMainWindow):
    """白色主题主窗口 - 顶部控制 + 横向波形。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("电池分析软件 - 简洁版")
        self.resize(1400, 900)
        
        # 数据管理
        self.is_running = False
        self.data_index = 0
        self.max_points = 600
        self.x_data = []
        self.ternary_v = []
        self.ternary_t = []
        self.blade_v = []
        self.blade_t = []
        
        self.volt_color = "#e74c3c"
        self.temp_color = "#3498db"
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 顶部标题栏
        main_layout.addWidget(self._create_title_bar())
        
        # 控制栏（横向布局）
        main_layout.addWidget(self._create_control_bar())
        
        # 波形区域（横向排列：左边三元，右边刀片）
        waveform_container = QWidget()
        waveform_layout = QHBoxLayout(waveform_container)
        waveform_layout.setContentsMargins(12, 12, 12, 12)
        waveform_layout.setSpacing(16)
        
        # 左图：三元电池
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(8)
        left_title = QLabel("三元电池 Ternary Battery")
        left_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.left_plot = self._create_plot()
        left_layout.addWidget(left_title)
        left_layout.addWidget(self.left_plot, 1)
        
        # 右图：刀片电池
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(8)
        right_title = QLabel("刀片电池 Blade Battery")
        right_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.right_plot = self._create_plot()
        right_layout.addWidget(right_title)
        right_layout.addWidget(self.right_plot, 1)
        
        waveform_layout.addWidget(left_container, 1)
        waveform_layout.addWidget(right_container, 1)
        
        main_layout.addWidget(waveform_container, 1)
        
        # 底部KPI横条
        kpi_bar = QWidget()
        kpi_bar.setFixedHeight(120)
        kpi_bar.setStyleSheet("background-color: #ffffff;")
        kpi_layout = QHBoxLayout(kpi_bar)
        kpi_layout.setContentsMargins(16, 12, 16, 12)
        kpi_layout.setSpacing(12)
        
        self.ternary_v_kpi = KPICard("三元电压", "V")
        self.ternary_t_kpi = KPICard("三元温度", "°C")
        self.blade_v_kpi = KPICard("刀片电压", "V")
        self.blade_t_kpi = KPICard("刀片温度", "°C")
        
        kpi_layout.addWidget(self.ternary_v_kpi)
        kpi_layout.addWidget(self.ternary_t_kpi)
        kpi_layout.addWidget(self.blade_v_kpi)
        kpi_layout.addWidget(self.blade_t_kpi)
        
        main_layout.addWidget(kpi_bar)
        
        # 状态栏
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage("就绪 - 点击开始进行数据采集")
        
        # 定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_data)
        
        # 初始化曲线
        self.volt_curves = []
        self.temp_curves = []
        self._init_plots()
    
    def _create_title_bar(self) -> QWidget:
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        layout.addStretch()
        title = QLabel("电池电压与温升分析系统")
        title.setObjectName("mainTitle")
        layout.addWidget(title)
        layout.addStretch()
        
        btn_help = QPushButton("帮助")
        btn_help.setObjectName("titleBtn")
        layout.addWidget(btn_help)
        
        btn_exit = QPushButton("退出")
        btn_exit.setObjectName("titleBtn")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)
        
        return title_bar
    
    def _create_control_bar(self) -> QWidget:
        control_bar = QWidget()
        control_bar.setObjectName("controlBar")
        control_bar.setFixedHeight(80)
        
        layout = QHBoxLayout(control_bar)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 产品信息输入
        layout.addWidget(QLabel("型号:"))
        self.edit_model = QLineEdit("BT-2024")
        self.edit_model.setFixedWidth(120)
        layout.addWidget(self.edit_model)
        
        layout.addWidget(QLabel("流水号:"))
        self.edit_sn = QLineEdit("SN-001")
        self.edit_sn.setFixedWidth(120)
        layout.addWidget(self.edit_sn)
        
        layout.addWidget(QLabel("测试员:"))
        self.edit_tester = QLineEdit("张工")
        self.edit_tester.setFixedWidth(100)
        layout.addWidget(self.edit_tester)
        
        layout.addStretch()
        
        # 颜色选择
        layout.addWidget(QLabel("电压色:"))
        self.volt_color_btn = QPushButton()
        self.volt_color_btn.setFixedSize(60, 30)
        self.volt_color_btn.setStyleSheet(f"background-color: {self.volt_color}; border: 2px solid #bdc3c7;")
        layout.addWidget(self.volt_color_btn)
        
        layout.addWidget(QLabel("温度色:"))
        self.temp_color_btn = QPushButton()
        self.temp_color_btn.setFixedSize(60, 30)
        self.temp_color_btn.setStyleSheet(f"background-color: {self.temp_color}; border: 2px solid #bdc3c7;")
        layout.addWidget(self.temp_color_btn)
        
        layout.addStretch()
        
        # 开始按钮
        self.btn_start = QPushButton("开始采集")
        self.btn_start.setObjectName("startButton")
        self.btn_start.clicked.connect(self._toggle_acquisition)
        layout.addWidget(self.btn_start)
        
        return control_bar
    
    def _create_plot(self) -> pg.PlotWidget:
        plot = pg.PlotWidget()
        plot.setBackground("#ffffff")
        plot.plotItem.hideButtons()
        plot.showGrid(x=True, y=True, alpha=0.3)
        
        # 双Y轴
        plot.setLabel('left', '电压 V', color='#e74c3c')
        plot.setYRange(0, 10)
        plot.getAxis('left').setPen('#e74c3c')
        plot.getAxis('left').setTextPen('#e74c3c')
        
        plot.setLabel('bottom', '时间 s', color='#7f8c8d')
        plot.setXRange(0, 300)
        plot.getAxis('bottom').setPen('#7f8c8d')
        plot.getAxis('bottom').setTextPen('#7f8c8d')
        
        viewbox_temp = pg.ViewBox()
        plot.plotItem.scene().addItem(viewbox_temp)
        plot.plotItem.getAxis('right').linkToView(viewbox_temp)
        viewbox_temp.setXLink(plot.plotItem)
        
        plot.plotItem.showAxis('right')
        plot.setLabel('right', '温度 °C', color='#3498db')
        plot.getAxis('right').setPen('#3498db')
        plot.getAxis('right').setTextPen('#3498db')
        
        def update_views():
            viewbox_temp.setGeometry(plot.plotItem.vb.sceneBoundingRect())
            viewbox_temp.linkedViewChanged(plot.plotItem.vb, viewbox_temp.XAxis)
        
        update_views()
        plot.plotItem.vb.sigResized.connect(update_views)
        viewbox_temp.setYRange(0, 260)
        plot.viewbox_temp = viewbox_temp
        
        return plot
    
    def _init_plots(self) -> None:
        x = np.linspace(0, 300, 600)
        
        v_left = self.left_plot.plot(x, x*0, pen=pg.mkPen(self.volt_color, width=2))
        t_left = pg.PlotCurveItem(x, x*0, pen=pg.mkPen(self.temp_color, width=2))
        self.left_plot.viewbox_temp.addItem(t_left)
        
        v_right = self.right_plot.plot(x, x*0, pen=pg.mkPen(self.volt_color, width=2))
        t_right = pg.PlotCurveItem(x, x*0, pen=pg.mkPen(self.temp_color, width=2))
        self.right_plot.viewbox_temp.addItem(t_right)
        
        self.volt_curves = [v_left, v_right]
        self.temp_curves = [t_left, t_right]
    
    def _toggle_acquisition(self) -> None:
        if not self.is_running:
            self.is_running = True
            self.data_index = 0
            self.x_data.clear()
            self.ternary_v.clear()
            self.ternary_t.clear()
            self.blade_v.clear()
            self.blade_t.clear()
            self.update_timer.start(100)
            self.btn_start.setText("停止采集")
            self.statusBar().showMessage("数据采集中...")
        else:
            self.is_running = False
            self.update_timer.stop()
            self.btn_start.setText("开始采集")
            self.statusBar().showMessage("已停止")
    
    def _update_data(self) -> None:
        t = self.data_index * 0.5
        
        v_t = 5 + 0.3 * np.sin(0.05 * t) + 0.1 * np.random.randn()
        t_t = 130 + 50 * np.sin(0.02 * t + 1.2) + 5 * np.random.randn()
        v_b = 5.2 + 0.25 * np.sin(0.05 * t + 0.4) + 0.08 * np.random.randn()
        t_b = 120 + 40 * np.sin(0.02 * t + 2.0) + 4 * np.random.randn()
        
        self.x_data.append(t)
        self.ternary_v.append(v_t)
        self.ternary_t.append(t_t)
        self.blade_v.append(v_b)
        self.blade_t.append(t_b)
        
        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.ternary_v.pop(0)
            self.ternary_t.pop(0)
            self.blade_v.pop(0)
            self.blade_t.pop(0)
        
        self.volt_curves[0].setData(self.x_data, self.ternary_v)
        self.temp_curves[0].setData(self.x_data, self.ternary_t)
        self.volt_curves[1].setData(self.x_data, self.blade_v)
        self.temp_curves[1].setData(self.x_data, self.blade_t)
        
        self.ternary_v_kpi.set_value(f"{v_t:.2f}")
        self.ternary_t_kpi.set_value(f"{t_t:.2f}")
        self.blade_v_kpi.set_value(f"{v_b:.2f}")
        self.blade_t_kpi.set_value(f"{t_b:.2f}")
        
        self.data_index += 1

