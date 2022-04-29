#Task Implemented
#1. RL Agent (robot) env intiation with OpenAI gym + Pybullet
#2. Custom setup of trajectorz to learn with waypoints() and objective function (reward function)

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
from pathlib import Path
import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random



if not p.isConnected():
    p.connect(p.GUI)


class RobotEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, trajectory_type, num_samples, seed_x=5001, seed_y=9001 ):

        p.resetDebugVisualizerCamera(cameraDistance=2.92, cameraYaw=-63.80, cameraPitch=-112.80,
                                     cameraTargetPosition=[-0.03, -0.04, -0.30])
        #TODO
        self.action_space = spaces.Box(np.array([0.0, 0.0, 0.6]), np.array([0.45, 0.5, 0.9]), shape=(3,),
                                       dtype=np.float32)

        #TODO
        self.observation_space = spaces.Box(np.array([0.0, 0.0, 0.6, 0.0, 0.0, 0.6]),
                                            np.array([0.45, 0.5, 0.9, 0.45, 0.5, 0.9]), shape=(6,), dtype=np.float32)

        self.target_point_index = 0
        self.max_possible_target_point_index = 9
        self.threshold_distance = 0.001
        self.base_Position =  [0, 0, 1.4]
        self.starting_point = [0.25, 0.22, 0.8]
        self.episode_no= 0
        self.trajectory = trajectory_type
        self.step_without_progress = 0
        self.start_point = True
        self.num_samples = num_samples
        self.seed_x = seed_x
        self.seed_y = seed_y
        # Parameters for URDF file of UR5 (Orientation, start point)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        planeId = p.loadURDF("plane.urdf")
        urdfRootPath = pybullet_data.getDataPath()
        target_ori_euler = [math.pi, 0, 0]
        target_ori_quaternion = p.getQuaternionFromEuler(target_ori_euler)
        urdf_file_path = Path.cwd().parents[2] / Path("gym_LAMA_ur5/ur_description/urdf/ur5_robot.urdf")
        self.UR5Id = p.loadURDF(
            "/gym_LAMA_ur5/ur_description/urdf/ur5_robot.urdf",
            useFixedBase=1,baseOrientation = target_ori_quaternion, basePosition=self.base_Position)

        tableUid = p.loadURDF(os.path.join(urdfRootPath, "table/table.urdf"), basePosition=[0.1, 0.3, 0.1])
        self.waypoints()
        for i in range(self.num_samples-1):
            p.addUserDebugLine((self.x[i], self.y[i], 0.8), (self.x[i + 1], self.y[i + 1], 0.8),
                               lineColorRGB=[0.5, 0.5, 0.5])

    def waypoints(self):
        if self.trajectory == "traj_1":

            theta = np.linspace(0, 2 * np.pi, self.num_samples, endpoint=True)

            self.x, self.y = self.starting_point[0] + 0.15 * np.cos(theta),self.starting_point[1] + 0.15 * np.sin(theta)
            self.z = np.array([0.8]*10)


        elif self.trajectory == "traj_2":
            self.x = np.array([0.2]*self.num_samples)
            self.y = np.linspace(0.1, 0.5, num=self.num_samples, endpoint=True)
            self.z = np.array([0.8]*self.num_samples)
        # print(self.x, self.y, self.z)

        elif self.trajectory == "traj_3":
            self.x = []
            self.y = []
            for j in range(self.num_samples):
                random.seed(self.seed_x + j)
                self.x.append(random.uniform(0.15, 0.35))
            for i in range(self.num_samples):
                random.seed(self.seed_y + i)
                self.y.append(random.uniform(0.1, 0.5))

            self.z = np.array([0.8] * self.num_samples)

        return self.x, self.y, self.z


    def reset(self):
        # resetting the environment with initial pose
        p.resetSimulation

        self.target_point_index = 0
        target_ori_euler_end_eff = [math.pi / 2, math.pi / 2, 0]
        target_ori_quaternion_end_eff = p.getQuaternionFromEuler(target_ori_euler_end_eff)
        target_joint = p.calculateInverseKinematics(self.UR5Id, 7,
                                                    targetPosition=self.starting_point,
                                                    targetOrientation=target_ori_quaternion_end_eff,
                                                    residualThreshold=0.00001, maxNumIterations=2000, solver=0)
        p.setJointMotorControlArray(self.UR5Id, range(1, 7), p.POSITION_CONTROL, targetPositions=target_joint,
                                    targetVelocities=[0] * 6, forces=[500] * 6, positionGains=[0.03] * 6,
                                    velocityGains=[1] * 6)

        for _ in range(300):
            p.stepSimulation()

        self.waypoints()

        observation = np.concatenate(((p.getLinkState(self.UR5Id, 7)[0]), (self.x[self.target_point_index], self.y[self.target_point_index], self.z[self.target_point_index])))
        # print("obs {}".format(observation))
        return np.array(observation)



    def step(self, action):
        print("**episode_no {}**".format(self.episode_no))
        print("**Step number {}**".format(self.target_point_index))
        # simulating robot for a single step
        a = action[0]
        b = action[1]
        c = action[2]
        collision = False
        target_ori_euler_end_eff = [math.pi / 2, math.pi / 2, 0]
        target_ori_quaternion_end_eff = p.getQuaternionFromEuler(target_ori_euler_end_eff)
        target_joint = p.calculateInverseKinematics(self.UR5Id, 7, targetPosition=[a, b, c],
                                                    targetOrientation=target_ori_quaternion_end_eff,
                                                    residualThreshold=0.00001, maxNumIterations=2000, solver=0)
        p.setJointMotorControlArray(self.UR5Id, range(1, 7), p.POSITION_CONTROL, targetPositions=target_joint,
                                    targetVelocities=[0] * 6, forces=[500] * 6, positionGains=[0.03] * 6,
                                    velocityGains=[1] * 6)
        for _ in range(300):
            p.stepSimulation()
            if p.getContactPoints():
                collision = True
                robot_position_on_collision = p.getLinkState(self.UR5Id, 7)[0]
                break


        robot_position = robot_position_on_collision if collision else p.getLinkState(self.UR5Id, 7)[0]

        dist_x = abs(robot_position[0] - self.x[self.target_point_index])
        dist_y = abs(robot_position[1] - self.y[self.target_point_index])
        dist_z = abs(robot_position[2] - self.z[self.target_point_index])

        total_distance = (dist_z*1000)**2 + (dist_y*1000)**2 + (dist_x*1000)**2
        #
        # mu = 0
        # sigma = 0.009
        # reward = ((math.exp(
        #     -(float(total_distance - mu) / sigma) * (float(total_distance - mu) / sigma) / 2.0) / math.sqrt(
        #     2.0 * math.pi) * sigma)) * 1000000

        reward = -1000 if collision else -math.sqrt(total_distance)




        # if (dist_x<= 0.01 and dist_y<= 0.01 and dist_z<= 0.01) :
        #      if (dist_x<= self.threshold_distance and dist_y<= self.threshold_distance and dist_z<= self.threshold_distance) :
        #         reward = 100
        #      else:
        #         reward = -((dist_x) + (dist_y) + (dist_z)) * 100
        # else:
        #       reward = -((dist_x) + (dist_y) + (dist_z)) * 1000


        info = {"episode": self.episode_no,
                "index" : self.target_point_index,
                "reward_step": reward,
                'distance_x': (robot_position[0] - self.x[self.target_point_index]),
                'distance_y': (robot_position[1] - self.y[self.target_point_index]),
                'distance_z': (robot_position[2] - self.z[self.target_point_index]),
                'action_by_policy': (a,b,c),
                'robot_pos': robot_position,
                'target': (self.x[self.target_point_index], self.y[self.target_point_index], self.z[self.target_point_index])}

        done= False
        if self.target_point_index != self.max_possible_target_point_index:
            observation = np.concatenate((np.array(robot_position), (
                self.x[self.target_point_index + 1], self.y[self.target_point_index + 1], self.z[self.target_point_index + 1])))

        else:
            observation = np.concatenate((np.array(robot_position), (0.0,0.0,0.6)))

        if self.target_point_index == self.max_possible_target_point_index:
                    self.episode_no += 1
                    done = True

        self.target_point_index += 1

        print(info)
        return np.array(observation), reward, done, info



    def close(self):
        p.disconnect()


