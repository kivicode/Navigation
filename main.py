from Functions import *
from Robots import Robot_Main
import cv2

cam = cv2.VideoCapture(1)
_, frame = cam.read()


def setup():
    firstSetup(frame)


def main():
    _, frame = cam.read()  # cv2.imread('images/table.png')
    cv2.imshow('Original', frame)

    firstSetup(frame)

    frame = removePerspective(frame)
    frame, fields = getFields(frame)
    print(fields)

    cv2.imshow('Final', frame)
    cv2.setMouseCallback('Final', onMouse)


while True:
    setup()
    try:
        main()
    except Exception as e:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
