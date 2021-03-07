#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import time


class Logs(object):

    def __init__(self, class_name=None):
        self.class_name = class_name
        day = time.strftime("%Y-%m-%d_%H")
        file_dir = os.path.dirname(__file__)
        self.mkdir(file_dir+'/LogInfo/')
        file = file_dir + f'/LogInfo/{day}.log'
        self.logger = logging.Logger(self.class_name)
        self.logger.setLevel(logging.INFO)
        self.logfile = logging.FileHandler(file, encoding='utf-8')
        self.logfile.setLevel(logging.INFO)
        self.control = logging.StreamHandler()
        self.control.setLevel(logging.INFO)
        # 去除 - %(name)s
        self.formater = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] >> %(filename)s >> 第%(lineno)d行  - %(message)s ',
            '%Y-%m-%d %H:%M:%S')
        self.logfile.setFormatter(self.formater)
        self.control.setFormatter(self.formater)
        self.logger.addHandler(self.logfile)
        self.logger.addHandler(self.control)

    def mkdir(self,path):

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.isdir(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.mkdir(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False

if __name__ == '__main__':
    l =Logs()
    l.logger.info("11")
