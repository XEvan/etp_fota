import array
import ctypes
import inspect
import os
import platform
from ctypes import *
from xml.dom.minidom import parse

import clr

from aw_lib.xldriver_lib.xldriver_channelbased_lib.can_lib.can_structures import XLchipParams
from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
from aw_lib.xldriver_lib.xldriver_channelbased_lib.structures import XL_DRIVER_CONFIG
from common.constants import Constants
from logger import rfic_error, rfic_info

clr.FindAssembly(os.path.join(Constants.BASE_DIR, "bin", "vxlapi_NET.dll"))
clr.AddReference(os.path.join(Constants.BASE_DIR, "bin", "vxlapi_NET"))
from vxlapi_NET import *
import vxlapi_NET


class XLDefine(XLDefine): pass


class XLClass(XLClass): pass


# platform.architecture()：获取python版本是32位还是64位
#   64位：('64bit', 'WindowsPE')
#   32位：('32bit', 'WindowsPE')
python_version = platform.architecture()[0]  # 32bit or 64bit


class ChannelBased:
    net_driver = vxlapi_NET.XLDriver()

    # 动态加载32bit或者64bit的dll(根据python的版本加载)  -s
    dll_file = "vxlapi64.dll" if "64" in str(python_version) else "vxlapi.dll"
    dll = cdll.LoadLibrary(os.path.join(Constants.BASE_DIR, "bin", dll_file))

    # 动态加载32bit或者64bit的dll(根据python的版本加载)  -e

    def __init__(self):
        self.hwType = ChannelBasedConstants.XL_HWTYPE_VN5640
        self.hwIndex = ChannelBasedConstants.VN5640_1

        self.eth_params()  # 以太网的参数
        self.can_params()  # can的参数

    def eth_params(self):
        self.ethPortHandle = c_int32(-1)
        self.ethNotificationHandle = c_int(-1)
        self.ethPermissionMask = c_uint64(0)
        self.ethUserHandle = c_uint16(1)
        self.ethAccessMask = c_uint64(0)

        # 设置application的name
        appName, appConfig = self.load_eth_settings()
        self.ethAppName = c_char_p(bytes(appName, encoding="utf-8"))
        self.ethAppChannel = appConfig

        self.ethBusType = ChannelBasedConstants.XL_BUS_TYPE_ETHERNET

    def can_params(self):
        self.canPortHandle = c_int32(-1)
        self.canNotificationHandle = c_int(-1)
        self.canPermissionMask = c_uint64(0)
        self.canUserHandle = c_uint16(2)
        self.canAccessMask = c_uint64(0)

        # 设置application的name
        appName, appConfig = self.load_can_settings()
        self.canAppName = c_char_p(bytes(appName, encoding="utf-8"))
        self.canAppChannel = appConfig

        self.canBusType = ChannelBasedConstants.XL_BUS_TYPE_CAN

    def load_eth_settings(self):
        '''
        从xml中加载配置信息
        :return:AppName, ConfigDict
        '''
        xml_path = os.path.join(Constants.BASE_DIR, "config", "settings.xml")
        domTree = parse(xml_path)
        rootNode = domTree.documentElement

        resultDict = {}
        appConfig = rootNode.getElementsByTagName("ApplicationConfig")[0]
        appName = appConfig.getElementsByTagName("EthAppName")[0].childNodes[0].data

        ethConfig = rootNode.getElementsByTagName("EthConfig")[0]
        for ethNode in ethConfig.childNodes:
            if not ethNode.nodeName.startswith("#"):
                enabled = ethNode.getAttribute("enabled")
                if str(enabled).lower() == "false":  # 如果是false的，表示不使能
                    continue
                ethName = ethNode.getElementsByTagName("EthName")[0].childNodes[0].data
                appChannel = ethNode.getElementsByTagName("AppChannel")[0].childNodes[0].data
                hwChannel = ethNode.getElementsByTagName("HwChannel")[0].childNodes[0].data
                ip = ethNode.getElementsByTagName("IP")[0].childNodes[0].data
                port = ethNode.getElementsByTagName("Port")[0].childNodes[0].data
                resultDict[ethName] = {
                    "appChannel": int(appChannel),
                    "hwChannel": int(hwChannel),
                    "accessChannelMask": c_uint64(0),
                    "ip": ip,
                    "port": int(port)
                }
        return appName, resultDict

    def load_can_settings(self):
        '''
        从xml中加载配置信息
        :return:AppName, ConfigDict
        '''
        xml_path = os.path.join(Constants.BASE_DIR, "config", "settings.xml")
        domTree = parse(xml_path)
        rootNode = domTree.documentElement

        resultDict = {}
        appConfig = rootNode.getElementsByTagName("ApplicationConfig")[0]
        appName = appConfig.getElementsByTagName("CanAppName")[0].childNodes[0].data

        ethConfig = rootNode.getElementsByTagName("CanConfig")[0]
        for ethNode in ethConfig.childNodes:
            if not ethNode.nodeName.startswith("#"):
                enabled = ethNode.getAttribute("enabled")
                if str(enabled).lower() == "false":  # 如果是false的，表示不使能
                    continue
                canName = ethNode.getElementsByTagName("CanName")[0].childNodes[0].data
                appChannel = ethNode.getElementsByTagName("AppChannel")[0].childNodes[0].data
                hwChannel = ethNode.getElementsByTagName("HwChannel")[0].childNodes[0].data
                resultDict[canName] = {
                    "appChannel": int(appChannel),
                    "hwChannel": int(hwChannel),
                    "accessChannelMask": c_uint64(0)
                }
        return appName, resultDict

    def is_little_endian(self):
        a = array.array('H', [1]).tobytes()
        if a[0] == 1:
            return True
        else:
            return False

    def network2host_order(self, val):
        if self.is_little_endian():
            val = (val << 8) | (val >> 8)
        return hex(val)[2:]

    def host2network_order(self, val):
        return self.network2host_order(val)

    def stop_thread(self, thread):
        """终止线程"""
        try:
            tid = ctypes.c_long(thread.ident)
            if not inspect.isclass(SystemExit):
                exctype = type(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
            if res == 0:
                # pass
                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        except Exception as err:
            rfic_error(err)

    def open_driver(self):
        # 打开驱动  -s
        status = self.dll.xlOpenDriver()
        rfic_info("open driver:", status)
        # 打开驱动  -e

    def get_driver_config(self):
        pDriverConfig = XL_DRIVER_CONFIG()
        status = self.dll.xlGetDriverConfig(byref(pDriverConfig))
        rfic_info("get driver config:", status)

    def set_appl_config(self, app_name, app_channels, bus_type):
        '''
        为Application设置applicationName
        指定该applicationName对应的哪个VN5640设备，以及该VN5640的总线类型
        当前仅支持 1 个VN5640
        e.g.
            AppName1:VN5640 1
            AppName2:VN5640 2
        '''
        for ethName, value_dict in app_channels.items():
            status = self.dll.xlSetApplConfig(app_name,
                                              value_dict["appChannel"],
                                              self.hwType,
                                              self.hwIndex,
                                              value_dict["hwChannel"],
                                              bus_type)

    def get_channel_mask(self, app_name, app_channels, accessmask, permissionmask, bus_type):
        for ethName, value_dict in app_channels.items():
            channel = c_uint(-1)
            self.dll.xlGetApplConfig(app_name,
                                     value_dict["appChannel"],
                                     self.hwType,
                                     self.hwIndex,
                                     channel,
                                     bus_type)
            channelMask = self.dll.xlGetChannelMask(self.hwType, self.hwIndex, value_dict["hwChannel"])
            value_dict["accessChannelMask"] = channelMask

            accessmask.value |= channelMask
        permissionmask.value = accessmask.value

    def open_port(self, app_name, port_handle, accessmask, permissionmask, bus_type):
        status = self.dll.xlOpenPort(byref(port_handle),
                                     app_name,
                                     accessmask,
                                     byref(permissionmask),
                                     8 * 1024 * 1024,
                                     ChannelBasedConstants.XL_INTERFACE_VERSION_V4,
                                     bus_type
                                     )
        rfic_info("open port:", status, port_handle)

    def set_notification(self, port_handle, notification_handle):
        status = self.dll.xlSetNotification(port_handle, byref(notification_handle), 1)
        rfic_info("set notification:", status)

    def activate_channel(self, port_handle, accessmask, bus_type):
        XL_ACTIVATE_NONE = 0
        status = self.dll.xlActivateChannel(port_handle, accessmask, bus_type, XL_ACTIVATE_NONE)
        rfic_info("activate status:", status)

    def deactive_channel(self, port_handle, accessmask):
        status = self.dll.xlDeactivateChannel(port_handle, accessmask)
        rfic_info("deactivate status:", status)

    def eth_set_bypass(self, port_handle, mask, user_handle, mode):
        status = self.dll.xlEthSetBypass(port_handle, mask, user_handle, mode)
        rfic_info("set bypass:", status)

    def set_bypass_init(self, port_handle, user_handle, app_channel, mode=ChannelBasedConstants.XL_ETH_BYPASS_MACCORE):
        mask = 0
        for ethName, value_dict in app_channel.items():
            mask |= value_dict["accessChannelMask"]
        self.eth_set_bypass(port_handle, mask, user_handle, mode)

    def set_can_channel_params(self, port_handle, accessmask):
        """
        使用给定参数初始化accessMask定义的通道
        如果要调用此函数，端口必须具有init access访问权限
        """
        pChipParams = XLchipParams()
        status = self.dll.xlCanSetChannelParams(port_handle, accessmask, byref(pChipParams))
        rfic_info("set can channel params:", status)

    def set_can_channel_bitrate(self, port_handle, accessmask, bitrate=500000):
        """
        指定比特率
        """
        bitrate = c_ulong(bitrate)
        status = self.dll.xlCanSetChannelBitrate(port_handle, accessmask, bitrate)
        rfic_info("set can channel bitrate:", status)

    def set_can_channel_output(self, port_handle, accessmask, mode=ChannelBasedConstants.XL_OUTPUT_MODE_NORMAL):
        """
        如果mode=XL_OUTPUT_MODE_SILENT，当收到CAN消息后，CANchip不会生成任何acknowledges
        在静默模式下，不能发送消息，但是可以接收消息
        如果没有调用该方法，那么默认的模式是：normal模式(有acknowledges)
        """
        status = self.dll.xlCanSetChannelOutput(port_handle, accessmask, mode)
        rfic_info("set can channel output:", status)

    def set_can_channel_transceiver(self, port_handle, accessmask):
        transceiver_type = ChannelBasedConstants.XL_TRANSCEIVER_TYPE_CAN_252
        line_mode = ChannelBasedConstants.XL_TRANSCEIVER_LINEMODE_NORMAL
        res_net = 0  # reserved for future use, Set to 0.
        status = self.dll.xlCanSetChannelTransceiver(port_handle, accessmask, transceiver_type, line_mode, res_net)
        rfic_info("set can channel transceiver:", status)
