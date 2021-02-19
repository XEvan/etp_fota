import array
import ctypes
import inspect
import os
import platform
from ctypes import *
from xml.dom.minidom import parse

import clr

from aw_lib.xldriver_lib.xldriver_channelbased_lib.channelbased_constants import ChannelBasedConstants
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

    # 动态加载32bit或者64bit的dll(根据python的版本加载)
    dll_file = "vxlapi64.dll" if "64" in str(python_version) else "vxlapi.dll"
    dll = cdll.LoadLibrary(os.path.join(Constants.BASE_DIR, "bin", dll_file))

    DRIVER_INIT_STATUS = False

    DRIVER_OPEN_STATUS = False
    PORT_OPEN_STATUS = False
    ACTIVATE_CHANNEL_STATUS = False

    def __init__(self):
        self.portHandle = c_int32(-1)
        self.notificationHandle = c_int(-1)
        self.permissionMask = c_uint64(0)
        self.userHandle = c_uint16(123)

        appName, appConfig = self.load_settings()

        self.appName = c_char_p(bytes(appName, encoding="utf-8"))
        self.appChannel = appConfig

        self.accessMask = c_uint64(0)

        self.hwType = ChannelBasedConstants.XL_HWTYPE_VN5640
        self.hwIndex = ChannelBasedConstants.VN5640_1
        self.busType = ChannelBasedConstants.XL_BUS_TYPE_ETHERNET

    def load_settings(self):
        '''
        从xml中加载配置信息
        :return:AppName, ConfigDict
        '''
        xml_path = os.path.join(Constants.BASE_DIR, "config", "settings.xml")
        domTree = parse(xml_path)
        rootNode = domTree.documentElement

        resultDict = {}
        appConfig = rootNode.getElementsByTagName("ApplicationConfig")[0]
        appName = appConfig.getElementsByTagName("name")[0].childNodes[0].data

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
        if not ChannelBased.DRIVER_OPEN_STATUS:
            status = self.dll.xlOpenDriver()
            if status == 0:
                ChannelBased.DRIVER_OPEN_STATUS = True
            rfic_info("open driver:", status)
        # 打开驱动  -e

    def set_appl_config(self):
        '''
        为Application设置applicationName
        指定该applicationName对应的哪个VN5640设备，以及该VN5640的总线类型
        当前仅支持 1 个VN5640
        e.g.
            AppName1:VN5640 1
            AppName2:VN5640 2
        '''
        for ethName, value_dict in self.appChannel.items():
            status = self.dll.xlSetApplConfig(self.appName,
                                              value_dict["appChannel"],
                                              self.hwType,
                                              self.hwIndex,
                                              value_dict["hwChannel"],
                                              self.busType)

    def get_channel_mask(self):
        for ethName, value_dict in self.appChannel.items():
            channel = c_uint(-1)
            self.dll.xlGetApplConfig(self.appName,
                                     value_dict["appChannel"],
                                     self.hwType,
                                     self.hwIndex,
                                     channel,
                                     self.busType)
            channelMask = self.dll.xlGetChannelMask(self.hwType, self.hwIndex, value_dict["hwChannel"])
            value_dict["accessChannelMask"] = channelMask

            self.accessMask.value |= channelMask
        self.permissionMask = self.accessMask

    def open_port(self):
        if not ChannelBased.PORT_OPEN_STATUS:
            status = self.dll.xlOpenPort(byref(self.portHandle),
                                         self.appName,
                                         self.accessMask,
                                         byref(self.permissionMask),
                                         8 * 1024 * 1024,
                                         ChannelBasedConstants.XL_INTERFACE_VERSION_V4,
                                         ChannelBasedConstants.XL_BUS_TYPE_ETHERNET
                                         )
            if status == 0:
                ChannelBased.PORT_OPEN_STATUS = True
            rfic_info("open port:", status, self.portHandle)

    def set_notification(self):
        status = self.dll.xlSetNotification(self.portHandle, byref(self.notificationHandle), 1)
        rfic_info("set notification:", status)

    def activate_channel(self):
        XL_BUS_TYPE_ETHERNET = 0x00001000
        XL_ACTIVATE_NONE = 0
        if not ChannelBased.ACTIVATE_CHANNEL_STATUS:
            status = self.dll.xlActivateChannel(self.portHandle, self.accessMask, XL_BUS_TYPE_ETHERNET,
                                                XL_ACTIVATE_NONE)
            rfic_info("activate status:", status)
            if status == 0:
                ChannelBased.ACTIVATE_CHANNEL_STATUS = True

    def deactive_channel(self):
        if ChannelBased.ACTIVATE_CHANNEL_STATUS:
            status = self.dll.xlDeactivateChannel(self.portHandle, self.accessMask)
            rfic_info("deactivate status:", status)
            if status == 0:
                ChannelBased.ACTIVATE_CHANNEL_STATUS = False

    def set_bypass_init(self, mode=ChannelBasedConstants.XL_ETH_BYPASS_MACCORE):
        mask = 0
        for ethName, value_dict in self.appChannel.items():
            mask |= value_dict["accessChannelMask"]
        status = self.dll.xlEthSetBypass(self.portHandle,
                                         mask,
                                         self.userHandle,
                                         mode)
        rfic_info("set bypass init:", status)

    def set_bypass(self, source, target, mode):
        # 指定哪两个ETH的ByPass
        mask = self.appChannel[source]["accessChannelMask"] | self.appChannel[target]["accessChannelMask"]
        status = self.dll.xlEthSetBypass(self.portHandle,
                                         mask,
                                         self.userHandle,
                                         mode)
        rfic_info("set bypass[%s]:" % mode, status)

    def set_bypass_inactive_mode(self, source, target):
        self.deactive_channel()
        # 指定哪两个ETH的ByPass
        mask = self.appChannel[source]["accessChannelMask"] | self.appChannel[target]["accessChannelMask"]
        status = self.dll.xlEthSetBypass(self.portHandle,
                                         mask,
                                         self.userHandle,
                                         ChannelBasedConstants.XL_ETH_BYPASS_INACTIVE)
        rfic_info("set bypass inactive:", status)
        self.activate_channel()

    def set_bypass_mac_mode(self, source, target):
        self.deactive_channel()
        # 指定哪两个ETH的ByPass
        mask = self.appChannel[source]["accessChannelMask"] | self.appChannel[target]["accessChannelMask"]
        status = self.dll.xlEthSetBypass(self.portHandle,
                                         mask,
                                         self.userHandle,
                                         ChannelBasedConstants.XL_ETH_BYPASS_MACCORE)
        rfic_info("set bypass mac:", status)
        self.activate_channel()

    def driver_init(self):
        if not ChannelBased.DRIVER_INIT_STATUS:
            self.open_driver()
            self.set_appl_config()
            self.get_channel_mask()
            self.open_port()
            ChannelBased.DRIVER_INIT_STATUS = True

    def channel_setup(self):
        if ChannelBased.DRIVER_INIT_STATUS:
            self.set_notification()
            self.set_bypass_init()  # 默认都设置成MAC BYPASS
            self.activate_channel()

    def close_port_and_driver(self):
        '''
        关闭端口和驱动
        :return:
        '''
        if ChannelBased.DRIVER_INIT_STATUS:
            self.deactive_channel()
            status = self.dll.xlClosePort(self.portHandle)
            if status == 0:
                ChannelBased.PORT_OPEN_STATUS = False
            status = self.dll.xlCloseDriver()
            if status == 0:
                ChannelBased.DRIVER_OPEN_STATUS = False
            ChannelBased.DRIVER_INIT_STATUS = False
