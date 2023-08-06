# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: if tag MyException
"""
from .my_exception import MyException


class IFExpressIncorrectException(MyException):
    def __init__(self, error: str):
        msg = "标签的ex表达式计算错误，具体错误原因为:{}".format( error)
        super(IFExpressIncorrectException, self).__init__(msg)


class IFDescIsNullException(MyException):
    def __init__(self):
        super(IFDescIsNullException, self).__init__("if标签的描述不能为空！")


class UnexpectedTagsException(MyException):
    def __init__(self):
        super(UnexpectedTagsException, self).__init__("存在不应存在的标签，请检查！")


class FileIsNotExistsException(MyException):
    def __init__(self, file):
        super(FileIsNotExistsException, self).__init__("文件上传接口中指定的文件：{} 不存在，请检查！".format(file))


class ReqDataIsIncorrectException(MyException):
    def __init__(self):
        super(ReqDataIsIncorrectException, self).__init__("请求报文格式不正确，请检查！")


class XMLRuntimeException(MyException):
    def __init__(self, msg):
        super(XMLRuntimeException, self).__init__(msg)


class SetupException(MyException):
    def __init__(self, msg):
        super(SetupException, self).__init__("案例前置处理异常：{}".format(msg))


class TeardownException(MyException):
    def __init__(self, msg):
        super(TeardownException, self).__init__("案例后置处理异常：{}".format(msg))
