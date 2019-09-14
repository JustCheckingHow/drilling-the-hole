import numpy as np
import math
from collections import deque

import time

"""
ZERO ANGLE IS AT 12 o'clock 
0 Hz is STOP signal 
"""
MAX_FREQ = 5

# action = (freq, ?STOP)
# Hz, True/False

# observation - state
# [(ang, goal), (angl, goal)....]


class Environment:
    def __init__(self, N):
        self.state = np.zeros((1, 2))
        self.moves = np.arange(1)
        self.state_history = []
        self.act_policy = []
        self.observations = deque(maxlen=N)
        self.time_delta = 0.03

        # environment params
        self.decay_rate = 1.
        self.time_delay = 1.
        self.radius = 2.

        self.goal = 0
        self.movement = 0

    def distance_travelled(self, frequency, time):
        rotations = frequency * time * MAX_FREQ # 1 Hz is one rotation per second
        return rotations

    def decay_function(self, time, frequency):
        return frequency * np.exp(-self.decay_rate * time)

    def calculate_next_angle(self, frequency, time):
        angle = self.distance_travelled(frequency, time)  # past state plus update
        print(f"Angle: {self.state[0]}, input:{frequency}, movement: {angle}, result: {(angle + self.state[0]) % 1}, ", end="")
        self.movement = angle
        return (angle + self.state[0]) % 1

    def act(self, time, action):
        next_observation = (self.calculate_next_angle(action[0], time), self.goal)
        self.observations.append(next_observation)
        # self.state = next_observation
        return next_observation

    def step(self, action):
        # self.act_policy.append(action)
        next_obs = self.act(self.time_delta, action)
        reward, done = self._check_win(action)
        print(f"reward: {reward}")
        self.state = next_obs
        time.sleep(self.time_delta)
        self.time_delay += np.random.random()*0.1-0.05
        return self.observations, reward, done

    def reset(self):
        position = np.random.random()
        self.goal = 0
        self.observations.clear()
        for _ in range(self.observations.maxlen):
            self.observations.append((position, self.goal))

        self.state = (position, self.goal)
        self.moves = np.arange(9)
        return self.observations

    def _check_win(self, action):
        # state[1] = 0.5
        # state[0] = 0.3
        # movement = 0.3
        # reward = abs(0.5 - 0.3 - 0.3) - abs (0.5-0.3) = 0.1-0.2 = -0.1
        reward = np.abs(self.state[1] - (self.state[0] + self.movement)) - np.abs(self.state[1] - self.state[0])
        if action[1] > 10:
            # done
            return -np.abs(self.state[1] - (self.state[0] + self.movement))*0, True
        else:
            # not done
            return -reward, False
