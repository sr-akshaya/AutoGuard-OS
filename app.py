from flask import Flask, jsonify, render_template
import sqlite3
import random
import datetime

app = Flask(__name__)

# -------------------------
# DATABASE SETUP
# -------------------------

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            priority TEXT,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()


# -------------------------
# VEHICLE DATA GENERATION
# -------------------------

def generate_vehicle_data():
     engine_temp = random.randint(200, 230)
    battery = random.randint(50, 100)
    tire_psi = random.randint(25, 36)

    alert_message = None
    priority = None

    if engine_temp > 210:
        alert_message = "Engine Overheating"
        priority = "CRITICAL"
    elif tire_psi < 30:
        alert_message = "Low Tire Pressure"
        priority = "MEDIUM"
    elif battery < 65:
        alert_message = "Low Battery"
        priority = "LOW"

    if alert_message:
        insert_alert(alert_message, priority)

    return {
        "engine_temp": engine_temp,
        "battery": battery,
        "tire_psi": tire_psi
    }


# -------------------------
# INSERT ALERT INTO DATABASE
# -------------------------

def insert_alert(message, priority):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO alerts (message, priority, timestamp)
        VALUES (?, ?, ?)
    ''', (message, priority, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/data")
def data():
    return jsonify(generate_vehicle_data())


@app.route("/alerts")
def get_alerts():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT message, priority, timestamp FROM alerts ORDER BY id DESC LIMIT 5")
    alerts = c.fetchall()

    conn.close()

    return jsonify(alerts)


if __name__ == "__main__":
    app.run(debug=True)
