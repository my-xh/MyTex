# -*- coding: utf-8 -*-

"""
@File    : filters.py
@Time    : 2021/5/14 0:15
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 过滤器
"""

import re
from abc import ABCMeta, abstractmethod

from handlers import Handler


class Filter(metaclass=ABCMeta):
    """过滤器基类"""

    @abstractmethod
    def do_filter(self, data, handler: Handler):
        """
        对数据进行过滤

        :param data: 原始数据
        :param handler: 处理程序
        :return: 过滤后的数据
        """
        pass


class FilterChain(Filter):
    """过滤链"""

    def __init__(self):
        super().__init__()
        self.filters = []  # 过滤器列表

    def add_filter(self, _filter: Filter):
        """
        添加过滤器

        :param _filter: 要添加的过滤器
        """
        self.filters.append(_filter)

    def remove_filter(self, _filter: Filter):
        """
        移除过滤器

        :param _filter: 待移除的过滤器
        """
        self.filters.remove(_filter)

    def do_filter(self, data, handler):
        # 依次使用每一种过滤器对数据进行过滤
        for _filter in self.filters:
            data = _filter.do_filter(data, handler)
        return data


class ReFilter(Filter):
    """
    正则过滤器

    类属性:
        pattern: 正则匹配模式

        _type: 过滤类型
    """
    pattern = re.compile(r'.*')
    _type = ''

    def do_filter(self, data, handler: Handler):
        return self.pattern.sub(handler.sub(self._type), data)


class EmphasisFilter(ReFilter):
    """重点过滤器"""
    pattern = re.compile(r'\*(.*?)\*')
    _type = 'emphasis'


class UrlFilter(ReFilter):
    """超链接过滤器"""
    pattern = re.compile(r'(https?://[\d\w-]+(\.[\d\w-]+)+([?/=.&][\d\w-]+)+)', re.ASCII)
    _type = 'url'


class MailFilter(ReFilter):
    """邮箱过滤器"""
    pattern = re.compile(r'([\d\w]+@[\d\w]+(\.[\d\w]+)+)', re.ASCII)
    _type = 'mail'
