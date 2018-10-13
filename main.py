from Functions import *
import cv2
import time

debug = False
loop = True

FieldObjects = []
fps = 1/1

firstFrame = True

cam = cv2.VideoCapture(0)

while loop:
    start_time = time.time()

    frame = cv2.imread('images/table.png')
    # _, frame = cam.read()

    cv2.imshow('Original', frame)


    frame = removePerspective(cv2.imread('images/table3.png'), frame)

    frame = getFields(frame)[0]

    cv2.imshow('Final', frame)
    cv2.setMouseCallback('Final', onMouse)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    while abs(start_time-time.time()) < 1/fps and not firstFrame:
        a=0
    firstFrame = False

cam.release()
cv2.destroyAllWindows()
