import cv2
import numpy as np


def is_part_there(img):

    """
    Fist checks if an image is grey scaled and changes it if not
    This looks at the middle pixel of an image,
    assesses whether it is a part or the black background
    """
    if len(np.array(img).shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    half = len(img)//2
    if img[half, half] > 100:
        return True
    else:
        return False


