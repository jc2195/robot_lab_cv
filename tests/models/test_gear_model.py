# import pytest
# import cv2
# from ...src.models.gear_model import Gear
# from ...src.models.gearbox_model import Components

# class TestStatusRetrievalSmallGear:

#     def test_status_99(self):
#         small_gear = Gear(Components.SMALL_GEAR)
#         image =  cv2.imread("blank_1.jpg", cv2.IMREAD_GRAYSCALE)
#         small_gear.inspect(image)
#         assert small_gear.status["code"] == 99
#         assert small_gear.status["message"] == "Inspection incomplete"

#     def test_status_0(self):
#         small_gear = Gear(Components.SMALL_GEAR)
#         image =  cv2.imread("all_pass_1.jpg", cv2.IMREAD_GRAYSCALE)
#         small_gear.inspect(image)
#         small_gear.getStatus()
#         assert small_gear.status["code"] == 0
#         assert small_gear.status["message"] == "Pass"

#     def test_status_1(self):
#         small_gear = Gear(Components.SMALL_GEAR)
#         image =  cv2.imread("blank_1.jpg", cv2.IMREAD_GRAYSCALE)
#         small_gear.inspect(image)
#         small_gear.getStatus()
#         assert small_gear.status["code"] == 1
#         assert small_gear.status["message"] == "Worn gear"

#     def test_status_2(self):
#         small_gear = Gear('tests/images/raw/set1x.jpg', Components.SMALL_GEAR)
#         small_gear.teeth = 12
#         small_gear.getStatus()
#         assert small_gear.status["code"] == 2
#         assert small_gear.status["message"] == "Missing teeth"

# class TestStatusRetrievalLargeGear:

#     def test_status_99(self):
#         large_gear = Gear('tests/images/raw/set1x.jpg', Components.LARGE_GEAR)
#         assert large_gear.status["code"] == 99
#         assert large_gear.status["message"] == "Inspection incomplete"

#     def test_status_0(self):
#         large_gear = Gear('tests/images/raw/set1x.jpg', Components.LARGE_GEAR)
#         large_gear.teeth = Components.LARGE_GEAR.TEETH_COUNT
#         large_gear.getStatus()
#         assert large_gear.status["code"] == 0
#         assert large_gear.status["message"] == "Pass"

#     def test_status_1(self):
#         large_gear = Gear('tests/images/raw/set1x.jpg', Components.LARGE_GEAR)
#         large_gear.teeth = 1
#         large_gear.getStatus()
#         assert large_gear.status["code"] == 1
#         assert large_gear.status["message"] == "Worn gear"

#     def test_status_2(self):
#         large_gear = Gear('tests/images/raw/set1x.jpg', Components.LARGE_GEAR)
#         large_gear.teeth = 12
#         large_gear.getStatus()
#         assert large_gear.status["code"] == 2
#         assert large_gear.status["message"] == "Missing teeth"