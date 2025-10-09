import os
import re
from pathlib import Path

# 定义英文到中文的翻译映射
translations = {
    # 常见术语翻译
    "Setup Procedure": "设置步骤",
    "What's command?": "什么是命令？",
    "Status Byte and Event Registers": "状态字节和事件寄存器",
    "Input and output buffers": "输入和输出缓冲区",
    "Communication commands": "通信命令",
    "Command table": "命令表",
    "Description": "描述",
    "Standard": "标准",
    "Execution control": "执行控制",
    "Configuration": "配置",
    "Channel": "通道",
    "Scaling": "缩放",
    "Comments": "注释",
    "Triggering": "触发",
    "Alarm": "报警",
    "Environment": "环境",
    "Memory": "存储器",
    "Screen": "屏幕",
    "Cursor": "光标",
    "Calculations": "计算",
    "Troubleshooting": "故障排除",
    "Introduction": "介绍",
    "Outline": "概述",
    "Command Summary": "命令摘要",
    "Command Details": "命令详情",
    "Example programs": "示例程序",
    
    # 技术术语
    "Command": "命令",
    "Query": "查询",
    "Response": "响应",
    "Message": "消息",
    "Buffer": "缓冲区",
    "Queue": "队列",
    "Register": "寄存器",
    "Bit": "位",
    "Byte": "字节",
    "Protocol": "协议",
    "Interface": "接口",
    "Setting": "设置",
    "Configuration": "配置",
    "Parameter": "参数",
    "Value": "值",
    "Data": "数据",
    "Error": "错误",
    "Warning": "警告",
    "Status": "状态",
    "Event": "事件",
    "Enable": "启用",
    "Disable": "禁用",
    "ON": "开",
    "OFF": "关",
    
    # 文件和目录名保持原样
    "Right01.htm": "Right01.htm",
    "Right02.htm": "Right02.htm",
    "Right03.htm": "Right03.htm",
    "Right04.htm": "Right04.htm",
    "Right05.htm": "Right05.htm",
    "Right06.htm": "Right06.htm",
    "Right07.htm": "Right07.htm",
    "Right08.htm": "Right08.htm",
    "Right09.htm": "Right09.htm",
    "Right10.htm": "Right10.htm",
    "Right11.htm": "Right11.htm",
    "Right12.htm": "Right12.htm",
    "Right13.htm": "Right13.htm",
    "Right14.htm": "Right14.htm",
    "Right15.htm": "Right15.htm",
    "Left01.htm": "Left01.htm",
    "Top01.htm": "Top01.htm",
    "Frame01.htm": "Frame01.htm",
    "MainFrame01.htm": "MainFrame01.htm",
    
    # 代码和命令保持原样
    "*STB?": "*STB?",
    "*ESR?": "*ESR?",
    "*ESE": "*ESE",
    "*ESE?": "*ESE?",
    "*CLS": "*CLS",
    "*OPC": "*OPC",
    ":HEADer": ":HEADer",
    ":HEADer?": ":HEADer?",
    "ABORT": "ABORT",
    "CONFigure": "CONFigure",
    "UNIT": "UNIT",
    "SCALing": "SCALing",
    "COMMent": "COMMent",
    "TRIGger": "TRIGger",
    "ALARm": "ALARm",
    "SYSTem": "SYSTem",
    "MEMory": "MEMory",
    "DISPlay": "DISPlay",
    "CURSor": "CURSor",
    "CALCulate": "CALCulate",
    
    # 单位和数值保持原样
    "USB2.0": "USB2.0",
    "IEEE802.3": "IEEE802.3",
    "1000BASE-T": "1000BASE-T",
    "100BASE-TX": "100BASE-TX",
    "TCP/IP": "TCP/IP",
    "1Gbps": "1Gbps",
    "30m": "30m",
    "IEEE802.11b/g/n": "IEEE802.11b/g/n",
    "WPA-PSK/WPA2-PSK": "WPA-PSK/WPA2-PSK",
    "TKIP/AES": "TKIP/AES",
    "192.168.0.1": "192.168.0.1",
    "192.168.255.254": "192.168.255.254",
    "192.168.1.1": "192.168.1.1",
    "192.168.1.2": "192.168.1.2",
    "255.255.255.0": "255.255.255.0",
    "8802": "8802",
    
    # 保留HTML标签和属性
    "<html>": "<html>",
    "</html>": "</html>",
    "<head>": "<head>",
    "</head>": "</head>",
    "<body>": "<body>",
    "</body>": "</body>",
    "<title>": "<title>",
    "</title>": "</title>",
    "<p>": "<p>",
    "</p>": "</p>",
    "<span>": "<span>",
    "</span>": "</span>",
    "<table>": "<table>",
    "</table>": "</table>",
    "<tr>": "<tr>",
    "</tr>": "</tr>",
    "<td>": "<td>",
    "</td>": "</td>",
    "<br>": "<br>",
    "<b>": "<b>",
    "</b>": "</b>",
    "<a>": "<a>",
    "</a>": "</a>",
    "<div>": "<div>",
    "</div>": "</div>",
    "<ul>": "<ul>",
    "</ul>": "</ul>",
    "<li>": "<li>",
    "</li>": "</li>",
    "<ol>": "<ol>",
    "</ol>": "</ol>",
    "<img": "<img",
    "<link": "<link",
    "<meta": "<meta",
    "<style>": "<style>",
    "</style>": "</style>",
    "<!--": "<!--",
    "-->": "-->",
}

def translate_text(text):
    """翻译文本，保留代码和数值不变"""
    # 对于整行的代码或数值，直接返回
    if re.match(r'^\s*[A-Z_*?:]*\s*$', text) or re.match(r'^\s*[0-9.,+\-Ee]+\s*$', text):
        return text
    
    # 应用翻译映射
    translated = text
    for eng, chn in translations.items():
        translated = translated.replace(eng, chn)
    
    return translated

def process_html_file(file_path):
    """处理单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分割内容为行
        lines = content.split('\n')
        translated_lines = []
        
        for line in lines:
            # 跳过纯代码行和数值行
            if re.match(r'^\s*<[!?]*[a-zA-Z]*.*>$', line.strip()) or \
               re.match(r'^\s*[A-Z_*?:0-9.,+\-Ee\s]*$', line) or \
               '<meta' in line or '<link' in line or 'DOCTYPE' in line:
                translated_lines.append(line)
            else:
                # 翻译包含文本的行
                translated_line = translate_text(line)
                translated_lines.append(translated_line)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(translated_lines))
        
        print(f"已处理文件: {file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return False

def process_directory(directory_path):
    """递归处理目录中的所有HTML文件"""
    html_files = Path(directory_path).rglob("*.htm")
    success_count = 0
    error_count = 0
    
    for html_file in html_files:
        if process_html_file(str(html_file)):
            success_count += 1
        else:
            error_count += 1
    
    print(f"处理完成: {success_count} 个文件成功, {error_count} 个文件失败")

if __name__ == "__main__":
    # 处理chinese目录下的所有HTML文件
    process_directory("../chinese")