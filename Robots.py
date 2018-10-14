from Functions import *
import math


class Robot_Main:

    pos = [8, 70]

    def gotTo(self, pos, cmd, prev_cmd = ""):
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
        cv2.circle(frame, (marker['2'][0], marker['2'][1]), 2, (0, 0, 255), -1)
        print(getRealPos(marker['2'][0], marker['2'][1]))
        return frame

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

