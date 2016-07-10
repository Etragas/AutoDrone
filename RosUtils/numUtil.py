from geometry_msgs.msg import Pose, Point
from geometry_msgs.msg import Vector3
from tf.transformations import quaternion_inverse, quaternion_multiply, euler_from_quaternion

def is_num(candidate):
    try:
        val = float(candidate)
        return True
    except:
        return False

def addPose(pose1 , pose2 ):
    """
    :param pose1: Pose
    :param pose2: Pose
    :return:
    """
    pos = pose1.position + pose2.position
    ang = quaternion_multiply(pose1.orientation,pose2.orientation)
    return Pose(position=pos, orientation=ang)


def addToVec(template, dist, amount):
    template[dist] += amount
    return template