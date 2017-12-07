import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21,GPIO.IN)


def motionSensor():
	if GPIO.input(21):
		print("Motion Detected")
	else:
		print("No motion")

#GPIO.add_event_detect(21,GPIO.BOTH,callback=motionSensor,bouncetime=150)


if __name__=="__main__":
	while True:
		motionSensor()
		time.sleep(0.1)
