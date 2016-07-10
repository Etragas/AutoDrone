from std_msgs.msg import _Empty

from Transmission_Formats import *
from RosUtils.numUtil import *
import re
import threading
import time
from Manager import *
from Drone_Data import Ros_Parrot_Collector
from nav_msgs.msg import Odometry
import rospy
from std_msgs import *
from Controller import XYZ_Controller
from Camera import *
import rospy
import subprocess
import os
from std_msgs.msg import Empty
goal = None
wrapped = None
arguments = None
COMMAND_FILE = 'cmds.txt'
DEFAULT_OPEN = 'r'
DEFAULT_PROMPT = "Please enter a command:\n"

takeoff = rospy.Publisher('ardrone/takeoff', Empty, queue_size=50)

land = rospy.Publisher('ardrone/land', Empty, queue_size=50)
msg = Empty()


def parse_user_input():
    global wrapped
    """


    :param arguments: A dictionary corresponding to the input string and corresponding format
    :return: The object ready for sending
    """
    # SetGoal [1,1,1,0,0,180,0]
    # SetGoal [1,1,1,0,0,270,0]
    # SetGoal [1,1,0,0,0,0,local]
    # SetGoal [-1,-2,0,0,0,0,local]
    # SetGoal [0,0,1,0,0,0,0]
    # SetGoal [0,0,2,0,0,0,0]
    # SetGoal [2,2,1,0,0,45,0]
    # SetGoal [3,1,2,0,0,0,0]
    while 1:
        cmd = raw_input(DEFAULT_PROMPT)
        try:
            transmission_cmd, data = cmd.strip().split()
            transmission_format = arguments[transmission_cmd]
            if transmission_cmd == "SetGoal":
                data = [x for x in re.split("[\[\],]",data) if (is_num(x) or x.isalpha())]
                wrapper = getattr(eval(transmission_format), transmission_format)
                temp = wrapper(*data)
                print("Correct Command")
                print("Confirm your goal:y/n")
                print(temp)
                if (raw_input().strip() in 'Yy'):
                    wrapped = temp
            if transmission_cmd == "Takeoff":
                takeoff.publish(msg)
            if transmission_cmd == "Land":
                land.publish(msg)

        except Exception:
            print(Exception.message)
            print("Invalid Command")

def load_cmds(COMMAND_FILE,DEFAULT_OPEN):
    arguments = {}

    arg_file = open(COMMAND_FILE,DEFAULT_OPEN)
    for x in arg_file.readlines():
        cmd_call, transmission_format = x.strip().split(':')
        arguments[cmd_call] = transmission_format
    return arguments


if __name__ == '__main__':
    global position
    # Load Dictionary for arguments
    arguments = load_cmds(COMMAND_FILE,DEFAULT_OPEN)

    #This don't work so good, need tolook at
    #gazebo = threading.Thread(target=subprocess.Popen("./start_gazebo.sh", shell=True))
    #gazebo.start()



    rospy.init_node("Master", anonymous=True, disable_signals=True)
    rate = rospy.Rate(200)

    listener = threading.Thread(target=parse_user_input)
    listener.start()

    drone_pos = Ros_Parrot_Collector.Ros_Parrot_Collector()
    poser = threading.Thread(target=drone_pos.start)
    poser.start()

    controller = XYZ_Controller.XYZ_Controller()
    commander = threading.Thread(target=controller.start)
    commander.start()

    camera = Camera_Capturer.image_converter()
    cameraCommand = threading.Thread(target=camera.start)
    cameraCommand.start()
    #TODO:
    #Implement Listener
    overlord = Director.Director()
    admin = threading.Thread(target=overlord.start)
    admin.start()


    #position_col.start()#Check if the goal has been changed, if so update the Director
    while True:
        if goal != wrapped:
            goal = wrapped
            print "Goal Changed"
            print(goal)
            overlord.feed(goal=goal.pose,frame=goal.frame,Drone_Data_Gen=drone_pos,controller=controller,Commander=controller)
        time.sleep(.1)

     #pack = parse_user_input(arguments)

