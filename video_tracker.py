import cv2
import numpy as np
import imutils
import math
from solver import Solver
from bosh_env import Environment
import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
import csv

sct = mss()


class Config:
    def __init__(self):
        with open('config.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.mydict = {rows[0]: rows[1] for rows in reader}
        print(self.mydict)

    def get(self, key):
        return self.mydict[key]

    def set(self, key, value):
        self.mydict[key] = value

    def __del__(self):
        with open('config.csv', mode='w') as infile:
            # writer = csv.DictWriter(infile, ["key", "val"])
            for key, item in self.mydict.items():
                infile.write(f"{key},{item}\n")


class ScreenCap:
    def read(self):
        w, h = 768, 432
        monitor = {'top': 410, 'left': 1753, 'width': w, 'height': h}
        img = Image.frombytes('RGB', (w, h), sct.grab(monitor).rgb)
        # img = np.array(img)[:, :, [2, 1, 0]]
        return np.array(img)


class VideoTracker:
    def __init__(self, video_stream):
        # self.vcap = cv2.VideoCapture(video_stream)
        self.solver = Solver(Environment())
        self.vcap = ScreenCap()
        self.config = Config()
        self.large_circle = None
        self.frame_no=0
        self.time = None
        self.enable_calibration = False
        self.calibrated = False
        self.function = self.solver.zeroero
        self.chain = []

    def calc_dist(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def set_instructions(self, instructions):
        self.chain = instructions

    def which_angle(self, tris, tracker_center):
        closest = None
        closest_dist = 9999999
        for p, ang in tris:
            dist = self.calc_dist(p, tracker_center)
            if dist <= closest_dist:
                closest_dist = dist
                closest = ang
        return closest

    def detect_large_circle(self, img):
        """
        Image must be in greyscale 
        """
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.2, 100, 50, 150,
                                   100)
        circle_mask = np.zeros(img.shape[:2], dtype='uint8')

        large_circle = None
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            print(circles)
            # loop over the (x, y) coordinates and radius of the circles
            try:
                for (x, y, r) in circles:
                    large_circle = (x, y, r)
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            except TypeError:
                return (0, 0, 1), circle_mask
        cv2.circle(circle_mask, tuple(large_circle[:2]), large_circle[-1], 255, -1)
        # masked_img = cv2.bitwise_and(img, img, mask=circle_mask)

        return large_circle, circle_mask

    def image_get_angles(self, img, large_circle):
        ANGLE_RESOLUTION = 5  # degs
        divide_circles = 360 / 60  # minute scale
        x, y, r = large_circle
        # generate a set of points on a circle
        tris = []
        angles = np.arange(0, 180, 10)
        angles_len = len(angles)
        for i, ang in enumerate(angles):
            # minute
            xp = int(r * np.sin(ang * (np.pi / 180))) + x
            yp = int(r * np.cos(ang * (np.pi / 180))) + y
            # xpn = int(r * np.sin(angles[(i + 1) % angles_len] * (np.pi / 180))) + x
            # ypn = int(r * np.cos(angles[(i + 1) % angles_len] * (np.pi / 180))) + y
            cv2.circle(img, (xp, yp), 3, (int(ang), 0, 0), -1)
            # reflect a point
            angp = 180 + ang
            # angp_rev = 180 + angles[(i + 1) % angles_len]
            xp2 = int(r * np.sin(angp * (np.pi / 180))) + x
            yp2 = int(r * np.cos(angp * (np.pi / 180))) + y
            # xp2n = int(r * np.sin(angp_rev * (np.pi / 180))) + x
            # yp2n = int(r * np.cos(angp_rev * (np.pi / 180))) + y
            cv2.circle(img, (xp2, yp2), 3, (0, int(ang), 255), -1)
            cv2.line(img, (xp, yp), (xp2, yp2), (255, 0, 0))
            tris.append(((xp, yp), ang))
            tris.append(((xp2, yp2), angp))
        return tris

    def change_mode(self, mode, *args):
        if mode=="angle":
            self.function = self.solver.zeroero
            self.solver.goal = args[0]
        elif mode=="rotation":
            self.solver.movement_angle = args[0]
            self.function = self.solver.zeroangle

    def run_tracking(self):
        # while (self.vcap.isOpened()):
        while True:
            # ret, frame = self.vcap.read()
            frame = self.vcap.read()
            frame = cv2.resize(frame, (int(800), int(480)))
            h, w, ch = frame.shape
            # converting from BGR to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Range for upper range
            lower = eval(self.config.get("pixels_lower").replace("  ", " ").replace(" ", ","))
            upper = eval(self.config.get("pixels_upper").replace("  ", " ").replace(" ", ","))

            lower_red = np.array(lower)
            upper_red = np.array(upper)

            mask = cv2.inRange(hsv, lower_red, upper_red)
            # Generating the final mask to detect red color
            res1 = cv2.bitwise_and(frame, frame, mask=mask)
            # res1  has color mask
            res1_gray = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.large_circle is None:
                self.large_circle, self.large_circle_mask = self.detect_large_circle(frame_gray)
            frame = cv2.bitwise_and(frame, frame, mask=self.large_circle_mask)
            frame_limited = cv2.bitwise_and(frame, frame, mask=mask)
            tris = self.image_get_angles(frame, self.large_circle)
            frame_limited_gray = cv2.cvtColor(frame_limited, cv2.COLOR_BGR2GRAY)
            cnts = cv2.findContours(frame_limited_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
            text = f"Angle: None"
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                try:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    # only proceed if the radius meets a minimum size
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), -1)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    angle = self.which_angle(tris, (x, y))
                    text = f"Angle: {angle}"

                    # current_ms = self.vcap.get(cv2.CAP_PROP_POS_MSEC)
                    if self.time is None:
                        # self.function(0, angle/360)
                        self.time = time.time()
                    else:
                        pass
                        # self.function(time.time()-self.time, angle/360)

                    if self.solver.solved:
                        print("SOLVED")
                        mode, args = self.chain.pop(0)
                        self.change_mode(mode, args)
                        self.solver.solved = False

                except ZeroDivisionError:
                        continue

            cv2.putText(frame, text, (10, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.imshow('Res', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # self.vcap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # vc = VideoTracker('rtsp://hackathon:!Hackath0n@192.168.0.2:554/2')
    vc = VideoTracker('output_left3pink.mp4')
    vc.set_instructions([["angle", 0.0], ["angle", 0.1]])
    vc.run_tracking()

