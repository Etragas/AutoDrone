

"""
Goal encodes the 6 dimensional goal state vector for the object.
d0 ... d2 correspond to the 3d co-ordinates x,y,z
d3 ... d5 correspond to the orientation of rotation phi, theta, psi (around x, y, z)
d6 corresponds to the frame. If 0 then global frame, if 1 then local frame.
"""
import numpy as np
from geometry_msgs import msg
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry

class Goal:

    def __init__(self, *vec):
        self.x, self.y ,self.z , self.phi, self.theta, self.psi = map(float,vec[:6])
        self.frame = (vec[6] == 'local')
        pos = msg.Vector3(x=self.x, y=self.y, z=self.z)
        ang = quaternion_from_euler(self.phi, self.theta, self.psi)
        self.pose = msg.Pose(position=pos,orientation=ang)

    def __repr__(self):
        return str(self.pose) + "\n" + "Frame: " + str("Local" if self.frame else "Global")