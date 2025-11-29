#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查配置文件内容"""

import json
import os

config_file = os.path.expanduser('~/.battery_analyzer/app_config.json')

if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    print(json.dumps(config, indent=2, ensure_ascii=False))
else:
    print('配置文件不存在')

