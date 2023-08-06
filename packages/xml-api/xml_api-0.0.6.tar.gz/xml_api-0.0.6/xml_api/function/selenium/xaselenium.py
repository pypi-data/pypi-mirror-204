import importlib

from requests import Session

from ..cfg.config import ConfigLoader
from ..cookies.cookie import CookiesUtils
from ..utils.utils import Utils
from ...exception.my_exception import MyException


class XmlApiSelenium(object):

    def __init__(self, config: ConfigLoader, browser, browser_path, driver_path, silent):
        # 取得配置
        self.__config = config
        # 取得浏览器
        self.__browser = browser if browser is not None else self.__config.get_config("selenium_browser")
        # 取得浏览器路径
        self.__browser_path = browser_path if browser_path is not None else self.__config.get_config(
            "selenium_browser_path")
        # 取得driver路径
        self.__driver_path = driver_path if driver_path is not None else self.__config.get_config(
            "selenium_driver_path")
        # 定义silent
        if silent is None:
            self.__silent = self.__config.get_config("selenium_silent", bool)
        else:
            self.__silent = silent
        # 定义driver
        self.__driver = None

    def merge_cookies_to_requests(self, session: Session):
        if session is None:
            return session
        for cookie in self.__driver.get_cookies():
            name = cookie.get("name")
            value = cookie.get("value")
            optional = {}
            if cookie.get("domain") is not None:
                optional['domain'] = cookie.get("domain")
            if cookie.get("expiry") is not None:
                optional['expires'] = cookie.get("expiry")
            if cookie.get("path") is not None:
                optional['path'] = cookie.get("path")
            if cookie.get("secure") is not None:
                optional['secure'] = cookie.get("secure")
            if cookie.get("httpOnly") is not None:
                optional['rest'] = {'HttpOnly': cookie.get("httpOnly")},
            session.cookies.set(name, value, **optional)
        return session

    @property
    def driver(self):
        return self.__driver

    def make_driver(self, session: Session = None):
        """
        取到执行driver,并传入session，当调用get时合并cookie
        :return:
        """
        if importlib.util.find_spec("selenium") is None:
            raise MyException("如需使用selenium，请安装selenium==3.141.0")
        from selenium import webdriver as webdriver
        if Utils.lower(self.__browser) == "chrome":
            # 判断是否指定了浏览器路径
            option = None
            from selenium.webdriver.chrome.options import Options
            if self.__browser_path:
                # 指定浏览器参数
                option = Options()
                option.binary_location = self.__browser_path
                # 配置无需弹出浏览器
            if self.__silent:
                if option is None:
                    option = Options()
                option.add_argument('--headless')
                option.add_argument('--disable-gpu')
            # 如果指定了驱动路径
            driver_path = None
            if self.__driver_path:
                driver_path = self.__driver_path
            # 启动浏览器
            if option and driver_path:
                driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
            elif driver_path:
                driver = webdriver.Chrome(executable_path=driver_path)
            elif option:
                driver = webdriver.Chrome(chrome_options=option)
            else:
                driver = webdriver.Chrome()
        elif Utils.lower(self.__browser) == "edge":
            # 判断是否指定了浏览器路径
            option = None
            from selenium.webdriver.chrome.options import Options
            if self.__browser_path:
                # 指定浏览器参数
                option = Options()
                option.binary_location = self.__browser_path
            # 配置无需弹出浏览器
            if self.__silent:
                if option is None:
                    option = Options()
                option.add_argument('headless')
            # 如果指定了驱动路径
            driver_path = None
            if self.__driver_path:
                driver_path = self.__driver_path
            # 启动浏览器
            if option and driver_path:
                driver = webdriver.Edge(executable_path=driver_path, options=option)
            elif driver_path:
                driver = webdriver.Edge(executable_path=driver_path)
            elif option:
                driver = webdriver.Edge(options=option)
            else:
                driver = webdriver.Edge()
        else:
            raise MyException("还不支持 {} 浏览器！".format(self.__browser))
        self.__add_method(driver, session)
        self.__driver = driver

    def release_driver(self):
        """
        释放driver
        :return:
        """
        if self.__driver is not None:
            self.__driver.quit()
            self.__driver = None

    def __add_method(self, driver, session: Session):
        """
        增加一些函数
        :param driver:
        :return:
        """

        def sync_cookies():
            """
            同步cookies
            """
            CookiesUtils.merge_requests_to_selenium(session, driver)

        setattr(driver, "sync_cookies", sync_cookies)
