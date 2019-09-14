from steering_interface import Commands, SteeringInterface
import paho.mqtt.client as mqtt

class SteeringPython(SteeringInterface):
    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.connect()

    def connect(self):
        self.client.connect("192.168.0.1", 1883, 60)

    def set_freq(self, new_freq):
        super().set_freq(new_freq)
        self.client.publish("freq", int(new_freq))

    def set_command(self, command):
        super().set_command()
        
        if command == Commands.LEFT:
            self.left()

        if command == Commands.RIGHT:
            self.right()

        if command == Commands.STOP:
            self.stop()


    def left(self):
        self.client.publish("move", "left")

    def right(self):
        self.client.publish("move", "right")

    def stop(self):
        self.client.publish("move", "stop")




