#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 PDF 导出功能"""

import os

print("=" * 50)
print("测试 reportlab 库")
print("=" * 50)

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    print("✓ reportlab 导入成功！")
except ImportError as e:
    print(f"✗ reportlab 导入失败: {e}")
    exit(1)

print("\n测试字体文件:")
font_paths = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttf", 
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
]
for p in font_paths:
    exists = os.path.exists(p)
    print(f"  {p}: {'✓ 存在' if exists else '✗ 不存在'}")

# 尝试注册字体
print("\n尝试注册字体:")
font_registered = False
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            font_registered = True
            print(f"✓ 成功注册字体: {font_path}")
            break
        except Exception as e:
            print(f"✗ 注册失败 {font_path}: {e}")

# 创建测试 PDF
print("\n创建测试 PDF...")
try:
    doc = SimpleDocTemplate(
        "test_report.pdf",
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    if font_registered:
        title_style = ParagraphStyle(
            'ChineseTitle',
            parent=styles['Title'],
            fontName='ChineseFont',
            fontSize=18,
        )
        normal_style = ParagraphStyle(
            'ChineseNormal',
            parent=styles['Normal'],
            fontName='ChineseFont',
            fontSize=10,
        )
    else:
        title_style = styles['Title']
        normal_style = styles['Normal']
    
    story.append(Paragraph("电池电压与温升测试分析报告", title_style))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("这是一个测试PDF文件，用于验证中文显示功能。", normal_style))
    story.append(Spacer(1, 10*mm))
    
    # 测试表格
    data = [
        ["测试项目", "数值", "单位"],
        ["温度", "25.5", "°C"],
        ["电压", "9.24", "V"],
    ]
    table = Table(data, colWidths=[50*mm, 50*mm, 30*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont' if font_registered else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    
    doc.build(story)
    print("✓ PDF 创建成功: test_report.pdf")
    print(f"  文件大小: {os.path.getsize('test_report.pdf')} bytes")
    
except Exception as e:
    import traceback
    print(f"✗ PDF 创建失败: {e}")
    traceback.print_exc()

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)

