import numpy as np
import time

from environment import Environment


class Solver:
    def __init__(self, env):
        self.env = env
        self.speed, self.normalized_speed = 0, 0
        self.delta = None
        # self.position = np.asarray(env.reset()[-1][0])
        self.goal = 0.5
        self.final_action = None
        self.finished = False
        self.last_pos = 0
        self.last_pos_2 = 0

        self.coeff = 1
        self.coeff_decay = 0.7
        self.last_time = time.time()
        self.position = None

    def zero(self, time, position):
        delta = 0.2
        self.last_time = time

        direction = np.sign(self.goal - position) * self.coeff

        # if self.last_pos_2 == position:
        #     self.coeff *= self.coeff_decay

        self.last_pos_2 = self.last_pos
        self.last_pos = position

        if self.delta is None:
            self.delta = delta
        else:
            self.delta = self.delta * 0.3 + delta * 0.7

        if self.position is not None:
            self.speed = position - self.position
            self.normalized_speed = self.speed / delta
            real_speed = self.normalized_speed * self.delta
            print(real_speed)
            if position < self.goal < position + real_speed:
                self.final_action = np.abs(self.goal - position) / real_speed
            elif position > self.goal > position + self.speed:
                self.final_action = np.abs(self.goal - position) / real_speed
            else:
                self.position = position
            print(f"Position: {self.position}, Goal: {self.goal}, delta: {self.delta}, speed: {real_speed}, direction: {direction}")

        else:
            self.position = position

        if self.final_action is None:
            self.env.step(direction, False)
        else:
            print("FINAL")
            self.env.step(self.final_action, True)
            self.finished = True


if __name__ == "__main__":
    solver = Solver(Environment(4))
    solver.env.reset()
    for i in range(100):
        solver.zero(time.time(), solver.env.state[0])
        if solver.finished:
            break

    print(solver.env.state)
