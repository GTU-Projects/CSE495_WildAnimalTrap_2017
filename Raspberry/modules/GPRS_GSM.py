import time
import serial

class GPRS_GSM():
    def __init__(self,port,baudrate,timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.isConnected = True

    def connect(self):
        try:
            self.conn = serial.Serial(port = self.port,baudrate = self.baudrate, timeout = self.timeout)
            print("Connected to GSM/GPRS Module")
            self.isConnected=True
        except Exception as e:
            print(str(e))
            self.isConnected=False

        return self.isConnected

    def sendCommand(self,cmd,delay):
        try:
            self.conn.write(cmd.encode())
            time.sleep(delay)
            retVal = self.conn.read(100)
            print("RetVal:",retVal)
            return retVal
        except Exception as e:
            print("SendCommandException:",str(e))

    def initAT(self):
        self.sendCommand("AT\r",1)
        self.sendCommand("ATE0\r",1) # close echo mode

    def initTCPSocket(self,ip,port):
        self.sendCommand("AT+CPIN?\r",1);
        self.sendCommand("AT+CREG?\r",1);
        self.sendCommand("AT+CGATT?\r",1);
        self.sendCommand("AT+CIPSHUT\r",1);
        self.sendCommand("AT+CIPSTATUS\r",1);
        self.sendCommand("AT+CIPMUX=0\r",1);
        self.sendCommand("AT+CSTT?\r",1);
        self.sendCommand("AT+CSTT=\"vodafone\",\"\",\"\"\r",3);
        self.sendCommand("AT+CIICR\r",3);
        self.sendCommand("AT+CIFSR\r",1);
        self.sendCommand("AT+CIPSTART=\"TCP\",\"{}\",\"{}\"\r".format(ip,port),1);

    def makeCall(self,phone):
        print("Start to call")
        self.conn.write("ATD{};\r".encode())
        time.sleep(30)
        print("End of call")

    def readSocket(self,size):
        r = None
        try:
            r = self.conn.read(size)
            r = r.decode("UTF-8")
        except Exception as e:
            print("ReadSocketException:",str(e))
            r = None
        return r

if __name__=="__main__":
    module  = GPRS_GSM("/dev/ttyAMA0",19200,1.0)
    module.connect()
    module.initAT()
    module.initTCPSocket("138.197.121.142","5669")
    while True:
        r = module.readSocket(1)
        if r=="":
            pass
        elif r=="O":
            print("OpenDoor")
        elif r=="C":
            print("Capture")
        else:
            print("Invalid Command")
        time.sleep(1)
    #module.send2Socket("TESTMSG")
    #module.getRequest("www.google.com.tr")
    #module.makeCall("+05534912147")