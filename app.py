from flask import Flask, render_template, request, redirect, session
import os
import webbrowser
from threading import Timer

from flask_socketio import SocketIO
from geopy.geocoders import Nominatim
from werkzeug.utils import secure_filename

from accident_ai import detect_accident
from database import create_table, insert_data, get_data

try:
    from email_alert import send_email
except:
    send_email = None

from sms_alert import send_sms


# ---------------- APP SETUP ----------------
app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app)

create_table()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- AUTO OPEN BROWSER ----------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return " Invalid login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# ---------------- DETECT ----------------
@app.route("/detect", methods=["POST"])
def detect():

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # AI detection
    status, severity = detect_accident(filepath)

    # USER LIVE LOCATION
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    print("LAT:", lat)
    print("LON:", lon)

    if lat and lon:
        location = f"Lat: {lat}, Lon: {lon}"
        map_link = f"https://www.google.com/maps?q={lat},{lon}"
    else:
        location = "Location not available"
        map_link = None

    insert_data(status, str(severity), location)

    return render_template("result.html",
                           status=status,
                           severity=severity,
                           lat=lat,
                           lon=lon,
                           map_link=map_link)


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    data = get_data()
    return render_template("dashboard.html", data=data)


# ---------------- RUN ----------------
if __name__ == "__main__":
    print("Server Starting...")
    Timer(1, open_browser).start()
    socketio.run(app, debug=True)