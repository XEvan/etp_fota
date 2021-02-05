import threading
import time
from ctypes import byref

from scapy.layers.inet import IP, TCP

from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased import ChannelBased, XLDefine
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from aw_lib.xldriver_lib.xldriver_channelbased_lib.message_recorder import MessageRecorder
from aw_lib.xldriver_lib.xldriver_channelbased_lib.structures_rx import T_XL_ETH_EVENT


class ChannelBasedRx(ChannelBased):
    def __init__(self):
        super(ChannelBasedRx, self).__init__()
        self.eth_recv_thread = None

    def terminate_monitor(self):
        '''
        停止监听线程
        :return:
        '''
        try:
            if self.eth_recv_thread:
                self.stop_thread(self.eth_recv_thread)
        except:
            pass
        self.eth_recv_thread = None

    def eth_recv_monitor(self):
        if not self.eth_recv_thread:
            self.eth_recv_thread = threading.Thread(target=self.eth_recv_threading, args=())
            self.eth_recv_thread.start()

    def eth_recv_threading(self):
        receivedEvent = T_XL_ETH_EVENT()
        while True:  # 在时间内判读有没有消息读到
            waitResult = self.net_driver.XL_WaitForSingleObject(self.notificationHandle.value, 1000)
            if waitResult != XLDefine.WaitResults.WAIT_TIMEOUT and waitResult != -1:
                ethReceiveStatus = XLDefine.XL_Status.XL_SUCCESS
                while ethReceiveStatus != XLDefine.XL_Status.XL_ERR_QUEUE_IS_EMPTY:
                    ethReceiveStatus = self.dll.xlEthReceive(self.portHandle,
                                                             byref(receivedEvent))
                    # XL_ERR_QUEUE_IS_EMPTY = 10
                    if ethReceiveStatus == XLDefine.XL_Status.XL_SUCCESS and receivedEvent.tag != 8:
                        if ChannelBasedConstants.XL_ETH_EVENT_TAG_FRAMERX == receivedEvent.tag:
                            self.monitor_data_parse(receivedEvent.tagData.frameRxOk)
                        elif ChannelBasedConstants.T_XL_ETH_DATAFRAME_TXACK == receivedEvent.tag:
                            self.monitor_data_parse(receivedEvent.tagData.frameTxAck)
                        elif ChannelBasedConstants.XL_ETH_EVENT_TAG_FRAMETX_ACK_SWITCH == receivedEvent.tag:
                            self.monitor_data_parse(receivedEvent.tagData.frameTxAckSw)
                        elif ChannelBasedConstants.T_XL_ETH_DATAFRAME_TXACK_OTHERAPP == receivedEvent.tag:
                            self.monitor_data_parse(receivedEvent.tagData.frameTxAckOtherApp)

    def monitor_data_parse(self, obj):
        # get mac
        srcMAC = []
        dstMAC = []  # 目的MAC
        for i in range(6):
            srcMAC.append(obj.sourceMAC[i])
            dstMAC.append(obj.destMAC[i])

        tmp = []
        for i in range(0, obj.dataLen - 1):
            tmp.append(hex(obj.frameData.rawData[i])[2:])
        payload = self.normalize_packet(tmp)
        ethType = payload[:2]
        payload = payload[2:]
        payload = b''.join([bytes().fromhex(i) for i in payload])
        res = IP(payload)

        if res.getlayer(TCP) is None:
            # 没有解析到TCP的数据
            return
        srcIp = res["IP"].src
        dstIp = res["IP"].dst
        proto = res["IP"].proto
        sport = res["TCP"].sport
        dport = res["TCP"].dport
        seq = res["TCP"].seq
        ack = res["TCP"].ack
        flags = int(res["TCP"].flags)
        window = res["TCP"].window
        try:
            raw = res["TCP"].load
        except:
            raw = b''
        payload_len = len(raw)

        MessageRecorder.add(srcIp, dstIp,
                            sport, dport,
                            srcMAC=srcMAC, dstMAC=dstMAC,
                            srcIp=srcIp, dstIp=dstIp,
                            srcPort=sport, dstPort=dport,
                            ethType=ethType,
                            proto=proto,
                            seq=seq,
                            ack=ack,
                            flags=flags,
                            window=window,
                            raw=raw,
                            payload_len=payload_len,
                            timestamp=time.time())

    def normalize_packet(self, value):
        '''
        格式化数据包，不足两位的组成两位
        :param value:数据包
        :return:
        '''
        result = []
        for i in value:
            if len(i) == 1:
                result.append('0%s' % str(i))
            else:
                result.append(str(i))
        return result
