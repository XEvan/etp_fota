from aw_lib.xldriver_lib.xldriver_channelbased_lib.can_lib.channelbased_can_tx import ChannelBasedCanTx


class ChannelBasedCanController(ChannelBasedCanTx):
    def __init__(self):
        super(ChannelBasedCanController, self).__init__()

    def driver_init(self):
        self.open_driver()
        self.set_appl_config(self.canAppName, self.canAppChannel, self.canBusType)
        self.get_channel_mask(self.canAppName, self.canAppChannel, self.canAccessMask, self.canPermissionMask,
                              self.canBusType)
        self.open_port(self.canAppName, self.canPortHandle, self.canAccessMask, self.canPermissionMask, self.canBusType)

    def channel_setup(self):
        """
            with init access(access_mask=permission_mask):
                ①channel parameters can be changed/configured
                ②CAN messages can be transmitted on the channel
                ③CAN messages can be received on the channel

            without init access(access_mask!=permission_mask):
                ①CAN messages can be transmitted on the channel
                ②CAN messages can be received on the channel
        """
        if self.canAccessMask.value == self.canPermissionMask.value:
            print("with init access")
            self.set_can_channel_bitrate(self.canPortHandle, self.canAccessMask, 500000)
        else:
            print("without init access")

        self.set_notification(self.canPortHandle, self.canNotificationHandle)
        self.activate_channel(self.canPortHandle, self.canAccessMask, self.canBusType)

    def reset(self):
        '''
        初始化
        :return:
        '''

        self.driver_init()
        self.channel_setup()