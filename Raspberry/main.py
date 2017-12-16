import os,sys
from modules import NetworkThread as NT

PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")

import Constants

def main():

    netThread = None
    try:
        netThread = NT.NetworkThread("127.0.0.1",5669,"95")
        #netThread.setDaemon(True)
        netThread.start()

        while not netThread.threadDone:
            pass

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