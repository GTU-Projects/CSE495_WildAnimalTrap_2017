import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

class TrapServiceThread(threading.Thread):
    def __init__(self,ip,socket):
        threading.Thread.__init__(self)
        self.threadDoneFlag=False

        self.ip = ip
        self.sock = socket

        self.logger = logging.getLogger("ClientThread["+str(ip)+"]")
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        
        while not self.threadDoneFlag:
            try:
                buffer = self.sock.recv(1024) # read byte from socket
                # decode buffer to UTF-8 to se human readable text
                print("TrapServiceThread: Read:",buffer)
                
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
        
   