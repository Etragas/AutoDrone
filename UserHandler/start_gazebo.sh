#!/usr/bin/env bash
echo -e "ros" | sudo -S ls
sudo -s
exec roslaunch cvg_sim_gazebo ardrone_testworld.launch