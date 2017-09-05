import sys
import time
from vysor import Vysor
# from camera import MyCamera
# from scenemanager import Scene
from callbacks import GUI
from PyQt5 import QtWidgets
import win32api


capture = Vysor()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # cam = MyCamera()
    # capture.start()
    window = GUI()
    window.move(0, 0)
    window.show()
    # img = capture.fmtConvert(capture.frame)
    # capture.crop(img,10,20,240,460)
        # if cam.update() == -1:
        #     break
        # window.update()
    sys.exit(app.exec_())
