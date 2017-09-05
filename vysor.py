import numpy as np
import cv2
from PIL import ImageGrab
import threading
import time
import win32gui
import scene
from path import *

# =============================================
class Vysor(object):
    RESOLUTION = [1920, 1080] # resolution of the smart phone screen
    UPDATE_PERIOD = 0.01 # capture every 0.01 sec
    dictionary = {}

    def __init__(self):
        self.frame = []
        self.rect = [0, 0, 0, 0] # x1,y1,x2,y2. capture rect in PC display coordinate
        self.width = 0
        self.height = 0
        self.init_dictionary()

    def init_dictionary(self):
        with open(PATH_DROP + "list.txt") as f:
            for line in f:
               (key, val) = line.split()
               self.dictionary[int(key)] = val

    def start(self):
        handle_thread = threading.Thread(target=self._handler, daemon=True)
        handle_thread.start()

    def _handler(self):
        while True:
            self.frame = ImageGrab.grab()
            time.sleep(self.UPDATE_PERIOD)

    def get_window(self):
        img = self.frame.copy()
        rgb = self.fmtConvert(img)
        x1, y1, x2, y2 = tuple(self.rect)
        gamescr = rgb[y1:y2,x1:x2]
        cv2.imshow("Region of Interest", gamescr)
        cv2.waitKey(0)

    def get_window_party_hp(self):
        img = self.frame.copy()
        rgb = self.fmtConvert(img)
        x1, y1, x2, y2 = tuple(self.rect)
        gamescr = rgb[y1:y2,x1:x2]
        crop = self.crop(gamescr,465,585,1650,619)
        print(scene.detectHP(crop))
        # cv2.imshow("Region of Interest", crop)
        # cv2.waitKey(0)

    def get_window_enemy_party(self):
        img = self.frame.copy()
        rgb = self.fmtConvert(img)
        x1, y1, x2, y2 = tuple(self.rect)
        gamescr = rgb[y1:y2,x1:x2]
        crop = self.crop(gamescr,195,305,972,840)
        # cv2.imshow("Region of Interest", crop)
        # cv2.waitKey(0)
        scene.detectEnemy(crop)

    def get_window_drop(self):
        img = self.frame.copy()
        rgb = self.fmtConvert(img)
        x1, y1, x2, y2 = tuple(self.rect)
        gamescr = rgb[y1:y2,x1:x2]
        crop = self.crop(gamescr,720,120,1200,800)
        # cv2.imshow("Region of Interest", crop)
        # cv2.waitKey(0)
        # cv2.imwrite('drop.png', crop)
        scene.detectDrop(crop,self.dictionary)

    def set_wh(self):
        self.width = self.rect[2] - self.rect[0]
        self.height = self.rect[3] - self.rect[1]

    def fmtConvert(self,img):
        bgr = np.array(img)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return rgb

    def xyConvert(self,x,y):
        nx = int(x / self.RESOLUTION[0] * self.width)
        ny = int(y / self.RESOLUTION[1] * self.height)
        return (nx, ny)

    def crop(self,img,x1,y1,x2,y2):
        nx1, ny1 = self.xyConvert(x1,y1)
        nx2, ny2 = self.xyConvert(x2,y2)
        crop = img[ny1:ny2,nx1:nx2]
        return crop
