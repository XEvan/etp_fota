import copy

from common.common import Singleton


class MessageRecorder(metaclass=Singleton):
    '''
    监听消息记录器，全局唯一(使用单例模式)
    '''
    msg_dict = {}  # 消息存储
    msg_dict_tmp = {}  # 临时消息存储，可能会不定时被清空

    @staticmethod
    def add(srcIP, dstIP, sport, dport, **kwargs):
        key = (srcIP, dstIP, sport, dport)
        record = MessageRecorder.msg_dict.get(key)
        if record is None:
            MessageRecorder.msg_dict[key] = []
        if kwargs not in MessageRecorder.msg_dict[key]:
            MessageRecorder.msg_dict[key].append(kwargs)
            # rfic_info("监测到新消息:", key, kwargs)
            MessageRecorder.msg_dict_tmp = copy.deepcopy(MessageRecorder.msg_dict)  # 拷贝到临时字典中

    @staticmethod
    def get_tmp_message_list(key):
        # print(key, MessageRecorder.msg_dict_tmp.get(key, []))
        return MessageRecorder.msg_dict_tmp.get(key, [])

    @staticmethod
    def get_message_list(key):
        # print(key, MessageRecorder.msg_dict_tmp.get(key, []))
        return MessageRecorder.msg_dict.get(key, [])

    @staticmethod
    def clear_tmp_message_list():
        # 清除临时消息存储
        MessageRecorder.msg_dict_tmp.clear()

    @staticmethod
    def clear_serious():
        # 清除所有内存消息
        MessageRecorder.msg_dict.clear()

    @staticmethod
    def clear_both():
        # 清除临时内存消息和所有内存消息
        MessageRecorder.msg_dict_tmp.clear()
        MessageRecorder.msg_dict.clear()
