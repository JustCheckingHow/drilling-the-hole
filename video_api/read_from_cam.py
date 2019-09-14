import cv2
import os
from datetime import datetime


def capture_camera_video():
    capture = cv2.VideoCapture('rtsp://hackathon:!Hackath0n@192.168.0.2:554/1')
    print(capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT), capture.get(cv2.CAP_PROP_FPS))

    if not os.path.exists("./videos"):
        os.mkdir("./videos")

    out_file = "output_"+str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".mp4"
    out = cv2.VideoWriter("./videos/"+out_file, -1, 60.0, (1280, 720))

    while(True):
        ret, frame = capture.read()
        if ret:
            out.write(frame)
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    out.release()
    cv2.destroyAllWindows()

def capture_camera_picture():
    capture = cv2.VideoCapture('rtsp://hackathon:!Hackath0n@192.168.0.2:554/1')
    print(capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT), capture.get(cv2.CAP_PROP_FPS))

    if not os.path.exists("./pictures"):
        os.mkdir("./pictures")
    ret, frame = capture.read()
    if ret:
        cv2.imshow('frame', frame)
        cv2.imwrite("./pictures/output_"+str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".png", frame)
    capture.release()
    cv2.destroyAllWindows()

