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
            print(frame)
            firstSetup(frame)
            frame, poss = removePerspective(frame)
            show('Final', frame)
            cv2.setMouseCallback('Final', onMouse)

            if cv2.waitKey(1) & 0xFF == ord('l'):
                break
        except Exception as exception:
            print(exception)


def main():
    frame = getImage()

    print(frame)

    # show('Original', frame)

    # centers = getMarkers(frame)
    # center = centers[1]
    # print(center)
    # cv2.line(frame, (center[0], center[1]), (center[0] + 100, center[1]), (0, 0, 255), 2)
    # cv2.line(frame, (center[0], center[1]), (center[0], center[1] + 100), (0, 255, 0), 2)
    # for c in centers.items():
    #     ce = c[1]
    #     cv2.circle(frame, (ce[0], ce[1]), 10, (255, 0, 0), -1)
    #     cv2.circle(frame, fixCoord(ce, center, 2), 10, (0, 0, 255), -1)



    # frame, poss = removePerspective(frame)

    # markers = getMarkers(frame, debug=False)
    # frame, pos = main_robot.getPos(frame, markers)

    show('Final', frame)


cv2.namedWindow("Final")

setup()

while True:
    try:
        main()
    except Exception as e:
        print(e)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# camA.release()
cv2.destroyAllWindows()
