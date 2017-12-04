import socket

class ClientConnHelper():
    def __init__(self):
        self.isConnected=False
        self.MAX_WRITE_LEN=1024

    def connect(self,ip,port):
        try:
            self.isConnected
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((socket.gethostname(),port))
            print("connected")
        except Exception as e:
            print("error"+str(e))

    def sendMsg(self,str):
        
        try:
            self.sock.send("test".encode())
            return True
        except Exception as e:
            print(str(e))
            return False

if __name__=="__main__":
    conn = ClientConnHelper()
    conn.connect("0.0.0.0",5669)
    conn.sendMsg("HmTest".encode())