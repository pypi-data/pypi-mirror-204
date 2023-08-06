"""
    author: Li Junxian
    function:is used to process function
"""
import importlib
import os
import sys
from copy import deepcopy
from threading import Lock
from types import ModuleType
from typing import Union


def demo():
    pass


class Module(object):
    """
    功能读取、调用、帮助信息输出
    """
    # 创建锁
    __LOCK = Lock()

    def __init__(self, module: Union[str, ModuleType]):
        """
        模块的文件:模块文件全路径
        """
        if isinstance(module, str):
            module_file = module
            suffix = self.__get_suffix(module_file)
            if suffix not in [".py"]:
                raise Exception("{} 不是一个py文件！".format(module_file))
            if not os.path.exists(module_file):
                raise Exception("{} 不存在".format(module_file))
            dirname = os.path.dirname(module_file)
            pure_file_name = self.__get_pure_file_name(module_file)
            self.__module = self.__get_module_object(dirname, pure_file_name)
        elif isinstance(module, ModuleType):
            self.__module = module
        else:
            raise Exception("module参数类型错误")
        self.__func = list()
        self.__class = list()
        self.__var = list()
        self.__m = list()
        self.__process_module_object()

    @staticmethod
    def __get_suffix(file):
        """
        取得文件小写后缀
        """
        return os.path.splitext(file)[-1].lower()

    @staticmethod
    def __get_pure_file_name(file):
        """
        取得文件的名称，并去掉后缀
        :param file:
        :return:
        """
        return os.path.splitext(os.path.basename(file))[0]

    @staticmethod
    def __get_module_object(dirname, pure_file_name):
        """
        取得模块对象
        :return:
        """
        # 加锁
        Module.__LOCK.acquire()
        # 记录原始sys_path
        sys_path = deepcopy(sys.path)
        # 先判断是否存在
        if dirname not in sys.path:
            sys.path.insert(1, dirname)
        module = importlib.import_module(pure_file_name)
        # 恢复sys_path
        sys.path = sys_path
        # 解锁
        Module.__LOCK.release()
        return module

    def __process_module_object(self):
        """
        取得func信息
        """
        for name in dir(self.__module):
            if name in ["builtins"]:
                continue
            if name.startswith("__"):
                continue
            o = getattr(self.__module, name)
            if type(o) is type:
                self.__class.append(name)
            elif type(o) is type(demo):
                self.__func.append(name)
            elif type(o) is type(os):
                self.__m.append(name)
            else:
                self.__var.append(name)

    def has_var(self, name):
        """
        判断是否有此变量
        :param name:
        :return:
        """
        if name in self.__var:
            return True
        return False

    def has_func(self, name):
        """
        判断是否有此函数
        :param name:
        :return:
        """
        if name in self.__func:
            return True
        return False

    def has_class(self, name):
        """
        判断是否由此类
        :param name:
        :return:
        """
        if name in self.__class:
            return True
        return False

    def has_module(self, name):
        """
        判断是否由此模块
        :param name:
        :return:
        """
        if name in self.__m:
            return True
        return False

    def var(self, name):
        """
        取得要调用的类
        :param name:
        :return:
        """
        if not self.has_var(name):
            raise Exception("此 {} 变量不存在!".format(name))
        return getattr(self.__module, name)

    def clazz(self, name):
        """
        取得要调用的类
        :param name:
        :return:
        """
        if not self.has_class(name):
            raise Exception("此 {} 类不存在!".format(name))
        return getattr(self.__module, name)

    def func(self, name):
        """
        取得要调用的方法
        """
        if not self.has_func(name):
            raise Exception(" {} 函数不存在!".format(name))
        return getattr(self.__module, name)

    def module(self, name):
        """
        取得要调用的模块
        :param name:
        :return:
        """
        if not self.has_module(name):
            raise Exception("此 {} 模块不存在!".format(name))
        return getattr(self.__module, name)

    @property
    def py_module(self):
        """
        取得模块对象
        :return:
        """
        return self.__module

class OutModule(object):
    def __init__(self, name, module: Module):
        self.__name = name
        self.__module = module

    @property
    def name(self):
        return self.__name

    @property
    def module(self):
        return self.__module

    @property
    def py_module(self):
        return self.__module.py_module

