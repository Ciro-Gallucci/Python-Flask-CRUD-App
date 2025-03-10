from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome
import logging
import time
import MySQLdb

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash message'

'''# Configurazione del database MySQL tramite variabili d'ambiente
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Inserisci la password corretta
app.config['MYSQL_DB'] = 'python_crud'
'''

'''
# Configurazione del database
DB_HOST = "db"  # Deve essere "db", non "localhost"
DB_USER = "user"
DB_PASSWORD = "password"
DB_NAME = "students_db"
'''

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
            conn.ping()  # Test della connessione
            conn.close()
            print("Database pronto!")
            return True
        except Exception as e:
            print(f"Database non pronto, riprovo... ({retries} tentativi rimanenti) - Errore: {e}")
            time.sleep(5)
            retries -= 1
    print("Database non disponibile, uscita.")
    return False

# Funzione per verificare la connessione al database
'''def check_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = MySQLdb.connect(
                host="db",  # Assicurati che sia "db" e non "localhost"
                user="user",
                passwd="password",
                db="students_db"
            )
            conn.ping()  # Test della connessione
            return True
        except Exception as e:
            print(f"Database non pronto, retrying... ({retries} tentativi rimanenti) - Errore: {e}")
            time.sleep(5)
            retries -= 1
    return False'''


@app.route('/')
def index():
    try:
        # Verifica la connessione al database
        if mysql.connection:
            logging.debug("Connessione al database stabilita con successo")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM students")
            data = cur.fetchall()
            cur.close()
        else:
            flash("Errore nella connessione al database!")
            logging.error("Connessione al database fallita!")
            return render_template('index.html', students=[])
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

        # Controlla se la connessione è valida
        if not mysql.connection:
            flash("Errore nella connessione al database!")
            return redirect(url_for('index'))

        try:
            flash("Dati inseriti con successo!")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students(name, email, phone) VALUES(%s, %s, %s)", (name, email, phone))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            flash(f"Errore durante l'inserimento: {e}")
            return redirect(url_for('index'))

        return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == "POST":
        # Validazione dei dati inviati
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not name or not email or not phone:
            flash("Please fill in all fields!")
            return redirect(url_for('index'))

        if not check_db_connection():
            return redirect(url_for('index'))

        try:
            flash("Data Updated Successfully")

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s
                WHERE id=%s
            """, (name, email, phone, id_data))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            flash(f"Errore durante l'aggiornamento dei dati: {str(e)}")
            return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    if not check_db_connection():
        return redirect(url_for('index'))

    try:
        flash("Data Deleted Successfully")

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        flash(f"Errore durante la cancellazione dei dati: {str(e)}")

    return redirect(url_for('index'))


# Configura il logger
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    if wait_for_db():
        print("Database pronto, avvio Flask...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        exit(1) # Se il database non è pronto, il container si ferma


