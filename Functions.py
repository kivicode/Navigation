import cv2
import cv2.aruco as aruco
import numpy as np
import imutils

camA = cv2.VideoCapture(1)

fieldWidth = 730
fieldHeight = 345

screenWidth = 730
screenHeight = 345

position = []

markerPositions = {}
perspectM = None

order = [1, 2, 3, 6]

'''
    order[1]       order[2]
    
    
    
    order[0]       order[3]
'''


def nothing(x):
    pass


def getImage():
    _, frameA = camA.read()
    return frameA


def show(name, frame, rpi = False):
    return cv2.imshow(name, imutils.resize(frame, height=600) if rpi else frame)


def firstSetup(img):
    global markerPositions
    markerPositions = getMarkers(img)


def removePerspective(second):
    m = correctPositions()
    src = np.float32([m[order[0]],
                      m[order[1]],
                      m[order[2]],
                      m[order[3]]])

    w, h = screenWidth, screenHeight
    dst = np.float32([(0, h),
                      (0, 0),
                      (w, 0),
                      (w, h)])

    nh, nw = second.shape[:2]
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(second, M, (nw, nh), flags=cv2.INTER_LINEAR)
    return warped, perspectM


def correctPositions():
    m = markerPositions
    scale = 4
    center = getCenter(m)
    nm = {
        1: [(m[order[0]][0] - center[0]) * scale + center[0], (m[order[0]][1] - center[1]) * scale + center[1]],
        2: [(m[order[1]][0] - center[0]) * scale + center[0], (m[order[1]][1] - center[1]) * scale + center[1]],
        3: [(m[order[2]][0] - center[0]) * scale + center[0], (m[order[2]][1] - center[1]) * scale + center[1]],
        6: [(m[order[3]][0] - center[0]) * scale + center[0], (m[order[3]][1] - center[1]) * scale + center[1]]
    }

    return nm


def getCenter(m):
    mx = (m[1][0] + m[2][0] + m[3][0] + m[6][0]) / 4
    my = (m[1][1] + m[2][1] + m[3][1] + m[6][1]) / 4
    return [mx, my]


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


def onMouse(event, x, y, a, b):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = getRealPos(x, y)
        print("X: " + str(position[0]) + "mm\tY: " + str(position[1]) + "mm")


def getMarkers(gray, debug=False):
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
            cv2.circle(gray, (center[0], center[1]), 2, (0, 0, 255), -1)

            markers[ids[i][0]] = (center[0], center[1])
            if debug:
                cv2.imshow("G", gray)
            i += 1
    return markers
