from aw_lib.xldriver_lib.xldriver_channelbased_lib.can_lib.channelbased_can_controller import ChannelBasedCanController

can = ChannelBasedCanController()
can.driver_init()
can.channel_setup()