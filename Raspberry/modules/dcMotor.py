import RPi.GPIO as GPIO
import time
import Constants

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class DCMotor():
    def __init__(self, pin1, pin2,pinPWM=None, pwmFreq=None,dutyCycle=None):
        self.pin1=pin1
        self.pin2=pin2
        self.dutyCycle = dutyCycle
        
        self.isPWMOpen=False

        GPIO.setup(self.pin1,GPIO.OUT)
        GPIO.setup(self.pin2,GPIO.OUT)

        if pinPWM!=None:
            self.pinPWM=pinPWM
            GPIO.setup(self.pinPWM,GPIO.OUT)
            self.pwm = GPIO.PWM(self.pinPWM,pwmFreq)

    def turnLeft(self):
        GPIO.output(self.pin1,1)
        GPIO.output(self.pin2,0)
        self.pwm.start(self.dutyCycle)
        self.isPWMOpen=True

    def turnRight(self):
        GPIO.output(self.pin1,0)
        GPIO.output(self.pin2,1)
        self.pwm.start(self.dutyCycle)
        self.isPWMOpen=True

    def stop(self):
        GPIO.output(self.pin1,0)
        GPIO.output(self.pin2,0)
        
        if self.isPWMOpen:
            GPIO.output(self.pinPWM,0)
            self.pwm.stop()
            self.isPWMOpen = False


    def turnLeftWithDelays(self,risingTime,follingTime):
        GPIO.output(self.pin1,1)
        GPIO.output(self.pin2,0)
        time.sleep(risingTime)
        GPIO.output(self.pin1,0)
        time.sleep(follingTime)

    def turnRightWithDelays(self,risingTime,follingTime):
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
            time.sleep(5)
            self.turnRight()
            time.sleep(5)
        self.stop()

    def _testTurnWithDelay(self):
        for i in range(0,10):
            self.turnLeftWithDelay(0.05,0.2)
        for i in range(0,10):
            self.turnRightWithDelay(0.05,0.2)

        self.stop()
        print("DC motor tests done. Did you see movements?")

def __moduleTest():
    dcMotor = DCMotor(Constants.GPIO_PIN_DC_1,Constants.GPIO_PIN_DC_2,Constants.GPIO_PIN_DC_PWM,200,25)
    dcMotor._test()
    
if __name__=="__main__":
    __moduleTest()
