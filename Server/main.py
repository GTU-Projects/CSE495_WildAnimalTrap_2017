import flask
import flask_login

# create and config flask app
app = flask.Flask(__name__)
#app.config["DEBUG"]=True
app.config["SECRET_KEY"]="HM_GTU_CSE495"


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {"hmen.56@gmail.com":{"password":"Hasan5669"}}

class User(flask_login.UserMixin):
    pass
    
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return None

    user = User()
    user.id=email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return None

    user = User()
    user.id = email

    if request.form["password"] == users[email]["password"]:
        user.is_authenticated = True
    else:
        user.is_authenticated = False

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if flask.request.method == 'POST':
        
        email = flask.request.form['email']
        password = flask.request.form['password']
        
        if email == "" or password == "":
            return flask.render_template('login.html', error = "Empty E-Mail or Password")

        email = email.replace("\'","").replace("\"","")
        password = password.replace("\'","").replace("\"","")

        if email not in users:
            return flask.render_template('login.html', error = "Invalid E-Mail or Password",info=False)

        if flask.request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return flask.render_template("index.html")
        else:
            return flask.render_template('login.html', error = "Invalid E-Mail or Password")

    return flask.render_template('login.html', error = False, info=False)

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
