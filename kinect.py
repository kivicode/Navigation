from Functions import removePerspective, correctPositions, getMarkers, getImage
import cv2
import numpy as np

# import freenect

ORANGE = 0
GREEN = 1

side = GREEN

field_mask_pts_orange = np.array([[0, 296], [277, 131], [637, 216], [640, 480]])
field_mask_pts_green = np.array([[0, 480], [0, 220], [318, 148], [640, 343], [640, 480]])
field_mask_pts = [field_mask_pts_orange, field_mask_pts_green]
help_mask_pts_orange = np.array([[234, 320], [223, 197], [526, 220], [526, 391]])
help_mask_pts_green = np.array([[174, 285], [169, 114], [433, 124], [457, 254]])
help_mask_pts = [help_mask_pts_orange, help_mask_pts_green]

screen_lines = []


def line_intersection(a, b):
    a_from, a_to = a
    b_from, b_to = b
    line1StartX, line1StartY = a_from
    line1EndX, line1EndY = a_to
    line2StartX, line2StartY = b_from
    line2EndX, line2EndY = b_to
    denominator = ((line2EndY - line2StartY) * (line1EndX - line1StartX)) - (
            (line2EndX - line2StartX) * (line1EndY - line1StartY))

    a = line1StartY - line2StartY
    b = line1StartX - line2StartX
    numerator1 = ((line2EndX - line2StartX) * a) - ((line2EndY - line2StartY) * b)
    numerator2 = ((line1EndX - line1StartX) * a) - ((line1EndY - line1StartY) * b)
    a = numerator1 / denominator
    b = numerator2 / denominator

    x = line1StartX + (a * (line1EndX - line1StartX))
    y = line1StartY + (a * (line1EndY - line1StartY))

    return [int(x), int(y)]


def draw_hint(image):
    cv2.polylines(image, [field_mask_pts[side].reshape((-1, 1, 2))], True, (255, 0, 255), 2)


def make_lines(img, canny):
    global screen_lines
    lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=50, minLineLength=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            y1 += 20
            li_a = line_intersection([[x1, y1], [x2, y2]],
                                     [field_mask_pts[side].copy().tolist()[1],
                                      field_mask_pts[side].copy().tolist()[2]])
            li_b = line_intersection([[x1, y1], [x2, y2]],
                                     [field_mask_pts[side].copy().tolist()[0],
                                      field_mask_pts[side].copy().tolist()[3]])
            cv2.line(img, tuple(li_a), tuple(li_b), (0, 255, 0), 5)
            print(li_a, li_b)
            screen_lines.append([li_b, li_a])
            break


# c
# def get_video():
# array, _ = freenect.sync_get_video()
# array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
# return array


# points = [-1, -1, -1, -1]
points = [[647, 249],
          [975, 220],
          [1102, 324],
          [732, 367]]
index = 0
finished = False


def clicked(event, x, y, flags, param):
    global index, finished, prev_pts
    if event == cv2.EVENT_LBUTTONDBLCLK and not finished:
        points[index] = [x, y]
        print(x, y)
        index += 1
        if not -1 in points:
            finished = True
    else:
        finished = False


cv2.namedWindow('newFrame')
cv2.setMouseCallback("newFrame", clicked)
marker = []
prev_pts = [[100, 100]]

while True:
    # depth, timestamp = freenect.sync_get_depth()
    frame = getImage()

    if True:
        try:
            marker = getMarkers(frame)[5][2].tolist()[0][:1][0]
            if marker not in prev_pts:
                prev_pts.append(marker)
            if None not in prev_pts:
                cv2.polylines(frame, [np.array([prev_pts], np.int32).reshape((-1, 1, 2))], False, (255, 0, 255), 3)
        except Exception as e:
            prev_pts = []
            print("Marker not found", e)

    cv2.imshow('main', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
