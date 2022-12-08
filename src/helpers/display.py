import cv2
import time
import os

class Viewer:
    def show(self):
        now = time.time()
        while True:
            if time.time() - now > 0.1:
                with open("images/live/99.jpg", 'rb') as im :
                    im.seek(-2,2)
                    if im.read() == b'\xff\xd9':
                        image = cv2.imread(f"images/live/99.jpg")
                        cv2.imshow("Latest inspection", image)
                        cv2.waitKey(1)
                        now = time.time()