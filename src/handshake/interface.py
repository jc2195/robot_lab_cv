from ..helpers.hardware import AutomationHat
from ..inspection.inspect_gearbox import InspectionProcedure
import time

def plcInterface():
    inspection_procedure = InspectionProcedure()
    AutomationHat.busyOff()
    print("Busy is OFF")
    while True:
        while True:
            if AutomationHat.getTriggerSignal() == 1:
                print("Trigger is ON")
                break
        AutomationHat.busyOn()
        print("Busy is ON")
        result = inspection_procedure.inspect()
        AutomationHat.flipPassing(result)
        print("Results sent")
        AutomationHat.busyOff()
        print("Busy is OFF")
        while True:
            if AutomationHat.getTriggerSignal() == 0:
                print("Trigger is OFF")
                break
        time.sleep(1)

plcInterface()