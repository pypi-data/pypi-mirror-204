

class MyAssertionError(object):

    @staticmethod
    def raise_error(msg):
        raise TAssertionError(msg)


class TAssertionError(AssertionError):

    def __init__(self, msg):
        self.__msg = msg

    @property
    def msg(self):
        return self.__msg

    def __str__(self):
        msg = '''\n    raise\nAssertionError:{}'''.format(self.__msg)
        return msg
