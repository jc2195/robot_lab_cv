from ..helpers.cv import ImageManipulation, Contours
import cv2
import numpy as np

class Gear:
    def __init__(self, master_image, metadata):
        self.metadata = metadata
        self.master_image = master_image
        self.type = metadata.LOGGING_NAME
        self.location = metadata.MASTER_LOCATION
        self.image = None
        self.teeth = 0
        self.status = {
            "code": 99,
            "message": "Inspection incomplete"
        }

    def prepareImage(self, image, metadata):
        image = ImageManipulation.trimImage(image, metadata.MASTER_LOCATION)
        image = ImageManipulation.binaryFilter(image, metadata.MASTER_BINARY_THRESHOLD, 255)
        image = ImageManipulation.morphologyOpen(image)
        return image

    def getNumTeeth(self):
        outer_contour = Contours.getContourByArea(self.image, self.metadata.AREA_CUTOFF)

        centre, main_radius = cv2.minEnclosingCircle(outer_contour)
        main_radius -= 15

        blank_image = np.full((self.image.shape[0], self.image.shape[1]), 0, dtype=np.uint8)
        img1 = cv2.circle(blank_image.copy(),(int(centre[0]),int(centre[1])), int(main_radius), 20, 2)
        img2 = cv2.drawContours(blank_image.copy(), outer_contour, -1, 20, 2)
        intersection = img1 + img2
        ret, intersection = cv2.threshold(intersection, 30, 255, cv2.THRESH_BINARY)

        cnts = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        self.teeth = len(cnts) / 2

    def getStatus(self):
        if self.teeth == self.metadata.TEETH_COUNT:
            self.status["code"] = 0
            self.status["message"] = "Pass"
        elif self.teeth < 2:
            self.status["code"] = 1
            self.status["message"] = "Worn gear"
        else:
            self.status["code"] = 2
            self.status["message"] = "Missing teeth"

    def inspect(self):
        self.image = self.prepareImage(self.master_image, self.metadata)
        self.getNumTeeth()
        self.getStatus()
        return self.status