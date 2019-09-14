import numpy as np
import math
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
        self.observations = []

        # environment params
        self.decay_rate = 1.
        self.time_delay = 1.
        self.radius = 2.

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
        return angle

    def act(self, time, action):
        next_observation = (0., False)
        self.observations.append(next_observation)

    def step(self, action):
        self.act_policy.append(action)
        reward, done = self._check_win(action)
        return self.state, reward, done

    def reset(self):
        self.state = np.zeros((9))
        self.moves = np.arange(9)
        return self.state

    def _check_win(self, action):
        if action[1]:
            # done
            return 10 * (self.state[0] - self.state[1]), True
        else:
            # not done
            return (self.state[0] - self.state[1]), False
