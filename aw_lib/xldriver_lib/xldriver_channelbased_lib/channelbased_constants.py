class ChannelBasedConstants:
    XL_HWTYPE_VN5640 = 89
    VN5640_1 = 0
    ETHERNET_SEGMENT_1 = 0
    ETHERNET_SEGMENT_2 = 1
    ETHERNET_SEGMENT_3 = 2
    ETHERNET_SEGMENT_4 = 3
    ETHERNET_SEGMENT_5 = 4
    ETHERNET_SEGMENT_6 = 5
    ETHERNET_SEGMENT_7 = 6
    ETHERNET_SEGMENT_8 = 7
    ETHERNET_SEGMENT_9 = 8

    XL_INTERFACE_VERSION_V4 = 4
    XL_BUS_TYPE_ETHERNET = 0x00001000
    XL_BUS_TYPE_CAN = 0x00000001

    XL_ETH_BYPASS_INACTIVE = 0
    XL_ETH_BYPASS_PHY = 1
    XL_ETH_BYPASS_MACCORE = 2

    XL_ETH_EVENT_TAG_FRAMERX = 0x0500  # 1280
    T_XL_ETH_DATAFRAME_TXACK = 0x0510  # 1296
    XL_ETH_EVENT_TAG_FRAMETX_ACK_SWITCH = 0x0511  # 1297
    T_XL_ETH_DATAFRAME_TXACK_OTHERAPP = 0x0513  # 1299

    XL_OUTPUT_MODE_SILENT = 0  # switch CAN trx into default silent mode
    XL_OUTPUT_MODE_NORMAL = 1  # switch CAN trx into normal mode
    XL_OUTPUT_MODE_TX_OFF = 2  # switch CAN trx into silent mode with tx pin off
    XL_OUTPUT_MODE_SJA_1000_SILENT = 3  # switch CAN trx into SJA1000 silent mode

    # ##################transceiver type  -s
    # Lowspeed (252/1053/1054)
    XL_TRANSCEIVER_TYPE_CAN_251 = 0x0001
    XL_TRANSCEIVER_TYPE_CAN_252 = 0x0002
    # Highspeed (1041 and 1041opto)
    XL_TRANSCEIVER_TYPE_CAN_1041 = 0x0010  # 1041
    XL_TRANSCEIVER_TYPE_CAN_1041_OPTO = 0x0011  # 1041 with optical isolation
    # Single Wire (AU5790)
    XL_TRANSCEIVER_TYPE_CAN_SWC = 0x0006  # single wire
    XL_TRANSCEIVER_TYPE_CAN_SWC_OPTO = 0x000C  # single wire, SWC with optical isolation
    XL_TRANSCEIVER_TYPE_CAN_SWC_PROTO = 0x0005  # single wire, Prototype. Driver may latch-up.
    # Truck & Trailer
    XL_TRANSCEIVER_TYPE_CAN_B10011S = 0x000D  # B10011S truck-and-trailer
    XL_TRANSCEIVER_TYPE_PB_CAN_TT_OPTO = 0x0119
    # ##################transceiver type  -e

    # ##################line mode  -e
    # Lowspeed (252/1053/1054)
    XL_TRANSCEIVER_LINEMODE_SLEEP = 0x0008  # Puts CANcab into sleep mode.
    XL_TRANSCEIVER_LINEMODE_NORMAL = 0x0009  # Enables normal operation.
    # Single Wire (AU5790)
    XL_TRANSCEIVER_LINEMODE_SWC_WAKEUP = 0x0007  # Enables the sending of high voltage messages (used to wake up sleeping nodes on the bus).
    XL_TRANSCEIVER_LINEMODE_SWC_SLEEP = 0x0004  # Switches to sleep mode.
    XL_TRANSCEIVER_LINEMODE_SWC_NORMAL = 0x0005  # Switches to normal operation.
    XL_TRANSCEIVER_LINEMODE_SWC_FAST = 0x0006  # Switches transceiver to fast mode.
    # Truck & Trailer
    XL_TRANSCEIVER_LINEMODE_TT_CAN_H = 0x000b  # Switches the transceiver to one-wire-mode on CAN High.
    XL_TRANSCEIVER_LINEMODE_TT_CAN_L = 0x000c  # Switches the transceiver to one-wire-mode on CAN Low.
    # ##################line mode  -e

    XL_TRANSMIT_MSG = 0x000A
    XL_CAN_EV_TAG_TX_MSG = 0x0440  # TX:CAN/CAN-FD event tags
