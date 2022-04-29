import pybullet as p
import time
import pybullet_data
import math
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
import sys
from pathlib import Path
import os

sys.path.insert(0, './')
if Path(os.getcwd()).name == "Pybullet test":
 os.chdir(str(Path().cwd().parents[1]))



physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -10)  # describe gravity in (x,y,z)
planeId = p.loadURDF("plane.urdf")
base_Position = [0, 0, .3]
UR5Id = p.loadURDF(
   ## PUT THE URDF FILE PATH HERE, IN MY CASE = /home/anshul/Documents/pybulletproject/robot_movement_interface/dependencies/ur_description/urdf/ur5_robot.urdf
    "gym_LAMA_ur5/ur_description/urdf/ur5_robot.urdf",
    useFixedBase=1, basePosition=base_Position)


p.setRealTimeSimulation(0)
starting_point = [0.25, 0.20, 0.4]
target_ori_euler = [-math.pi / 2, -math.pi / 2, 0]
target_ori_quaternion = p.getQuaternionFromEuler(target_ori_euler)

num_samples = 20
#logid = p.startStateLogging(p.STATE_LOGGING_GENERIC_ROBOT,"velocity_test.txt", [1])
# make a simple unit circle
theta = np.linspace(0, 2 * np.pi, num_samples)
x, y = starting_point[0] + 0.2 * np.cos(theta), starting_point[1] + 0.2 * np.sin(theta)
link_states = []



file = open("gym_LAMA_ur5/Offline data/vel_data5.csv", "a")



for i in range(20):
    p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=217.60, cameraPitch=-99.80,
                                 cameraTargetPosition=[-0.03, -0.04, -0.30])
    target_joint = p.calculateInverseKinematics(UR5Id, 7, targetPosition=[x[i], y[i], 0.4],
                                                targetOrientation=target_ori_quaternion,residualThreshold=0.0001, maxNumIterations=300, solver=0)
    p.setJointMotorControlArray(UR5Id, range(1, 7), p.POSITION_CONTROL, targetPositions=target_joint) #targetVelocities=[0] * 6, forces=[500] * 6, positionGains=[0.03] * 6,
                                    #velocityGains=[1] * 6)

    ## Script to add data to "file" created above by ---- file = open("gym_LAMA_ur5/Offline data/vel_data5.csv", "a")

    for k in range(100):
        p.stepSimulation()
        list1 = []
        for j in range(1,7):
            list1.append(p.getJointState(UR5Id, j)[1])
        arr = np.asarray(list1)
        print(arr)
        np.savetxt(file, [arr], delimiter=',')
    link_states.append(list(p.getLinkState(UR5Id, 7)[0]))


linkstate_array = np.array(link_states)

plt.plot(x, y, 'b')
plt.plot(linkstate_array[:, 0], linkstate_array[:, 1], "r")
plt.title("plot showing the path followed by UR5, Red =Robot Path Blue= Our Input")
plt.xlabel("x-cordinates")
plt.ylabel("y-cordinates")
plt.show()
p.stopStateLogging(logid)
p.disconnect()
file.close()



