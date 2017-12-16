import threading
import time
from SocketInterface import SocketInterface
import Constants

class NetworkThread(threading.Thread):
    def __init__(self,ip="138.197.121.142",port="5669",serial=95, useGPRS=False):
        threading.Thread.__init__(self)

        self.sockInt = SocketInterface(ip,port)

        # serial number for authentication of server-trap connection
        self.serial = str(serial)

        self.threadDone = False
        self.isConnected = False

    def run(self):
        try:
            while not self.threadDone:
                # if there is no connection try to connect every 5 sec
                while not self.threadDone and not self.sockInt.isConnected:
                    self.sockInt.connect()
                    time.sleep(1)

                # send serial number to thread
                while not self.threadDone and not self.isConnected:
                    self.sockInt.send2Socket(self.serial.encode())
                    resp = self.sockInt.receiveFromSocket()
                    if resp ==b'A':
                        print("Connection established")
                        self.isConnected=True
                    else:
                        print("SerialAuthentication Failed. Try 5 seconds later.")
                        time.sleep(5)

                while not self.threadDone and self.sockInt.isConnected:
                    cmd = self.sockInt.receiveFromSocket()
                    if cmd:
                        cmd = int(cmd)
                        if cmd==Constants.REQ_TAKE_PHOTO:
                            photo = getPhoto()
                            self.sockInt.send2Socket(photo)
                        elif cmd==Constants.REQ_CLOSE_DOOR:
                            print("CloseDoor")
                        elif cmd==Constants.REQ_OPEN_DOOR:
                            print("ThakePhoto")

        except Exception as e:
            print("NetworkThread: run: exception: ",str(e))
        except KeyboardInterrupt:
            print("here")
        finally:
            self.threadDone=True
        print("Thread done")

    def stop(self):
        self.threadDone = True

import os
path = os.path.dirname(os.path.abspath(__file__))
def getPhoto(path=path+"/wolf.jpg"):
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
        netThread = NetworkThread("127.0.0.1",5669,"95")
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
