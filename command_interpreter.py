import re
from steering_python import SteeringPython

class SteeringPythonMock:
    def move_angle_right(self, angle):
        print(f"moved {angle} degrees on right")

    def move_angle_left(self, angle):
        print(f"moved {angle} degrees on left")

    def pause(self, duration):
        print(f"paused for {duration} seconds")

    def set_freq(self, freq):
        print(f"set speed on {freq}")

    def stop(self):
        print("stopped")

    def return_to_base(self):
        print("returned to base position")

class CommandInterpreter:
    def __init__(self):
        self.sp = SteeringPythonMock()
        self.SPEED = 0

    def interpreter(self, command: str):
        regexp = re.compile(r"((^\s*(TURN)\s+([+-]\d+\s*)$)|"
                            r"(^\s*(PAUSE)\s+(\d+)\s*$)|"
                            r"(^\s*(SPEED)\s+(\d+)\s*$)|"
                            r"^\s*(STOP)\s*$)|"
                            r"^\s*(BASE)\s*$")
        m = regexp.match(command)
        if m is not None:
            command_words = m.group(0).split()
            cmd = command_words[0]
            if cmd == "TURN":
                value = command_words[1][1:]
                if command_words[1][0] == "+":
                    self.action_clockwise(value)
                else:
                    self.action_counterclockwise(value)
            elif cmd == "PAUSE":
                self.action_pause(command_words)
            elif cmd == "SPEED":
                self.action_speed(command_words)
            elif cmd == "STOP":
                self.action_stop()
            elif cmd == "BASE":
                self.action_base()
        else:
            raise ValueError("command {} could not be interpreted".format(command))

    def action_clockwise(self, value):
        if int(value) < 0:
            raise ValueError("invalid values provided: {}".format(value))
        self.sp.set_freq(self.SPEED)
        self.sp.move_angle_right(int(value) % 360)

    def action_counterclockwise(self, value):
        if int(value) < 0:
            raise ValueError("invalid values provided: {}".format(value))
        self.sp.set_freq(self.SPEED)
        self.sp.move_angle_left(int(value) % 360)

    def action_pause(self, command_words):
        if int(command_words[1]) < 0:
            raise ValueError("invalid values provided: {}".format(command_words[1]))
        self.sp.pause(int(command_words[1])/100)

    def action_speed(self, command_words):
        if int(command_words[1]) < 0:
            raise ValueError("invalid values provided: {}".format(command_words[1]))
        self.SPEED = command_words[1]

    def action_stop(self):
        self.sp.stop()

    def action_base(self):
        self.sp.return_to_base()


ci = CommandInterpreter()
ci.interpreter("SPEED 30")
ci.interpreter("TURN -50")
ci.interpreter("TURN -30")
ci.interpreter("SPEED 10")
ci.interpreter("TURN +370")
ci.interpreter("PAUSE 476")
ci.interpreter("STOP")
ci.interpreter("BASE")