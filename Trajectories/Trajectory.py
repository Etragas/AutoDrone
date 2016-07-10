class Trajectory:
    def __init__(self,points):
        self.points = points
        d = []

    def getNextPoint(self):
        return self.points.pop()