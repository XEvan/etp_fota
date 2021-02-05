import os
from xml.dom.minidom import parse

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QPushButton, QTreeView, QDialog

from common.constants import Constants


class VN5640Setting(QDialog):
    def __init__(self):
        super(VN5640Setting, self).__init__()
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)
        self.setWindowTitle("VN5640配置")

        params = self.load_settings_config()

        nodeList = ["ETH1/2", "ETH3/4", "ETH5/6", "ETH7/8"]

        self.treeView = QTreeView(self)
        self.treeView.setGeometry(QRect(10, 10, 570, 520))

        self.itemModel = QStandardItemModel()
        self.itemModel.setHorizontalHeaderLabels(["Ethernet", "Values"])

        self.treeView.setModel(self.itemModel)
        self.treeView.setColumnWidth(0, 180)  # 设置列宽

        for node in nodeList:
            root = QStandardItem(node)
            root.setCheckable(True)
            root.setCheckState(Qt.Checked)
            root.setEditable(False)

            for childIndex in node.replace("ETH", "").split("/"):  # ETH1/2->[1, 2]
                childName = "ETH" + childIndex  # ETH1
                childNode = QStandardItem(childName)
                childNode.setForeground(QColor("#00ae9d"))
                childNode.setEditable(False)

                defaultParams = params.get(childName, {})

                rowItems = [QStandardItem('ECU name'), QStandardItem(defaultParams.get("ECU name"))]
                rowItems[0].setEditable(False)
                childNode.appendRow(rowItems)

                rowItems = [QStandardItem('IP'), QStandardItem(defaultParams.get("IP"))]
                rowItems[0].setEditable(False)
                childNode.appendRow(rowItems)

                rowItems = [QStandardItem('Port'), QStandardItem(defaultParams.get("Port"))]
                rowItems[0].setEditable(False)
                childNode.appendRow(rowItems)

                root.appendRow(childNode)

            self.itemModel.appendRow(root)
        self.treeView.expandAll()

        self.saveBtn = QPushButton("保存", self)
        self.saveBtn.setGeometry(QRect(490, 540, 90, 30))

    def load_settings_config(self):
        xml_path = os.path.join(Constants.BASE_DIR, "config", "settings.xml")
        domTree = parse(xml_path)
        rootNode = domTree.documentElement

        resultDict = {}
        ethConfig = rootNode.getElementsByTagName("EthConfig")[0]
        for ethNode in ethConfig.childNodes:
            if not ethNode.nodeName.startswith("#"):
                enabled = ethNode.getAttribute("enabled")
                # if str(enabled).lower() == "false":  # 如果是false的，表示不使能
                #     continue
                nodeName = ethNode.nodeName
                ethName = ethNode.getElementsByTagName("EthName")[0].getAttribute("ecuName")
                ip = ethNode.getElementsByTagName("IP")[0].childNodes[0].data
                port = ethNode.getElementsByTagName("Port")[0].childNodes[0].data
                resultDict[nodeName] = {
                    "ECU name": ethName,
                    "IP": ip,
                    "Port": port,
                }
        return resultDict
