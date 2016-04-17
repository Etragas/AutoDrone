import sys
import rospy
from rospy_tutorials.msg import HeaderString
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs import msg

NAME = 'nava_listener'


def talker():
    pos = msg.Vector3(x=0, y=0, z=0)
    ang = msg.Vector3(x=0.0, y=0, z=0)
    tw = msg.Twist(pos, ang)
    print(tw)
    pub = rospy.Publisher('cmd_vel', msg.Twist, queue_size=50)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(50)  # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(tw)
        pub.publish(tw)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
