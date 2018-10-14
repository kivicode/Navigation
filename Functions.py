from typing import List, Any
from webcolors import *
from ImageProcessing import *
import cv2
import cv2.aruco as aruco
import math
import numpy as np

camA = cv2.VideoCapture(1)
camB = cv2.VideoCapture(2)

fieldWidth = 730
fieldHeight = 345

screenWidth = 730
screenHeight = 345

green = [[65, 128, 62], 36, 110]
blue = [[176, 124, 45], 26, 39]
red = []

position = []

markerPositions = {}

Sfields = {
    "A": {
        "red": {"pos": [[0, 35], [90, 70]], "color": (0, 0, 255)},
        "green": {"pos": [[0, 70], [90, 104]], "color": (0, 255, 0)},
        "blue": {"pos": [[0, 104], [92, 137]], "color": (255, 0, 0)}
    },
    "B": {
        "red": {"pos": [[515, 45], [595, 71]], "color": (0, 0, 255)},
        "green": {"pos": [[510, 75], [595, 104]], "color": (0, 255, 0)},
        "blue": {"pos": [[510, 107], [590, 134]], "color": (255, 0, 0)}
    }
}


def nothing(x):
    pass


def getImage():
    _, frameA = camA.read()
    _, frameB = camB.read()
    return mergeImages(frameA, frameB)


def getFields(image):
    flds = {}
    poss = {}
    for A in Sfields["A"].items():
        name = A[0]
        params = A[1]
        pos = params["pos"]
        color = params["color"]
        center = (int((pos[0][0]+pos[1][0])/2)-10, int((pos[0][1]+pos[1][1])/2)-5)
        poss[name] = [center]
        cv2.circle(image, center, 5, color, -1)
    flds["A"] = poss
    poss = {}

    for B in Sfields["B"].items():
        name = B[0]
        params = B[1]
        pos = params["pos"]
        color = params["color"]
        center = (int((pos[0][0]+pos[1][0])/2)+10, int((pos[0][1]+pos[1][1])/2)-17)
        poss[name] = [center]
        cv2.circle(image, center, 5, color, -1)
    flds["B"] = poss
    return image, flds


def getFields_Beta(image, fa, fb, fc, ca, cb):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, fa, fb, fc)[:140, :]  # 11 17 17
    edged = cv2.Canny(gray, ca, cb)  # 30 200
    img2, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    rectangles = []
    cv2.imshow("Gray", img2)
    i = 0
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area <= 4000 and area >= 1000:
            print(area)
            rect = getBoundingRect(cnt)
            cropped = image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
            color = getObjectColor(cropped)  # bgr
            # print(color)
            label = closest_colour(color)
            r = Rect(rect[0], rect[1], color=color, label=label)
            # image = r.draw(image)
            rectangles.append(r)

    return image, cnts


def closest_colour(requested_colour):
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
    return np.average(img, axis=0)[0][0], np.average(img, axis=0)[0][1], np.average(img, axis=0)[0][2]


def drawContours(frame, arr, color=(25, 105, 255)):
    for cnt in arr:
        cv2.drawContours(frame, [cnt], -1, color, 3)
    return frame


def getRoves(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 5, 17, 17)
    edged = cv2.Canny(gray, 20, 150)  # 30 200
    img2, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea)
    rectangles = []
    cv2.imshow("Gray", img2)
    i = 0
    for cnt in cnts:
        area = cv2.contourArea(cnt)

        rect = getBoundingRect(cnt)
        cropped = image[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
        r = Rect(rect[0], rect[1])
        center = r.getCenter()
        # and not center[0] in range(104, 518) and not center[1] in range(328, 387)
        if r.S() > 200 and r.S() < 1000:
            image = r.draw(image)
            rectangles.append(r)
            print(area)

    return image, cnts


def firstSetup(img):
    global markerPositions
    markerPositions = getMarkers(img)["markers"]


perspectM = None
def removePerspective(second):
    m = markerPositions
    perspectM = m
    src = np.float32([m[1],
                      m[2],
                      m[3],
                      m[6]])

    w, h = screenWidth, screenHeight
    dst = np.float32([(0, h),
                      (0, 0),
                      (w, 0),
                      (w, h)])

    nh, nw = second.shape[:2]
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(second, M, (nw, nh), flags=cv2.INTER_LINEAR)
    return warped[:h, :w], perspectM


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
    centers = {}
    i = 0
    for corner in corners:
        for cur in corner:
            center = [int((cur[0][0] + cur[2][0]) / 2), int((cur[0][1] + cur[2][1]) / 2)]
            centers[str(ids[i][0])] = center
            # cv2.circle(gray, (center[0], center[1]), 2, (0, 0, 255), -1)
            # cv2.rectangle(gray, (cur[0][0], cur[0][1]), (cur[2][0], cur[2][1]), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(gray, str(ids[i][0]), (center[0], center[1]), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            markers[ids[i][0]] = (center[0], center[1])
            # cv2.imshow("G", gray)
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
        return 0, 0, 0
    return r_total / count, g_total / count, b_total / count


def initBar(name, f, t):
    cv2.createTrackbar(name, 'Original', f, t, nothing)


def getBar(name):
    return cv2.getTrackbarPos(name, 'Original')


class Rect:
    def __init__(self, f, t, label="", color=(0, 0, 0)):
        self.leftUp = f
        self.rightDown = t
        self.label = label
        self.color = color

    def draw(self, image, color=None):
        cv2.rectangle(image, self.leftUp, self.rightDown, (0, 0, 0), -1)
        # cv2.putText(image, str(self.label), (self.leftUp[0] - 3, self.leftUp[1] + 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (0, 0, 0), 1, cv2.LINE_AA)
        return image

    def getCenter(self):
        return int((self.leftUp[0] + self.rightDown[0]) / 2), int((self.leftUp[1] + self.rightDown[1]) / 2)

    def S(self):
        w = abs(self.leftUp[0] - self.rightDown[0])
        h = abs(self.leftUp[1] - self.rightDown[1])
        return w * h

    def P(self):
        w = abs(self.leftUp[0] - self.rightDown[0])
        h = abs(self.leftUp[1] - self.rightDown[1])
        return 2 * (w + h)

    def isInside(self, a):
        return not (self.leftUp[0] < a.leftUp[0] and self.leftUp[1] < a.leftUp[1] and self.rightDown[0] > a.rightDown[
            0] and self.rightDown[1] > a.rightDown[1])

def dist(a, b):
    dx = abs(a[0]-b[0])
    dy = abs(a[1]-b[1])
    return math.sqrt(dx**2 + dy**2)