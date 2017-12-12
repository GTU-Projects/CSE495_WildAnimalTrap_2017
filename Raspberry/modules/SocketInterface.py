import socket

class SocketInterface():

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

        self.isConnected = False

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket.connect((self.ip,self.port))
            self.isConnected = True
        except Exception as e:
            self.isConnected = False
            print("SocketInterface: connect: exception:",str(e))

    def send2Socket(self,str):
        retVal = False
        try:
            self.socket.sendall(str.encode())
            retVal= True
        except Exception as e:
            print("SocketInterface: send2Socket: exception:",str(e))

        return retVal

    def receiveFromSocket(self):

        retVal = None
        try:
            retVal =  self.socket.recv(1)
        except Exception as e:
            print("SocketInterface: receiveFromSocket: exception:",str(e))
            retVal = None

        return retVal
    
    def disconnect(self):
        self.socket.close()
