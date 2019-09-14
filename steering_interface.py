from enum import Enum

MAX_FREQ = 50
MIN_FREQ = 0
BROKER_IP = "192.168.0.1"
BROKER_PORT = 1883
PERSIST_SESSION = 60


class Commands(Enum):
    LEFT = 1
    RIGHT = 2
    STOP = 3

class SteeringInterface:
    def __init__(self):
        self._current_freq = None
        self._current_command = Commands.STOP

    def set_freq(self, new_freq):
        if int(new_freq) < MIN_FREQ or new_freq > MAX_FREQ:
            raise("SteeringInterface.freq, new_freq not in range!")
        pass

    def set_command(self, command):
        pass

    def left(self):
        pass

    def right(self):
        pass
