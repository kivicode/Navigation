from Functions import *
import cv2
import time

from Tests.ColorTests import *

debug = False
loop = True

FieldObjects = []
fps = 0

cam = cv2.VideoCapture(0)

def setup():
    frame = cv2.imread('images/table3.png')
    cv2.imshow('Original', frame)
    firstSetup(frame)
    if m == []:
        setup()


# setup()


while loop:
    start_time = time.time()
    # try:

    frame = cv2.imread('images/table.png')
    firstSetup(cv2.imread('images/table3.png'))

    frame = removePerspective(frame)


    frame = getFields(frame)[0]

    cv2.imshow('Final', frame)
    cv2.setMouseCallback('Final', onMouse)
        # except Exception as e:
        #     print("Markers not found", "error:", e)

    # except:
    #     print("Cam not found")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps = int(1.0 / (time.time() - start_time))
cam.release()
cv2.destroyAllWindows()
