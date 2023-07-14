from flask_app.models.user import User
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    # if "user_id" not in session:
    #     return redirect("/logout")
    # data = {
    #     'id': session['user_id']
    # }
    return render_template("dashboard.html")

@app.route("/submit", methods=["POST"])
def submit():
    # if request.form["action"] == "register":
    #     is_valid = User.is_valid_user(request.form)
    # if not is_valid:
    #     return redirect('/dashboard')
    if not User.is_valid_user(request.form):
        return redirect('/dashboard')
    data={
        "user_name":request.form["user_name"].lower(),
        "email":request.form["email"].lower(),
        "password":bcrypt.generate_password_hash(request.form["password"])
    }

    id=User.save(data)
    session['user_id'] = id
    return redirect("/show")

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/dashboard')
    # if not bcrypt.check_password_hash(user.password, request.form['password']):
    if not bcrypt.generate_password_hash(request.form['password']):
        flash("Invalid Password","login")
        return redirect('/dashboard')
    session['user_id'] = user.id
    return redirect('/show')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/dashboard")