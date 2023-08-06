# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: post processor MyException
"""
from .my_exception import MyException


class PostTypeIsIncorrectException(MyException):
    def __init__(self, error_type: str) -> None:
        msg = "标签处理器不支持此type:{}".format(error_type)
        super(PostTypeIsIncorrectException, self).__init__(msg)


class PostDescIsNullException(MyException):
    def __init__(self) -> None:
        super(PostDescIsNullException, self).__init__("标签的desc不能为空！")


class PostKeyTypeIsIncorrectException(MyException):
    def __init__(self, key: str):
        msg = "标签的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{}！".format(key)
        super(PostKeyTypeIsIncorrectException, self).__init__(msg)


class PostActIsIncorrectException(MyException):
    def __init__(self, act: str):
        msg = "标签的act错误,不能是:{}!".format(act)
        super(PostActIsIncorrectException, self).__init__(msg)


class PostVarTypeIsNotSupportException(MyException):
    def __init__(self, type_: str):
        msg = "标签的var_type不受支持,不能是:{}".format(type_)
        super(PostVarTypeIsNotSupportException, self).__init__(msg)


class PostNameIsNotSupportedException(MyException):
    def __init__(self, name: str):
        msg = "标签的name不符合规则,只能以字母下划线开头且只包含字母数字下划线,不能是:{}".format(name)
        super(PostNameIsNotSupportedException, self).__init__(msg)


class PostNameIsNullException(MyException):
    def __init__(self):
        msg = "标签的name不能是空!"
        super(PostNameIsNullException, self).__init__(msg)


class PostValueIsNotSpecifiedException(MyException):
    def __init__(self):
        msg = "标签的value或type未指定！"
        super(PostValueIsNotSpecifiedException, self).__init__(msg)


class PostSqlIsNotSpecifiedException(MyException):
    def __init__(self):
        msg = "标签未配置sql语句!"
        super(PostSqlIsNotSpecifiedException, self).__init__(msg)

class PostScopeIsNotSupportException(MyException):
    def __init__(self, scope: str):
        msg = "标签的scope不受支持,不能是:{}".format(scope)
        super(PostScopeIsNotSupportException, self).__init__(msg)


class PostExpressIsIncorrectException(MyException):
    def __init__(self, error: str):
        msg = "标签的ex属性指定的表达式计算出错，错误原因时为:{}".format(error)
        super(PostExpressIsIncorrectException, self).__init__(msg)


class PostNotFindValueException(MyException):
    def __init__(self, res_type: str, key: str):
        msg = "标签未在结果 {} 中找到关键字为 {} 或关键字格式不正确".format(res_type, key)
        super(PostNotFindValueException, self).__init__(msg)


class PostReTypeIsNotSupportedException(MyException):
    def __init__(self, re_type: str):
        msg = "标签不支持处理此种类型的结果:{}".format(re_type)
        super(PostReTypeIsNotSupportedException, self).__init__(msg)


class PostReqDataIsNullException(MyException):
    def __init__(self):
        msg = "标签无法处理请求报文，因为该接口的请求报文为空!"
        super(PostReqDataIsNullException, self).__init__(msg)


class PostSleepValueIsNotNumberException(MyException):
    def __init__(self, value: str):
        msg = "标签传入的结果值必须一个数字，而不是：{}".format(value)
        super(PostSleepValueIsNotNumberException, self).__init__(msg)


class PostTransferFailException(MyException):
    def __init__(self, value: str, type_: str):
        msg = "标签取到的数据 {} 不是 {} 类型，转型失败!".format(value, type_)
        super(PostTransferFailException, self).__init__(msg)


class PostValueAndExceptValueIsNotSameException(MyException):
    def __init__(self, real: str, except_v: str):
        msg = "标签取到的值 {} 与value属性说明的值 {} 不一致！".format(real, except_v)
        super(PostValueAndExceptValueIsNotSameException, self).__init__(msg)


class PostValueAndExceptValueIsNotMatchedException(MyException):
    def __init__(self, real: str, regex: str):
        msg = "标签取到的值 {} 与处理器value说明的正则表达式 {} 不匹配!".format(real, regex)
        super(PostValueAndExceptValueIsNotMatchedException, self).__init__(msg)


class PostValueTypeIsNotCorrectException(MyException):
    def __init__(self, value, _type):
        msg = "标签取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或tuple!".format(value, _type)
        super(PostValueTypeIsNotCorrectException, self).__init__(msg)


class PostValueLengthIsNotCorrectException(MyException):
    def __init__(self, need_length, real_length):
        msg = "标签需要的变量数:{}个与实际得到的变量数:{}个不等!".format(need_length, real_length)
        super(PostValueLengthIsNotCorrectException, self).__init__(msg)
