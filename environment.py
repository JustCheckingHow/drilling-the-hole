import numpy as np

class Environment:
    def __init__(self):
        self.state = np.zeros((9))
        self.moves = np.arange(9)
        self.draws = 0
        self.p1_wins = 0
        self.p2_wins = 0

    def act(self, player, action):
        if self.state[action] == 0:
            self.state[action] = player

            reward, done = self._check_win()
            return self.state, reward, done 
        else:
            return -1, -1, -1

    def reset(self):
        self.state = np.zeros((9))
        self.moves = np.arange(9)
        return self.state
        
    def _check_win(self):
        winning_sets = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for winning_set in winning_sets:
            res = set(self.state[winning_set])
            if len(res)==1 and list(res)[0]!=0:
                if list(res)[0]==1:
                    self.p1_wins += 1
                else:
                    self.p2_wins += 1

                return 1, True

        if 0 not in set(self.state):
            self.draws += 1
            return 0, True
        return 0, False