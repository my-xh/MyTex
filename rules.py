# -*- coding: utf-8 -*-

"""
@File    : rules.py
@Time    : 2021/5/13 23:58
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 规则
"""

from abc import ABCMeta, abstractmethod

from handlers import Handler


class Rule(metaclass=ABCMeta):
    """规则基类"""

    def __init__(self, _type):
        self._type = _type  # 规则类型

    @abstractmethod
    def _condition(self, block):
        """
        判定文本块是否符合规则

        :param block: 文本块
        :return: True，如果符合规则，否则False
        """
        pass

    def action(self, block, handler: Handler):
        """
        使用指定处理程序对文本块进行处理

        :param block: 文本块
        :param handler: 处理程序
        :return: True，如果不需要继续处理，否则False
        """
        handler.start(self._type)
        handler.feed(block)
        handler.end(self._type)
        return True


class HeadingRule(Rule):
    """判定标题的规则"""

    def __init__(self, _type='heading'):
        super().__init__(_type)

    def _condition(self, block):
        # 标题只包含一行文本块，不超过70个字符且不以冒号结尾
        return True if '\n' not in block and len(block) <= 70 and not block.endswith(':') else False


class TitleRule(HeadingRule):
    """判定题目的规则"""

    def __init__(self, _type='title'):
        super().__init__(_type)
        self.is_first = True  # 标记是否是第一个文本块

    def _condition(self, block):
        # 题目是第一个文本块，且是一个标题

        if not self.is_first:
            return False
        self.is_first = False
        return super()._condition(block)


class ListItemRule(Rule):
    """判定列表项的规则"""

    def __init__(self, _type='listitem'):
        super().__init__(_type)

    def _condition(self, block):
        # 列表项是以连字符（-）开头的文本块
        return True if block.startswith('-') else False

    def action(self, block, handler: Handler):
        block = block[1:].strip()  # 去除连字符
        return super().action(block, handler)


class UListRule(ListItemRule):
    """判定无序列表的规则"""

    def __init__(self, _type='ulist'):
        super().__init__(_type)
        self.inside = False  # 标记是否在列表内

    def _condition(self, block):
        # 列表判定需要跨文本块，将判断逻辑移交给self.action()
        return True

    def action(self, block, handler: Handler):
        # 列表从非列表项紧跟的第一个列表项开始，到紧跟着非列表项的最后一个列表项结束
        if super()._condition(block):
            if not self.inside:
                self.inside = True
                handler.start(self._type)
        else:
            if self.inside:
                self.inside = False
                handler.end(self._type)
        return False  # 可继续进行其他规则的判定


class ParagraphRule(Rule):
    """判定段落的规则"""

    def __init__(self, _type='paragraph'):
        super().__init__(_type)

    def _condition(self, block):
        # 不满足其他规则的文本块都是段落
        return True


class Rules(Rule):
    """规则集"""

    def __init__(self, handler=None):
        super().__init__('document')
        self.handler = handler
        self._rules = []  # 规则列表

    def add_rule(self, rule: Rule):
        """
        添加规则

        :param rule: 要添加的规则对象
        """
        self._rules.append(rule)

    def remove_rule(self, rule: Rule):
        """
        移除规则

        :param rule: 待移除的规则对象
        """
        self._rules.remove(rule)

    def set_handler(self, handler):
        """
        设置处理程序

        :param handler: 要使用的处理程序
        :return: self
        """
        self.handler = handler
        return self

    def __enter__(self):
        if not isinstance(self.handler, Handler):
            raise AttributeError('请先用set_handler()方法设置一个处理程序！')
        self.handler.start(self._type)
        return self

    def __exit__(self, *args):
        self.handler.end(self._type)

    def _condition(self, block):
        # 具体判定移交self.action()
        return True

    def action(self, block, *args):
        # 逐一检测每一个规则，并分别执行相应的动作
        for rule in self._rules:
            if rule._condition(block):
                last = rule.action(block, self.handler)
                if last:  # 不再检测后面的规则
                    break
        return True
