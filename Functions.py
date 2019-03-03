import cv2
import cv2.aruco as aruco
import numpy as np
import imutils

camA = cv2.VideoCapture(0)

import freenect

fieldWidth = 730
fieldHeight = 345

screenWidth = 730
screenHeight = 345

position = []

markerPositions = {}
perspectM = None

order = [0, 1, 2, 3]

poss = []

'''
    order[1]       order[2]
    
    
    
    order[0]       order[3]
'''


def nothing(x):
    pass


def getImage():
    _, frameA = camA.read()
    return frameA
    # return cv2.imread('images/test_img.jpg')


def show(name, frame, rpi=False):
    return cv2.imshow(name, imutils.resize(frame, height=600) if rpi else frame)


def firstSetup(img):
    global markerPositions
    markerPositions = getMarkers(img)


def removePerspective(second, src):
    w, h = 700, 500
    dst = np.float32([(0, h),
                      (0, 0),
                      (w, 0),
                      (w, h)])

    nh, nw = second.shape[:2]
    M = cv2.getPerspectiveTransform(np.array([src], np.float32), dst)
    warped = cv2.warpPerspective(second, M, (nw, nh), flags=cv2.INTER_LINEAR)
    return warped


def correctPositions(m, scale, first):
    center = m[first]

    nm = [
        fixCoord(m[0], center, scale),
        fixCoord(m[1], center, scale),
        fixCoord(m[2], center, scale),
        fixCoord(m[3], center, scale)
    ]
    return nm


def drawCoordSys(img, center):
    cv2.line(img, (center[0], center[1]), (center[0] + 100, center[1]), (0, 0, 255), 2)
    cv2.line(img, (center[0], center[1]), (center[0], center[1] + 100), (0, 255, 0), 2)
    return img


def fixCoord(m, center, scale):
    return (m[0] - center[0]) * scale + center[0], (m[1] - center[1]) * scale + center[1]


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


mpos = [0, 0]


def onMouse(event, x, y, a, b):
    global position, mpos
    if event == cv2.EVENT_LBUTTONDBLCLK:
        position = [x, y]
        poss.append(position)
        print("X: " + str(position[0]) + "mm\tY: " + str(position[1]) + "mm")
    if event == cv2.EVENT_LBUTTONDOWN:
        mpos[0] = x
        mpos[1] = y
        print("X: " + str(position[0]) + "mm\tY: " + str(position[1]) + "mm")


def perpend(l1, l2, dst):
    x1, y1 = l1
    x2, y2 = l2
    x3, y3 = dst
    k = ((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)) / (((y2 - y1) ** 2) + ((x2 - x1) ** 2))
    x4 = x3 - k * (y2 - y1)
    y4 = y3 + k * (x2 - x1)
    to = (int(x4), int(y4))
    return to


def dist(p1, p2):
    return np.math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def getMarkers(gray, debug=False):
    markers = {}
    parameters = aruco.DetectorParameters_create()
    dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)
    cornerss, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary,
                                                           parameters=parameters)
    centers = {}
    i = 0
    for corners in cornerss:
        for cur in corners:
            center = [int((cur[0][0] + cur[2][0]) / 2), int((cur[0][1] + cur[2][1]) / 2)]
            centers[str(ids[i][0])] = center

            markers[ids[i][0]] = (center[0], center[1])
            if debug:
                cv2.circle(gray, (center[0], center[1]), 20, (0, 0, 255), -1)
                cv2.putText(gray, str(ids[i][0]), (center[0], center[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2,
                            cv2.LINE_AA)
                cv2.imshow("G", gray)
            i += 1
    return markers


def get_depth_map():
    array, _ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array


def slider(win, name, f, t):
    cv2.createTrackbar(name, win, f, t, lambda x: 0)


def get(win, name):
    return cv2.getTrackbarPos(name, win)


def line_interception(l11, l12, l21, l22):
    x1, y1 = l11
    x2, y2 = l12
    x3, y3 = l21
    x4, y4 = l22
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

    intersectionX = int(x1 + (uA * (x2 - x1)))
    intersectionY = int(y1 + (uA * (y2 - y1)))

    return intersectionX, intersectionY


def get_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2
    return np.math.degrees(np.math.atan2(det, dot))


def angle_between_points(p0, p1, p2):
    a = (p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2
    b = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    c = (p2[0] - p0[0]) ** 2 + (p2[1] - p0[1]) ** 2
    return np.math.acos((a + b - c) / np.math.sqrt(4 * a * b)) * 180 / np.math.pi


def rotate(origin, point, angle):
    """angle in degrees"""
    angle = np.math.radians(-angle)
    ox, oy = origin
    px, py = point

    qx = ox + np.math.cos(angle) * (px - ox) - np.math.sin(angle) * (py - oy)
    qy = oy + np.math.sin(angle) * (px - ox) + np.math.cos(angle) * (py - oy)
    return int(qx), int(qy)


def mult(v, k):
    return v[0] * k, v[1] * k
