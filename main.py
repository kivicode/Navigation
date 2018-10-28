from Functions import *
from Robots import Robot_Main
import cv2
import time

main_robot = Robot_Main(5)


#
#
def setup():
    while True:
        try:
            frame = getImage()
            firstSetup(frame)
            frame, poss = removePerspective(frame)
            show('Final', frame)
            cv2.setMouseCallback('Final', onMouse)
            if cv2.waitKey(1) & 0xFF == ord('l'):
                break
        except Exception as exception:
            print(exception)


cv2.namedWindow("Final")


def main():
    frame = getImage()

    show('Original', frame)

    frame, poss = removePerspective(frame)

    markers = getMarkers(frame, debug=False)
    frame, pos = main_robot.getPos(frame, markers)

    show('Final', frame)


setup()
while True:
    try:
        main()
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camA.release()
cv2.destroyAllWindows()
