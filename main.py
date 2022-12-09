'''
 # @ Author: yyn
 # @ Create Time: 2022-12-04 21:40:34
 # @ Description: Simple Sand Clock
 '''

import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QTextEdit, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen,QScreen
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QTimer


class Info:
    version = '0.0.0.0'
    app_name = 'SandCLK'


class CoreWindow(QDialog):
    all_time = 0
    remain_time = 0

    tick_count = 0
    hour = 0
    min = 0
    down = True

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint | Qt.Tool)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(80, 80)
        screen = self.screen()
        self.move(int(screen.size().width() / 2) - 40, 0)

    def start_tick(self, seconds):
        self.all_time = seconds
        self.remain_time = 0
        self.tick_count = 0
        self.hour = int(seconds / 3600)
        self.min = int((seconds % 3600) / 60)
        self.down = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(500)

    def tick(self):
        duration_time = self.all_time - self.remain_time

        hour = int(duration_time / 3600)
        if hour != self.hour:
            self.hour = hour

        min = int(duration_time % 3600 / 60)
        if min != self.min:
            self.min = min

        if self.tick_count % 2:
            self.remain_time += 1

        self.tick_count += 1
        if (self.remain_time == self.all_time):
            self.timer.killTimer()
            self.down = True
            return

        self.update()
        

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        font_pen = QPen()
        # font_pen.setColor(QColor(0, 0, 0))
        font_pen.setColor(QColor(7,153,255))
        font_pen.setWidth(2)

        painter.setPen(font_pen)
        painter.setFont(QFont('SimSun', 18))

        if not self.down:
            text = ''
            if self.tick_count % 2:
                text = str(self.hour) + ':' + str(self.min)
            else:
                text = str(self.hour) + ' ' + str(self.min)

            painter.drawText(event.rect(), Qt.AlignCenter, text)
            painter.drawArc(5, 5, 70, 70, 90 * 16, int(((self.all_time -
                            self.remain_time) / self.all_time) * 360) * 16)
        else:
            painter.drawText(event.rect(), Qt.AlignCenter, 'DOWN')

        painter.end()

class InputWindw(QDialog):
    hour = 0
    min = 0

    def __init__(self): 
        super(QDialog,self).__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle('Input Seconds')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.hour_edit = QLineEdit(self)
        self.hour_edit.setText('input hour')
        self.hour_edit.textChanged.connect(self.hour_edit_handle)
        self.layout.addWidget(self.hour_edit)
        self.layout.addStretch()

        self.min_edit = QLineEdit(self)
        self.min_edit.setText('input min')
        self.min_edit.textChanged.connect(self.min_edit_handle)
        self.layout.addWidget(self.min_edit)

        self.ok_button = QPushButton(self)
        self.ok_button.setText('OK')
        self.ok_button.clicked.connect(self.ok_handle)
        self.layout.addWidget(self.ok_button)

        self.cancle_button = QPushButton(self)
        self.cancle_button.setText('cancle')
        self.cancle_button.clicked.connect(self.cancle_handle)
        self.layout.addWidget(self.cancle_button)

    def hour_edit_handle(self):
        self.hour = self.hour_edit.text()

    def min_edit_handle(self):
        self.min = self.min_edit.text()
        # if self.min.toint

    def ok_handle(self):
        self.core_wnd = CoreWindow()
        self.core_wnd.start_tick(int(self.hour) * 3600 + int(self.min) * 60)
        self.hide()
        self.core_wnd.show()

    def cancle_handle(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName(Info.app_name)
    app.setApplicationDisplayName(Info.app_name)
    app.setApplicationVersion(Info.version)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    input_wnd = InputWindw()
    input_wnd.show()
    sys.exit(app.exec_())

