from Functions import *


class Robot_Main:
    pos = [8, 70]

    def gotTo(self, pos, cmd, prev_cmd=""):
        self.sendCMD(prev_cmd)
        self.moveY(pos[1] - self.pos[1])
        self.moveX(pos[0] - self.pos[0])
        self.sendCMD(cmd)
        self.pos = pos

    def moveX(self, dist):
        pass

    def moveY(self, dist):
        pass

    def sendCMD(self, cmd):
        pass

    def getPos(self, frame, marker):
        cv2.circle(frame, (marker[self.marker][0], marker[self.marker][1]), 5, (0, 0, 255), -1)
        self.pos = [int(marker[self.marker][0] / 0.78), marker[self.marker][1]]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(self.pos[0]) + ", " + str(self.pos[1]),
                    (marker[self.marker][0], marker[self.marker][1]),
                    font,
                    1,
                    (0, 255, 0),
                    2)
        return frame, self.pos

    @property
    def __repr__(self):
        return "Main robot with " + str(self.pos) + " pos"

    def __init__(self, marker):
        self.marker = marker


class Robot_Small:
    pos = [8, 70]

    def gotTo(self, pos, cmd):
        self.moveY(pos[1] - self.pos[1])
        self.moveX(pos[0] - self.pos[0])
        self.sendCMD(cmd)

    def moveX(self, dist):
        pass

    def moveY(self, dist):
        pass

    def sendCMD(self, cmd):
        pass

    @property
    def __repr__(self):
        return "Main robot with " + str(self.pos) + " pos"
