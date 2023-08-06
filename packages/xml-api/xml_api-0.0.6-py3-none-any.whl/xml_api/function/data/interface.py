# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:read all interfaces information
"""
import re
from typing import Union

from xml_api.exception.my_exception import MyException
from xml_api.function.cfg.config import ConfigLoader
from xml_api.function.express.express import Express
from xml_api.function.utils.utils import Utils


class Interface(object):
    __express_re = re.compile(r"\${(.*?)}")

    def __init__(self, config: ConfigLoader, interface_info):
        """
        :return:
        """
        self.__config = config
        # 接口名称
        self.__name = self.__get_correct_name(interface_info.get("name"))
        # 接口协议
        self.__protocol = self.__get_correct_protocol(interface_info.get("protocol"))
        # 请求类型
        self.__method = self.__get_correct_method(interface_info.get("method"), self.__protocol)
        # 请求路径
        self.__path = self.__get_correct_path(Utils.extract_attrs_from_dict(interface_info, "path", "$value"))
        # 请求头
        self.__header = self.__get_correct_header(Utils.extract_attrs_from_dict(interface_info, "header", "$value"))
        # 得到正确的请求
        self.__param = self.__get_correct_param(Utils.extract_attrs_from_dict(interface_info, "param", "$value"))
        # 得到正确的请求体和请求体格式
        self.__body, self.__body_type = self.__get_correct_body_and_body_type(
            Utils.extract_attrs_from_dict(interface_info, "body", "$value"),
            Utils.extract_attrs_from_dict(interface_info, "body", "type"))
        # 请求端口
        self.__port = self.__get_correct_port(Utils.extract_attrs_from_dict(interface_info, "port", "$value"))
        # 请求服务器
        self.__server = self.__get_correct_server(Utils.extract_attrs_from_dict(interface_info, "server", "$value"))
        # http类型传递文件
        # {name:(path,imei)}
        self.__files = self.__get_correct_files(Utils.extract_attrs_from_dict(interface_info, "files", "file"))
        # cookies
        self.__cookies = self.__get_correct_cookies(Utils.extract_attrs_from_dict(interface_info, "cookies", "$value"))
        # auth
        self.__auth = self.__get_correct_auth(Utils.extract_attrs_from_dict(interface_info, "auth", "$value"))
        # auth type
        self.__auth_type = self.__get_correct_auth_type(Utils.extract_attrs_from_dict(interface_info, "auth", "type"))

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):
        self.__protocol = protocol

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header: Union[str, None]):
        """
        设置header
        :param header:
        :return:
        """
        if type(header) != str and header is not None:
            raise MyException("必须是字符串!而不是{}".format(type(header)))
        self.__header = header

    @property
    def param(self):
        """
        返回param
        :return:
        """
        return self.__param

    @param.setter
    def param(self, param):
        self.__param = param

    @property
    def body(self):
        """
        返回body
        :return:
        """
        return self.__body

    @body.setter
    def body(self, body: Union[str, None]):
        """
        设置body
        :param body:
        :return:
        """
        if type(body) != str and body is not None:
            raise MyException("必须是字符串!而不是{}".format(type(body)))
        self.__body = body

    @property
    def body_type(self):
        return self.__body_type

    @body_type.setter
    def body_type(self, body_type):
        self.__body_type = body_type

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server):
        self.__server = server

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, files):
        self.__files = files

    @property
    def cookies(self):
        return self.__cookies

    @cookies.setter
    def cookies(self, cookies):
        self.__cookies = cookies

    @property
    def auth(self):
        return self.__auth

    @auth.setter
    def auth(self, auth):
        self.__auth = auth

    @property
    def auth_type(self):
        return self.__auth_type

    @auth_type.setter
    def auth_type(self, auth_type):
        self.__auth_type = auth_type

    def __get_correct_auth_type(self, auth_type):
        """
        得到争取的auth_type
        :param auth_type:
        :return:
        """
        # 如果auth_type是空，直接原样返回
        if auth_type is None or auth_type == "":
            return None
        try:
            header = Express.calculate_str(self.__config, auth_type)
        except Exception as e:
            raise MyException("解析auth时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    def __get_correct_auth(self, auth):
        """
        得到正确的auth
        :param auth:
        :return:
        """
        # 如果auth是空，直接原样返回
        if auth is None or auth == "":
            return None
        try:
            header = Express.calculate_str(self.__config, auth)
        except Exception as e:
            raise MyException("解析auth时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    def __get_correct_cookies(self, cookies):
        """
        得到正确的cookies字符串
        :param cookies:
        :return:
        """
        # 如果cookies是空，直接原样返回
        if cookies is None or cookies == "":
            return None
        try:
            header = Express.calculate_str(self.__config, cookies)
        except Exception as e:
            raise MyException("解析cookies时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    def __get_correct_path(self, path):
        """
        得到正确的路径
        :param path:
        :return:
        """
        if path is None:
            return path
        if path and path.startswith("/"):
            path = path[1:]
        try:
            path = Express.calculate_str(self.__config, path)
        except Exception as e:
            raise MyException("解析path时产生了一个错误，具体的错误内容如下：{}".format(e))
        return path

    def __get_correct_header(self, header):
        """
        根据协议取到正确的请求头
        :param header:
        :return:
        """
        # 如果请求头是空，直接原样返回
        if header is None or header == "":
            return header
        try:
            header = Express.calculate_str(self.__config, header)
        except Exception as e:
            raise MyException("解析header时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    @staticmethod
    def __get_correct_protocol(protocol):
        """
        得到正确的协议，协议应全是小写
        :param protocol:
        :return:
        """
        if not protocol:
            raise MyException("此接口的协议为空！")
        protocol = protocol.lower()
        if protocol in ["http", "tcp", "https", "sql", "tcp_for_flow_bank"]:
            return protocol
        raise MyException("还不支持[{}]协议!".format(protocol))

    @staticmethod
    def __get_correct_desc(desc):
        """
        获得正确的描述，描述不能为空
        :param desc:
        :return:
        """
        if not desc:
            raise MyException("此接口的描述为空！}")
        return desc

    @staticmethod
    def __get_correct_name(name):
        """
        获得正确的name，name不能为空
        :param name:
        :return:
        """
        if not name:
            raise MyException("接口的名称不能为空!")
        return name

    def __get_correct_param(self, param):
        if param is None:
            return None
        return Express.calculate_str(self.__config, param)

    def __get_correct_body_and_body_type(self, body, body_type):
        """
        得到正确的请求体和请求体格式
        :param body:
        :param body_type:
        :return:
        """
        # 先判断请求体和请求体格式是否为空
        if body is None and body_type is None:
            return None, None
        # 当请求体不为空，请求体格式为空时，默认请求体格式为"key_value"
        if body_type:
            body_type = body_type.lower()
        if body and body_type is None:
            body_type = "key_value"
        try:
            body = Express.calculate_str(self.__config, body)
        except Exception as e:
            raise MyException("解析body时产生了一个错误，具体的错误内容如下：{}".format(e))
        return body, body_type

    def __get_correct_port(self, port):
        """
        得到正确的端口
        :param port:
        :return:
        """
        # 如果端口是空，直接原样返回
        if port is None or port == "":
            return port
        try:
            port = Express.calculate_str(self.__config, port)
        except Exception as e:
            raise MyException("解析port时产生了一个错误，具体的错误内容如下：{}".format(e))
        return port

    def __get_correct_server(self, server):
        """
        得到正确的服务器
        :param server:
        :return:
        """
        if server is None or server == "":
            return server
        try:
            server = Express.calculate_str(self.__config, server)
        except Exception as e:
            raise MyException("解析server时产生了一个错误，具体的错误内容如下：{}".format(e))
        return server

    @staticmethod
    def __get_correct_method(method, protocol):
        """
        得到正确的http请求方法
        :param method:
        :param protocol:
        :return:
        """
        if method:
            method = method.lower()
        if protocol in ["http", "https"] and method not in ["post", "get", "delete", "patch", "put"]:
            raise MyException("此接口配置有误，HTTP接口的请求方法不能是[{}],只能是GET,POST,DELETE,PATCH,PUT!".format(method))
        return method

    @staticmethod
    def __check_need_to_be_replaced(param):
        """
        检查变量需要被替换吗？
        :param param:
        :return:
        """
        if type(param) == dict and len(param) == 0:
            return True
        return False

    def __get_correct_files(self, files):
        """
        取得正确的files
        :param files:
        :return:
        """
        if files is None:
            return None
        if files == "":
            return None
        files = files if type(files) == list else [files]
        n_files = {}
        for file in files:
            file_name = file.get("$value")
            mime = file.get("mime")
            if mime == "":
                mime = None
            name = file.get("name")
            if name is None or name == "":
                raise MyException("文件的name不能为空！")
            n_files[name] = (file_name, mime)
        if n_files == {}:
            return None
        self.__body_type = "key_value"
        return n_files


class Interfaces(object):
    def __init__(self, interface_data, config: ConfigLoader):
        """
        读取所有的接口信息
        :return: None
        """
        # 配置
        self.__config = config
        # 取得处理后接口信息
        self.__interface_info = self.__parse_interface_data(interface_data)

    def get(self, interface_name) -> Interface:
        """
        取得接口
        :return:
        """
        if self.__interface_info.get(interface_name) is None:
            raise MyException("接口 {} 不存在！".format(interface_name))
        return Interface(self.__config, self.__interface_info.get(interface_name))

    @staticmethod
    def __parse_interface_data(interfaces_data):
        """
        提取接口信息，并存入接口字典
        :return:
        """
        interfaces = Utils.extract_attrs_from_dict(interfaces_data, "interface")
        # 如果取到的是字典，则转换为列表
        if type(interfaces) == dict:
            interfaces = [interfaces]
        if interfaces is None:
            interfaces = list()
        # 如果取到的是列表，则遍历列表
        interface_info = dict()
        for interface_data in interfaces:
            # 取得接口名称
            interface_name = Utils.extract_attrs_from_dict(interface_data, "name")
            interface_info[interface_name] = interface_data
        return interface_info
