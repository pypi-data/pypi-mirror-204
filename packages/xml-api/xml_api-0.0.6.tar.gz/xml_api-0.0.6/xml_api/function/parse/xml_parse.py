import io
from xml.sax import make_parser
from xml.sax.handler import ContentHandler, feature_namespaces
from xml.sax.xmlreader import InputSource
from .key.point import PointKey

from ..utils.utils import Utils


class TextValue(object):
    def __init__(self, value=""):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class ListValue(object):

    def __init__(self):
        self.__list = list()

    def push(self, value):
        self.__list.append(value)

    def pop(self, key, index):
        new_list = list()
        i = 0
        for e in self.__list:
            if type(e) is Node and e.name == key:
                if index == i:
                    i += 1
                    continue
                i += 1
                if index == None:
                    continue
            elif type(e) is TextValue and key == "$text":
                if index == i:
                    i += 1
                    continue
                i += 1
                if index == None:
                    continue
            new_list.append(e)
        self.__list = new_list

    def size(self):
        return len(self.__list)

    @property
    def value(self):
        return self.__list

    def get(self, key, index):
        t = ListValue()
        i = 0
        for e in self.__list:
            if type(e) is Node and e.name == key:
                t.push(e)
                if i == index:
                    return e, e.value
                i += 1
            elif key == "$text" and type(e) is TextValue:
                t.push(e)
                if i == index:
                    return self, e
                i += 1
        if t.size() == 0:
            raise Exception("key错误！")
        if index != None and index >= i:
            raise Exception("key错误！")
        return self, t

    def replace(self, key, index, value):
        i = 0
        for e in self.__list:
            if type(e) is Node and e.name == key:
                if i == index:
                    e.value = TextValue(value)
                elif index == None:
                    e.value = TextValue(value)
                i += 1
            elif key == "$text" and type(e) is TextValue:
                if i == index:
                    e.value = value
                elif index is None:
                    e.value = value
                i += 1

    def insert(self, key, index, value):
        i = 0
        temp = list()
        for e in self.__list:
            if type(e) is Node and e.name == key:
                temp.append(e)
                if i == index:
                    e.value = TextValue(value)
                elif index is None:
                    e.value = TextValue(value)
                i += 1
            elif key == "$text" and type(e) is TextValue:
                if i == index:
                    e.value = value
                elif index is None:
                    e.value = value
                i += 1
        if index != None and index >= len(temp):
            node = Node()
            node.name = key
            node.value = TextValue(value)
            self.__list.append(node)


class Node(object):

    def __init__(self, name=None):
        self.__name = name
        self.__value = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def push(self, o):
        if self.__value is None:
            self.__value = o
        elif type(self.__value) is ListValue:
            self.__value.push(o)
        else:
            temp = self.__value
            self.__value = ListValue()
            self.__value.push(temp)
            self.__value.push(o)

    def get(self, k):
        if self.name == k:
            return self.value
        else:
            raise Exception("key错误！")

    def replace(self, key, value):
        if self.name == key:
            self.value = TextValue(value)
        else:
            raise Exception("key错误！")

    def insert(self, key, value):
        if self.name == key:
            self.value = TextValue(value)
            return True
        else:
            return False

    def remove_node(self, key):
        if self.__value.name == key:
            self.__value = None

    def remove_list_value(self, key, index):
        self.__value.pop(key, index)


class ParseXmlHandler(ContentHandler):
    """
    xml handler
    """

    def __init__(self):
        super().__init__()
        # 用来保存当前节点的文本
        self.__active_element_text = ""
        # 用来保存xml结构的栈区
        self.__stack_of_saving_xml_structure = []
        # 用来保存当前节点
        self.__active_node = None

    def startElement(self, name, attribute):
        # 遇到一个节点，以节点的名字作为参数,属性值为其字典内容
        if self.__active_element_text != "":
            # 当文本元素不为空时，对其进行存储
            self.__active_node.push(TextValue(self.__active_element_text))
            self.__active_element_text = ""
        # 如果当前节点不为空，则将当前节点置入栈区
        if self.__active_node:
            self.__stack_of_saving_xml_structure.append(self.__active_node)
        # 初始化相关数据
        self.__active_node = Node(name)

    def characters(self, content):
        content = content.strip()
        if content != "":
            self.__active_element_text += content

    def endElement(self, name):
        # 存储文本节点
        if self.__active_element_text != "":
            self.__active_node.push(TextValue(self.__active_element_text))
            self.__active_element_text = ""
        # 如果堆栈里还有元素，需要处理
        if len(self.__stack_of_saving_xml_structure) <= 0:
            return
        # 合并元素节点
        active_node: Node = self.__active_node
        self.__active_node = self.__stack_of_saving_xml_structure.pop()
        self.__active_node.push(active_node)

    @property
    def xml(self):
        return self.__active_node


