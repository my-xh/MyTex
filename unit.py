# -*- coding: utf-8 -*-

"""
@File    : unit.py.py
@Time    : 2021/5/13 23:00
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 文本块生成器
"""


def lines(file):
    """
    逐行获取文件内容，最后以换行符结束

    :param file: 文件
    :return: 一行内容
    """
    yield from file
    yield '\n'


def blocks(file):
    """
    获取所有文本块，一个文本块由空行之前的所有行组成

    :param file: 文件
    :return: 文本块
    """
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:  # 当遇到空行且空行前有内容时
            yield ''.join(block).strip()
            block = []


if __name__ == '__main__':
    with open('text/test_input.txt') as f:
        for block in blocks(f):
            print(block)
