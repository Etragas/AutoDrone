#Receives a Goal Object
#Retrieves the relevant resources e.g odometry etc
#Sends to controller
from Trajectories import *
from Transmission_Formats import *
from Utils.Numeric import *
import numpy as np
import time
from ardrone_autonomy import msg
from geometry_msgs import msg

class Director:
    def __init__(self):
        self.goal = None
        self.frame = None
        self.Trajectory_Gen= None
        self.Drone_Data_Gen= None
        self.Alarm_Gen = None
        self.controller = None
        self.Commander = None
        self.newGoal = False


    def start(self):
        #Initiate the main loop
        #Grab the trajectory
        #Grab the odometry
        #Feed into the controller
        #...
        while 1:
            if not(self.goal is None):
                while (not self.newGoal):
                    #print('woof')
                    drone_current_pos = self.Drone_Data_Gen.getPose()
                    #print(drone_current_pos)
                    #current_traj_goal = self.Trajectory_Gen.retrieveNextPoint(drone_current_pos,self.frame) #Frame sensitive
                    commands = self.controller.compute_cmd(self.goal,drone_current_pos)
                    self.Commander.update_Command(commands)
                #If here then newGoal
                print('meow')
                print(self.newGoal)
                print(self.goal)
                time.sleep(1)
                #frame force to be local for the time being
                g = self.goal.position
                d = self.Drone_Data_Gen.getPose().position
                lin_cmd = msg.Vector3(x = g.x+d.x, y=g.y+d.y, z = g.z+d.z)
                self.goal.position = lin_cmd
                self.Trajectory_Gen = No_Map_Trajectory.No_Map_Trajectory(self.goal,self.frame,self.Drone_Data_Gen.getPose())
                self.newGoal = False






        return

    def feed(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        self.newGoal = True

    def feed_new_goal(self,goal):
        self.goal = goal.twist
        self.frame = goal.frame
        self.newGoal = True
