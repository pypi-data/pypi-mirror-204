"""
作者：李俊贤
日期：2023年3月31日
功能：用于命令行的模块
"""
# 使用模块获取命令行参数
import argparse
import logging

from xml_api import *

def main():
    # 读取命令行参数
    parser = argparse.ArgumentParser(description="XML API")
    parser.add_argument("-f", "--filepath",required=True, help="the file to run")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {}".format(version))
    parser.add_argument("-m", "--module",required=False, help="custom py module path")
    parser.add_argument("-l", "--level",required=False,choices=["debug","info","warning","error"], help="log level")
    # 解析命令行参数
    args = parser.parse_args()
    # 取到文件路径
    filepath = args.filepath
    # 如果文件路径不存在，则报错，并结束程序
    if not filepath:
        parser.error("filepath is required")
    # 引入执行器
    executor = XMLAPIExecutor(filepath)
    # 如果存在模块，则导入
    if args.module:
        executor.add_py_module(args.module)
    # 如果存在日志等级，则设置日志等级
    if args.level:
        # 设置日志等级
        # 根据输入进行日志等级的设置
        if args.level == "debug":
            executor.enable_console_log(level=logging.DEBUG)
        elif args.level == "info":
            executor.enable_console_log(level=logging.INFO)
        elif args.level == "warning":
            executor.enable_console_log(level=logging.WARNING)
        elif args.level == "error":
            executor.enable_console_log(level=logging.ERROR)
        else:
            parser.error("level is invalid")
    else:
        executor.enable_console_log()
    # 执行
    executor.run()
    executor.wait()
