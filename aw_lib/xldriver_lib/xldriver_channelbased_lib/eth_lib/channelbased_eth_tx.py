import time
from ctypes import byref, c_ushort

from scapy.contrib.automotive.someip import SOMEIP
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Dot1Q
from scapy.utils import hexdump

from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased import ChannelBased, XLDefine
from aw_lib.xldriver_lib.xldriver_channelbased_lib.message_recorder import MessageRecorder
from aw_lib.xldriver_lib.xldriver_channelbased_lib.eth_lib.structures_tx import T_XL_ETH_DATAFRAME_TX
from logger import rfic_info


class ChannelBasedEthTx(ChannelBased):
    def __init__(self):
        super(ChannelBasedEthTx, self).__init__()

    def get_required_message(self, source, target, service_id, method_id):
        '''
        检索期望消息
        '''
        srcIP = self.ethAppChannel[source]["ip"]
        srcPort = self.ethAppChannel[source]["port"]
        dstIP = self.ethAppChannel[target]["ip"]
        dstPort = self.ethAppChannel[target]["port"]
        while True:
            try:
                msg_list = MessageRecorder.get_tmp_message_list((srcIP, dstIP, srcPort, dstPort))
                for msg in msg_list[::-1]:
                    target_params = msg  # 只关注最后一条
                    try:
                        raw = SOMEIP(target_params['raw'])
                        # raw.show()
                        msg_service_id = raw.srv_id
                        msg_method_id = raw.method_id
                        if msg_service_id == service_id and msg_method_id == method_id:
                            rfic_info("检索到期望消息", target_params)
                            MessageRecorder.clear_tmp_message_list() # 清空临时消息，缩短消息检索时间
                            time.sleep(0.03) # 等待消息流程完成
                            return True, target_params
                    except:
                        pass
            except:
                pass
            # time.sleep(0.5) # 等待接收到下一条消息

    def send_msg_as_method(self, source, target, matrix):
        '''
        发送(TCP)method消息，需要等待对端回复
            A->B:PSH+ACK
            B->A:PSH+ACK
            A->B:ACK
        :param source: 源ECU
        :param target: 目的ECU
        :param matrix: 通信矩阵，包含service_id,method_id,msg_type
        :return:
        '''

        # 监听本端给对端发的ACK消息
        srcIP = self.ethAppChannel[source]["ip"]
        srcPort = self.ethAppChannel[source]["port"]
        dstIP = self.ethAppChannel[target]["ip"]
        dstPort = self.ethAppChannel[target]["port"]
        msg_list = MessageRecorder.get_message_list((srcIP, dstIP, srcPort, dstPort))
        while len(msg_list) == 0:
            msg_list = MessageRecorder.get_message_list((srcIP, dstIP, srcPort, dstPort))
        target_params = msg_list[-1]  # 只关注最后一条

        # 本端发送PSH+ACK消息
        tx_data = self.generate_tx_data(target_params, "PA", matrix)
        self.eth_send(target, tx_data)

        # 监听对端给本端发的PSH+ACK消息
        msg_list = MessageRecorder.get_message_list((dstIP, srcIP, dstPort, srcPort))
        while len(msg_list) == 0:  # 没有消息的时候，不停的收
            msg_list = MessageRecorder.get_message_list((dstIP, srcIP, dstPort, srcPort))
        target_params = msg_list[-1]  # 只关注最后一条
        raw_info = SOMEIP(target_params['raw']).show(dump=True)
        rfic_info(raw_info)

        # 本端发送ACK消息
        tx_data = self.generate_tx_data(target_params, "A")
        return self.eth_send(target, tx_data)

    def eth_send(self, target, txData):
        ethSendStatus = self.dll.xlEthTransmit(self.ethPortHandle, self.ethAppChannel[target]["accessChannelMask"],
                                               self.ethUserHandle, byref(txData))
        rfic_info("xlEthTransmit:%s" % ethSendStatus)
        time.sleep(0.05)  # 报文发送之后，等待对端响应response
        if ethSendStatus == 0:
            return True
        else:
            return False

    def generate_tx_data(self, target_params, flags="PA", matrix=None):
        rfic_info(target_params)
        txData = T_XL_ETH_DATAFRAME_TX()
        if flags == "PA":
            srcIp = target_params["srcIp"]  # 本端：'192.168.0.101'
            dstIp = target_params["dstIp"]  # 对端：'192.168.0.100'
            srcPort = target_params["srcPort"]
            dstPort = target_params["dstPort"]
            window = target_params["window"]
            seq = target_params["seq"]
            ack = target_params["ack"]
            srcMAC = target_params["srcMAC"]
            dstMAC = target_params["dstMAC"]
        elif flags == "A":
            srcIp = target_params["dstIp"]  # 本端：'192.168.0.101'
            dstIp = target_params["srcIp"]  # 对端：'192.168.0.100'
            srcPort = target_params["dstPort"]
            dstPort = target_params["srcPort"]
            window = target_params["window"]
            seq = target_params["ack"]
            ack = target_params["seq"] + target_params["payload_len"]
            srcMAC = target_params["dstMAC"]
            dstMAC = target_params["srcMAC"]
        else:
            srcIp = target_params["srcIp"]  # 本端：'192.168.0.101'
            dstIp = target_params["dstIp"]  # 对端：'192.168.0.100'
            srcPort = target_params["srcPort"]
            dstPort = target_params["dstPort"]
            window = target_params["window"]
            seq = target_params["seq"]
            ack = target_params["ack"]
            srcMAC = target_params["srcMAC"]
            dstMAC = target_params["dstMAC"]

        for i in range(len(srcMAC)):
            txData.sourceMAC[i] = srcMAC[i]
            txData.destMAC[i] = dstMAC[i]

        txData.frameIdentifier = 0
        txData.flags = XLDefine.XLethernet_TX_Flags.XL_ETH_DATAFRAME_FLAGS_USE_SOURCE_MAC

        payload_length, combine_payload = self.generate_someip_based_tcp(srcIp, dstIp,
                                                                         srcPort, dstPort,
                                                                         seq, ack, flags,
                                                                         matrix)
        txData.dataLen = payload_length + 2  # min. 46 bytes + 2 bytes for etherType
        if txData.dataLen < 46:
            txData.dataLen = 46 + 2  # 数据位长度最小是 46+2

        eth_tp_v = self.host2network_order(0x0800)  # 本地字节序转成网络字节序 IPv4
        ethTp = c_ushort()
        ethTp.value = int(eth_tp_v, 16)
        txData.frameData.ethFrame.etherType = ethTp.value  # 设置字节序的类型

        for i in range(len(combine_payload)):
            txData.frameData.ethFrame.payload[i] = int(combine_payload[i], 16)

        return txData

    def generate_someip_based_tcp(self, s_ip, d_ip, s_port, d_port, seq=2496318543, ack=594476641, flags="PA",
                                  matrix=None):
        vlan = Dot1Q(vlan=4)
        ip = IP(src=s_ip, dst=d_ip)

        tcp = TCP(flags=flags, sport=s_port, dport=d_port, seq=seq, ack=ack)
        if flags == "PA":  # PSH+ACK
            if matrix is None:
                matrix = {}
            srv_id = matrix.get("srv_id", 0xffff)
            method_id = matrix.get("method_id", 65535)
            session_id = matrix.get("session_id", 1)
            msg_type = matrix.get("msg_type", SOMEIP.TYPE_NOTIFICATION)
            req_data = matrix.get("req_data", [])
            someip = SOMEIP(srv_id=srv_id, sub_id=0x0,
                            method_id=method_id, event_id=0,
                            client_id=method_id, session_id=session_id,
                            msg_type=msg_type)
            packet = b''.join([bytes().fromhex(i) for i in req_data])
            target = ip / tcp / someip / packet
        elif flags == "A":  # ACK
            target = ip / tcp
        else:
            target = ip / tcp

        payload_length = len(target)
        hex_target = hexdump(target, True)
        results = hex_target.split("\n")
        finalResult = []
        for item in results:
            finalResult.append(item.split("  ")[1])
        x = " ".join(finalResult)
        x_list = x.split(" ")
        return payload_length, x_list
