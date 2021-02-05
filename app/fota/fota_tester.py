import json
import os
import time

from aw_lib.aw_manager import AwManager
from common.constants import Constants


class FotaTester:
    # 调用VN5640的驱动
    xldriver_handle = AwManager.xldriver_channelbased_manager

    def setUp(self):
        pass

    def run(self):
        pass

    def tearDown(self):
        pass

    def generate_result_template(self, route, func_desc):
        '''
        生成测试报告模板
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

    def result_process(self, route, result_dict):
        '''
        报告后处理
        '''
        result_dict["log"] = Constants.EACH_CASE_LOG
        result_dict["spendTime"] = str(round(time.time() - result_dict["startTime"], 3)) + " s"
        result_dict["status"] = "成功" if result_dict["status"] == True else "失败"
        report_name = os.path.join(Constants.REPORT_DIR, "%s.json" % route)
        with open(report_name, "w") as dump_f:
            json.dump(result_dict, dump_f)