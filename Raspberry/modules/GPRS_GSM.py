import time
import serial

class GPRS_GSM():
    def __init__(self,port,baudrate,timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.isConnected = True

    def initHWModule(self):
        try:
            self.conn = serial.Serial(port = self.port,baudrate = self.baudrate, timeout = self.timeout)
            print("Connected to GSM/GPRS Module")
            self.isConnected=True
            
            self.initAT()
            print("GPRS_GSM Module was Initialized")
            
        except Exception as e:
            print(str(e))
            self.isConnected=False

        return self.isConnected

    def sendCommand(self,cmd):
        try:
            print("Send:",cmd)
            self.conn.write(cmd.encode())
            retVal = self.conn.readline()
            retVal = self.conn.readline()
            print("Resp:",retVal)
            return retVal
        except Exception as e:
            print("SendCommandException:",str(e))

    def initAT(self):
        self.sendCommand("AT\r")
        self.sendCommand("ATE0\r") # close echo mode
        print("initAT End")

    def initNetworkCfg(self):
        #self.sendCommand("AT+CPIN?\r")
        #self.sendCommand("AT+CREG?\r")
        #self.sendCommand("AT+CGATT?\r")
        
        while self.sendCommand("AT+CIPSHUT\r") != b'SHUT OK\r\n':
            time.sleep(0.5)
            
        while self.sendCommand("AT+CIPSTATUS\r") != b'OK\r\n':
            time.sleep(0.5)
        
        while self.sendCommand("AT+CIPMUX=0\r")!=b'STATE: IP INITIAL\r\n':
            time.sleep(0.5)
            
        while self.sendCommand("AT+CGATT\r") != b'OK\r\n':
            time.sleep(0.5)
            
        #self.sendCommand("AT+CSTT?\r")
        
        while self.sendCommand("AT+CSTT=\"vodafone\",\"\",\"\"\r") != b'OK\r\n':
            time.sleep(0.5)
            
        # bring-up gprs connection
        while self.sendCommand("AT+CIICR\r") != b'OK\r\n' or False:
            time.sleep(0.5)
            
        self.sendCommand("AT+CIFSR\r")
        print("initNetCfg End")
        return True
        
    def openTCPSocket(self,ip,port):
        while self.sendCommand("AT+CIPSTART=\"TCP\",\"{}\",\"{}\"\r".format(ip,port)) != b'OK\r\n':
            time.sleep(0.5)
            
        self.readLineFromSocket()
        self.readLineFromSocket()
        print("openTCPSocket End")

    def makeCall(self,phone):
        print("Start to call.ATD{number};\r".format(number=phone))
        self.sendCommand("ATD{number};\r".format(number=phone));
        
    def send2Socket(self,bArray):
        print("Send2Socket:",bArray)
        self.conn.write(b'AT+CIPSEND\r')
        
        # read first \r\n
        r = self.readLineFromSocket()
        # read '>' sign
        r = self.readLineFromSocket()
                
        self.conn.write(bArray)
        self.conn.write(bytes([26]))
        self.conn.flush()
        
        # read \r\n
        r = self.readLineFromSocket()
        
        # read command result
        r=self.readLineFromSocket()
        while len(r)!=0 or r!=b'SEND OK\r\n':
            r=self.readLineFromSocket()
            
        
    def finishCall(self):
        self.sendCommand("ATH0\r");
        print("Finish phone call")

    def readLineFromSocket(self):
        r = self.conn.readline()
        print("ReadLine:",r)
        return r
        
    def readSocket(self,size):
        """ Read byte data from socket which is size is given with size
            parameter.
        """
        r = None
        try:
            r = self.conn.read(size)
        except Exception as e:
            print("ReadSocketException:",str(e))
            r = None
        print("Read:",r)
        return r
        
    def test(self):
        print("Test1: Start Phone Call")
        self.comInt.makeCall("+905534912147")
        time.sleep(10)
        self.comInt.finishCall()
        print("Test1: Done")
        
        print("Test2: Read 10 Times from socket")
        for i in range(0,10):
            a = self.comInt.readSocket(1000)
            print(a)
            time.sleep(1)
        print("Test2: End")

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
    #module.getRequest("w.google.com.tr")
    #module.makeCall("+05534912147")
