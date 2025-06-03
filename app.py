import dbPackage
import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import dbPackage.dbDays
import dbPackage.dbPerformances
import dbPackage.dbStages
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
    font = session.get("font", False)
    noTickets = dbPackage.dbTickets.getNoTickets()
    noPerformances = dbPackage.dbPerformances.getNoPerformances()
    noDays = dbPackage.dbDays.getNoDays()
    
    return render_template("home.html", noTickets=noTickets, noPerformances=noPerformances, noDays=noDays, font=font)

@app.route("/biglietti")
def tickets():
    font = session.get("font", False)
    tickets = dbPackage.dbTicketTypes.getTicketTypes()
    days = dbPackage.dbDays.getDays()
    return render_template("tickets.html", tickets=tickets, days=days, font=font)

@app.route("/buy", methods=["POST"])
def buy():
    if not current_user.is_authenticated:
        flash("Azione non permessa: l'utente non è autenticato", "danger")
        return redirect(url_for("tickets"))

    if dbPackage.dbTickets.hasIDTicket(current_user.id):
        flash("Azione non permessa: l'utente ha già un biglietto", "danger")
        return redirect(url_for("tickets"))

    try:
        startDate = int(request.form.get("day"))
    except (ValueError, TypeError):
        flash("Errore nella selezione della giornata", "danger")
        return redirect(url_for("tickets"))

    ticketID = request.form.get("ticketType")
    noDaysTicket = dbPackage.dbTicketTypes.getTicketType(ticketID)["NoOfDays"]
    days = dbPackage.dbDays.getDays()
    daysNo = len(days)

    # Verifica se le giornate selezionate sono consecutive e disponibili
    if startDate + noDaysTicket - 1 > daysNo:
        flash("Biglietto non prenotato: la tipologia selezionata non combacia con le giornate disponibili", "danger")
        return redirect(url_for("tickets"))

    for i in range(noDaysTicket):
        day = days[startDate - 1 + i]
        if day["NoPeople"] >= 200:
            flash(f"Biglietto non registrato: la giornata di {day['Day']} ({day['YYYY_MM_DD']}) è al completo", "danger")
            return redirect(url_for("tickets"))

    # Tutto OK: procedi con la registrazione
    dbPackage.dbTickets.insertTicket(ticketID, startDate, current_user.id)
    for i in range(noDaysTicket):
        dbPackage.dbDays.addPerson(startDate + i)

    flash("Biglietto acquistato correttamente!", "success")
    return redirect(url_for("tickets"))

@app.route("/sign-up", methods=["POST"])
def sign_up():
    name = request.form.get("name").upper()
    surname = request.form.get("surname").upper()
    email = request.form.get("email")
    typeUser = request.form.get("typeUser")
    password = request.form.get("password")
    
    password_with_hash = generate_password_hash(password)
    if dbPackage.dbUsers.insertUser(name, surname, email, typeUser, password_with_hash):
        flash("Ciao, <strong>" + name + "</strong>! Iscrizione effettuata con successo.", "success")
    else:
        flash("<strong>Iscrizione non riuscita!</strong> L'indirizzo mail inserito è già presente nel nostro DB. Riprova con un'altra mail.", "danger")
    
    return redirect(url_for("home"))

@app.route("/auth", methods=["POST"])
def auth():
    user_form = request.form.to_dict()
    user_db = dbPackage.dbUsers.getUserViaEmail(user_form["email"])
    if not user_db or not check_password_hash(user_db["Password"], user_form["password"]):
        flash("<strong>Login fallito</strong>, credenziali non valide.", "danger")
        return redirect(url_for("home"))
    else:
        user = User(
            id = user_db["ID"],
            name = user_db["Name"],
            surname = user_db["Surname"],
            email = user_db["EMail"],
            mode = user_db["Type"],
            password = user_db["Password"],
            hasTicket = dbPackage.dbTickets.hasIDTicket(user_db["ID"]),
        )
        
        login_user(user)
        flash("Ciao, <strong>" + user.name + "</strong>! Login effettuato con successo.", "success")
        return redirect(url_for("home"))
                
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout effettuato con successo!", "success")
    return redirect(url_for("home"))

