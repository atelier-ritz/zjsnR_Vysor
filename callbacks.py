from PyQt5 import QtCore, QtWidgets, uic
from vysor import Vysor
from motormanager import MotorManager
import win32gui, win32api
from client import Client
import time
# ==================================
# Qt UI Config
# ==================================
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

client = Client()
mm = MotorManager(client)
# ==================================
# Class GUI
# ==================================
class GUI(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        mm.setOrigin(self.spb_origin1.value(),self.spb_origin2.value())
        mm.setCorner(self.spb_corner1.value(),self.spb_corner2.value())
        # image
        self.spb_x1.valueChanged.connect(self.on_spb_x1)
        self.spb_y1.valueChanged.connect(self.on_spb_y1)
        self.spb_x2.valueChanged.connect(self.on_spb_x2)
        self.spb_y2.valueChanged.connect(self.on_spb_y2)
        self.btn_auto.clicked.connect(self.on_btn_auto)
        self.btn_show_autoget.clicked.connect(self.on_btn_show_autoget)
        self.btn_enemy_party.clicked.connect(self.on_btn_enemy_party)
        self.btn_party_HP.clicked.connect(self.on_btn_party_HP)
        self.btn_drop.clicked.connect(self.on_btn_drop)
        # motor
        self.btn_setparam.clicked.connect(self.on_btn_setparam)
        self.btn_motorgo1.clicked.connect(self.on_btn_motorgo1)
        self.btn_motorgo2.clicked.connect(self.on_btn_motorgo2)
        self.btn_motorgoto1.clicked.connect(self.on_btn_motorgoto1)
        self.btn_motorgoto2.clicked.connect(self.on_btn_motorgoto2)
        self.btn_motorgotoX.clicked.connect(self.on_btn_motorgotoX)
        self.btn_motorgotoY.clicked.connect(self.on_btn_motorgotoY)
        self.btn_touch.clicked.connect(self.on_btn_touch)
        self.btn_setOrigin.clicked.connect(self.on_btn_setOrigin)
        self.btn_setCorner.clicked.connect(self.on_btn_setCorner)
        self.btn_autosetEncoder.clicked.connect(self.on_btn_autosetEncoder)
        # macros
        self.btn_auto61.clicked.connect(self.on_btn_auto61)
        # timer
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.update)
        self.my_timer.start(100) # msec
        # object
        self.capture = Vysor()
        self.capture.start()
    #======================================================
    # image
    #======================================================
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
    #======================================================
    # motor
    #======================================================
    def on_btn_setparam(self):
        rpm1 = self.spb_rpm1.value()
        rpm2 = self.spb_rpm2.value()
        stepperrev1 = self.spb_stepperrev1.value()
        stepperrev2 = self.spb_stepperrev2.value()
        mm.setParam(rpm1, rpm2, stepperrev1, stepperrev2)
    def on_btn_motorgo1(self):
        val = self.spb_steps1.value()
        mm.motorgo(0,val)
    def on_btn_motorgo2(self):
        val = self.spb_steps2.value()
        mm.motorgo(1,val)
    def on_btn_motorgoto1(self):
        goal_steps = self.spb_goto1.value()
        mm.motorGoTo(0,goal_steps)
    def on_btn_motorgoto2(self):
        goal_steps = self.spb_goto2.value()
        mm.motorGoTo(1,goal_steps)
    def on_btn_motorgotoX(self):
        goal_pixel = self.spb_gotoX.value()
        mm.motorGoToX(goal_pixel)
    def on_btn_motorgotoY(self):
        goal_pixel = self.spb_gotoY.value()
        mm.motorGoToY(goal_pixel)
    def on_btn_touch(self):
        period = self.spb_period.value()
        mm.touch(period)
    def on_btn_setOrigin(self):
        x = self.spb_origin1.value()
        y = self.spb_origin2.value()
        mm.setOrigin(x, y)
    def on_btn_setCorner(self):
        x = self.spb_corner1.value()
        y = self.spb_corner2.value()
        mm.setCorner(x, y)
    def on_btn_autosetEncoder(self):
        x_pixel = self.spb_currentX_pixel.value()
        y_pixel = self.spb_currentY_pixel.value()
        x_steps = mm.position[1]
        y_steps = mm.position[0]
        originX_steps = - (x_pixel / 1920 * 590) + x_steps
        originY_steps = - (y_pixel / 1080 * 330) + y_steps
        cornerX_steps = originX_steps + 590
        cornerY_steps = originY_steps + 330
        self.spb_corner1.setValue(cornerY_steps)
        self.spb_corner2.setValue(cornerX_steps)
        self.spb_origin1.setValue(originY_steps)
        self.spb_origin2.setValue(originX_steps)
        mm.setOrigin(originX_steps, originY_steps)
        mm.setCorner(cornerX_steps, cornerY_steps)
    #======================================================
    # macros
    #======================================================
    def on_btn_auto61(self):
        mm.motorGoToX(1404)
        time.sleep(.5)
        mm.motorGoToY(274)
        while True:
            print(client.isMotorDone)
            if sum(client.isMotorDone) == 2:
                break
            time.sleep(.5)
        time.sleep(.5)
        mm.touch(.2)
        time.sleep(2.5)
        mm.touch(.2)
        time.sleep(.5)
        mm.motorGoToX(965)
        time.sleep(.5)
        mm.motorGoToY(997)
        while True:
            print(client.isMotorDone)
            if sum(client.isMotorDone) == 2:
                break
            time.sleep(.5)
        time.sleep(.5)
        mm.touch(.2)
        time.sleep(3)
        mm.touch(.2)
        time.sleep(1)
        mm.touch(.2)
        time.sleep(1)
        mm.touch(.2)
        time.sleep(1)
        mm.touch(.2)
        time.sleep(1)
        mm.touch(.2)
        while True:
            enemy = self.capture.get_window_enemy_party()
            if enemy[0] == 'ss' or enemy[0] == 'ss+' or enemy[0] == 'cv':
                break
            time.sleep(1)
        if enemy[0] == 'ss' or enemy[0] == 'ss+':
            mm.motorGoToX(1370)
            time.sleep(.5)
            mm.motorGoToY(924)
            time.sleep(3)
            mm.touch(.2)
        else:
            mm.motorGoToX(1601)
            time.sleep(.5)
            mm.motorGoToY(924)
            time.sleep(3)
            mm.touch(.2)

    #======================================================
    # update
    #======================================================
    def update(self):
        x, y = win32api.GetCursorPos()
        self.lbl_csrX.setNum(x)
        self.lbl_csrY.setNum(y)
        pos_steps = mm.position
        self.lbl_posmotor1.setNum(pos_steps[0])
        self.lbl_posmotor2.setNum(pos_steps[1])
        self.capture.set_wh()
