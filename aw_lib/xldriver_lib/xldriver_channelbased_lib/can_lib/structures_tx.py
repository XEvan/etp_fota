from ctypes import Structure, c_ubyte, c_ushort, Union, c_uint, c_uint64


class s_xl_can_msg(Structure):
    MAX_MSG_LEN = 8
    _fields_ = [
        ("id", c_uint),
        ("flags", c_ushort),
        ("dlc", c_ushort),
        ("res1", c_uint64),
        ("data", c_ubyte * MAX_MSG_LEN),
        ("res2", c_uint64)
    ]


class s_xl_chip_state(Structure):
    _fields_ = [
        ("busStatus", c_ubyte),
        ("txErrorCounter", c_ubyte),
        ("rxErrorCounter", c_ubyte)
    ]


class s_xl_lin_msg(Structure):
    _fields_ = [
        ("id", c_ubyte),
        ("dlc", c_ubyte),
        ("flags", c_ushort),
        ("data", c_ubyte * 8),
        ("crc", c_ubyte)
    ]


class s_xl_lin_no_ans(Structure):
    _fields_ = [
        ("id", c_ubyte)
    ]


class s_xl_lin_wake_up(Structure):
    _fields_ = [
        ("flag", c_ubyte),
        ("unused", c_ubyte * 3),
        ("startOffs", c_uint),
        ("width", c_uint)
    ]


class s_xl_lin_sleep(Structure):
    _fields_ = [
        ("flag", c_ubyte)
    ]


class s_xl_lin_crc_info(Structure):
    _fields_ = [
        ("id", c_ubyte),
        ("flag", c_ubyte)
    ]


class s_xl_lin_msg_api(Union):
    _fields_ = [
        ("linMsg", s_xl_lin_msg),
        ("linNoAns", s_xl_lin_no_ans),
        ("linWakeUp", s_xl_lin_wake_up),
        ("linSleep", s_xl_lin_sleep),
        ("linCRCinfo", s_xl_lin_crc_info)
    ]


class s_xl_sync_pulse(Structure):
    _fields_ = [
        ("pulseCode", c_ubyte),
        ("time", c_uint64),
    ]


class s_xl_daio_data(Structure):
    _fields_ = [
        ("flags", c_ushort),
        ("timestamp_correction", c_uint),
        ("mask_digital", c_ubyte),
        ("value_digital", c_ubyte),
        ("mask_analog", c_ubyte),
        ("reserved0", c_ubyte),
        ("value_analog", c_ushort * 4),
        ("pwm_frequency", c_uint),
        ("pwm_value", c_ushort),
        ("reserved1", c_uint),
        ("reserved2", c_uint)
    ]


class s_xl_transceiver(Structure):
    _fields_ = [
        ("event_reason", c_ubyte),
        ("is_present", c_ubyte)
    ]


class XL_IO_DIGITAL_DATA(Structure):
    _fields_ = [
        ("digitalInputData", c_uint)
    ]


class XL_IO_ANALOG_DATA(Structure):
    _fields_ = [
        ("measuredAnalogData0", c_uint),
        ("measuredAnalogData1", c_uint),
        ("measuredAnalogData2", c_uint),
        ("measuredAnalogData3", c_uint),
    ]


class piggy_data(Union):
    _fields_ = [
        ("digital", XL_IO_DIGITAL_DATA),
        ("analog", XL_IO_ANALOG_DATA)
    ]


class s_xl_daio_piggy_data(Structure):
    _fields_ = [
        ("daioEvtTag", c_uint),
        ("triggerType", c_uint),
        ("data", piggy_data),
    ]


class XL_KLINE_RX_DATA(Structure):
    _fields_ = [
        ("timeDiff", c_uint),
        ("data", c_uint),
        ("error", c_uint)
    ]


class XL_KLINE_TX_DATA(Structure):
    _fields_ = [
        ("timeDiff", c_uint),
        ("data", c_uint),
        ("error", c_uint)
    ]