class SimpleXmlParser(object):
    """
    xml 解析器
    """

    def __init__(self, xml: str):
        """
        xml 解析器
        :param xml: 需要解析的xml字符串
        :return: None
        """
        self.__xml = xml

    def parse_xml(self) -> Node:
        """
        取得xml解析的结果
        :return: 由xml文件构成的字典值
        """
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        handler = ParseXmlHandler()
        parser.setContentHandler(handler)
        try:
            inpsrc = InputSource()
            inpsrc.setCharacterStream(io.StringIO(self.__xml))
            parser.parse(inpsrc)
        except Exception as e:
            raise e
        return handler.xml


class NodeToXml(object):
    """"""

    def __init__(self, node: Node, beauty=False, add=2, blank="", floor=0):
        self.__node = node
        self.__beauty = beauty
        self.__init_floor = floor
        self.__add = add
        self.__blank = blank

    def parse(self):
        node = self.__node
        x, e = self.__parse_detail(node, self.__init_floor)
        return x

    def __parse_detail(self, node, floor):
        """
            <a>
                <b>ddd</b>
            </a>
        :param node:
        :param floor:
        :return:
        """
        if type(node) is Node:
            if node.name is None:
                return self.__parse_detail(node.value, floor)
            if self.__beauty:
                xml = "{}<{}>".format(floor * self.__blank, node.name)
                x, e = self.__parse_detail(node.value, floor + self.__add)
                if e:
                    xml += "\n"
                xml += "{}".format(x)
                if e:
                    xml += "\n{}".format(floor * self.__blank)
                xml += "</{}>".format(node.name)
                return xml, True
            else:
                x, e = self.__parse_detail(node.value, floor + self.__add)
                return "<{}>{}</{}>".format(node.name, x, node.name), False
        elif node is None:
            return "", False
        elif type(node) is ListValue:
            xml = ""
            for n in node.value:
                x, e = self.__parse_detail(n, floor)
                if self.__beauty:
                    if type(n) is TextValue or n is None:
                        xml += "{}".format(floor * self.__blank)
                    xml += "{}".format(x)
                    xml += "\n"
                else:
                    xml += "{}".format(x)
            if self.__beauty:
                return xml[:-1], True
            return xml, False
        elif type(node) is TextValue:
            return node.value, False


