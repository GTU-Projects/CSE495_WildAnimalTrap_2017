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

    def sendCommand(self,cmd,timeout):
        try:
            print("++>Send:",cmd)
            self.conn.write(cmd.encode())
            time.sleep(timeout)
            retVal = self.conn.readline()
            retVal = self.conn.readline()
            print("-->Resp:",retVal)
            return retVal
        except Exception as e:
            print("SendCommandException:",str(e))

    def initAT(self):
        self.sendCommand("AT\r",1)
        self.sendCommand("ATE0\r",1) # close echo mode
        print("initAT End")

    def initNetworkCfg(self):
        #self.sendCommand("AT+CPIN?\r")
        #self.sendCommand("AT+CREG?\r")
        #self.sendCommand("AT+CGATT?\r")
        
        while self.sendCommand("AT+CIPSHUT\r",1) != b'SHUT OK\r\n':
            time.sleep(0.5)
            
        while self.sendCommand("AT+CIPSTATUS\r",1) != b'OK\r\n':
            time.sleep(0.5)
        
        resp = self.sendCommand("AT+CIPMUX=0\r",1)
        while resp and resp!=b'OK\r\n':
            resp = self.sendCommand("AT+CIPMUX=0\r",1)
            time.sleep(0.5)
            
        resp =  self.sendCommand("AT+CGATT\r",1)
        while resp and resp != b'OK\r\n':
            resp = self.sendCommand("AT+CGATT\r",1)
            time.sleep(0.5)
            
        #self.sendCommand("AT+CSTT?\r")
        
        reps = self.sendCommand("AT+CSTT=\"vodafone\",\"\",\"\"\r",1)
        while resp and resp != b'OK\r\n':
            resp = self.sendCommand("AT+CSTT=\"vodafone\",\"\",\"\"\r",1)
            time.sleep(0.5)
            
        # bring-up gprs connection
        resp  = self.sendCommand("AT+CIICR\r",2)
        while resp and resp!= b'OK\r\n':
            resp  = self.sendCommand("AT+CIICR\r",2)
            time.sleep(0.5)
            
        self.sendCommand("AT+CIFSR\r",2)
        print("initNetCfg End")
        return True
        
    def openTCPSocket(self,ip,port):
        resp = self.sendCommand("AT+CIPSTART=\"TCP\",\"{}\",\"{}\"\r".format(ip,port),3)
        while resp and resp != b'OK\r\n':
            resp =self.sendCommand("AT+CIPSTART=\"TCP\",\"{}\",\"{}\"\r".format(ip,port),3)
            time.sleep(0.5)
        
        # read new lines from uart line    
        self.readLineFromSocket()
        # read tcp socket status
        tcpStatus = self.readLineFromSocket()
        print("## openTCPSocket End")

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
