from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import logging
import time
import MySQLdb

app = Flask(__name__)

app.secret_key = 'flash message'

# Configurazione del database
DB_HOST = "db"
DB_USER = "user"
DB_PASSWORD = "password"
DB_NAME = "students_db"

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
        return render_template('index.html', students=[])

    return render_template('index.html', students=data)

if __name__ == "__main__":
    if wait_for_db():
        print("Database pronto, avvio Flask...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        exit(1)
