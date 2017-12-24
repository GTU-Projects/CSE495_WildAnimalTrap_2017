import threading
import time
from SocketInterface import SocketInterface
import os,sys
import GPRS_GSM
import string

RPi_SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(RPi_SRC_PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")
import Constants


class NetworkThread(threading.Thread):
    def __init__(self,ip="138.197.121.142",port="5669",serial=95, useGPRS=False, initAll=False):
        threading.Thread.__init__(self)

        # serial number for authentication of server-trap connection
        self.serial = str(serial)

        self.threadDone = False
        self.isConnected = False
        self.ip=ip
        self.port=port
        self.isInitialized = False # to initialize gsm modelu just one time
        
        if useGPRS:
            self.comInt = GPRS_GSM.GPRS_GSM("/dev/ttyAMA0",19200,1.0)
            self.comInt.initHWModule()
            
        print("NetworkThread initialized.")
        
    def run(self):
        try:
            while not self.threadDone:
                # TODO: Change this logic with better one
                # if there is no connection try to connect every 5 sec
                while not self.threadDone and not self.isInitialized:
                    if not self.isInitialized:
                        if self.comInt.initNetworkCfg():
                            self.comInt.openTCPSocket(self.ip,self.port)
                    self.isInitialized=True
                print("NT Connected to socket")

                # send serial number to thread
                while not self.threadDone and not self.isConnected:
                    self.comInt.send2Socket(self.serial.encode())
                    print("Waiting for server result")
                    resp = self.comInt.readLineFromSocket()
                    if resp:
                        resp = int(resp)
                    if resp ==Constants.SUCCESS:
                        print("Connection established")
                        self.isConnected=True
                    else:
                        print("SerialAuthentication Failed. Try 5 seconds later.")
                        time.sleep(2)

                while not self.threadDone and self.isConnected:
                    cmd = self.sockInt.readSocket(2)
                    if cmd:
                        cmd = int(cmd)
                        if cmd==Constants.REQ_TAKE_PHOTO:
                            photo = getPhoto()
                            print("Photo on sending queue")
                            self.sockInt.send2Socket(photo)
                            print("Photo send")
                        elif cmd==Constants.REQ_CLOSE_DOOR:
                            print("CloseDoor")
                            self.sockInt.send2Socket(b'0')
                        elif cmd==Constants.REQ_OPEN_DOOR:
                            print("OpenDoor")
                            self.sockInt.send2Socket(b'1')

        except Exception as e:
            print("NetworkThread: run: exception: ",str(e))
        except KeyboardInterrupt:
            print("here")
        finally:
            self.threadDone=True
        print("Thread done")

    def stop(self):
        self.threadDone = True


def getPhoto(path=RPi_SRC_PATH+"/wolf.jpg"):
    photo=None
    try:
        with open(path,"rb") as f:
            photo = f.read()
    except Exception as e:
        print("GetPhotoError")
        photo=None
    return photo

if __name__=="__main__":

    netThread = None
    try:
        netThread = NetworkThread("127.0.0.1",5669,"95",useGPRS=True)
        netThread.setDaemon(True)
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
