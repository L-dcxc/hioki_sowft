#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理配置文件"""

import os

config_file = os.path.expanduser('~/.battery_analyzer/app_config.json')

if os.path.exists(config_file):
    os.remove(config_file)
    print('✓ 配置文件已删除')
else:
    print('✓ 配置文件不存在')

