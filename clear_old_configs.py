#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理旧的设备配置文件（8800端口）"""

import os
import json
from pathlib import Path


def main():
    # 配置文件路径
    config_dir = Path.home() / ".xunyu_xy2580"
    device_configs_file = config_dir / "device_configs.json"
    
    print('=' * 70)
    print('清理旧设备配置')
    print('=' * 70)
    
    if not device_configs_file.exists():
        print('\n✓ 没有找到旧配置文件')
        return
    
    print(f'\n找到配置文件: {device_configs_file}')
    
    try:
        # 读取现有配置
        with open(device_configs_file, 'r', encoding='utf-8') as f:
            old_configs = json.load(f)
        
        print(f'\n旧配置包含 {len(old_configs)} 个设备:')
        for device_id in old_configs.keys():
            print(f'  - {device_id}')
        
        # 更新端口：8800 -> 8802
        new_configs = {}
        for device_id, config in old_configs.items():
            # 替换端口号
            new_device_id = device_id.replace(':8800', ':8802')
            new_configs[new_device_id] = config
            print(f'\n更新: {device_id} -> {new_device_id}')
        
        # 保存新配置
        with open(device_configs_file, 'w', encoding='utf-8') as f:
            json.dump(new_configs, f, indent=2, ensure_ascii=False)
        
        print(f'\n✓ 配置已更新，所有设备端口改为8802')
        print(f'\n新配置包含 {len(new_configs)} 个设备:')
        for device_id in new_configs.keys():
            print(f'  - {device_id}')
        
    except Exception as e:
        print(f'\n✗ 更新配置失败: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
    print('\n' + '=' * 70)
    print('现在可以重新运行主程序: python -m app.main')
    print('=' * 70)




