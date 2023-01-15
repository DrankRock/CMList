# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CMCrawl.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 1100)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.version = QtWidgets.QLabel(self.centralwidget)
        self.version.setObjectName("version")
        self.gridLayout.addWidget(self.version, 4, 0, 1, 1)
        self.url_frame = QtWidgets.QFrame(self.centralwidget)
        self.url_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.url_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.url_frame.setObjectName("url_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.url_frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        # export button
        self.export_btn = QtWidgets.QPushButton(self.url_frame)
        self.export_btn.setObjectName("export_btn")
        self.gridLayout_5.addWidget(self.export_btn, 4, 0, 1, 1)
        self.import_btn = QtWidgets.QPushButton(self.url_frame)
        self.import_btn.setObjectName("import_btn")
        self.gridLayout_5.addWidget(self.import_btn, 3, 0, 1, 1)
        self.copy_btn = QtWidgets.QPushButton(self.url_frame)
        self.copy_btn.setObjectName("copy_btn")
        self.gridLayout_5.addWidget(self.copy_btn, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.url_frame)
        self.pushButton_2.setStyleSheet("background-color: rgb(46, 194, 126);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_5.addWidget(self.pushButton_2, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.url_frame, 3, 1, 1, 1)
        self.url_buttons = QtWidgets.QFrame(self.centralwidget)
        self.url_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.url_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.url_buttons.setObjectName("url_buttons")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.url_buttons)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.cancel_url_btn = QtWidgets.QPushButton(self.url_buttons)
        self.cancel_url_btn.setStyleSheet("background-color: rgb(237, 51, 59);")
        self.cancel_url_btn.setObjectName("cancel_url_btn")
        self.gridLayout_6.addWidget(self.cancel_url_btn, 1, 0, 1, 1)
        self.run_url_btn = QtWidgets.QPushButton(self.url_buttons)
        self.run_url_btn.setStyleSheet("background-color: rgb(46, 194, 126);")
        self.run_url_btn.setObjectName("run_url_btn")
        self.gridLayout_6.addWidget(self.run_url_btn, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.url_buttons, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setBaseSize(QtCore.QSize(0, 50))
        self.line.setStyleSheet("background-color: rgb(119, 118, 123);")
        self.line.setLineWidth(10)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 2)
        self.scrollArea_current_list = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_current_list.setWidgetResizable(True)
        self.scrollArea_current_list.setObjectName("scrollArea_current_list")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 697, 419))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setObjectName("gridLayout_3")

        # Bottom table
        self.current_list_table = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        self.current_list_table.setObjectName("current_list_table")
        self.current_list_table.setColumnCount(0)
        self.current_list_table.setRowCount(0)

        self.gridLayout_3.addWidget(self.current_list_table, 1, 0, 1, 1)
        self.current_list_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.current_list_lbl.setObjectName("current_list_lbl")
        self.gridLayout_3.addWidget(self.current_list_lbl, 0, 0, 1, 1)
        self.scrollArea_current_list.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_current_list, 3, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.url_lbl = QtWidgets.QLabel(self.centralwidget)
        self.url_lbl.setObjectName("url_lbl")
        self.verticalLayout.addWidget(self.url_lbl)
        self.url_input_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.url_input_line_edit.setObjectName("url_input_line_edit")
        self.verticalLayout.addWidget(self.url_input_line_edit)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.scrollArea_found_list = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_found_list.setWidgetResizable(True)
        self.scrollArea_found_list.setObjectName("scrollArea_found_list")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 697, 420))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Top table
        self.found_items_table = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.found_items_table.setObjectName("found_items_table")
        self.found_items_table.setColumnCount(0)
        self.found_items_table.setRowCount(0)

        self.gridLayout_2.addWidget(self.found_items_table, 1, 0, 1, 1)
        self.found_items_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.found_items_lbl.setObjectName("found_items_lbl")
        self.gridLayout_2.addWidget(self.found_items_lbl, 0, 0, 1, 1)
        self.scrollArea_found_list.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea_found_list, 1, 0, 1, 1)
        self.sort_frame = QtWidgets.QFrame(self.centralwidget)
        self.sort_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sort_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sort_frame.setObjectName("sort_frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.sort_frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_4 = QtWidgets.QFrame(self.sort_frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.increasing = QtWidgets.QRadioButton(self.frame_4)
        self.increasing.setObjectName("increasing")
        self.gridLayout_7.addWidget(self.increasing, 0, 0, 1, 1)
        self.decreasing = QtWidgets.QRadioButton(self.frame_4)
        self.decreasing.setObjectName("decreasing")
        self.gridLayout_7.addWidget(self.decreasing, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_4, 1, 0, 1, 1)
        self.sort_lbl = QtWidgets.QLabel(self.sort_frame)
        self.sort_lbl.setObjectName("sort_lbl")
        self.gridLayout_4.addWidget(self.sort_lbl, 0, 0, 1, 1)
        self.by_rarity = QtWidgets.QPushButton(self.sort_frame)
        self.by_rarity.setObjectName("by_rarity")
        self.gridLayout_4.addWidget(self.by_rarity, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.sort_frame)
        self.pushButton.setStyleSheet("background-color: rgb(38, 162, 105);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.pushButton, 7, 0, 1, 1)
        self.by_number = QtWidgets.QPushButton(self.sort_frame)
        self.by_number.setObjectName("by_number")
        self.gridLayout_4.addWidget(self.by_number, 4, 0, 1, 1)
        self.by_expansion = QtWidgets.QPushButton(self.sort_frame)
        self.by_expansion.setObjectName("by_expansion")
        self.gridLayout_4.addWidget(self.by_expansion, 5, 0, 1, 1)
        self.by_name = QtWidgets.QPushButton(self.sort_frame)
        self.by_name.setStyleSheet("")
        self.by_name.setObjectName("by_name")
        self.gridLayout_4.addWidget(self.by_name, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.sort_frame, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 902, 26))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuAbout.addAction(self.actionPreferences)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CMCrawl"))
        self.version.setText(_translate("MainWindow", "CMCrawl v.0.1 - 15/01/23"))
        self.export_btn.setText(_translate("MainWindow", "export"))
        self.import_btn.setText(_translate("MainWindow", "import"))
        self.copy_btn.setText(_translate("MainWindow", "copy to clipboard"))
        self.pushButton_2.setText(_translate("MainWindow", "save to filler_list"))
        self.cancel_url_btn.setText(_translate("MainWindow", "Cancel"))
        self.run_url_btn.setText(_translate("MainWindow", "Run"))
        self.current_list_lbl.setText(_translate("MainWindow", "Current List :"))
        self.url_lbl.setText(_translate("MainWindow", "URL :"))
        self.found_items_lbl.setText(_translate("MainWindow", "Found items :"))
        self.increasing.setText(_translate("MainWindow", "Increasing"))
        self.decreasing.setText(_translate("MainWindow", "Decreasing"))
        self.sort_lbl.setText(_translate("MainWindow", "Sort :"))
        self.by_rarity.setText(_translate("MainWindow", "by rarity"))
        self.pushButton.setText(_translate("MainWindow", "add to filler_list"))
        self.by_number.setText(_translate("MainWindow", "by number"))
        self.by_expansion.setText(_translate("MainWindow", "by expansion"))
        self.by_name.setText(_translate("MainWindow", "by name"))
        self.menuAbout.setTitle(_translate("MainWindow", "File"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
