import RPi.GPIO as GPIO
import time
import sys,os

RPi_SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(RPi_SRC_PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")
import Constants


GPIO.setmode(GPIO.BCM)

GPIO.setup(Constants.GPIO_PIN_MOTION_SENSOR,GPIO.IN)



def motionSensor():
    if GPIO.input(Constants.GPIO_PIN_MOTION_SENSOR):
        print("Motion Detected")
    else:
        print("No motion")

#GPIO.add_event_detect(21,GPIO.BOTH,callback=motionSensor,bouncetime=150)


if __name__=="__main__":
    while True:
        motionSensor()
        time.sleep(1)
