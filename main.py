from Functions import *
import cv2
import time

debug = False
loop = True

FieldObjects = []
fps = 0

cam = cv2.VideoCapture(0)

while loop:
    start_time = time.time()

    frame = cv2.imread('images/table.png')
    # _, frame = cam.read()

    cv2.imshow('Original', frame)



    frame = removePerspective(cv2.imread('images/table3.png'), frame)

    FieldObjects = [
        colorMask(frame, green, )[1][1],
        colorMask(frame, blue)[1][1]
    ]

    for cnt in getFields(FieldObjects[0]):
        cv2.drawContours(frame, [cnt], 0, (0, 255, 0), -1, cv2.LINE_AA)

    for cnt in getFields(FieldObjects[1]):
        cv2.drawContours(frame, [cnt], 0, (255, 0, 0), -1, cv2.LINE_AA)

    FieldObjects = [
        colorMask(frame, green)[1][1],
        colorMask(frame, blue)[1][1]
    ]

    for cnt in getRoves(FieldObjects[0]):
        cv2.drawContours(frame, [getBoundingRect(cnt)], 0, (0, 255, 255), -1, cv2.LINE_AA)

    for cnt in getRoves(FieldObjects[1]):
        cv2.drawContours(frame, [getBoundingRect(cnt)], 0, (255, 0, 255), -1, cv2.LINE_AA)


    cv2.imshow('Final', frame)
    cv2.setMouseCallback('Final', onMouse)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    fps = int(1.0 / (time.time() - start_time))
cam.release()
cv2.destroyAllWindows()
