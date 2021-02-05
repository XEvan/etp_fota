import datetime
import logging
import os

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

log_mapping = {
    "info": logger.info,
    "debug": logger.debug,
    "error": logger.error
}
'''
    info:默认会添加到测试报告中，也会记录到本地日志文件中
    debug:不会添加到测试报告中，但是会记录到本地日志文件中
    error:会添加到测试报告中，也会记录到本地日志文件中
'''


def rfic_base(level, *args, **kwargs):
    pstr = ""
    for item in args[:-1]:
        pstr += str(item) + " "
    pstr += str(args[-1])

    log_mapping.get(level)(pstr)
    if level == "error":
        pstr = "<span style='color:red;'>[Error!!!]</span>" + pstr

    # 如果kwargs里面有log参数，那么把日志追加到log中  -s
    try:
        # 获取有没有log标记
        # 1、如果log是个列表，那么追加到该列表中
        # 2、如果log是个False，那么不追加
        # 3、如果是其他情况，比如没有传log参数，那么自动会追加到列表中
        log = kwargs.get("log")
        if isinstance(log, list):  # 如果log=[]，就添加到列表中
            log.append(pstr)
        elif log == False:  # 如果log=True，就添加到一个全局日志记录列表中
            pass
        else:  # 默认自动添加
            if level != "debug":
                Constants.EACH_CASE_LOG.append(pstr)
    except:
        pass
    # 如果kwargs里面有log参数，那么把日志追加到log中  -e
    return pstr


def rfic_info(*args, **kwargs):
    return rfic_base("info", *args, **kwargs)


def rfic_debug(*args, **kwargs):
    return rfic_base("debug", *args, **kwargs)


def rfic_error(*args, **kwargs):
    return rfic_base("error", *args, **kwargs)
