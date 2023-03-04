import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic, QtCore
from Project.Gui.func import read_file, save_file
from Project.Lib1_Words_Recognize.Recog_main import entry


class Gui:
    def __init__(self):
        self.ui = uic.loadUi('wings.ui')

        self.lib1_svbt = self.ui.lib1_svbt
        self.lib1_selbt = self.ui.lib1_selbt
        self.lib1_exebt = self.ui.lib1_exebt
        self.lib1_src_text = self.ui.lib1_src_text
        self.lib1_des_text = self.ui.lib1_des_text
        self.lib1_svpath = ''
        self.lib1_selbt.clicked.connect(self.button_fun1_1)
        self.lib1_exebt.clicked.connect(self.button_fun1_2)
        self.lib1_svbt.clicked.connect(self.button_fun1_3)

    def show(self):
        self.ui.show()

    def button_fun1_1(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui,
            '选择文件',
            filter='文件类型(*)'
        )
        if self.lib1_src_text.toPlainText() and not file_path:
            return
        elif not self.lib1_src_text.toPlainText() and not file_path:
            return
        self.lib1_flname = file_path.split('/')[-1]
        self.lib1_src_text.setPlainText(read_file(file_path))

    def button_fun1_2(self):
        if self.lib1_src_text.toPlainText():
            items = entry(self.lib1_src_text.toPlainText())
            str1 = ''
            print(items)
            for item in items:
                for i in range(len(item)):
                    if i != len(item)-1:
                        str1 += str(item[i]) + ','
                    else:
                        str1 += str(item[i])
                str1 += '\n'
            self.lib1_des_text.setPlainText(str1)
        else:
            return

    def button_fun1_3(self):
        file_path = QFileDialog.getExistingDirectory(self.ui, "选择保存路径")
        if file_path:
            save_file(self.lib1_des_text.toPlainText(), file_path, self.lib1_flname)


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)
a = Gui()
a.show()
sys.exit(app.exec_())