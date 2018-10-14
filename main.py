from Functions import *
import cv2
import time

from Tests.ColorTests import *

debug = False
loop = True

FieldObjects = []
fps = 0

cam = cv2.VideoCapture(1)
_, frame = cam.read()


def setup():
    cv2.imshow('Original', frame)
    firstSetup(frame)


setup()
firstSetup(frame)
while loop:
    start_time = time.time()

    _, frame = cam.read()  # cv2.imread('images/table.png')
    cv2.imshow('Original', frame)

    try:
        firstSetup(frame)

        frame = removePerspective(frame)
        frame, fields = getFields(frame)
        print(fields)


        cv2.imshow('Final', frame)
        cv2.setMouseCallback('Final', onMouse)

    except Exception as e:
        pass  # print("Markers not found", e)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps = int(1.0 / (time.time() - start_time))
cam.release()
cv2.destroyAllWindows()
