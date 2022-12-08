import cv2
import time
import os

class Viewer:
    def show(self):
        now = time.time()
        placeholder = cv2.imread(f"images/live/placeholder.jpg")
        cv2.imwrite("images/live/99.jpg", placeholder)
        while True:
            if time.time() - now > 0.1:
                with open("images/live/99.jpg", 'rb') as im :
                    im.seek(-2,2)
                    if im.read() == b'\xff\xd9':
                        image = cv2.imread(f"images/live/99.jpg")
                        height = image.shape[0]
                        width = image.shape[1]
                        multiplier = 720 / width
                        image = cv2.resize(image, (int(width * multiplier), int(height * multiplier)))
                        cv2.imshow("Latest inspection", image)
                        cv2.waitKey(1)
                        now = time.time()

viewer = Viewer()
viewer.show()