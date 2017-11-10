import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class DCmotor():
    def __init__(self, pin1, pin2):
        self.pin1=pin1
        self.pin2=pin2

        GPIO.setup(self.pin1,GPIO.OUT)
        GPIO.setup(self.pin2,GPIO.OUT)

    def turnLeft(self):
        GPIO.output(self.pin1,1)
        GPIO.output(self.pin2,0)

    def turnRight(self):
        GPIO.output(self.pin1,0)
        GPIO.output(self.pin2,1)

    def stop(self):
        GPIO.output(self.pin1,0)
        GPIO.output(self.pin2,0)

    def turnLeftWithPWM(self,risingTime,follingTime):
        GPIO.output(self.pin1,1)
        GPIO.output(self.pin2,0)
        time.sleep(risingTime)
        GPIO.output(self.pin1,0)
        time.sleep(follingTime)

    def turnRightWithPWM(self,risingTime,follingTime):
        GPIO.output(self.pin1,0)
        GPIO.output(self.pin2,1)
        time.sleep(risingTime)
        GPIO.output(self.pin2,0)
        time.sleep(follingTime)

    def _test(self):
        print("Starting DC motor tests")
        print("Will turn 5 times right and left and each turn will take 2 sec")

        for i in range(0,5):
            self.turnLeft()
            time.sleep(2)
            self.turnRight()
            time.sleep(2)
        self.stop()

    def _testPWM(self):
        for i in range(0,10):
            self.turnLeftWithPWM(0.05,0.2)
        for i in range(0,10):
            self.turnRightWithPWM(0.05,0.2)

        self.stop()
        print("DC motor tests done. Did you see movements?")

def dcMotorModuleTest():
    dcMotor = DCmotor(20,21)
    print("FirstTest")
    dcMotor._test()
    time.sleep(1)
    print("SecondTest")
    dcMotor._testPWM()

if __name__=="__main__":
    dcMotorModuleTest()
