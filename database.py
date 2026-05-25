
import sqlite3

#### Firebase Imports
##import firebase_admin
#from firebase_admin import credentials, firestore

# Firebase Setup (safe connection)
##try:
    ##if not firebase_admin._apps:
        ##cred = credentials.Certificate("firebase_key.json")
        ##firebase_admin.initialize_app(cred)
    ##db = firestore.client()
   ## print("Firebase Connected")
##except Exception as e:
   ## db = None
   ### print(" Firebase not connected:", e)


# ---------------- CREATE TABLE ----------------
def create_table():

    conn = sqlite3.connect("accident.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS accidents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT,
        severity TEXT,
        location TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT DATA ----------------
def insert_data(status, severity, location):

    #  Save in SQLite
    conn = sqlite3.connect("accident.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO accidents(status,severity,location) VALUES (?,?,?)",
        (status, severity, location)
    )

    conn.commit()
    conn.close()

    print(" Data saved in SQLite")

   ### #  Save in Firebase (if connected)
   ## if db:
       ## try:
            #3db.collection("accidents").add({
               ## "status": status,
               ## "severity": severity,
               ## "location": location
          ##  })
            ##print(" Data saved in Firebase")
        ##except Exception as e:
##print(" Firebase Error:", e)


# ---------------- GET DATA ----------------
def get_data():

    conn = sqlite3.connect("accident.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM accidents")

    data = cur.fetchall()

    conn.close()

    return data

