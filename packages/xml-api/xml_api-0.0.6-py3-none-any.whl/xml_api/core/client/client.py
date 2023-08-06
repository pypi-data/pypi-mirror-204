# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: client
"""
import abc
import logging

from .res_data import ResData
from ..process.post import PostProcessor
from ..process.pre import PreProcessor
from ...function.cfg.config import ConfigLoader
from ...function.data.interface import Interface
from ...function.utils.utils import Utils

logger = logging.getLogger(__name__)


class AbstractClient(metaclass=abc.ABCMeta):

    def __init__(self, config: ConfigLoader, interface_info: Interface, interface_data: dict, *context: dict):
        """
        客户端
        :param interface_info: 接口信息
        :param interface_data: 接口数据
        :param context: 上下文
        """
        # config
        self._config = config
        # 场景上下文
        self._context = context
        # 测试数据
        self._interface_data = interface_data
        # 接口信息
        self._interface_info = interface_info
        # 获取调用的接口名称
        self._name = Utils.extract_attrs_from_dict(self._interface_data, "name")
        # 获取接口调用描述
        self._description = Utils.extract_attrs_from_dict(self._interface_data, "description")
        # 数据库链接字符串
        self._db_info = self._interface_data.get("db_info")
        # 前置处理器数据
        self._pre_data = self._interface_data.get("pre_processor")
        # 后置处理器数据
        self._post_data = self._interface_data.get("post_processor")
        # 结果
        self._res = ResData()

    @abc.abstractmethod
    def _request(self):
        pass

    def request(self):
        # 如果有前置处理器进行前置处理
        if self._pre_data:
            if self._db_info is not None:
                if self._pre_data.get("db_info") is None:
                    self._pre_data["db_info"] = self._db_info
            PreProcessor(self._config, self._interface_data, self._interface_info, self._pre_data).work(*self._context)
        # 发送请求
        logger.debug("调用接口 {} ,该接口是 {} 类型的接口".format(self._interface_info.name, self._interface_info.protocol))
        self._request()
        logger.debug("接口调用结束，结果已返回")
        # 如果有后置处理器进行后置处理
        # 判断是否存在expect
        if self._post_data:
            if self._db_info is not None:
                if self._post_data.get("db_info") is None:
                    self._post_data["db_info"] = self._db_info
            PostProcessor(self._config, self._interface_data, self._interface_info, self._post_data, self._res).work(
                *self._context)
