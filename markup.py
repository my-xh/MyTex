# -*- coding: utf-8 -*-

"""
@File    : markup.py
@Time    : 2021/5/13 23:58
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 主程序
"""

import sys

from unit import blocks
from handlers import HTMLRenderer
from rules import Rules, UListRule, ListItemRule, TitleRule, HeadingRule, ParagraphRule
from filters import FilterChain, EmphasisFilter, UrlFilter, MailFilter


class Parser:
    """
    解析器基类

    属性:
        handler: 处理程序

        rules: 规则集

        filter_chain: 过滤链
    """

    def __init__(self, handler, rules, filter_chain):
        self.handler = handler
        self.rules = rules
        self.filter_chain = filter_chain

    def add_rule(self, rule):
        self.rules.add_rule(rule)

    def remove_rule(self, rule):
        self.rules.remove_rule(rule)

    def add_filter(self, _filter):
        self.filter_chain.add_filter(_filter)

    def remove_filter(self, _filter):
        self.filter_chain.remove_filter(_filter)

    def parse(self, file):
        """解析文本内容"""
        with self.rules.set_handler(self.handler):
            for block in blocks(file):
                block = self.filter_chain.do_filter(block, self.handler)  # 对文本块进行过滤
                self.rules.action(block)  # 按规则对文本块进行处理


class BasicTextParser(Parser):
    """简单文本解析器"""

    def __init__(self, handler):
        super().__init__(handler, Rules(), FilterChain())
        self.setup()

    def setup(self):
        """规则和过滤器配置"""
        self.add_rule(UListRule())
        self.add_rule(ListItemRule())
        self.add_rule(TitleRule())
        self.add_rule(HeadingRule())
        self.add_rule(ParagraphRule())
        self.add_filter(EmphasisFilter())
        self.add_filter(UrlFilter())
        self.add_filter(MailFilter())


if __name__ == '__main__':
    handler = HTMLRenderer()
    parser = BasicTextParser(handler)
    parser.parse(sys.stdin)

    # 测试示例
    # python markup.py < text/test_input.txt > text/test_output.html
