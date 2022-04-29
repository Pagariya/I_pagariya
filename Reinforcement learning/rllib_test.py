# import ray
# from ray import tune
# from ray.tune.registry import register_env
# from gym_LAMA_ur5.envs.lama_ur5_env import LamaEnv
# env_name = 'lama_ur5-v0'
#
# register_env(env_name, lambda config: LamaEnv())
#
# ray.init()
# tune.run(
#     "SAC",
#     stop={"timesteps_total": 2000},
#     config={
#         "env":env_name ,
#         "num_gpus": 0,
#         "num_workers": 1,
#         "evaluation_interval": 2,
#         #"lr": tune.grid_search([0.01, 0.001, 0.0001]),
#
#     },
# )



import ray
from ray import tune
import ray.rllib.agents.ppo as ppo

ray.init()
# tune.run(
#     "PPO",
stop_criteria={"timesteps_total": 1000},
config={
        "env": "CartPole-v0",
        "num_gpus": 0,
        "num_workers": 1,
        "lr": tune.grid_search([0.01, 0.001, 0.0001]),
        "eager": False,
    }

analysis = ray.tune.run(
    ppo.PPOTrainer,
    config=config,
    local_dir="~/ray"
    stop=stop_criteria,
    checkpoint_at_end=True)