"""
The methods in the class make no assumptions regarding frame and must be corrected for frame elsewhere
"""
import numpy as np
from  RosUtils.numUtil import *
from RosUtils.messageUtil import *
class Trajectory_Patterns:

    """
    This function builds a trajectory that involves 1 meter in each direction, with a return to origin on top of that.
    """
    def default_exploration_waypoints(self,goal,drone):
        goalPoints = []
        for direct in range(6):
            template = np.asarray([0, 0, 2, 0, 0, 0, 0])
            template[direct % 3]+=1 if direct < 3 else -1
            goalPoints.append(goal)
            goalPoints.append(buildPose(template))
        return goalPoints



