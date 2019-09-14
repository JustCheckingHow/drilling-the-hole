import numpy as np
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

    def distance_travelled(angle1, frequency, time):
        pass

    def decay_function(self, time, frequency):
        return frequency * np.exp(-self.decay_rate * time)

    def calculate_next_angle(self, time, frequency):
        angle = self.state[0] + self.time_delay * self.decay_function(
            time, frequency)  # past state plus update
        pass

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
