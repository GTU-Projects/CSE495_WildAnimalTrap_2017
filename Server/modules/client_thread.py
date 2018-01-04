import threading
import time
import logging
import queue
import sys,os
import json
import socket
from datetime import datetime as date
import YOLOHelper
import Constants

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

trapThreads = {}

detector = YOLOHelper.loadDetector()

class ClientData():
    """ Store client socket, thread and ip address
    """
    def __init__(self,ip,socket,thread, rQue, tQue):
        self.socket = socket
        self.thread = thread
        self.ip = ip
        self.rQue = rQue
        self.tQue = tQue

class TrapServiceThread(threading.Thread):

    def __init__(self,ip,socket,rQue, tQue):
        threading.Thread.__init__(self)
        self.threadDoneFlag=False

        # TODO: increate timeout for dicrease network control interval
        socket.settimeout(2.0)
        self.trapData = ClientData(ip,socket,self,rQue, tQue)

        self.logger = logging.getLogger("ClientThread["+str(ip)+"]")
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        global trapThreads

        serial = self.trapData.socket.recv(256) # read serial number first
        serial = str(serial.decode("UTF-8"))
        
        self.trapData.socket.send(b'0') # send acknowledge message to trap
        print("Trap:",serial,"connected")
        # TODO: if serial is valid ...

        trapThreads[serial] = self.trapData
        time.sleep(1)
        
        while not self.threadDoneFlag:
            try:

                # read socket there is a incoming request otherwise send commands
                # socket recv has 3 seconds timeout
                buffer = None
                try:
                    # if timeout occur, throw timeout exception
                    buffer = self.trapData.socket.recv(2)
                    if buffer == b'11':
                        # 2017-12-26_19.29.22.jpg = 23byte
                        filename = self.trapData.socket.recv(23)
                        photoPath = PATH+"/static/.trapData/"+serial+"/"+filename.decode("UTF-8")
                        print("Photo will be saved at:",photoPath)
                            # write image to file and send complete message to flask rest

                        photo = None
                        photoPacketSize = 1024
                        t = self.trapData.socket.recv(photoPacketSize)
                        if t:
                            photo = t
                            while len(t)>=photoPacketSize:
                                time.sleep(0.05)
                                t = self.trapData.socket.recv(photoPacketSize)
                                photo += t
                        print("PhotoLen:",len(photo))
                        with open(photoPath,"wb") as f:
                            f.write(photo)
                            os.sync() # direct write to disk
                            print("PhotoSaved:",photoPath)
                        self.trapData.rQue.put(filename)

                        print("Analyzing photo")
                        results = YOLOHelper.detectPhoto(detector,photoPath)

                        data = {}
                        jsonPath = PATH+"/static/.trapData/"+serial+"/guesses.json"

                        # if file already exist, add new results onto the old ones.
                        if os.path.exists(jsonPath):
                            with open(jsonPath,"r") as f:
                                data = json.load(f)

                        data[filename.decode("UTF-8")]=results

                        with open(jsonPath,"w") as f:
                            f.write(json.dumps(data))
                        os.sync()
                        time.sleep(0.3)
                        print("client_thread: TrapServiceThread: run: photo saved.")
                    elif buffer == b'09' or buffer==b'10': # req_pull_bait or req_push_bait
                        stat = self.trapData.socket.recv(1)
                        if stat == b'1':
                            self.trapData.rQue.put(Constants.SUCCESS)
                        else:
                            self.trapData.rQue.put(Constants.ERROR_UNKNOWN)
                    
                    continue

                except socket.timeout: # if there is no new request from server
                    pass
                except Exception as e:
                    print("Exception: client_thread: run:",str(e))
                    buffer = None

                # no coming request, send new user request to rpi if exist
                if not buffer:
                    # if queue is empty, will raise exception
                    cmd = self.trapData.tQue.get_nowait()
                    if cmd:
                        print("Send Req:",cmd)
                        # send command to trap/rpi
                        self.trapData.socket.sendall(cmd.encode())
            except queue.Empty:
                pass
            except Exception as e:
                print("TrapServiceThreadException:",str(e))

            time.sleep(1)

    def stop(self):
        while not self.threadDoneFlag:
            self.threadDoneFlag=True
        self.trapData.socket.close()
        print("Trap special socket closed")
        

if __name__=="__main__":
    try:
        hmThread = TrapServiceThread("127.0.0.1",None)
        hmThread.start()
        time.sleep(5)
    except KeyboardInterrupt:
        print("!! Ctrl + C !!!")
        hmThread.stop()
    finally:
        hmThread.join()
        
   