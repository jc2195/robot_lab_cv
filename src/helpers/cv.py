import cv2
import numpy as np

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

    def presenceDetection(image):
        if len(np.array(image).shape) != 2:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        half = len(image)//2
        if image[half, half] > 100:
            return True
        else:
            return False

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