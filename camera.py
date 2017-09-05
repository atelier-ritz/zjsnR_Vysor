#!/usr/bin/python3

# ==================================
# import lib
# ==================================
import cv2
import sys
import imgprocess as ip

# ==================================
# Class MyCamera
# ==================================
class MyCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        print('Camera working = {}'.format(self.cap.isOpened()))
        if not self.cap.isOpened():
            print('End program')
            self.cap.release()
            sys.exit()

        self.rectCnt = [] # tl(x,y) tr(x,y) bl(x,y) br(x,y) detected contour coordinate on the original image
        self.paraWarpedScreenSize = [0,0] # maxwidth, maxheight
        self.matWarp = None # perspective warp matrix
        self.guiFlagReferenceChanged = False
        # Mode Selection
        self.isTuningMode = True
        # Canny Edge
        self.paraCanny = [100,200] #low, high
        self.flagShowEdge = False
        # Gaussian Blur
        self.paraGaussianBlurSize = 1
        self.flagShowBlur = False
        # Contour Detection
        self.paraContourDetect = [5,20] # sample #, epsilon
        self.flagShowContous = False
        # Screen Detection
        self.flagDefineScreen = False
        self.flagShowWarp = False
        # Show Reference Line
        self.paraReferenceRect = [0,0,0.3,0.2]   #px,py,pw,ph range[0~1]
        self.mouseRectEventClick = [0,0,0,0]
        self.flagShowReference = False
        # Crop'n'show Button
        self.flagCropAndShow = False

        cv2.namedWindow("Realtime Capture")
        cv2.setMouseCallback("Realtime Capture", self.draw_rect_mouse)

    def update(self):
        _, frame = self.cap.read()
        if self.isTuningMode:
            self.update_tuning_mode(frame.copy())
        else:
            self.update_screen_mode(frame.copy())
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            self.cap.release()
            return -1
        return 0

    def update_tuning_mode(self,color):
        grey = cv2.cvtColor(color.copy(), cv2.COLOR_BGR2GRAY)
        grey = self.blur_and_canny(grey)
        if self.flagShowContous:
            screenCnt = ip.biggest_square_contour(grey,sampleNum = self.paraContourDetect[0],epsilon = self.paraContourDetect[1])
            if not screenCnt == []:
                cv2.drawContours(color, [screenCnt], -1, (0, 255, 0), 3)
            cv2.imshow('Realtime Capture',color)
            return
        cv2.imshow('Realtime Capture',grey)

    def blur_and_canny(self,grey):
        if self.flagShowBlur:
            grey = cv2.GaussianBlur(grey, (self.paraGaussianBlurSize,self.paraGaussianBlurSize),0)
        if self.flagShowEdge:
            grey = cv2.Canny(grey,self.paraCanny[0],self.paraCanny[1])
        return grey

    def update_screen_mode(self,img):
        if self.flagDefineScreen:
            self.flagDefineScreen = False
            self.define_screen_rect(img.copy())
        if self.flagShowWarp:
            if not sum(self.paraWarpedScreenSize) == 0:
                M = self.matWarp
                maxWidth = self.paraWarpedScreenSize[0]
                maxHeight = self.paraWarpedScreenSize[1]
                img = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
                if self.flagShowReference:
                    img = self.draw_rect_in_scale(img.copy(),self.paraReferenceRect)
                cv2.imshow('Realtime Capture',img)
                if self.flagCropAndShow:
                    self.flagCropAndShow = False
                    crop = self.crop_image_in_scale(img,self.paraReferenceRect)
                    cv2.imshow('Cropped Image',crop)
                return
        if len(self.rectCnt) == 4:
            img = ip.draw_rect_points(img,self.rectCnt)
        cv2.imshow('Realtime Capture',img)

    def define_screen_rect(self,color):
        grey = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        grey = self.blur_and_canny(grey)
        screenCnt = ip.biggest_square_contour(grey,sampleNum = self.paraContourDetect[0],epsilon = self.paraContourDetect[1])
        if not screenCnt == []:
            matrix, rect, maxWidth, maxHeight = ip.perspective_warp(screenCnt)
            self.matWarp = matrix
            self.rectCnt = rect
            self.paraWarpedScreenSize[0] = maxWidth
            self.paraWarpedScreenSize[1] = maxHeight

    def draw_rect_in_scale(self,img,rect):#rect[x,y,w,h] range[0~1]
        px,py,pw,ph = rect
        realWidth = self.paraWarpedScreenSize[0]
        realHeight = self.paraWarpedScreenSize[1]
        x = int(realWidth * px)
        w = int(realWidth * pw)
        y = int(realHeight * py)
        h = int(realHeight * ph)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255))
        return img

    def crop_image_in_scale(self,img,rect):#rect[x,y,w,h] range[0~1]
        px,py,pw,ph = rect
        realWidth = self.paraWarpedScreenSize[0]
        realHeight = self.paraWarpedScreenSize[1]
        x = int(realWidth * px)
        w = int(realWidth * pw)
        y = int(realHeight * py)
        h = int(realHeight * ph)
        crop = img[y:(y+h),x:(x+w)]
        return crop

    def draw_rect_mouse(self,event,x,y,flag,params):
        rect = self.mouseRectEventClick
        if event == cv2.EVENT_LBUTTONDOWN:
            rect[0] = x
            rect[1] = y
        elif event == cv2.EVENT_LBUTTONUP:
            rect[2] = x
            rect[3] = y
            rect = self.cvt_rect_value_to_scale(rect)
            self.paraReferenceRect = rect

    def cvt_rect_value_to_scale(self,rectValue): #rectValue[x1,y1,x2,y2]
        realWidth = self.paraWarpedScreenSize[0]
        realHeight = self.paraWarpedScreenSize[1]
        if realWidth == 0 or realHeight == 0:
            return [0,0,0,0]
        rectScale = [0,0,0,0]
        x1,y1,x2,y2 = rectValue
        rectScale[0] = x1/realWidth
        rectScale[1] = y1/realHeight
        rectScale[2] = (x2-x1)/realWidth
        rectScale[3] = (y2-y1)/realHeight
        self.guiFlagReferenceChanged = True
        return rectScale

