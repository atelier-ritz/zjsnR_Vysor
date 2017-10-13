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
        self.cbx_power.toggled.connect(self.on_cbx_power)
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
        # self.capture.get_window_drop()
        self.capture.isScene('drop')
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
        originX_steps = - (x_pixel / 1920 * 605) + x_steps
        originY_steps = - (y_pixel / 1080 * 350) + y_steps
        cornerX_steps = originX_steps + 605
        cornerY_steps = originY_steps + 350
        self.spb_corner1.setValue(cornerY_steps)
        self.spb_corner2.setValue(cornerX_steps)
        self.spb_origin1.setValue(originY_steps)
        self.spb_origin2.setValue(originX_steps)
        mm.setOrigin(originX_steps, originY_steps)
        mm.setCorner(cornerX_steps, cornerY_steps)
    def on_cbx_power(self,boolean):
        if boolean:
            mm.powerOn()
        else:
            mm.powerOff()
    #======================================================
    # macros
    #======================================================
    def on_btn_auto61(self):
        flagBuji = 0
        while True:
            mm.motorGoToXYAndTouch(1438,350,0.2) # chuzheng
            while client.isBusy: time.sleep(1)
            while not self.capture.isScene('chuzhengzhunbei'):
                mm.touch(.2)
                time.sleep(2)
            if flagBuji == 4:
                flagBuji = 0
                mm.motorGoToXYAndTouch(1815,104,0.2) # buji
                while client.isBusy: time.sleep(1)
                time.sleep(2)
                while not self.capture.isScene('buji'):
                    mm.touch(.2)
                    time.sleep(2)
                mm.motorGoToXYAndTouch(1277,795,0.2) # buji confirm
                while client.isBusy: time.sleep(1)
                while not self.capture.isScene('chuzhengzhunbei'):
                    mm.touch(.2)
                    time.sleep(2)
            mm.motorGoToXYAndTouch(963,981,0.2)  # chuzheng kaishi
            while client.isBusy: time.sleep(1)
            time.sleep(2)
            while not self.capture.isScene('zhandouzhunbei'):
                mm.touch(.2)
                time.sleep(2)
            enemy = self.capture.get_window_enemy_party()
            if enemy[0] == 'ss' or enemy[0] == 'ss+':
                mm.motorGoToXYAndTouch(1370,924,0.2) # fight
                while client.isBusy: time.sleep(1)
                while not self.capture.isScene('xuanzezhenxing'):
                    mm.touch(.2)
                    time.sleep(2)
                mm.motorGoToXYAndTouch(1556,917,0.2) # zhenxing
                while client.isBusy: time.sleep(1)
                time.sleep(1)
                mm.powerOff()
                time.sleep(1)
                while not self.capture.isScene('zhandoujieshu'): time.sleep(1)
                mm.powerOn()
                time.sleep(1)
                mm.touch(.2)
                time.sleep(2)
                mm.motorGoToXYAndTouch(1725,986,0.2) # before drop
                while client.isBusy: time.sleep(1)
                time.sleep(2)
                mm.motorGoToXYAndTouch(1188,757,0.2) # huigang
                while client.isBusy: time.sleep(1)
                time.sleep(2)
                while not self.capture.isScene('huigang'):
                    mm.touch(.2)
                    time.sleep(2)
                flagBuji += 1
            else:
                mm.motorGoToXYAndTouch(1601,924,0.2) # retreat
                while client.isBusy: time.sleep(1)
            time.sleep(2)
            while not self.capture.isScene('zhujiemian'):
                mm.touch(.2)
                time.sleep(2)

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
