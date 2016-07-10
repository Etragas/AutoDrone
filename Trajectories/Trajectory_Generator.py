from Trajectories import *
from geometry_msgs.msg import Point, Pose, Quaternion
from Trajectory_Patterns import Trajectory_Patterns
class Trajectory_Generator:
    def __init__(self):
        return

    def buildTrajectory(self,goal,drone):
        tp = Trajectory_Patterns()
        return Trajectory(tp.default_exploration_waypoints(goal,drone))

