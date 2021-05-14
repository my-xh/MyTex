# -*- coding: utf-8 -*-

"""
@File    : handlers.py.py
@Time    : 2021/5/13 23:41
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 处理程序
"""


class Handler:
    """基本处理程序"""

    def callback(self, prefix: str, name: str, *args):
        """查找并执行对应文本块处理方法

        :param prefix: 前缀，start文本块开头, end文本块结尾, sub文本块替换
        :param name: 文本块名称
        :param args: 可能的额外参数
        :return: 处理结果，如果有的话，否则返回None
        """
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        """
        添加文本块开头标记

        :param name: 文本块名称
        """
        self.callback('start_', name)

    def end(self, name):
        """
        添加文本块结尾标记

        :param name: 文本块名称
        """
        self.callback('end_', name)

    def sub(self, name):
        """
        文本块替换方法

        :param name: 文本块名称
        :return: 具体的替换方法
        """

        def substitution(match):
            """
            :param match: 正则匹配的结果
            :return: 替换后的结果，如果有替换的话，否则原样返回
            """
            result = self.callback('sub_', name, match)
            if result is None:
                result = match.group(0)
            return result

        return substitution

    @staticmethod
    def feed(block):
        """
        对文本块不做任何处理

        :param block: 文本块
        :return: 实际文本
        """
        print(block)


class HTMLRenderer(Handler):
    """用于渲染HTML页面的处理程序"""

    @staticmethod
    def start_document():
        """文档开头标记"""
        print('<html>\n<head>\n\t<title>Document</title>\n</head>\n<body>')

    @staticmethod
    def end_document():
        """文档结尾标记"""
        print('</body>\n</html>')

    @staticmethod
    def start_title():
        """题目开头标记"""
        print('<h1>')

    @staticmethod
    def end_title():
        """题目结尾标记"""
        print('</h1>')

    @staticmethod
    def start_heading():
        """标题开头标记"""
        print('<h2>')

    @staticmethod
    def end_heading():
        """标题结尾标记"""
        print('</h2>')

    @staticmethod
    def start_paragraph():
        """段落开头标记"""
        print('<p>')

    @staticmethod
    def end_paragraph():
        """段落结尾标记"""
        print('</p>')

    @staticmethod
    def start_ulist():
        """无序列表开头标记"""
        print('<ul>')

    @staticmethod
    def end_ulist():
        """无序列表结尾标记"""
        print('</ul>')

    @staticmethod
    def start_listitem():
        """列表项开头标记"""
        print('<li>')

    @staticmethod
    def end_listitem():
        """列表项结尾标记"""
        print('</li>')

    @staticmethod
    def sub_emphasis(match):
        """
        替换重点标记

        :param match: 正则匹配内容
        :return: 重点标记
        """
        return f'<em>{match.group(1)}</em>'

    @staticmethod
    def sub_url(match):
        """
        替换超链接标记

        :param match: 正则匹配内容
        :return: 超链接标记
        """
        return f'<a href="{match.group(1)}">{match.group(1)}</a>'

    @staticmethod
    def sub_mail(match):
        """
        替换邮箱标记

        :param match: 正则匹配内容
        :return: 邮箱标记
        """
        return f'<a href="mailto:{match.group(1)}">{match.group(1)}</a>'
