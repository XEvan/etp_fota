from app.app import App
from aw_lib.aw_manager import AwManager
from aw_lib.xldriver_lib.xldriver_channelbased_lib.message_recorder import MessageRecorder
from common.constants import Constants
from reporter import Reporter


class FotaTester(App):
    # 调用VN5640的驱动
    xldriver_handle = AwManager.xldriver_channelbased_manager

    def __init__(self, route="", desc=""):
        self.reporter = Reporter(route, desc)  # 实例化报告类
        Constants.EACH_CASE_LOG.clear()  # 每条测试用例之前，清空测试过程信息
        MessageRecorder.clear_both()  # 每条用例执行之前，清空消息流

    def setUp(self):
        pass

    def run(self):
        pass

    def tearDown(self):
        pass
