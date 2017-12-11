import socket
import logging
import time
import threading
from queue import Queue
from client_thread import TrapServiceThread 

logger = logging.getLogger("ConnectionHelper")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

class ServerConnHelperThread(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)

        self.MAX_LISTEN_LEN = 5
        self.MAX_BUFFER_LEN = 1024

        self.threadDone = False

        self.port = port
        self.isPortOpened = False

        # TODO: save threads to kill later

    def stop(self):
        self.threadDone=True

    def run(self):

        # turn until connection/port open
        self.openConnection()
        while not self.isPortOpened and not self.threadDone:
            self.openConnection()

        while not self.threadDone:
            try:
                # accept connection from outside
                # addres => (ip,port)
                (clientsocket,ip) = self.sock.accept()

                # thread will send data which is writed in transmit queue
                # and will save response vaue inside of receiveQueue
                transmitQueue = Queue()
                receiveQueue = Queue()
                # create threads for each trap
                clientThread = TrapServiceThread(ip,clientsocket,receiveQueue,transmitQueue)
                clientThread.setDaemon(True)
                clientThread.start()

            except Exception as e:
                print("ServerConnHelperThread, run, exception:",str(e))

    def openConnection(self):
        """ Open socket connection, bind and listen ports
        """
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind((socket.gethostbyname("localhost"),self.port))
            self.sock.listen(self.MAX_LISTEN_LEN)
            self.isPortOpened=True
            logger.info("Connection opened.")
        except Exception as e:
            self.isPortOpened=False
            print("ServerConnHelper: openConnection:",str(e))
        return self.isPortOpened


if __name__=="__main__":
    conn = None
    try:
        conn = ServerConnHelperThread(5669)
        conn.setDaemon(True)
        conn.start()

        while True:
            pass

    except KeyboardInterrupt:
        conn.stop()
        print("!! Ctrl + C !!!")
        pass