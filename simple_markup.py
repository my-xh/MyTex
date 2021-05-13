# -*- coding: utf-8 -*-

"""
@File    : simple_markup.py
@Time    : 2021/5/13 23:17
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 简单的标记程序
"""

import re
import sys
from unit import blocks

print('<html><head><title>标记测试</title></head><body>')

is_title = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.*?)\*', r'<em>\1</em>', block)
    if is_title:
        is_title = False
        print(f'<h1>{block}</h1>')
    else:
        print(f'<p>{block}</p>')

print('</body></html>')

# 终端测试
# python simple_markup.py < text/test_input.txt > text/test_output_prototype.html
