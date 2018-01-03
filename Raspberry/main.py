import os, sys
import time
from modules import NetworkManager as NM
from modules import dcMotor
from modules import DistSensor
from modules import stepMotor

PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")

import Constants







def main():

    netThread = None
    try:

        dcM = dcMotor.DCMotor(Constants.GPIO_PIN_DC_1,Constants.GPIO_PIN_DC_2,Constants.GPIO_PIN_DC_PWM,200,25)
        hcsr04 = DistSensor.HCSR04(Constants.GPIO_PIN_DIST_SENSOR_TRIG,Constants.GPIO_PIN_DIST_SENSOR_ECHO)
        stepM = stepMotor.MB11_stepper(gBottom=Constants.GPIO_PIN_STEP_1,
                                yBottom=Constants.GPIO_PIN_STEP_2,
                                gTop=Constants.GPIO_PIN_STEP_3,
                                yTop=Constants.GPIO_PIN_STEP_4)
        #netThread = NM.NetworkThread("138.197.121.142",5669,"95",useGPRS=False)
        netThread = NM.NetworkThread("192.168.1.29",5669,"95",useGPRS=False)
        #netThread.setDaemon(True)
        netThread.start()
        maxDoor=5
        maxBait=10
        while True:

            if netThread.doorCount==0 and netThread.openDoorCome:
                while netThread.doorCount!=maxDoor:
                    netThread.doorCount = netThread.doorCount+1
                    dcM.turnRight()
                    print("Door is opening")
                    time.sleep(1)
                dcM.stop()
                while netThread.baitCount!=maxBait:
                    netThread.baitCount=netThread.baitCount+1
                    stepM.turnRight()
                    print("Bait is pushed")
                    time.sleep(1)
                time.sleep(5)
                print("Waiting to animal go out")
                netThread.openDoorCome=0

            if netThread.doorCount==0:
                print("DOORLOCKED")
                dcM.stop()
                time.sleep(1)
                continue

            dist = hcsr04.readDistance()
            print("Dist",dist,"cm")
            if dist < 10 and netThread.baitCount==0:
                if netThread.doorCount!=0:
                    netThread.doorCount=netThread.doorCount-1
                    dcM.turnLeft()
                    print("Close Door:",netThread.doorCount)
            elif dist < 30:
                if netThread.baitCount!=0:
                    netThread.baitCount = netThread.baitCount-1
                    stepM.turnLeft()
                    print("Pull bait:",netThread.baitCount)
            else:
                if netThread.doorCount != 5:
                    netThread.doorCount = netThread.doorCount+1
                    dcM.turnRight()
                    print("Open Door:",netThread.doorCount)
                if(netThread.baitCount != 10):
                    netThread.baitCount = netThread.baitCount+1
                    stepM.turnRight()
                    print("Push Bait:",netThread.baitCount)
                dcM.stop()
            time.sleep(1)


    except Exception as e:
        print("NetworkThread: main: exception: ",str(e))
    except KeyboardInterrupt:
        print("!!! Ctrl + C !!!")
    finally:
        if netThread:
            netThread.stop()
            netThread.join()

if __name__=="__main__":
    main()
