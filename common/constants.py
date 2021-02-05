import os
import sys


class Constants:
    BASE_DIR = os.path.split(os.path.abspath(sys.argv[0]))[0]
    REPORT_DIR = None  # 生成的json文件保存路径
    REPORT_BASE_DIR = os.path.join(BASE_DIR, "report_json")  # 保存json目录的路径
    REPORT_HTML_PATH = os.path.join(BASE_DIR, "report_html") # 生成最终报告的路径
    CASES = {}
    LOG_BASE_DIR = os.path.join(BASE_DIR, "ept_logs")

    EACH_CASE_LOG = [] # 记录每一条测试用例的日志信息
