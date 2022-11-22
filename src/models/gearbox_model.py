from .gear_model import Gear
from .casing_model import Casing

import cv2
from types import SimpleNamespace
import time
from multiprocessing.pool import ThreadPool

Components = SimpleNamespace(
    TOP_CASING = SimpleNamespace(
        MASTER_LOCATION = (100,1250,50,1150),
        LEFT_HOLE_LOCATION = (470,620,350,500),
        RIGHT_HOLE_LOCATION = (470,620,550,700),
        MASTER_BINARY_THRESHOLD = 150,
        HOLE_BINARY_THRESHOLD = 150,
        HOLE_CONTOUR_AREA_MIN = 4000,
        HOLE_CONTOUR_AREA_MAX = 7000,
        CASING_DIAMETER_SPEC = 100,
        HOLE_DIAMETER_SPEC = 8.2,
        HOLE_DIAMETER_TOLERANCE = 0.5,
        LOGGING_NAME = "Top Casing"
    ),
    BOTTOM_CASING = SimpleNamespace(
        MASTER_LOCATION = (1200,2350,50,1170),
        LEFT_HOLE_LOCATION = (480,630,400,550),
        RIGHT_HOLE_LOCATION = (480,630,600,750),
        MASTER_BINARY_THRESHOLD = 220,
        HOLE_BINARY_THRESHOLD = 9,
        HOLE_CONTOUR_AREA_MIN = 500,
        HOLE_CONTOUR_AREA_MAX = 1500,
        CASING_DIAMETER_SPEC = 100,
        HOLE_DIAMETER_SPEC = 8.2,
        HOLE_DIAMETER_TOLERANCE = 0.5,
        LOGGING_NAME = "Bottom Casing"
    ),
    SMALL_GEAR = SimpleNamespace(
        MASTER_LOCATION = (920,1130,1430,1640),
        MASTER_BINARY_THRESHOLD = 70,
        AREA_CUTOFF = 5000,
        TEETH_COUNT = 14,
        LOGGING_NAME = "Small Gear"
    ),
    LARGE_GEAR = SimpleNamespace(
        MASTER_LOCATION = (50,460,1330,1720),
        MASTER_BINARY_THRESHOLD = 100,
        AREA_CUTOFF = 40000,
        TEETH_COUNT = 28,
        LOGGING_NAME = "Large Gear"
    )
)

class Gearbox:
    def __init__(self):
        self.image = None
        self.components = {
            Components.TOP_CASING.LOGGING_NAME: Casing(Components.TOP_CASING),
            Components.BOTTOM_CASING.LOGGING_NAME: Casing(Components.BOTTOM_CASING),
            Components.SMALL_GEAR.LOGGING_NAME: Gear(Components.SMALL_GEAR),
            Components.LARGE_GEAR.LOGGING_NAME: Gear(Components.LARGE_GEAR)
        }
        self.inspection_time = None
        self.passing_parts = {
            Components.TOP_CASING.LOGGING_NAME: 0,
            Components.BOTTOM_CASING.LOGGING_NAME: 0,
            Components.SMALL_GEAR.LOGGING_NAME: 0,
            Components.LARGE_GEAR.LOGGING_NAME: 0
        }
        self.pool = ThreadPool(4)

    def inspectComponent(self, component):
        component.inspect(self.image)

    def inspect(self, image):
        self.image = image
        self.refresh()
        try:
            start_time = time.time()
            self.pool.map(func=self.inspectComponent, iterable=self.components.values())
            self.inspection_time = (time.time() - start_time) * 1000
            self.validate()
            self.report()
        except:
            print('FATAL INSPECTION ERROR')

    def validate(self):
        for component in self.components:
            if self.components[component].status["code"] == 0:
                self.passing_parts[component] = 1

    def report(self):
        print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + "1" + "\033[0m")

        for component in self.components.values():
            if component.status["code"] == 0:
                print("\033[95m" + component.metadata.LOGGING_NAME + ": " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m")
            else:
                print("\033[95m" + component.metadata.LOGGING_NAME + ": " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m")

        print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{self.inspection_time:.3f}" + " ms" + "\033[0m")
        print("\n")

    def refresh(self):
        self.inspection_time = None
        self.passing_parts = {
            Components.TOP_CASING.LOGGING_NAME: 0,
            Components.BOTTOM_CASING.LOGGING_NAME: 0,
            Components.SMALL_GEAR.LOGGING_NAME: 0,
            Components.LARGE_GEAR.LOGGING_NAME: 0
        }