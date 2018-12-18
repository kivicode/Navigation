import cv2
import cv2.aruco as aruco
import numpy as np
import imutils

# camA = cv2.VideoCapture(1)

import freenect

fieldWidth = 730
fieldHeight = 345

screenWidth = 730
screenHeight = 345

position = []

markerPositions = {}
perspectM = None

order = [0, 1, 2, 3]

'''
    order[1]       order[2]
    
    
    
    order[0]       order[3]
'''


def nothing(x):
    pass


def getImage():
    # _, frameA = camA.read()
    # return frameA
    return cv2.imread('images/test_img.jpg')


def show(name, frame, rpi=False):
    return cv2.imshow(name, imutils.resize(frame, height=600) if rpi else frame)


def firstSetup(img):
    global markerPositions
    markerPositions = getMarkers(img)


def removePerspective(second, m):
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
    return warped


def correctPositions():
    # mult by 6,66
    # (221, 204)
    m = markerPositions
    scale = 4
    print(m)
    center = m[1]
    print(m[1])

    nm = {
        order[0]: fixCoord(m[order[0]], center, scale),
        order[1]: fixCoord(m[order[1]], center, scale),
        order[2]: fixCoord(m[order[2]], center, scale),
        order[3]: fixCoord(m[order[3]], center, scale)
    }

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
            # cv2.circle(gray, (center[0], center[1]), 20, (0, 0, 255), -1)
            cv2.putText(gray, str(ids[i][0]), (center[0], center[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2,
                        cv2.LINE_AA)

            markers[ids[i][0]] = (center[0], center[1])
            if debug:
                cv2.imshow("G", gray)
            i += 1
    return markers

def get_depth_map():
    array, _ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array