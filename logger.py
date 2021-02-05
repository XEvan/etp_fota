import datetime
import logging
import os
import traceback

from common.common import Singleton
from common.constants import Constants


class Logger(metaclass=Singleton):
    def __init__(self, loggername):
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        if not os.path.exists(Constants.LOG_BASE_DIR):
            os.makedirs(Constants.LOG_BASE_DIR)
        logname = os.path.join(Constants.LOG_BASE_DIR, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log'))
        fh = logging.FileHandler(logname, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.DEBUG)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger


logger = Logger("OTA").get_log()


def rfic_info(*args, **kwargs):
    pstr = ""
    for item in args[:-1]:
        pstr += str(item) + " "
    pstr += str(args[-1])
    logger.debug(pstr)
    # 如果kwargs里面有log参数，那么把日志追加到log中
    try:
        log = kwargs.get("log")
        if isinstance(log, list):
            log.append(pstr)
    except:
        pass
    return pstr


def rfic_error(*args, **kwargs):
    pstr = ""
    for item in args[:-1]:
        pstr += str(item) + " "
    pstr += str(args[-1])
    logger.error(pstr)
    # 如果kwargs里面有log参数，那么把日志追加到log中
    try:
        log = kwargs.get("log")
        if isinstance(log, list):
            # 在错误信息前面添加红色的[Error!!!]标记
            log.append("<span style='color:red;'>[Error!!!]</span>" + pstr)
    except Exception as e:
        traceback.print_exc()
        pass
    return pstr
