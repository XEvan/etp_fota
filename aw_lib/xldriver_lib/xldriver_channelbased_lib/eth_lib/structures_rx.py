from ctypes import Structure, c_uint, c_ushort, c_uint64, Union, c_ubyte


class T_XL_ETH_FRAME(Structure):
    _fields_ = [
        ("etherType", c_ushort),
        ("payload", c_ubyte * 1500),
    ]


class T_XL_ETH_FRAMEDATA(Structure):
    _fields_ = [
        ("rawData", c_ubyte * 1600),
        ("ethFrame", T_XL_ETH_FRAME)
    ]


class T_XL_ETH_DATAFRAME_RX(Structure):
    _fields_ = [
        ("frameIdentifier", c_uint),
        ("frameDuration", c_uint),
        ("dataLen", c_ushort),
        ("reserved", c_ushort),
        ("reserved2", c_uint * 3),
        ("fcs", c_uint),
        ("destMAC", c_ubyte * 6),
        ("sourceMAC", c_ubyte * 6),
        ("frameData", T_XL_ETH_FRAMEDATA)
    ]


class T_XL_ETH_DATAFRAME_RX_ERROR(Structure):
    _fields_ = [
        ("frameIdentifier", c_uint),
        ("frameDuration", c_uint),
        ("errorFlags", c_uint),
        ("dataLen", c_ushort),
        ("reserved", c_ushort),
        ("reserved2", c_uint * 3),
        ("fcs", c_uint),
        ("destMAC", c_ubyte * 6),
        ("sourceMAC", c_ubyte * 6),
        ("frameData", T_XL_ETH_FRAMEDATA)
    ]


class T_XL_ETH_DATAFRAME_TXACK(Structure):
    _fields_ = [
        ("frameIdentifier", c_uint),
        ("flags", c_uint),
        ("dataLen", c_ushort),
        ("reserved", c_ushort),
        ("frameDuration", c_uint),
        ("reserved2", c_uint * 2),
        ("fcs", c_uint),
        ("destMAC", c_ubyte * 6),
        ("sourceMAC", c_ubyte * 6),
        ("frameData", T_XL_ETH_FRAMEDATA)
    ]


class T_XL_ETH_DATAFRAME_TX_EVENT(Structure):
    _fields_ = [
        ("frameIdentifier", c_uint),
        ("flags", c_uint),
        ("dataLen", c_ushort),
        ("reserved", c_ushort),
        ("frameDuration", c_uint),
        ("reserved2", c_uint * 2),
        ("fcs", c_uint),
        ("destMAC", c_ubyte * 6),
        ("sourceMAC", c_ubyte * 6),
        ("frameData", T_XL_ETH_FRAMEDATA)
    ]


class T_XL_ETH_DATAFRAME_TX_ERROR(Structure):
    _fields_ = [
        ("errorType", c_uint),
        ("txFrame", T_XL_ETH_DATAFRAME_TX_EVENT)
    ]


class T_XL_ETH_CONFIG_RESULT(Structure):
    _fields_ = [
        ("result", c_uint)
    ]


class T_XL_ETH_CHANNEL_STATUS(Structure):
    _fields_ = [
        ("link", c_uint),
        ("speed", c_uint),
        ("duplex", c_uint),
        ("mdiType", c_uint),
        ("activeConnector", c_uint),
        ("activePhy", c_uint),
        ("clockMode", c_uint),
        ("brPairs", c_uint)
    ]


class XL_SYNC_PULSE_EV(Structure):
    _fields_ = [
        ("triggerSource", c_uint),
        ("reserved", c_uint),
        ("time", c_uint64)
    ]


class TX_ACK(Structure):
    _feilds_ = [
        ("frameIdentifier", c_uint),
        ("fcs", c_uint),
        ("sourceMAC", c_ubyte * 6),
        ("reserved", c_ubyte * 2)
    ]


class TX_ERROR(Structure):
    _fields_ = [
        ("errorType", c_uint),
        ("frameIdentifier", c_uint),
        ("fcs", c_uint),
        ("sourceMAC", c_ubyte * 6),
        ("reserved", c_ubyte * 2)
    ]


class EVENT_INFO(Union):
    _fields_ = [
        ("txAck", TX_ACK),
        ("txAckSw", TX_ACK),
        ("txError", TX_ERROR),
        ("txErrorSw", TX_ERROR),
        ("reserved", c_uint * 20)
    ]


class T_XL_ETH_LOSTEVENT(Structure):
    _fields_ = [
        ("eventTypeLost", c_ushort),
        ("reserved", c_ushort),
        ("reason", c_uint),
        ("eventInfo", EVENT_INFO)
    ]


class S_XL_ETH_TAG_DATA(Union):
    XL_ETH_EVENT_SIZE_MAX = 2048
    _fields_ = [
        ("rawData", c_ubyte * XL_ETH_EVENT_SIZE_MAX),
        ("frameRxOk", T_XL_ETH_DATAFRAME_RX),
        ("frameRxError", T_XL_ETH_DATAFRAME_RX_ERROR),
        ("frameTxAck", T_XL_ETH_DATAFRAME_TXACK),
        ("frameTxAckSw", T_XL_ETH_DATAFRAME_TXACK),
        ("frameTxAckOtherApp", T_XL_ETH_DATAFRAME_TXACK),
        ("frameTxError", T_XL_ETH_DATAFRAME_TX_ERROR),
        ("frameTxErrorSw", T_XL_ETH_DATAFRAME_TX_ERROR),
        ("frameTxErrorOtherApp", T_XL_ETH_DATAFRAME_TX_ERROR),
        ("configResult", T_XL_ETH_CONFIG_RESULT),
        ("channelStatus", T_XL_ETH_CHANNEL_STATUS),
        ("syncPulse", XL_SYNC_PULSE_EV),
        ("lostEvent", T_XL_ETH_LOSTEVENT)
    ]


class T_XL_ETH_EVENT(Structure):
    _fields_ = [
        ("size", c_uint),
        ("tag", c_ushort),
        ("channelIndex", c_ushort),
        ("ethUserHandle", c_uint),
        ("flagsChip", c_ushort),
        ("reserved", c_ushort),
        ("reserved1", c_uint64),
        ("timeStampSync", c_uint64),
        ("tagData", S_XL_ETH_TAG_DATA)
    ]
