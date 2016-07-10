

"""
Goal encodes the 6 dimensional goal state vector for the object.
d0 ... d2 correspond to the 3d co-ordinates x,y,z
d3 ... d5 correspond to the orientation of rotation phi, theta, psi (around x, y, z)
d6 corresponds to the frame. If 0 then global frame, if 1 then local frame.
"""
import numpy as np
from math import radians
from geometry_msgs.msg import Quaternion, Point, Pose
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry
from RosUtils import messageUtil
class Goal:

    def __init__(self, *vec):
        self.frame = (vec[6] == 'local')
        self.pose = messageUtil.buildPose(vec[:6])

    def __repr__(self):
        return str(self.pose) + "\n" + "Frame: " + str("Local" if self.frame else "Global")

