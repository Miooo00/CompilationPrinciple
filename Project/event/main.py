import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from compile import Ui_MainWindow



if __name__ == '__main__':
    # 创建App
    app = QApplication(sys.argv)

    myWindow = Ui_MainWindow()
    myWindow.show()
    sys.exit(app.exec_())
