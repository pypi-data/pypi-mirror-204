# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: frame config class
"""
import os
import sys

from ..express.module import Module
from ..utils.utils import Utils
from ...exception.my_exception import MyException
from .cfg import xml_api_config


class ConfigLoader(object):
    """
    项目的配置加载器，将一次性读取所有的配置
    """

    def __init__(self, configs: dict = None):
        # 取到项目根目录
        self.__base_path = ConfigLoader.get_base_path()
        # 用来存储读取的原始配置
        self.__config = xml_api_config
        # 用来存储读取的原始变量
        self.__vars = dict()
        # 当前环境
        self.__env = self.get_config("env")
        # 内部模块
        self.__inner_py_module = None
        # 载入内部模块
        self.__load_inner_py_module()
        # 自定义模块列表
        self.__py_modules = list()
        # 读取和计算xml的配置及变量
        self.__load_config(configs)

    def __load_config(self, configs):
        if configs is None:
            return
        # 读取和计算xml的配置及变量
        # 遍历传入的配置
        for key in configs.keys():
            # 遇到$开头的键，跳过
            if key.startswith("$"):
                continue
            # 遇到其它键，认为是配置或变量，进行读取
            self.__load_config_detail(key, configs[key])
        # 记录当前环境
        self.__env = self.get_config("env")

    def __load_config_detail(self, key, detail: dict):
        # 遍历传入的配置细节
        section_dict = dict()
        for k in detail.keys():
            # 遇到$开头的键，跳过
            if k.startswith("$"):
                continue
            # 遇到其它键，认为是配置或变量，进行读取
            if key == "config" and k in self.__config.keys():
                self.__config[k] = Utils.extract_attrs_from_dict(detail, k, "$value")
            else:
                section_dict[k] = Utils.extract_attrs_from_dict(detail, k, "$value")
        self.__vars[key] = section_dict

    def __load_inner_py_module(self):
        """加载内置模块"""
        from xml_api.function.func import _inner
        self.__inner_py_module = Module(_inner)

    @property
    def py_modules(self):
        return self.__py_modules

    @py_modules.setter
    def py_modules(self, py_modules):
        self.__py_modules = py_modules

    @property
    def inner_py_module(self):
        return self.__inner_py_module

    @staticmethod
    def get_base_path():
        path = sys.path[0]
        cwd = os.getcwd()
        if path.endswith("test_case"):
            return os.path.dirname(path)
        elif path.endswith("puppy.exe"):
            sys.path.insert(0, cwd)
            return os.getcwd()
        return path

    @staticmethod
    def process_config(name, cfg, _type):
        """处理配置"""
        if type(cfg) is not _type:
            if _type is bool:
                if cfg in ["True", "1", "true", "yes"]:
                    return True
                elif cfg in ["False", "0", "false", "no"]:
                    return False
                else:
                    raise MyException(" {} 配置项配置不正确，只能是True或False，不能是 {}".format(name, cfg))
            elif _type is int:
                if Utils.is_number(cfg):
                    return int(cfg)
                else:
                    raise MyException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
            elif _type is float:
                if Utils.is_float(cfg):
                    return float(cfg)
                else:
                    raise MyException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
        return cfg


    def get_config(self, name, _type=str):
        """
        得到配置项，返回_type指定类型
        :param _type:
        :param name:
        :return: 如果配置不存在则返回None
        """
        if name not in self.__config.keys():
            raise MyException("配置不存在：{}".format(name))
        return self.process_config(name, self.__config.get(name), _type)

    def have_config(self, name):
        """
        判断是否存在配置
        :param name:
        :return:
        """
        try:
            self.get_config(name)
            return True
        except:
            return False

    def set_config(self, name, value):
        """
        设置配置项，该配置项不会被写入文件。
        :param name:
        :param value:
        :return:
        """
        if name not in self.__config:
            raise MyException("该配置不存在：{}".format(name))
        self.__config[name] = value

    def get_var(self, name):
        """
        得到变量，不存在则报错
        :param name:
        :return: 如果配置不存在则返回None
        """
        if name not in self.vars.keys():
            raise MyException("变量不存在：{}".format(name))
        return self.vars.get(name)

    def have_var(self, name):
        """
        判断是否存在该变量
        :param name:
        :return:
        """
        try:
            self.get_var(name)
            return True
        except:
            return False

    def set_env(self, env):
        """
        设置环境
        :param env:
        :return:
        """
        if env not in self.__vars.keys():
            raise MyException("{} 环境不存在".format(env))
        self.__env = env

    def get_env(self):
        return self.__env

    @property
    def configs(self):
        return self.__config

    @property
    def vars(self):
        '''
        返回当前环境变量指定的变量组
        '''
        return self.__vars.get(self.get_env())
