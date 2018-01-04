import flask
import flask_login
import json
import sys, os, glob
import traceback


from db import DBHelper
from modules import comHelper

PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(PATH)
sys.path.insert(0,PROJECT_PATH+"/SharedData")

import Constants

trapDataDirPath = PATH+"/static/.trapData"


############### HEAD OF GLOBAL AREA - FLASK SETTINS ###############
app = None
login_manager = None
socketThread = None

def createFlaskApp():
    global app
    global login_manager
    
    try:
        # create and config flask app
        app = flask.Flask(__name__)
        #app.config["DEBUG"]=True
        app.config["SECRET_KEY"]="HM_GTU_CSE495"

        login_manager = flask_login.LoginManager()
        login_manager.init_app(app)

    except Exception as e:
        print("Flask ask create exception:",str(e))
        # Fatal Exception
        exit()
    return app

createFlaskApp()

############### END_ OF GLOBAL AREA - FLASK SETTINS ###############

class User(flask_login.UserMixin):
    def __init__(self,id):
        self.id=id
    
@login_manager.user_loader
def user_loader(email):
    return User(email)

@app.route("/signup",methods=["GET","POST"])
def sigup():
    try:

        data = flask.request.get_json()

        serial = data["serial"]
        email = data["email"]
        password = data["password"]

        retVal = DBHelper.createAccount(serial,email,password)
        if retVal!=Constants.SUCCESS:
            return flask.jsonify({"status":retVal})

        os.mkdir(trapDataDirPath+"/"+serial)

        return flask.jsonify({"status":retVal})
    except Exception as e:
        print("Exception:"+str(e))
        return flask.jsonify({"status":Constants.ERROR_UNKNOWN})

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if flask.request.method == 'POST':
            data = flask.request.get_json()
            
            email = data["email"].replace("\'","").replace("\"","")
            password = data["password"].replace("\'","").replace("\"","")

            retVal = DBHelper.checkCredential(email,password)
            # if email and password true
            if retVal == Constants.SUCCESS:
                user = User(email)
                flask_login.login_user(user)
                print("login success")
                return  flask.jsonify({"status":Constants.SUCCESS})
            elif retVal == Constants.ERROR_WRONG_EMAIL_PASS: # invalid credentials
                return  flask.jsonify({"status":Constants.ERROR_WRONG_EMAIL_PASS})
            else: # unknwon server error
                return flask.jsonify({"status":Constants.ERROR_UNKNOWN})
    except Exception as e:
        print("Exception:",str(e))
    return flask.render_template('login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.render_template("login.html",error = False, info="Logout successful")

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect("login")

@app.route('/',methods=["GET"])
@flask_login.login_required
def root():
    return flask.render_template("index.html")

@app.route("/getTraps",methods=["POST"])
@flask_login.login_required
def getTraps():
    trapsArray = Constants.SUCCESS
    try:
        trapsArray = DBHelper.getTraps(flask_login.current_user.id)
        print("getTraps:",trapsArray)
    except Excetion as e:
        print("GetTraps:",str(e))
        trapsArray = Constants.ERROR_UNKNOWN

    return flask.jsonify(trapsArray)

@app.route("/setDoor",methods=["POST"])
@flask_login.login_required
def setDoor():
    status = Constants.ERROR_UNKNOWN
    nextState = Constants.ERROR_UNKNOWN
    try:
        req = flask.request.get_json()
        serial = req["serial"]
        cmd = req["nextState"]
        print("main: serBait: serial:",serial,",cmd:",cmd)

        resp = None
        if cmd==1:
            resp = socketThread.sendReq2Trap(serial,Constants.REQ_CLOSE_DOOR)
        else:
            resp = socketThread.sendReq2Trap(serial,Constants.REQ_OPEN_DOOR)
       
        if resp == Constants.SUCCESS:
            status=Constants.SUCCESS
            nextState=cmd

    except Exception as e:
        print("FlaskException: setDoor:",str(e))
        status = Constants.ERROR_UNKNOWN
        nextState = Constants.ERROR_UNKNOWN

    print("NextStat:",nextState)
    return flask.jsonify({"status":status,"nextState":nextState})

@app.route("/setBait",methods=["POST"])
@flask_login.login_required
def setBait():
    status = Constants.ERROR_UNKNOWN
    nextState = Constants.ERROR_UNKNOWN
    try:
        req = flask.request.get_json()
        serial = req["serial"]
        cmd = req["nextState"]
        print("main: serBait: serial:",serial,",cmd:",cmd)

        resp = None
        if cmd==1:
            resp = socketThread.sendReq2Trap(serial,Constants.REQ_PULL_BAIT)
        else:
            resp = socketThread.sendReq2Trap(serial,Constants.REQ_PUSH_BAIT)
       
        if resp == Constants.SUCCESS:
            status=Constants.SUCCESS
            nextState=cmd

    except Exception as e:
        print("FlaskException: setDoor:",str(e))
        status = Constants.ERROR_UNKNOWN
        nextState = Constants.ERROR_UNKNOWN

    print("NextStat:",nextState)
    return flask.jsonify({"status":status,"nextState":nextState})

@app.route("/takePhoto",methods=["POST"])
@flask_login.login_required
def takePhoto():
    status = Constants.SUCCESS
    try:
        req = flask.request.get_json()
        serial = req["serial"]

        retVal = socketThread.sendReq2Trap(serial,Constants.REQ_TAKE_PHOTO)
        if retVal == Constants.ERROR_CONNECTION:
            status = Constants.ERROR_CONNECTION
        else:
            status = Constants.SUCCESS
    except Exception as e:
        print("Exception: main: takePhoto:",str(e))
        status = Constants.ERROR_UNKNOWN
    return flask.jsonify({"status":status})

@app.route("/getLastPhotoName",methods=["POST"])
@flask_login.login_required
def getLastPhotoName():
    try:
        data = flask.request.get_json()
        serial = data["serial"]

        path = "./static/.trapData/"+str(serial)+"/"
        # get last created/touched file name
        list_of_files = glob.glob(path+"*.jpg")
        print(list_of_files)
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = latest_file.replace(path,"")
        return flask.jsonify({"status":Constants.SUCCESS,"name":latest_file})
    except:
        return flask.jsonify({"status":Constants.ERROR_UNKNOWN})

@app.route("/getPhotoPaths",methods=["POST"])
@flask_login.login_required
def getPhotoPaths():
    status = Constants.SUCCESS
    try:
        req = flask.request.get_json()
        serial = req["serial"]
        fileList = [ f for f in os.listdir(trapDataDirPath+"/"+serial) if f.endswith(".jpg")]
        return flask.jsonify({"status":status,"paths":fileList})
    except Exception as e:
        status = Constants.ERROR_UNKNOWN
        return flask.jsonify({"status":status})

@app.route("/getTrapDetails",methods=["POST"])
@flask_login.login_required
def getTrapDetails():
    try:
        req = flask.request.get_json()
        serial = req["serial"]

        trap = DBHelper.getTrapDetails(serial)
        if trap == None:
            raise Exception

        print("main: getTrapDetails: trap:",str(trap))
        return flask.jsonify({"status":Constants.SUCCESS,
                            "name":trap.name,
                            "location":trap.location,
                            "ap":trap.ap})
    except Exception as e:
        print("Exception: main: getTrapDetails:",str(e))
        return flask.jsonify({"status":Constants.ERROR_UNKNOWN})

@app.route("/setTrapDetail",methods=["POST"])
@flask_login.login_required
def setTrapDetail():
    status = Constants.SUCCESS
    try:
        req = flask.request.get_json()

        trap = Constants.Trap(serial = req["serial"],
                                name=req["name"],
                                location =req["location"])

        status = DBHelper.setTrapDetail(trap)

        return flask.jsonify({"status":status})
    except Exception as e:
        status = Constants.ERROR_UNKNOWN
        return flask.jsonify({"status":status})

@app.route("/addNewTrap",methods=["POST"])
@flask_login.login_required
def addNewTrap():
    retVal = Constants.SUCCESS
    try:
        req = flask.request.get_json()
        serial = req["serial"]
        name = req["name"]
        location = req["location"]
        email = flask_login.current_user.id
        print(serial,name,location,email)

        retVal = DBHelper.addNewTrap(email,serial,name,location)
    except Exception as e:
        print("Exception: main: addNewTrap:"+str(e))
        retVal = Constants.ERROR_UNKNOWN

    return flask.jsonify({"status":retVal})

@app.route("/getImageGuesses",methods=["POST"])
@flask_login.login_required
def getImageGuesses():
    try:
        req = flask.request.get_json()
        serial = req["serial"]

        filePath = trapDataDirPath+"/"+serial+"/guesses.json"
        res = {}
        with open(filePath,"r") as f:
            res = json.load(f)
        return flask.jsonify({"status":Constants.SUCCESS,"guesses":res})
    except Exception as e:
        print("Exception: main: getImageGuesses:",str(e))
        traceback.print_exc()
        return flask.jsonify({"status":Constants.ERROR_UNKNOWN})

# you can access active trap connections with
# trap = socketThread.connections[ipAddress]
# trap.socket, trap.thread ...
if __name__ == "__main__":
    try:

        if not os.path.exists(trapDataDirPath):
            os.mkdir(trapDataDirPath)
            print("Trap Data Directory created.")
        # listen socket and create thread for each trap
        # all trap communication will be served over connection helper
        # TODO: remove comments
        socketThread = comHelper.ServerConnHelperThread(5669)
        socketThread.setDaemon(True)
        socketThread.start()

        app.run(host="0.0.0.0", port=5000)
        
    except KeyboardInterrupt:
        print("!!! Ctrl+C !!!")
    except Exception as e:
        print("Main: main: exception:",str(e))
    finally:
        if socketThread:
            socketThread.stop()
            socketThread.join()
