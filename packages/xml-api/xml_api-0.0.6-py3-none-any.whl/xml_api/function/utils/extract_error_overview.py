from ...exception.my_exception import MyException


class ExtractErrorOverview(object):

    __split_str_list=[""]

    @classmethod
    def get(cls,e):
        if isinstance(e,AssertionError) or isinstance(e,MyException):
            return e.msg
        elif isinstance(e,Exception):
            return str(e)
        else:
            return "Unknown Error Overview!"
