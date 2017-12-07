import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

class ClientThread(threading.Thread):
    def __init__(self,name,socket):
        threading.Thread.__init__(self)
        self.exitThread=False

        self.name = name
        self.sock = socket

        self.logger = logging.getLogger("ClientThread["+name+"]")
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        
        while self.exitThread==False:
            self.logger.debug("Thread run")
            time.sleep(0.5)
        self.logger.info("Thread done")

    def stop(self):
        while not self.exitThread:
            self.exitThread=True
        

if __name__=="__main__":

    hmThread = ClientThread("hmenn",None)
    hmThread.start()
    time.sleep(3)
    hmThread.stop()
    hmThread.join()