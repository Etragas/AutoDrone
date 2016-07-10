import numpy as np
from math import *
from Drone_Data import Ros_Parrot_Collector
from RosUtils.numUtil import *
from Trajectory import *
from Trajectory_Generator import Trajectory_Generator


class No_Map_Trajectory(Trajectory):

    def __init__(self, goal, frame, drone_data_gen):
        if (frame == 1):
            # Adjust goal
            psi = euler_from_quaternion(drone_data_gen.getOrientation())[2]
            rot =np.array([[cos(psi),-sin(psi),0],[sin(psi),cos(psi),0],[0,0,1]], dtype=np.float64)
            goal.position = np.dot(rot, goal.position)
            self.goal = addPose(goal, drone_data_gen.pose)
        else:
            dummy_drone = Ros_Parrot_Collector.Ros_Parrot_Collector()
            dummy_drone.pose = Pose(position=np.array([0, 0, 0], dtype=np.float32),
                                    orientation=np.array([0, 0, 0, 1], dtype=np.float32))
            self.goal = addPose(goal, dummy_drone.pose)
            # This should be origin instead of 0,0,0, wait until we have a ma
            #TODO: Use the map origin instead of 0,0,0 everywhere. Gotta wait for map impl for that
        g = Trajectory_Generator()
        self.trajectory = g.buildTrajectory(goal,drone_data_gen)
        print(self.trajectory.points)

    def generateTrajectoryPoint(self, drone_data_gen, goal, x=0):
        goalAngEuler = np.array(euler_from_quaternion(goal.orientation), dtype=np.float32)
        droneAngEuler = np.array(euler_from_quaternion(drone_data_gen.getOrientation()), dtype=np.float32)
        dist = abs(goal.position - drone_data_gen.getPosition())
        if(max(dist)< .1):
            if not self.trajectory.points:
                return self.goal
            self.goal = self.trajectory.getNextPoint()

            print("New Goal")
        return self.goal

        # return Pose(position=Vector3(x=goal.position.x+x, y=goal.position.y, z=goal.position.z+math.sin(+x)),orientation=goal.orientation)
