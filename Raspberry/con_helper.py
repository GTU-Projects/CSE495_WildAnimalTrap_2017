import socket

class ClientConnHelper():
    def __init__(self):
        self.isConnected=False
        self.MAX_WRITE_LEN=1024

    def connect(self,ip,port):
        try:
            
            self.ip=ip
            self.port=port
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            # TODO: look this line
            self.sock.connect((socket.gethostname(self.ip),self.port))
            self.isConnected=True
        except Exception as e:
            return self.isConnected

    def sendMsg(self,str):
        try:
            self.sock.send(str.encode())
            return True
        except Exception as e:
            return False

    def reConnect(self):
        try:
            self.sock.connect((socket.gethostbyname(self.ip),self.port))
            self.isConnected=True
        except:
            return self.isConnected

if __name__=="__main__":
    conn = ClientConnHelper()
    conn.connect("0.0.0.0",5669)
    conn.sendMsg("HmTest".encode())