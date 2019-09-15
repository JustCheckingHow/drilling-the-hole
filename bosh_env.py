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
        self.busy = False
        self.last_poll = 0

    def step(self, action, done):
        if not self.busy:
            if -1<action<1:
                self.sp.set_freq(action)

            if self.last_dir is None:
                if action==1:
                    self.sp.right()
                    self.last_dir=1
                elif action==-1:
                    self.sp.left()
                    self.last_dir=-1

            if done:
                self.sp.stop()
            self.last_poll = time.time()
            self.busy = True
        else:
            if time.time()-self.last_poll>0.2:
                self.busy = False
