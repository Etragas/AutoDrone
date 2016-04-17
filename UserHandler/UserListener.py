from Transmission_Formats import *
from Utils.Numeric import *
import re
import threading
import time
from Manager import *
from Drone_Data import Ros_Parrot_Collector
from nav_msgs.msg import Odometry
import rospy
from Controller import XYZ_Controller
import rospy
goal = None
wrapped = None
arguments = None
COMMAND_FILE = 'cmds.txt'
DEFAULT_OPEN = 'r'
DEFAULT_PROMPT = "Please enter a command:\n"

rospy.init_node("Master", anonymous=True, disable_signals=True)


def parse_user_input():
    global wrapped
    """

    :param arguments: A dictionary corresponding to the input string and corresponding format
    :return: The object ready for sending
    """
    while 1:
        cmd = raw_input(DEFAULT_PROMPT)
        try:
            transmission_cmd, data = cmd.strip().split()
            transmission_format = arguments[transmission_cmd]
            data = [x for x in re.split("[\[\],]",data) if (is_num(x) or x.isalpha())]
            wrapper = getattr(eval(transmission_format), transmission_format)
            temp = wrapper(*data)
            print("Correct Command")
            print("Confirm your goal:y/n")
            print(temp)
            if (raw_input().strip() in 'Yy'):
                wrapped = temp

        except Exception:
            print(Exception)
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
    # TODO: Put in the source
    arguments = load_cmds(COMMAND_FILE,DEFAULT_OPEN)


    #Start the goal listener thread
    listener = threading.Thread(target=parse_user_input)
    listener.start()

    drone_pos = Ros_Parrot_Collector.Ros_Parrot_Collector()
    poser = threading.Thread(target=drone_pos.start)
    poser.start()

    controller = XYZ_Controller.XYZ_Controller()
    commander = threading.Thread(target=controller.start)
    commander.start()

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
            overlord.feed(goal=goal.pose,frame=goal.frame,Drone_Data_Gen=drone_pos,controller=controller,Commander=controller)
        time.sleep(1)


     #pack = parse_user_input(arguments)

