#!/usr/bin/env python3
"""
功能：手动生成所有SKU的静态detail html
使用方法：
    ./regenerate_index_html.py
"""

# 添加搜索包路径
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '..meiduo_mall/apps')

# 设置Django运行所依赖的环境变量
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 让Django进行一次初始化
import django
django.setup()

from contents.crons import generate_static_index_html

if __name__ == '__main__':
    generate_static_index_html()