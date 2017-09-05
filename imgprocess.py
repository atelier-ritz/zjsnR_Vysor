
import cv2
import numpy as np

def biggest_square_contour(grey,sampleNum,epsilon):
    grey, contours, hierarchy = cv2.findContours(grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:sampleNum]
    screenCnt = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon / 1000.0 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    return screenCnt

def perspective_warp(contour):
    pts = contour.reshape(4,2)
    rect = np.zeros((4,2),dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]#top-left
    rect[2] = pts[np.argmax(s)]#bottom-right
    d = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(d)]#top-right
    rect[3] = pts[np.argmax(d)]#bottom-left
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    matrix = cv2.getPerspectiveTransform(rect, dst)
    rect = np.ndarray.tolist(rect.astype(int))
    return (matrix, rect, maxWidth, maxHeight)

def draw_rect_points(img,rect):
    for i in range(4):
        x = rect[i][0]
        y = rect[i][1]
        output = cv2.circle(img, (x,y), 4, (0, 0, 255), 4)
    return output
