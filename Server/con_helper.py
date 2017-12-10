import socket
import logging
import time
from client_thread import TrapServiceThread 

logger = logging.getLogger("ConnectionHelper")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-20s - %(levelname)-10s - %(threadName)-10s - %(message)s',
                    )

connections = {}

class ServerConnHelper():
    def __init__(self):
        self.MAX_LISTEN_LEN = 5
        self.MAX_BUFFER_LEN = 1024

    def openConnection(self,port):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind((socket.gethostbyname("localhost"),port))
            self.sock.listen(self.MAX_LISTEN_LEN)
            logger.info("Connection opened.")
        except Exception as e:
            print("ServerConnHelper: openConnection:",str(e))

    def accept(self):
        while True:
            try:
                # accept connection from outside
                # addres => (ip,port)
                (clientsocket,ip) = self.sock.accept()
                # save ip-socket pair
                connections[ip[0]]=clientsocket

                # create threads for each trap
                clientThread = TrapServiceThread(ip,clientsocket)
                clientThread.setDaemon(True)
                clientThread.start()

            except Exception as e:
                logger.error("AcceptException:"+str(e))

if __name__=="__main__":
    try:
        conn = ServerConnHelper()
        conn.openConnection(5669)
        conn.accept()
    except KeyboardInterrupt:
        print("!! Ctrl + C !!!")
        pass