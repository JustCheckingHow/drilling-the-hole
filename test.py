from steering_python import SteeringPython
import time as tm

if __name__ == "__main__":
    sp = SteeringPython()

    sp.set_freq(1)
    sp.right()
    tm.sleep(1)
    sp.stop()


