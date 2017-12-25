from darknetpy.detector import Detector

def loadDetector():
    return Detector('/opt/darknet',
                    '/opt/darknet/cfg/coco.data',
                    '/opt/darknet/cfg/yolo.cfg',
                    '/opt/darknet/yolo.weights')

def detectPhoto(detector,photoPath):
    return detector.detect(photoPath)


if __name__=="__main__":
    detector = loadDetector()

    photoPath = "/opt/darknet/data/wolf.jpg"
    res = detectPhoto(detector,photoPath)
    print(res)
