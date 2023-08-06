# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: beautify json
"""
import re
from ..parse.xml_parse import XmlParse, NodeToXml
from ..utils.utils import Utils


class BeautifyXml(object):
    __blank_re = re.compile(r"\s")
    __blank = Utils.BLANK_CHAR
    __single = 4

    def __init__(self, xml: str):
        """
        待美化的json字符串
        :param xml:
        """
        self.__xml = xml

    def beautify(self):
        """
        :return:
        """
        h, b = Utils.split_xml(self.__xml)
        number_of_blank = 4
        node = XmlParse.xml_to_node(b)
        xml = NodeToXml(node, True, number_of_blank, self.__blank, 4).parse()
        res = "{}\n{}".format(h, xml)
        return res
