from ctypes import Structure, c_uint, c_ubyte


class XLchipParams(Structure):
    _fields_ = [
        ("bitRate", c_uint),
        ("sjw", c_ubyte),
        ("tseg1", c_ubyte),
        ("tseg2", c_ubyte),
        ("sam", c_ubyte)
    ]
