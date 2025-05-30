import dbPackage
from flask import Flask, render_template

import dbPackage.dbDays
import dbPackage.dbPerformances
import dbPackage.dbTicketTypes
import dbPackage.dbTickets

app = Flask(__name__)

@app.route("/")
def home():
    noTickets = dbPackage.dbTickets.getNoTickets()
    noPerformances = dbPackage.dbPerformances.getNoPerformances()
    noDays = dbPackage.dbDays.getNoDays()
    
    return render_template("home.html", noTickets=noTickets, noPerformances=noPerformances, noDays=noDays)

@app.route("/biglietti")
def tickets():
    tickets = dbPackage.dbTicketTypes.getTicketTypes()
    return render_template("tickets.html", tickets=tickets)