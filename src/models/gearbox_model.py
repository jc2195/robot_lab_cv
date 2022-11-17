from .gear_model import Gear
from .casing_model import Casing

import cv2
from types import SimpleNamespace
import time

Components = SimpleNamespace(
    TOP_CASING = SimpleNamespace(
        MASTER_LOCATION = (175,1175,100,1100),
        LEFT_HOLE_LOCATION = (460,570,340,450),
        RIGHT_HOLE_LOCATION = (460,570,540,650),
        MASTER_BINARY_THRESHOLD = 150,
        LEFT_HOLE_BINARY_THRESHOLD = 150,
        RIGHT_HOLE_BINARY_THRESHOLD = 150,
        HOLE_CONTOUR_AREA_MIN = 4000,
        HOLE_CONTOUR_AREA_MAX = 7000,
        CASING_DIAMETER_SPEC = 100,
        HOLE_DIAMETER_SPEC = 8.2,
        HOLE_DIAMETER_TOLERANCE = 0.5,
        LOGGING_NAME = "Top Casing"
    ),
    BOTTOM_CASING = SimpleNamespace(
        MASTER_LOCATION = (1300,2300,100,1100),
        LEFT_HOLE_LOCATION = (440,550,360,470),
        RIGHT_HOLE_LOCATION = (445,555,555,665),
        MASTER_BINARY_THRESHOLD = 220,
        LEFT_HOLE_BINARY_THRESHOLD = 15,
        RIGHT_HOLE_BINARY_THRESHOLD = 15,
        HOLE_CONTOUR_AREA_MIN = 500,
        HOLE_CONTOUR_AREA_MAX = 1500,
        CASING_DIAMETER_SPEC = 100,
        HOLE_DIAMETER_SPEC = 8.2,
        HOLE_DIAMETER_TOLERANCE = 0.5,
        LOGGING_NAME = "Bottom Casing"
    ),
    SMALL_GEAR = SimpleNamespace(
        MASTER_LOCATION = (990,1160,1460,1630),
        MASTER_BINARY_THRESHOLD = 70,
        AREA_CUTOFF = 5000,
        TEETH_COUNT = 14,
        LOGGING_NAME = "Small Gear"
    ),
    LARGE_GEAR = SimpleNamespace(
        MASTER_LOCATION = (140,490,1350,1700),
        MASTER_BINARY_THRESHOLD = 100,
        AREA_CUTOFF = 40000,
        TEETH_COUNT = 28,
        LOGGING_NAME = "Large Gear"
    )
)

class Gearbox:
    def __init__(self, filename):
        self.filename = filename
        self.image = None
        self.components = None
        self.inspection_time = None
        self.passing_parts = {
            Components.TOP_CASING.LOGGING_NAME: 0,
            Components.BOTTOM_CASING.LOGGING_NAME: 0,
            Components.SMALL_GEAR.LOGGING_NAME: 0,
            Components.LARGE_GEAR.LOGGING_NAME: 0
        }

    def populateComponents(self):
        self.components = {
            Components.TOP_CASING.LOGGING_NAME: Casing(self.image, Components.TOP_CASING),
            Components.BOTTOM_CASING.LOGGING_NAME: Casing(self.image, Components.BOTTOM_CASING),
            Components.SMALL_GEAR.LOGGING_NAME: Gear(self.image, Components.SMALL_GEAR),
            Components.LARGE_GEAR.LOGGING_NAME: Gear(self.image, Components.LARGE_GEAR)
        }

    def prepareImage(self, filename):
        img_rgb = cv2.imread(filename)
        img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        return img_grey

    def inspect(self):
        try:
            start_time = time.time()
            self.image = self.prepareImage(self.filename)
            self.populateComponents()
            for component in self.components:
                self.components[component].inspect()
            self.inspection_time = time.time() - start_time
        except:
            print('FATAL INSPECTION ERROR')

    def validate(self):
        for component in self.components:
            if self.components[component].status["code"] == 0:
                self.passing_parts[component] = 1

    def report(self):
        print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + self.filename + "\033[0m")

        for component in self.components:
            if self.components[component].status["code"] == 0:
                print("\033[95m" + self.components[component].metadata.LOGGING_NAME + ": " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m")
            else:
                print("\033[95m" + self.components[component].metadata.LOGGING_NAME + ": " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m")

        print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{self.inspection_time:.3f}" + " seconds" + "\033[0m")
        print("\n")

