import logging
import os
import threading
from logging.handlers import QueueHandler
from queue import Queue

from ..process.processor import Processor
from ...function.analysis.xml_parser import XmlParserForString
from ...function.cfg.config import ConfigLoader
from ...function.data.inf import Inf
from ...function.data.interface import Interfaces
from ...function.database.db import DB
from ...function.express.module import Module, OutModule
from ...function.utils.utils import Utils
from ...function.cfg.cfg import xml_api_config


class ThreadLogFilter(logging.Filter):

    def __init__(self, thread_name: str):
        super().__init__(thread_name)
        self.__thread_name = thread_name

    def filter(self, record):
        return record.threadName == self.__thread_name


class ExecutorThread(threading.Thread):
    def __init__(self, xml, params, py_modules_path, configs):
        super().__init__()
        self.__xml = xml
        self.__py_modules_path = py_modules_path
        self.__params = params
        self.__result = None
        self.__e = None
        self.__configs = configs

    def run(self):
        try:
            # 创建inf
            inf = Inf()
            # 读取xml数据
            xml_data = XmlParserForString(self.__xml).parse_xml()
            # 初始化配置
            config = ConfigLoader(Utils.extract_attrs_from_dict(xml_data, "root", "configs"))
            # 设置编程配置
            for _name, _value in self.__configs.items():
                config.set_config(_name, _value)
            # 初始化模块
            py_modules = list()
            for module_path in self.__py_modules_path:
                # 取得模块的名字
                module_name = Utils.get_pure_file_name(module_path)
                py_modules.append(OutModule(module_name, Module(module_path)))
            config.py_modules = py_modules
            # 初始化接口
            interfaces = Interfaces(Utils.extract_attrs_from_dict(xml_data, "root", "interfaces"), config)
            inf.interfaces = interfaces
            # 初始化脚本
            script_data = Utils.extract_attrs_from_dict(xml_data, "root", "script")
            inf.script_data = script_data
            # 开始脚本调用
            processor = Processor(config, inf, self.__params)
            processor.start()
            # 获取结果
            self.__result = processor.context
        except Exception as e:
            self.__e = e

    @property
    def result(self):
        return self.__result

    @property
    def e(self):
        return self.__e


