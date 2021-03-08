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
        self.mkdir(file_dir + '/LogInfo/')
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

    def mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断目录是否存在
        isExists = os.path.isdir(path)

        if not isExists:
            # 如果不存在则创建目录
            os.mkdir(path)
        else:
            pass


if __name__ == '__main__':
    l = Logs()
    l.logger.info("11")
