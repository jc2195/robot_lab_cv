from .gear_model import Gear
from .casing_model import Casing
from multiprocessing.pool import ThreadPool
from types import SimpleNamespace

Components = SimpleNamespace(
    TOP_CASING = SimpleNamespace(
        MASTER_LOCATION = (1270,2270,230,1230),
        LEFT_HOLE_LOCATION = (435,595,310,460),
        RIGHT_HOLE_LOCATION = (440,600,510,660),
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
        MASTER_LOCATION = (150,1150,210,1210),
        LEFT_HOLE_LOCATION = (435,585,335,485),
        RIGHT_HOLE_LOCATION = (430,580,530,680),
        MASTER_BINARY_THRESHOLD = 220,
        HOLE_BINARY_THRESHOLD = 6,
        HOLE_CONTOUR_AREA_MIN = 300,
        HOLE_CONTOUR_AREA_MAX = 1500,
        CASING_DIAMETER_SPEC = 100,
        HOLE_DIAMETER_SPEC = 8.2,
        HOLE_DIAMETER_TOLERANCE = 0.5,
        LOGGING_NAME = "Bottom Casing"
    ),
    SMALL_GEAR = SimpleNamespace(
        MASTER_LOCATION = (910,1120,1745,1950),
        MASTER_BINARY_THRESHOLD = 80,
        AREA_MIN = 10000,
        AREA_MAX = 15000,
        TEETH_COUNT = 14,
        LOGGING_NAME = "Small Gear"
    ),
    LARGE_GEAR = SimpleNamespace(
        MASTER_LOCATION = (80,440,1650,2020),
        MASTER_BINARY_THRESHOLD = 100,
        AREA_MIN = 40000,
        AREA_MAX = 60000,
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
        self.passing_parts = {
            Components.TOP_CASING.LOGGING_NAME: 0,
            Components.BOTTOM_CASING.LOGGING_NAME: 0,
            Components.SMALL_GEAR.LOGGING_NAME: 0,
            Components.LARGE_GEAR.LOGGING_NAME: 0
        }
        self.status = {
            "code": 99,
            "message": "Inspection incomplete"
        }
        self.status_conditions = {
            "[1, 1, 1, 1]": [0, "All components passed"],
            "[1, 1, 1, 0]": [1, "Large gear failed"],
            "[1, 1, 0, 1]": [2, "Small gear failed"],
            "[1, 1, 0, 0]": [3, "Small gear and large gear failed"],
            "[1, 0, 1, 1]": [4, "Bottom casing failed"],
            "[1, 0, 1, 0]": [5, "Bottom casing and large gear failed"],
            "[1, 0, 0, 1]": [6, "Bottom casing and small gear failed"],
            "[1, 0, 0, 0]": [7, "Bottom casing, small gear and large gear failed"],
            "[0, 1, 1, 1]": [8, "Top casing failed"],
            "[0, 1, 1, 0]": [9, "Top casing and large gear failed"],
            "[0, 1, 0, 1]": [10, "Top casing and small gear failed"],
            "[0, 1, 0, 0]": [11, "Top casing, small gear and large gear failed"],
            "[0, 0, 1, 1]": [12, "Top casing and bottom casing failed"],
            "[0, 0, 1, 0]": [13, "Top casing, bottom casing and large gear failed"],
            "[0, 0, 0, 1]": [14, "Top casing, bottom casing and small gear failed"],
            "[0, 0, 0, 0]": [15, "All components failed"],
        }
        self.pool = ThreadPool(4)

    def inspectComponent(self, component):
        component.inspect(self.image)

    def inspect(self, image):
        self.image = image
        self.refresh()
        try:
            self.pool.map(func=self.inspectComponent, iterable=self.components.values())
            self.validate()
            self.getStatus()
            self.report()
        except:
            print('FATAL INSPECTION ERROR')

    def validate(self):
        for component in self.components:
            if self.components[component].status["code"] == 0:
                self.passing_parts[component] = 1

    def getStatus(self):
        self.status["code"] = self.status_conditions[str(list(self.passing_parts.values()))][0]
        self.status["message"] = self.status_conditions[str(list(self.passing_parts.values()))][1]

    def report(self):
        for component in self.components.values():
            if component.status["code"] == 0:
                print("\033[95m" + component.metadata.LOGGING_NAME + ": " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m" + "\033[0m" + f" (Code {component.status['code']})")
            else:
                print("\033[95m" + component.metadata.LOGGING_NAME + ": " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m" + f" (Code {component.status['code']})")
        
        if self.status["code"] == 0:
            print("\033[95m" + "Gearbox" + ": " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m" + f" (Code {self.status['code']})")
        else:
            print("\033[95m" + 'Gearbox:' + ": " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m" + "\033[0m" + f" (Code {self.status['code']})")

    def refresh(self):
        self.passing_parts = {
            Components.TOP_CASING.LOGGING_NAME: 0,
            Components.BOTTOM_CASING.LOGGING_NAME: 0,
            Components.SMALL_GEAR.LOGGING_NAME: 0,
            Components.LARGE_GEAR.LOGGING_NAME: 0
        }
        self.status = {
            "code": 99,
            "message": "Inspection incomplete"
        }