@app.route("/pagina-personale")
@login_required
def my_page():
    font = session.get("font", False)
    return render_template("my_page.html", font=font) 

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
            hasTicket = dbPackage.dbTickets.hasIDTicket(user_db["ID"])
        )
    else:
        user = None
    
    return user

@app.route("/artisti")
def performances():
    font = session.get("font", False)
    performances = dbPackage.dbPerformances.getPublishedPerformances()
    return render_template("performances.html", font=font, performances=performances)

@app.route("/pagina-personale/bozze")
@login_required
def drafts ():
    font = session.get("font", False)
    if current_user.mode != "Organizzatore":
        flash("Azione non permessa: la realizzazione di una bozza è compito di un organizzatore", "warning")
        return redirect(url_for("my_page"))
    days = dbPackage.dbDays.getDays()
    stages = dbPackage.dbStages.getStages()
    drafts = dbPackage.dbPerformances.getDraftPerformancesByID(current_user.id)
    return render_template("my_page_drafts.html", days=days, stages=stages, drafts=drafts, font=font)

@app.route("/crea-bozza", methods=["POST"])
@login_required
def publish():
    data = request.form.to_dict()
    if not current_user.is_authenticated:
        flash("Azione non permessa: l'utente non è autenticato", "danger")
        return redirect(url_for("home"))
    if current_user.mode != "Organizzatore":
        flash("Azione non permessa: la realizzazione di una bozza è compito di un organizzatore", "warning")
        return redirect(url_for("my_page"))
    if dbPackage.dbPerformances.isArtistPresent(data["artist"]):
        flash("Artista già presente, la performance non può essere aggiunta", "warning")
        return redirect(url_for("drafts"))
    if (data["start-date"] > data["end-date"]):
        flash("Impossibile inserire la bozza: la data di fine viene prima della data di inizio", "warning")
        return redirect(url_for("drafts"))
    if (data["start-date"] == data["end-date"]) and (data["start-time"] > data["end-time"]):
        flash("Impossibile inserire la bozza: l'ora di fine viene prima dell'ora di inizio", "warning")
        return redirect(url_for("drafts"))
    
    uploaded_file = request.files.get("image")
    if uploaded_file:
        
        filename = uploaded_file.filename
        ext = os.path.splitext(filename)[1]  # ".jpg", ".png", ecc.

        safe_name = data["artist"].replace(" ", "_")
        path = f"/images/performances/{safe_name}{ext}"
        uploaded_file.save("static" + path)
        
    dbPackage.dbPerformances.addPerformance(data["artist"], data["genre"], data["description"], path, current_user.id, data["start-date"], data["start-time"], data["end-date"], data["end-time"], data["stage"])
    flash("Bozza creata con successo", "success")
    return redirect(url_for("drafts"))

@app.route("/pubblizaione-esibizione", methods=["POST"])
@login_required
def post():
    performance_id = request.form.get("performance_id")
    if dbPackage.dbPerformances.isPerformanceAddable(performance_id):
        dbPackage.dbPerformances.publishPerformance(performance_id)
        flash("Esibizione disponibile sul sito web!", "success")
        return redirect(url_for("drafts"))
    else:
        flash("Esibizione non pubblicata, ci sono dei problemi con le altre esibizioni", "warning")
        return redirect(url_for('drafts'))

@app.route("/font_change")
def font_change():
    font = session.get("font", False)
    return render_template("accessibility.html", font=font)

@app.route("/font_change", methods=["POST"])
def change_font():
    choice = request.form.get("fontToggle")
    if choice is None:
        font = False
    else:
        font = True
    session["font"] = font
    return render_template("accessibility.html", font=font)
