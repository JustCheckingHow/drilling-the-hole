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
        self.

    def step(self, action):
        if action[0]>0:
            dir = 1
        else:
            dir = -1


    def _move(self, dir):
        if dir==1:
            self.sp.right()
        elif dir==-1:
            self.sp.left()

