from ..helpers.hardware import AutomationHat
from ..inspection.inspect_gearbox import InspectionProcedure
import time

def plcInterface():
    inspection_procedure = InspectionProcedure()
    inspectionMode = False
    AutomationHat.busyOff()
    print("Busy is OFF")
    runningTotal = [0, 0, 0, 0]
    while True:
        while True:
            inspectionMode = False
            if AutomationHat.getTriggerSignal() == 1:
                print("Trigger is ON")
                inspectionMode = True
                break
            elif AutomationHat.getReplenishSignal() == 1:
                print("Replenish Trigger is ON")
                break
        if inspectionMode == True:
            AutomationHat.busyOn()
            print("Busy is ON")
            while True:
                if AutomationHat.getTriggerSignal() == 0:
                    print("Trigger is OFF")
                    break
            inspection_procedure.takePicture()
            result = inspection_procedure.inspect()
            runningTotal[0] = runningTotal[0] + 1 - result[0]
            runningTotal[1] = runningTotal[1] + 1 - result[1]
            runningTotal[2] = runningTotal[2] + 1 - result[2]
            runningTotal[3] = runningTotal[3] + 1 - result[3]
            AutomationHat.flipPassing(result)
            print("Results sent")
            AutomationHat.busyOff()
            print("Busy is OFF")
            inspection_procedure.upload()
        else:
            print("Replenishing parts in buffer")
            AutomationHat.busyOn()           
            while True:
                if AutomationHat.getReplenishSignal() == 0:
                    print("Replenish is OFF")
                    runningTotal = [0, 0, 0, 0]
                    break
    
                


plcInterface()