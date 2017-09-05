from PyQt5 import QtCore, QtWidgets, uic
from vysor import Vysor
import win32gui, win32api
import time
import cv2
# ==================================
# Qt UI Config
# ==================================
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# ==================================
# Class GUI
# ==================================
class GUI(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.spb_x1.valueChanged.connect(self.on_spb_x1)
        self.spb_y1.valueChanged.connect(self.on_spb_y1)
        self.spb_x2.valueChanged.connect(self.on_spb_x2)
        self.spb_y2.valueChanged.connect(self.on_spb_y2)
        self.btn_auto.clicked.connect(self.on_btn_auto)
        self.btn_show_autoget.clicked.connect(self.on_btn_show_autoget)
        self.btn_enemy_party.clicked.connect(self.on_btn_enemy_party)
        self.btn_party_HP.clicked.connect(self.on_btn_party_HP)
        self.btn_drop.clicked.connect(self.on_btn_drop)

        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.update)
        self.my_timer.start(100) # msec

        self.capture = Vysor()
        self.capture.start()

    def on_spb_x1(self,val):
        self.capture.rect[0] = val
    def on_spb_y1(self,val):
        self.capture.rect[1] = val
    def on_spb_x2(self,val):
        self.capture.rect[2] = val
    def on_spb_y2(self,val):
        self.capture.rect[3] = val

    def on_btn_show_autoget(self):
        self.capture.get_window()
    def on_btn_auto(self):
        hwnd = win32gui.FindWindow(None, "Redmi Note 3")
        if not hwnd == 0:
            x1,y1,x2,y2 = win32gui.GetWindowRect(hwnd)
            self.spb_x1.setValue(x1+8)
            self.spb_y1.setValue(y1+32)
            self.spb_x2.setValue(x2-8)
            self.spb_y2.setValue(y2-8)
    def on_btn_enemy_party(self):
        self.capture.get_window_enemy_party()
    def on_btn_party_HP(self):
        self.capture.get_window_party_hp()
    def on_btn_drop(self):
        self.capture.get_window_drop()

    def update(self):
        # cursorinfo
        x, y = win32api.GetCursorPos()
        self.lbl_csrX.setNum(x)
        self.lbl_csrY.setNum(y)
        # Vysor window size info
        self.capture.set_wh()
