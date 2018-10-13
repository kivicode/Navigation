from typing import List, Any
from webcolors import *
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

m = []

fields = []

def nothing(x):
    pass


def getFields(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 5, 17, 17)[:300, :] #11 17 17
    edged = cv2.Canny(gray, 20, 150) #30 200
    img2, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    rectangles = []
    cv2.imshow("Gray", img2)
    i = 0
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area <= 4500 and area >= 1000:
            rect = getBoundingRect(cnt)
            cropped = image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
            color = getObjectColor(cropped) #bgr
            print(color)
            label = closest_colour(color)
            r = Rect(rect[0], rect[1], color=color, label=label)
            rectangles.append(r)
    flds = []
    for r in rectangles:
        check = True
        for a in rectangles:
            if r != a and check:
                if not r.isInside(a):
                    rectangles.remove(r)
                    check = False
        if check:
            image = r.draw(image)
            flds.append(r)
    return image, cnts

def closest_colour(requested_colour):
    # min_colours = {}
    # for key, name in css3_hex_to_names.items():
    #     r_c, g_c, b_c = hex_to_rgb(key)
    #     rd = (r_c - requested_colour[0]) ** 2
    #     gd = (g_c - requested_colour[1]) ** 2
    #     bd = (b_c - requested_colour[2]) ** 2
    #     min_colours[(rd + gd + bd)] = name
    # return min_colours[min(min_colours.keys())]
    best = int(sorted(requested_colour)[2])
    b = int(requested_colour[0])
    g = int(requested_colour[1])
    r = int(requested_colour[2])
    if best == r:
        return "red"
    elif best == g:
        return "green"
    elif best == b:
        return "blue"

def getObjectColor(img):
    return (np.average(img, axis=0)[0][0], np.average(img, axis=0)[0][1], np.average(img, axis=0)[0][2])


def drawContours(frame, arr, color=(25, 105, 255)):
    for cnt in arr:
        cv2.drawContours(frame, [cnt], -1, color, 3)
    return frame


def getRoves(FieldObjects):
    out = []
    sortied = sorted(FieldObjects, key=lambda contour: cv2.contourArea(contour))
    for cnt in sortied:
        area = cv2.contourArea(cnt)
        if 30 < area <= 200:
            out.append(cnt)
    return out

def firstSetup(img):
    global m
    m = getMarkers(img)["markers"]

def removePerspective(second):
    global m
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


def getBoundingRotatedRect(cnt):
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box


def getBoundingRect(cnt, margin=None):
    if margin is None:
        margin = [(0, 0), (0, 0)]
    x, y, w, h = cv2.boundingRect(cnt)
    return (x + margin[0][0], y + margin[0][1]), (x + w + margin[1][0], y + h + margin[1][1])


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
            cv2.rectangle(gray, (cur[0][0], cur[0][1]), (cur[2][0], cur[2][1]), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray, str(ids[i][0]), (center[0], center[1]), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            markers[ids[i][0]] = (center[0], center[1])
            cv2.imshow("G", gray)
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
            r, g, b = img[y, x]
            r_total += r
            g_total += g
            b_total += b
            count += 1
    if count == 0:
        return (0, 0, 0)
    return r_total / count, g_total / count, b_total / count


class Rect:
    def __init__(self, f, t, label="", color=(0, 0, 0)):
        self.leftUp = f
        self.rightDown = t
        self.label = label
        self.color = color

    def draw(self, image, color=None):
        cv2.rectangle(image, self.leftUp, self.rightDown, self.color if color==None else color, -1)
        cv2.putText(image, str(self.label), (self.leftUp[0]-3, self.leftUp[1]+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
        return image

    def getCenter(self):
        return int((self.leftUp[0] + self.rightDown[0]) / 2), int((self.leftUp[1] + self.rightDown[1]) / 2)

    def S(self):
        w = abs(self.leftUp[0] - self.rightDown[0])
        h = abs(self.leftUp[1] - self.rightDown[1])
        return w*h

    def P(self):
        w = abs(self.leftUp[0] - self.rightDown[0])
        h = abs(self.leftUp[1] - self.rightDown[1])
        return 2*(w+h)

    def isInside(self, a):
        return not (self.leftUp[0] < a.leftUp[0] and self.leftUp[1] < a.leftUp[1] and self.rightDown[0] > a.rightDown[0] and self.rightDown[1] > a.rightDown[1])
