import cv2, numpy as np
from Functions import correctPositions

cap = cv2.VideoCapture(1)


def corners_unwarp(img, nx, ny, scale):
    undist = img

    gray = cv2.cvtColor(undist, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

    if ret:
        # cv2.drawChessboardCorners(undist, (nx, ny), corners, ret)
        offset = 100
        img_size = (gray.shape[1], gray.shape[0])

        pts = [corners[0].tolist()[0], corners[nx - 1].tolist()[0], corners[-1].tolist()[0], corners[-nx].tolist()[0]]

        pts = correctPositions(pts, scale, 0)

        src = np.float32(pts)
        dst = np.float32([[offset, offset], [img_size[0] - offset, offset],
                          [img_size[0] - offset, img_size[1] - offset],
                          [offset, img_size[1] - offset]])
        M = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(undist, M, img_size)
        return warped, ret
    else:
        return img, ret


while True:

    _, frame = cap.read()
    cv2.imshow('fram', frame)

    wrapped, ret = corners_unwarp(frame, 9, 6, 6)

    print('draw')
    if ret:
        cv2.imshow('frame', wrapped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
