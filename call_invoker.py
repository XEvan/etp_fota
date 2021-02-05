import datetime
import json
import os
import shutil
import time
from functools import partial

from jinja2 import Environment, FileSystemLoader

from common.constants import Constants
from load_app import get_totest_classes
from logger import rfic_info
from rpc_package.callinvoker_pb2 import CallResponse


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
        if hasattr(self, route):
            new_func = getattr(self, route)
            new_func(params)

            return CallResponse(status="Pass", value="", message="")
        else:
            return CallResponse(status="Fail", value="", message="没有找到测试用例!")

    def start(self, params=None):
        # 所有用例开始执行之前的初始化动作
        rfic_info("开始执行测试用例...")

        # 生成测试报告文件夹  -s
        Constants.REPORT_DIR = os.path.join(Constants.REPORT_BASE_DIR,
                                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        if not os.path.exists(Constants.REPORT_DIR):
            os.makedirs(Constants.REPORT_DIR)
        # 生成测试报告文件夹  -e

    def run(self, params=None):
        '''
        远程调用主要调度
        '''

        # self.start()
        test_case_dict = get_totest_classes()
        class_item = test_case_dict[params]["class_item"](params)  # 实例化用例
        class_item.setUp()  # 一条用例初始设置
        class_item.run()  # 一条用例主逻辑
        class_item.tearDown()  # 一条用例执行完
        # self.stop()

    def main(self, test_case_dict=None):
        '''
        主要调度
        '''

        self.start()

        # 动态加载现有的测试用例
        if test_case_dict is None:
            test_case_dict = get_totest_classes()
        for route, item in test_case_dict.items():
            class_item = item["class_item"](route)  # 实例化用例
            class_item.setUp()  # 一条用例初始设置
            class_item.run()  # 一条用例主逻辑
            class_item.tearDown()  # 一条用例执行完

        self.stop()

    def stop(self, params=None):
        # 所有用例执行完成后执行的动作
        rfic_info("测试用例执行完成...")
        self.generate_html()

    def generate_html(self):
        env = Environment(loader=FileSystemLoader(os.path.join(Constants.BASE_DIR, 'template')))  # 加载模板
        template = env.get_template('report_template.html')

        report_names = os.listdir(Constants.REPORT_DIR)

        testFail = 0  # 失败数
        testPass = 0  # 成功数
        spendTime = 0  # 耗时
        testResult = []
        startTime = []
        for file in report_names:
            file_path = os.path.join(Constants.REPORT_DIR, file)
            with open(file_path, "r", encoding="utf-8") as load_f:
                data = json.load(load_f)

                startTime.append(data.get("startTime", 0))

                st = data.get("spendTime", "0.0 s")
                if "s" in str(st):
                    spendTime += float(st.split(" ")[0])
                else:
                    spendTime += float(st)
                testResult.append(data)
                if "失败" in data.get("status"):
                    testFail += 1
                if "成功" in data.get("status"):
                    testPass += 1

        startTime = [0] if len(startTime) == 0 else startTime
        startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(min(startTime)))
        testAll = len(report_names)

        # 新建一个时间文件夹  -s
        folder = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        finalPath = os.path.join(Constants.REPORT_HTML_PATH, folder)
        # if not os.path.exists(finalPath):
        #     os.makedirs(finalPath)
        # 新建一个时间文件夹  -e
        # 拷贝css和js文件  -s
        if not os.path.exists(finalPath):
            # 如果目标路径不存在原文件夹的话就拷贝
            shutil.copytree(os.path.join(Constants.BASE_DIR, "template", "templates"), finalPath)
        # 拷贝css和js文件  -e

        report_path = os.path.join(finalPath, "index.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            context = {
                "title": "OTA测试报告",
                "spendTime": spendTime,
                "startTime": startTime,
                "testAll": testAll,
                "testPass": testPass,
                "testFail": testFail,
                "testResult": testResult
            }

            html_content = template.render(context)
            f.write(html_content)
        os.startfile(finalPath)