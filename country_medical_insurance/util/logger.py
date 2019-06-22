# -*- coding: utf-8 -*-
import logging
import os
import datetime


class Log(object):
    def __init__(self, logName):
        self.logger = logging.getLogger(logName)
        self.logger.setLevel(logging.DEBUG)
        time = datetime.datetime.now()
        logFilePath = os.path.abspath('../log/') + '/{}-{}-{}'.format(time.year, time.month, time.day)
        self.check_mkdir(logFilePath)
        logFile = logFilePath + '/out.log'
        formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')
        loghanlder = logging.FileHandler(logFile, encoding='utf-8')  # encoding要申明下，不然中文写入中文文件会乱码
        loghanlder.setFormatter(formatter)
        loghanlder.setLevel(logging.DEBUG)
        logSt = logging.StreamHandler()
        logSt.setFormatter(formatter)
        self.logger.addHandler(loghanlder)
        self.logger.addHandler(logSt)

    def debug(self, msg):
        self.logger.debug(msg)

    def check_mkdir(self, logFilePath):
        if not os.path.exists(logFilePath):
            os.makedirs(logFilePath)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warn(self, msg):
        self.logger.warning(msg)

