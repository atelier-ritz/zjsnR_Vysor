# ==================================
# import lib
# ==================================
import cv2
import numpy as np
from PIL import Image
import sys
import math
from matplotlib import pyplot as plt
from operator import itemgetter
from path import *

def detectHP(img):
    hp = []
    height, width = img.shape[:2]
    singleWidth = int(width/6)
    # print(width,height)
    print('====== Party HP detection result ======')
    for i in range(6):
        crop = img[int(height*0.4):int(height*0.6),int(singleWidth*(i+0.1)):int(singleWidth*(i+0.15))]
        # crop = img[5:height-5,int(singleWidth*i):int(singleWidth*(i+1))]
        # cv2.imshow("Region of Interest", crop)
        # cv2.waitKey(0)
        average_color_per_row = np.average(crop, axis=0)
        average_color = np.average(average_color_per_row, axis=0)
        # print(average_color)
        b = average_color[0]
        g = average_color[1]
        r = average_color[2]
        if r > 100:
            if g > 100:
                if b > 100:
                    hp.append(None)
                else:
                    hp.append('yellow')
            else:
                hp.append('red')
        else:
            hp.append('green')
    return hp

def detectEnemy(img):
    enemy = []
    height, width = img.shape[:2]
    singleWidth = int(width/2)
    singleHeight = int(height/3)
    capturedHist = []
    print('====== Enemy type detection result ======')
    i=1
    # for i in range(6):
    x = singleWidth * (i % 2)
    y = singleHeight * math.floor(i / 2)
    crop = img[y:int(y+singleHeight*0.68),x:int(x+singleWidth*0.95)]
    # cv2.imwrite('{}.png'.format(i), crop)
    enemyType = getEnemyType61(crop)
    enemy.append(enemyType)
    print("{} - {}".format(i+1,enemyType))
    return enemy

def getEnemyType61(imgOfOneEnemy):
    hist = getHistBGR(imgOfOneEnemy)
    sample = ['clt','cv','ss','ss+','none','cl','dd','bc','ca+','ca','ca_b','cl+','dd+','ss++']
    sampleImgs = [cv2.imread(PATH_ENEMY_ICON + imgName + ".png") for imgName in sample]
    sampleHist = [getHistBGR(sampleImg) for sampleImg in sampleImgs]
    similarity = {} # {name1:similarity1,name2: similarity2,...}
    for i,h in enumerate(sampleHist):
        d = compareHistBGR(hist,h)
        similarity[sample[i]] = d
    # print(similarity)
    enemyType = max(similarity.keys(), key=(lambda key: similarity[key]))
    return enemyType

def detectDrop(img,dictionary):
    hist = getHistBGR(img)
    sample = ['1','2']
    sampleImgs = [cv2.imread(PATH_DROP + imgName + ".png") for imgName in sample]
    sampleHist = [getHistBGR(sampleImg) for sampleImg in sampleImgs]
    similarity = {} # {name1:similarity1,name2: similarity2,...}
    for i,h in enumerate(sampleHist):
        d = compareHistBGR(hist,h)
        similarity[sample[i]] = d
    # print(similarity)
    dropID = max(similarity.keys(), key=(lambda key: similarity[key]))
    print('====== Detect drop result ======')
    print(dictionary[int(dropID)])

def detectScene(img,sceneName):
    hist = getHistBGR(img)
    sampleImg = cv2.imread(PATH_SCENE + sceneName + ".png")
    sampleHist = getHistBGR(sampleImg)
    similarity = compareHistBGR(hist,sampleHist)
    print(similarity)
    if similarity > 2.7:
        return True
    return False

def compareHistBGR(imghist1,imghist2):
    similarityBGR = []
    for i in range(3):
        d = cv2.compareHist(imghist1[i], imghist2[i], method=0)
        similarityBGR.append(d)
    similarity = sum(similarityBGR)
    return similarity

def getHistBGR(img):
    color = ('b','g','r')
    histBGR = []
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        histBGR.append(histr)
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    return histBGR





















    # akaze = cv2.AKAZE_create()
    # bf = cv2.BFMatcher()
    # _, des = akaze.detectAndCompute(img, None)
    #
    # sample = ['clt','cv','ss','ss+','none']
    # sampleImgs = [cv2.imread(imgName + ".png") for imgName in sample]
    # sampleDes = []
    # sampleKp = []
    # for sampleImg in sampleImgs:
    #     kp, des =  akaze.detectAndCompute(sampleImg, None)
    #     sampleDes.append(des)
    #     sampleKp.append(kp)
    # for i,contents in enumerate(sampleDes):
    #     matches = bf.knnMatch(des, contents, k=2)
    #     good = []
    #     for m, n in matches:
    #         if m.distance < 0.5 * n.distance:
    #             good.append([m])
    #     print(len(good))
    #     img3 = cv2.drawMatchesKnn(img, kp, sampleImgs[i], sampleKp[i], good, None, flags=2)
    #     cv2.imshow('Comparison',img3)
    #     cv2.waitKey(0)
    #     if len(good) > 5:
    #         print('Detection Result: This is ' + sample[i] + '.')
    #         break
