from picamera import PiCamera
import time

class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640,480)
        self.camera.framerate = 10
        #self.rawCapture = PiRGBArray(self.camera,size=self.camera.resolution())
        
    def getFrame(self):
        time.sleep(3)
        print("11")
        self.camera.capture("p.jpg")
        time.sleep(3)
        print("22")
        self.camera.capture("p1.jpg")


if __name__=="__main__":
    cam = Camera()
    cam.getFrame()
