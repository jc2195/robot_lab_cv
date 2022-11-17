from ..helpers.hardware import AutomationHat
from ..inspection.inspect_gearbox import InspectionProcedure

def plc_interface():
    while True:
        while True:
            if AutomationHat.getTriggerSignal() == 1:
                break
        AutomationHat.busyOn()
        inspection_procedure = InspectionProcedure()
        result = inspection_procedure.inspect()
        AutomationHat.flipPassing(result)
        AutomationHat.busyOff()