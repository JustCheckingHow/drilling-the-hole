from video_api.read_from_cam import capture_camera_picture, capture_camera_video
from steering_python import SteeringPython
import time as tm
import threading

if __name__ == "__main__":
    sp = SteeringPython()

    for direction in [sp.right, sp.left]:
        dir = "right" if direction == sp.right else "left"
        for i in [1, 3, 5, 10, 15, 20]:
            t = threading.Thread(target=capture_camera_video, args=(dir + str(i) + "pink", 8))
            t.start()
            tm.sleep(2)
            sp.set_freq(i)
            direction()
            tm.sleep(4)
            sp.stop()
            tm.sleep(1)
            t.join()
