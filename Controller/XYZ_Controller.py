import time
from math import *
import rospy
from ardrone_autonomy import msg
# listen_to_topic("ardrone/odometry")
import numpy as np
from numpy import sign
from geometry_msgs import msg
from geometry_msgs.msg import Vector3
from tf.transformations import euler_from_quaternion


def callback(data, obj):
    obj.position = data.pose.pose


#    print(type(val))
#    print(data.pose.pose)



def cleanse(var, const):
    """
    This converts a PID command based off distance in to a command appropriate to the AR Autonomy controller
    The ardrone accepts cmd_vel messages in an arbitrary range, so cleanse is NOT NECESSARY
    But it is HIGHLY RECOMMENDED that it be left on for stability purposes.
    :param var: The value to be normalized
    :param const: This constant is used to stabilize the commands to the drone by creating a maximum amount of output
    :return:
    """

    if var > 0:
        if var > 1:
            var = 1.0 / const
        else:
            var = float(var) / const
    if var < 0:
        if var < -1:
            var = -1.0 / const
        else:
            var = float(var) / const
    if abs(var) < .001:
        var = 0
    return var


SPEED_SCALE = 4

class XYZ_Controller:
    """
    This class is responsible for handling positional commands only
    """
    global FREQ
    FREQ = 200
    I_SCALE = 0  # 1/FREQ
    P_SCALE = 5
    D_SCALE = 2
    AI_SCALE = 0  # .01/FREQ
    AP_SCALE = 5
    AD_SCALE = .1
    def __init__(self, Name="Commander", topic="cmd_vel", Node=None):
        self.position = 0
        self.name = Name
        self.topic = topic
        self.cmd_vel = None
        self.node = Node
        self.li = 0
        self.ai = 0
        self.xi = 0
        self.yi = 0
        self.zi = 0
        self.axi = 0
        self.ayi = 0
        self.azi = 0

    def start(self):
        self.talk(self.name, self.topic)

    def compute_cmd(self, goal, drone_data_gen, frame):
        goalAngEuler = np.array(euler_from_quaternion(goal.orientation), dtype=np.float32)
        droneAngEuler = np.array(euler_from_quaternion(drone_data_gen.getOrientation()), dtype=np.float32)
        posCmd = self.commands_lin(goal.position, drone_data_gen.getPosition())
        posCmd = posCmd - XYZ_Controller.D_SCALE * drone_data_gen.getLinear()
        posCmd = np.array([cleanse(x, SPEED_SCALE ) for x in posCmd], dtype=np.float32)
        # print(posCmd)
        posCmd = self.angle_correct(drone_data_gen.getOrientation(), posCmd)
        # print(posCmd)
        angCmd = self.commands_ang(goalAngEuler, droneAngEuler)
        angCmd = np.array([cleanse(x, SPEED_SCALE) for x in angCmd], dtype=np.float32)
        angCmd[0] = 0
        angCmd[1] = 0
        # ax, ay, az = self.commands_lin(goalAngEuler,droneAngEuler)
        # ax, ay, az = map(lambda x: cleanse(x,10), [ax,ay,az])
        lin_cmd = msg.Vector3(*posCmd)
        ang_cmd = Vector3(*angCmd)
        return msg.Twist(lin_cmd, ang_cmd)

    def commands_lin(self, goal, drone):
        I_SCALE = XYZ_Controller.I_SCALE
        P_SCALE = XYZ_Controller.P_SCALE
        self.li += I_SCALE * (goal - drone)
        cmd = P_SCALE * (goal - drone) + self.li
        return cmd

    def angle_correct(self, drone_ori, cmd):
        phi, theta, psi = euler_from_quaternion(drone_ori)
        drone_new = [0, 0, cmd[2]]
        # FUCKING SCRUB WOLF OMFG
        drone_new[0] = cos(psi) * cmd[0] + sin(psi) * cmd[1]
        drone_new[1] = -sin(psi) * cmd[0] + cos(psi) * cmd[1]
        return drone_new

    #
    # def commands_lin(self, goal, drone):
    #     I_SCALE = XYZ_Controller.I_SCALE
    #     P_SCALE = XYZ_Controller.P_SCALE
    #     self.xi += I_SCALE * (goal.x - drone.x)
    #     self.yi += I_SCALE * (goal.y - drone.y)
    #     self.zi += I_SCALE * (goal.z - drone.z)
    #     cmdx = P_SCALE * (goal.x - drone.x) + self.xi
    #     cmdy = P_SCALE * (goal.y - drone.y ) + self.yi
    #     cmdz = P_SCALE * (goal.z - drone.z) + self.zi
    #     return cmdx, cmdy, cmdz

    def commands_ang(self, goal, drone):
        #Convert all angles to positive vals and find closest goal
        drone[2] = drone[2]%(2*pi)
        cand = [goal[2] % (2*pi),goal[2] % (2*pi)+(2*pi),goal[2] % (2*pi)-(2*pi)]
        goal[2] = cand[np.argmin((map(lambda x: abs(x-drone[2] ),cand)))]
        AI_SCALE = XYZ_Controller.AI_SCALE
        AP_SCALE = XYZ_Controller.AP_SCALE
        self.ai += AI_SCALE * (goal - drone)
        acmd = AP_SCALE * (goal - drone) + self.ai
        acmd[2] = acmd[2]
        return acmd

    def update_Command(self, new_cmd):
        self.cmd_vel = new_cmd

    def talk(self, NAME, topic_name):
        global rospy, FREQ
        pub = rospy.Publisher(topic_name, msg.Twist, queue_size=FREQ)
        # rospy.init_node(NAME, anonymous=True, disable_signals=True)
        rate = rospy.Rate(200)  # 200hz
        while self.cmd_vel is None:
            print("waiting")
            time.sleep(1)
        print("done")
        while not rospy.is_shutdown():
            # hello_str = "hello world %s" % rospy.get_time()
            # rospy.loginfo(tw)
            pub.publish(self.cmd_vel)
            rate.sleep()
