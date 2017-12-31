import threading
import time
import SocketInterface
import os,sys
import GPRS_GSM
import string
import queue
import Constants
import CameraService

tQue = queue.Queue()
rQue = queue.Queue()

class NetworkThread(threading.Thread):
    def __init__(self,ip="138.197.121.142",port=5669,serial=95, useGPRS=False):
        threading.Thread.__init__(self)

        # serial number for authentication of server-trap connection
        self.serial = str(serial)

        self.threadDone = False
        self.isConnected = False
        self.ip=ip
        self.port=port
        self.isInitialized = False # to initialize gsm modelu just one time
        
        self.cam = CameraService.Camera()

        self.comInt = SocketInterface.SocketInterface(self.ip,self.port)
        print("NetworkThread initialized.")
        
    def run(self):
        try:
            while not self.threadDone:
                # TODO: Change this logic with better one
                # if there is no connection try to connect every 5 sec
                while not self.threadDone:
                    if self.comInt.connect():
                        break
                    time.sleep(1)

                print("NT Connected to socket")

                # send serial number to thread
                while not self.threadDone and not self.isConnected:
                    self.comInt.send2Socket(self.serial.encode())
                    print("Waiting for server result")
                    resp = self.comInt.receiveFromSocket(10)
                    if resp:
                        resp = int(resp)
                    if resp ==Constants.SUCCESS:
                        print("Connection established")
                        self.isConnected=True
                    else:
                        print("SerialAuthentication Failed. Try 5 seconds later.")
                        time.sleep(5)

                # start data transfer between 
                while not self.threadDone and self.isConnected:
                    
                    # if there is a request to send data to server
                    # via socket, send it
                    try:
                        tData = tQue.get_nowait()
                        if tData:
                            self.comInt.send2Socket(tData)
                    except queue.Empty:
                        pass
                        #print("Transmit buffer is empty.")
                     
                    # read requests from server
                    try:
                        cmd = self.comInt.receiveFromSocket(10)
                        if cmd:
                            cmd = int(cmd)
                            if cmd==Constants.REQ_OPEN_DOOR:
                                print("OpenDoor")
                                self.comInt.send2Socket(b'07')
                            elif cmd==Constants.REQ_CLOSE_DOOR:
                                print("CloseDoor")
                                self.comInt.send2Socket(b'08')
                            elif cmd==Constants.REQ_PULL_BAIT:
                                print("Pull Bait")
                                self.comInt.send2Socket(b'09')
                            elif cmd==Constants.REQ_PUSH_BAIT:
                                print("Push Bait")
                                self.comInt.send2Socket(b'10')
                            elif cmd==Constants.REQ_TAKE_PHOTO:
                                # take frame from camera and convert it
                                # byte array to send over socket
                                photoName = self.cam.getFrame()
                                photo = getPhotoByteArray(photoName)
                                print("PhotoSize:",len(photo))
                                # first send photo code, name and photo
                                self.comInt.send2Socket(b'11')
                                self.comInt.send2Socket(photoName.encode())
                                self.comInt.send2Socket(photo)
                                print("Photo:",photoName,"was sent")
                    except Exception as e:
                        print("NetworkThread: run: readSockException:",str(e))
                    
        except Exception as e:
            print("NetworkThread: run: exception: ",str(e))
        except KeyboardInterrupt:
            print("here")
        finally:
            self.threadDone=True
        print("Thread done")

    def stop(self):
        self.threadDone = True

def addServerPendingQue(bArray):
    tQue.put(bArray)

def getPhotoByteArray(path="wolf.jpg"):
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
