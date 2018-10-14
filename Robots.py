class Robot_Main:
    pos = [8, 70]
    radius = 150

    fields = []
    elements = {"r": [],
                "g": [],
                "b": []}

    def __repr__(self):
        return "Main robot with " + str(self.pos) + " pos and " + str(self.radius) + " radius"