import threading
import time
from SocketInterface import SocketInterface


class NetworkThread(threading.Thread):
    def __init__(self,ip=138.197.121.142,port=5669,serial=95):
        threading.Thread.__init__(self)

        self.sockInt = SocketInterface(ip,port)

        # serial number for authentication of server-trap connection
        self.serial = str(serial)

        self.threadDone = False
        self.isConnected = False

    def run(self):
        try:
            # if there is no connection try to connect every 5 sec
            while not self.threadDone and not self.sockInt.isConnected:
                self.sockInt.connect()
                time.sleep(1)

            # send serial number to thread
            while not self.threadDone and not self.isConnected:
                self.sockInt.send2Socket(self.serial)
                resp = self.sockInt.receiveFromSocket()
                resp = resp.decode("UTF-8")
                if resp =="A":
                    print("Connection established")
                    self.isConnected=True
                else:
                    print("SerialAuthentication Failed. Try 5 seconds later.")
                    time.sleep(5)

            while not self.threadDone:
                cmd = self.sockInt.receiveFromSocket()
                cmd = cmd.decode("UTF-8")
                if cmd=="O":
                    print("OpenDoor")
                elif cmd=="C":
                    print("CloseDoor")
                elif cmd=="P":
                    print("ThakePhoto")
        except Exception as e:
            print("NetworkThread: run: exception: ",str(e))
        print("Thread done")

    def stop(self):
        self.threadDone = True

if __name__=="__main__":

    netThread = None
    try:
        netThread = NetworkThread("127.0.0.1",5669,"95")
        netThread.setDaemon(True)
        netThread.start()

        while not netThread.threadDone:
            pass

    except Exception as e:
        print("NetworkThread: main: exception: ",str(e))
    except KeyboardInterrupt:
        print("!!! Ctrl + C !!!")
    finally:
        if netThread:
            netThread.stop()
            netThread.join()
