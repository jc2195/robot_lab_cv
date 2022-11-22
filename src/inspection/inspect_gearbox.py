from ..models.gearbox_model import Gearbox
from ..helpers.hardware import Camera
import cv2

class InspectionProcedure:
    def __init__(self):
        self.gearbox = Gearbox()
        self.camera = Camera()

    def inspect(self):
        self.camera.takePicture()
        self.gearbox.inspect(self.camera.image_trimmed)
        return self.retrieveValidationVector(self.gearbox.passing_parts)

    def retrieveValidationVector(self, report):
        output = []
        output.append(report["Top Casing"])
        output.append(report["Bottom Casing"])
        output.append(report["Small Gear"])
        output.append(report["Large Gear"])
        return output