#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Battery Analyzer 主窗口（简体中文 UI 骨架）。

布局目标：
- 左侧控制面板：测试设置、导出报告、采集时长/点数、保存/召回波形、产品信息、开始按钮。
- 中部：双波形区域（左：三元电池；右：刀片电池）。
- 底部：关键指标 KPI（电压、温度），各自大号数字显示。

后续会把 LR8450 的实时采集与分析（温升比对、电压压降、mX+b、mAh）接入到相应槽函数。
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QStatusBar,
)

import pyqtgraph as pg


class KPIWidget(QWidget):
    """KPI 数字显示（标题 + 数值+单位在同一框内）。"""

    def __init__(self, title: str, unit: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.unit = unit

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("kpiTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setProperty("class", "kpiTitle")

        # 数值+单位放在同一个标签内
        self.value_label = QLabel(f"0.00{unit}")
        self.value_label.setObjectName("valueLabel")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setProperty("class", "kpi")
        self.value_label.setStyleSheet(
            "background-color: #0b213f; "
            "border: 1px solid #2b4b7d; "
            "border-radius: 6px; "
            "padding: 8px 12px; "
            "color: #98d2ff; "
            "font-weight: bold; "
            "font-size: 28px;"
        )

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value_text: str) -> None:
        """设置数值（自动附加单位）。"""
        self.value_label.setText(f"{value_text}{self.unit}")


class WaveformPair(QWidget):
    """双波形显示面板（每个图表有双Y轴：左侧电压，右侧温度）。"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QGridLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        # 左：三元电池
        self.left_title = QLabel("三元电池波形 (Ternary Battery Waveform)")
        self.left_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_title.setStyleSheet("color: #6dd5ed; font-size: 14px; font-weight: bold;")
        
        self.left_plot = self._create_dual_axis_plot()
        
        # 右：刀片电池
        self.right_title = QLabel("刀片电池波形 (Blade Battery Waveform)")
        self.right_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_title.setStyleSheet("color: #6dd5ed; font-size: 14px; font-weight: bold;")
        
        self.right_plot = self._create_dual_axis_plot()

        layout.addWidget(self.left_title, 0, 0)
        layout.addWidget(self.right_title, 0, 1)
        layout.addWidget(self.left_plot, 1, 0)
        layout.addWidget(self.right_plot, 1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

    def _create_dual_axis_plot(self) -> pg.PlotWidget:
        """创建带双Y轴的图表（左：电压，右：温度）。"""
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground("#0c1830")
        
        # 隐藏左下角的 AutoRange 按钮（A按钮）
        plot_widget.plotItem.hideButtons()
        
        # 左Y轴：电压（V）
        plot_widget.setLabel('left', '电压 V', color='#33c1ff', **{'font-size': '11pt'})
        plot_widget.setYRange(0, 10)
        plot_widget.getAxis('left').setPen(pg.mkPen('#33c1ff', width=2))
        plot_widget.getAxis('left').setTextPen('#33c1ff')
        
        # 底部X轴：时间（Time）
        plot_widget.setLabel('bottom', '时间 Time', units='s', color='#6dd5ed', **{'font-size': '11pt'})
        plot_widget.setXRange(0, 300)
        plot_widget.getAxis('bottom').setPen(pg.mkPen('#4a90e2', width=2))
        plot_widget.getAxis('bottom').setTextPen('#6dd5ed')
        
        # 右Y轴：温度（T）
        viewbox_temp = pg.ViewBox()
        plot_widget.plotItem.scene().addItem(viewbox_temp)
        plot_widget.plotItem.getAxis('right').linkToView(viewbox_temp)
        viewbox_temp.setXLink(plot_widget.plotItem)
        
        # 配置右轴
        plot_widget.plotItem.showAxis('right')
        plot_widget.setLabel('right', '温度 T', units='°C', color='#ffb347', **{'font-size': '11pt'})
        plot_widget.getAxis('right').setPen(pg.mkPen('#ffb347', width=2))
        plot_widget.getAxis('right').setTextPen('#ffb347')
        
        # 同步右侧 ViewBox 的几何位置
        def update_views():
            viewbox_temp.setGeometry(plot_widget.plotItem.vb.sceneBoundingRect())
            viewbox_temp.linkedViewChanged(plot_widget.plotItem.vb, viewbox_temp.XAxis)
        
        update_views()
        plot_widget.plotItem.vb.sigResized.connect(update_views)
        
        # 设置温度轴范围
        viewbox_temp.setYRange(0, 260)
        
        # 存储 viewbox 以便后续绘图
        plot_widget.viewbox_temp = viewbox_temp
        
        # 网格
        plot_widget.showGrid(x=True, y=True, alpha=0.15)
        
        return plot_widget


class ControlPanel(QWidget):
    """左侧控制面板。"""

    start_requested = Signal()
    voltage_color_changed = Signal(str)  # 电压颜色改变信号
    temp_color_changed = Signal(str)     # 温度颜色改变信号

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)

        # 操作区
        ops = QGroupBox("操作")
        ops_layout = QVBoxLayout(ops)
        self.btn_testing = QPushButton("测试设置")
        self.btn_report = QPushButton("导出报告")
        self.btn_acq_time = QPushButton("采集时长")
        self.btn_acq_points = QPushButton("采集点数")
        self.btn_save = QPushButton("保存波形")
        self.btn_recall = QPushButton("召回波形")
        ops_layout.addWidget(self.btn_testing)
        ops_layout.addWidget(self.btn_report)
        ops_layout.addWidget(self.btn_acq_time)
        ops_layout.addWidget(self.btn_acq_points)
        ops_layout.addWidget(self.btn_save)
        ops_layout.addWidget(self.btn_recall)

        # 通道与显示选项
        vis = QGroupBox("显示设置")
        vis_layout = QVBoxLayout(vis)
        vis_layout.setSpacing(8)
        
        # 电压行：标签 + 像素选择 + 颜色块
        volt_row = QHBoxLayout()
        volt_label = QLabel("电压")
        volt_label.setFixedWidth(40)
        volt_row.addWidget(volt_label)
        self.combo_volt_pix = QComboBox()
        self.combo_volt_pix.addItems(["1像素", "2像素", "3像素", "4像素"])
        self.combo_volt_pix.setCurrentIndex(2)  # 默认3像素
        self.combo_volt_pix.setFixedWidth(80)
        volt_row.addWidget(self.combo_volt_pix)
        self.volt_color_btn = QPushButton()
        self.volt_color_btn.setFixedSize(50, 22)
        self.volt_color_btn.setStyleSheet("background-color: #ff9933; border: 1px solid #2b4b7d; border-radius: 3px;")
        self.volt_color_btn.clicked.connect(lambda: self._choose_color("volt"))
        volt_row.addWidget(self.volt_color_btn)
        volt_row.addStretch()
        vis_layout.addLayout(volt_row)
        
        # 温度行：标签 + 像素选择 + 颜色块
        temp_row = QHBoxLayout()
        temp_label = QLabel("温度")
        temp_label.setFixedWidth(40)
        temp_row.addWidget(temp_label)
        self.combo_temp_pix = QComboBox()
        self.combo_temp_pix.addItems(["1像素", "2像素", "3像素", "4像素"])
        self.combo_temp_pix.setCurrentIndex(2)  # 默认3像素
        self.combo_temp_pix.setFixedWidth(80)
        temp_row.addWidget(self.combo_temp_pix)
        self.temp_color_btn = QPushButton()
        self.temp_color_btn.setFixedSize(50, 22)
        self.temp_color_btn.setStyleSheet("background-color: #66ccff; border: 1px solid #2b4b7d; border-radius: 3px;")
        self.temp_color_btn.clicked.connect(lambda: self._choose_color("temp"))
        temp_row.addWidget(self.temp_color_btn)
        temp_row.addStretch()
        vis_layout.addLayout(temp_row)
        
        # 存储当前颜色
        self.volt_color = "#ff9933"
        self.temp_color = "#66ccff"

        # 产品信息（上下排列，紧凑布局）
        info = QGroupBox("产品信息")
        info_layout = QVBoxLayout(info)
        info_layout.setSpacing(6)
        
        # 产品型号
        info_layout.addWidget(QLabel("产品型号"))
        self.edit_model = QLineEdit("5mm")
        self.edit_model.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_model.setStyleSheet("font-size: 18px; font-weight: bold; color: #33c1ff; padding: 6px;")
        info_layout.addWidget(self.edit_model)
        
        # 产品流水号
        info_layout.addWidget(QLabel("产品流水号"))
        self.edit_sn = QLineEdit("25mm/s")
        self.edit_sn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_sn.setStyleSheet("font-size: 18px; font-weight: bold; color: #33c1ff; padding: 6px;")
        info_layout.addWidget(self.edit_sn)
        
        # 测试员
        info_layout.addWidget(QLabel("测试员"))
        self.edit_tester = QLineEdit("1dot/s")
        self.edit_tester.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_tester.setStyleSheet("font-size: 18px; font-weight: bold; color: #33c1ff; padding: 6px;")
        info_layout.addWidget(self.edit_tester)

        # 开始按钮
        self.btn_start = QPushButton("开始")
        self.btn_start.setObjectName("startButton")
        self.btn_start.clicked.connect(self.start_requested.emit)

        root.addWidget(ops)
        root.addWidget(vis)
        root.addWidget(info)
        root.addStretch(1)
        root.addWidget(self.btn_start)
    
    def _choose_color(self, channel: str) -> None:
        """选择通道颜色。"""
        from PySide6.QtGui import QColor
        from battery_analyzer.ui.color_dialog import SimpleColorDialog
        
        # 获取当前颜色
        current_color = QColor(self.volt_color if channel == "volt" else self.temp_color)
        
        # 打开自定义中文颜色选择对话框
        title = "选择电压颜色" if channel == "volt" else "选择温度颜色"
        color = SimpleColorDialog.get_color_from_dialog(current_color, title, self)
        
        if color and color.isValid():
            color_hex = color.name()
            if channel == "volt":
                self.volt_color = color_hex
                self.volt_color_btn.setStyleSheet(
                    f"background-color: {color_hex}; border: 1px solid #2b4b7d; border-radius: 3px;"
                )
                # 发射信号通知主窗口更新电压曲线颜色
                self.voltage_color_changed.emit(color_hex)
            else:
                self.temp_color = color_hex
                self.temp_color_btn.setStyleSheet(
                    f"background-color: {color_hex}; border: 1px solid #2b4b7d; border-radius: 3px;"
                )
                # 发射信号通知主窗口更新温度曲线颜色
                self.temp_color_changed.emit(color_hex)


class MainWindow(QMainWindow):
    """主窗口。"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("电池电压与温升分析软件")
        self.resize(1280, 800)

        # 中央布局（包含顶部标题栏）
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部标题栏
        title_bar = self._create_title_bar()
        main_layout.addWidget(title_bar)

        # 主内容区域
        content = QWidget()
        hbox = QHBoxLayout(content)
        hbox.setContentsMargins(8, 8, 8, 8)
        hbox.setSpacing(12)

        # 左侧控制
        self.control = ControlPanel()
        self.control.setFixedWidth(260)
        self.control.start_requested.connect(self._on_start)
        self.control.voltage_color_changed.connect(self.update_voltage_color)
        self.control.temp_color_changed.connect(self.update_temp_color)

        # 中部双波形
        self.waveforms = WaveformPair()

        # 底部 KPI 区域（4个KPI：左侧2个三元电池，右侧2个刀片电池）
        bottom = QWidget()
        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(12)
        
        # 三元电池电压
        self.ternary_voltage_kpi = KPIWidget("三元电池电压\nTernary Battery Voltage", "V")
        bottom_layout.addWidget(self.ternary_voltage_kpi)
        
        # 三元电池温度
        self.ternary_temp_kpi = KPIWidget("三元电池温度\nTernary Battery Temperature", "°C")
        bottom_layout.addWidget(self.ternary_temp_kpi)
        
        # 刀片电池电压
        self.blade_voltage_kpi = KPIWidget("刀片电池电压\nBlade Battery Voltage", "V")
        bottom_layout.addWidget(self.blade_voltage_kpi)
        
        # 刀片电池温度
        self.blade_temp_kpi = KPIWidget("刀片电池温度\nBlade Battery Temperature", "°C")
        bottom_layout.addWidget(self.blade_temp_kpi)

        # 将中部区域组装为上下两块
        center_col = QWidget()
        center_layout = QVBoxLayout(center_col)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(12)
        center_layout.addWidget(self.waveforms, 1)
        center_layout.addWidget(bottom, 0)

        hbox.addWidget(self.control, 0)
        hbox.addWidget(center_col, 1)

        main_layout.addWidget(content, 1)

        # 状态栏
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage("就绪——等待连接与开始测试")

        # 存储曲线对象以便更新颜色
        self.volt_curves = []  # [左图电压曲线, 右图电压曲线]
        self.temp_curves = []  # [左图温度曲线, 右图温度曲线]
        
        # 虚拟数据生成
        self.is_running = False
        self.data_index = 0
        self.max_points = 600  # 最多显示600个点（300秒）
        
        # 数据缓冲区
        self.x_data = []
        self.ternary_volt_data = []
        self.ternary_temp_data = []
        self.blade_volt_data = []
        self.blade_temp_data = []
        
        # 当前颜色（从控制面板获取）
        self.current_volt_color = "#ff9933"
        self.current_temp_color = "#66ccff"
        
        # 定时器：每100ms更新一次数据
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_waveform)
        
        # 预置示例波形（初始静态数据）
        self._plot_demo()

    def _plot_demo(self) -> None:
        """绘制示例波形（电压在左Y轴，温度在右Y轴）。"""
        import numpy as np

        x = np.linspace(0, 300, 600)
        
        # 三元电池数据
        y_v_ternary = 5 + 0.3 * np.sin(0.05 * x) + 0.1 * np.random.randn(600)  # 电压 0-10V
        y_t_ternary = 130 + 50 * np.sin(0.02 * x + 1.2) + 5 * np.random.randn(600)  # 温度 0-260°C
        
        # 刀片电池数据
        y_v_blade = 5.2 + 0.25 * np.sin(0.05 * x + 0.4) + 0.08 * np.random.randn(600)
        y_t_blade = 120 + 40 * np.sin(0.02 * x + 2.0) + 4 * np.random.randn(600)

        # 左图：三元电池
        # 电压曲线（左Y轴，主ViewBox）
        volt_curve_left = self.waveforms.left_plot.plot(x, y_v_ternary, pen=pg.mkPen(self.current_volt_color, width=2), name="电压")
        self.volt_curves.append(volt_curve_left)
        
        # 温度曲线（右Y轴，viewbox_temp）
        temp_curve_left = pg.PlotCurveItem(x, y_t_ternary, pen=pg.mkPen(self.current_temp_color, width=2), name="温度")
        self.waveforms.left_plot.viewbox_temp.addItem(temp_curve_left)
        self.temp_curves.append(temp_curve_left)

        # 右图：刀片电池
        # 电压曲线（左Y轴）
        volt_curve_right = self.waveforms.right_plot.plot(x, y_v_blade, pen=pg.mkPen(self.current_volt_color, width=2), name="电压")
        self.volt_curves.append(volt_curve_right)
        
        # 温度曲线（右Y轴）
        temp_curve_right = pg.PlotCurveItem(x, y_t_blade, pen=pg.mkPen(self.current_temp_color, width=2), name="温度")
        self.waveforms.right_plot.viewbox_temp.addItem(temp_curve_right)
        self.temp_curves.append(temp_curve_right)

        # 初始化 KPI
        self.ternary_voltage_kpi.set_value("0.00")
        self.ternary_temp_kpi.set_value("0.00")
        self.blade_voltage_kpi.set_value("0.00")
        self.blade_temp_kpi.set_value("0.00")

    def _create_title_bar(self) -> QWidget:
        """创建顶部标题栏（科技风格）。"""
        title_container = QWidget()
        title_container.setObjectName("titleBar")
        title_container.setFixedHeight(60)
        title_container.setStyleSheet("""
            QWidget#titleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0a1a35, stop:0.5 #0c1f3f, stop:1 #0a1a35);
                border-bottom: 2px solid #1a4d7d;
            }
            QLabel#mainTitle {
                color: #6dd5ed;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 2px;
            }
            QPushButton#titleBtn {
                background-color: transparent;
                color: #6dd5ed;
                border: 1px solid #2b5a8a;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 13px;
            }
            QPushButton#titleBtn:hover {
                background-color: #1a3a5f;
                border-color: #4a8fdd;
            }
        """)

        layout = QHBoxLayout(title_container)
        layout.setContentsMargins(20, 10, 20, 10)

        layout.addStretch()
        
        # 主标题
        title = QLabel("电池电压与温升采集软件")
        title.setObjectName("mainTitle")
        layout.addWidget(title)

        layout.addStretch()

        # 帮助按钮
        btn_help = QPushButton("❓ Help")
        btn_help.setObjectName("titleBtn")
        btn_help.clicked.connect(self._show_help)
        layout.addWidget(btn_help)

        # 退出按钮
        btn_exit = QPushButton("✖ Exit")
        btn_exit.setObjectName("titleBtn")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        return title_container

    def _show_help(self) -> None:
        """显示帮助信息。"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "帮助",
            "电池电压与温升分析软件\n\n"
            "功能：\n"
            "• 三元电池与刀片电池温升比对\n"
            "• 电池压降采集分析\n"
            "• mX+b 线性校准\n"
            "• mAh 容量测试\n\n"
            "后续将接入 LR8450 设备进行实时数据采集。"
        )

    def update_voltage_color(self, color_hex: str) -> None:
        """更新电压曲线颜色。"""
        self.current_volt_color = color_hex  # 更新当前颜色
        for curve in self.volt_curves:
            curve.setPen(pg.mkPen(color_hex, width=2))
        self.statusBar().showMessage(f"电压曲线颜色已更新为 {color_hex}")
    
    def update_temp_color(self, color_hex: str) -> None:
        """更新温度曲线颜色。"""
        self.current_temp_color = color_hex  # 更新当前颜色
        for curve in self.temp_curves:
            curve.setPen(pg.mkPen(color_hex, width=2))
        self.statusBar().showMessage(f"温度曲线颜色已更新为 {color_hex}")
    
    def _update_waveform(self) -> None:
        """定时更新波形（虚拟数据）。"""
        import numpy as np
        
        # 生成新的数据点
        t = self.data_index * 0.5  # 每0.5秒一个点
        
        # 三元电池数据（带随机波动）
        v_ternary = 5 + 0.3 * np.sin(0.05 * t) + 0.1 * np.random.randn()
        t_ternary = 130 + 50 * np.sin(0.02 * t + 1.2) + 5 * np.random.randn()
        
        # 刀片电池数据（温度略低）
        v_blade = 5.2 + 0.25 * np.sin(0.05 * t + 0.4) + 0.08 * np.random.randn()
        t_blade = 120 + 40 * np.sin(0.02 * t + 2.0) + 4 * np.random.randn()
        
        # 添加到缓冲区
        self.x_data.append(t)
        self.ternary_volt_data.append(v_ternary)
        self.ternary_temp_data.append(t_ternary)
        self.blade_volt_data.append(v_blade)
        self.blade_temp_data.append(t_blade)
        
        # 限制数据点数量（滚动显示）
        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.ternary_volt_data.pop(0)
            self.ternary_temp_data.pop(0)
            self.blade_volt_data.pop(0)
            self.blade_temp_data.pop(0)
        
        # 更新曲线
        if len(self.volt_curves) >= 2 and len(self.temp_curves) >= 2:
            # 左图：三元电池
            self.volt_curves[0].setData(self.x_data, self.ternary_volt_data)
            self.temp_curves[0].setData(self.x_data, self.ternary_temp_data)
            
            # 右图：刀片电池
            self.volt_curves[1].setData(self.x_data, self.blade_volt_data)
            self.temp_curves[1].setData(self.x_data, self.blade_temp_data)
        
        # 更新KPI显示（显示最新值）
        self.ternary_voltage_kpi.set_value(f"{v_ternary:.2f}")
        self.ternary_temp_kpi.set_value(f"{t_ternary:.2f}")
        self.blade_voltage_kpi.set_value(f"{v_blade:.2f}")
        self.blade_temp_kpi.set_value(f"{t_blade:.2f}")
        
        self.data_index += 1
    
    # 槽函数：开始/停止虚拟数据采集
    def _on_start(self) -> None:
        """开始虚拟数据采集。"""
        if not self.is_running:
            self.is_running = True
            self.data_index = 0
            self.x_data.clear()
            self.ternary_volt_data.clear()
            self.ternary_temp_data.clear()
            self.blade_volt_data.clear()
            self.blade_temp_data.clear()
            
            # 启动定时器（100ms更新一次）
            self.update_timer.start(100)
            
            self.statusBar().showMessage("虚拟数据采集进行中...")
            self.control.btn_start.setText("停止")
            self.control.btn_start.clicked.disconnect()
            self.control.btn_start.clicked.connect(self._on_stop)
    
    def _on_stop(self) -> None:
        """停止虚拟数据采集。"""
        if self.is_running:
            self.is_running = False
            self.update_timer.stop()
            
            self.statusBar().showMessage("虚拟数据采集已停止")
            self.control.btn_start.setText("开始")
            self.control.btn_start.clicked.disconnect()
            self.control.btn_start.clicked.connect(self._on_start)
