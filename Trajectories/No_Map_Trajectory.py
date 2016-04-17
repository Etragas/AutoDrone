from Trajectory import  *
class No_Map_Trajectory(Trajectory):


    def __init__(self,goal,frame,drone_pos):
        self.goal = goal
        if (frame == 1):
            self.goal = self.goal + drone_pos


    def generateTrajectory(self,drone_pos):
        return self.goal
