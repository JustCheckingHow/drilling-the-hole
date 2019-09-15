import numpy as np
import cv2
from mss import mss
from PIL import Image

sct = mss()

while 1:
    w, h = 768, 432
    monitor = {'top': 410, 'left': 1753, 'width': w, 'height': h}
    img = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)
    # img = np.array(img)[:, :, [2, 1, 0]]
    cv2.imshow('test', np.array(img))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break