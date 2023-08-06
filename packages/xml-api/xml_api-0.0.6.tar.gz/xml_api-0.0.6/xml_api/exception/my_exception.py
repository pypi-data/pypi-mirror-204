# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:  Base Exception
"""


class MyException(Exception):
    def __init__(self, e):
        if type(e) is not str:
            self.__name = e.__class__.__name__
            self.__msg = e.__str__()
        else:
            self.__msg = e

    @property
    def msg(self):
        return self.__msg

    def __gen_error(self):
        if hasattr(self, "_MyException__name"):
            return '\n{}:\n  {}'.format(self.__name,
                                        self.__msg)
        else:
            return '\nMyException:\n  {}'.format(self.__msg)

    def __str__(self):
        return self.__gen_error()
