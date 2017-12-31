# information codes
SUCCESS=0
ERROR_UNKNOWN=-1
ERROR_EMPTY_EMAIL_PASS=1
ERROR_WRONG_EMAIL_PASS=2
ERROR_USED_EMAIL=3
ERROR_USED_SERIAL=4
ERROR_UNK_SERIAL=5
ERROR_CONNECTION = 6
ERROR_SERIAL_INVALID=7

# request codes
REQ_OPEN_DOOR = 7
REQ_CLOSE_DOOR = 8
REQ_PULL_BAIT = 9
REQ_PUSH_BAIT = 10
REQ_TAKE_PHOTO = 11

# pin assignments
GPIO_PIN_DIST_SENSOR_TRIG = 17
GPIO_PIN_DIST_SENSOR_ECHO = 27

GPIO_PIN_STEP_1 = 6
GPIO_PIN_STEP_2 = 16
GPIO_PIN_STEP_3 = 19
GPIO_PIN_STEP_4 = 26

GPIO_PIN_DC_1 = 20
GPIO_PIN_DC_2 = 21
GPIO_PIN_DC_PWM = 18

class Trap():
    def __init__(self,serial=None,userId=None,name=None,location=None):
        self.serial=serial
        self.userId=userId
        self.location=location
        self.name=name
        # active/passive state
        self.ap = 1

    def __str__(self):
        str = "Serial:{}, UserId:{}, Name:{}, Location:{}"
        return str.format(self.serial,self.userId,self.name,self.location)



