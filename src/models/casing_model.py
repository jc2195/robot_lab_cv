from ..helpers.cv import ImageManipulation, Contours
from multiprocessing.pool import ThreadPool
import cv2

class Casing:
    def __init__(self, metadata):
        self.metadata = metadata
        self.master_image = None
        self.type = metadata.LOGGING_NAME
        self.location = metadata.MASTER_LOCATION
        self.image = None
        self.outer_image = None
        self.hole_images = {
            "left": None,
            "right": None
        }
        self.mm_per_pixel = None
        self.hole_diameters = {
            "left": None,
            "right": None
        }
        self.status = {
            "code": 99,
            "message": "Inspection incomplete"
        }
        self.pool = ThreadPool()

    def prepareImage(self):
        self.image = ImageManipulation.trimImage(self.master_image, self.metadata.MASTER_LOCATION)

    def prepareOuterImage(self):
        self.outer_image = ImageManipulation.binaryFilter(self.image, self.metadata.MASTER_BINARY_THRESHOLD, 255)
        self.getMmPerPixel()

    def prepareLeftHoleImage(self):
        self.hole_images["left"] = ImageManipulation.trimImage(self.image, self.metadata.LEFT_HOLE_LOCATION)
        if self.metadata.LOGGING_NAME == "Bottom Casing":
            self.hole_images["left"] = cv2.equalizeHist(self.hole_images["left"])
        self.hole_images["left"] = ImageManipulation.binaryFilter(self.hole_images["left"], self.metadata.HOLE_BINARY_THRESHOLD, 255)

    def prepareRightHoleImage(self):
        self.hole_images["right"] = ImageManipulation.trimImage(self.image, self.metadata.RIGHT_HOLE_LOCATION)
        if self.metadata.LOGGING_NAME == "Bottom Casing":
            self.hole_images["right"] = cv2.equalizeHist(self.hole_images["right"])
        self.hole_images["right"] = ImageManipulation.binaryFilter(self.hole_images["right"], self.metadata.HOLE_BINARY_THRESHOLD, 255)

    def prepareHoleImages(self):
        self.prepareLeftHoleImage()
        self.prepareRightHoleImage()

    def getMmPerPixel(self):
        outer_contour = Contours.getContourByArea(self.outer_image, 500000)
        (x,y),main_radius = cv2.minEnclosingCircle(outer_contour)
        self.mm_per_pixel = (self.metadata.CASING_DIAMETER_SPEC / 2) / main_radius

    def getHoleDiameters(self):
        for label in ["left", "right"]:
            outer_contour = Contours.getContourByArea(self.hole_images[label], self.metadata.HOLE_CONTOUR_AREA_MIN, self.metadata.HOLE_CONTOUR_AREA_MAX)
            centre, hole_radius = cv2.minEnclosingCircle(outer_contour)
            self.hole_diameters[label] = hole_radius * 2 * self.mm_per_pixel

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

    def inspect(self, image):
        self.master_image = image
        self.refresh()
        try:
            self.prepareImage()
            self.prepareOuterImage()
            try:
                self.prepareHoleImages()
                self.getHoleDiameters()
            except:
                if self.metadata.LOGGING_NAME == "Bottom Casing":
                    self.prepareHoleImages(self.metadata.HOLE_BINARY_THRESHOLD + 50)
                    self.getHoleDiameters(self.metadata.HOLE_CONTOUR_AREA_MIN * 2, self.metadata.HOLE_CONTOUR_AREA_MAX * 2)
            self.getStatus()
        except:
            pass

        return self.status

    def refresh(self):
        self.image = None
        self.outer_image = None
        self.hole_images = {
            "left": None,
            "right": None
        }
        self.mm_per_pixel = None
        self.hole_diameters = {
            "left": None,
            "right": None
        }
        self.status = {
            "code": 99,
            "message": "Inspection incomplete"
        }