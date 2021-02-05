from scapy.contrib.automotive.someip import SOMEIP

from app.fota.fota_tester import FotaTester
from aw_lib.xldriver_lib.xldriver_channelbased_lib.message_recorder import MessageRecorder
from common.common import RILPrint
from logger import rfic_info

debug = True


class Test003(FotaTester):
    __func_desc__ = "这是测试用例3"

    def __init__(self, route=""):
        self.route = route

        # 记录过程日志，写入测试报告中
        self.log = []

        # 生成报告
        self.result_dict = self.generate_result_template(self.route, self.__func_desc__)

        # 每条用例执行之前，清空消息流
        MessageRecorder.clear_both()

    @RILPrint
    def setUp(self):
        # VN5640初始化
        rfic_info("初始化VN5640", log=self.log)
        if not debug:
            self.xldriver_handle.reset()
        # 开启消息监测
        rfic_info("开始消息流监听", log=self.log)
        if not debug:
            self.xldriver_handle.eth_recv_monitor()
        # 台架上电
        rfic_info("台架上电", log=self.log)
        return "success"

    @RILPrint
    def run(self):
        src, dst = "device100", "device102"
        # src, dst = "device102", "device100"

        # 等待具体的消息过来后，开始进行消息的仿真发送
        rfic_info("等待指定的ABC消息。。。", log=self.log)
        if not debug:
            status, target_params = self.xldriver_handle.get_required_message(src, dst, 0x0100, 0x3b)
            rfic_info("收到期望消息:", str(target_params), log=self.log)

        rfic_info("断开原始通信链路", log=self.log)
        if not debug:
            self.xldriver_handle.set_bypass_inactive_mode(src, dst)

        rfic_info("开始组包...", log=self.log)
        # 消息仿真与发送  -s
        req_data = ["FE", "FF", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01",
                    "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01",
                    "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01",
                    "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01", "01",
                    "01", "01", "01", "01", "01", "01", "00", "00"]
        matrix = {
            "srv_id": 0x0100,
            "method_id": 0x3b,
            "session_id": 1,
            "msg_type": SOMEIP.TYPE_REQUEST,
            "req_data": req_data
        }
        rfic_info("消息构造:srv_id=%s,method_id=%s" % (hex(matrix["srv_id"]), hex(matrix["method_id"])),
                  log=self.log)
        rfic_info("消息发送指向:%s-->%s" % (src, dst), log=self.log)

        if not debug:
            status = self.xldriver_handle.send_msg_as_method(src, dst, matrix)
            result_msg = "passed" if status else "failed"
            rfic_info("消息发送完成", result_msg, log=self.log)

        rfic_info("打开原始通信链路", log=self.log)
        if not debug:
            self.xldriver_handle.set_bypass_mac_mode(src, dst)
        # 消息仿真与发送  -e

        return "success"

    @RILPrint
    def tearDown(self):
        # 停止消息监测
        rfic_info("停止消息监测", log=self.log)
        # self.xldriver_handle.terminate_monitor()
        # xldriver恢复初始设置
        rfic_info("重置Vn5640", log=self.log)
        # self.xldriver_handle.recovery()
        # 台架下电
        rfic_info("台架下电", log=self.log)

        # 处理测试报告
        self.result_process(self.route, self.result_dict, self.log)

        return "success"
