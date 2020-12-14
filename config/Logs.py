#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import time


class logs(object):

    def __init__(self, class_name=None):
        self.class_name = class_name
        day = time.strftime("%Y-%m-%d_%H")
        file_dir = os.path.dirname(__file__)
        file = file_dir + f'/logs2/{day}.log'
        self.logger = logging.Logger(self.class_name)
        self.logger.setLevel(logging.INFO)
        self.logfile = logging.FileHandler(file, encoding='utf-8')
        self.logfile.setLevel(logging.INFO)
        self.control = logging.StreamHandler()
        self.control.setLevel(logging.INFO)
        self.formater = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] >> %(filename)s >> 第%(lineno)d行 - %(name)s - %(message)s ',
            '%Y-%m-%d %H:%M:%S')
        self.logfile.setFormatter(self.formater)
        self.control.setFormatter(self.formater)
        self.logger.addHandler(self.logfile)
        self.logger.addHandler(self.control)