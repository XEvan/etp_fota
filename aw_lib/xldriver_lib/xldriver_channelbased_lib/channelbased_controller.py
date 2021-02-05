import time

from scapy.contrib.automotive.someip import SOMEIP

from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_rx import ChannelBasedRx
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_tx import ChannelBasedTx


class ChannelBasedController(ChannelBasedTx, ChannelBasedRx):
    def __init__(self):
        super(ChannelBasedController, self).__init__()

    def reset(self):
        '''
        初始化：两个步骤是连着的，固定的
        :return:
        '''
        self.driver_init()
        self.channel_setup()

    def recovery(self):
        '''
        恢复初始设置：关闭端口和驱动
        :return:
        '''
        self.close_port_and_driver()

    def run(self):
        self.reset()
        self.eth_recv_monitor()

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

        src, dst = "device100", "device102"
        # src, dst = "device102", "device100"

        time.sleep(10)
        self.set_bypass(src, dst, ChannelBasedConstants.XL_ETH_BYPASS_INACTIVE)
        for i in range(5):
            self.send_msg_as_method(src, dst, matrix)
            time.sleep(5)
        time.sleep(10)

        self.set_bypass(src, dst, ChannelBasedConstants.XL_ETH_BYPASS_MACCORE)

        # 停止监听线程
        self.terminate_monitor()
