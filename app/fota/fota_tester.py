import json
import os
import time

from app.app import App
from aw_lib.aw_manager import AwManager
from aw_lib.xldriver_lib.xldriver_channelbased_lib.message_recorder import MessageRecorder
from common.constants import Constants


class FotaTester(App):
    # 调用VN5640的驱动
    xldriver_handle = AwManager.xldriver_channelbased_manager

    def __init__(self, route="", desc=""):
        self.route = route  # 测试用例的路径信息
        # 初始化报告内容
        Constants.EACH_CASE_LOG.clear()
        self.result_dict = self.generate_result_template(route, desc)

        # 每条用例执行之前，清空消息流
        MessageRecorder.clear_both()

    def setUp(self):
        pass

    def run(self):
        pass

    def tearDown(self):
        pass

    def generate_result_template(self, route, func_desc):
        '''
        初始化测试报告模板
        '''
        result_dict = {
            "className": route,
            "methodName": "test_main",
            "description": func_desc,
            "startTime": time.time(),
            "spendTime": 0,
            "status": True,
            "log": []
        }
        return result_dict

    def result_process(self, result_dict):
        '''
        报告的后处理
        '''
        result_dict["log"] = Constants.EACH_CASE_LOG  # 该信息会显示在html测试报告中
        result_dict["spendTime"] = str(round(time.time() - result_dict["startTime"], 3)) + " s"
        result_dict["status"] = "成功" if result_dict["status"] == True else "失败"
        report_name = os.path.join(Constants.REPORT_DIR, "%s.json" % str(self.route))
        with open(report_name, "w") as dump_f:
            json.dump(result_dict, dump_f)
