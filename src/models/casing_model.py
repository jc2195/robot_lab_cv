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

    def prepareImage(self, metadata):
        self.image = ImageManipulation.trimImage(self.master_image, metadata.MASTER_LOCATION)

    def prepareOuterImage(self):
        self.outer_image = ImageManipulation.binaryFilter(self.image, self.metadata.MASTER_BINARY_THRESHOLD, 255)

    def prepareLeftHoleImage(self, threshold):
        self.hole_images["left"] = ImageManipulation.trimImage(self.image, self.metadata.LEFT_HOLE_LOCATION)
        if self.metadata.LOGGING_NAME == "Bottom Casing":
            self.hole_images["left"] = cv2.equalizeHist(self.hole_images["left"])
        self.hole_images["left"] = ImageManipulation.binaryFilter(self.hole_images["left"], threshold, 255)

    def prepareRightHoleImage(self, threshold):
        self.hole_images["right"] = ImageManipulation.trimImage(self.image, self.metadata.RIGHT_HOLE_LOCATION)
        if self.metadata.LOGGING_NAME == "Bottom Casing":
            self.hole_images["right"] = cv2.equalizeHist(self.hole_images["right"])
        self.hole_images["right"] = ImageManipulation.binaryFilter(self.hole_images["right"], threshold, 255)

    def prepareHoleImages(self, threshold):
        # left = Thread(target=self.prepareLeftHoleImage, args=[threshold], daemon=False)
        # right = Thread(target=self.prepareRightHoleImage, args=[threshold], daemon=False)
        # left.start()
        # right.start()
        # left.join()
        # right.join()
        self.prepareLeftHoleImage(threshold)
        self.prepareRightHoleImage(threshold)
        # self.hole_images["left"] = ImageManipulation.trimImage(self.image, self.metadata.LEFT_HOLE_LOCATION)
        # self.hole_images["right"] = ImageManipulation.trimImage(self.image, self.metadata.RIGHT_HOLE_LOCATION)

        # if self.metadata.LOGGING_NAME == "Bottom Casing":
        #     self.hole_images["left"] = cv2.equalizeHist(self.hole_images["left"])
        #     self.hole_images["right"] = cv2.equalizeHist(self.hole_images["right"])

        # self.hole_images["left"] = ImageManipulation.binaryFilter(self.hole_images["left"], threshold, 255)
        # self.hole_images["right"] = ImageManipulation.binaryFilter(self.hole_images["right"], threshold, 255)

    def getMmPerPixel(self):
        outer_contour = Contours.getContourByArea(self.outer_image, 500000)
        (x,y),main_radius = cv2.minEnclosingCircle(outer_contour)
        self.mm_per_pixel = (self.metadata.CASING_DIAMETER_SPEC / 2) / main_radius

    def getHoleDiameters(self, minArea, maxArea):
        for label in ["left", "right"]:
            outer_contour = Contours.getContourByArea(self.hole_images[label], minArea, maxArea)
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
        self.refresh(image)
        try:
            self.prepareImage(self.metadata)
            self.prepareOuterImage()
            self.getMmPerPixel()
            try:
                self.prepareHoleImages(self.metadata.HOLE_BINARY_THRESHOLD)
                self.getHoleDiameters(self.metadata.HOLE_CONTOUR_AREA_MIN, self.metadata.HOLE_CONTOUR_AREA_MAX)
            except:
                if self.metadata.LOGGING_NAME == "Bottom Casing":
                    self.prepareHoleImages(self.metadata.HOLE_BINARY_THRESHOLD + 50)
                    self.getHoleDiameters(self.metadata.HOLE_CONTOUR_AREA_MIN * 2, self.metadata.HOLE_CONTOUR_AREA_MAX * 2)
            self.getStatus()
        except:
            pass

        return self.status

    def refresh(self, master_image):
        self.master_image = master_image
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