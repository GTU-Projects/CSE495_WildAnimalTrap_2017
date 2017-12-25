import RPi.GPIO as GPIO
import time, os, sys
import Constants

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class HCSR04():
    def __init__(self,TRIG_PIN,ECHO_PIN):
        self.ECHO_PIN=ECHO_PIN
        self.TRIG_PIN=TRIG_PIN
        
        GPIO.setup(self.TRIG_PIN,GPIO.OUT)
        GPIO.setup(self.ECHO_PIN,GPIO.IN)

    def readDistance(self):
        # trigger to measure distance
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.5)
        # trigger again
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)

        # find time difference between signals
        while GPIO.input(self.ECHO_PIN)==0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO_PIN)==1:
            pulse_end = time.time()

        # calculate distance(values was taken from internet)
        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if distance > 2 and distance < 400:
            return distance - 0.5
        else:
            return -1

def testDistanceSensor():
    hcsr04 = HCSR04(Constants.GPIO_PIN_DIST_SENSOR_TRIG,Constants.GPIO_PIN_DIST_SENSOR_ECHO)
    while True:
        dist = hcsr04.readDistance()
        print("Distance:",dist,"cm")
        time.sleep(1)
