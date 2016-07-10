import pcl
import octomap
import numpy as np

p = pcl.load('/home/ros/TestM/Meowth.nvm.cmvs/Meowth.0.ply','ply')
print(p)
pcl.save(p,'/home/ros/TestM/Meowth.nvm.cmvs/Meowth.pcd','pcd')
p = pcl.load('/home/ros/TestM/Meowth.nvm.cmvs/Meowth.pcd')
fil = p.make_statistical_outlier_filter()
fil.set_mean_k (50)
fil.set_std_dev_mul_thresh (1.0)
fil.filter().to_file("/home/ros/TestM/Meowth.nvm.cmvs/inliersSparse.pcd")

