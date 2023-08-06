# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: tcp client
"""
import logging
import socket
from .client import AbstractClient
from ...exception.my_exception import MyException
from ...function.cfg.config import ConfigLoader
from ...function.data.interface import Interface
from ...function.format.format import FormatOutput

logger = logging.getLogger(__name__)


class TCP(AbstractClient):
    """
    TCP 接口客户端
    """

    def __init__(self, config: ConfigLoader, interface_info: Interface, interface_data: dict, _type, *context: dict):
        """
        HTTP 接口客户端
        :param interface_info:接口信息
        :param interface_data: 接口数据
        :param context: 场景上下文
        :return:
        """
        super().__init__(config, interface_info, interface_data, *context)
        self.__type = _type

    def _request(self):
        # 获得请求体
        body = self._interface_info.body
        body = "" if body is None else body
        h = self._interface_info.header
        h = "" if h is None else h
        data = "{}{}".format(h, body)
        data = data
        # 构造请求头
        name = self._interface_info.name
        port = self._interface_info.port
        server = self._interface_info.server
        body_type = self._interface_info.body_type
        if self.__type == "tcp":
            client = TcpClient(server, port, data, self._config)
        elif self.__type == "tcp_for_flow_bank":
            client = TcpClientForFB(server, port, data, self._config)
        else:
            raise MyException("不支持的TCP协议：{}!".format(self.__type))
        logger.info(FormatOutput.format_request_output(self._config, "TCP", name, "{}:{}".format(
            server, port), client.header, data, body_type))
        res = client.request()
        self._res.code = res.code
        self._res.header = res.header
        self._res.text = res.text
        # 打印响应结果
        logger.info(FormatOutput.format_response_output(self._config, "TCP", self._res))


class TcpRes(object):
    def __init__(self, code, header, text):
        self.__code = code
        self.__header = header
        self.__text = text

    @property
    def code(self):
        return self.__code

    @property
    def header(self):
        return self.__header

    @property
    def text(self):
        return self.__text


class TcpClient(object):
    """
    普通tcp客户端，根据报文长度计算header
    """

    def __init__(self, server, port, data, config: ConfigLoader):
        self.__config = config
        self.__timeout = self.__config.get_config("client_tcp_timeout", float)
        self.__encoding = self.__config.get_config("client_tcp_encoding")
        self.__server = server
        self.__port = port
        self.__data = data
        self.__b_data = self.__data.encode(self.__encoding)
        self.__header, self.__b_header = self.__generate_header()

    @property
    def header(self):
        return self.__header

    def request(self):
        s = None
        try:
            # 检查端口
            self.__check_port(self.__port)
            # 创建TCP套接字
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置超时时间
            s.settimeout(self.__timeout)
            # 连接到端口
            s.connect((self.__server, int(self.__port)))
            # 对数据编码
            data = self.__b_data
            # 对头编码
            header = self.__b_header
            # 发送头
            s.sendall(header)
            # 发送数据
            s.sendall(data)
            # 再次设置超时时间
            s.settimeout(self.__timeout)
            # 先接收8位头部
            res_h = s.recv(8)
            if res_h is None or res_h == "" or res_h == b'':
                raise MyException("接收的响应头为空，请检查请求报文是否正确")
            # 获得接下来的数据宽度
            width = int(res_h)
            # 定义完成的数据byte
            res_data_of_byte = bytes()
            # 当接收的数据小于0时
            while width > 0:
                # 再次设置超时时间
                s.settimeout(self.__timeout)
                # 每次接收1024个字节
                byte_data = s.recv(1024)
                # 减去实际接收的数据宽度
                width = width - len(byte_data)
                # 拼接返回的数据
                res_data_of_byte += byte_data
            return TcpRes(200, res_h.decode(self.__encoding), res_data_of_byte.decode(self.__encoding))
        except UnicodeDecodeError:
            raise MyException("TCP客户端解码响应报文错误，建议修改编码方式")
        except ConnectionRefusedError:
            raise MyException("[WinError 10061] 由于目标计算机拒绝，无法连接。")
        except Exception:
            raise
        finally:
            if s:
                s.close()

    def __generate_header(self):
        # 根据header（定长8）和body的长度，生成请求报文的header
        # sb的值，i在3-8之间，补5个0，再加上body总长度
        sb = ''
        body_len = len(self.__b_data)
        head = str(body_len)
        for i in range(len(head), 8):
            sb += '0'
        sb += str(body_len)
        return sb, sb.encode(self.__encoding)

    @staticmethod
    def __check_port(port):
        if not port.isnumeric():
            raise MyException("TCP接口的端口必须是数字，不能是：{}".format(port))


class TcpClientForFB(object):
    """
    流程银行的tcp
    """

    def __init__(self, server, port, data, config: ConfigLoader):
        self.__config = config
        self.__timeout = self.__config.get_config("client_tcp_timeout", float)
        self.__encoding = self.__config.get_config("client_tcp_encoding")
        self.__server = server
        self.__port = port
        self.__data = data
        self.__b_data = self.__data.encode(self.__encoding)
        self.__header, self.__b_header = self.__generate_header()

    @property
    def header(self):
        return self.__header

    def request(self):
        s = None
        try:
            # 检查端口
            self.__check_port(self.__port)
            # 创建TCP套接字
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置超时时间
            s.settimeout(self.__timeout)
            # 连接到端口
            s.connect((self.__server, int(self.__port)))
            # 对数据编码
            data = self.__b_data
            # 对头编码
            header = self.__b_header
            # 发送头
            s.sendall(header)
            # 发送数据
            s.sendall(data)
            # 再次设置超时时间
            s.settimeout(self.__timeout)
            # 先接收4位头部
            res_h = s.recv(4)
            if res_h is None or res_h == "" or res_h == b'':
                raise MyException("接收的响应头为空，请检查请求报文是否正确")
            # 获得接下来的数据宽度
            width = self.__get_response_length(res_h)
            # 定义完成的数据byte
            res_data_of_byte = bytes()
            # 当接收的数据小于0时
            while width > 0:
                # 再次设置超时时间
                s.settimeout(self.__timeout)
                # 每次接收1024个字节
                byte_data = s.recv(1024)
                # 减去实际接收的数据宽度
                width = width - len(byte_data)
                # 拼接返回的数据
                res_data_of_byte += byte_data
            return TcpRes(200, res_h, res_data_of_byte.decode(self.__encoding))
        except UnicodeDecodeError:
            raise MyException("TCP客户端解码响应报文错误，建议修改编码方式")
        except ConnectionRefusedError:
            raise MyException("[WinError 10061] 由于目标计算机拒绝，无法连接。")
        except Exception:
            raise
        finally:
            if s:
                s.close()

    def __generate_header(self):
        from ...useful.jvm import JVMProcess
        num = len(self.__b_data)
        return JVMProcess.exe(generate_header_detail, num)

    @staticmethod
    def __get_response_length(res_h):
        num = 0
        for i in range(4):
            num += res_h[i] << 24 - i * 8
        return num

    @staticmethod
    def __check_port(port):
        if not port.isnumeric():
            raise MyException("TCP接口的端口必须是数字，不能是：{}".format(port))


def generate_header_detail(jp, num):
    t = list()
    for i in range(4):
        t.append(jp.JByte(num >> 24 - i * 8))
    t_t = [i + 256 if i < 0 else i for i in t]
    b_header = bytes(bytearray(t_t))
    return b_header, b_header
