from module import GPRS_GSM # load gsm module interface

def main():
    try:
        networkModule = GPRS_GSM("/dev/ttyAMA0",19200,2.0)
        networkModule.initAT()
        networkModule.initTCPSocket("138.197.121.142","5669")
    except KeyboardInterrupt:
        print("!! Ctrl+C !!")
    except Exception as e:
        print("MainException:",str(e))


if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("!! Ctrl+C !!")
    except Exception as e:
        print("MainException:",str(e))
