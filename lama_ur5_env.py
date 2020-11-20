import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random
from numpy import genfromtxt


class LamaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # 34.12659403193003
        # -33.92315242325826
        physicsClient = p.connect(p.DIRECT)
        p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=217.60, cameraPitch=-99.80,
                                     cameraTargetPosition=[-0.03, -0.04, -0.30])
        self.action_space = spaces.Box(np.array([-38, -38, -38, -38, -38, -38]),
                                       np.array([38, 38, 38, 38, 38, 38]), shape=(6,),
                                       dtype=np.float32)
        self.observation_space = spaces.Box(
            np.array([-38, -38, -38, -38, -38, -38,-38, -38, -38, -38, -38, -38,-38, -38, -38, -38, -38, -38]),
            np.array([38, 38, 38, 38, 38, 38,38, 38, 38, 38, 38, 38,38, 38, 38, 38, 38, 38]), shape=(18,), dtype=np.float32)


        self.x = np.linspace(0.25, 0.30, 5)
        self.y = 0.30
        self.z = .4
        self.vel_list = []
        self.base_Position = [0, 0, 1]
        self.step_episode = 0
        self.file = open("vel_datas.csv", "a")
        self.my_data = genfromtxt('vel_data_straight_line.csv', delimiter=',')
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        planeId = p.loadURDF("plane.urdf")
        target_ori_euler_base = [math.pi, 0, 0]
        target_ori_quaternion = p.getQuaternionFromEuler(target_ori_euler_base)
        self.UR5Id = p.loadURDF(
            ## PUT THE URDF FILE PATH HERE, IN MY CASE = /home/anshul/Documents/pybulletproject/robot_movement_interface/dependencies/ur_description/urdf/ur5_robot.urdf
            "/home/anshul/Documents/pybulletproject/robot_movement_interface/dependencies/ur_description/urdf/ur5_robot.urdf",
            useFixedBase=1, basePosition=self.base_Position, baseOrientation=target_ori_quaternion)

        # p.addUserDebugLine((0.3, 0.3, 1.2), (0.5, 0.3, 1.2), lineColorRGB=[200, 100, 100])
        # p.addUserDebugLine((0.3, 0.3, 1.2), (0.3, 0.5, 1.2), lineColorRGB=[200, 100, 100])

    def reset(self):
        # reseting the environmnet with intial pose
        p.resetSimulation
        self.step_episode = 0
        # file = open("vel_datas.csv", "r+")
        # file.seek(0)
        # file.truncate(0)
        self.vel_list.clear()
        rest_poses = [0, 0, 0, 0, 0, 0]
        for i in range(1, 7):
            p.resetJointState(self.UR5Id, i, rest_poses[i-1])

        observation = np.concatenate(((0, 0, 0, 0, 0, 0), self.my_data[0], self.my_data[1]))

        return np.array(observation)

    def step(self, action):
        done = False
        reward = 0
        info = {}
        arr = (action[0], action[1], action[2], action[3], action[4], action[5])

        self.vel_list.append(arr)
        if self.step_episode == 499:
            # my_data1 = genfromtxt('vel_datas.csv', delimiter=',')
            way_point = []
            info = {}
            done = True
            reward = 0
            for i in range(500):
                p.setJointMotorControlArray(self.UR5Id, range(1, 7), p.VELOCITY_CONTROL, targetVelocities=self.vel_list[i])
                p.stepSimulation()
                if i % 99 == 0:
                    way_point.append(p.getLinkState(self.UR5Id, 7)[0])

            for j in range(5):
                info["difference_at j+1 point"] = [
                    self.x[j] - way_point[j][0] + self.y - way_point[j][1] + self.z - way_point[j][2]]
                reward += -np.log(abs((self.x[j] - way_point[j][0]) + (self.y - way_point[j][1]) + (
                        self.z - way_point[j][2])))

            info["achieved_points"] = way_point
            info["target_points"] = [self.x, self.y, self.z]
            print(reward)

        if self.step_episode == 499:
            observation = np.zeros(18)
        else:
            observation = np.concatenate((self.my_data[self.step_episode - 1], self.my_data[self.step_episode],
                                          self.my_data[self.step_episode + 1]))

        self.step_episode += 1
        # print(self.step_episode)

        return np.array(observation), reward, done, info

    def seed(self):
        pass

    def close(self):
        p.disconnect()
