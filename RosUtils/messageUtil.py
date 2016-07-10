import numpy as np
from math import radians
from geometry_msgs.msg import Pose
from tf.transformations import quaternion_from_euler
def buildPose(vec):
    x, y, z, phi, theta, psi = map(float, vec[:6])
    pos = np.asarray([x, y, z], dtype=np.float64)
    rads = map(lambda x: radians(x), [phi, theta, psi])
    ang = np.asarray(quaternion_from_euler(*rads), dtype=np.float64)
    # Apparently a quaternion is sometimes a 4d array and sometimes an object... Trash
    pose = Pose(position=pos, orientation=ang)
    return pose
