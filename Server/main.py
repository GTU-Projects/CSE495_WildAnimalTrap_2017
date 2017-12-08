import flask
import flask_login
import json
import Constants
from db import DBHelper

# create and config flask app
app = flask.Flask(__name__)
#app.config["DEBUG"]=True
app.config["SECRET_KEY"]="HM_GTU_CSE495"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
