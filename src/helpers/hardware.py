import automationhat
import picamera

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

class PiCamera:
    def takePicture():
        camera = picamera.PiCamera()
        camera.resolution = (3200, 2400)
        camera.capture("images/live/0.jpg")
        camera.close()