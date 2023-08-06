# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: pre processor
"""
import logging
import re
import time

from ...exception.db import *
from ...exception.inf_process import *
from ...exception.other import *
from ...exception.pre import *
from ...function.cfg.config import ConfigLoader
from ...function.data.interface import Interface
from ...function.database.db import DB
from ...function.express.express import Express, ParamType
from ...function.format.format import FormatOutput
from ...function.parse.files_parse import Files
from ...function.parse.json_parse import JsonParse
from ...function.parse.regex_parse import Regex
from ...function.parse.table_parse import TableParse
from ...function.parse.well_parse import WellParse
from ...function.parse.xml_parse import XmlParse
from ...function.utils.utils import Utils

logger = logging.getLogger(__name__)


class ProcessorData(object):
    """
    前置处理器单条数据
    """
    __name_re = re.compile(r"[\w_][\w_\d]*")

    def __init__(self, db_info: str, type_p: str, key: str, act: str, name: str, var_type: str, value: str,
                 re_type: str, desc: str, value_: str, scope: str, req_type: str):
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
        :return:
        """
        # 取到正确的desc参数
        self.desc = self.__get_correct_desc(desc)
        # 取到正确scope参数
        self.scope = self.__get_correct_scope(scope)
        # 取到正确的type参数
        self.type = self.__get_correct_type(type_p)
        # 取到正确的db_info，如果type is sql
        self.db_info = self.__get_correct_db_info(db_info)
        # 取到正确的动作
        self.act = self.__get_correct_act(act)
        # 取到正确的names
        self.names, self.var_type = self.__get_correct_names_and_var_type(name, var_type, key, self.act)
        # 取到正确的value
        self.value = self.__get_correct_value(value, self.act)
        # 取到正确的sql
        self.sql = self.__get_correct_sql(value_, self.type)
        # 取到正确的re_type
        self.re_type = self.__get_correct_re_type(re_type, self.type, self.sql, req_type, key)
        # key使用的正则表达式
        # 取第几个值
        # 取到正确的key
        self.key, self.key_regex, self.key_count = self.__get_correct_key(key, self.re_type)

    @staticmethod
    def __get_correct_type(type_p):
        """
        默认发为res_data
        取到正确的前置处理器的类型
        res_data:代表从结果中取值
        sql：代表执行sql，从sql的结果中取值
        :param type_p:
        :return:
        """
        if type_p is None:
            return "none"
        if type_p:
            type_p = type_p.lower()
        if type_p in ["sql", "req_data", "req_header", "none"]:
            return type_p
        else:
            raise PreTypeIsIncorrectException(type_p)

    @staticmethod
    def __get_correct_desc(desc):
        """
        获得正确的描述，描述不能为空
        :param desc:
        :return:
        """
        if not desc:
            raise PreDescIsNullException()
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
            raise PreKeyTypeIsIncorrectException(key)
        return key, key_regex, key_count

    @staticmethod
    def __get_correct_re_type(re_type, type_a, sql, req_type, key):
        """
        取到正确的re_type，默认为json
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
            elif type_a == "req_header":
                return "key_value"
            elif type_a == "req_data":
                return req_type
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
            raise PreActIsIncorrectException("空")
        if act:
            act = act.lower()
        if act in ["equal", "set", "match", "print", "sleep", "execute", "logger"]:
            return act
        else:
            raise PreActIsIncorrectException(act)

    @staticmethod
    def __get_correct_names_and_var_type(name, var_type, key, act):
        """
        取到正确的name和类型
        :param name:
        :return:
        """
        names = []
        if var_type not in ["str", "int", "float", "bool", "auto", None]:
            raise PreVarTypeIsNotSupportException(var_type)
        if name is None and act == "set":
            # 判断key是否包含特殊字符
            if key is None:
                raise PreNameIsNullException()
            else:
                if ProcessorData.__name_re.fullmatch(key):
                    names.append(key)
                else:
                    raise PreNameIsNullException()
        if name:
            if "," in name:
                names = name.split(",")
                names = list(map(lambda x: x.strip(), names))
            else:
                names = [name.strip()]
            for n in names:
                if not ProcessorData.__name_re.fullmatch(n):
                    raise PreNameIsNotSupportedException(n)
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
                raise PreValueIsNotSpecifiedException()
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
            raise PreSqlIsNotSpecifiedException()
        if value_:
            # sql语句存在时检查sql语句
            DB.check_sql(value_)
        if value_ is None:
            return None
        return value_

    @staticmethod
    def __get_correct_scope(scope):
        if scope is None:
            return None
        if scope not in ["local", "global"]:
            raise PreScopeIsIncorrectException()
        return scope

    @staticmethod
    def __get_correct_db_info(db_info):
        """
        取到正确的db_info对象，如果type is sql
        :param db_info:
        :return:
        """
        return db_info


class InfoData(object):
    """
    单条参数
    """
    __express_re = re.compile(r"\${(.*?)}")

    def __init__(self, source: dict, scope: str, name, value, act):
        """

        :param scope:
        :param name:
        :param value:
        """
        self.source = source
        # 得scope
        self.scope = self.__get_correct_scope(scope)
        # 得到name,key使用的正则表达式,取第几个值
        self.name, self.name_key, self.name_count = self.__get_correct_name(name, self.scope)
        # 得到动作
        self.act = self.__get_correct_act(act)
        # 得到要替换的value
        self.value = self.__get_correct_value(value, self.act, self.name)

    @staticmethod
    def __get_correct_scope(scope):
        """
        得到正确的body
        :return:
        """
        if scope is None:
            return "body"
        scope = scope.lower()
        if scope == "file":
            return "files"
        return scope

    @staticmethod
    def __get_correct_name(name, scope):
        """
        得到正确的name
        :param name:
        :return:
        """
        name_key, name_count = None, None
        if name is None:
            raise InfNameIsNullException()
        if Regex.start_with_regex(name):
            # 判断scope是否是file，如果是file，则抛出错误
            if scope == "file":
                raise InfFileNameIsIncorrectException(name)
            # 当是正则表达式时，获得其正则表达式
            name_key, name_count = Regex.get_real_regex(name)
            name = "$regex"
        if WellParse.is_well(name):
            name_key = name
            name = "#"
        if name == "$whole" and scope == "file":
            raise InfFileNameIsIncorrectException(name)
        return name, name_key, name_count

    @staticmethod
    def __get_correct_act(act):
        """
        得到正确的动作
        :param act:
        :return:
        """
        if act is None:
            act = "replace"
        else:
            act = act.lower()
        if act not in ["delete", "replace", "insert", "print", "replace or insert"]:
            raise InfActIsIncorrectException(act)
        return act

    @staticmethod
    def __get_correct_value(value, act, name):
        """
        得到正确的value
        :param value:
        :return:
        """
        if act in ["delete"]:
            return None
        if value is None:
            raise InfValueIsNotNoneException(act, name)
        return value


class PreProcessor(object):
    """
    前置处理器
    """

    # 空白字符正则
    __space_re_o = re.compile(r"\s")

    # 前置处理的标签
    __pre_tag = Utils.PRE_TAG
    # 接口处理的标签
    __interface_tag = Utils.INTERFACE_TAG

    def __init__(self, config: ConfigLoader, interface_data: dict, interface_info: Interface, data: dict):
        self.__config = config
        # db_info
        self.__db_info = data.get("db_info")
        # 接口信息
        self.__interface_info = interface_info
        # 接口数据
        self.__interface_data = interface_data
        # 取到前置处理器的数据
        self.__data = data
        # 循环的数量
        self.__cycle = 0
        # 记录break的状态
        self.__break = False
        # 记录continue的状态
        self.__continue = False

    def work(self, *context: dict):
        """
        前置处理器开始工作
        """
        logger.debug("执行前置处理")
        # 创建一个局部上下文
        new_context = {}
        self.__core(self.__data, self.__db_info, new_context, *context)

    def __core(self, data, db_info, *context: dict):
        """
        工作核心
        """
        un = self.__pre_tag + self.__interface_tag
        is_if = False
        hit_if = False
        for pre in Utils.merge_and_sort(data, un):
            name = pre.get("name")
            value = pre.get("value")
            logger.info("执行{}标签".format(name))
            # 判断是if还是其他
            if name == "if":
                # 处理if
                is_if = True
                hit_if = self.__if(value, db_info, *context)
            elif is_if and name == "elif":
                if not is_if:
                    raise MyException("标签 elif 位置错误！")
                # 处理elif
                if hit_if:
                    continue
                hit_if = self.__if(value, db_info, *context)
            elif name == "else":
                if not is_if:
                    raise MyException("标签 else 位置错误！")
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
                self.__cycle += 1
                is_if = False
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
                # 判断是属于前置处理还是接口处理
                if name in self.__pre_tag:
                    # 单个处理器参数
                    db_info = db_info if value.get("db_info") is None else Express.calculate_str(self.__config,
                                                                                                 value.get("db_info"),
                                                                                                 *context)
                    type_ = value.get("type")
                    key = value.get("key")
                    act = value.get("act")
                    desc = value.get("desc")
                    n = value.get("name")
                    var_type = value.get("var_type")
                    v = value.get("value")
                    re_type = value.get("re_type")
                    _v = value.get("$value")
                    sql = value.get("sql")
                    scope = value.get("scope")
                    if name == "processor":
                        raise MyException("processor标签已弃用，请使用对应标签替换！")
                    elif name == "print":
                        v = _v if v is None else v
                        type_ = type_ if type_ else "req_data" if v is None else "none"
                        key = "$whole" if key is None else key
                        act = "print"
                        desc = desc if desc else "打印请求报文" if type_ == "req_data" and key == "$whole" else "打印"
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
                    elif name == "print_var":
                        v = "${{{}}}".format(n)
                        type_ = "none"
                        key = "$whole"
                        act = "print"
                        desc = "打印变量 {} ".format(n)
                    elif name == "sql":
                        desc = "执行sql"
                        type_ = "sql"
                        key = "$whole" if key is None else key
                        # 如果存在name，则使用set动作，不存在则是用match
                        act = "match" if n is None else "set"
                        v = ".*" if n is None else v
                        scope = "global" if scope is None else scope
                    elif name == "expression":
                        type_ = "none"
                        key = "$whole"
                        v = _v
                        desc = "执行表达式 {}".format(v)
                        act = "execute"
                    else:
                        raise UnexpectedTagsException()
                    pre = ProcessorData(db_info, type_, key, act, n, var_type, v, re_type, desc, sql, scope,
                                        self.__interface_info.body_type)
                    self.__work_for_pre(pre, *context)
                else:
                    # 单个接口内容处理
                    scope = name
                    n = value.get("name")
                    v = value.get("$value")
                    act = value.get("act")
                    if type(value) != dict:
                        raise InfNameIsNullException()
                    if name in self.__interface_tag:
                        pass
                    else:
                        raise UnexpectedTagsException()
                    inf = InfoData(pre, scope, n, v, act)
                    self.__work_for_interface(inf, *context)

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
                logger.debug("for标签无可遍历的数据")
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
                logger.debug("for标签无可遍历的数据")

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

    def __if(self, data, db_info, *context: dict):
        """
        处理if
        """
        # 取到ex，如果ex计算的值是一个假值，则不执行
        ex = data.get("ex")
        db_info = db_info if data.get("db_info") is None else Express.calculate_str(self.__config, data.get("db_info"),
                                                                                    *context)
        if not Express.is_express(ex):
            raise MyException("标签格式有误，ex属性必须是被${{}}包围的表达式")
        if len(Express.get_express_list(ex)) > 1:
            raise MyException("标签格式有误，ex属性只能指定1个表达式")
        r = Express.calculate_str(self.__config, ex, *context)
        if r:
            logger.info("判断为真，执行子标签")
            logger.debug("ex表达式结果为 {} ，继续执行子标签".format(r))
            self.__core(data, db_info, *context)
        else:
            logger.info("判断为假，不执行子标签")
            logger.debug("ex表达式结果为 {} ，不执行子标签".format(r))
        return r

    def __else(self, data, db_info, *context: dict):
        """
        处理else
        """
        # 取到ex，如果ex计算的值是一个假值，则不执行
        logger.info("所有分支未命中，执行else分支")
        db_info = db_info if data.get("db_info") is None else Express.calculate_str(self.__config, data.get("db_info"),
                                                                                    *context)
        logger.debug("继续执行子标签")
        self.__core(data, db_info, *context)

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

    def __inject_res_and_req(self, context: dict):
        # 注入变量
        context["__req_data__"] = self.__interface_info.body
        context["__req_header__"] = self.__interface_info.header

    def __work_for_pre(self, pre, *context: dict):
        self.__inject_res_and_req(context[0])
        logger.debug("标签开始执行,它的描述为 {}".format(pre.desc))
        if pre.type == "none" and pre.value is not None:
            # 直接对value值进行操作
            self.__process_value(pre, *context)
        elif pre.type == "sql":
            # 对sql进行前置处理
            logger.debug("标签将从 数据库 取得数据")
            self.__process_sql(pre, *context)
        elif pre.type == "req_data":
            # 对请求报文进行处理
            logger.debug("标签将从 请求报文 取得数据")
            self.__process_req_data(pre, *context)
        elif pre.type == "req_header":
            # 对响应头进行处理
            logger.debug("标签将从 请求头 取得数据")
            self.__process_req_header(pre, *context)
        elif pre.type == "none":
            raise PreValueIsNotSpecifiedException()
        else:
            raise PreTypeIsIncorrectException(pre.type)

    def __process_req_header(self, pre: ProcessorData, *context: dict):
        """
        处理请求头
        """
        re_type = pre.re_type
        key = Express.calculate_str(self.__config, pre.key, *context)
        desc = pre.desc
        res = self.__interface_info.header
        names = pre.names
        act = pre.act
        var_type = pre.var_type
        expect = Express.calculate_str(self.__config, pre.value, *context)
        source_value = pre.value
        scope = pre.scope
        if key == "$whole":
            res = None if res == "" else res
            self.__process(act, desc, res, expect, names, var_type, scope, *context)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            re_regex = Regex(pre.key_regex, pre.key_count).get_value(res)
            if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                raise PreNotFindValueException(pre.type,
                                               "$regex[{}]:{}".format(pre.key_regex, str(pre.key_count)))
            if re_regex is Utils.ERROR and source_value is not None and act == "set":
                re_regex = expect
                logger.debug("标签从 请求头 提取数据失败，使用默认值 {}".format(expect))
            self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
        else:
            if re_type in ["key_value"]:
                re_json = JsonParse(res).get_value(key)
                if re_json is Utils.ERROR and (source_value is None or act != "set"):
                    raise PreNotFindValueException(pre.type, key)
                if re_json is Utils.ERROR and source_value is not None and act == "set":
                    re_json = expect
                    logger.debug("标签从 请求头 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_json, expect, names, var_type, scope, *context)
            else:
                raise PreReTypeIsNotSupportedException(re_type)

    def __process_req_data(self, pre: ProcessorData, *context: dict):
        """
        处理请求报文
        :param pre:
        :return:
        """
        re_type = self.__interface_info.body_type
        if re_type is None:
            raise PreReqDataIsNullException()
        key = Express.calculate_str(self.__config, pre.key, *context)
        desc = pre.desc
        res = self.__interface_info.body
        names = pre.names
        act = pre.act
        var_type = pre.var_type
        expect = Express.calculate_str(self.__config, pre.value, *context)
        source_value = pre.value
        scope = pre.scope
        if key == "$whole":
            res = None if res == "" else res
            self.__process(act, desc, res, expect, names, var_type, *context)
        elif key == "$regex":
            # 如果使用正则时，则提取后再进行比较
            re_regex = Regex(pre.key_regex, pre.key_count).get_value(res)
            if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                raise PreNotFindValueException(pre.type,
                                               "$regex[{}]:{}".format(pre.key_regex, str(pre.key_count)))
            if re_regex is Utils.ERROR and source_value is not None and act == "set":
                re_regex = expect
                logger.debug("标签从 请求报文 提取数据失败，使用默认值 {}".format(expect))
            self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
        else:
            if re_type in ["json", "key_value", "form_gb18030"]:
                re_json = JsonParse(res).get_value(key)
                if re_json is Utils.ERROR and (source_value is None or act != "set"):
                    raise PreNotFindValueException(pre.type, key)
                if re_json is Utils.ERROR and source_value is not None and act == "set":
                    re_json = expect
                    logger.debug("标签从 请求报文 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_json, expect, names, var_type, scope, *context)
            elif re_type == "xml":
                re_xml = XmlParse(res).get_value(key)
                if re_xml is Utils.ERROR and (source_value is None or act != "set"):
                    raise PreNotFindValueException(pre.type, key)
                if re_xml is Utils.ERROR and source_value is not None and act == "set":
                    re_xml = expect
                    logger.debug("标签从 请求报文 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_xml, expect, names, var_type, scope, *context)
            else:
                raise PreReTypeIsNotSupportedException(re_type)

    def __process_sql(self, pre: ProcessorData, *context: dict):
        """
        处理sql
        :param pre:
        :return:
        """
        # 处理sql执行结果
        re_type = pre.re_type
        key = Express.calculate_str(self.__config, pre.key, *context)
        desc = pre.desc
        sql = Express.calculate_str(self.__config, pre.sql, *context)
        db_info = pre.db_info
        scope = pre.scope
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
        names = pre.names
        act = pre.act
        var_type = pre.var_type
        expect = Express.calculate_str(self.__config, pre.value, *context)
        source_value = pre.value
        if re_type == "table":
            if key == "$whole":
                res = None if res.res == "" else TableParse(res.res).get_value(key)
                self.__process(act, desc, res, expect, names, var_type, scope, *context)
            elif key == "$regex":
                re_regex = Regex(pre.key_regex, pre.key_count).get_value(res.res)
                if re_regex is Utils.ERROR and (source_value is None or act != "set"):
                    raise PreNotFindValueException(pre.type,
                                                   "$regex[{}]:{}".format(pre.key_regex, str(pre.key_count)))
                if re_regex is Utils.ERROR and source_value is not None and act == "set":
                    re_regex = expect
                    logger.debug("标签从 数据库 提取数据失败，使用默认值 {}".format(expect))
                self.__process(act, desc, re_regex, expect, names, var_type, scope, *context)
            else:
                # 如果是其他key
                real = TableParse(res.res).get_value(key)
                if real is Utils.ERROR and (source_value is None or act != "set"):
                    raise PreNotFindValueException(pre.type, key)
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
            raise PreReTypeIsNotSupportedException(re_type)

    def __process_value(self, pre: ProcessorData, *context: dict):
        """
        直接对value值进行处理
        :param pre:
        :return:
        """
        value = Express.calculate_str(self.__config, pre.value, *context)
        self.__process(pre.act, pre.desc, value, None, pre.names, pre.var_type, pre.scope, *context)

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
        elif act == "execute":
            # 执行表达式
            pass
        elif act == "logger":
            logger.debug(value)
        else:
            raise PreActIsIncorrectException(act)

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
            raise PreSleepValueIsNotNumberException(str(value))
        logger.debug("标签执行成功，将睡眠 {} 秒".format(wait))
        time.sleep(wait)

    @staticmethod
    def __process_set(names, value, var_type, scope, *context: dict):
        """
        set类型的前置处理器
        :return:
        """
        if len(names) > 1:
            if type(value) not in [list, tuple]:
                raise PreValueTypeIsNotCorrectException(value, type(value))
            if len(names) != len(value):
                raise PreValueLengthIsNotCorrectException(len(names), len(value))
            for i in range(len(names)):
                _value = PreProcessor.__get_specified_type_var(value[i], var_type)
                if scope == "global":
                    for _context in context:
                        _context[names[i]] = _value
                    logger.debug("标签存储了变量 {} 到变量池，其值为 {}".format(names[i], value[i]))
                else:
                    context[0][names[i]] = _value
                    logger.debug("标签存储了变量 {} 到当前变量池，其值为 {}".format(names[i], value[i]))
        else:
            _value = PreProcessor.__get_specified_type_var(value, var_type)
            if scope == "global":
                for _context in context:
                    _context[names[0]] = _value
                logger.debug("标签存储了变量 {} 到变量池，其值为 {}".format(names[0], value))
            else:
                context[0][names[0]] = PreProcessor.__get_specified_type_var(value, var_type)
                logger.debug("标签存储了变量 {} 到当前变量池，其值为 {}".format(names[0], value))

    @staticmethod
    def __process_print(value, desc, var_type):
        """
        打印类型的前置处理器
        :return:
        """
        if not value:
            logger.info(FormatOutput.format_pre_info(desc, value))
        else:
            logger.info(FormatOutput.format_pre_info(desc, PreProcessor.__get_specified_type_var(value, var_type)))
        logger.debug("标签执行了打印")

    @staticmethod
    def __get_specified_type_var(var, var_type):
        """
        取到指定类型的变量
        :param var:
        :param var_type:
        :return:
        """
        # 如果var_type等于auto，则先自动推测返回类型，如果找不到匹配的，则直接返回
        if var_type == "auto":
            if ParamType.is_int(var):
                var_type = "int"
            elif ParamType.is_float(var):
                var_type = "float"
            elif ParamType.is_bool(var):
                var_type = "bool"
            elif var is None:
                return var
            else:
                var_type = "str"
        if var_type == "str":
            return str(var)
        elif var_type == "int":
            if not ParamType.is_int(str(var)):
                raise PreTransferFailException(str(var), "int")
            return ParamType.to_int(var)
        elif var_type == "float":
            if not ParamType.is_float(str(var)) and not ParamType.is_int(str(var)):
                raise PreTransferFailException(str(var), "float")
            return ParamType.to_float(var)
        elif var_type == "bool":
            value = str(var)
            if not ParamType.is_bool(str(value)):
                raise PreTransferFailException(str(var), "bool")
            return ParamType.to_bool(value)
        else:
            return var

    def __process_equal(self, real, expect):
        """
        真值和expect是否相等，如果不相等则抛出错误
        :param real:
        :param expect:
        :return:
        """
        if type(expect) is type(real):
            result = expect == real
        elif type(expect) in [dict, list, tuple] or type(real) in [dict, list, tuple]:
            expect = self.__space_re_o.sub("", str(expect))
            real = self.__space_re_o.sub("", str(real))
            result = expect == real
        else:
            result = str(expect) == str(real)
        if not result:
            raise PreValueAndExceptValueIsNotSameException(str(real), str(expect))

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
            raise PreValueAndExceptValueIsNotMatchedException(str(real), str(expect))

    def __work_for_interface(self, inf, *context: dict):
        """
        对接口处理器进行处理
        :param inf:
        :return:
        """
        self.__inject_res_and_req(context[0])
        # 判断参数是用来替换接口的哪个信息
        scope = inf.scope
        act = inf.act
        # 获取数据类型
        if scope == "header":
            # 替换请求头
            logger.debug("正在处理 {} 接口请求头的数据".format(self.__interface_info.name))
            ty = "json"
        elif scope == "body":
            # 替换请求报文
            logger.debug("正在处理 {} 接口请求报文 的数据".format(self.__interface_info.name))
            ty = self.__interface_info.body_type
        elif scope == "files":
            # 替换文件
            logger.debug("正在处理 {} 接口文件域 的数据".format(self.__interface_info.name))
            ty = "files"
        elif scope == "port":
            # 替换端口
            logger.debug("正在处理 {} 接口的端口".format(self.__interface_info.name))
            ty = "port"
        elif scope == "server":
            # 替换地址
            logger.debug("标签正在处理 {} 接口的服务器".format(self.__interface_info.name))
            ty = "server"
        elif scope == "param":
            # 替换请求参数
            logger.debug("正在处理 {} 接口请求参数 的数据".format(self.__interface_info.name))
            ty = "key_value"
        elif scope == "method":
            logger.debug("正在处理 {} 接口的请求方法".format(self.__interface_info.name))
            ty = "method"
        elif scope == "path":
            logger.debug("正在处理 {} 接口的请求路径".format(self.__interface_info.name))
            ty = "path"
        elif scope == "type":
            logger.debug("正在处理 {} 接口请求报文 的数据格式".format(self.__interface_info.name))
            ty = "type"
            scope = "body_type"
        else:
            raise UnexpectedTagsException()
        # 处理动作
        if act == "delete":
            self.__delete(ty, scope, inf, *context)
        elif act == "replace":
            self.__replace(ty, scope, inf, *context)
        elif act == "insert":
            self.__insert(ty, scope, inf, *context)
        elif act == "replace or insert":
            self.__replace_or_insert(ty, scope, inf, *context)
        else:
            raise InfActIsIncorrectException(act)
        logger.debug("已处理完成")

    def __delete(self, ty: str, scope: str, param: InfoData, *context: dict):
        """
        删除参数指定的键,并返回删除后的值
        :param param:
        :return:
        """
        # 取得要替换的key,$whole指整个替换
        key = Express.calculate_str(self.__config, param.name, *context)
        if key == "$whole":
            # 整个删除
            setattr(self.__interface_info, scope, None)
            logger.debug("将处理中数据整个清空")
        elif key == "$regex":
            # 正则删除
            attr = getattr(self.__interface_info, scope)
            deleted_re = Regex(param.name_key, param.name_count).remove_value(attr)
            if deleted_re is None:
                raise InfDataIsNotMatchedException(scope, param.name_key, self.__interface_info.name, str(attr))
            else:
                setattr(self.__interface_info, scope, deleted_re)
                logger.debug("使用正则表达式 {} ,删除了处理数据中的第 {} 个匹配".format(param.name_key, param.name_count))
        elif key == "#":
            # 字符符name
            raise InfDataNotSupportException(scope, self.__interface_info.name, "#表达式", "delete")
        else:
            # 部分删除
            # 取得要处理的请求数据
            attr = getattr(self.__interface_info, scope)
            # 按数据类型处理
            if ty == "json" or ty == "key_value" or ty == "form_gb18030":
                if not JsonParse.is_correct_json(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                deleted_re = JsonParse(attr).delete_value(key)
                logger.debug("删除了处理中数据由 {} 指定的内容".format(key))
            elif ty == "xml":
                if not XmlParse.is_xml(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                deleted_re = XmlParse(attr).remove_value(key)
                logger.debug("删除了处理中数据由 {} 指定的内容".format(key))
            elif ty == "files":
                if not Files.is_file_interface(attr):
                    raise InfIsNotFileException(self.__interface_info.name)
                deleted_re = Files(attr).remove_value(key)
                logger.debug("删除了处理中数据由 {} 指定的内容".format(key))
            else:
                raise InfReTypeIsUnsupportedException(ty)
            # 处理结果
            if deleted_re is None:
                raise InfDataIsNotFindException(scope, key, self.__interface_info.name)
            else:
                setattr(self.__interface_info, scope, deleted_re)

    def __replace(self, ty: str, scope: str, param: InfoData, *context: dict):
        # 取得要替换的key,$whole指整个替换
        replace_key = Express.calculate_str(self.__config, param.name, *context)
        # 取得要替换的值
        if self.__interface_info.body_type == "sql":
            value = Express.calculate_str(self.__config, param.value, *context)
        else:
            value = Express.calculate_str(self.__config, param.value, *context)
        if replace_key == "$whole":
            # 整个替换
            setattr(self.__interface_info, scope, value)
            logger.debug("将处理中数据整体替换为 {}".format(value))
        elif replace_key == "$regex":
            # 正则替换
            attr = getattr(self.__interface_info, scope)
            replace_re = Regex(param.name_key, param.name_count).replace_value(attr, value)
            if replace_re is None:
                raise InfDataIsNotMatchedException(scope, param.name_key, self.__interface_info.name, str(attr))
            else:
                setattr(self.__interface_info, scope, replace_re)
                logger.debug(
                    "使用了正则表达式 {} ,替换了处理中数据第 {} 个匹配为 {}".format(param.name_key, param.name_count, value))
        elif replace_key == "#":
            attr = getattr(self.__interface_info, scope)
            replace_re = WellParse(attr).replace_value(param.name_key, value)
            if replace_re is None:
                raise InfDataNotContainsTheWellException(scope, param.name_key, self.__interface_info.name, str(attr))
            else:
                setattr(self.__interface_info, scope, replace_re)
                logger.debug("将处理中数据的 {} 部分替换为 {}".format(param.name_key, value))
        else:
            # 按类型替换
            # 取得要替换的源值
            attr = getattr(self.__interface_info, scope)
            # 按类型处理
            if ty == "json" or ty == "key_value" or ty == "form_gb18030":
                if not JsonParse.is_correct_json(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                replace_re = JsonParse(attr).replace_value(replace_key, value)
                logger.debug("将处理中数据由 {} 指定的内容替换为 {}".format(replace_key, value))
            elif ty == "xml":
                if not XmlParse.is_xml(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                replace_re = XmlParse(attr).replace_value(replace_key, value)
                logger.debug("将处理中数据由 {} 指定的内容替换为 {}".format(replace_key, value))
            elif ty == "files":
                if not Files.is_file_interface(attr):
                    raise InfIsNotFileException(self.__interface_info.name)
                replace_re = Files(attr).replace_value(replace_key, value)
                logger.debug("将处理中数据由 {} 指定的内容替换为 {}".format(replace_key, value))
            else:
                raise InfReTypeIsUnsupportedException(ty)
            # 对处理后的结果处理
            if replace_re is None:
                raise InfDataIsNotFindException(scope, replace_key, self.__interface_info.name)
            else:
                setattr(self.__interface_info, scope, replace_re)

    def __insert(self, ty: str, scope: str, param: InfoData, *context: dict):
        # 取得要插入的key,$whole指整个插入
        insert_key = Express.calculate_str(self.__config, param.name, *context)
        # 取得要插入的值
        value = Express.calculate_str(self.__config, param.value, *context)
        if insert_key == "$whole":
            # 整个插入
            setattr(self.__interface_info, scope, value)
            logger.debug("处理中数据被全覆盖，并插入了新的内容 {}".format(value))
        elif insert_key == "$regex":
            # 字符符name
            raise InfDataNotSupportException(scope, self.__interface_info.name, "正则表达式", "insert")
        elif insert_key == "#":
            # 字符符name
            raise InfDataNotSupportException(scope, self.__interface_info.name, "#表达式", "insert")
        else:
            # 部分插入
            # 取得要处理记录
            attr = getattr(self.__interface_info, scope)
            # 按类型处理
            if ty == "json" or ty == "key_value" or ty == "form_gb18030":
                if not JsonParse.is_correct_json(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                insert_re = JsonParse(attr).insert_value(insert_key, value)
                logger.debug("向处理中数据插入了由 {} 指定的内容 {}".format(insert_key, value))
            elif ty == "files":
                if not Files.is_file_interface(attr):
                    raise InfIsNotFileException(self.__interface_info.name)
                insert_re = Files(attr).insert_value(insert_key, value)
                logger.debug("向处理中数据插入了由 {} 指定的内容 {}".format(insert_key, value))
            elif ty == "xml":
                if not XmlParse.is_xml(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                insert_re = XmlParse(attr).insert_value(insert_key, value)
                logger.debug("向处理中数据插入了由 {} 指定的内容 {}".format(insert_key, value))
            else:
                raise InfReTypeIsUnsupportedException(ty)
            # 处理结果数据
            if insert_re is None:
                raise InfInsertFailException(scope, self.__interface_info.name, insert_key, str(value))
            else:
                setattr(self.__interface_info, scope, insert_re)

    def __replace_or_insert(self, ty: str, scope: str, param: InfoData, *context: dict):
        # 取得要替换或插入的key，$whole指整个处理
        key = Express.calculate_str(self.__config, param.name, *context)
        # 取得处理后的值
        value = Express.calculate_str(self.__config, param.value, *context)
        if key == "$whole":
            # 整个插入
            setattr(self.__interface_info, scope, value)
            logger.debug("处理中的数据被全替换为 {}".format(value))
        elif key == "$regex":
            # 正则替换
            attr = getattr(self.__interface_info, scope)
            replace_re = Regex(param.name_key, param.name_count).replace_value(attr, value)
            if replace_re is None:
                raise InfDataIsNotMatchedException(scope, param.name_key, self.__interface_info.name, str(attr))
            else:
                setattr(self.__interface_info, scope, replace_re)
                logger.debug(
                    "使用了正则表达式 {} ,替换了处理中数据第 {} 个匹配为 {}".format(param.name_key, param.name_count, value))
        elif key == "#":
            attr = getattr(self.__interface_info, scope)
            replace_re = WellParse(attr).replace_value(param.name_key, value)
            if replace_re is None:
                raise InfDataNotContainsTheWellException(scope, param.name_key, self.__interface_info.name, str(attr))
            else:
                setattr(self.__interface_info, scope, replace_re)
                logger.debug("将处理中数据的 {} 部分替换为 {}".format(param.name_key, value))
        else:
            # 按类型替换或插入
            # 取得要替换或插入的源值
            attr = getattr(self.__interface_info, scope)
            # 按类型处理
            if ty == "json" or ty == "key_value" or ty == "form_gb18030":
                if not JsonParse.is_correct_json(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                replace_re = JsonParse(attr).replace_value(key, value)
                if replace_re is None:
                    insert_re = JsonParse(attr).insert_value(key, value)
                    if insert_re is None:
                        raise InfInsertFailException(scope, self.__interface_info.name, key, str(value))
                    else:
                        setattr(self.__interface_info, scope, insert_re)
                        logger.debug("向处理中数据插入了由 {} 指定的内容 {}".format(key, value))
                else:
                    setattr(self.__interface_info, scope, replace_re)
                    logger.debug("将处理中数据由 {} 指定的内容替换为 {}".format(key, value))
            elif ty == "xml":
                if not XmlParse.is_xml(attr):
                    raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                replace_re = XmlParse(attr).replace_value(key, value)
                if replace_re is None:
                    if not XmlParse.is_xml(attr):
                        raise InfDataIsIncorrectException(scope, self.__interface_info.name)
                    insert_re = XmlParse(attr).insert_value(key, value)
                    if insert_re is None:
                        raise InfInsertFailException(scope, self.__interface_info.name, key, str(value))
                    else:
                        setattr(self.__interface_info, scope, insert_re)
                        logger.debug("向处理中数据插入了由 {} 指定的内容 {}".format(key, value))
                else:
                    setattr(self.__interface_info, scope, replace_re)
                    logger.debug("将处理中数据由 {} 指定的内容替换为 {}".format(key, value))
            elif ty == "files":
                if not Files.is_file_interface(attr):
                    raise InfIsNotFileException(self.__interface_info.name)
                replace_re = Files(attr).replace_value(key, value)
                if replace_re is None:
                    if not Files.is_file_interface(attr):
                        raise InfIsNotFileException(self.__interface_info.name)
                    insert_re = Files(attr).insert_value(key, value)
                    if insert_re is None:
                        raise InfInsertFailException(scope, self.__interface_info.name, key, str(value))
                    else:
                        setattr(self.__interface_info, scope, insert_re)
                        logger.debug("向处理中数据插入了由 {} 指定的内容 {}".format(key, value))
                else:
                    setattr(self.__interface_info, scope, replace_re)
                    logger.debug("将处理中数据由 {} 指定的内容替换为 {}".format(key, value))
            else:
                raise InfReTypeIsUnsupportedException(ty)
