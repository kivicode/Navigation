from Functions import *
from Robots import Robot_Main
import cv2

main_robot = Robot_Main(5)


def setup():
    cv2.setMouseCallback('Final', onMouse)
    slider("Final", "shift", 0, 300)
    while True:
        frame = getImage()
        for p in poss:
            cv2.circle(frame, tuple(p), 5, (0, 255, 0), -1)
        show('Final', frame)

        if cv2.waitKey(1) & 0xFF == ord('p') or len(poss) == 3:
            break


def main():
    frame = getImage()

    try:

        resX, resY = 1.5, 2

        W, H = int(250 * resX), int(250 * resY)

        dst = [[0, H], [0, 0], [W, 0]]

        dst[1][0] += get("Final", "shift")

        pts1 = np.float32([poss])
        pts2 = np.float32(dst)

        M = cv2.getAffineTransform(pts1, pts2)

        frame = cv2.warpAffine(frame, M, (W, H))

        marker_position = getMarkers(frame)[120]

        cv2.line(frame, tuple(marker_position), (0, marker_position[1]), (0, 0, 0), 2)
        cv2.line(frame, tuple(marker_position), (marker_position[0], 0), (0, 0, 0), 2)

        cv2.putText(frame, str(marker_position[0]),
                    tuple(np.int32([marker_position[0] / 2, marker_position[1]]).tolist()),
                    cv2.FONT_HERSHEY_COMPLEX, 1,
                    (50, 0, 255),
                    2,
                    cv2.LINE_AA)

        cv2.putText(frame, str(marker_position[1]),
                    tuple(np.int32([marker_position[0], marker_position[1] / 2]).tolist()),
                    cv2.FONT_HERSHEY_COMPLEX, 1,
                    (50, 0, 255),
                    2,
                    cv2.LINE_AA)

    except Exception as error:
        print(error)

    if len(poss) > 3:
        poss.clear()
        setup()
    show('Final', frame)
    # print(distA, distB)
    # marks = getMarkers(frame, True)
    # print(marks)


cv2.namedWindow("Final")

setup()

while True:
    try:
        main()
    except Exception as e:
        print(e)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('l'):
        poss.clear()
        setup()

# camA.release()
cv2.destroyAllWindows()
