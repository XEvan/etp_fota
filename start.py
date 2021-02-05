import sys

from PyQt5.QtWidgets import QApplication

from call_invoker import CallInvoker
from graphic_ui.main_frame import MainFrame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainFrame()
    frame.show()
    app.exec()

    # invoker = CallInvoker()
    # invoker.main()
