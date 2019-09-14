import numpy as np
import math
from collections import deque
from steering_python import SteeringPython

import time


class Environment:
    def __init__(self):
        self.sp = SteeringPython()
        self.sp.set_freq(1)
        self.last_dir = None

    def step(self, action, done):
        if -1<action<1:
            self.sp.set_freq(action[0])
        if action>0:
            self.sp.right()
        else:
            self.sp.left()

        if done:
            self.sp.stop()