class XL_KLINE_TESTER_5BD(Structure):
    _fields_ = [
        ("tag5bd", c_uint),
        ("timeDiff", c_uint),
        ("data", c_uint)
    ]


class XL_KLINE_ECU_5BD(Structure):
    _fields_ = [
        ("tag5bd", c_uint),
        ("timeDiff", c_uint),
        ("data", c_uint)
    ]


class XL_KLINE_TESTER_FI_WU_PATTERN(Structure):
    _fields_ = [
        ("timeDiff", c_uint),
        ("fastInitEdgeTimeDiff", c_uint)
    ]


class XL_KLINE_ECU_FI_WU_PATTERN(Structure):
    _fields_ = [
        ("timeDiff", c_uint),
        ("fastInitEdgeTimeDiff", c_uint)  # TiniL
    ]


class XL_KLINE_CONFIRMATION(Structure):
    _fields_ = [
        ("channel", c_uint),
        ("confTag", c_uint),
        ("result", c_uint)
    ]


class XL_KLINE_ERROR_RXTX(Structure):
    _fields_ = [
        ("rxtxErrData", c_uint)
    ]


class XL_KLINE_ERROR_TESTER_5BD(Structure):
    _fields_ = [
        ("tester5BdErr", c_uint)
    ]


class XL_KLINE_ERROR_ECU_5BD(Structure):
    _fields_ = [
        ("ecu5BdErr", c_uint)
    ]


class XL_KLINE_ERROR_IBS(Structure):
    _fields_ = [
        ("ibsErr", c_uint),
        ("rxtxErrData", c_uint)
    ]


class kline_data_error(Union):
    _fields_ = [
        ("rxtxErr", XL_KLINE_ERROR_RXTX),
        ("tester5BdErr", XL_KLINE_ERROR_TESTER_5BD),
        ("ecu5BdErr", XL_KLINE_ERROR_ECU_5BD),
        ("ibsErr", XL_KLINE_ERROR_IBS),
        ("reserved", c_uint * 4)
    ]


class XL_KLINE_ERROR(Structure):
    _fields_ = [
        ("klineErrorTag", c_uint),
        ("reserved", c_uint),
        ("data", kline_data_error)
    ]


class kline_data(Union):
    _fields_ = [
        ("klineRx", XL_KLINE_RX_DATA),
        ("klineTx", XL_KLINE_TX_DATA),
        ("klineTester5Bd", XL_KLINE_TESTER_5BD),
        ("klineEcu5Bd", XL_KLINE_ECU_5BD),
        ("klineTesterFiWu", XL_KLINE_TESTER_FI_WU_PATTERN),
        ("klineEcuFiWu", XL_KLINE_ECU_FI_WU_PATTERN),
        ("klineConfirmation", XL_KLINE_CONFIRMATION),
        ("klineError", XL_KLINE_ERROR)
    ]


class s_xl_kline_data(Structure):
    _fields_ = [
        ("klineEvtTag", c_uint),
        ("reserved", c_uint),
        ("data", kline_data),
    ]


class TagDataUnion(Union):
    _fields_ = [
        ("msg", s_xl_can_msg),
        ("chipState", s_xl_chip_state),
        ("linMsgApi", s_xl_lin_msg_api),
        ("syncPulse", s_xl_sync_pulse),
        ("daioData", s_xl_daio_data),
        ("transceiver", s_xl_transceiver),
        ("daioPiggyData", s_xl_daio_piggy_data),
        ("klineData", s_xl_kline_data)
    ]


class XLevent(Structure):
    _fields_ = [
        ("tag", c_ubyte),
        ("chanIndex", c_ubyte),
        ("transId", c_ushort),
        ("portHandle", c_ushort),
        ("flags", c_ubyte),
        ("reserved", c_ubyte),
        ("tagData", TagDataUnion)
    ]
