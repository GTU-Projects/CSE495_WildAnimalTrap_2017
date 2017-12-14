import flask
import flask_login
import json
import Constants
from db import DBHelper
import comHelper
from client_thread import trapThreads

# create and config flask app
app = flask.Flask(__name__)
#app.config["DEBUG"]=True
app.config["SECRET_KEY"]="HM_GTU_CSE495"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self,id):
        self.id=id

class Trap():
    def __init__(self,serial,userId,location):
        self.serial=serial
        self.userId=userId
        self.location=location
    
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


        retVal = DBHelper.checkAccount(serial,email)
        # if serial used or not know, warn user
        if retVal!=Constants.SUCCESS:
            return flask.jsonify({"status":retVal})

        # if creates return success otherwise return error
        retVal = DBHelper.createAccount(serial,email,password)

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
        print("AllTraps:",trapsArray)
    except Excetion as e:
        print("GetTraps:",str(e))
        trapsArray = Constants.ERROR_UNKNOWN

    return flask.jsonify(trapsArray)

@app.route("/setDoor",methods=["POST"])
@flask_login.login_required
def setDoor():
    status = Constants.SUCCESS
    nextState = Constants.ERROR_UNKNOWN
    try:
        req = flask.request.get_json()
        serial = req["serial"]
        cmd = req["nextState"]

        # 1 opendoor
        # 2 closedoor
        # 3 take photo
        """
        trapThreads["serial"].trapData.tQue.push(str(cmd))

        retVal = trapThreads["serial"].trapData.rQue.pop()

        if retVal:
            print("Door state changed")
        else:
            print("Door state change error")
        """
        nextState = cmd

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

        print("TakePhotoReqFrom:",serial)

        status = Constants.SUCCESS

    except Exception as e:
        print("main: takePhoto: exception:",str(e))
        status = Constants.ERROR_UNKNOWN

    return flask.jsonify({"status":status})


socketThread = None
# you can access active trap connections with
# trap = socketThread.connections[ipAddress]
# trap.socket, trap.thread ...

if __name__ == "__main__":
    try:
        # listen socket and create thread for each trap
        # all trap communication will be served over connection helper
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
