import threading
import time
import logging
import queue
import sys,os
from datetime import datetime as date

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

trapThreads = {}

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

        socket.settimeout(5.0)
        self.trapData = ClientData(ip,socket,self,rQue, tQue)

        self.logger = logging.getLogger("ClientThread["+str(ip)+"]")
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        global trapThreads

        serial = self.trapData.socket.recv(256) # read serial number first
        serial = str(serial.decode("UTF-8"))
        
        self.trapData.socket.send(b'A') # send acknowledge message to trap
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
                    buffer = self.trapData.socket.recv(1024*1024)
                    if buffer:
                        fileName = str(date.now()).replace(" ","_")
                        photoPath = PATH+"/static/.trapData/"+serial+"/"+fileName+".jpg"
                        print("Photo will be saved at:",photoPath)
                        # write image to file and send complete message to flask rest
                        with open(photoPath,"wb") as f:
                            f.write(buffer)
                            os.sync() # direct write to disk
                            print("PhotoSaved:",photoPath)
                        self.trapData.rQue.put(fileName)
                        continue

                except Exception as e:
                    buffer = None

                # no coming request, send new user request to rpi if exist
                if not buffer:
                    # if queue is empty, will raise exception
                    cmd = self.trapData.tQue.get_nowait()
                    if cmd:
                        print("Send Req:",cmd)
                        # send command to trap/rpi
                        self.trapData.socket.sendall(cmd.encode())
                elif buffer == "A":
                    print("Trap Send Animal caught signal")
                elif buffer.startswith('P-'):
                    print("Trap Send Photo Byte array")
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
        
   