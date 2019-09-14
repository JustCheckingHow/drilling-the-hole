import cv2
import numpy as np
import imutils
import math 
from solver import Solver
from bosh_env import Environment


class VideoTracker:
    def __init__(self, video_stream):
        self.vcap = cv2.VideoCapture(video_stream)
        # self.solver = Solver(Environment())

    def calc_dist(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)

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
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.2, 100, 140, 150,
                                140)

        large_circle = None
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                large_circle = (x, y, r)
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255),
                            -1)
        circle_mask = np.zeros(img.shape[:2], dtype='uint8')
        cv2.circle(circle_mask, tuple(large_circle[:2]), large_circle[-1], 255, -1)
        masked_img = cv2.bitwise_and(img, img, mask=circle_mask)
        return large_circle, masked_img


    def image_get_angles(self, img, large_circle):
        ANGLE_RESOLUTION = 5  # degs
        divide_circles = 360 / 60  # minute scale
        x, y, r = large_circle
        # generate a set of points on a circle
        tris = []
        angles = np.arange(0, 180, 30)
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


    def run_tracking(self):
        while (self.vcap.isOpened()):
            ret, frame = self.vcap.read()
            frame = cv2.resize(frame, (int(800), int(480)))
            h, w, ch = frame.shape
            # converting from BGR to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Range for upper range
            
            lower_red = np.array([145, 210, 100])
            upper_red = np.array([169, 242, 195])
            
            mask = cv2.inRange(hsv, lower_red, upper_red)

            # Generating the final mask to detect red color
            res1 = cv2.bitwise_and(frame, frame, mask=mask)
            gray = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            large_circle, frame_gray = self.detect_large_circle(frame_gray)
            tris = self.image_get_angles(frame, large_circle)

            cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

                    current_ms = self.vcap.get(cv2.CAP_PROP_POS_MSEC)
                    # self.solver.zero(current_ms, angle/360)

                except ZeroDivisionError:
                    continue

            cv2.putText(frame, text, (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.imshow('Res', frame_gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.vcap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # vc = VideoTracker('rtsp://hackathon:!Hackath0n@192.168.0.2:554/2')
    vc = VideoTracker('output_left3pink.mp4')
    vc.run_tracking()