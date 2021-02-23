import datetime
import json
import os
import shutil
import time

from jinja2 import Environment, FileSystemLoader

from common.constants import Constants


class Reporter:
    def __init__(self, route, func_desc):
        self.route = route
        self.result_dict = {
            "className": route,
            "methodName": "test_main",
            "description": func_desc,
            "startTime": time.time(),
            "spendTime": 0,
            "status": True,
            "log": []
        }

    def set_test_status(self, status=True):
        '''
        设置测试成功或者失败，默认成功
        '''
        self.result_dict["status"] = status

    def result_process(self):
        '''
        单个测试数据的后处理
        '''
        self.result_dict["log"] = Constants.EACH_CASE_LOG  # 该信息会显示在html测试报告中
        self.result_dict["spendTime"] = str(round(time.time() - self.result_dict["startTime"], 3)) + " s"
        self.result_dict["status"] = "成功" if self.result_dict["status"] == True else "失败"
        report_name = os.path.join(Constants.REPORT_DIR, "%s.json" % str(self.route))
        with open(report_name, "w") as dump_f:
            json.dump(self.result_dict, dump_f)

    @staticmethod
    def generate_html():
        """
        汇总每条测试用例生成的json文件，最终生成html测试报告
        """
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
        os.startfile(finalPath)  # 打开生成的最终报告目录