class XMLAPIExecutor(object):
    INIT = 0
    RUN_ING = 1
    NORMAL_END = 2
    ERROR_END = 3

    def __init__(self, xml: str):
        """
        使用xml文件或xml字符串初始化执行器
        :param xml:
        """
        # 记录执行器状态
        self.__status = XMLAPIExecutor.INIT
        # 判断xml是否为文件路径
        if os.path.isfile(xml):
            self.__xml = open(xml, encoding="utf-8").read()
        else:
            self.__xml = xml
        # 构造一个参数池
        self.__params = dict()
        # 创建logger
        self.__logger = logging.getLogger("xml_api")
        self.__logger.setLevel(logging.DEBUG)
        # 记录编程配置
        self.__configs = dict()
        # 记录自定义模块启用状态
        self.__py_modules_enable = False
        # 记录自定义模块路径
        self.__py_modules_path = list()
        # 存储执行器结果
        self.__result = dict()
        # 存储执行器异常
        self.__e = None
        # 执行线程
        self.__thread = None
        # 控制台日志handler
        self.__console_handler = None
        # 日志队列
        self.__queue = None
        self.__queue_handler = None
        self.__queue_log = None
        # 日志handlers
        self.__log_handlers = list()

    def __update_executor_status(self):
        '''
        更新执行器状态
        :return:
        '''
        if self.__thread is not None:
            if self.__thread.is_alive():
                self.__status = XMLAPIExecutor.RUN_ING
            else:
                # 去掉logger的handler
                for handler in self.__log_handlers:
                    self.__logger.removeHandler(handler)
                # 判断是否有异常
                if self.__thread.e is None:
                    self.__status = XMLAPIExecutor.NORMAL_END
                    self.__result = self.__thread.result
                else:
                    self.__status = XMLAPIExecutor.ERROR_END
                    self.__e = self.__thread.e
                self.__thread = None

    def set_param(self, name, value):
        '''
        设置入参
        :param name: 参数名
        :param value: 参数值
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再设置参数")
        self.__params[name] = value

    def set_params(self, params: dict):
        '''
        批量设置入参
        :param params:
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再设置参数")
        # 将入参添加到参数池中
        for key in params:
            self.__params[key] = params[key]

    def set_config(self, name, value):
        '''
        设置配置
        :param name:
        :param value:
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再设置配置")
        # 先判断是否为合法配置
        if name not in xml_api_config:
            raise Exception("不合法的配置 {}，可用的配置有：\n{}".format(name, "\n".join(xml_api_config.keys())))
        if name == "db_oracle_instant_client_dir":
            if DB.if_oracle_library_is_initialized:
                raise Exception("oracle library已经初始化，无法配置db_oracle_instant_client_dir")
        self.__configs[name] = value

    def import_module(self, module_path: str):
        '''
        增加自定义模块，请使用全路径
        :param module_path:
        :return:
        '''
        self.__update_executor_status()
        if not self.__py_modules_enable:
            raise Exception("请先启用自定义模块功能")
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再添加模块")
        # 如果模块路径不存在，则抛错
        if not os.path.isfile(module_path):
            raise FileNotFoundError("模块路径不存在")
        # 判断是否已经添加过该模块
        for path in self.__py_modules_path:
            if Utils.get_pure_file_name(module_path) == Utils.get_pure_file_name(path):
                raise Exception("已存在同名模块")
        self.__py_modules_path.append(module_path)

    def enable_console_log(self, level=logging.INFO, _format=None):
        '''
        启用控制台日志
        :param level:
        :param _format:
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再设置控制台日志")
        if self.__console_handler is None:
            self.__console_handler = logging.StreamHandler()
            self.__logger.addHandler(self.__console_handler)
            self.__log_handlers.append(self.__console_handler)
        self.__console_handler.setLevel(level)
        if _format is not None:
            self.__console_handler.setFormatter(logging.Formatter(_format))

    def enable_queue_log(self, level=logging.INFO, _format=None):
        '''
        启用队列日志
        :param level:
        :param _format:
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再设置队列日志")
        if self.__queue_handler is None:
            self.__queue = Queue()
            self.__queue_handler = QueueHandler(self.__queue)
            self.__logger.addHandler(self.__queue_handler)
            self.__log_handlers.append(self.__queue_handler)
        self.__queue_handler.setLevel(level)
        if _format is not None:
            self.__queue_handler.setFormatter(logging.Formatter(_format))

    def enable_py_module(self):
        '''
        启用python模块
        :return:
        '''
        self.__py_modules_enable = True

    def add_handler(self, handler: logging.Handler):
        '''
        添加日志handler
        :param handler:
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor已经运行，无法再添加日志handler")
        self.__logger.addHandler(handler)
        self.__log_handlers.append(handler)

    def run(self):
        '''
        执行
        :return:
        '''
        self.__update_executor_status()
        if self.__status != XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor只能运行一次")
        self.__status = XMLAPIExecutor.RUN_ING
        # 开始脚本调用
        self.__thread = ExecutorThread(self.__xml, self.__params, self.__py_modules_path, self.__configs)
        # 过滤不同线程的日志
        _filter = ThreadLogFilter(self.__thread.name)
        for handler in self.__log_handlers:
            handler.addFilter(_filter)
        self.__thread.start()

    def wait(self):
        '''
        等待执行结束
        :return:
        '''
        if self.__status != XMLAPIExecutor.RUN_ING:
            raise Exception("XMLAPIExecutor未运行")
        self.__thread.join()
        self.__update_executor_status()

    def get_result(self):
        '''
        获取结果集
        :return:
        '''
        self.__update_executor_status()
        if self.__status == XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor还未运行")
        if self.__status == XMLAPIExecutor.RUN_ING:
            raise Exception("XMLAPIExecutor还未运行结束")
        if self.__status == XMLAPIExecutor.ERROR_END:
            raise Exception("XMLAPIExecutor运行出错，无法获取结果，请使用get_e()获取异常")
        return self.__result

    def get_result_by_name(self, name):
        '''
        获取结果集中的某个值
        :param name:
        :return:
        '''
        self.__update_executor_status()
        if self.__status == XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor还未运行")
        if self.__status == XMLAPIExecutor.RUN_ING:
            raise Exception("XMLAPIExecutor还未运行结束")
        if self.__status == XMLAPIExecutor.ERROR_END:
            raise Exception("XMLAPIExecutor运行出错，无法获取结果，请使用get_e()获取异常")
        return self.__result.get(name)

    def get_error(self) -> Exception:
        '''
        获取异常
        :return:
        '''
        self.__update_executor_status()
        if self.__status == XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor还未运行")
        if self.__status == XMLAPIExecutor.RUN_ING:
            raise Exception("XMLAPIExecutor还未运行结束")
        if self.__status == XMLAPIExecutor.NORMAL_END:
            raise Exception("XMLAPIExecutor正常运行结束")
        return self.__e

    def next_log(self) -> logging.LogRecord:
        '''
        获取下一条日志
        :return:
        '''
        if self.__status == XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor未运行，无法获取日志")
        if self.__queue is None:
            raise Exception("XMLAPIExecutor未设置日志队列，无法获取日志")
        log = self.__queue_log
        self.__queue_log = None
        return log

    def have_log(self):
        '''
        是否有日志
        :return:
        '''
        if self.__queue_log is not None:
            return True
        # 判断是否有日志
        self.__update_executor_status()
        if self.__status == XMLAPIExecutor.INIT:
            raise Exception("XMLAPIExecutor未运行，无法获取日志")
        if self.__queue is None:
            raise Exception("XMLAPIExecutor未设置日志队列，无法获取日志")
        while True:
            try:
                log = self.__queue.get(timeout=0.1)
                self.__queue_log = log
                return True
            except:
                self.__update_executor_status()
                if self.__status in [XMLAPIExecutor.NORMAL_END, XMLAPIExecutor.ERROR_END]:
                    if self.__queue.empty():
                        return False
                    else:
                        log = self.__queue.get()
                        self.__queue_log = log
                        return True

    def is_normal_end(self):
        '''
        是否正常结束
        :return:
        '''
        self.__update_executor_status()
        return self.__status == XMLAPIExecutor.NORMAL_END

    def is_error_end(self):
        '''
        是否异常结束
        :return:
        '''
        self.__update_executor_status()
        return self.__status == XMLAPIExecutor.ERROR_END

    def is_end(self):
        '''
        是否结束
        :return:
        '''
        self.__update_executor_status()
        return self.__status in [XMLAPIExecutor.NORMAL_END, XMLAPIExecutor.ERROR_END]

    @property
    def status(self):
        '''
        获取状态
        :return:
        '''
        self.__update_executor_status()
        return self.__status
