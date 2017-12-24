import os,sys
import time
from modules import NetworkManager as NM

PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")

import Constants

def main():

    netThread = None
    try:
        #netThread = NT.NetworkThread("127.0.0.1",5669,"95")
        netThread = NM.NetworkThread("138.197.121.142",5669,"95",useGPRS=False)
        #netThread.setDaemon(True)
        netThread.start()
        

        while not netThread.threadDone:
            time.sleep(10)
            NM.addServerPendingQue(b'123')
            
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