# ==================================
# Callback Functions
# ==================================
    def set_bool_tuning_mode(self,boolean):
        self.isTuningMode = boolean
    def set_canny_low(self,val):
        self.paraCanny[0] = val
    def set_canny_high(self,val):
        self.paraCanny[1] = val
    def set_flag_show_edge(self,boolean):
        self.flagShowEdge = boolean
    def set_gaussian_blur_size(self,val):
        self.paraGaussianBlurSize = val
    def set_flag_show_blur(self,boolean):
        self.flagShowBlur = boolean
    def set_sample_num(self,val):
        self.paraContourDetect[0] = val
    def set_epsilon(self,val):
        self.paraContourDetect[1] = val
    def set_flag_show_contours(self,boolean):
        self.flagShowContous = boolean
    def set_flag_define_screen(self):
        self.flagDefineScreen = True
    def set_flag_show_warp(self,boolean):
        self.flagShowWarp = boolean
    def set_clip_limit(self,val):
        self.paraContrast[0] = val
    def set_grid_size(self,val):
        self.paraContrast[1] = val
    def set_flag_show_reference(self,boolean):
        self.flagShowReference = boolean
    def set_reference_x(self,val):
        self.paraReferenceRect[0] = val
    def set_reference_y(self,val):
        self.paraReferenceRect[1] = val
    def set_reference_w(self,val):
        self.paraReferenceRect[2] = val
    def set_reference_h(self,val):
        self.paraReferenceRect[3] = val
    def set_flag_crop_and_show(self):
        self.flagCropAndShow = True
