from ctypes import Structure, c_uint, c_ushort, c_ubyte


class T_XL_ETH_FRAME(Structure):
    _fields_ = [
        ("etherType", c_ushort),
        ("payload", c_ubyte * 1500),
    ]


class T_XL_ETH_FRAMEDATA(Structure):
    _fields_ = [
        ("ethFrame", T_XL_ETH_FRAME),
        ("rawData", c_ubyte * 1600)
    ]


class T_XL_ETH_DATAFRAME_TX(Structure):
    _fields_ = [
        ("frameIdentifier", c_uint),
        ("flags", c_uint),
        ("dataLen", c_ushort),
        ("reserved", c_ushort),
        ("reserved2", c_uint * 4),
        ("destMAC", c_ubyte * 6),
        ("sourceMAC", c_ubyte * 6),
        ("frameData", T_XL_ETH_FRAMEDATA)
    ]
