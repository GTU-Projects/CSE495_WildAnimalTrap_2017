import flask
import flask_login
import json
import Constants

# create and config flask app
app = flask.Flask(__name__)
#app.config["DEBUG"]=True
app.config["SECRET_KEY"]="HM_GTU_CSE495"


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {"email":"hmen.56@gmail.com","password":"Hasan5669"}


class User(flask_login.UserMixin):
    def __init__(self,id):
        self.id=id
    
@login_manager.user_loader
def user_loader(email):
    return User(email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    try:
        if flask.request.method == 'POST':
            data = flask.request.get_json()
            
            email = data["email"]
            password = data["password"]
            if email == "" or password == "":
                return {"status":Constants.ERROR_EMPTY_EMAIL_PASS}

            email = email.replace("\'","").replace("\"","")
            password = password.replace("\'","").replace("\"","")

            # TODO: add checkLogin
            if  email == users["email"] and password==users['password']:
                user = User(email)
                flask_login.login_user(user)
                print("login success")
                return  flask.jsonify({"status":Constants.SUCCESS})
            else:
                return  flask.jsonify({"status":Constants.ERROR_WRONG_EMAIL_PASS})

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
