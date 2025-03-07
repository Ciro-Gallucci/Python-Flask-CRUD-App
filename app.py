from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome
import logging
import time
import os
import MySQLdb

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash_message'

# Configurazione database tramite variabili d'ambiente
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'user')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'students_db')

mysql = MySQL(app)

def wait_for_db():
    """Attende che il database sia pronto prima di avviare Flask."""
    retries = 10
    while retries > 0:
        try:
            conn = MySQLdb.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                passwd=app.config['MYSQL_PASSWORD'],
                db=app.config['MYSQL_DB'],
                charset="utf8mb4"
            )
            conn.ping()
            conn.close()
            print("Database pronto!")
            return True
        except Exception as e:
            print(f"Database non pronto, riprovo... ({retries} tentativi rimanenti) - Errore: {e}")
            time.sleep(5)
            retries -= 1
    print("Database non disponibile, uscita.")
    return False

@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(f"Errore durante il recupero dei dati: {e}")
        logging.error(f"Errore durante il recupero dei dati: {e}")
        return render_template('index.html', students=[])
    
    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not name or not email or not phone:
            flash("Tutti i campi sono obbligatori!")
            return redirect(url_for('index'))

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students(name, email, phone) VALUES(%s, %s, %s)", (name, email, phone))
            mysql.connection.commit()
            cur.close()
            flash("Dati inseriti con successo!")
        except Exception as e:
            flash(f"Errore durante l'inserimento: {e}")
    
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not id_data or not name or not email or not phone:
            flash("Tutti i campi sono
