"""
    author: Li Junxian
    function:about java
"""
import importlib.util
from multiprocessing import Process, Queue

if importlib.util.find_spec("jpype") is None:
    raise Exception("要使用jvm，请安装JPype1==1.3.0!")
jpype = importlib.import_module("jpype")


class JVMProcess(Process):

    def __init__(self, queue, fun, *args, **kwargs):
        super().__init__()
        self.__fun = fun
        self.__queue: Queue = queue
        self.__args = args
        self.__kwargs = kwargs

    def run(self) -> None:
        """
        执行jvm
        """
        jpype.startJVM()
        try:
            res = self.__fun(jpype, *self.__args, **self.__kwargs)
            self.__queue.put(res)
        except Exception as e:
            self.__queue.put(e)
        finally:
            jpype.shutdownJVM()

    @classmethod
    def exe(cls, fun,*args,**kwargs):
        """
        如果执行出错，将抛出错误

        可传入一个函数，该函数不能是匿名函数闭包，该函数第一个参数是jpype，其余参数可以自定义，需在该函数内完成java数据类型转换到python。

        def test(jpype):
            return str(jpype.JString("ddd"))
        """
        queue = Queue()
        jvm = JVMProcess(queue,fun,*args,**kwargs)
        jvm.start()
        jvm.join()
        data = queue.get()
        if isinstance(data, Exception):
            raise data
        return data
