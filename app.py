# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date
import sqlite3
import os

app = Flask(__name__, template_folder="cliniccarepros/templates")
app.secret_key = 'secret_key_for_flask_flash_messages'

# ---------- PATH FOR DATABASE ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "clinic.db")

# ---------- DATABASE FUNCTIONS ----------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hn TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            address TEXT,
            citizen_id TEXT,
            healthcare TEXT
        )
        """)
        conn.commit()

# ---------- ROUTES ----------
@app.route('/')
def index():
    return redirect(url_for('patients'))

@app.route('/patients')
def patients():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patients")
            rows = cur.fetchall()
        return render_template('patients.html', patients=rows)
    except Exception as e:
        return f"Error loading patients: {e}", 500

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        try:
            hn = request.form.get('hn', '')
            first_name = request.form.get('first_name', '')
            last_name = request.form.get('last_name', '')
            dob = request.form.get('dob', '')
            address = request.form.get('address', '')
            citizen_id = request.form.get('citizen_id', '')
            healthcare = request.form.get('healthcare', '')

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO patients (hn, first_name, last_name, dob, address, citizen_id, healthcare)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (hn, first_name, last_name, dob, address, citizen_id, healthcare))
                conn.commit()

            flash("เพิ่มผู้ป่วยเรียบร้อยแล้ว", "success")
            return redirect(url_for('patients'))
        except Exception as e:
            return f"Error adding patient: {e}", 500

    return render_template('add_patient.html')

# ---------- INITIALIZE DATABASE ON STARTUP ----------
with app.app_context():
    init_db()

# ---------- STARTUP ----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
