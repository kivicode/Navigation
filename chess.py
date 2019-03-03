import sys

import numpy as np
import cv2

from Functions import removePerspective, fixCoord, getMarkers

cam = cv2.VideoCapture(0)

W = 9
H = 6


def IX(x, y):
    return y * W + x


setup = True
src = None

points = []
while True:
    img = cam.read()[1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    getMarkers(img)

    cv2.imshow('dst', img)
    if cv2.waitKey(1) & 0xff == 27:
        break
cv2.destroyAllWindows()
