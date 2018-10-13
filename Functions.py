from typing import List, Any

import cv2
import cv2.aruco as aruco
import math
import numpy as np

fieldWidth = 3000
fieldHeight = 1000

screenWidth = 593
screenHeight = 383

green = [[65, 128, 62], 36, 110]
blue = [[176, 124, 45], 26, 39]
red = []

position = []

def nothing(x):
    pass

def getContours(im):
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return im

def drawContours(frame, arr, color=(25, 105, 255)):
    for cnt in arr:
        cv2.drawContours(frame, [cnt], -1, color, -1)
    return frame



def getFields(FieldObjects):
    sortied = sorted(FieldObjects, key=lambda cnt: cv2.contourArea(cnt))
    box = getBoundingRect(sortied[len(sortied) - 1])
    box1 = getBoundingRect(sortied[len(sortied) - 3])
    return [box, box1]


def getRoves(FieldObjects):
    out = []
    sortied = sorted(FieldObjects, key=lambda contour: cv2.contourArea(contour))
    for cnt in sortied:
        area = cv2.contourArea(cnt)
        if 30 < area <= 200:
            out.append(cnt)
    return out


def removePerspective(img, second):

    m = getMarkers(img)["markers"]
    src = np.float32([m[1],
                      m[2],
                      m[3],
                      m[6]])

    dst = np.float32([(0, 400),
                      (0, 0),
                      (600, 0),
                      (600, 400)])

    h, w = second.shape[:2]
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(second, M, (w, h), flags=cv2.INTER_LINEAR)
    return warped


def getBoundingRect(cnt):
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box


def getRealPos(x, y):
    px = x / screenWidth
    py = y / screenHeight
    ox = px * fieldWidth
    oy = py * fieldHeight
    return [int(ox), int(oy)]


def getRandomColor():
    return 255 * np.random.random_sample(), 255 * np.random.random_sample(), 255 * np.random.random_sample()


def onMouse(event, x, y, a, b):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = getRealPos(x, y)
        print("X: " + str(position[0]) + "mm\tY: " + str(position[1]) + "mm")


def getMarkers(gray):
    markers = {}
    parameters = aruco.DetectorParameters_create()
    dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary,
                                                          parameters=parameters)
    centers = []
    i = 0

    for corner in corners:
        for cur in corner:
            center = [int((cur[0][0] + cur[2][0]) / 2), int((cur[0][1] + cur[2][1]) / 2)]
            centers.append(center)
            # cv2.circle(gray, (center[0], center[1]), 2, (0, 0, 255), -1)
            # cv2.rectangle(gray, (cur[0][0], cur[0][1]), (cur[2][0], cur[2][1]), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray, str(ids[i][0]), (center[0], center[1]), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            markers[ids[i][0]] = (center[0], center[1])
            i += 1
    return {"frame": gray, "centers": centers, "markers": markers}


def average_color(img):
    height, width, _ = img.shape

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img[y,x]
            r_total += r
            g_total += g
            b_total += b
            count += 1
    if count == 0:
        return (0,0,0)
    return (r_total/count, g_total/count, b_total/count)

def test_calibrate(img, x, y):
    edges = cv2.Canny(img,x,y)
    return edges
