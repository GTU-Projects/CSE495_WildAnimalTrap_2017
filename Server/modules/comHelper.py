import socket
import logging
import time
import threading
import queue
import Constants
import traceback
from client_thread import TrapServiceThread 
from client_thread import trapThreads

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

        self.perTrapThreads = []

        # TODO: save threads to kill later

    def stop(self):
        self.threadDone=True

        for th in self.perTrapThreads:
            print("Send stop signal to trap threads")
            th.stop()
        
        for th in self.perTrapThreads:
            print("Join thread")
            th.join()

        if self.isPortOpened:
            self.sock.close()

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
                transmitQueue = queue.Queue()
                receiveQueue = queue.Queue()
                # create threads for each trap
                clientThread = TrapServiceThread(ip,clientsocket,receiveQueue,transmitQueue)
                # save thread to kill or use later
                self.perTrapThreads.append(clientThread)
                clientThread.setDaemon(True)
                clientThread.start()

            except Exception as e:
                print("ServerConnHelperThread, run, exception:",str(e))

    def openConnection(self):
        """ Open socket connection, bind and listen ports
        """
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((socket.gethostbyname("localhost"),self.port))
            self.sock.listen(self.MAX_LISTEN_LEN)
            self.isPortOpened=True
            logger.info("Connection opened.")
        except Exception as e:
            self.isPortOpened=False
            print("ServerConnHelper: openConnection:",str(e))
        return self.isPortOpened

    def sendReq2Trap(self,serial,reqConstant):
        try:
            print("SendReq2Trap:{serial},{const}".format(serial=serial,const=reqConstant))
            if len(trapThreads)==0:
                print("Trap not connected yet.")
                return Constants.ERROR_CONNECTION

            # send command to trap special thread
            trapThreads[str(serial)].tQue.put(str(reqConstant))
            print("Message put on transmit queue")

            # now, wait and take response for taking photo request
            resp  = trapThreads[str(serial)].rQue.get()
            return resp
        except Exception as e:
            traceback.print_exc()
            print("**Exception: comHelper: sendReq2Trap",str(e))
            return Constants.ERROR_CONNECTION


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