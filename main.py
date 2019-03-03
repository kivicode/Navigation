from Functions import *
from Robots import Robot_Main
import cv2
import time

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
        K = 0.1797510448

        dst = [[0, H], [0, 0], [W, 0]]

        dst[1][0] += get("Final", "shift")

        pts1 = np.float32([poss])
        pts2 = np.float32(dst)

        M = cv2.getAffineTransform(pts1, pts2)

        frame = cv2.warpAffine(frame, M, (W, H))

        mpos = getMarkers(frame)[120]

        cv2.line(frame, tuple(mpos), (0, mpos[1]), (0, 0, 0), 2)
        cv2.line(frame, tuple(mpos), (mpos[0], 0), (0, 0, 0), 2)

        cv2.putText(frame, str(mpos[0]),
                    tuple(np.int32([mpos[0] / 2, mpos[1]]).tolist()),
                    cv2.FONT_HERSHEY_COMPLEX, 1,
                    (50, 0, 255),
                    2,
                    cv2.LINE_AA)

        cv2.putText(frame, str(mpos[1]),
                    tuple(np.int32([mpos[0], mpos[1] / 2]).tolist()),
                    cv2.FONT_HERSHEY_COMPLEX, 1,
                    (50, 0, 255),
                    2,
                    cv2.LINE_AA)

        # A = np.asarray(poss[0])
        # O = np.asarray(poss[1])
        # B = np.asarray(poss[2])
        #
        # # print(angle_between_points(l11, l12, l22))
        #
        # mpos = getMarkers(frame)[120]
        #
        # dst = np.asarray(mpos)
        #
        # # to1 = perpend(A, O, dst)
        # # to1 = rotate(mpos, to1, 90 - angle_between_points(A, O, B))
        # # cv2.line(frame, to1, tuple(mpos), (255, 0, 255), 2)
        # #
        # # cv2.putText(frame, str(int(dist(to1, tuple(mpos)))), tuple(A.tolist()), cv2.FONT_HERSHEY_COMPLEX, 1,
        # #             (0, 0, 0),
        # #             2,
        # #             cv2.LINE_AA)
        #
        # to2 = perpend(B, O, dst)
        # to2 = rotate(mpos, to2, 127 - angle_between_points(A, O, B))
        # cv2.line(frame, to2, tuple(mpos), (255, 0, 255), 2)
        #
        # cv2.putText(frame, str(int(dist(to2, tuple(mpos)))), tuple(B.tolist()), cv2.FONT_HERSHEY_COMPLEX, 1,
        #             (0, 0, 0),
        #             2,
        #             cv2.LINE_AA)

    except Exception as e:
        print(e)

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
        print("EAWFESGRDNTHnhdfsg")
        setup()

# camA.release()
cv2.destroyAllWindows()
