from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from aw_lib.xldriver_lib.xldriver_channelbased_lib.eth_lib.channelbased_eth_rx import ChannelBasedEthRx
from aw_lib.xldriver_lib.xldriver_channelbased_lib.eth_lib.channelbased_eth_tx import ChannelBasedEthTx
from logger import rfic_info


class ChannelBasedEthController(ChannelBasedEthTx, ChannelBasedEthRx):
    def __init__(self):
        super(ChannelBasedEthController, self).__init__()

    def set_bypass_inactive_mode(self, source, target):
        """
            Eth下设置通道的bypass为inactive
        """
        self.deactive_channel(self.ethPortHandle, self.ethAccessMask)
        # 指定哪两个ETH的ByPass
        mask = self.ethAppChannel[source]["accessChannelMask"] | self.ethAppChannel[target]["accessChannelMask"]
        self.eth_set_bypass(self.ethPortHandle, mask, self.ethUserHandle, ChannelBasedConstants.XL_ETH_BYPASS_INACTIVE)
        self.activate_channel(self.ethPortHandle, self.ethAccessMask, self.ethBusType)

    def set_bypass_mac_mode(self, source, target):
        """
            Eth下设置通道的bypass为 mac bypass
        """
        self.deactive_channel(self.ethPortHandle, self.ethAccessMask)
        # 指定哪两个ETH的ByPass
        mask = self.ethAppChannel[source]["accessChannelMask"] | self.ethAppChannel[target]["accessChannelMask"]
        self.eth_set_bypass(self.ethPortHandle, mask, self.ethUserHandle, ChannelBasedConstants.XL_ETH_BYPASS_MACCORE)
        self.activate_channel(self.ethPortHandle, self.ethAccessMask, self.ethBusType)

    def driver_init(self):
        self.open_driver()
        self.set_appl_config(self.ethAppName, self.ethAppChannel, self.ethBusType)
        self.get_channel_mask(self.ethAppName, self.ethAppChannel, self.ethAccessMask, self.ethPermissionMask,
                              self.ethBusType)
        self.open_port(self.ethAppName, self.ethPortHandle, self.ethAccessMask, self.ethPermissionMask, self.ethBusType)

    def channel_setup(self):
        self.set_notification(self.ethPortHandle, self.ethNotificationHandle)
        self.set_bypass_init(self.ethPortHandle, self.ethUserHandle, self.ethAppChannel)  # 默认都设置成MAC BYPASS
        self.activate_channel(self.ethPortHandle, self.ethAccessMask, self.ethBusType)

    def cleanup(self):
        '''
        关闭端口和驱动
        :return:
        '''
        self.deactive_channel(self.ethPortHandle, self.ethAccessMask)
        status = self.dll.xlClosePort(self.ethPortHandle)
        rfic_info("close port:", status)
        status = self.dll.xlCloseDriver()
        rfic_info("close driver:", status)

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
        self.cleanup()
