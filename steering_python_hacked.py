import clr, sys, os, time

sys.path.append(os.getcwd())

clr.AddReference(os.path.join(os.path.dirname(__file__), 'EAL.dll'))
clr.AddReference(os.path.join(os.path.dirname(__file__), 'SiP.dll'))

from System import String
from System.Collections import *

from EAL import Interfaces, Enums
from EAL.Interfaces import Motion
from EAL.EALConnection import EALConnection
from steering_interface import Commands

class SteeringPythonHacked():
    def __init__(self, device_ip, debug = False):
        self.eal_conn = EALConnection()
        self.debug = debug

        self.eal_conn.Connect(device_ip)

        self.axis = self.eal_conn.Motion.Axes[0]
        self.axis.SetCondition(Enums.AxisCondition.AXIS_CONDITION_ACTIVE)
        self.axis.Movement.Power(False)
        self.axis.SetCondition(Enums.AxisCondition.AXIS_CONDITION_ACTIVE_PARAMETERIZATION)       # Activates parameterisation mode
        self.eal_conn.InitializeEFC(0, True, 10000, False)                                       # Initializes the axis
        if debug: 
            self.eal_conn.Parameter.WriteData(2.0, 'C2.43')
        self.axis.SetCondition(Enums.AxisCondition.AXIS_CONDITION_ACTIVE)                        # Activates Operating mode
        self.axis.Movement.Power(True)                                                           # Powers-on task will be added to queue.

        self.freq = 0.0
        self.speed = 0.0
        self.direction = 1

    def set_freq(self, new_freq, accel_deccel = 4000.0):
        self.freq = new_freq
        self.accel_deccel = accel_deccel
        
    def setSpeed(self, speed, accel_deccel = 4000.0):
        self.speed = speed

    def set_command(self, command):
        
        if command == Commands.LEFT:
            self.direction = -1
            self.left()

        if command == Commands.RIGHT:
            self.direction = 1
            self.right()

        if command == Commands.STOP:
            self.stop()

    def left(self):
        self.axis.Movement.MoveFrequency(self.freq * self.direction, self.accel_deccel, self.accel_deccel, 0)

    def right(self):
        self.axis.Movement.MoveFrequency(self.freq * self.direction, self.accel_deccel, self.accel_deccel, 0)

    def stop(self):
        self.axis.Movement.MoveFrequency(0, self.accel_deccel, self.accel_deccel, 0)

    def move_frequency_wrapper(self, freq, accel, deccel, jerk):
        self.axis.Movement.MoveFrequency(freq, accel, deccel, jerk)

    def move_velocity_wrapper(self, velocity, accel, deccel, jerk):
        self.axis.Movement.MoveVelocity(velocity, accel, deccel, jerk)

    def get_actual_frequency_wrapper(self):
        return self.axis.GetActualFrequency()

    def get_actual_velocity_wrapper(self):
        if not self.debug:
            return -1
        return self.eal_conn.Parameter.ReadData('d0.01')