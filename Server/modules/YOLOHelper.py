import sys,os
from darknetpy.detector import Detector

CURRENTDIRPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,CURRENTDIRPATH)

def loadDetector():
    return Detector('/opt/darknet',
                    '/opt/darknet/cfg/coco.data',
                    '/opt/darknet/cfg/yolo.cfg',
                    '/opt/darknet/yolo.weights')

def detectPhoto(detector,photoPath):
    return detector.detect(photoPath)


if __name__=="__main__":
    detector = loadDetector()

    photoPath =CURRENTDIRPATH+"/wolf.jpg"
    res = detectPhoto(detector,photoPath)
    print(res)
