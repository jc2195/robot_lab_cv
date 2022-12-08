from ..helpers.hardware import AutomationHat
from ..helpers.display import Viewer
from ..inspection.inspect_gearbox import InspectionProcedure
from multiprocessing.pool import Pool
import time

def runPool(items):
    viewer = Viewer()
    viewer.show()

def plcInterface():
    pool = Pool(1)
    result = pool.map_async(func=runPool, iterable=[])
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
    AutomationHat.replenishAcknowledgeOn()
    print("Replenish acknowledge is ON")
    while True:
        if AutomationHat.getTriggerSignal() == 1:
            print("Trigger is ON")
    AutomationHat.replenishAcknowledgeOff()
    print("Replenish acknowledge is OFF")
    for part_key in ["Top Casing", "Bottom Casing", "Small Gear", "Large Gear"]:
        while True:
            if AutomationHat.getTriggerSignal == 0:
                print("Trigger is OFF")
                break
        AutomationHat.replenishAcknowledgeOn()
        print("Replenish acknowledge is ON")
        while True:
            if AutomationHat.getTriggerSignal == 1:
                print("Trigger is ON")
                break
        AutomationHat.flipReplenish(inspection_procedure.result_cache[part_key])
        AutomationHat.replenishAcknowledgeOff()
        print("Replenish acknowledge is OFF")
    while True:
        if AutomationHat.getTriggerSignal == 0:
            print("Trigger is OFF")
            break
    while True:
        if AutomationHat.getReplenishTriggerSignal == 0:
            print("Replenish trigger is OFF")
            break

plcInterface()