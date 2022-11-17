from ..models.gearbox_model import Gearbox
from ..helpers.hardware import PiCamera

class InspectionProcedure:
    def __init__(self):
        self.filename = "images/live/0.jpg"
        self.gearbox = None

    def begin(self):
        PiCamera.takePicture()
        self.gearbox = Gearbox(self.filename)
        self.gearbox.inspect()
        self.gearbox.validate()
        self.gearbox.report()
        output = self.retrieveValidationVector(self.gearbox.passing_parts)
        return output

    def retrieveValidationVector(self, report):
        output = []
        output.append(report["Top Casing"])
        output.append(report["Bottom Casing"])
        output.append(report["Small Gear"])
        output.append(report["Large Gear"])
        return output