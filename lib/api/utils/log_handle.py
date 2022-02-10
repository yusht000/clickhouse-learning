#!/usr/bin/env python3
# coding: utf-8

import logging
from config.setting import LOG_INFO


PATH = LOG_INFO.get("PATH")
ERROR_PATH = LOG_INFO.get("ERROR_PATH")

logger = logging.getLogger(
    LOG_INFO.get("NAME")
)

logger.setLevel(LOG_INFO.get("LEVEL"))


_logFormat = logging.Formatter(
    '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "process": "%(process)d", "funcname": "%(funcName)s", "filename": "%(filename)s", "msg": "%(message)s"}',
     datefmt='%Y-%m-%d %H:%M:%S'
)


_logFileHandler = logging.FileHandler(
    PATH,
    encoding="utf-8"
)


_logFileHandler.setLevel(logging.INFO)
_logFileHandler.setFormatter(_logFormat)
logger.addHandler(_logFileHandler)



_logErrorFileHandler = logging.FileHandler(
    ERROR_PATH,
    encoding='utf-8'
)

_logErrorFileHandler.setLevel(logging.ERROR)
_logErrorFileHandler.setFormatter(_logFormat)
logger.addHandler(_logErrorFileHandler)






if __name__ == '__main__':



    logger = logging.getLogger('api')
    # logger.setLevel(logging.DEBUG)
    #
    # rf_handler = logging.handlers.TimedRotatingFileHandler('/Users/bairong/tmp/all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    #
    # rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    #
    #
    # f_handler = logging.FileHandler('/Users/bairong/tmp/test.log')
    # f_handler.setLevel(logging.ERROR)
    # f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    #
    #
    # logger.addHandler(rf_handler)
    # logger.addHandler(f_handler)
    #
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')











