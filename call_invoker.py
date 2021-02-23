import datetime
import os
import traceback

from common.constants import Constants
from load_app import load_modules_from_path
from logger import rfic_info, rfic_error
from reporter import Reporter


class CallInvoker:
    def __init__(self):
        # 显示logo信息
        self.show_logo()

    def show_logo(self):
        with open("logo.info") as f:
            data = f.readlines()
        for line in data:
            rfic_info(line.replace("\n", ""))

    def call(self, route, params, description):
        """
        远程调用的接口
        """
        from rpc_package.callinvoker_pb2 import CallResponse
        if hasattr(self, route):
            new_func = getattr(self, route)
            new_func(params)

            return CallResponse(status="Pass", value="", message="")
        else:
            return CallResponse(status="Fail", value="", message="没有找到测试用例!")

    def run(self, params=None):
        """
        远程调用主要调度
        """
        # self.start()
        test_case_dict = load_modules_from_path()
        class_item = test_case_dict[params]["class_item"](params)  # 实例化用例
        class_item.setUp()  # 一条用例初始设置
        class_item.run()  # 一条用例主逻辑
        class_item.tearDown()  # 一条用例执行完
        # self.stop()

    def start(self, params=None):
        # 所有用例开始执行之前的初始化动作
        rfic_info("开始执行测试用例...")

        # 生成测试报告文件夹  -s
        Constants.REPORT_DIR = os.path.join(Constants.REPORT_BASE_DIR,
                                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        if not os.path.exists(Constants.REPORT_DIR):
            os.makedirs(Constants.REPORT_DIR)
        # 生成测试报告文件夹  -e

    def main(self, test_case_dict=None):
        """
        主要调度逻辑：
            step1：start() 所有测试用例执行之前调用一次
            step2：遍历界面上选中的测试用例
                sub_step1：setUp() 单条用例初始化
                sub_step2：run() 单条用例主逻辑
                sub_step3：tearDown() 单条用例收尾操作
                sub_step4：result_process() 单条用例测试报告处理
            step3：stop() 所有测试用例执行完成后调用一次
        """

        # 所有测试用例执行之前执行一次，比如初始化测试报告的路径
        self.start()

        # 动态加载现有的测试用例  -s
        if test_case_dict is None:  # 如果没有传用例，默认加载全部用例进行执行(调试使用)
            test_case_dict = load_modules_from_path()
        for route, item in test_case_dict.items():
            class_item = item["class_item"](route)  # 实例化用例
            try:
                class_item.setUp()  # 一条用例的初始化
                class_item.run()  # 一条用例的主逻辑
                class_item.tearDown()  # 一条用例的收尾
                class_item.reporter.result_process()  # 一条用例执行完成后，生成一下该用例的报告
            except:
                rfic_error("[%s]执行失败!\n失败原因:%s" % (str(route), str(traceback.format_exc())))  # 会记录到测试报告中
                class_item.reporter.set_test_status(False)  # 当前用例失败
                class_item.reporter.result_process()  # 一条用例执行完成后，生成一下该用例的报告
        # 动态加载现有的测试用例  -e

        # 所有测试用例执行完成后执行一次，比如生成测试报告
        self.stop()

    def stop(self, params=None):
        # 所有用例执行完成后执行的动作
        rfic_info("测试用例执行完成...")
        Reporter.generate_html()  # 汇总每条测试用例生成的json文件，最终生成html测试报告
