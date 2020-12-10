#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhangjun
# @Date  : 2018/7/26 9:21
# @Desc  : Description
# import logging
from config import Logs
# logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logger = Logs.logs()
    logger.info("this is infoasdadas")
    logger.debug("this is debug")
    logger.error("this is error")
    logger.warning("this is warning")