import sys
import rospy
from rospy_tutorials.msg import HeaderString
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from ardrone_autonomy import msg
import threading
import time


#listen_to_topic("ardrone/odometry")

import sys
import rospy
from rospy_tutorials.msg import HeaderString
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs import msg
def callback(data, obj):
    obj.position = data.pose.pose
#    print(type(val))
#    print(data.pose.pose)


def cleanse(var,const):
    if var > 0:
        if var > 1:
            var = 1.0/const
        else:
            var = float(var)/const
    if var < 0:
        if var < -1:
            var = -1.0/const
        else:
            var = float(var)/const
    return var



class XYZ_Controller:
    FREQ = 200
    I_SCALE = .001/FREQ
    P_SCALE = .25
    D_SCALE = .1
    def __init__(self,Name = "Commander", topic = "cmd_vel", Node = None):
        self.position = 0
        self.name = Name
        self.topic = topic
        self.cmd_vel = None
        self.node = Node
        self.xi = 0
        self.yi = 0
        self.zi = 0

    def start(self):
        self.talk(self.name,self.topic)

    def compute_cmd(self,goal,drone_pos):
        g = goal.position
        d = drone_pos.position
        x,y,z = self.commands_lin(g,d)
        x,y,z = map(lambda x: cleanse(x,2), [x,y,z])
        lin_cmd = msg.Vector3(x = x, y =y , z = z)
        ang = msg.Vector3(x=0.0, y=0, z=0)
        return msg.Twist(lin_cmd, ang)

    def commands_lin(self, g, d):
        I_SCALE = XYZ_Controller.I_SCALE
        P_SCALE = XYZ_Controller.P_SCALE
        self.xi += I_SCALE * (g.x - d.x)
        self.yi += I_SCALE * (g.y - d.y)
        self.zi += I_SCALE * (g.z - d.z)
        cmdx = P_SCALE * (d.x - g.x) + self.xi
        cmdy = P_SCALE * (d.y - g.y) + self.yi
        cmdz = P_SCALE * (d.z - g.z) + self.zi
        return cmdx, cmdy, cmdz
    def update_Command(self,new_cmd):
        self.cmd_vel = new_cmd

    def talk(self,NAME,topic_name):
        global rospy

        pub = rospy.Publisher(topic_name, msg.Twist, queue_size=200)
        #rospy.init_node(NAME, anonymous=True, disable_signals=True)
        rate = rospy.Rate(200)  # 200hz
        while self.cmd_vel is None:
            print("waiting")
            time.sleep(1)
        print("done")
        while not rospy.is_shutdown():
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(tw)
            pub.publish(self.cmd_vel)
            rate.sleep()

