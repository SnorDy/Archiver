import os
import sys
import shutil
import datetime
import threading, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(449, 301)
        MainWindow.setStyleSheet("background-color:rgb(45, 48, 50);\n"
                                 "font: 12pt \"Terminator Two\";\n"
                                 "color:white")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.archive_btn = QtWidgets.QPushButton(self.centralwidget)
        self.archive_btn.setGeometry(QtCore.QRect(10, 20, 431, 41))
        self.archive_btn.setStyleSheet("border:none;background-color:rgb(48, 105, 221);border-radius:5px")
        self.archive_btn.setObjectName("archive_btn")
        self.result_btn = QtWidgets.QPushButton(self.centralwidget)
        self.result_btn.setGeometry(QtCore.QRect(10, 70, 431, 41))
        self.result_btn.setStyleSheet("border:none;background-color:rgb(48, 105, 221);border-radius:5px")
        self.result_btn.setObjectName("result_btn")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 170, 431, 31))
        self.progressBar.setStyleSheet("QProgressBar{\n"
                                       "border-radius:5px;\n"
                                       "font: 12pt \"Terminator Two\";\n"
                                       "color:white;\n"
                                       "background-color:rgb(162, 162, 162);\n"
                                       "}\n"
                                       "\n"
                                       "QProgressBar::chunk{\n"
                                       "background-color:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 107, 217, 255), stop:0.710227 rgba(40, 255, 255, 255));border-radius:5px;\n"
                                       "}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(10, 260, 431, 21))
        self.result_label.setText("")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setObjectName("result_label")
        self.quit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.quit_btn.setGeometry(QtCore.QRect(10, 210, 431, 41))
        self.quit_btn.setStyleSheet("border:none;background-color:rgb(255, 83, 106);border-radius:5px")
        self.quit_btn.setObjectName("quit_btn")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(10, 120, 431, 41))
        self.start_btn.setStyleSheet("border:none;background-color:rgb(113, 221, 131);border-radius:5px")
        self.start_btn.setObjectName("start_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.archive_btn.setText(_translate("MainWindow", "select archiving directory"))
        self.result_btn.setText(_translate("MainWindow", "select result directory"))
        self.quit_btn.setText(_translate("MainWindow", "quit"))
        self.start_btn.setText(_translate("MainWindow", "start"))


class Win(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.arch_dir = ''
        self.res_dir = ''
        self.archive_btn.clicked.connect(lambda: self.select_dir('a'))
        self.result_btn.clicked.connect(lambda: self.select_dir('r'))
        self.quit_btn.clicked.connect(sys.exit)
        self.start_btn.clicked.connect(self.start)

    def select_dir(self, mode):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        if dlg.exec():
            if mode == 'a':
                win.progressBar.setValue(0)
                self.arch_dir = dlg.selectedFiles()[-1]
                self.result_label.setText('archive selected')

            else:
                win.progressBar.setValue(0)
                self.res_dir = dlg.selectedFiles()[-1]
                self.result_label.setText('result directory selected')

    def start(self):
        global flag
        if not (self.arch_dir):
            self.result_label.setText('no directory to archive')
        elif not (self.res_dir):
            self.result_label.setText('no result directory')
        else:
            flag = 0
            make_reserve_arc_gui(self.arch_dir, self.res_dir)


def progress():
    global flag
    count = 0
    while not (flag):
        count += 1
        if count == 100:
            count = 99
        time.sleep(0.1)
        win.progressBar.setValue(count)
    win.progressBar.setValue(100)
    win.result_label.setText('done')


def make_reserve_arc_gui(source, dest):
    global flag
    try:
        t1 = threading.Thread(target=progress, args=[])
        t1.daemon = True
        t1.start()
        dirname = source.split(r'/')[-1]
        now = str(datetime.datetime.now()).replace(':', '.')
        if now.count('.') == 3:
            now = now[::-1]
            now = now[now.find('.'):]
            now = now[::-1]
        shutil.make_archive(os.path.join(dest, dirname + '_saved_' + now), 'zip', source)
        flag = 1
    except Exception:
        win.result_label.setText('error')


def make_reserve_arc(source, dest):
    now = str(datetime.datetime.now()).replace(':', '.')
    dirname = source.split(r'/')[-1]
    if now.count('.') == 3:
        now = now[::-1]
        now = now[now.find('.'):]
        now = now[::-1]
    shutil.make_archive(os.path.join(dest, dirname + '_saved_' + now), 'zip', source)


if __name__ == '__main__':
    app = QApplication([])
    win = Win()
    win.show()
    sys.exit(app.exec())
