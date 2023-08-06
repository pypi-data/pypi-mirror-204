from datetime import datetime

from .color import Color
from ..beautify.beautify import Beautify
from ..cfg.config import ConfigLoader
from ..utils.utils import Utils
from ...core.client.res_data import ResData


class FormatOutput(object):
    # 标题
    __color_of_title = Color.green_front
    # 默认
    __default = Color.default
    # 关键性
    __color_of_key = Color.purple
    # 空白
    __blank_char = Utils.BLANK_CHAR
    # 中文空白
    __blank_char_by_cn = Utils.BLANK_CHAR_BY_CN

    @staticmethod
    def __to_good_str(string):
        string = str(string)
        return string

    @staticmethod
    def format_request_output(config:ConfigLoader,protocol, desc, address, header, data, data_type, file=None, param=None, cookies=None,
                           auth=None):
        """
        格式化打印请求信息
        :param protocol: HTTP的GET或者POST，或者其他协议
        :param desc: 接口的描述
        :param address: 接口的地址
        :param header:请求头
        :param data: 请求体
        :param data_type: 请求体数据类型
        :param file: 文件接口发送的文件
        :param param: 请求参数
        :param cookies: cookie信息
        :param auth: 认证信息
        :return:
        """
        if config.get_config("body_beautify", bool):
            data = Beautify(data, data_type).beautify()
            if protocol in ['GET', 'POST']:
                header = Beautify(header, "key_value").beautify()
        format_info = ">>>>请求[{}]: {}\n".format(protocol, desc)
        req_time=datetime.now()
        format_info += "{}请求时间: {}\n".format(FormatOutput.__blank_char * 4, req_time)
        format_info += "{}地{}址: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__blank_char_by_cn * 2,
                                            FormatOutput.__to_good_str(address))
        format_info += "{}请{}求头: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__blank_char_by_cn,
                                             "无自定义请求头" if header is None else FormatOutput.__to_good_str(header))
        if cookies is not None:
            format_info += "    Cookies: {}\n".format(FormatOutput.__to_good_str(cookies))
        if auth is not None:
            format_info += "{}认{}证: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__blank_char_by_cn * 2,
                                                FormatOutput.__to_good_str(auth))
        if param is not None:
            format_info += "{}请求参数: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__to_good_str(param))
        format_info += "{}请求数据: {}\n".format(FormatOutput.__blank_char * 4,
                                            "无请求数据" if data is None else FormatOutput.__to_good_str(data))
        if file is not None:
            format_info += "{}上传文件: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__to_good_str(str(file)))
        format_info += "{}数据格式: {}".format(FormatOutput.__blank_char * 4, data_type)
        return format_info

    @staticmethod
    def format_response_output(config:ConfigLoader,protocol, res: ResData):
        """
        格式化打印响应信息
        :param res:
        :param protocol:
        :return:
        """
        code = res.code
        header = res.header
        _type = res.re_type
        if config.get_config("body_beautify", bool):
            data = Beautify(res.text, _type).beautify()
        else:
            data = res.text
        res_time=datetime.now()
        data = FormatOutput.__to_good_str(data)
        format_info = "<<<<响应[{}]:\n".format(protocol)
        format_info += "{}响应时间: {}\n".format(FormatOutput.__blank_char * 4,res_time )
        format_info += "{}状{}态: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__blank_char_by_cn * 2, code)
        format_info += "{}响{}应头: {}\n".format(FormatOutput.__blank_char * 4, FormatOutput.__blank_char_by_cn, header)
        format_info += "{}响应数据: {}{}{}".format(FormatOutput.__blank_char * 4, FormatOutput.__color_of_title, data,
                                              FormatOutput.__default)
        return format_info

    @staticmethod
    def format_out_put(info):
        info = FormatOutput.__to_good_str(info)
        return info

    @staticmethod
    def format_post_info(desc, value):
        var_type = type(value)
        value = FormatOutput.__to_good_str(value)
        info = "[{}]后置处理器打印的值为：[{}{}{}]，值的类型为：{}".format(desc, FormatOutput.__color_of_key, value, FormatOutput.__default,
                                                         var_type.__name__)
        return info

    @staticmethod
    def format_pre_info(desc, value):
        var_type = type(value)
        value = FormatOutput.__to_good_str(value)
        info = "[{}]前置处理器打印的值为：[{}{}{}]，值的类型为：{}".format(desc, FormatOutput.__color_of_key, value, FormatOutput.__default,
                                                         var_type.__name__)
        return info