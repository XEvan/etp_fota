from ctypes import byref, c_uint

from aw_lib.xldriver_lib.xldriver_channelbased_lib.can_lib.structures_tx import XLevent
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased import ChannelBased
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from logger import rfic_info


class ChannelBasedCanTx(ChannelBased):
    def __init__(self):
        super(ChannelBasedCanTx, self).__init__()

    def can_send(self, canMask, xlEvent):
        pEventCount = c_uint(1)
        status = self.dll.xlCanTransmit(self.canPortHandle, canMask, byref(pEventCount), byref(xlEvent))
        rfic_info("can transmit:", status)

    def generate_tx_data(self):
        xlEvent = XLevent()

        xlEvent.tag = ChannelBasedConstants.XL_TRANSMIT_MSG
        xlEvent.tagData.msg.id = 0x01
        xlEvent.tagData.msg.dlc = 8
        xlEvent.tagData.msg.flags = 0
        xlEvent.tagData.msg.data[0] = 1
        xlEvent.tagData.msg.data[1] = 2
        xlEvent.tagData.msg.data[2] = 3
        xlEvent.tagData.msg.data[3] = 4
        xlEvent.tagData.msg.data[4] = 5
        xlEvent.tagData.msg.data[5] = 6
        xlEvent.tagData.msg.data[6] = 7
        xlEvent.tagData.msg.data[7] = 8
        return xlEvent
