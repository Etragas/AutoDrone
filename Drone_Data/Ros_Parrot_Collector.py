import numpy as np
import rospy
from geometry_msgs.msg import Pose, Twist
from nav_msgs.msg import Odometry


def callback(data, obj):
    """
    Data is an Odometry object
    :param data: Odometry with twist and pose
    :param obj: The drone
    :return:
    """
    dp = data.pose.pose.position
    do = data.pose.pose.orientation
    daccel = data.twist.twist.linear
    dang = data.twist.twist.angular
    obj.pose.position = np.asarray([dp.x, dp.y, dp.z], dtype=np.float64)
    obj.pose.orientation = np.asarray([do.x, do.y, do.z, do.w], dtype=np.float64)
    obj.twist.linear = np.asarray([daccel.x, daccel.y, daccel.z], dtype=np.float64)
    obj.twist.angular = np.asarray([dang.x, dang.y, dang.z], dtype=np.float64)


class Ros_Parrot_Collector:
    def __init__(self, Name="Collector", topic="/ground_truth/state"):
        self.pose = Pose()
        self.twist = Twist()
        self.name = Name
        self.topic = topic

    def start(self):
        self.listen_to_topic(self.name, self.topic)

    def getPose(self):
        return self.pose

    def getPosition(self):
        return self.pose.position

    def getOrientation(self):
        return self.pose.orientation

    def getAngular(self):
        return self.twist.angular

    def getLinear(self):
        return self.twist.linear

    def listen_to_topic(self, NAME, topic_name):
        global rospy
        rospy.Subscriber(topic_name, Odometry, callback, self)
        print("Meow")
        rospy.spin()

# listen_to_topic("ardrone/odometry")
