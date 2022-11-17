from ..helpers.cv import ImageManipulation, Contours
import cv2

class Casing:
    def __init__(self, master_image, metadata):
        self.metadata = metadata
        self.master_image = master_image
        self.type = metadata.LOGGING_NAME
        self.location = metadata.MASTER_LOCATION
        self.image = None
        self.outer_image = None
        self.left_hole_image = None
        self.right_hole_image = None
        self.mm_per_pixel = None
        self.hole_diameters = {
            "left": None,
            "right": None
        }
        self.status = {
            "code": 99,
            "message": "Inspection incomplete"
        }

    def prepareImage(self, image, metadata):
        image = ImageManipulation.trimImage(image, metadata.MASTER_LOCATION)
        return image

    def prepareOuterImage(self):
        self.outer_image = ImageManipulation.binaryFilter(self.image, self.metadata.MASTER_BINARY_THRESHOLD, 255)

    def prepareHoleImages(self):
        self.left_hole_image = ImageManipulation.trimImage(self.image, self.metadata.LEFT_HOLE_LOCATION)
        self.right_hole_image = ImageManipulation.trimImage(self.image, self.metadata.RIGHT_HOLE_LOCATION)

        if self.metadata.LOGGING_NAME == "Bottom Casing":
            self.left_hole_image = cv2.equalizeHist(self.left_hole_image)
            self.right_hole_image = cv2.equalizeHist(self.right_hole_image)

        self.left_hole_image = ImageManipulation.binaryFilter(self.left_hole_image, self.metadata.LEFT_HOLE_BINARY_THRESHOLD, 255)
        self.right_hole_image = ImageManipulation.binaryFilter(self.right_hole_image, self.metadata.RIGHT_HOLE_BINARY_THRESHOLD, 255)

    def getMmPerPixel(self):
        outer_contour = Contours.getContourByArea(self.outer_image, 500000)
        (x,y),main_radius = cv2.minEnclosingCircle(outer_contour)
        self.mm_per_pixel = (self.metadata.CASING_DIAMETER_SPEC / 2) / main_radius

    def getHoleDiameters(self):
        for hole in self.hole_diameters:
            outer_contour = Contours.getContourByArea(self.left_hole_image, self.metadata.HOLE_CONTOUR_AREA_MIN, self.metadata.HOLE_CONTOUR_AREA_MAX)
            centre, hole_radius = cv2.minEnclosingCircle(outer_contour)
            self.hole_diameters[hole] = hole_radius * 2 * self.mm_per_pixel

    def getStatus(self):
        minSpec = self.metadata.HOLE_DIAMETER_SPEC - self.metadata.HOLE_DIAMETER_TOLERANCE
        maxSpec = self.metadata.HOLE_DIAMETER_SPEC + self.metadata.HOLE_DIAMETER_TOLERANCE

        if (minSpec < self.hole_diameters["left"] < maxSpec) and (minSpec < self.hole_diameters["right"] < maxSpec):
            self.status["code"] = 0
            self.status["message"] = "Pass"
        elif (maxSpec < self.hole_diameters["left"]) and (minSpec < self.hole_diameters["right"] < maxSpec):
            self.status["code"] = 1
            self.status["message"] = "Left hole diameter too large"
        elif (minSpec < self.hole_diameters["left"] < maxSpec) and (maxSpec < self.hole_diameters["right"]):
            self.status["code"] = 2
            self.status["message"] = "Right hole diameter too large"
        elif (maxSpec < self.hole_diameters["left"]) and (maxSpec < self.hole_diameters["right"]):
            self.status["code"] = 3
            self.status["message"] = "Both hole diameters too large"
        elif (minSpec > self.hole_diameters["left"]) and (minSpec < self.hole_diameters["right"] < maxSpec):
            self.status["code"] = 4
            self.status["message"] = "Left hole diameter too small"
        elif (minSpec < self.hole_diameters["left"] < maxSpec) and (minSpec > self.hole_diameters["right"]):
            self.status["code"] = 5
            self.status["message"] = "Right hole diameter too small"
        elif (minSpec > self.hole_diameters["left"]) and (minSpec > self.hole_diameters["right"]):
            self.status["code"] = 6
            self.status["message"] = "Both hole diameters too small"
        elif (minSpec > self.hole_diameters["left"]) and (maxSpec < self.hole_diameters["right"]):
            self.status["code"] = 7
            self.status["message"] = "Left hole diameter too small, right hole diameter too large"
        elif (maxSpec < self.hole_diameters["left"]) and (minSpec > self.hole_diameters["right"]):
            self.status["code"] = 8
            self.status["message"] = "Left hole diameter too large, right hole diameter too small"

    def inspect(self):
        self.image = self.prepareImage(self.master_image, self.metadata)
        self.prepareOuterImage()
        self.prepareHoleImages()
        self.getMmPerPixel()
        self.getHoleDiameters()
        self.getStatus()
        return self.status