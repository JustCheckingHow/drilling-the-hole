from environment import Environment
from teacher import Teacher
from ddpg.agent import Agent, Config

lr_actor = 7e-3
lr_critic = 3e-4
history_length = 4

env = Environment(history_length)
teacher = Teacher(env)
config = Config(buffer_size=4000, batch_size=256, gamma=0.98, tau=1e-3, lr_actor=lr_actor, lr_critic=lr_critic, update_every=4)
agent = Agent(history_length, action_size=2, config=config)

logs = teacher.train(agent, 10000, 100, history_length)