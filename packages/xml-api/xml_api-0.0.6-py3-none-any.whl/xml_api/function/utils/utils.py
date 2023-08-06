# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: utils of processor
"""
import os
import re
from urllib.parse import quote


class Utils(object):
    AUTO_XML_FILE_NAME_RE = re.compile(
        r"^test_(\d+)([a-zA-Z_\u4e00-\u9fa5，。；（）][a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*)_(\d+)([a-zA-Z_\u4e00-\u9fa5，。；（）]["
        r"a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*)$")

    UNIT_XML_FILE_NAME_RE = re.compile(
        r"^test_([a-zA-Z_\u4e00-\u9fa5，。；（）][a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*)_([a-zA-Z_\u4e00-\u9fa5，。；（）]["
        r"a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*)$")

    BLANK_CHAR = chr(32)
    BLANK_CHAR_BY_CN = chr(12288)

    FLOW_INNER_TAG = ["$order", "set", "flow.py", "if", "for", "return", "while", "selenium", "set", "sql", "interface",
                      "continue", "break", "logger", "elif", "else", "sleep", "selenium", "raise"]

    PRE_TAG = ["processor", "print", "sleep", "set", "print_var", "if", "sql", "while", "break", "continue", "for",
               "expression", "logger", "elif", "else", "raise"]

    MAIN_TAG = ["if", "while", "interface", "set", "flow.py", "return", "for", "break", "sql", "continue",
                "selenium", "sleep", "logger", "elif", "else", "env", "raise"]

    INTERFACE_TAG = ["server", "header", "body", "file", "port", "param", "method", "path", "type"]

    POST_TAG = ["processor", "print", "sleep", "set", "rep_res", "print_var", "if", "sql", "while", "break", "continue",
                "for", "expression", "logger", "elif", "else", "raise"]

    ASSERT_TAG = ["expect"]

    class __Error(object):
        pass

    ERROR = __Error()

    @classmethod
    def merge_and_sort(cls, data: dict, keys: list):
        """
        合并data字典里的keys指定的键，并根据其$order进行升序排序
        :param data:
        :param keys:
        :return:
        """
        merge = []
        for t in keys:
            if t not in data:
                continue
            d = data.get(t)
            # 判断while内容时字典还是列表
            # 字典时直接加入cases即可
            if type(d) == dict:
                d = [d]
            for i in d:
                # 遍历存入
                merge.append({"name": t, "value": i, "$order": i.get("$order")})
        # 根据$order排序
        merge.sort(key=lambda x: x.get("$order"))
        return merge

    @classmethod
    def extract_attrs_from_dict(cls, d: dict, *attr_names):
        """
        从字典中提取指定的属性，当属性嵌套不存在时返回空
        """
        for attr in attr_names:
            if d is None:
                return None
            d = d.get(attr)
        return d

    @classmethod
    def extract_path_and_row(cls, d: dict):
        if d is None:
            return "Unknown Path", "Unknown Line"
        file_path = "Unknown Path"
        if d.get("$file_path"):
            file_path = d.get("$file_path")
        row = "Unknown Line"
        if d.get("$row"):
            row = d.get("$row")
        return file_path, row

    @classmethod
    def quote_(cls, o: dict, encoding: str):
        """
        将字典转为表单格式的字符串
        :param encoding:
        :param o:
        :return:
        """
        l = []
        query = list(o.items())
        for k, v in query:
            if type(k) is str:
                k = quote(k, encoding=encoding)
            if type(v) is str:
                v = quote(v, encoding=encoding)
            l.append(k + '=' + v)
        return '&'.join(l)

    @classmethod
    def is_number(cls, string):
        """
        判断是否是数字
        :param string:
        :return:
        """
        try:
            _t = int(string)
            return True
        except:
            return False

    @classmethod
    def is_float(cls, string):
        """
        判断是否是数字
        :param string:
        :return:
        """
        try:
            _t = float(string)
            return True
        except:
            return False

    @classmethod
    def add_zero_to(cls, text, length: int):
        """
        补零，补零后的长度
        :param text:
        :param length:
        :return:
        """
        if length <= 1:
            length = 2
        format = "{:0>" + str(length) + "d}"
        return format.format(int(text))

    @classmethod
    def extract_module_and_scene(cls, module):
        if cls.AUTO_XML_FILE_NAME_RE.fullmatch(module):
            data = cls.AUTO_XML_FILE_NAME_RE.findall(module)
            return data[0]
        if cls.UNIT_XML_FILE_NAME_RE.fullmatch(module):
            data = cls.UNIT_XML_FILE_NAME_RE.findall(module)
            return None, data[0][0], None, data[0][1]
        return None, None, None, None

    @classmethod
    def split_xml(cls, xml):
        index = xml.find("<?")
        front, back = xml[:index + 1], xml[index + 1:]
        index = back.find("<")
        front += back[:index]
        back = back[index:]
        return front, back

    @classmethod
    def get_pure_file_name(cls, file_path):
        return os.path.basename(file_path).split(".")[0]

    @classmethod
    def upper(cls,string):
        if string is None:
            return None
        return string.upper()

    @classmethod
    def lower(cls,string):
        if string is None:
            return None
        return string.lower()

