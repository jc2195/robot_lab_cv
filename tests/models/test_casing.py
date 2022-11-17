# import pytest
# from ...src.models.casing_model import Casing
# from ...src.models.gearbox_model import Components

# class TestStatusRetrievalTopCasing:

#     def test_status_99(self):
#         casing = Casing('tests/images/raw/set1x.jpg', Components.TOP_CASING)
#         assert casing.status["code"] == 99
#         assert casing.status["message"] == "Inspection incomplete"

#     def test_status_0(self):
#         casing = Gear('tests/images/raw/set1x.jpg', Components.TOP_CASING)
#         small_gear.teeth = Components.SMALL_GEAR.TEETH_COUNT
#         small_gear.getStatus()
#         assert small_gear.status["code"] == 0
#         assert small_gear.status["message"] == "Pass"

#     def test_status_1(self):
#         small_gear = Gear('tests/images/raw/set1x.jpg', Components.SMALL_GEAR)
#         small_gear.teeth = 1
#         small_gear.getStatus()
#         assert small_gear.status["code"] == 1
#         assert small_gear.status["message"] == "Worn gear"

#     def test_status_2(self):
#         small_gear = Gear('tests/images/raw/set1x.jpg', Components.SMALL_GEAR)
#         small_gear.teeth = 12
#         small_gear.getStatus()
#         assert small_gear.status["code"] == 2
#         assert small_gear.status["message"] == "Missing teeth"

#     def getHoleDiameters(self):
#         for hole in self.hole_diameters:
#             outer_contour = Contours.getContourByArea(self.left_hole_image, self.metadata.HOLE_CONTOUR_AREA_MIN, self.metadata.HOLE_CONTOUR_AREA_MAX)
#             centre, hole_radius = cv2.minEnclosingCircle(outer_contour)
#             self.hole_diameters[hole] = hole_radius * 2 * self.mm_per_pixel

#     def getStatus(self):
#         minSpec = self.metadata.HOLE_DIAMETER_SPEC - self.metadata.HOLE_DIAMETER_TOLERANCE
#         maxSpec = self.metadata.HOLE_DIAMETER_SPEC + self.metadata.HOLE_DIAMETER_TOLERANCE

#         if (minSpec < self.hole_diameters["left"] < maxSpec) and (minSpec < self.hole_diameters["right"] < maxSpec):
#             self.status["code"] = 0
#             self.status["message"] = "Pass"
#         elif (maxSpec < self.hole_diameters["left"]) and (minSpec < self.hole_diameters["right"] < maxSpec):
#             self.status["code"] = 1
#             self.status["message"] = "Left hole diameter too large"
#         elif (minSpec < self.hole_diameters["left"] < maxSpec) and (maxSpec < self.hole_diameters["right"]):
#             self.status["code"] = 2
#             self.status["message"] = "Right hole diameter too large"
#         elif (maxSpec < self.hole_diameters["left"]) and (maxSpec < self.hole_diameters["right"]):
#             self.status["code"] = 3
#             self.status["message"] = "Both hole diameters too large"
#         elif (minSpec > self.hole_diameters["left"]) and (minSpec < self.hole_diameters["right"] < maxSpec):
#             self.status["code"] = 4
#             self.status["message"] = "Left hole diameter too small"
#         elif (minSpec < self.hole_diameters["left"] < maxSpec) and (minSpec > self.hole_diameters["right"]):
#             self.status["code"] = 5
#             self.status["message"] = "Right hole diameter too small"
#         elif (minSpec > self.hole_diameters["left"]) and (minSpec > self.hole_diameters["right"]):
#             self.status["code"] = 6
#             self.status["message"] = "Both hole diameters too small"
#         elif (minSpec > self.hole_diameters["left"]) and (maxSpec < self.hole_diameters["right"]):
#             self.status["code"] = 7
#             self.status["message"] = "Left hole diameter too small, right hole diameter too large"
#         elif (maxSpec < self.hole_diameters["left"]) and (minSpec > self.hole_diameters["right"]):
#             self.status["code"] = 8
#             self.status["message"] = "Left hole diameter too large, right hole diameter too small"