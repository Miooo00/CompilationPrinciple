# 文件处理
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QFileDialog, QWidget, QTextEdit


class FileProcess(QWidget):
    def openFile(self, component: QTextEdit):
        # 文件选取
        self.fname, filetype = QFileDialog.getOpenFileName(self,
                                                      "选取文件",
                                                      "./",
                                                      "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        if self.fname[0]:  # 判断路径非空
            f = QFile(self.fname)  # 创建文件对象，不创建文件对象也不报错 也可以读文件和写文件
            # open()会自动返回一个文件对象
            f = open(self.fname, "r", encoding='utf-8')  # 打开路径所对应的文件， "r"以只读的方式 也是默认的方式
            data = ''
            with f:
                data = data + f.read()
            component.setText(data)
            # 设置换行模式
            component.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
            f.close()

    def saveFile(self, component: QTextEdit):
        f = open(self.fname, "w", encoding='utf-8')
        f.write(component.toPlainText())


