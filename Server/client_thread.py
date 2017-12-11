import threading
import time
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )


trapThreads = {}

class ClientData():
    """ Store client socket, thread and ip address
    """
    def __init__(self,ip,socket,thread, rQue, tQeu):
        self.socket = socket
        self.thread = thread
        self.ip = ip
        self.rQue = rQue
        self.tQue = tQue

class TrapServiceThread(threading.Thread):
    def __init__(self,ip,socket,rQue, tQue):
        threading.Thread.__init__(self)
        self.threadDoneFlag=False

        socket.settimeout(3.0)
        self.trapData = ClientData(ip,socket,self,rQue, tQue)

        self.logger = logging.getLogger("ClientThread["+str(ip)+"]")
        self.logger.setLevel(logging.DEBUG)

    def run(self):

        buffer = self.sock.recv(256).decode("UTF-8") # read serial number first
        # TODO: if serial is valid ...

        trapThreads[buffer] = self.trapData
        
        while not self.threadDoneFlag:
            try:

                # read socket there is a incoming request otherwise send commands
                # socket recv has 3 seconds timeout
                buffer = self.trapData.sock.recv(256).decode("UTF-8") # read byte from socket
                # decode buffer to UTF-8 to se human readable text
                print("TrapServiceThread: Read:",buffer)
            
                if buffer.startswith('S-'):
                    print("Trap Send Serial Number for connection")
                    # TODO: set trap according to serial number
                    #       match Serial-TrapIp address
                elif buffer == "A":
                    print("Trap Send Animal caught signal")
                elif buffer.startswith('P-'):
                    print("Trap Send Photo Byte array")

                ## push receive data to rQeu

                else:
                    # if empty throw empty exception and continue to recv operation
                    cmd = self.trapData.tQue.get_nowait()
                    
                    # send command to trap/rpi
                    self.trapData.soc.sendall(cmd)

                
            except Exception as e:
                print("TrapServiceThreadException:",str(e))

            time.sleep(1)

    def stop(self):
        while not self.threadDoneFlag:
            self.threadDoneFlag=True
        

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
        
   