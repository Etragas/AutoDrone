import sys
import rospy
from rospy_tutorials.msg import HeaderString
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from ardrone_autonomy import msg

NAME = 'nava_listener'
def callback(data):
	#print(data)
	position = data.pose.pose.position
	x,y,z = position.x, position.y, position.z
	print(data.pose.pose.position)


def listen_to_topic(topic_name):
	rospy.Subscriber(topic_name, Odometry, callback)
	rospy.init_node(NAME,anonymous=True)

	print("Meow")
	rospy.spin()


listen_to_topic("ardrone/odometry")