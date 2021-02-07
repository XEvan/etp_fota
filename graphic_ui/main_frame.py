import sys
import threading

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QCheckBox, QListWidgetItem, QListWidget

from call_invoker import CallInvoker
from graphic_ui.vn5640_settings_controller import VN5640SettingController
from load_app import load_modules_from_path


class MainFrame(QMainWindow):
    msgboxsignal = pyqtSignal(str)

    def __init__(self):
        super(MainFrame, self).__init__()
        self.setMaximumSize(500, 600)
        self.setMinimumSize(500, 600)
        self.setWindowTitle("OTA测试平台")
        self.invoker = CallInvoker()
        self.listWidget = QListWidget(self)
        self.listWidget.resize(500, 420)


        self.test_case_dict = load_modules_from_path()
        self.insert(list(self.test_case_dict.keys()))

        self.vn5640SettingBtn = QPushButton("VN5640配置", self)
        self.vn5640SettingBtn.move(20, 520)
        self.vn5640SettingBtn.clicked.connect(self.vn5640SettingBtnSlot)

        self.startBtn = QPushButton("开始测试", self)
        self.startBtn.move(380, 520)
        self.startBtn.clicked.connect(self.startBtnSlot)

        self.msgboxsignal.connect(self.msgboxSlot)

    def insert(self, data_list):
        """
        :param list: 要插入的选项文字数据列表 list[str] eg：['城市'，'小区','小区ID']
        """
        for i in data_list:
            box = QCheckBox(i)  # 实例化一个QCheckBox，吧文字传进去
            item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
            self.listWidget.addItem(item)  # 把QListWidgetItem加入QListWidget
            self.listWidget.setItemWidget(item, box)  # 再把QCheckBox加入QListWidgetItem

    def getChoose(self):
        """
        得到备选统计项的字段
        :return: list[str]
        """
        count = self.listWidget.count()  # 得到QListWidget的总个数
        cb_list = [self.listWidget.itemWidget(self.listWidget.item(i))
                   for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox
        # print(cb_list)
        chooses = []  # 存放被选择的数据
        for cb in cb_list:  # type:QCheckBox
            if cb.isChecked():
                chooses.append(cb.text())
        return chooses

    # 添加一个退出的提示事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', "确认退出?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(5)
        else:
            event.ignore()

    def startBtnSlot(self):
        self.startBtn.setEnabled(False)
        t = threading.Thread(target=self.startBtnSlotThread, args=())
        t.start()

    def startBtnSlotThread(self):
        chooses = self.getChoose()

        testDict = {}

        for item in chooses:
            testDict[item] = self.test_case_dict.get(item)

        self.invoker.main(testDict)

        self.startBtn.setEnabled(True)

        self.msgboxsignal.emit("测试完成")

    def msgboxSlot(self, pstr):
        QMessageBox.information(self, 'Message', pstr, QMessageBox.Yes)

    def vn5640SettingBtnSlot(self):
        # app = QApplication(sys.argv)
        pyui = VN5640SettingController()
        pyui.exec_()  # .show()
        # app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    frame = MainFrame()
    frame.show()
    app.exec()
