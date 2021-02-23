from ctypes import Structure, c_uint8, c_uint, c_byte, c_ubyte, c_ushort, c_uint64, Union


class T_XL_ETH_CONFIG(Structure):
    XL_ETH_MODE_SPEED_AUTO_100 = 2
    XL_ETH_MODE_SPEED_AUTO_1000 = 4
    XL_ETH_MODE_SPEED_AUTO_100_1000 = 5
    XL_ETH_MODE_SPEED_FIXED_100 = 8
    XL_ETH_MODE_SPEED_FIXED_1000 = 9
    XL_ETH_MODE_DUPLEX_DONT_CARE = 0
    XL_ETH_MODE_DUPLEX_AUTO = 1
    XL_ETH_MODE_DUPLEX_FULL = 3
    XL_ETH_MODE_CONNECTOR_DONT_CARE = 0
    XL_ETH_MODE_CONNECTOR_RJ45 = 1
    XL_ETH_MODE_CONNECTOR_DSUB = 2
    XL_ETH_MODE_PHY_DONT_CARE = 0
    XL_ETH_MODE_PHY_IEEE_802_3 = 1
    XL_ETH_MODE_PHY_BROADR_REACH = 2
    XL_ETH_MODE_CLOCK_DONT_CARE = 0
    XL_ETH_MODE_CLOCK_AUTO = 1
    XL_ETH_MODE_CLOCK_MASTER = 2
    XL_ETH_MODE_CLOCK_SLAVE = 3
    XL_ETH_MODE_MDI_AUTO = 1
    XL_ETH_MODE_MDI_STRAIGHT = 2
    XL_ETH_MODE_MDI_CROSSOVER = 3
    XL_ETH_MODE_BR_PAIR_DONT_CARE = 0
    XL_ETH_MODE_BR_PAIR_1PAIR = 1
    _fields_ = [
        ("speed", c_uint8),
        ("duplex", c_uint8),
        ("phy", c_uint8),
        ("clockMode", c_uint8),
        ("mdiMode", c_uint8),
        ("brPairs", c_uint8)
    ]


class Can(Structure):
    _fields_ = [
        ("bitRate", c_uint),
        ("sjw", c_ubyte),
        ("tseg1", c_ubyte),
        ("tseg2", c_ubyte),
        ("sam", c_ubyte),
        ("outputMode", c_ubyte),
        ("reserved1", c_ubyte * 7),
        ("canOpMode", c_ubyte)
    ]


class CanFD(Structure):
    _fields_ = [
        ("arbitrationBitRate", c_uint),
        ("sjwAbr", c_ubyte),
        ("tseg1Abr", c_ubyte),
        ("tseg2Abr", c_ubyte),
        ("samAbr", c_ubyte),
        ("outputMode", c_ubyte),
        ("sjwDbr", c_ubyte),
        ("tseg1Dbr", c_ubyte),
        ("tseg2Dbr", c_ubyte),
        ("dataBitRate", c_uint),
        ("canOpMode", c_ubyte)
    ]


class Most(Structure):
    _fields_ = [
        ("activeSpeedGrade", c_uint),
        ("compatibleSpeedGrade", c_uint),
        ("inicFwVersion", c_uint)
    ]


class Flexray(Structure):
    _fields_ = [
        ("status", c_uint),
        ("cfgMode", c_uint),
        ("baudrate", c_uint)
    ]


class Ethernet(Structure):
    _fields_ = [
        ("macAddr", c_ubyte * 6),
        ("connector", c_ubyte),
        ("phy", c_ubyte),
        ("link", c_ubyte),
        ("speed", c_ubyte),
        ("clockMode", c_ubyte),
        ("bypass", c_ubyte)
    ]


class Tx(Structure):
    _fields_ = [
        ("bitrate", c_uint),
        ("parity", c_uint),
        ("minGap", c_uint)
    ]


class Rx(Structure):
    _fields_ = [
        ("bitrate", c_uint),
        ("minBitrate", c_uint),
        ("maxBitrate", c_uint),
        ("parity", c_uint),
        ("minGap", c_uint),
        ("autoBaudrate", c_uint)
    ]


class DirUnion(Union):
    _fields_ = [
        ("tx", Tx),
        ("rx", Rx),
        ("raw", c_ubyte * 24)
    ]


class A429(Structure):
    _fields_ = [
        ("channelDirection", c_ushort),
        ("res1", c_ushort),
        ("dir", DirUnion)
    ]


class DataUnion(Union):
    _fields_ = [
        ("can", Can),
        ("canFD", CanFD),
        ("most", Most),
        ("flexray", Flexray),
        ("ethernet", Ethernet),
        ("a429", A429),
        ("raw", c_ubyte * 28)
    ]


class XLbusParams(Structure):
    _fields_ = [
        ("ethBusType", c_uint),
        ("data", DataUnion)
    ]


class XLchannelConfig(Structure):
    XL_MAX_LENGTH = 31
    _fields_ = [
        ("name", c_byte * (XL_MAX_LENGTH + 1)),
        ("hwType", c_ubyte),
        ("hwIndex", c_ubyte),
        ("hwChannel", c_ubyte),
        ("transceiverType", c_ushort),
        ("transceiverState", c_ushort),
        ("configError", c_ushort),
        ("channelIndex", c_ubyte),
        ("channelMask", c_uint64),
        ("channelCapabilities", c_uint),
        ("channelBusCapabilities", c_uint),
        # Channel
        ("isOnBus", c_ubyte),
        ("connectedBusType", c_uint),
        ("busParams", XLbusParams),
        ("_doNotUse", c_uint),
        ("driverVersion", c_uint),
        ("interfaceVersion", c_uint),
        ("raw_data", c_uint * 10),
        ("serialNumber", c_uint),
        ("articleNumber", c_uint),
        ("transceiverName", c_byte * (XL_MAX_LENGTH + 1)),
        ("specialCabFlags", c_uint),
        ("dominantTimeout", c_uint),
        ("dominantRecessiveDelay", c_ubyte),
        ("recessiveDominantDelay", c_ubyte),
        ("connectionInfo", c_ubyte),
        ("currentlyAvailableTimestamps", c_ubyte),
        ("minimalSupplyVoltage", c_ushort),
        ("maximalSupplyVoltage", c_ushort),
        ("maximalBaudrate", c_uint),
        ("fpgaCoreCapabilities", c_ubyte),
        ("specialDeviceStatus", c_ubyte),
        ("channelBusActiveCapabilities", c_ushort),
        ("breakOffset", c_ushort),
        ("delimiterOffset", c_ushort),
        ("reserved", c_uint * 3)
    ]


class XL_DRIVER_CONFIG(Structure):
    XL_CONFIG_MAX_CHANNELS = 64
    _fields_ = [
        ("dllVersion", c_uint),
        ("channelCount", c_uint),  # total number of channels
        ("reserved", c_uint * 10),
        ("channel", XLchannelConfig * XL_CONFIG_MAX_CHANNELS)
    ]
