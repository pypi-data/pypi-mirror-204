import builtins
import hashlib
import os
import random
import string
import time



def int(o):
    """转型为int"""
    return builtins.int(builtins.float(o))


def float(o):
    """转型为float"""
    return builtins.float(o)


def str(o):
    """转型为str"""
    return builtins.str(o)


def bool(o):
    """转型为bool"""
    return builtins.bool(o)


def len(o):
    """获得对象的长度"""
    return builtins.len(o)


def type(o):
    """获得数据的类型"""
    return builtins.type(o)


def loads(json_str):
    """将json字符串转为json对象"""
    from xml_api.function.parse.json_parse import JsonParse
    json = JsonParse.to_json(json_str)
    if json is None:
        raise Exception("[{}]不是正确的json字符串".format(json))
    return json


def dumps(o):
    """将json对象转为json字符串"""
    from xml_api.function.parse.json_parse import JsonParse
    return JsonParse.to_good_json_str(o)


def random_letter_and_number(length: int):
    """取得指定长度的随机字母和数字的组合"""
    s = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
    s = ''.join(s)
    return s


def random_number(length: int):
    """取得length长的随机数字"""
    s = [random.choice(string.digits) for _ in range(length)]
    s = ''.join(s)
    return s


def slice(s, f, l):
    """对字符串切片(s:待切片字符串,f:左切片数,l:右切片数)"""
    s = str(s)
    return s[f:l]


def joint(*args):
    """拼接字符串"""
    s = ""
    for a in args:
        a = str(a)
        s = "{}{}".format(s, a)
    return s


def now(format_str="%Y%m%d%H%M%S"):
    """取得现在的日期"""
    return time.strftime(format_str)


def get_now_date(year=True, mon=True, day=True, hour=True, min=True, second=True):
    """取得当前日期的字符串"""
    format_str = ""
    if year:
        format_str += "%Y"
    if mon:
        format_str += "%m"
    if day:
        format_str += "%d"
    if hour:
        format_str += "%H"
    if min:
        format_str += "%M"
    if second:
        format_str += "%S"
    return time.strftime(format_str)


def path_join(a, b):
    """拼接目录"""
    return os.path.join(a, b)

def sleep(wait):
    """睡眠wait秒"""
    time.sleep(wait)


def SHA1(o):
    """SHA1加密"""
    hash_new = hashlib.sha1()
    hash_new.update(str(o).encode("utf8"))
    hash_value = hash_new.hexdigest()
    # print(type(hash_value))
    hash_value = hash_value.upper()  # 转换为大写
    # print(hash_value)
    return hash_value


def MD5(o):
    """对pwd进行md5加密"""
    m = hashlib.md5()
    m.update(str(o).encode("utf-8"))
    return m.hexdigest()


def range(stop, start=0):
    return builtins.range(start, stop)


def round(o, ndigits=2):
    """四舍五入"""
    return builtins.round(o, ndigits)
