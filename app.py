from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome
import logging
import time
import MySQLdb

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash message'

# Configurazione del database da variabili d'ambiente (consigliato)
import os
DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'students_db')

app.config['MYSQL_HOST'] = DB_HOST
app.config['MYSQL_USER'] = DB_USER
app.config['MYSQL_PASSWORD'] = DB_PASSWORD
app.config['MYSQL_DB'] = DB_NAME

mysql = MySQL(app)


def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            conn = MySQLdb.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASSWORD,
                db=DB_NAME,
                charset="utf8mb4"
            )
            conn.ping()  # Test della connessione
            conn.close()
            print("Database pronto!")
            return True
        except Exception as e:
            print(f"Database non pronto, riprovo... ({retries} tentativi rimanenti) - Errore: {e}")
            time.sleep(5)  # Attendere 5 secondi prima di riprovare
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
        data = []

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
            logging.error(f"Errore durante l'inserimento: {e}")

        return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not name or not email or not phone:
            flash("Tutti i campi sono obbligatori!")
            return redirect(url_for('index'))

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s
                WHERE id=%s
            """, (name, email, phone, id_data))
            mysql.connection.commit()
            cur.close()
            flash("Dati aggiornati con successo!")
        except Exception as e:
            flash(f"Errore durante l'aggiornamento: {e}")
            logging.error(f"Errore durante l'aggiornamento: {e}")

    return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
        mysql.connection.commit()
        cur.close()
        flash("Dati eliminati con successo!")
    except Exception as e:
        flash(f"Errore durante la cancellazione: {e}")
        logging.error(f"Errore durante la cancellazione: {e}")

    return redirect(url_for('index'))


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    if wait_for_db():
        print("Database pronto, avvio Flask...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        exit(1)
