import RPi.GPIO as GPIO
import time, os, sys

RPi_SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(RPi_SRC_PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")
import Constants


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = Constants.GPIO_PIN_DIST_SENSOR_TRIG
ECHO = COnstants.GPIO_PIN_DIST_SENSOR_ECHO

print ("HC-SR04 mesafe sensoru")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

while True:

    GPIO.output(TRIG, False)
    print ("Olculuyor...")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance > 2 and distance < 400:
        print("Mesafe",distance - 0.5,"cm")
    else:
        print ("Menzil asildi")
