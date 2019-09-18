import re
import time
import video_tracker


class CommandInterpreter:
    def __init__(self):
        self.list_of_instructions = []
        self.SPEED = 0

    def interpreter(self, command: str):
        print("command: ", command)
        try:
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
                    value = command_words[1]
                    self.list_of_instructions.append(["TURN", int(value)])
                    print("TURN")
                elif cmd == "PAUSE":
                    self.list_of_instructions.append(["PAUSE"])
                    print("PAUSE")
                elif cmd == "SPEED":
                    print("SPEED")
                    self.list_of_instructions.append(
                        ["SPEED", int(command_words[1])])
                elif cmd == "STOP":
                    print("STOP")
                    self.list_of_instructions.append(["STOP"])
                    self.list_of_instructions = []
                elif cmd == "BASE":
                    print("BASE")
                    self.list_of_instructions.append(["BASE"])
            else:
                print("command {} could not be interpreted".format(command))
        except TypeError:
            pass


if __name__ == "__main__":
    ci = CommandInterpreter()
    ci.interpreter("SPEED 30")
    ci.interpreter("TURN +200")
    ci.interpreter("TURN -50")
    ci.interpreter("TURN -30")
    ci.interpreter("SPEED 10")
    ci.interpreter("TURN +370")
    ci.interpreter("PAUSE 476")
    ci.interpreter("STOP")
    ci.interpreter("BASE")
