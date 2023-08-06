# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: pre processor exception
"""
from .my_exception import MyException


class PreTypeIsIncorrectException(MyException):
    def __init__(self, error_type: str) -> None:
        msg = "标签不支持type属性值为{}".format(error_type)
        super(PreTypeIsIncorrectException, self).__init__(msg)


class PreDescIsNullException(MyException):
    def __init__(self) -> None:
        super(PreDescIsNullException, self).__init__("标签desc属性不能为空!")


class PreKeyTypeIsIncorrectException(MyException):
    def __init__(self, key: str):
        msg = "标签的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{}".format(key)
        super(PreKeyTypeIsIncorrectException, self).__init__(msg)


class PreActIsIncorrectException(MyException):
    def __init__(self, act: str):
        msg = "标签的act错误，不能是:{}".format(act)
        super(PreActIsIncorrectException, self).__init__(msg)


class PreVarTypeIsNotSupportException(MyException):
    def __init__(self, type_: str):
        msg = "标签的var_type不受支持，不能是:{}".format(type_)
        super(PreVarTypeIsNotSupportException, self).__init__(msg)


class PreNameIsNotSupportedException(MyException):
    def __init__(self, name: str):
        msg = "标签的name不符合规则,只能以字母下划线开头且只包含字母数字下划线,不能是:{}".format(name)
        super(PreNameIsNotSupportedException, self).__init__(msg)


class PreNameIsNullException(MyException):
    def __init__(self):
        msg = "标签的name不能是空"
        super(PreNameIsNullException, self).__init__(msg)


class PreValueIsNotSpecifiedException(MyException):
    def __init__(self):
        msg = "标签的value或type属性未指定！"
        super(PreValueIsNotSpecifiedException, self).__init__(msg)


class PreSqlIsNotSpecifiedException(MyException):
    def __init__(self):
        msg = "标签的type为sql时必须配置sql属性，用来说明要执行的sql语句！"
        super(PreSqlIsNotSpecifiedException, self).__init__(msg)


class PreScopeIsIncorrectException(MyException):
    def __init__(self):
        msg = "标签的scope属性不正确，只能是global或local"
        super(PreScopeIsIncorrectException, self).__init__(msg)


class PreExpressIsIncorrectException(MyException):
    def __init__(self, error: str):
        msg = "标签的ex属性指定的表达式计算错误，原因为:{}".format(error)
        super(PreExpressIsIncorrectException, self).__init__(msg)


class PreNotFindValueException(MyException):
    def __init__(self, res_type: str, key: str):
        msg = "标签未在结果：{}中找到关键字为：{}的数据或该关键字不正确！".format(res_type, key)
        super(PreNotFindValueException, self).__init__(msg)


class PreReTypeIsNotSupportedException(MyException):
    def __init__(self, re_type: str):
        msg = "标签不支持处理此种类型的结果:{}！".format(re_type)
        super(PreReTypeIsNotSupportedException, self).__init__(msg)


class PreReqDataIsNullException(MyException):
    def __init__(self):
        msg = "标签无法处理请求报文，因为该接口的请求报文为空！"
        super(PreReqDataIsNullException, self).__init__(msg)


class PreSleepValueIsNotNumberException(MyException):
    def __init__(self, value: str):
        msg = "标签传入的结果值必须一个数字，而不是：{}".format(value)
        super(PreSleepValueIsNotNumberException, self).__init__(msg)


class PreTransferFailException(MyException):
    def __init__(self, value: str, type_: str):
        msg = "标签取到的数据 {} 不是 {} 类型，转型失败".format(value, type_)
        super(PreTransferFailException, self).__init__(msg)


class PreValueAndExceptValueIsNotSameException(MyException):
    def __init__(self, real: str, except_v: str):
        msg = "标签取到的值 {} 与处理器value说明的值 {} 不一致!".format(real, except_v)
        super(PreValueAndExceptValueIsNotSameException, self).__init__(msg)


class PreValueAndExceptValueIsNotMatchedException(MyException):
    def __init__(self, real: str, regex: str):
        msg = "标签取到的值 {} 与处理器value说明的正则表达式 {} 不匹配！".format(real, regex)
        super(PreValueAndExceptValueIsNotMatchedException, self).__init__(msg)


class PreValueTypeIsNotCorrectException(MyException):
    def __init__(self, value, _type):
        msg = "标签取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或tuple".format(value, _type)
        super(PreValueTypeIsNotCorrectException, self).__init__(msg)


class PreValueLengthIsNotCorrectException(MyException):
    def __init__(self, need_length, real_length):
        msg = "标签需要的变量数:{}个与实际得到的变量数:{}个不等".format(need_length, real_length)
        super(PreValueLengthIsNotCorrectException, self).__init__(msg)