class XmlParse(object):

    def __init__(self, xml: str):
        """
        xml字符串提取器
        :param xml:
        """
        if xml:
            xml = xml.strip()
        else:
            xml = ""
        self.__xml_prefix,self.__xml=Utils.split_xml(xml)

    @classmethod
    def xml_to_node(cls, xml):
        return SimpleXmlParser(xml).parse_xml()

    @classmethod
    def node_to_xml(cls, node):
        if type(node) is str:
            return node
        else:
            return NodeToXml(node).parse()

    def get_value(self, key: str):
        """
        从xml获取的值，如果没有取到，则返回错误标志
        :return:
        """
        point_key = PointKey(key)
        try:
            if self.__xml == "":
                node = Node()
            else:
                node = XmlParse.xml_to_node(self.__xml)
            while point_key.has():
                k = point_key.next()
                if type(node) is Node and type(k) is str:
                    node = node.get(k)
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() > 0:
                        i = 0
                    if point_key.is_index_next_key():
                        i = point_key.next()
                    pre, node = node.get(k, i)
                else:
                    raise Exception("不是预期的！")
            if type(node) is ListValue and node.size()==1:
                pre,node=node.get(k,0)
            # 还需调用一次转xml
            return XmlParse.node_to_xml(node)
        except Exception:
            return Utils.ERROR

    def replace_value(self, key, value):
        """
        将字xml指定的值设置为指定的value，并返回替换后的字符串
        :param value:
        :param key:
        :return
        """
        point_key = PointKey(key)
        try:
            if self.__xml == "":
                node = Node()
            else:
                node = XmlParse.xml_to_node(self.__xml)
            if self.get_value(key) == Utils.ERROR:
                return None
            n_node = node
            while point_key.size() > 2:
                k = point_key.next()
                if type(node) is Node and type(k) is str:
                    node = node.get(k)
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() > 0:
                        i = 0
                    if point_key.is_index_next_key():
                        i = point_key.next()
                    pre, node = node.get(k, i)
                else:
                    raise Exception("不是预期的！")
            if point_key.size() <= 2:
                k = point_key.next()
                if type(node) is Node:
                    if point_key.size() == 1:
                        node = node.get(k)
                        k = point_key.next()
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() == 1:
                        i = 0
                        if not point_key.is_index_next_key():
                            pre, node = node.get(k, i)
                            k = point_key.next()
                else:
                    raise Exception("不是预期的！")
                if type(node) is Node:
                    node.replace(k, value)
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() > 0:
                        i = 0
                    if point_key.is_index_next_key():
                        i = point_key.next()
                    node.replace(k, i, value)
                else:
                    raise Exception("不是预期的！")
            return "{}{}".format(self.__xml_prefix, XmlParse.node_to_xml(n_node))
        except Exception:
            return None

    def remove_value(self, key: str):
        """
        从xml匹配的值，并返回移除后的字符串
        :return:
        """
        point_key = PointKey(key)
        try:
            if self.__xml == "":
                node = Node()
            else:
                node = XmlParse.xml_to_node(self.__xml)
            if self.get_value(key) == Utils.ERROR:
                return None
            pre_node = Node()
            pre_node.value = node
            n_node = pre_node
            while point_key.size() > 2:
                k = point_key.next()
                if type(node) is Node and type(k) is str:
                    pre_node = node
                    node = node.get(k)
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() > 1:
                        i = 0
                    if point_key.is_index_next_key():
                        i = point_key.next()
                    pre_node, node = node.get(k, i)
                else:
                    raise Exception("不是预期的！")
            if point_key.size() <= 2:
                k = point_key.next()
                if type(node) is Node:
                    if point_key.size() == 1:
                        pre_node = node
                        node = node.get(k)
                        k = point_key.next()
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() == 1:
                        i = 0
                        if not point_key.is_index_next_key():
                            pre_node, node = node.get(k, i)
                            k = point_key.next()
                else:
                    raise Exception("不是预期的！")
                if type(pre_node) is Node:
                    if type(node) is Node:
                        pre_node.remove_node(k)
                    elif type(node) is ListValue:
                        i = None
                        if point_key.size() > 0:
                            i = 0
                        if point_key.is_index_next_key():
                            i = point_key.next()
                        pre_node.remove_list_value(k, i)
                    else:
                        raise Exception("不是预期的！")
                else:
                    raise Exception("不是预期的！")
            return "{}{}".format(self.__xml_prefix, XmlParse.node_to_xml(n_node))
        except Exception:
            return None

    def insert_value(self, key: str, value):
        """
        插入
        """
        point_key = PointKey(key)
        try:
            if self.__xml == "":
                node = Node()
            else:
                node = XmlParse.xml_to_node(self.__xml)
            pre_node = Node()
            pre_node.value = node
            n_node = pre_node
            while point_key.size() > 2 and type(node) is not TextValue:
                k = point_key.next()
                if type(node) is Node and type(k) is str:
                    pre_node = node
                    node = node.get(k)
                elif type(node) is ListValue:
                    i = None
                    if point_key.size() > 0:
                        i = 0
                    if point_key.is_index_next_key():
                        i = point_key.next()
                    pre_node, node = node.get(k, i)
                else:
                    raise Exception("不是预期的！")
            # 如果是textvalue就进行创建
            if type(node) is TextValue:
                if type(pre_node) is Node:
                    pre_node.value = TextValue(self.__create_tag(point_key, value))
                else:
                    raise Exception("未预期的错误")
            else:
                if point_key.size() <= 2:
                    k = point_key.next()
                    if type(node) is Node:
                        if point_key.size() == 1 and not point_key.is_index_next_key():
                            pre_node = node
                            node = node.get(k)
                            k = point_key.next()
                    elif type(node) is ListValue:
                        i = None
                        if point_key.size() == 1:
                            i = 0
                            if not point_key.is_index_next_key():
                                pre_node, node = node.get(k, i)
                                k = point_key.next()
                    else:
                        raise Exception("不是预期的！")
                    if type(pre_node) is Node:
                        if type(node) is Node:
                            i=0
                            if point_key.size()>0:
                                if point_key.is_index_next_key():
                                    i=point_key.next()
                                else:
                                    raise Exception("不是期望的！")
                            if not (i<=0 and node.insert(k,value)):
                                new_node = Node(k)
                                new_node.push(TextValue(value))
                                pre_node.push(new_node)
                        elif type(node) is ListValue:
                            i = None
                            if point_key.size() > 0:
                                i = 0
                            if point_key.is_index_next_key():
                                i = point_key.next()
                            node.insert(k, i, value)
                        else:
                            raise Exception("不是预期的！")
                    else:
                        raise Exception("不是预期的")
            return "{}{}".format(self.__xml_prefix, XmlParse.node_to_xml(n_node))
        except Exception:
            return None

    def __create_tag(self, point_key: PointKey, value):
        """
        创建标签
        """
        if point_key.size() == 0:
            return value
        if point_key.size() > 0:
            if point_key.is_index_next_key():
                raise Exception("提取表达式格式不正确！")
            tag = point_key.next()
            if point_key.is_index_next_key():
                point_key.next()
            return "<{}>{}</{}>".format(tag, self.__create_tag(point_key, value), tag)

    @staticmethod
    def is_xml(xml):
        try:
            XmlParse.xml_to_node(xml)
        except:
            return False
        return True
