# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: post processor
"""
import logging
import re
import time

from xml_api.core.client.res_data import ResData
from ...exception.db import *
from ...exception.expect import *
from ...exception.my_assertion_error import MyAssertionError
from ...exception.other import *
from ...exception.post import *
from ...function.cfg.config import ConfigLoader
from ...function.data.interface import Interface
from ...function.database.db import DB
from ...function.express.express import Express, ParamType
from ...function.format.format import FormatOutput
from ...function.parse.json_parse import JsonParse
from ...function.parse.regex_parse import Regex
from ...function.parse.table_parse import TableParse
from ...function.parse.xml_parse import XmlParse
from ...function.utils.utils import Utils

logger = logging.getLogger(__name__)


class ProcessorData(object):
    """
    后置处理器单条数据
    """
    __name_re = re.compile(r"[\w_][\w_\d]*")

    def __init__(self, db_info: str, type_p: str, key: str, act: str, name: str, var_type: str,
                 value: str,
                 re_type: str, desc: str, value_: str, scope: str, res_type: str, req_type):
        """
        单条数据
        :param type_p: 可选值：res_data，值结果从响应报文中取到
        :param key: any或$whole，指取结果的关键值还是整体
        :param act: set，指获得结果中的key对应的指并注入上下文中，取名为name
        :param name: name 取的名字，如果未传，则取value指
        :param value: value 与结果比对的值，如果以美元符号开头，则指从上下文中取出对比的值
        :param re_type: 结果的类型 json
        :param desc: 处理器描述
        :param value_: sql
        :param scope:if参数
        :param res_type:推测的响应类型
        :param req_type:说明的请求类型
        :return:
        """
        # 取到正确的if参数
        self.scope = self.__get_correct_scope(scope)
        # 取到正确的type参数
        self.type = self.__get_correct_type(type_p)
        # 取到正确的db_info对象，如果type is sql
        self.db_info = self.__get_correct_db_info(db_info)
        # 取到正确的动作
        self.act = self.__get_correct_act(act)
        # 取到正确的name
        self.names, self.var_type = self.__get_correct_names_and_var_type(name, var_type, key, self.act)
        # 取到正确的value
        self.value = self.__get_correct_value(value, self.act)
        # 取到正确的sql
        self.sql = self.__get_correct_sql(value_, self.type)
        # 取到正确的re_type
        self.re_type = self.__get_correct_re_type(re_type, self.type, self.sql, res_type, req_type, key)
        # key使用的正则表达式
        # 取第几个值
        # 取到正确的key
        self.key, self.key_regex, self.key_count = self.__get_correct_key(key, self.re_type)
        # 取到正确的desc参数
        self.desc = self.__get_correct_desc(desc)

    @staticmethod
    def __get_correct_type(type_p):
        """
        默认发为res_data
        取到正确的后置处理器的类型
        res_data:代表从结果中取值
        sql：代表执行sql，从sql的结果中取值
        :param type_p:
        :return:
        """
        if type_p is None:
            return "none"
        if type_p:
            type_p = type_p.lower()
        if type_p in ["res_data", "sql", "req_data", "none", "res_header", "req_header"]:
            return type_p
        else:
            raise PostTypeIsIncorrectException(type_p)

    @staticmethod
    def __get_correct_desc(desc):
        """
        获得正确的描述，描述不能为空
        :param desc:
        :return:
        """
        if not desc:
            raise PostDescIsNullException()
        return desc

    @staticmethod
    def __get_correct_key(key, re_type):
        """
        取到争取的key，key默认为$whole
        :param key:
        :return:
        """
        key_regex, key_count = None, None
        if key is None:
            return "$whole"
        if Regex.start_with_regex(key):
            # 当是正则表达式时，获得其正则表达式
            key_regex, key_count = Regex.get_real_regex(key)
            key = "$regex"
        if key not in ["$whole", "$rows", "$columns"] and re_type == "table" and not TableParse.check_key(key):
            # 当结果类型为table时，判断key是否符合要求，如果不符合则抛出错误
            raise PostKeyTypeIsIncorrectException(key)
        return key, key_regex, key_count

    @staticmethod
    def __get_correct_re_type(re_type, type_a, sql, res_type, req_type, key):
        """
        取到正确的re_type，默认为None
        json,xml,key_value,number,table,html
        :return:
        """
        if re_type is None or re_type == "":
            # 自动推断re_type
            if type_a == "sql" and sql:
                if DB.is_a_query_statement(sql):
                    # 如果是查询语句
                    if key in ["$rows", "$columns"]:
                        return "number"
                    return "table"
                else:
                    return "number"
            elif type_a in ["res_header", "req_header"]:
                return "key_value"
            elif type_a == "req_data":
                return req_type
            elif type_a == "res_data":
                return res_type if res_type is not None else req_type
            else:
                return None
        return re_type.lower()

    @staticmethod
    def __get_correct_act(act):
        """
        取到正确的动作，不能为空
        :param act:
        :return:
        """
        if act is None:
            raise PostActIsIncorrectException("None")
        if act:
            act = act.lower()
        if act in ["equal", "set", "match", "print", "sleep", "replace_body", "execute", "logger"]:
            return act
        else:
            raise PostActIsIncorrectException(act)

    @staticmethod
    def __get_correct_names_and_var_type(name, var_type, key, act):
        """
        取到正确的name和类型,name只能以字母，下划线开头且只能包含字母数字下划线
        :param name:
        :return:
        """
        names = []
        if var_type not in ["str", "int", "float", "bool", "auto", None]:
            raise PostVarTypeIsNotSupportException(var_type)
        if name is None and act == "set":
            # 判断key是否包含特殊字符
            if key is None:
                raise PostNameIsNullException()
            else:
                if ProcessorData.__name_re.fullmatch(key):
                    names.append(key)
                else:
                    raise PostNameIsNullException()
        if name:
            if "," in name:
                names = name.split(",")
                names = list(map(lambda x: x.strip(), names))
            else:
                names = [name.strip()]
            for n in names:
                if not ProcessorData.__name_re.fullmatch(n):
                    raise PostNameIsNotSupportedException(n)
        return names, var_type

    @staticmethod
    def __get_correct_value(value, act):
        """
        取到正确的value
        :param value:
        :return:
        """
        if value is None:
            if act in ["match", "equal"]:
                raise PostValueIsNotSpecifiedException()
            return None
        return value

    @staticmethod
    def __get_correct_sql(value_, type_p):
        """
        取到正确的sql
        :param value_:
        :return:
        """
        if type_p == "sql" and (value_ is None or value_ == ""):
            raise PostSqlIsNotSpecifiedException()
        if value_:
            # sql语句存在时检查sql语句
            DB.check_sql(value_)
        if value_ is None:
            return None
        return value_

    @staticmethod
    def __get_correct_scope(scope):
        if scope is None:
            return 'global'
        if scope not in ['global', 'local']:
            raise PostScopeIsNotSupportException(scope)
        return scope

    @staticmethod
    def __get_correct_db_info(db_info):
        """
        取到正确的db_info对象，如果type is sql
        :param db_info:
        :return:
        """
        return db_info


class AssertData(object):
    """
    单条断言数据
    """

    __express_re = re.compile(r"\${(.*?)}")

    def __init__(self, db_info: str, type_a: str, key: str, act: str, re_type: str, sql: str, desc: str,
                 expect_value: str, value: str, var_type: str, res_type: str, req_type: str):
        # 取到正确的type，用来指示断言什么内容,默认断言结果
        self.type = self.__get_correct_type(type_a)
        # 取到正确的db_info，如果type is sql
        self.db_info = self.__get_correct_db_info(db_info)
        # 当结果来源为sql时，此要执行的sql不能为空
        self.sql = self.__get_correct_sql(sql, self.type)
        # 结果的类型
        self.re_type = self.__get_correct_re_type(re_type, self.type, self.sql, res_type, req_type, key)
        # 结果中的指定关键字：$whole|any|$regex[]:
        self.key, self.key_regex, self.key_count = self.__get_correct_key(key, self.re_type, self.type)
        # 断言的动作:equal|match
        self.act = self.__get_correct_act(act)
        # 获取正确的期望值
        self.expect_value = self.__get_correct_expect_value(expect_value)
        # 获取value
        self.value = self.__get_correct_value(value, self.type)
        # 获取var_type
        self.var_type = self.__get_correct_var_type(var_type)
        # 取到正确的断言器描述
        self.desc = self.__get_correct_desc(desc, self.type, self.act, self.key)

    @staticmethod
    def __get_correct_value(value, type_):
        """
        取到正确的value
        :param value:
        :return:
        """
        if value is None:
            if type_ == "expression":
                raise ExpectTagOfValueIsNullException()
            return None
        return value

    @staticmethod
    def __get_correct_type(type_a):
        """
        取到正确的断言器的类型
        :param type_a:
        :return:
        """
        if type_a is None:
            return "res_data"
        if type_a:
            return type_a.lower()

    @staticmethod
    def __get_correct_desc(desc, type_, act, key):
        """
        取到正确的断言器描述
        :param desc:
        :return:
        """
        if desc:
            return desc
        if type_ == "res_data":
            o_type = "响应数据"
        elif type_ == "res_header":
            o_type = "响应头"
        elif type_ == "expression":
            o_type = "表达式"
        elif type_ == "sql":
            o_type = "数据库"
        elif type_ == "status":
            o_type = "响应状态码"
        else:
            o_type = "未知"
        if act == "include":
            o_act = "包含"
        elif act == "in":
            o_act = "存在于"
        elif act == "equal":
            o_act = "等于"
        elif act == "not include":
            o_act = "不包含"
        elif act == "not in":
            o_act = "不存在于"
        elif act == "match":
            o_act = "匹配"
        elif act == "greater":
            o_act = "大于"
        elif act == "greater or equal":
            o_act = "大于等于"
        elif act == "less":
            o_act = "小于"
        elif act == "less or equal":
            o_act = "小于等于"
        elif act == "not equal":
            o_act = "不等于"
        elif act == "content equal":
            o_act = "内容相等"
        elif act == "content not equal":
            o_act = "内容不相等"
        else:
            o_act = "未知操作"
        if key == "$whole":
            if act == "match":
                return "断言{}整体{}期望正则表达式".format(o_type, o_act)
            else:
                return "断言{}整体{}期望值".format(o_type, o_act)
        elif key == "$row":
            if act == "match":
                return "断言{}受影响行数{}期望正则表达式".format(o_type, o_act)
            else:
                return "断言{}受影响行数{}期望值".format(o_type, o_act)
        elif key == "$columns":
            if act == "match":
                return "断言{}受影响列数{}期望正则表达式".format(o_type, o_act)
            else:
                return "断言{}受影响列数{}期望值".format(o_type, o_act)
        else:
            if act == "match":
                return "断言{}中的{}{}期望正则表达式".format(o_type, key, o_act)
            else:
                return "断言{}中的{}{}期望值".format(o_type, key, o_act)

    @staticmethod
    def __get_correct_re_type(re_type, type_a, sql, res_type, req_type, key):
        """
        取到正确的断言结果类型
        :param re_type:
        :return:
        """
        if re_type is None or re_type == "":
            # 自动推断re_type
            if type_a == "sql" and sql:
                if DB.is_a_query_statement(sql):
                    # 如果是查询语句
                    if key in ["$rows", "$columns"]:
                        return "number"
                    return "table"
                else:
                    return "number"
            elif type_a in ["res_header", "req_header"]:
                return "key_value"
            elif type_a == "req_data":
                return req_type
            elif type_a == "res_data":
                return res_type if res_type is not None else req_type
            elif type_a == "status":
                return "number"
            else:
                return None
        return re_type.lower()

    @staticmethod
    def __get_correct_key(key, re_type, type_a):
        """
        取得正确的断言器的key
        :param key:
        :return:
        """
        key_regex, key_count = None, None
        if key is None or key == "" or type_a == "expression":
            key = "$whole"
        if Regex.start_with_regex(key):
            # 当是正则表达式时，获得其正则表达式
            key_regex, key_count = Regex.get_real_regex(key)
            key = "$regex"
        if key not in ["$whole", "$rows", "$columns"] and re_type == "table" and not TableParse.check_key(key):
            # 当结果类型为table时，判断key是否符合要求，如果不符合则抛出错误
            raise ExpectKeyTypeIsIncorrectException(key)
        return key, key_regex, key_count

    @staticmethod
    def __get_correct_act(act):
        """
        取得正确的动作
        :param act:
        :return:
        """
        if act is None:
            raise ExpectActIsNullException()
        return act.lower()

    @staticmethod
    def __get_correct_sql(sql, type_a):
        """
        获得正确的sql
        :param sql:
        :param type_a:
        :return:
        """
        if type_a == "sql" and (sql is None or sql == ""):
            raise ExpectSqlIsNullException()
        if sql:
            # sql语句存在时检查sql语句
            DB.check_sql(sql)
        if sql is None:
            return None
        return sql

    @staticmethod
    def __get_correct_expect_value(value):
        """
        取到正确的value
        :param value:
        :return:
        """
        if value is None:
            raise ExpectValueIsNullException()
        return value

    @staticmethod
    def __get_correct_db_info(db_info):
        """
        取到正确的db对象，如果type is sql
        :param db_info:
        :return:
        """
        return db_info

    @staticmethod
    def __get_correct_var_type(var_type: str):
        """
        取到正确的实际值类型
        :return:
        """
        if var_type not in ["str", "int", "float", "bool", "auto", None]:
            raise MyException("断言标签的var_type不受支持,不能是:{}!".format(var_type))
        return var_type


class PostProcessor(object):
    """
    后置处理器
    """
    # 空白字符正则
    __space_re_o = re.compile(r"\s")

    # 后置相关标签
    __post_tag = Utils.POST_TAG
    # 断言标签
    __assert_tag = Utils.ASSERT_TAG

    def __init__(self, config: ConfigLoader, interface_data: dict, interface_info: Interface, data: dict, res: ResData):
        self.__config = config
        # 期望的实际值和期望值的长度
        self.__length_for_expect = self.__config.get_config("expect_length", int)
        # db_info
        self.__db_info = data.get("db_info")
        # 接口信息
        self.__interface_info = interface_info
        # 接口数据
        self.__interface_data = interface_data
        # 响应
        self.__res = res
        # 后置处理数据
        self.__data = data
        # 循环的数量
        self.__cycle = 0
        # 记录break的状态
        self.__break = False
        # 记录continue的状态
        self.__continue = False

    def work(self, *context: dict):
        """
        后置处理器开始工作
        """
        logger.info("执行后置处理")
        # 创建一个新的上下文
        new_context = {}
        self.__core(self.__data, self.__db_info, new_context, *context)

    def __core(self, data, db_info, *context: dict):
        """
        工作核心
        """
        un = self.__assert_tag + self.__post_tag
        is_if = False
        hit_if = False
        for post in Utils.merge_and_sort(data, un):
            # 判断一下循环数量是否不为0，break和continue是否为true
            if self.__cycle != 0 and (self.__break or self.__continue):
                return
            # 合并后置处理器
            name = post.get("name")
            value = post.get("value")
            logger.info("执行{}标签".format(name))
            # 判断是if还是其他
            if name == "if":
                # 处理if
                is_if = True
                hit_if = self.__if(value, db_info, *context)
            elif name == "elif":
                if not is_if:
                    raise MyException("标签 elif 位置出错！")
                if hit_if:
                    continue
                hit_if = self.__if(value, db_info, *context)
            elif name == "else":
                if not is_if:
                    raise MyException("标签 else 位置出错！")
                if hit_if:
                    hit_if = False
                    is_if = False
                    continue
                self.__else(value, db_info, *context)
            elif name == "break" and self.__cycle != 0:
                is_if = False
                self.__break = True
            elif name == "continue" and self.__cycle != 0:
                is_if = False
                self.__continue = True
            elif name == "while":
                # 处理while
                is_if = False
                self.__cycle += 1
                self.__while(value, db_info, *context)
                self.__cycle -= 1
            elif name == "for":
                self.__cycle += 1
                is_if = False
                self.__for(value, db_info, *context)
                self.__cycle -= 1
            elif name == "raise":
                is_if = False
                self.__raise(value, *context)
            else:
                is_if = False
                if name in self.__post_tag:
                    # 其他情况
                    # 单个处理器参数
                    db_info = db_info if value.get("db_info") is None else Express.calculate_str(self.__config,
                                                                                                 value.get("db_info"),
                                                                                                 *context)
                    type_ = value.get("type")
                    key = value.get("key")
                    desc = value.get("desc")
                    n = value.get("name")
                    var_type = value.get("var_type")
                    v = value.get("value")
                    re_type = value.get("re_type")
                    _v = value.get("$value")
                    scope = value.get("scope")
                    sql = value.get("sql")
                    if name == "processor":
                        raise MyException("processor标签已弃用，请使用对应标签替换！")
                    elif name == "print":
                        v = _v if v is None else _v
                        type_ = type_ if type_ else "res_data" if v is None else "none"
                        key = "$whole" if key is None else key
                        act = "print"
                        desc = desc if desc else "打印响应报文" if type_ == "res_data" and key == "$whole" else "打印"
                    elif name == "sleep":
                        type_ = "none" if type_ is None else type_
                        key = "$whole" if key is None else key
                        act = "sleep"
                        v = value.get("time")
                        desc = "睡眠 {} 秒".format(v)
                    elif name == "logger":
                        type_ = "none" if type_ is None else type_
                        key = "$whole" if key is None else key
                        act = "logger"
                        v = _v if v is None else v
                        desc = "日志记录"
                    elif name == "set":
                        type_ = "none" if type_ is None else type_
                        key = "$whole" if key is None else key
                        scope = "global" if scope is None else scope
                        act = "set"
                        v = v if v is not None else _v
                        desc = desc if desc is not None else "注入变量[{}]".format(
                            n) if type_ == "none" else "从 {} 提取 {} ,并取名 {} 注入变量池".format(type_, key, n)
                    elif name == "rep_res":
                        v = v if v is not None else _v
                        type_ = "none" if type_ is None else type_
                        key = "$whole" if key is None else key
                        act = "replace_body"
                        desc = "替换响应报文"
                    elif name == "print_var":
                        v = "${{{}}}".format(n)
                        type_ = "none"
                        key = "$whole"
                        act = "print"
                        desc = "打印变量[{}]".format(n)
                    elif name == "sql":
                        desc = "执行sql"
                        type_ = "sql"
                        key = "$whole" if key is None else key
                        # 如果存在name，则使用set动作，不存在则是用match
                        act = "match" if n is None else "set"
                        scope = "global" if scope is None else scope
                        v = ".*" if n is None else v if v is not None else _v
                    elif name == "expression":
                        type_ = "none"
                        key = "$whole"
                        v = _v
                        desc = "执行表达式 {}".format(v)
                        act = "execute"
                    else:
                        raise UnexpectedTagsException()
                    post = ProcessorData(db_info, type_, key, act, n, var_type, v, re_type, desc, sql,
                                         scope,
                                         self.__res.re_type,
                                         self.__interface_info.body_type)
                    self.__work_for_post(post, *context)
                else:
                    # 断言处理
                    db_info = db_info if value.get("db_info") is None else Express.calculate_str(self.__config,
                                                                                                 value.get("db_info"),
                                                                                                 *context)
                    ass = AssertData(db_info, value.get("type"), value.get("key"), value.get("act"),
                                     value.get("re_type"), value.get("sql"), value.get("desc"), value.get("$value"),
                                     value.get("value"), value.get("var_type"), self.__res.re_type,
                                     self.__interface_info.body_type)
                    self.__work_for_assert(ass, *context)

    def __for(self, data, db_info, *context: dict):
        """
        遍历数据
        :param data:
        :param context:
        :return:
        """
        logger.debug("正在遍历数据")
        items = Express.calculate_str(self.__config, data.get("data"), *context)
        if type(items) not in [dict, list, tuple]:
            raise MyException("for标签仅能遍历字典、列表、元祖，不可遍历：{}".format(type(items)))
        key = data.get("name")
        key_len = len(key.split(","))
        keys = key.split(",")
        db_info = db_info if data.get("db_info") is None else Express.calculate_str(self.__config, data.get("db_info"),
                                                                                    *context)
        if type(items) == dict and key_len not in [2, 3]:
            raise MyException("for标签遍历字典时，必须提供2个或3个key，且用英文逗号分开")
        if type(items) in [list, tuple] and key_len not in [1, 2]:
            raise MyException("for标签遍历列表、元祖时，必须提供1个或2个key，且用英文逗号分开")
        if key_len > 1:
            keys = list(map(lambda x: x.strip(), keys))
        new_context = {}
        if type(items) == dict:
            if len(items.items()) > 0:
                index = 0
                for k, v in items.items():
                    logger.debug("将 {} 注入局部变量池，取名 {}".format(str(k), keys[0]))
                    logger.debug("将 {} 注入局部变量池，取名 {}".format(str(v), keys[1]))
                    new_context[keys[0]] = k
                    new_context[keys[1]] = v
                    if key_len == 3:
                        new_context[keys[2]] = index
                        index += 1
                    self.__core(data, db_info, new_context, *context)
                    if self.__break:
                        self.__break = False
                        break
                    if self.__continue:
                        self.__continue = False
                        continue
            else:
                logger.debug("for无可遍历的数据")
        if type(items) in [list, tuple]:
            if len(items) > 0:
                index = 0
                for v in items:
                    logger.debug("将 {} 注入局部变量池，取名 {}".format(str(v), key))
                    if key_len == 1:
                        new_context[key] = v
                    elif key_len == 2:
                        new_context[keys[0]] = v
                        new_context[keys[1]] = index
                        index += 1
                    self.__core(data, db_info, new_context, *context)
                    if self.__break:
                        self.__break = False
                        break
                    if self.__continue:
                        self.__continue = False
                        continue
            else:
                logger.debug("for无可遍历的数据")

    def __while(self, data, db_info, *context: dict):
        """
        处理while
        :param data: 
        :return: 
        """
        # while需要增加一个执行次数，如果这个实际的执行次数超过了这个次数，将抛出异常
        ex = data.get("ex")
        db_info = db_info if data.get("db_info") is None else Express.calculate_str(self.__config, data.get("db_info"),
                                                                                    *context)
        if not Express.is_express(ex):
            raise MyException("while的标签格式有误，ex属性必须是被${{}}包围的表达式")
        if len(Express.get_express_list(ex)) > 1:
            raise MyException("while的标签格式有误，ex属性只能指定1个表达式")
        count = 10 if data.get("count") is None else int(data.get("count"))
        t = 0
        new_context = {}
        while t < count:
            r = Express.calculate_str(self.__config, ex, new_context, *context)
            if not r:
                logger.info("循环结束")
                logger.debug("ex表达式结果为 {}，循环结束".format(r))
                break
            logger.info("循环命中")
            logger.debug("ex表达式结果为 {}，循环继续".format(r))
            t += 1
            self.__core(data, db_info, new_context, *context)
            if self.__break:
                self.__break = False
                break
            if self.__continue:
                self.__continue = False
                continue
        else:
            raise MyException("while标签已经执行了指定的次数[{}],但还未返回需要的结果".format(count))

    def __raise(self, data, *context: dict):
        """
        处理抛出异常
        :param data:
        :param context:
        :return:
        """
        value = data.get("$value")
        msg = Express.calculate_str(self.__config, value, *context)
        raise XMLRuntimeException(msg)

    def __if(self, data, db_info, *context: dict):
        """
        处理if
        """
        # 取到ex，如果ex计算的值是一个假值，则不执行
        ex = data.get("ex")
        db_info = db_info if data.get("db_info") is None else Express.calculate_str(self.__config, data.get("db_info"),
                                                                                    *context)
        if not Express.is_express(ex):
            raise MyException("if的标签格式有误，ex属性必须是被${{}}包围的表达式")
        if len(Express.get_express_list(ex)) > 1:
            raise MyException("if的标签格式有误，ex属性只能指定1个表达式")
        r = Express.calculate_str(self.__config, ex, *context)
        if r:
            logger.info("判断为真，执行子标签")
            logger.debug("ex表达式结果为 {}，继续执行子标签".format(r))
            self.__core(data, db_info, *context)
        else:
            logger.info("判断为假，不执行子标签")
            logger.debug("ex表达式结果为 {}，不执行子标签".format(r))
        return r

    def __else(self, data, db_info, *context: dict):
        """
        处理if
        """
        # 取到ex，如果ex计算的值是一个假值，则不执行
        logger.info("所有分支未命中，执行else分支")
        db_info = db_info if data.get("db_info") is None else Express.calculate_str(self.__config, data.get("db_info"),
                                                                                    *context)
        self.__core(data, db_info, *context)

    def __inject_res_and_req(self, context: dict):
        # 注入变量
        context["__res_data__"] = self.__res.text
        context["__res_header__"] = self.__res.header
        context["__req_data__"] = self.__interface_info.body
        context["__req_header__"] = self.__interface_info.header
        context["__status__"] = self.__res.code

    def __work_for_post(self, data, *context: dict, ):
        # 执行之前，把四个变量的值注入进去
        self.__inject_res_and_req(context[0])
        logger.debug("标签开始执行,它的描述为 {}".format(data.desc))
        if data.type == "none" and data.value is not None:
            # 直接对value值进行操作
            self.__process_value(data, *context)
        elif data.type == "res_data":
            # 对结果进行后置处理
            self.__process_res_data(data, *context)
            logger.debug("标签将从 响应报文 取得数据")
        elif data.type == "sql":
            # 对sql进行后置处理
            self.__process_sql(data, *context)
            logger.debug("标签将从 数据库 取得数据")
        elif data.type == "req_data":
            # 对请求报文进行处理
            self.__process_req_data(data, *context)
            logger.debug("标签将从 请求报文 取得数据")
        elif data.type == "res_header":
            # 对响应头进行处理
            self.__process_res_header(data, *context)
            logger.debug("标签将从 响应头 取得数据")
        elif data.type == "req_header":
            # 对响应头进行处理
            self.__process_req_header(data, *context)
            logger.debug("标签将从 请求头 取得数据")
        elif data.type == "none":
            raise PostValueIsNotSpecifiedException()
        else:
            raise PostTypeIsIncorrectException(data.type)

    def __process_req_header(self, post: ProcessorData, *context: dict):
        """
        处理请求头
        """
        re_type = post.re_type
        key = Express.calculate_str(self.__config, post.key, *context)
        desc = post.desc
        res = self.__interface_info.header
        names = post.names
        act = post.act
        var_type = post.var_type
        expect = Express.calculate_str(self.__config, post.value, *context)
        source_value = post.value
        scope = post.scope
        if key == "$whole":
            res = None if res == "" else res
            self.__process(act, desc, res, expect, names, var_type, scope, *context)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            re_regex = Regex(post.key_regex, post.key_count).get_value(res)
            if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                raise PostNotFindValueException(post.type,
                                                "$regex[{}]:{}".format(post.key_regex, str(post.key_count)))
            if re_regex is Utils.ERROR and source_value is not None and act == "set":
                re_regex = expect
                logger.debug("标签从 请求头 提取数据失败，使用默认值 {}".format(expect))
            self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
        else:
            if re_type in ["key_value"]:
                re_json = JsonParse(res).get_value(key)
                if re_json is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if re_json is Utils.ERROR and source_value is not None and act == "set":
                    re_json = expect
                    logger.debug("标签从 请求头 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_json, expect, names, var_type, scope, *context)
            else:
                raise PostReTypeIsNotSupportedException(re_type)

    def __process_res_header(self, post: ProcessorData, *context: dict):
        """
        处理响应头
        """
        re_type = post.re_type
        key = Express.calculate_str(self.__config, post.key, *context)
        desc = post.desc
        res = self.__res.header
        names = post.names
        act = post.act
        var_type = post.var_type
        scope = post.scope
        expect = Express.calculate_str(self.__config, post.value, *context)
        source_value = post.value
        if key == "$whole":
            res = None if res == "" else res
            self.__process(act, desc, res, expect, names, var_type, scope, *context)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            re_regex = Regex(post.key_regex, post.key_count).get_value(res)
            if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                raise PostNotFindValueException(post.type,
                                                "$regex[{}]:{}".format(post.key_regex, str(post.key_count)))
            if re_regex is Utils.ERROR and source_value is not None and act == "set":
                re_regex = expect
                logger.debug("标签从 响应头 提取数据失败，使用默认值 {}".format(expect))
            self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
        else:
            if re_type in ["key_value"]:
                re_json = JsonParse(res).get_value(key)
                if re_json is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if re_json is Utils.ERROR and source_value is not None and act == "set":
                    re_json = expect
                    logger.debug("标签从 响应头 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_json, expect, names, var_type, scope, *context)
            else:
                raise PostReTypeIsNotSupportedException(re_type)

    def __process_req_data(self, post: ProcessorData, *context: dict):
        """
        处理请求报文
        :param post:
        :return:
        """
        re_type = self.__interface_info.body_type
        if re_type is None:
            raise PostReqDataIsNullException()
        key = Express.calculate_str(self.__config, post.key, *context)
        desc = post.desc
        res = self.__interface_info.body
        names = post.names
        act = post.act
        var_type = post.var_type
        expect = Express.calculate_str(self.__config, post.value, *context)
        source_value = post.value
        scope = post.scope
        if key == "$whole":
            res = None if res == "" else res
            self.__process(act, desc, res, expect, names, var_type, scope, *context)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            re_regex = Regex(post.key_regex, post.key_count).get_value(res)
            if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                raise PostNotFindValueException(post.type,
                                                "$regex[{}]:{}".format(post.key_regex, str(post.key_count)))
            if re_regex is Utils.ERROR and source_value is not None and act == "set":
                re_regex = expect
                logger.debug("标签从 请求报文 提取数据失败，使用默认值 {}".format(expect))
            self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
        else:
            if re_type in ["json", "key_value", "form_gb18030"]:
                re_json = JsonParse(res).get_value(key)
                if re_json is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if re_json is Utils.ERROR and source_value is not None and act == "set":
                    re_json = expect
                    logger.debug("标签从 请求报文 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_json, expect, names, var_type, scope, *context)
            elif re_type == "xml":
                re_xml = XmlParse(res).get_value(key)
                if re_xml is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if re_xml is Utils.ERROR and source_value is not None and act == "set":
                    re_xml = expect
                    logger.debug("标签从 请求报文 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_xml, expect, names, var_type, scope, *context)
            else:
                raise PostReTypeIsNotSupportedException(re_type)

    def __process_res_data(self, post: ProcessorData, *context: dict):
        """
        处理结果
        :param post:
        :return:
        """
        re_type = post.re_type
        key = Express.calculate_str(self.__config, post.key, *context)
        desc = post.desc
        res = self.__res.text
        names = post.names
        act = post.act
        var_type = post.var_type
        expect = Express.calculate_str(self.__config, post.value, *context)
        scope = post.scope
        source_value = post.value
        if key == "$whole":
            res = None if res == "" else res
            self.__process(act, desc, res, expect, names, var_type, scope, *context)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            re_regex = Regex(post.key_regex, post.key_count).get_value(res)
            if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                raise PostNotFindValueException(post.type,
                                                "$regex[{}]:{}".format(post.key_regex, str(post.key_count)))
            if re_regex is Utils.ERROR and source_value is not None and act == "set":
                re_regex = expect
                logger.debug("标签从 响应报文 提取数据失败，使用默认值 {}".format(expect))
            self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
        else:
            if re_type in ["json", "key_value"]:
                re_json = JsonParse(res).get_value(key)
                if re_json is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if re_json is Utils.ERROR and source_value is not None and act == "set":
                    re_json = expect
                    logger.debug("标签从 响应报文 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_json, expect, names, var_type, scope, *context)
            elif re_type == "xml":
                xml_res = XmlParse(res).get_value(key)
                if xml_res is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if xml_res is Utils.ERROR and source_value is not None and act == "set":
                    xml_res = expect
                    logger.debug("标签从 响应报文 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, xml_res, expect, names, var_type, scope, *context)
            else:
                raise PostReTypeIsNotSupportedException(re_type)

    def __process_sql(self, post: ProcessorData, *context: dict):
        """
        处理sql
        :param post:
        :return:
        """
        # 处理sql执行结果
        re_type = post.re_type
        key = Express.calculate_str(self.__config, post.key, *context)
        desc = post.desc
        sql = Express.calculate_str(self.__config, post.sql, *context)
        scope = post.scope
        # 取得db_info
        db_info = post.db_info
        if db_info is None:
            if self.__config.have_var("db_info"):
                db_info = self.__config.get_var("db_info")
            else:
                raise DBInformationIsNotConfiguredException(self.__config)
        if not DB.is_the_db_info_correct(db_info):
            raise DBInformationIsIncorrectException(db_info)
        # 执行sql
        res = DB(db_info, self.__config).execute(sql)
        logger.debug("标签执行了sql语句 {}".format(sql))
        logger.debug("其结果为 {}".format(res.res))
        names = post.names
        act = post.act
        var_type = post.var_type
        expect = Express.calculate_str(self.__config, post.value, *context)
        source_value = post.value
        if re_type == "table":
            if key == "$whole":
                res = None if res.res == "" else TableParse(res.res).get_value(key)
                self.__process(act, desc, res, expect, names, var_type, scope, *context)
            elif key == "$regex":
                re_regex = Regex(post.key_regex, post.key_count).get_value(res.res)
                if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type,
                                                    "$regex[{}]:{}".format(post.key_regex, str(post.key_count)))
                if re_regex is Utils.ERROR and source_value is not None and act == "set":
                    re_regex = expect
                    logger.debug("标签从 数据库 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
            else:
                # 如果是其他key
                real = TableParse(res.res).get_value(key)
                if real is Utils.ERROR and (source_value is None or act != "set"):
                    raise PostNotFindValueException(post.type, key)
                if real is Utils.ERROR and source_value is not None and act == "set":
                    real = expect
                    logger.debug("标签从 数据库 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, real, expect, names, var_type, scope, *context)
        elif re_type == "number":
            if key == "$rows":
                self.__process(act, desc, res.rows, expect, names, var_type, scope, *context)
            elif key == "$columns":
                self.__process(act, desc, res.columns, expect, names, var_type, scope, *context)
            else:
                self.__process(act, desc, res.res, expect, names, var_type, scope, *context)
        else:
            raise PostReTypeIsNotSupportedException(re_type)

    def __process_value(self, post: ProcessorData, *context: dict):
        """
        直接对value值进行处理
        :param post:
        :return:
        """
        value = Express.calculate_str(self.__config, post.value, *context)
        scope = post.scope
        self.__process(post.act, post.desc, value, None, post.names, post.var_type, scope, *context)

    def __process(self, act, desc, value, expect, names, var_type, scope, *context: dict):
        """
        处理
        :param act:
        :param names:
        :param var_type:
        :param value:
        :param desc:
        :return:
        """
        # logger.print_log("标签最终取得的数据是 {} ，类型是 {}".format(value, type(value)))
        if act == "set":
            self.__process_set(names, value, var_type, scope, *context)
        elif act == "print":
            self.__process_print(value, desc, var_type)
        elif act == "equal":
            self.__process_equal(value, expect)
        elif act == "match":
            self.__process_match(value, expect)
        elif act == "sleep":
            self.__process_sleep(value)
        elif act == "replace_body":
            # 将响应体替换为指定值
            self.__process_replace_body(value)
        elif act == "execute":
            # 执行表达式
            pass
        elif act == "logger":
            # 日志记录
            logger.debug(value)
        else:
            raise PostActIsIncorrectException(act)

    def __process_replace_body(self, value):
        """
        将响应体替换为指定的value
        :return:
        """
        logger.debug("标签执行成功，将把响应报文替换为 {}".format(str(value)))
        self.__res.text = str(value)

    @staticmethod
    def __process_sleep(value):
        """
        睡眠的value值必须是一个可以转为数字的字符串
        :param value:
        :return:
        """
        wait = str(value)
        try:
            wait = int(wait)
        except Exception:
            raise PostSleepValueIsNotNumberException(str(value))
        logger.debug("标签执行成功，将睡眠 {} 秒".format(wait))
        time.sleep(wait)

    @staticmethod
    def __process_set(names, value, var_type, scope, *context: dict):
        """
        set类型的后置处理器
        :return:
        """
        if len(names) > 1:
            if type(value) not in [list, tuple]:
                raise PostValueTypeIsNotCorrectException(value, type(value))
            if len(names) != len(value):
                raise PostValueLengthIsNotCorrectException(len(names), len(value))
            for i in range(len(names)):
                _value = PostProcessor.__get_specified_type_var(value[i], var_type)
                if scope == "global":
                    for _context in context:
                        _context[names[i]] = _value
                    logger.debug("标签存储了变量 {} 到变量池，其值为 {}".format(names[i], value[i]))
                else:
                    context[0][names[i]] = _value
                    logger.debug("标签存储了变量 {} 到当前变量池，其值为 {}".format(names[i], value[i]))
        else:
            _value = PostProcessor.__get_specified_type_var(value, var_type)
            if scope == "global":
                for _context in context:
                    _context[names[0]] = _value
                logger.debug("标签存储了变量 {} 到变量池，其值为 {}".format(names[0], value))
            else:
                context[0][names[0]] = _value
                logger.debug("标签存储了变量 {} 到局部变量池，其值为 {}".format(names[0], value))

    @staticmethod
    def __process_print(value, desc, var_type):
        """
        打印类型的后置处理器
        :return:
        """
        if not value:
            logger.info(FormatOutput.format_post_info(desc, value))
        else:
            logger.info(FormatOutput.format_post_info(desc, PostProcessor.__get_specified_type_var(value, var_type)))
        logger.debug("标签执行了打印")

    @staticmethod
    def __get_specified_type_var(var, var_type):
        """
        取到指定类型的变量
        :param var:
        :param var_type:
        :return:
        """
        # 如果var_type等于auto，则先自动推测返回类型
        if var_type == "auto":
            if ParamType.is_int(var):
                var_type = "int"
            elif ParamType.is_float(var):
                var_type = "float"
            elif ParamType.is_bool(var):
                var_type = "bool"
            else:
                var_type = "str"
        if var_type == "str":
            return str(var)
        elif var_type == "int":
            if not ParamType.is_int(str(var)):
                raise PostTransferFailException(str(var), "int")
            return ParamType.to_int(var)
        elif var_type == "float":
            if not ParamType.is_float(str(var)) and not ParamType.is_int(str(var)):
                raise PostTransferFailException(str(var), "float")
            return ParamType.to_float(var)
        elif var_type == "bool":
            value = str(var)
            if not ParamType.is_bool(str(value)):
                raise PostTransferFailException(str(var), "bool")
            return ParamType.to_bool(value)
        else:
            return var

    def __process_equal(self, real, expect):
        """
        处理真值和期望值等于的情况
        :param real:
        :param expect:
        :return:
        """
        type_of_expect = type(expect)
        type_of_real = type(real)
        if (type_of_expect == type_of_real) or (type_of_expect != type_of_real and type_of_expect != str):
            result = expect == real
        elif type_of_expect != type_of_real and type_of_real in [dict, list, tuple] and type_of_expect == str:
            expect = self.__space_re_o.sub("", str(expect))
            real = self.__space_re_o.sub("", str(real))
            result = expect == real
        else:
            result = str(expect) == str(real)
        if not result:
            raise PostValueAndExceptValueIsNotSameException(real, expect)

    @staticmethod
    def __process_match(real, expect):
        """
        使用正则进行等于判断
        :param expect: 正则
        :param real: 真实值
        :return:
        """
        res = re.match(expect, str(real))
        if res is None:
            raise PostValueAndExceptValueIsNotMatchedException(real, expect)

    def __work_for_assert(self, ass: AssertData, *context: dict):
        self.__inject_res_and_req(context[0])
        logger.debug("断言标签开始执行，它的描述为 {}".format(ass.desc))
        if ass.type == "res_data":
            # 与结果进行比较
            logger.debug("标签将从 响应结果 中提取数据进行断言")
            self.__assert_re(ass, *context)
        elif ass.type == "sql":
            # 与sql执行结果进行比较
            logger.debug("标签将从 数据库 中提取数据进行断言")
            self.__assert_sql(ass, *context)
        elif ass.type == "status":
            # 与响应状态进行比较
            logger.debug("标签将从 响应状态 中提取数据进行断言")
            self.__assert_status(ass, *context)
        elif ass.type == "expression":
            # 与表达式进行比较，表达式位于ass.value
            logger.debug("标签将与 表达式 进行断言")
            self.__assert_expression(ass, *context)
        elif ass.type == "res_header":
            logger.debug("标签将从 响应头 中提取数据进行断言")
            self.__assert_res_header(ass, *context)
        else:
            raise ExpectTypeIsUnsupportedException(ass.type)
        logger.debug("断言执行结束")

    def __assert_expression(self, ass: AssertData, *context: dict):
        """
        断言表达式
        :param ass:
        :return:
        """
        res = Express.calculate_str(self.__config, ass.value, *context)
        expect_value = Express.calculate_str(self.__config, ass.expect_value, *context)
        desc = ass.desc
        act = ass.act
        self.__assert(act, expect_value, res, desc, ass.type, ass.var_type)

    def __assert_sql(self, ass: AssertData, *context: dict):
        """
        断言sql执行结果
        :param ass:
        :return:
        """
        re_type = ass.re_type
        sql = Express.calculate_str(self.__config, ass.sql, *context)
        # 取得db_info
        db_info = ass.db_info
        if db_info is None:
            if self.__config.have_var("db_info"):
                db_info = self.__config.get_var("db_info")
            else:
                raise DBInformationIsNotConfiguredException(self.__config)
        if not DB.is_the_db_info_correct(db_info):
            raise DBInformationIsIncorrectException(db_info)
        # 执行sql
        res = DB(db_info, self.__config).execute(sql)
        logger.debug("标签执行了sql语句 {}".format(sql))
        logger.debug("其结果为 {}".format(res.res))
        key = Express.calculate_str(self.__config, ass.key, *context)
        value = Express.calculate_str(self.__config, ass.expect_value, *context)
        desc = ass.desc
        act = ass.act
        if re_type == "table":
            # 返回的是table
            if key == "$whole":
                # 对整个结果进行比较
                self.__assert(act, value, TableParse(res.res).get_value(key), desc, ass.type, ass.var_type, sql)
            elif key == "$regex":
                # 如果使用正则时，则提取后再进行比较
                real = Regex(ass.key_regex, ass.key_count).get_value(res.res)
                if real is Utils.ERROR:
                    self.__throw_assert(False, None, value,
                                        "sql执行结果中不存在此第{}个匹配：{}".format(ass.key_count, ass.key_regex),
                                        ass.type, sql, desc, "\n注明：该SQL执行结果为：{}".format(res.res))
                else:
                    self.__assert(act, value, real, desc, ass.type, ass.var_type, sql)
            else:
                # 如果是其他key
                real = TableParse(res.res).get_value(key)
                if real is Utils.ERROR:
                    self.__throw_assert(False, None, value, "sql执行结果中不存在此切片指定的值：{}".format(key), ass.type, sql, desc,
                                        "\n注明：该SQL执行结果为：{}".format(res.res))
                else:
                    self.__assert(act, value, real, desc, ass.type, ass.var_type, sql)
        elif re_type == "number":
            # 返回的是number
            if key == "$rows":
                self.__assert(act, value, res.rows, desc, ass.type, ass.var_type, sql)
            elif key == "$columns":
                self.__assert(act, value, res.columns, desc, ass.type, ass.var_type, sql)
            else:
                self.__assert(act, value, res.res, desc, ass.type, ass.var_type, sql)
        else:
            raise ExpectReTypeUnsupportedException(ass.re_type)

    def __assert_res_header(self, ass: AssertData, *context: dict):
        """
        断言响应头
        :param ass:断言抽象数据
        :return:
        """
        re_type = ass.re_type
        res = self.__res.header
        key = Express.calculate_str(self.__config, ass.key, *context)
        value = Express.calculate_str(self.__config, ass.expect_value, *context)
        desc = ass.desc
        act = ass.act
        # 取出结果数据
        if key == "$whole":
            # 如果是整个断言
            self.__assert(act, value, res, desc, ass.type, ass.var_type)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            real = Regex(ass.key_regex, ass.key_count).get_value(res)
            if real is Utils.ERROR:
                self.__throw_assert(False, None, value, "响应头中不存在此第{}个匹配：{}".format(ass.key_count, ass.key_regex),
                                    ass.type, None, desc)
            else:
                self.__assert(act, value, real, desc, ass.type, ass.var_type)
        else:
            if re_type == "key_value":
                # 如果结果类型为key_value
                real_res = JsonParse(res).get_value(key)
                if real_res is Utils.ERROR:
                    self.__throw_assert(False, None, value, "响应头中不存在期望的键或键格式错误：{}".format(key), ass.type, None, desc)
                else:
                    self.__assert(act, value, real_res, desc, ass.type, ass.var_type)
            else:
                raise ExpectReTypeUnsupportedException(ass.re_type)

    def __assert_re(self, ass: AssertData, *context: dict):
        """
        断言结果
        :param ass:断言抽象数据
        :return:
        """
        re_type = ass.re_type
        res = self.__res.text
        key = Express.calculate_str(self.__config, ass.key, *context)
        value = Express.calculate_str(self.__config, ass.expect_value, *context)
        desc = ass.desc
        act = ass.act
        # 取出结果数据
        if key == "$whole":
            # 如果是整个断言
            self.__assert(act, value, res, desc, ass.type, ass.var_type)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            real = Regex(ass.key_regex, ass.key_count).get_value(res)
            if real is Utils.ERROR:
                self.__throw_assert(False, None, value, "响应报文中不存在此第{}个匹配：{}".format(ass.key_count, ass.key_regex),
                                    ass.type, None, desc)
            else:
                self.__assert(act, value, real, desc, ass.type, ass.var_type)
        else:
            if re_type == "json" or re_type == "key_value":
                # 如果结果类型为json
                if not JsonParse.is_correct_json(res):
                    raise ExpectJsonException(str(res))
                real_res = JsonParse(res).get_value(key)
                if real_res is Utils.ERROR:
                    self.__throw_assert(False, None, value, "响应报文中不存在期望的键或键格式错误：{}".format(key), ass.type, None, desc)
                else:
                    self.__assert(act, value, real_res, desc, ass.type, ass.var_type)
            elif re_type == "table":
                # 如果结果类型是table，一般情况下接口的响应报文不存在table型数据，暂不处理
                table_res = TableParse(res).get_value(key)
                if table_res is Utils.ERROR:
                    self.__throw_assert(False, None, value, "响应报文中中不存在此切片指定的值：{}".format(key), ass.type, None, desc)
                else:
                    self.__assert(act, value, table_res, desc, ass.type, ass.var_type)
            elif re_type == "number":
                # 返回的数据如果是number，即数字，在此处理
                raise ExpectReTypeUnsupportedException(ass.re_type)
            elif re_type == "xml":
                xml_res = XmlParse(res).get_value(key)
                if xml_res is Utils.ERROR:
                    self.__throw_assert(False, None, value, "响应报文中不存在期望的节点或键格式错误：{}".format(key), ass.type, None, desc)
                else:
                    self.__assert(act, value, xml_res, desc, ass.type, ass.var_type)
            else:
                raise ExpectReTypeUnsupportedException(ass.re_type)

    def __assert_status(self, ass: AssertData, *context: dict):
        """
        断言响应状态
        """
        re_type = ass.re_type
        res = self.__res.code
        key = Express.calculate_str(self.__config, ass.key, *context)
        value = Express.calculate_str(self.__config, ass.expect_value, *context)
        desc = ass.desc
        act = ass.act
        # 取出结果数据
        if key == "$whole":
            # 如果是整个断言
            self.__assert(act, value, res, desc, ass.type, ass.var_type)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            real = Regex(ass.key_regex, ass.key_count).get_value(res)
            if real is Utils.ERROR:
                self.__throw_assert(False, None, value, "响应状态中不存在第{}个匹配：{}".format(ass.key_count, ass.key_regex),
                                    ass.type,
                                    None, desc)
            else:
                self.__assert(act, value, real, desc, ass.type, ass.var_type)
        else:
            if re_type == "number":
                # 返回的数据如果是number，即数字，在此处理
                self.__assert(act, value, res, desc, ass.type, ass.var_type)
                pass
            else:
                raise ExpectReTypeUnsupportedException(ass.re_type)

    def __assert(self, act, expect, real, desc, type_, var_type, sql=None):
        """
        断言，根据不同的动作调用不同的断言器
        :param act:断言的动作
        :param expect:期望值
        :param real:实际值
        :param desc:断言器描述
        :param type_:断言器的类型
        :param sql:如果是sql断言，执行的sql语句
        :return:
        """
        expect = expect
        real = PostProcessor.__get_specified_type_var(real, var_type)
        logger.debug("断言的实际值是 {}".format(real))
        logger.debug("断言的期望值是 {}".format(expect))
        if act == "match":
            # 调用正则匹配
            logger.debug("将断言实际值是否与期望值说明的正则表达式是否匹配")
            self.__assert_match(expect, real, desc, type_, sql)
        elif act == "include":
            logger.debug("将断言实际值是否 包含 期望值")
            self.__assert_include(expect, real, desc, type_, sql)
        elif act == "not include":
            logger.debug("将断言实际值是否 不包含 期望值")
            self.__assert_not_include(expect, real, desc, type_, sql)
        elif act == "equal":
            # 调用相等
            logger.debug("将断言实际值是否 等于 期望值")
            self.__assert_equal(expect, real, desc, type_, sql)
        elif act == "not equal":
            # 调用相等
            logger.debug("将断言实际值是否 不等于 期望值")
            PostProcessor.__assert_not_equal(expect, real, desc, type_, sql)
        elif act == "in":
            logger.debug("将断言实际值是否 存在于 期望值中")
            self.__assert_in(expect, real, desc, type_, sql)
        elif act == "not in":
            logger.debug("将断言实际值是否 不存在于 期望值中")
            self.__assert_not_in(expect, real, desc, type_, sql)
        elif act == "greater":
            logger.debug("将断言实际值是否 大于 期望值")
            self.__assert_greater(expect, real, desc, type_, sql)
        elif act == "greater or equal":
            logger.debug("将断言实际值是否 大于等于 期望值")
            self.__assert_greater_or_equal(expect, real, desc, type_, sql)
        elif act == "less":
            logger.debug("将断言实际值是否 小于 期望值")
            self.__assert_less(expect, real, desc, type_, sql)
        elif act == "less or equal":
            logger.debug("将断言实际值是否 小于等于 期望值")
            self.__assert_less_or_equal(expect, real, desc, type_, sql)
        elif act == "content equal":
            logger.debug("将断言实际值内容是否 与 期望值内容相同")
            self.__assert_content_equal(expect, real, desc, type_, sql)
        elif act == "content not equal":
            logger.debug("将断言实际值内容是否 与 期望值内容不相同")
            self.__assert_content_not_equal(expect, real, desc, type_, sql)
        else:
            raise ExpectActIsUnsupportedException(act)

    def __assert_include(self, expect, real, desc, type_, sql=None):
        """
        判断实际值包含期望值
        :param expect: 期望
        :param real: 实际
        :param desc: 断言器描述
        :param type_:断言起类型
        :param sql:断言器执行的sql
        :return:
        """
        type_of_real = type(real)
        if type_of_real in [tuple, list, dict]:
            # 如果实际值是元组列表字典，则直接遍历每一项与期望值进行比较，如果存在一个匹配的则表示存在
            assert_re = False
            for t in real:
                if PostProcessor.__does_a_equal_b(expect, t):
                    assert_re = True
                    break
        else:
            t_expect = str(expect)
            t_real = str(real)
            assert_re = t_expect in t_real
        expect = "实际值包含 {}".format(expect)
        # 断言响应状态成功，描述：查询一个转入方数据，响应码正确
        self.__throw_assert(assert_re, real, expect, "实际值未包含期望值!", type_, sql, desc)

    def __assert_not_include(self, expect, real, desc, type_, sql=None):
        """
        判断实际值不包含期望值
        :param expect: 期望
        :param real: 实际
        :param desc: 断言器描述
        :param type_:断言起类型
        :param sql:断言器执行的sql
        :return:
        """
        type_of_real = type(real)
        if type_of_real in [tuple, list, dict]:
            # 如果实际值是元组列表字典，则直接遍历每一项与期望值进行比较，如果每一项都不相等，则表明不包含
            assert_re = True
            for t in real:
                if PostProcessor.__does_a_equal_b(expect, t):
                    assert_re = False
                    break
        else:
            t_expect = str(expect)
            t_real = str(real)
            assert_re = t_expect not in t_real
        expect = "实际值不包含 {}".format(expect)
        # 断言响应状态成功，描述：查询一个转入方数据，响应码正确
        self.__throw_assert(assert_re, real, expect, "实际值包含了期望值!", type_, sql, desc)

    def __assert_in(self, expect, real, desc, type_, sql=None):
        """
        判断实际值存在于期望值
        :param expect: 期望
        :param real: 实际
        :param desc: 断言器描述
        :param type_:断言起类型
        :param sql:断言器执行的sql
        :return:
        """
        type_of_expect = type(expect)
        type_of_real = type(real)
        if type_of_expect in [tuple, list, dict]:
            # 如果期望值是元组列表字典，则直接遍历每一项与实际值进行比较，如果存在一个匹配的则表示存在
            assert_re = False
            for t in expect:
                if PostProcessor.__does_a_equal_b(real, t):
                    assert_re = True
                    break
        elif type_of_expect is str and type_of_real in [tuple, list, dict]:
            t_expect = PostProcessor.__space_re_o.sub("", str(expect))
            t_real = PostProcessor.__space_re_o.sub("", str(real))
            assert_re = t_real in t_expect
        else:
            t_expect = str(expect)
            t_real = str(real)
            assert_re = t_real in t_expect
        expect = "实际值存在于 {} 中".format(expect)
        # 断言响应状态成功，描述：查询一个转入方数据，响应码正确
        self.__throw_assert(assert_re, real, expect, "实际值未存在于期望值中!", type_, sql, desc)

    def __assert_not_in(self, expect, real, desc, type_, sql=None):
        """
        判断实际值不存在于期望值
        :param expect: 期望
        :param real: 实际
        :param desc: 断言器描述
        :param type_:断言起类型
        :param sql:断言器执行的sql
        :return:
        """
        type_of_expect = type(expect)
        type_of_real = type(real)
        if type_of_expect in [tuple, list, dict]:
            # 如果期望值是元组列表字典，则直接遍历每一项与实际值进行比较，如果一个都不匹配的则表示不存在
            assert_re = True
            for t in expect:
                if PostProcessor.__does_a_equal_b(real, t):
                    assert_re = False
                    break
        elif type_of_expect is str and type_of_real in [tuple, list, dict]:
            t_expect = PostProcessor.__space_re_o.sub("", str(expect))
            t_real = PostProcessor.__space_re_o.sub("", str(real))
            assert_re = t_real not in t_expect
        else:
            t_expect = str(expect)
            t_real = str(real)
            assert_re = t_real not in t_expect
        expect = "实际值不存在于 {} 中".format(expect)
        # 断言响应状态成功，描述：查询一个转入方数据，响应码正确
        self.__throw_assert(assert_re, real, expect, "实际值已存在于期望值中!", type_, sql, desc)

    def __assert_equal(self, expect, real, desc, type_, sql=None):
        """
        判断实际值是否等于期望
        :param expect: 期望
        :param real: 实际
        :param desc: 断言器描述
        :return:
        """
        assert_re = PostProcessor.__does_a_equal_b(expect, real)
        expect = "实际值等于 {}".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值与期望值不等!", type_, sql, desc)

    def __assert_content_equal(self, expect, real, desc, type_, sql=None):
        # 判断内容是否相等，主要是用于list、tuple、set的内部元素比较，如果传入其它数据类型，将调用__assert_equal方法
        if isinstance(expect, (list, tuple, set)) and isinstance(real, (list, tuple, set)):
            assert_re = PostProcessor.__is_the_content_of_a_equal_to_that_of_b(expect, real)
            expect = "实际值内容等于 {}".format(expect)
            self.__throw_assert(assert_re, real, expect, "实际值的内容与期望值的内容不等!", type_, sql, desc)
        else:
            self.__assert_equal(expect, real, desc, type_, sql)

    def __assert_content_not_equal(self, expect, real, desc, type_, sql=None):
        # 判断内容是否不相等，主要是用于list、tuple、set的内部元素比较，如果传入其它数据类型，将调用__assert_not_equal方法
        if isinstance(expect, (list, tuple, set)) and isinstance(real, (list, tuple, set)):
            assert_re = not PostProcessor.__is_the_content_of_a_equal_to_that_of_b(expect, real)
            expect = "实际值内容不等于 {}".format(expect)
            self.__throw_assert(assert_re, real, expect, "实际值的内容与期望值的内容相等!", type_, sql, desc)
        else:
            self.__assert_not_equal(expect, real, desc, type_, sql)

    def __assert_not_equal(self, expect, real, desc, type_, sql=None):
        """
        判断实际值是否等于期望
        :param expect: 期望
        :param real: 实际
        :param desc: 断言器描述
        :return:
        """
        assert_re = not PostProcessor.__does_a_equal_b(expect, real)
        expect = "实际值不等于 {}".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值与期望值相等!", type_, sql, desc)

    def __assert_greater(self, expect, real, desc, type_, sql=None):
        """
        断言大于
        :param expect:
        :param real:
        :param desc:
        :param type_:
        :param sql:
        :return:
        """
        real = PostProcessor.__get_specified_type_var(real, "auto")
        expect = PostProcessor.__get_specified_type_var(expect, "auto")
        type_of_a = type(expect)
        type_of_b = type(real)
        if type_of_a not in [int, float] or type_of_b not in [int, float]:
            raise MyException("断言大于仅能比对数字，不能比对 {} 和 {}".format(type_of_a, type_of_b))
        assert_re = real > expect
        expect = "实际值大于 {}".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值未大于期望值!", type_, sql, desc)

    def __assert_greater_or_equal(self, expect, real, desc, type_, sql=None):
        """
        断言大于等于
        :param expect:
        :param real:
        :param desc:
        :param type_:
        :param sql:
        :return:
        """
        real = PostProcessor.__get_specified_type_var(real, "auto")
        expect = PostProcessor.__get_specified_type_var(expect, "auto")
        type_of_a = type(expect)
        type_of_b = type(real)
        if type_of_a not in [int, float] or type_of_b not in [int, float]:
            raise MyException("断言大于等于仅能比对数字，不能比对 {} 和 {}".format(type_of_a, type_of_b))
        assert_re = real >= expect
        expect = "实际值大于等于 {}".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值未大于等于期望值!", type_, sql, desc)

    def __assert_less(self, expect, real, desc, type_, sql=None):
        """
        断言小于
        :param expect:
        :param real:
        :param desc:
        :param type_:
        :param sql:
        :return:
        """
        real = PostProcessor.__get_specified_type_var(real, "auto")
        expect = PostProcessor.__get_specified_type_var(expect, "auto")
        type_of_a = type(expect)
        type_of_b = type(real)
        if type_of_a not in [int, float] or type_of_b not in [int, float]:
            raise MyException("断言小于仅能比对数字，不能比对 {} 和 {}".format(type_of_a, type_of_b))
        assert_re = real < expect
        expect = "实际值小于 {}".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值未小于期望值!", type_, sql, desc)

    def __assert_less_or_equal(self, expect, real, desc, type_, sql=None):
        """
        断言小于等于
        :param expect:
        :param real:
        :param desc:
        :param type_:
        :param sql:
        :return:
        """
        real = PostProcessor.__get_specified_type_var(real, "auto")
        expect = PostProcessor.__get_specified_type_var(expect, "auto")
        type_of_a = type(expect)
        type_of_b = type(real)
        if type_of_a not in [int, float] or type_of_b not in [int, float]:
            raise MyException("断言小于等于仅能比对数字，不能比对 {} 和 {}".format(type_of_a, type_of_b))
        assert_re = real <= expect
        expect = "实际值小于等于 {}".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值未小于等于期望值!", type_, sql, desc)

    @staticmethod
    def __does_a_equal_b(a, b):
        """
        判断a是否等于b
        :param a: 期望
        :param b: 断言器描述
        :return:
        """
        type_of_a = type(a)
        type_of_b = type(b)
        if type_of_a == type_of_b:
            return a == b
        if type_of_a != type_of_b:
            if type_of_a != str and type_of_b != str:
                return a == b
            elif type_of_b in [dict, list, tuple] and type_of_a == str:
                t_expect = PostProcessor.__space_re_o.sub("", str(a))
                t_real = PostProcessor.__space_re_o.sub("", str(b))
                return t_expect == t_real
            elif type_of_a in [dict, list, tuple] and type_of_b == str:
                t_expect = PostProcessor.__space_re_o.sub("", str(a))
                t_real = PostProcessor.__space_re_o.sub("", str(b))
                return t_expect == t_real
        return str(a) == str(b)

    @staticmethod
    def __is_the_content_of_a_equal_to_that_of_b(a, b):
        """
        判断a和b的内容是否相等，a和b必须是list、tuple、set
        """
        if len(a) != len(b):
            return False
        for i in a:
            if i not in b:
                return False
        for i in b:
            if i not in a:
                return False
        return True

    def __assert_match(self, expect, real, desc, type_, sql=None):
        """
        使用正则进行断言
        :param expect: 正则期望
        :param real: 真实值
        :param desc: 断言器描述
        :return:
        """
        assert_re = re.match(expect, str(real)) is not None
        expect = "实际值匹配正则表达式 {} ".format(expect)
        self.__throw_assert(assert_re, real, expect, "实际值与期望不匹配!", type_, sql, desc)

    def __throw_assert(self, assert_re, real, expect, reason, type_, sql, desc, error=None):
        """
        抛出断言错误
        :param assert_re: 断言的结果
        :param real: 实际值
        :param expect: 期望值
        :param reason: 原因
        :param type_: 断言起类型
        :param sql: 断言起执行的sql语句
        :param desc: 断言器描述
        :param error: 主动说明的错误
        :return:
        """
        if len(str(real)) > self.__length_for_expect:
            real = str(real)[:self.__length_for_expect] + "..."
        if len(str(expect)) > self.__length_for_expect:
            expect = str(expect)[:self.__length_for_expect] + "..."
        if type_ == "res_data":
            type_ = "响应数据"
        elif type_ == "status":
            type_ = "响应状态"
        elif type_ == "sql":
            type_ = "数据库表"
        elif type_ == "expression":
            type_ = "自定义表达式"
        elif type_ == "res_header":
            type_ = "响应头"
        else:
            raise ExpectTypeIsUnsupportedException(type_)
        if assert_re:
            logger.debug("断言成功")
            logger.info("    断言[{}]成功，描述：{}".format(type_, desc))
        else:
            logger.debug("断言失败")
            logger.info("    断言[{}]失败，描述：{}".format(type_, desc))
            if sql is not None:
                if real is None:
                    msg = "断言[{}]失败，描述：{}\nSQL：{}\n失败原因：{}".format(type_, desc, sql, reason)
                else:
                    msg = "断言[{}]失败，描述：{}\nSQL：{}\n失败原因：{}\n\n--期望{}\n--实际值：{}".format(type_, desc, sql, reason, expect,
                                                                                       real)
            else:
                if real is None:
                    msg = "断言[{}]失败，描述：{}\n失败原因：{}".format(type_, desc, reason)
                else:
                    msg = "断言[{}]失败，描述：{}\n失败原因：{}\n\n--期望{}\n--实际值：{}".format(type_, desc, reason, expect, real)
            MyAssertionError.raise_error(msg if error is None else "{}{}".format(msg, error))
