import os,sys
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
        
        dcM = dcMotor.DCMotor(Constants.GPIO_PIN_DC_1,Constants.GPIO_PIN_DC_2,Constants.GPIO_PIN_DC_PWM,200,15)
        hcsr04 = DistSensor.HCSR04(Constants.GPIO_PIN_DIST_SENSOR_TRIG,Constants.GPIO_PIN_DIST_SENSOR_ECHO)
        stepM = stepMotor.MB11_stepper(gBottom=Constants.GPIO_PIN_STEP_1,
                                yBottom=Constants.GPIO_PIN_STEP_2,
                                gTop=Constants.GPIO_PIN_STEP_3,
                                yTop=Constants.GPIO_PIN_STEP_4)
        
        
        #netThread = NM.NetworkThread("138.197.121.142",5669,"95",useGPRS=False)
        netThread = NM.NetworkThread("192.168.1.29",5669,"95",useGPRS=False)
        #netThread.setDaemon(True)
        netThread.start()
        
        while True:
            """
            dist = hcsr04.readDistance()
            print("Dist",dist,"cm")
            if dist < 20:
                print("DCM")
                dcM.turnLeft()
                time.sleep(5)
            elif dist < 30:
                print("StepM")
                stepM.turnLeft()
            else:
                dcM.stop()
            """
            time.sleep(5)
            
            
            
            
            
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
