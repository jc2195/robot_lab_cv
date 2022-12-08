from ..helpers.hardware import AutomationHat
from ..inspection.inspect_gearbox import InspectionProcedure
import time

def plcInterface():
    inspection_procedure = InspectionProcedure()
    AutomationHat.busyOff()
    print("Busy is OFF")
    while True:
        if AutomationHat.getTriggerSignal() == 1:
            print("Trigger is ON")
            inspectionBranch(inspection_procedure)
        elif AutomationHat.getReplenishTriggerSignal() == 1:
            print("Replenish trigger is ON")
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
    for part_key in ["Top Casing", "Bottom Casing", "Small Gear", "Large Gear"]:
        AutomationHat.replenishAcknowledgeOn()
        print("Replenish acknowledge is ON")
        while True:
            if AutomationHat.getReplenishTriggerSignal == 0:
                print("Replenish trigger is OFF")
                break
        AutomationHat.flipReplenish(inspection_procedure.result_cache[part_key])
        print("Replenish results sent")
        AutomationHat.replenishAcknowledgeOff()
        print("Replenish acknowledge is OFF")
        while True:
            if AutomationHat.getReplenishTriggerSignal == 1:
                print("Replenish trigger is ON")
                break
    AutomationHat.replenishAcknowledgeOn()
    print("Replenish acknowledge is ON")
    while True:
        if AutomationHat.getReplenishTriggerSignal == 0:
            print("Replenish trigger is OFF")
            break
    AutomationHat.replenishAcknowledgeOff()
    print("Replenish acknowledge is OFF")

plcInterface()