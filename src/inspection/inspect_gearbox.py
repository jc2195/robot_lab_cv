from ..models.gearbox_model import Gearbox
# from ..helpers.hardware import PiCamera

class InspectionProcedure:
    def __init__(self):
        self.filename = "images/live/0.jpg"
        self.gearbox = Gearbox()

    def inspect(self):
        # PiCamera.takePicture()
        self.gearbox.inspect(self.filename)
        return self.retrieveValidationVector(self.gearbox.passing_parts)

    def retrieveValidationVector(self, report):
        output = []
        output.append(report["Top Casing"])
        output.append(report["Bottom Casing"])
        output.append(report["Small Gear"])
        output.append(report["Large Gear"])
        return output

    def mockInspection(self):
        self.gearbox.inspect(self.filename)
        return self.retrieveValidationVector(self.gearbox.passing_parts)


inspection_procedure = InspectionProcedure()
total = 0
for i in range(10):
    inspection_procedure.mockInspection()
    total += inspection_procedure.gearbox.inspection_time
print(total/10)