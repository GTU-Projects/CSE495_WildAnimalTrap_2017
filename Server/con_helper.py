import socket
import logging
import time

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
            print(str(e))

    def accept(self):
        while True:
            try:
                # accept connection from outside
                # addres => (ip,port)
                (clientsocket,address) = self.sock.accept()
                # save ip-socket pair
                connections[address[0]]=clientsocket
                logger.debug("Client[{}:{}] accepted.".format(address[0],address[1]))

                self.read(address[0])

            except Exception as e:
                logger.error("Accept exception"+str(e))

    def read(self,ip):
        buffer = []
        bytes_recv =0
        try:
            sock = connections[ip]
            while True:
                buffer = sock.recv(1024)
                print("Read:",buffer.decode("UTF-8"))
                time.sleep(1)
        except Exception as e:
            print("err"+str(e))


if __name__=="__main__":
    conn = ServerConnHelper()
    conn.openConnection(5669)
    conn.accept()
    conn.read("127.0.0.1")
