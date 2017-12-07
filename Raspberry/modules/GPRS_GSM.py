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

    def getRequest(self, url):
        try:
            self.conn.write("AT+CSQ".encode())
            time.sleep(0.2)
            print(self.conn.readline())
            

            self.conn.write("AT+CGATT?".encode())
            time.sleep(0.2)
            print(self.conn.readline())
            

            self.conn.write("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"".encode())
            time.sleep(1.2)
            print(self.conn.readline())
            

            self.conn.write("AT+SAPBR=3,1,\"APN\",\"CMNET\"".encode())
            time.sleep(4.2)
            print(self.conn.readline())
            

            self.conn.write("AT+SAPBR=1,1".encode())
            time.sleep(2.2)
            print(self.conn.readline())
            

            self.conn.write("AT+HTTPINIT".encode())
            time.sleep(2.2)
            print(self.conn.readline())
            

            self.conn.write("AT+HTTPPARA=\"URL\",\"www.google.com.tr\"".encode())
            time.sleep(1.2)
            print(self.conn.readline())
            

            self.conn.write("AT+HTTPACTION=0".encode())
            time.sleep(10.2)
            print(self.conn.readline())
            

            self.conn.write("AT+HTTPREAD".encode())
            time.sleep(10.2)
            print(self.conn.readline())
            

        except Exception as e:
            print(str(e))
            return False

    def makeCall(self,phone):
        print("Start to call")
        self.conn.write("ATD{};\r".encode())
        time.sleep(30)
        print("End of call")

    def test(self):
        self.conn.write("AT\r".encode())
        time.sleep(0.1)
        retVal = self.conn.readline()
        print("text:",retVal.decode("UTF-8"))

if __name__=="__main__":
    module  = GPRS_GSM("/dev/ttyAMA0",19200,1.0)
    module.connect()
    #module.getRequest("www.google.com.tr")
    #module.makeCall("+05534912147")
    module.test()