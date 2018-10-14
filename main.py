from Functions import *
from Robots import Robot_Main
import cv2

cam = cv2.VideoCapture(1)
_, frame = cam.read()

main_robot = Robot_Main()


def setup():
    firstSetup(frame)
    cv2.namedWindow('Final')
    cv2.setMouseCallback('Final', onMouse)
    # print(main_robot.checkWay([200, 70]))

def main():
    global frame
    cv2.imshow('Original', frame)

    # firstSetup(frame)

    frame = removePerspective(frame)
    # frame, fields = getFields(frame)

    marker = getMarkers(frame)["centers"]
    # print(marker['2'])

    cv2.circle(frame, (marker['2'][0], marker['2'][1]), 2, (0, 0, 255), -1)
    print(getRealPos(marker['2'][0], marker['2'][1]))

    cv2.imshow('Final', frame)


while True:
    setup()
    try:
        _, frame = cam.read()  # cv2.imread('images/table.png')
        if len(m) != 4:
            firstSetup(frame)
        main()
    except Exception as e:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
