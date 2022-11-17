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

class ImageManipulation:
    def trimImage(image, boundary):
        image = image[
                boundary[0]:boundary[1],
                boundary[2]:boundary[3]
            ]
        return image

    def binaryFilter(image, min_limit, max_limit):
        ret, image = cv2.threshold(image, min_limit, max_limit, cv2.THRESH_BINARY)
        return image

    def morphologyOpen(image):
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))

class Contours:
    def getContourByArea(image, minArea = -float('Inf'), maxArea = float('Inf')):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        outer_contour = None

        for contour in contours:
            area = cv2.contourArea(contour)
            if minArea < area < maxArea:
                outer_contour = contour
                break

        return outer_contour