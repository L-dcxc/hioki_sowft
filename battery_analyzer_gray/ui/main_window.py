#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Battery Analyzer Gray Theme - 主窗口（卡片式布局）。"""

from __future__ import annotations

from typing import Optional
import numpy as np

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QStatusBar, QGroupBox, QFormLayout,
    QDialog, QRadioButton, QMessageBox,
)

import pyqtgraph as pg


class DataCard(QWidget):
    """数据卡片组件。"""

    def __init__(self, title: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)
        
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
    
    def add_content(self, widget: QWidget) -> None:
        self.content_layout.addWidget(widget)


class KPIDisplay(QWidget):
    """KPI显示组件。"""

    def __init__(self, label: str, unit: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        label_widget = QLabel(label)
        label_widget.setProperty("class", "kpiLabel")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.value_label = QLabel(f"0.00{unit}")
        self.value_label.setProperty("class", "kpiValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(label_widget)
        layout.addWidget(self.value_label)
    
    def set_value(self, value: str) -> None:
        self.value_label.setText(f"{value}{self.unit}")


class MainWindow(QMainWindow):
    """灰色主题主窗口 - 卡片式布局。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("电池分析软件 - 专业版")
        self.resize(1400, 900)
        
        self.is_running = False
        self.data_index = 0
        self.max_points = 600
        self.x_data = []
        self.ternary_v = []
        self.ternary_t = []
        self.blade_v = []
        self.blade_t = []

        self.volt_color = "#ff6b6b"
        self.temp_color = "#4ecdc4"

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 顶部工具栏
        main_layout.addWidget(self._create_toolbar())

        # 创建波形图表（先创建，再初始化）
        self.left_plot = self._create_plot()
        self.right_plot = self._create_plot()

        # 主内容区（垂直布局：上方波形，下方控制+KPI）
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(12)

        # 上方：波形显示区域（水平排列）
        waveform_container = QWidget()
        waveform_layout = QHBoxLayout(waveform_container)
        waveform_layout.setContentsMargins(0, 0, 0, 0)
        waveform_layout.setSpacing(12)

        # 左：三元电池波形
        ternary_card = DataCard("三元电池数据 Ternary Battery")
        ternary_card.add_content(self.left_plot)
        waveform_layout.addWidget(ternary_card)

        # 右：刀片电池波形
        blade_card = DataCard("刀片电池数据 Blade Battery")
        blade_card.add_content(self.right_plot)
        waveform_layout.addWidget(blade_card)

        content_layout.addWidget(waveform_container)

        # 下方：控制面板和KPI（水平排列）
        bottom_container = QWidget()
        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(12)

        # 左：控制面板
        control_section = QWidget()
        control_layout = QVBoxLayout(control_section)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(8)

        control_card = DataCard("控制面板")
        control_widget = self._create_controls()
        control_card.add_content(control_widget)
        control_layout.addWidget(control_card)

        bottom_layout.addWidget(control_section, 1)

        # 右：KPI显示
        kpi_section = QWidget()
        kpi_section.setStyleSheet("background-color: #353535; border: 1px solid #555555; border-radius: 8px;")
        kpi_layout = QGridLayout(kpi_section)
        kpi_layout.setContentsMargins(12, 12, 12, 12)
        kpi_layout.setSpacing(10)

        # 标题
        kpi_title = QLabel("实时数据监控")
        kpi_title.setObjectName("cardTitle")
        kpi_layout.addWidget(kpi_title, 0, 0, 1, 2)

        # 四个KPI显示（2x2网格）
        self.ternary_v_kpi = KPIDisplay("三元电压", "V")
        self.ternary_t_kpi = KPIDisplay("三元温度", "°C")
        self.blade_v_kpi = KPIDisplay("刀片电压", "V")
        self.blade_t_kpi = KPIDisplay("刀片温度", "°C")

        kpi_layout.addWidget(self.ternary_v_kpi, 1, 0)
        kpi_layout.addWidget(self.ternary_t_kpi, 1, 1)
        kpi_layout.addWidget(self.blade_v_kpi, 2, 0)
        kpi_layout.addWidget(self.blade_t_kpi, 2, 1)

        bottom_layout.addWidget(kpi_section, 1)

        content_layout.addWidget(bottom_container)

        main_layout.addWidget(content, 1)

        # 状态栏
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage("系统就绪")

        # 初始化数据和定时器（在所有组件创建完成后）
        self.is_running = False
        self.data_index = 0
        self.max_points = 600
        self.x_data = []
        self.ternary_v = []
        self.ternary_t = []
        self.blade_v = []
        self.blade_t = []

        self.volt_color = "#ff6b6b"
        self.temp_color = "#4ecdc4"

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_data)

        # 初始化曲线（在波形图表创建完成后）
        self._init_plots()

    def _create_toolbar(self) -> QWidget:
        toolbar = QWidget()
        toolbar.setObjectName("toolbar")
        toolbar.setFixedHeight(60)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(16, 10, 16, 10)
        
        title = QLabel("电池电压与温升分析系统")
        title.setObjectName("appTitle")
        layout.addWidget(title)
        
        layout.addStretch()
        
        btn_export = QPushButton("导出报告")
        layout.addWidget(btn_export)
        
        btn_settings = QPushButton("系统设置")
        layout.addWidget(btn_settings)
        
        return toolbar

    def _create_controls(self) -> QWidget:
        """创建控制面板（产品信息和显示设置）。"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        # 产品信息
        info_group = QGroupBox("产品信息")
        info_layout = QFormLayout(info_group)
        self.edit_model = QLineEdit("BT-PRO-2024")
        self.edit_sn = QLineEdit("SN-12345")
        self.edit_tester = QLineEdit("李工")
        info_layout.addRow("型号:", self.edit_model)
        info_layout.addRow("流水号:", self.edit_sn)
        info_layout.addRow("测试员:", self.edit_tester)
        layout.addWidget(info_group)

        # 颜色设置（简化版，只显示颜色块）
        color_group = QGroupBox("显示设置")
        color_layout = QVBoxLayout(color_group)

        volt_row = QHBoxLayout()
        volt_row.addWidget(QLabel("电压色:"))
        self.volt_color_btn = QPushButton()
        self.volt_color_btn.setFixedSize(80, 30)
        self.volt_color_btn.setStyleSheet(f"background-color: {self.volt_color}; border: 2px solid #555555;")
        volt_row.addWidget(self.volt_color_btn)
        volt_row.addStretch()
        color_layout.addLayout(volt_row)

        temp_row = QHBoxLayout()
        temp_row.addWidget(QLabel("温度色:"))
        self.temp_color_btn = QPushButton()
        self.temp_color_btn.setFixedSize(80, 30)
        self.temp_color_btn.setStyleSheet(f"background-color: {self.temp_color}; border: 2px solid #555555;")
        temp_row.addWidget(self.temp_color_btn)
        temp_row.addStretch()
        color_layout.addLayout(temp_row)

        layout.addWidget(color_group)

        layout.addStretch()

        # 开始按钮
        self.btn_start = QPushButton("开始测试")
        self.btn_start.setObjectName("actionBtn")
        self.btn_start.clicked.connect(self._toggle_acquisition)
        layout.addWidget(self.btn_start)

        return widget

    def _init_plots(self) -> None:
        """初始化波形图表曲线。"""
        x = np.linspace(0, 300, 600)

        # 清空现有曲线
        self.left_plot.clear()
        self.right_plot.clear()

        # 创建电压曲线（左Y轴）
        v_left = self.left_plot.plot(x, x*0, pen=pg.mkPen(self.volt_color, width=2))
        v_right = self.right_plot.plot(x, x*0, pen=pg.mkPen(self.volt_color, width=2))

        # 创建温度曲线（右Y轴）
        t_left = pg.PlotCurveItem(x, x*0, pen=pg.mkPen(self.temp_color, width=2))
        t_right = pg.PlotCurveItem(x, x*0, pen=pg.mkPen(self.temp_color, width=2))

        self.left_plot.viewbox_temp.addItem(t_left)
        self.right_plot.viewbox_temp.addItem(t_right)

        self.volt_curves = [v_left, v_right]
        self.temp_curves = [t_left, t_right]

    def _update_data(self) -> None:
        """更新虚拟数据。"""
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

        # 更新曲线
        if len(self.volt_curves) >= 2 and len(self.temp_curves) >= 2:
            self.volt_curves[0].setData(self.x_data, self.ternary_v)
            self.temp_curves[0].setData(self.x_data, self.ternary_t)
            self.volt_curves[1].setData(self.x_data, self.blade_v)
            self.temp_curves[1].setData(self.x_data, self.blade_t)

            # 更新KPI显示
            if hasattr(self, 'ternary_v_kpi'):
                self.ternary_v_kpi.set_value(f"{v_t:.2f}")
                self.ternary_t_kpi.set_value(f"{t_t:.2f}")
                self.blade_v_kpi.set_value(f"{v_b:.2f}")
                self.blade_t_kpi.set_value(f"{t_b:.2f}")

        self.data_index += 1

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
            self.btn_start.setText("停止测试")
            self.statusBar().showMessage("数据采集中...")
        else:
            self.is_running = False
            self.update_timer.stop()
            self.btn_start.setText("开始测试")
            self.statusBar().showMessage("已停止")

    def _create_plot(self) -> pg.PlotWidget:
        plot = pg.PlotWidget()
        plot.setBackground("#2b2b2b")
        plot.plotItem.hideButtons()
        plot.showGrid(x=True, y=True, alpha=0.2)
        
        plot.setLabel('left', '电压 V', color='#ff6b6b')
        plot.setYRange(0, 10)
        plot.getAxis('left').setPen('#ff6b6b')
        plot.getAxis('left').setTextPen('#ff6b6b')
        
        plot.setLabel('bottom', '时间 s', color='#b0b0b0')
        plot.setXRange(0, 300)
        plot.getAxis('bottom').setPen('#b0b0b0')
        plot.getAxis('bottom').setTextPen('#b0b0b0')
        
        viewbox_temp = pg.ViewBox()
        plot.plotItem.scene().addItem(viewbox_temp)
        plot.plotItem.getAxis('right').linkToView(viewbox_temp)
        viewbox_temp.setXLink(plot.plotItem)
        
        plot.plotItem.showAxis('right')
        plot.setLabel('right', '温度 °C', color='#4ecdc4')
        plot.getAxis('right').setPen('#4ecdc4')
        plot.getAxis('right').setTextPen('#4ecdc4')
        
        def update_views():
            viewbox_temp.setGeometry(plot.plotItem.vb.sceneBoundingRect())
            viewbox_temp.linkedViewChanged(plot.plotItem.vb, viewbox_temp.XAxis)
        
        update_views()
        plot.plotItem.vb.sigResized.connect(update_views)
        viewbox_temp.setYRange(0, 260)
        plot.viewbox_temp = viewbox_temp

        return plot