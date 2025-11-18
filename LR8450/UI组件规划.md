# PySide6 工程与组件规划

## 工程结构建议

```
project_sowf/
├─ app/
│  ├─ main.py              # 程序入口，初始化 QApplication & 主窗口
│  ├─ core/
│  │  ├─ config.py         # 全局配置/路径
│  │  ├─ state.py          # 应用状态、信号定义
│  │  ├─ device_manager.py # 设备发现/连接管理（占位）
│  │  └─ data_bus.py       # 采集数据分发接口（占位）
│  ├─ ui/
│  │  ├─ main_window.py    # QMainWindow 骨架
│  │  ├─ widgets/
│  │  │  ├─ waveform_panel.py
│  │  │  ├─ channel_sidebar.py
│  │  │  ├─ control_toolbar.py
│  │  │  ├─ status_bar.py
│  │  │  ├─ log_table.py
│  │  │  └─ setting_dialog/
│  │  │     ├─ __init__.py
│  │  │     ├─ connection_page.py
│  │  │     ├─ unit_page.py
│  │  │     ├─ channel_page.py
│  │  │     ├─ measure_page.py
│  │  │     └─ summary_page.py
│  │  ├─ style.py          # 全局样式表（工业风配色）
│  │  └─ resources/        # 图标/字体
│  └─ utils/
│     ├─ settings.py       # QSettings 封装
│     └─ validators.py     # 表单校验
└─ tests/ (后续补充)
```

## 主窗口组件

- `MainWindow` (`QMainWindow`)
  - 菜单栏 `File/View/Help`
  - 工具栏 `MainToolBar` → `control_toolbar.ControlToolBar`
  - 中央部件：`WaveformPanel`
  - 右侧 Dock：`ChannelSidebar`（含 Tab）
  - 底部 Dock：`DataTableDock`（日志/数值表）
  - 状态栏：`StatusBarWidget`

### WaveformPanel
- 基于 `pyqtgraph.GraphicsLayoutWidget`
- 包含：主波形视图、多页 Tab（10 页内）、时间轴缩放控件、A/B 光标条。
- 暂用模拟数据刷屏，验证 20FPS 左右渲染。

### ChannelSidebar
- `QTabWidget`，包含：
  - `ChannelTable` (`QTableView`)：通道列表、开关、量程等
  - `AlarmTable`：报警状态
  - `EventList`：事件标记
  - `MonitorPanel`：可拆分独立窗口
- 支持折叠/隐藏。

### ControlToolBar
- `QToolBar` 集成：
  - 打开/保存工程按钮
  - `连接设置` 按钮 (弹 `SettingDialog`)
  - `测量开始`、`停止`、`暂停`
  - Excel 推送、LUW 保存、截图、事件标记等开关
- 提供信号：`start_acquisition`, `stop_acquisition`, `open_settings` 等。

### StatusBarWidget
- 继承 `QStatusBar`
- 显示：连接状态 (图标+文本)、采样 FPS、缓存占用、报警计数、Excel 推送状态、当前时间。

### DataTableDock
- 使用 `QDockWidget` + `QTabWidget`
- `DataLogTable` (`QTableView`)：时间/通道值
- `OperationLog` (`QPlainTextEdit`)：操作日志
- Excel 推送状态页。

## 设置对话框 (`SettingDialog`)
- 采用 `QDialog` + `QStackedWidget`
- 顶部按钮栏：`Connection` `Units` `Channels` `Measurement` `Analysis` `Summary`
- 底部：`取消` `应用` `下一步`
- 各页面调用核心模块接口（暂留 stub）：
  - `ConnectionPage`
    - 表单：接口类型、IP、端口、超时
    - 动作：Ping 按钮 -> 调用 `device_manager.test_connection`
  - `UnitPage`
    - 表格展示检测到的单元/插槽，支持刷新
  - `ChannelPage`
    - 表格 + 批量操作侧栏；暂用模拟通道数据
  - `MeasurePage`
    - 采样间隔、记录时间、触发模式、保存策略
  - `SummaryPage`
    - 显示变更摘要，提供保存模板

## 信号 & 状态流 (占位)

在 `core/state.py` 中定义 `QObject` 子类用于跨组件通信：

```python
class AppState(QObject):
    connectionChanged = Signal(bool, str)
    acquisitionStarted = Signal()
    acquisitionStopped = Signal()
    waveformDataUpdated = Signal(object)  # placeholder for numpy array
    alarmRaised = Signal(object)
    logMessage = Signal(str, str)
```

UI 组件订阅这些信号，实现 UI 与后台模块解耦。

## 下一步实现顺序
1. 初始化 `app/main.py`、`MainWindow` 骨架、菜单/工具栏/状态栏空控件。
2. 添加 `WaveformPanel` 占位（随机数据刷新），验证性能。
3. 构建 `SettingDialog` 框架，填充表单控件。
4. 接入 `AppState` 信号，用假数据模拟采集流程。
5. 待硬件恢复后绑定真实 DeviceManager。



