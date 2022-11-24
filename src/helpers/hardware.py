from picamera import PiCamera
import automationhat
import numpy as np

class AutomationHat:
    def getTriggerSignal():
        return automationhat.input.one.read()

    def busyOn():
        automationhat.output.one.write(0)

    def busyOff():
        automationhat.output.one.write(1)

    def flipPassing(results):
        automationhat.output.two.write(results[0])
        automationhat.output.three.write(results[1])
        automationhat.relay.one.write(results[2])
        automationhat.relay.two.write(results[3])

class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (3200, 2400)
        self.image = np.empty((2400, 3200), dtype=np.uint8)
        self.image_trimmed = np.empty((1760, 2350), dtype=np.uint8)

    def takePicture(self):
        try:
            self.camera.capture(self.image, "yuv")
            print("Picture Taken")
            print("\n")
        except IOError:
            pass
        self.image_trimmed = self.image[0:2350, 0:1760]