import dbPackage
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import dbPackage.dbDays
import dbPackage.dbPerformances
import dbPackage.dbTicketTypes
import dbPackage.dbTickets
import dbPackage.dbUsers
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "WEBAPP-2025"

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def home():
    noTickets = dbPackage.dbTickets.getNoTickets()
    noPerformances = dbPackage.dbPerformances.getNoPerformances()
    noDays = dbPackage.dbDays.getNoDays()
    
    return render_template("home.html", noTickets=noTickets, noPerformances=noPerformances, noDays=noDays)

@app.route("/biglietti")
def tickets():
    tickets = dbPackage.dbTicketTypes.getTicketTypes()
    days = dbPackage.dbDays.getDays()
    return render_template("tickets.html", tickets=tickets, days=days)

@app.route("/sign-up", methods=["POST"])
def sign_up():
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    typeUser = request.form.get("typeUser")
    password = request.form.get("password")
    
    password_with_hash = generate_password_hash(password)
    dbPackage.dbUsers.insertUser(name, surname, email, typeUser, password_with_hash)
    
    return redirect(url_for("home"))

@app.route("/auth", methods=["POST"])
def auth():
    user_form = request.form.to_dict()
    user_db = dbPackage.dbUsers.getUserViaEmail(user_form["email"])
    if not user_db or not check_password_hash(user_db["Password"], user_form["password"]):
        print("NOT LOGGED")
        return redirect(url_for("home"))
    else:
        user = User(
            id = user_db["ID"],
            name = user_db["Name"],
            surname = user_db["Surname"],
            email = user_db["EMail"],
            mode = user_db["Type"],
            password = user_db["Password"],
        )
        
        login_user(user)
        print("LOGGED")
        return redirect(url_for("home"))
        
                
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
        

@login_manager.user_loader
def load_user(user_id):
    user_db = dbPackage.dbUsers.getUser(user_id)
    if user_db is not None:
        user = User(
            id=user_db["ID"],
            name=user_db["Name"],
            surname=user_db["Surname"],
            email=user_db["EMail"],
            mode=user_db["Type"],
            password=user_db["Password"],
        )
    else:
        user = None
    
    return user
    