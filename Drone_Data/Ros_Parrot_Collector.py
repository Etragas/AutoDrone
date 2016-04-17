import sys
import rospy
from rospy_tutorials.msg import HeaderString
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from ardrone_autonomy import msg
import threading
import time


def callback(data, obj):
    obj.position = data.pose.pose
#    print(type(val))
#    print(data.pose.pose)

class Ros_Parrot_Collector:

    def __init__(self,Name = "Collector", topic = "ardrone/odometry"):
        self.position = 0
        self.name = Name
        self.topic = topic


    def start(self):
        self.listen_to_topic(self.name,self.topic)

    def getPose(self):
        return self.position



    def listen_to_topic(self,NAME,topic_name):
        global rospy
        rospy.Subscriber(topic_name, Odometry, callback,self)
        print("Meow")
        rospy.spin()


#listen_to_topic("ardrone/odometry")