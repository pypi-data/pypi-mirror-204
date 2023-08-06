from ...function.data.interface import Interfaces


class Inf(object):
    def __init__(self):
        # 接口列表
        self.__interfaces = None
        # 脚本数据
        self.__script_data = None

    @property
    def interfaces(self) -> Interfaces:
        return self.__interfaces

    @interfaces.setter
    def interfaces(self, interfaces: Interfaces):
        self.__interfaces = interfaces

    @property
    def script_data(self) -> dict:
        return self.__script_data

    @script_data.setter
    def script_data(self, script_data):
        self.__script_data = script_data
