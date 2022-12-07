from ..helpers.hardware import AutomationHat
from ..inspection.inspect_gearbox import InspectionProcedure
import time

def plcInterface():
    inspection_procedure = InspectionProcedure()
    AutomationHat.busyOff()
    print("Busy is OFF")
    counter = 0
    while True:
        if AutomationHat.getTriggerSignal() == 1:
            print("Trigger is ON")
            inspectionBranch(inspection_procedure)
        elif AutomationHat.getReplenishSignal() == 1:
            print("Replenish Trigger is ON")
            replenishBranch(inspection_procedure)
    
def inspectionBranch(inspection_procedure):
    AutomationHat.busyOn()
    print("Busy is ON")
    while True:
        if AutomationHat.getTriggerSignal() == 0:
            print("Trigger is OFF")
            break
    inspection_procedure.takePicture()
    print("Picture taken")
    result = inspection_procedure.inspect()
    print("Inspection complete")
    AutomationHat.flipPassing(result)
    print("Results sent")
    AutomationHat.busyOff()
    print("Busy is OFF")
    inspection_procedure.upload()

def replenishBranch(inspection_procedure):
    print("Replenishing parts in buffer")
    # AutomationHat.busyOn()           
    # while True:
    #     if AutomationHat.getReplenishSignal() == 0:
    #         print("Replenish is OFF")
    #         break

plcInterface()