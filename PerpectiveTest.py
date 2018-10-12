import numpy as np
import cv2
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    gray = cv2.imread('images/marker.png')
    # print(frame.shape) #480x640
    # Our operations on the frame come here
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    for corner in corners:
        for cur in corner:
            print(cur)
            center = [int((cur[0][0]+cur[2][0])/2), int((cur[0][1]+cur[2][1])/2)]
            cv2.circle(gray, (center[0], center[1]), 2, (0, 0, 255), -1)
            cv2.rectangle(gray, (cur[0][0], cur[0][1]), (cur[2][0], cur[2][1]), (0, 255, 0), 3)

    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()