from picamera import PiCamera
import time

class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640,480)
        self.camera.framerate = 10
        #self.rawCapture = PiRGBArray(self.camera,size=self.camera.resolution())
        
    def getFrame(self):
        photoName = None
        try:
            time.sleep(2)
            photoName = time.strftime("%Y-%m-%d_%H.%M.%S",time.gmtime())+".jpg"
            self.camera.capture(photoName)
        except Exception as e:
            print("GetFrameException:",str(e))
            photoName = None
            
        return photoName

if __name__=="__main__":
    cam = Camera()
    print("Photo:",cam.getFrame(),"saved.")
