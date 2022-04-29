import gym
from stable_baselines.sac.policies import MlpPolicy
from stable_baselines import SAC
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

env = gym.make('lama_ur5-v0')

model = SAC(MlpPolicy, env, verbose=1, tensorboard_log="./test1/")
model.learn(total_timesteps=7000)

*************************NEW SCRIPT*******************************
import gym
import gym_LAMA_ur5
import numpy as np
import os
from stable_baselines.sac.policies import MlpPolicy
from stable_baselines import SAC
from stable_baselines.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold


env = gym.make('CartPole-v1')

#callback_on_best = StopTrainingOnRewardThreshold(reward_threshold=5, verbose=1)
#eval_callback = EvalCallback(env, callback_on_new_best=callback_on_best, verbose=1)

model = SAC(MlpPolicy, env)
log_dir = "/tmp/"
model.save(log_dir + "lama")
stats_path = os.path.join(log_dir, "lama.pkl")
model.get_parameter_list()

*************************NEW SCRIPT*******************************

model.learn(total_timesteps=1000000)
model.save(stats_path)

del model

model = SAC.load(log_dir + "lama")

obs = env.reset()

reward_episodes = {reward_episode: 0 for reward_episode in range(10)}
for e in range(300):
    env.reset()
    for t in range(500):
        action, _ = model.predict(obs)
        observation, reward, done, info=env.step(action)
        print(info)
        reward_episodes[e] += reward


print(reward_episodes)
env.close()

#


