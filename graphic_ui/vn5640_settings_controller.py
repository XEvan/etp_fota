import os
from xml.dom.minidom import parse

from common.constants import Constants
from graphic_ui.vn5640_settings import VN5640Setting


class VN5640SettingController(VN5640Setting):
    def __init__(self):
        super(VN5640SettingController, self).__init__()

        self.saveBtn.clicked.connect(self.savebtn_slot)

    def get_tree_dict(self):
        '''
        获取配置树
        :return:
        '''
        resultDict = {}
        for row in range(self.itemModel.rowCount()):
            item = self.itemModel.item(row, 0)
            nodeText = item.text()
            if self.itemModel.hasChildren():
                resultDict[nodeText] = {
                    "enabled": True if item.checkState() == 2 else False
                }
                self.traverse_recursive(item, resultDict[nodeText])
            else:
                resultDict[nodeText] = self.itemModel.item(row, 1).text()
        return resultDict

    def traverse_recursive(self, model, resultDict):
        for sub_row in range(model.rowCount()):
            child = model.child(sub_row, 0)
            nodeText = child.text()
            if child.hasChildren():
                resultDict[nodeText] = {}
                self.traverse_recursive(child, resultDict[nodeText])
            else:
                resultDict[nodeText] = model.child(sub_row, 1).text()

    def savebtn_slot(self):
        xml_path = os.path.join(Constants.BASE_DIR, "config", "settings.xml")
        domTree = parse(xml_path)
        rootNode = domTree.documentElement

        params = self.get_tree_dict()
        for eth, values_dict in params.items():
            enabled = values_dict.get("enabled")
            for nodeName, value in values_dict.items():
                if isinstance(value, dict):
                    node = rootNode.getElementsByTagName(nodeName)[0]  # ETH1
                    node.setAttribute("enabled", str(enabled))
                    node.getElementsByTagName("EthName")[0].setAttribute("ecuName", str(value["ECU name"]))
                    node.getElementsByTagName("IP")[0].childNodes[0].nodeValue = str(value["IP"])
                    node.getElementsByTagName("Port")[0].childNodes[0].nodeValue = str(value["Port"])
        # 将修改后的xml文件保存
        # os.remove(xml_path)
        with open(xml_path, 'w') as fh:
            domTree.writexml(fh)
        # resultDict = {}
        # ethConfig = rootNode.getElementsByTagName("EthConfig")[0]
        # for ethNode in ethConfig.childNodes:
        #     if not ethNode.nodeName.startswith("#"):
        #         enabled = ethNode.getAttribute("enabled")
        #         # if str(enabled).lower() == "false":  # 如果是false的，表示不使能
        #         #     continue
        #         nodeName = ethNode.nodeName
        #         ethName = ethNode.getElementsByTagName("EthName")[0].getAttribute("ecuName")
        #         ip = ethNode.getElementsByTagName("IP")[0].childNodes[0].data
        #         port = ethNode.getElementsByTagName("Port")[0].childNodes[0].data
        #         resultDict[nodeName] = {
        #             "ECU name": ethName,
        #             "IP": ip,
        #             "Port": port,
        #         }
