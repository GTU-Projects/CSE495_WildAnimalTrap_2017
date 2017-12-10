import socket
import logging
import time
import threading
from client_thread import TrapServiceThread 

logger = logging.getLogger("ConnectionHelper")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

class ClientData():
    """ Store client socket, thread and ip address
    """
    def __init__(self,ip,socket,thread):
        self.socket = socket
        self.thread = thread

class ServerConnHelperThread(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)

        self.MAX_LISTEN_LEN = 5
        self.MAX_BUFFER_LEN = 1024

        self.threadDone = False

        self.port = port
        self.connections = {}

    def stop(self):
        self.threadDone=True

        for i in self.connections:
            
            print(self.connections[i].socket)

    def run(self):

        self.openConnection()

        while not self.threadDone:
            try:
                # accept connection from outside
                # addres => (ip,port)
                (clientsocket,ip) = self.sock.accept()
                # save ip-socket pair
                

                # create threads for each trap
                clientThread = TrapServiceThread(ip,clientsocket)

                self.connections[ip[0]] = ClientData(ip,clientsocket,clientThread)

                clientThread.setDaemon(True)
                clientThread.start()
            except Exception as e:
                print("ServerConnHelperThread, run, exception:",str(e))

    def openConnection(self):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind((socket.gethostbyname("localhost"),self.port))
            self.sock.listen(self.MAX_LISTEN_LEN)
            logger.info("Connection opened.")
        except Exception as e:
            print("ServerConnHelper: openConnection:",str(e))


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