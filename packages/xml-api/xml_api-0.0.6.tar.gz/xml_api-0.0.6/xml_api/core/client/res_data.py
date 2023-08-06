# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: response of client
"""
import re


class ResData(object):
    __xml_re = re.compile(r"[\S\s]*?<\w*/?>[\s\S]*?(</\w*>)?")
    __json_re = re.compile(r"{[\s\S]*?}")

    def __init__(self, response_code=-1, response_text="", response_header="", response_header_type=None,
                 response_text_type_from_http=None):
        # 构建一个响应结果
        # 接口响应结果
        self.__response_code = response_code
        # 接口响应内容
        self.__response_text = response_text
        # 接口响应头
        self.__response_header = response_header
        # 标志响应结果是否需要重新推测
        self.__need_speculate_res_type = True
        # 推测响应结果类型
        self.__re_type = None
        # 响应头的类型
        self.__response_header_type = response_header_type
        # http专有字段，用于说明响应的类型
        self.__response_text_type_from_http = response_text_type_from_http

    def __speculate_res_type(self):
        """
        推测响应结果类型
        json,xml
        """
        if self.__re_type is not None and self.__need_speculate_res_type is False:
            return self.__re_type
        self.__need_speculate_res_type = False
        if self.__response_text_type_from_http is not None:
            if "text/html" == self.__response_text_type_from_http:
                self.__re_type = "html"
            elif "application/json" == self.__response_text_type_from_http:
                self.__re_type = "json"
        if self.__re_type is not None:
            return self.__re_type
        res = str(self.__response_text)
        if "</html>" in res and "</body>" in res:
            self.__re_type = "html"
        elif ResData.__json_re.match(res):
            self.__re_type = "json"
        elif ResData.__xml_re.match(res):
            self.__re_type = "xml"
        return self.__re_type

    @property
    def re_type(self):
        return self.__speculate_res_type()

    @re_type.setter
    def re_type(self, re_type):
        self.__re_type = re_type

    @property
    def code(self):
        return self.__response_code

    @code.setter
    def code(self, code):
        self.__response_code = code

    @property
    def text(self):
        return self.__response_text

    @text.setter
    def text(self, text):
        self.__need_speculate_res_type = True
        self.__response_text = text

    @property
    def header(self):
        return self.__response_header

    @header.setter
    def header(self, header):
        self.__response_header = header

    @property
    def header_type(self):
        return self.__response_header_type

    @header_type.setter
    def header_type(self, header_type):
        self.__response_header_type = header_type

    @property
    def response_text_type_from_http(self):
        return self.__response_text_type_from_http

    @response_text_type_from_http.setter
    def response_text_type_from_http(self, _type):
        self.__response_text_type_from_http = _type
