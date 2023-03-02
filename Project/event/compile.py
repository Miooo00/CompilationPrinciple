# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, qApp
from event.action import FileProcess as fileProcess

# 我现在就是一个MainWindow
class Ui_MainWindow(QMainWindow,):
    def __init__(self):
        super().__init__()
        self.setStyle()
        self.setupUi()
    def setupUi(self):
        # 设置项目名称
        self.setObjectName("Compile")
        # 改变画布尺寸
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout.addWidget(self.textBrowser_2)
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.verticalLayout.addWidget(self.textBrowser_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        # 设置中间组件
        self.setCentralWidget(self.centralwidget)


        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menubar)
        self.menu_7.setObjectName("menu_7")
        self.menu_8 = QtWidgets.QMenu(self.menubar)
        self.menu_8.setObjectName("menu_8")
        self.setMenuBar(self.menubar)

        self.open = QtWidgets.QAction(self)
        self.open.setObjectName("open")
        # lambda 匿名函数 进行正常传入参数
        self.open.triggered.connect(lambda :fileProcess.openFile(self,self.textEdit))
        self.close = QtWidgets.QAction(self)
        self.close.setObjectName("close")
        self.close.triggered.connect(lambda :qApp.quit())
        self.save = QtWidgets.QAction(self)
        self.save.setObjectName("save")
        self.save.triggered.connect(lambda:fileProcess.saveFile(self,self.textEdit))
        self.help = QtWidgets.QAction(self)
        self.help.setObjectName("help")
        self.about = QtWidgets.QAction(self)
        self.about.setObjectName("about")
        self.menu.addAction(self.open)
        self.menu.addAction(self.close)
        self.menu.addAction(self.save)
        self.menu_3.addAction(self.help)
        self.menu_3.addAction(self.about)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menubar.addAction(self.menu_7.menuAction())
        self.menubar.addAction(self.menu_8.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())



        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle('compile')
        self.menu.setTitle('文件')
        self.menu_2.setTitle("编辑")
        self.menu_3.setTitle("帮助")
        self.menu_4.setTitle("词法分析")
        self.menu_5.setTitle("语法分析")
        self.menu_6.setTitle("中间代码")
        self.menu_7.setTitle("目标代码生成")
        self.menu_8.setTitle("查看")

        self.open.setText("打开")
        self.open.setToolTip("open")
        self.open.setShortcut("F")
        self.close.setText("关闭")
        self.close.setToolTip("close")
        self.save.setText("保存")
        self.save.setToolTip("save")
        self.help.setText('帮助')
        self.help.setToolTip("help")
        self.about.setText("关于 Compiler")
        self.about.setToolTip("about")
    def setStyle(self):
        self.setStyleSheet('QTextBrowser{font: italic 20pt "Times New Roman";}')