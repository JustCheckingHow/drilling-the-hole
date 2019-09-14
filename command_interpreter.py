import re
from steering_python import SteeringPython

class SteeringPythonMock:
    def move_angle_right(self, angle):
        print(f"moved {angle} degrees on right")

    def move_angle_left(self, angle):
        print(f"moved {angle} degrees on left")

    def pause(self, duration):
        print(f"paused for {duration} seconds")

    def stop(self):
        print("stopped")


class CommandInterpreter:
    def __init__(self):
        self.sp = SteeringPythonMock()
        self.SPEED = 0
        self.PAUSE = 0

    def interpreter(self, command: str):
        regexp = re.compile(r"(^(CLOCKWISE) (\d+)$|(^(PAUSE) (\d+) (ms|s|m)$)|(^(COUNTERCLOCKWISE) (\d+)$)|^(STOP)$)")
        m = regexp.match(command)
        if m is not None:
            command_words = m.group(0).split(" ")
            cmd = command_words[0]
            if cmd == "CLOCKWISE" and int(command_words[1]) > 0:
                self.action_clockwise(command_words)
            elif cmd == "COUNTERCLOCKWISE" and int(command_words[1]) > 0:
                self.action_counterclockwise(command_words)
            elif cmd == "PAUSE" and int(command_words[1]) > 0:
                self.action_pause(command_words)
            elif cmd == "STOP":
                self.action_stop()
        else:
            raise ValueError("command {} could not be interpreted".format(command))

    def action_clockwise(self, command_words):
        if int(command_words[1]) < 0:
            raise ValueError("invalid values provided: {}".format(command_words[1]))
        self.sp.move_angle_right(int(command_words[1]) % 360)

    def action_counterclockwise(self, command_words):
        if int(command_words[1]) < 0:
            raise ValueError("invalid values provided: {}".format(command_words[1]))
        self.sp.move_angle_left(int(command_words[1]) % 360)

    def action_pause(self, command_words):
        if int(command_words[1]) < 0:
            raise ValueError("invalid values provided: {}".format(command_words[1]))
        unit = command_words[2]
        if unit == "m":
            duration = int(command_words[1]) * 60
        elif unit == "ms":
            duration = int(command_words[1]) / 100
        else:
            duration = int(command_words[1])
        self.sp.pause(duration)

    def action_stop(self):
        self.sp.stop()




ci = CommandInterpreter()
ci.interpreter("CLOCKWISE 700")
ci.interpreter("CLOCKWISE -700")
ci.interpreter("COUNTERCLOCKWISE 200")
ci.interpreter("PAUSE 600 ms")
ci.interpreter("PAUSE 600 m")
ci.interpreter("PAUSE 60 s")
ci.interpreter("STOP")