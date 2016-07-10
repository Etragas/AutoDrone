# Receives a Goal Object
# Retrieves the relevant resources e.g odometry etc
# Sends to controller
import threading
import time

import rospy

from Trajectories import *

"""
The Directory is the resource manager of the application, it keeps track of almost every relevant variable being updated
via threads started through the UserListener."""


class Director:
    def __init__(self):
        self.goal = None
        self.frame = None
        self.Trajectory_Gen = None
        self.Drone_Data_Gen = None
        self.Alarm_Gen = None
        self.controller = None
        self.Commander = None
        self.newGoal = False
        self.rate = rospy.Rate(200)

    def start(self):
        while 1:
            if not (self.goal is None):
                while (not self.newGoal):
                    self.goal = self.Trajectory_Gen.generateTrajectoryPoint(self.Drone_Data_Gen, self.goal)
                    commands = self.controller.compute_cmd(self.goal, self.Drone_Data_Gen, self.frame)
                    self.Commander.update_Command(commands)
                    self.rate.sleep()
                time.sleep(1)
                self.Trajectory_Gen = No_Map_Trajectory(self.goal, self.frame, self.Drone_Data_Gen)
                self.goal = self.Trajectory_Gen.goal
                self.newGoal = False

    def printStatus(self):
        threading.Timer(1, self.printStatus).start()
        print(self.Drone_Data_Gen.getPose())

    def feed(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.newGoal = True

    def feed_new_goal(self, goal):
        self.goal = goal.twist
        self.frame = goal.frame
        self.newGoal = True
