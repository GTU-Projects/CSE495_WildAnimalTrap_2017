import logging

TrapLoggerLevels = {"DEBUG":logging.DEBUG,
                    "INFO":logging.INFO,
                    "WARNING":logging.WARNING,
                    "ERROR":logging.ERROR}

class TrapLogger():
    def __init__(self,name):

        self.level=logging.DEBUG
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.FORMAT = FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'

    def setLevel(self,level):

        try:
            if level in TrapLoggerLevels:
                self.level=TrapLoggerLevels[level]
            else:
                self.level=TrapLoggerLevels["WARNING"]
            self.logger.setLevel(self.level)
        except Exception as e:
            print(str(e))

    def info(msg):
        try:
            self.level>self.INFO:
                print(msg)

        except:
