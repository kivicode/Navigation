from Functions import removePerspective
import cv2
import numpy as np
import freenect

field_mask_pts = np.array([[0, 296], [277, 131], [637, 216], [640, 480]])
help_mask_pts = np.array([[234, 320], [223, 197], [526, 220], [526, 391]])

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


def draw_hint(frame):
    cv2.polylines(frame, [(field_mask_pts).reshape((-1, 1, 2))], True, (255, 0, 255), 2)


def make_lines(img, canny):
    global screen_lines
    lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x1 in range(273, 480) and x2 in range(273, 480) and np.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)) > 50:
                li_a = line_intersection([[x1, y1], [x2, y2]],
                                         [field_mask_pts.copy().tolist()[1], field_mask_pts.copy().tolist()[2]])
                li_b = line_intersection([[x1, y1], [x2, y2]],
                                         [field_mask_pts.copy().tolist()[0], field_mask_pts.copy().tolist()[3]])
                cv2.line(img, tuple(li_a), tuple(li_b), (0, 255, 0), 5)
                print(li_a, li_b)
                screen_lines.append([li_b, li_a])
                break


def get_video():
    array, _ = freenect.sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array


while True:
    # depth, timestamp = freenect.sync_get_depth()
    # frame = get_video()

    # depth = depth.astype(np.uint8)
    depth = cv2.imread('images/home_tests_for.png')
    depth = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)

    field_mask = np.zeros_like(depth)
    cv2.fillConvexPoly(field_mask, field_mask_pts, (255, 255, 255))

    help_mask = np.zeros_like(depth)
    cv2.fillConvexPoly(help_mask, help_mask_pts, (255, 255, 255))

    depth = cv2.bitwise_not(depth, mask=field_mask)
    stick = cv2.bitwise_not(depth, mask=help_mask)

    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)

    stick_canny = cv2.Canny(stick, 10, 20)
    try:
        make_lines(depth, stick_canny)
        print("Succ")
    except Exception as e:
        print(e)

    # calibration_pts.append()
    pts = field_mask_pts.tolist()
    screen_lines.append([pts[0], pts[1]])
    screen_lines.append([pts[1], screen_lines[0][1]])
    screen_lines.append([pts[0], screen_lines[0][0]])
    for i in screen_lines:
        # try:
        cv2.line(depth, tuple(i[0]), tuple(i[1]), (0, 0, 255), 2)
        # except:
        #     pass

    draw_hint(depth)
    depth = removePerspective(depth, [pts[0], pts[1], screen_lines[0][1], screen_lines[0][0]])
    cv2.imshow('BW', depth)
    cv2.imshow('Stick', stick_canny)
    # cv2.imshow('Field', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
