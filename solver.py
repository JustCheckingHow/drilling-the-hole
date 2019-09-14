import numpy as np
import time

from environment import Environment


class Solver:
    def __init__(self, env):
        self.env = env
        self.speed, self.normalized_speed = 0, 0
        self.delta = None
        self.position = np.asarray(env.reset()[-1][0])
        self.goal = 0
        self.final_action = None
        self.finished = False
        self.last_pos = self.position
        self.last_pos_2 = self.position

        self.coeff = 1
        self.coeff_decay = 0.7

    def zero(self):
        direction = np.sign(self.goal - self.position) * self.coeff
        start = time.time()

        if self.final_action is None:
            pos, _, _ = self.env.step([direction, self.goal])
            pos = np.asarray(pos[-1][0])
        else:
            pos, _, _ = self.env.step([self.final_action, self.goal])
            pos = np.asarray(pos[-1][0])
            self.finished = True

        if self.last_pos_2 == pos:
            self.coeff *= self.coeff_decay

        self.last_pos_2 = self.last_pos
        self.last_pos = pos

        delta = time.time() - start
        if self.delta is None:
            self.delta = delta
        else:
            self.delta = self.delta * 0.3 + delta * 0.7

        self.speed = pos - self.position
        self.normalized_speed = self.speed / delta
        real_speed = self.normalized_speed * self.delta

        if pos < self.goal < pos + real_speed:
            self.final_action = np.abs(self.goal - pos) / real_speed
        elif pos > self.goal > pos + self.speed:
            self.final_action = np.abs(self.goal - pos) / real_speed
        else:
            self.position = pos


if __name__ == "__main__":
    solver = Solver(Environment(4))
    for i in range(100):
        solver.zero()
        if solver.finished:
            break

    print(solver.env.state)
