import numpy as np
import math
from collections import deque
"""
ZERO ANGLE IS AT 12 o'clock 
0 Hz is STOP signal 
"""
MAX_FREQ = 50

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
        self.time_delta = 0.001

        # environment params
        self.decay_rate = 1.
        self.time_delay = 1.
        self.radius = 2.

        self.goal = 0

    def distance_travelled(self, angle, frequency, time):
        circumference = (2 * math.pi * self.radius)
        rotations = frequency * circumference * time  # 1 Hz is one rotation per second
        return angle + rotations * 360

    def decay_function(self, time, frequency):
        return frequency * np.exp(-self.decay_rate * time)

    def calculate_next_angle(self, frequency, time):
        previous_angle, goal = self.state
        angle = self.distance_travelled(previous_angle, frequency,
                                        time)  # past state plus update
        return angle%360/360.0

    def act(self, time, action):
        next_observation = (self.calculate_next_angle(action[0], time), self.goal)
        self.observations.append(next_observation)
        self.state = next_observation

    def step(self, action):
        # self.act_policy.append(action)
        self.act(self.time_delta, action)
        reward, done = self._check_win(action)
        return self.observations, reward, done

    def reset(self):
        position = 0.1
        self.goal = 0.5
        self.observations.clear()
        for _ in range(self.observations.maxlen):
            self.observations.append((position, self.goal))

        self.state = (position, self.goal)
        self.moves = np.arange(9)
        return self.observations

    def _check_win(self, action):
        if action[1] > 0:
            # done
            return -abs(10 * (self.state[0] - self.state[1])), True
        else:
            # not done
            return -abs(self.state[0] - self.state[1]), False
