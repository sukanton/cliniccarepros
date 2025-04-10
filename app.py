from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("clinic.db") as conn:
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

@app.route('/')
def index():
    return redirect(url_for('patients'))

@app.route('/patients')
def patients():
    with sqlite3.connect("clinic.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients")
        rows = cur.fetchall()
    return render_template('patients.html', patients=rows)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        hn = request.form['hn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        address = request.form['address']
        citizen_id = request.form['citizen_id']
        healthcare = request.form['healthcare']

        with sqlite3.connect("clinic.db") as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO patients (hn, first_name, last_name, dob, address, citizen_id, healthcare)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (hn, first_name, last_name, dob, address, citizen_id, healthcare))
            conn.commit()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
