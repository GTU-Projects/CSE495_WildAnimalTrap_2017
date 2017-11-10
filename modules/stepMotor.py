import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class MB11_stepper():
    def __init__(self,gBottom,yBottom,gTop,yTop):
        """ Give Philips MB11 Step motor wires connected pins.
            g Means Gray pin
            y Means Yellow pin
        """
        self.gBottom=gBottom
        self.yBottom=yBottom
        self.gTop=gTop
        self.yTop=yTop

        # set pins to output mode
        GPIO.setup(self.gBottom,GPIO.OUT)
        GPIO.setup(self.yBottom,GPIO.OUT)
        GPIO.setup(self.gTop,GPIO.OUT)
        GPIO.setup(self.yTop,GPIO.OUT)

        self.setStepDelay() # set step delay because logic faster than mechanic

    def setStepDelay(self,stepDelay=0.05):
        """ Set delay time to wait until step motor act to next movement
        """
        self.stepDelay=stepDelay

    def turnLeft(self):
        """ Turn motor 1 complete step to left
        """
        GPIO.output(self.gBottom,1)
        GPIO.output(self.yBottom,0)
        GPIO.output(self.gTop,0)
        GPIO.output(self.yTop,0)
        time.sleep(self.stepDelay)

        GPIO.output(self.gBottom,0)
        GPIO.output(self.yBottom,0)
        GPIO.output(self.gTop,1)
        GPIO.output(self.yTop,0)
        time.sleep(self.stepDelay)

        GPIO.output(self.gBottom,0)
        GPIO.output(self.yBottom,1)
        GPIO.output(self.gTop,0)
        GPIO.output(self.yTop,0)
        time.sleep(self.stepDelay)

        GPIO.output(self.gBottom,0)
        GPIO.output(self.yBottom,0)
        GPIO.output(self.gTop,0)
        GPIO.output(self.yTop,1)
        time.sleep(self.stepDelay)

    def turnRight(self):
        """ To motor 1 complete step to right
        """
        GPIO.output(self.gBottom,0)
        GPIO.output(self.yBottom,0)
        GPIO.output(self.gTop,0)
        GPIO.output(self.yTop,1)
        time.sleep(self.stepDelay)

        GPIO.output(self.gBottom,0)
        GPIO.output(self.yBottom,1)
        GPIO.output(self.gTop,0)
        GPIO.output(self.yTop,0)
        time.sleep(self.stepDelay)

        GPIO.output(self.gBottom,0)
        GPIO.output(self.yBottom,0)
        GPIO.output(self.gTop,1)
        GPIO.output(self.yTop,0)
        time.sleep(self.stepDelay)

        GPIO.output(self.gBottom,1)
        GPIO.output(self.yBottom,0)
        GPIO.output(self.gTop,0)
        GPIO.output(self.yTop,0)
        time.sleep(self.stepDelay)

    def _test(self):
        print("Starting to test step motor")
        print("Turn 5*10 complete step to left and right")
        for i in range(0,5):
            for j in range(0,10):
                self.turnRight()
            for j in range(0,10):
                self.turnLeft()
        print("Test done! Did you see movements?")


def stepMotorModuleTest():
    stepMotor = MB11_stepper(gBottom=6,yBottom=13,gTop=19,yTop=26)
    stepMotor._test()


 if __name__=="__main__":
    stepMotorModuleTest()