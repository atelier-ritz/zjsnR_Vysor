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
    window = GUI()
    window.move(0, 0)
    window.show()
    sys.exit(app.exec_())
